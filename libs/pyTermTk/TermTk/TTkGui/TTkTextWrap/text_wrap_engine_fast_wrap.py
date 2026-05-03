# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__:list = []

import sys
from dataclasses import dataclass
import math
from threading import RLock
from typing import Final, List, Optional, Tuple


from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _RetScreenPosition, _RetScreenPositions, _RetScreenRows, _WrapLine, _ReWrapData, _WrapState

# TODO: remove Python 3.9 compatibility routine once dropped support
# Python 3.9 compatibility: key parameter was added in Python 3.10
if sys.version_info >= (3, 10):
    from bisect import bisect_left, bisect_right
else:
    from bisect import bisect_left as _bisect_left, bisect_right as _bisect_right
    class _BisectKeyLine:
        __slots__ = ('_buf', '_key')
        _buf:List[_WrapLine]
        def __init__(self, buf:List[_WrapLine], key):
            self._buf = buf
            self._key = key
        def __len__(self) -> int:
            return len(self._buf)
        def __getitem__(self, i) -> int:
            return self._key(self._buf[i])
    def bisect_left(a, x, lo=0, hi=None, *, key=None):
        '''Compatibility wrapper for bisect_left with key parameter support.'''
        if key is None:
            return _bisect_left(a, x, lo, hi if hi is not None else len(a))
        keys = _BisectKeyLine(a, key)
        return _bisect_left(keys, x, lo, hi if hi is not None else len(a))

    def bisect_right(a, x, lo=0, hi=None, *, key=None):
        '''Compatibility wrapper for bisect_right with key parameter support.'''
        if key is None:
            return _bisect_right(a, x, lo, hi if hi is not None else len(a))
        keys = _BisectKeyLine(a, key)
        return _bisect_right(keys, x, lo, hi if hi is not None else len(a))

_WRAP_CHUNK_LINES: Final[int] = 128

@dataclass
class _WrapChunk():
    '''A lazily-computed block of wrapped rows for a contiguous range of document lines.

    :param id: logical chunk index (``first_line // _WRAP_CHUNK_LINES``).
    :type id: int
    :param y: screen row where this chunk starts.
    :type y: int
    :param first_line: first document line covered by this chunk.
    :type first_line: int
    :param last_line: last document line covered by this chunk.
    :type last_line: int
    :param size: total number of wrapped rows in :py:attr:`buffer`.
    :type size: int
    :param buffer: wrapped row fragments produced by :py:meth:`_WrapEngine_Interface._wrapLine`.
    :type buffer: List[:py:class:`_WrapLine`]
    '''
    id: int
    y: int
    first_line: int
    last_line: int
    size: int
    buffer: List[_WrapLine]

class _WrapEngine_FastWrap(_WrapEngine_Interface):
    '''Chunk-based lazy wrap engine optimized for large documents.

    Instead of wrapping every document line upfront (like
    :py:class:`_WrapEngine_FullWrap`), this engine divides the document into
    fixed-size chunks of ``_WRAP_CHUNK_LINES`` lines and wraps them on demand
    when a screen region is queried via :py:meth:`screenRows`.

    Chunks are cached in a sorted list keyed by screen position (``y``) so
    that repeated queries for the same viewport don't re-wrap.  Coordinate
    conversions (:py:meth:`dataToScreenPosition`, :py:meth:`screenToDataPosition`,
    :py:meth:`normalizeScreenPosition`) are wrap-accurate for cached chunks
    and fall back to unwrapped line semantics for uncached regions.

    Thread Safety: All chunk list operations are protected with an RLock mutex.
    '''
    __slots__ = ('_chunks', '_chunksLock', '_chunksSize')

    _chunks: List[_WrapChunk]
    _chunksSize: int


    def __init__(self, state:_WrapState):
        self._chunks = []
        self._chunksLock = RLock()
        self._chunksSize = 0
        super().__init__(state)


    def size(self) -> int:
        '''Return an estimated total number of wrapped screen rows.

        When no chunks have been materialized yet, falls back to the raw
        document line count.  Otherwise extrapolates from the average
        wrapped rows per chunk.

        :return: estimated wrapped row count.
        :rtype: int
        '''
        with self._chunksLock:
            num_all_lines = self._wrapState.textDocument.lineCount()
            chunks = self._chunks
            if not chunks:
                return num_all_lines
            last_chunk = chunks[-1]
            last_line = last_chunk.last_line
            unprocessed_tail_lines = num_all_lines - last_line
            average_chunk_size = sum(_c.size for _c in chunks) // len(chunks)
            return last_chunk.y + last_chunk.size + average_chunk_size * unprocessed_tail_lines // _WRAP_CHUNK_LINES


    def rewrap(self, data: Optional[_ReWrapData]=None) -> None:
        '''Invalidate cached chunks affected by a document change.

        For incremental edits, only chunks at or after the changed line are
        discarded; earlier chunks remain valid.  For a full rewrap (no *data*),
        the entire chunk cache is cleared.

        :param data: optional incremental change descriptor.
        :type data: Optional[:py:class:`_ReWrapData`]
        '''
        if not (w := self._wrapState.size):
            return
        with self._chunksLock:
            self._chunksSize = 0
            num_all_lines = self._wrapState.textDocument.lineCount()
            num_ids = num_all_lines // _WRAP_CHUNK_LINES
            if num_ids > 6:
                if isinstance(data, _ReWrapData):
                    line = data.line
                    first_chunk_id = line // _WRAP_CHUNK_LINES
                    idx = bisect_left(self._chunks, first_chunk_id, key=lambda _ch: _ch.id)
                    self._chunks = self._chunks[:idx]
                    self._chunksSize = sum(_c.size for _c in self._chunks)
                else:
                    first_chunk_id = 0
                    self._chunks = []

                if not self._makeChunk_and_prev(chunk_logical_id=first_chunk_id, y=0):
                    return

                last_id = num_ids
                last_estimated_y = last_id * self._chunksSize // len(self._chunks)
                if not self._makeChunk_and_prev(chunk_logical_id=last_id, y=last_estimated_y):
                    return
                self._align_chunks()
            else:
                self._chunks = []
                pos_y = 0
                for id in range(num_ids):
                    if not (chunk := self._makeChunk_and_prev(chunk_logical_id=id, y=pos_y)):
                        return
                    pos_y += chunk.size


    def dataToScreenPosition(self, line:int, pos:int) -> _RetScreenPositions:
        '''Map document coordinates to wrapped screen coordinates.

        The target chunk is materialized on demand when missing, so the
        mapping is wrap-accurate for valid document positions.

        :param line: source line index.
        :type line: int
        :param pos: character offset within the source line.
        :type pos: int

        :return: wrapped screen coordinates and optional extra position.
        :rtype: :py:class:`_RetScreenPositions`
        '''
        text_document = self._wrapState.textDocument
        chunkId = line // _WRAP_CHUNK_LINES
        chunk:Optional[_WrapChunk] = None
        with self._chunksLock:
            # bisect by first_line to find the chunk whose range covers 'line'
            idx = bisect_right(self._chunks, chunkId, key=lambda _ch: _ch.id)
            if self._chunks and 0 < idx <= len(self._chunks):
                chunk = self._chunks[idx-1]
            if not chunk or chunk.id != chunkId:
                # Chunk not cached — materialise it from the document line position.
                estimated_chunk_size = self._chunksSize // len(self._chunks) if self._chunks else _WRAP_CHUNK_LINES
                estimated_chunk_y = estimated_chunk_size * chunkId
                chunk = self._makeChunk_and_prev(chunk_logical_id=chunkId, y=estimated_chunk_y)
                if chunk:
                    self._align_chunks()

        if chunk:
            data_line = text_document.dataLine(line)
            if data_line is None:
                data_line = text_document.dataLine(chunk.buffer[-1].line)
                pos = data_line.termWidth() if data_line else 0
                x, y = pos, chunk.y + len(chunk.buffer) -1
                return _RetScreenPositions(main=_RetScreenPosition(x=x,y=y))
            for bi, row in enumerate(chunk.buffer):
                if row.line == line:
                    if row.start <= pos <= row.stop:
                        # Compute the screen column from the fragment start to pos
                        l = data_line.substring(row.start, pos).tab2spaces(self._wrapState.tabSpaces)
                        x, y = l.termWidth(), chunk.y + bi
                        extra = None
                        # Check if this is the end of the line and the beginning of the next one
                        if pos == row.stop and bi < chunk.size - 1 and chunk.buffer[bi+1].line == line:
                            extra = _RetScreenPosition(x=0,y=y+1)
                        return _RetScreenPositions(main=_RetScreenPosition(x=x,y=y), extra=extra)
                    if row.last_slice and pos > row.stop:
                        # Compute the screen column from the fragment start to pos
                        l = data_line.substring(row.start, row.stop).tab2spaces(self._wrapState.tabSpaces)
                        x, y = l.termWidth(), chunk.y + bi
                        return _RetScreenPositions(main=_RetScreenPosition(x=x,y=y))

        return _RetScreenPositions(main=_RetScreenPosition(x=0,y=0))


    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Map wrapped screen coordinates back to source document coordinates.

        Chunks are materialized on demand to preserve wrap-accurate mapping.
        Out-of-range positions are clamped to safe defaults.

        :param x: horizontal screen coordinate (terminal cells).
        :type x: int
        :param y: vertical screen coordinate (wrapped row index).
        :type y: int

        :return: ``(line, pos)`` source document coordinates.
        :rtype: Tuple[int, int]
        '''
        if y < 0:
            return 0,0
        text_document = self._wrapState.textDocument
        with self._chunksLock:
            if not (chunk := self._get_chunk_from_position(y)) and self._chunks:
                document_size = text_document.lineCount()
                return document_size-1, 0

            dy = y - chunk.y
            if 0 <= dy < chunk.size:
                dy = min(dy, len(chunk.buffer) - 1)
                row = chunk.buffer[dy]
                dt = row.line
                fr = row.start
                to = row.stop
                data_line = text_document.dataLine(dt)
                if data_line is None:
                    return 0, 0
                # Convert screen column to character offset within the fragment
                pos = fr + data_line.substring(fr, to).tabCharPos(x, self._wrapState.tabSpaces)
                return dt, pos

        return 0,0


    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Snap a screen coordinate to the nearest valid character cell.

        Clamps *y* to the valid range and adjusts *x* to land on a real
        character boundary (respecting tab expansion and wide characters).
        Wrap-accurate for cached or newly materialized chunks, with a
        line-based fallback when no wrapped chunk can be resolved.

        :param x: horizontal screen coordinate.
        :type x: int
        :param y: vertical screen coordinate.
        :type y: int

        :return: normalized ``(x, y)``.
        :rtype: Tuple[int, int]
        '''
        x = max(0, x)
        text_document = self._wrapState.textDocument
        with self._chunksLock:
            idx = bisect_right(self._chunks, y, key=lambda _ch: _ch.y)
            if idx > 0:
                chunk = self._chunks[idx - 1]
                dy = y - chunk.y
                if 0 <= dy < chunk.size:
                    dy = min(dy, len(chunk.buffer) - 1)
                    row = chunk.buffer[dy]
                    dt = row.line
                    fr = row.start
                    to = row.stop
                    data_line = text_document.dataLine(dt)
                    if data_line is None:
                        return 0, 0
                    # Round-trip: screen col -> char offset -> back to screen col
                    s = data_line.substring(fr, to)
                    x = s.tabCharPos(x, self._wrapState.tabSpaces)
                    x = s.substring(0, x).tab2spaces(self._wrapState.tabSpaces).termWidth()
                    return x, y
        # Fallback: unwrapped line semantics
        y = self._clampLine(y)
        data_line = text_document.dataLine(y)
        if data_line is None:
            return 0, 0
        x = data_line.tabCharPos(x, self._wrapState.tabSpaces)
        x = data_line.substring(0, x).tab2spaces(self._wrapState.tabSpaces).termWidth()
        return x, y


    def screenRows(self, y:int, h:int) -> _RetScreenRows:
        '''Return wrapped row fragments for a viewport region.

        Materializes any chunks that overlap ``[y, y+h)`` on demand and
        slices the relevant rows from each chunk's buffer.

        :param y: first screen row of the viewport.
        :type y: int
        :param h: number of rows to retrieve.
        :type h: int

        :return: wrapped row descriptors covering the viewport.
        :rtype: :py:class:`_RetScreenRows`
        '''
        with self._chunksLock:
            ret: List[_WrapLine] = []
            chunks, delta = self._get_chunks_from_range(y,y+h)
            y+=delta
            for chunk in chunks:
                dy = y - chunk.y
                lo = max(0,dy)
                hi = dy+h
                ret.extend(chunk.buffer[lo:hi])
            return _RetScreenRows(rows=ret)

    def _find_next_chunk_index_to_screen_position(self, y:int) -> int:
        chunk_id = bisect_left(self._chunks, y, key=lambda _ch:_ch.y)
        return chunk_id

    def _find_next_chunk_index_to_line(self, line:int) -> int:
        chunk_id = bisect_left(self._chunks, line, key=lambda _ch:_ch.first_line)
        return chunk_id

    def _shift_chunks_y(self, start_index:int, delta_y:int) -> None:
        '''Shift cached chunk screen positions by ``delta_y`` from ``start_index`` onward.'''
        if delta_y == 0:
            return
        for _ch in self._chunks[start_index:]:
            _ch.y += delta_y

    def _reflow_following_chunks(self, start_index:int) -> None:
        '''Ensure following chunks never overlap previous ones while preserving gaps.'''
        if start_index <= 0:
            start_index = 1
        for _i in range(start_index, len(self._chunks)):
            _prev = self._chunks[_i-1]
            _cur = self._chunks[_i]
            _min_y = _prev.y + _prev.size
            if _cur.y < _min_y:
                _cur.y = _min_y

    def _align_chunks(self) -> None:
        '''Realign chunk screen offsets after insertion/replacement.

        Recompute every following chunk ``y`` from the first cached chunk so
        chunks remain monotonic and preserve logical-id gaps as virtual
        unwrapped space.
        '''
        if not self._chunks:
            return
        estimated_chunk_size = _WRAP_CHUNK_LINES if not self._chunks else self._chunksSize // len(self._chunks)
        last_chunk = self._chunks[0]
        for chunk in self._chunks[1:]:
            id = chunk.id
            last_id = last_chunk.id
            chunk.y = last_chunk.y + last_chunk.size + (id - last_id -1) * estimated_chunk_size
            last_chunk = chunk


    def _get_chunk_from_position(self, y:int) -> Optional[_WrapChunk]:
        '''Retrieve or create the chunk containing screen row *y*.

        Lookup strategy (all operations happen while holding ``_chunksLock``):

          1. Binary-search the chunk list for the rightmost chunk starting at
              or before *y*.
          2. If *y* falls inside that chunk, return it (cache hit).
          3. If *y* is before the first known chunk, create an estimated chunk
              anchored at *y* and realign all following chunks.
          4. If *y* is after the last known chunk, append a new chunk and keep
              it anchored at *y* (no trailing chunks to realign).
          5. If *y* falls in a gap between chunks, estimate a logical id using
              distance from the previous chunk and insert there.
          6. If the estimate would collide with the next chunk id, drop the
              stale tail and rebuild lazily from the inserted point.

        :param y: target screen row.
        :type y: int

        :return: the chunk covering *y*.
        :rtype: :py:class:`_WrapChunk`
        '''
        with self._chunksLock:
            estimated_chunk_size = _WRAP_CHUNK_LINES if not self._chunks else self._chunksSize // len(self._chunks)
            number_of_active_chunks = len(self._chunks)
            # Find rightmost chunk with .y <= y
            chunk_index = bisect_right(self._chunks, y, key=lambda _ch: _ch.y)

            if chunk_index > 0:
                chunk = self._chunks[chunk_index-1]
                if y < chunk.y + chunk.size:
                    # Cache hit: y is inside this chunk
                    return chunk

            if chunk_index == 0:
                # y is before the first cached chunk (or cache is empty):
                # bootstrap/insert and then realign every following chunk.
                estimated_chunk_id = y // estimated_chunk_size
                if not (chunk_head := self._makeChunk_and_prev(chunk_logical_id=estimated_chunk_id, y=y)):
                    return None
                self._align_chunks()
                return chunk_head
            elif chunk_index == number_of_active_chunks:
                # y is beyond the current tail: append a forward chunk.
                # Keep the chunk anchored at y to avoid unnecessary reflow.
                last_chunk = self._chunks[-1]
                last_y = last_chunk.y + last_chunk.size
                estimated_chunk_id = last_chunk.id + 1 + max(0, (y - last_y) // estimated_chunk_size )
                if not (chunk_tail := self._makeChunk_and_prev(chunk_logical_id=estimated_chunk_id, y=y)):
                    return None
                return chunk_tail
            else:
                # y falls between 2 cached chunks.
                # Insert a newly estimated chunk and repair the tail ordering.
                prev_chunk = self._chunks[chunk_index-1]
                next_chunk = self._chunks[chunk_index]
                prev_last_y = prev_chunk.y + prev_chunk.size
                estimated_chunk_id = prev_chunk.id + 1 +max(0, (y - prev_last_y) // estimated_chunk_size )
                if estimated_chunk_id >= next_chunk.id:
                    # Tail is inconsistent with the new estimate. Drop it and
                    # rebuild lazily so logical ids remain strictly increasing.
                    self._chunks = self._chunks[:chunk_index]
                    self._chunksSize = sum(_c.size for _c in self._chunks)
                if not (chunk_mid := self._makeChunk_and_prev(chunk_logical_id=estimated_chunk_id, y=y)):
                    return None
                self._align_chunks()
                return chunk_mid


    def _get_chunks_from_range(self, y_start:int, y_stop:int) -> Tuple[List[_WrapChunk],int]:
        '''Return all chunks that overlap the screen range ``[y_start, y_stop)``.

        Iterates forward from *y_start*, materializing chunks as needed,
        until the covered screen area reaches *y_stop*.

        :param y_start: first screen row.
        :type y_start: int
        :param y_stop: exclusive end screen row.
        :type y_stop: int

        :return: ordered list of overlapping chunks and the applied y offset.
        :rtype: Tuple[List[:py:class:`_WrapChunk`], int]
        '''
        ret: List[_WrapChunk] = []
        y_start_new = max(0, y_start)
        y_stop_new = y_stop+_WRAP_CHUNK_LINES
        with self._chunksLock:
            y = y_start_new
            while y < y_stop_new:
                if not (chunk := self._get_chunk_from_position(y)):
                    break
                if chunk is None or chunk.size == 0:
                    # Past the end of the document — nothing left to wrap
                    break
                if ( y_start < chunk.y+chunk.size and
                     y_stop >= chunk.y ):
                    ret.append(chunk)
                # Advance past this chunk to the next uncovered screen row
                y = chunk.y + chunk.size
            return ret, 0


    def _makeChunk_and_prev(self, chunk_logical_id: int, y: int) -> Optional[_WrapChunk]:
        '''Wrap the chunk at *chunk_logical_id* and, if missing, also its predecessor.

        The predecessor's screen position is back-calculated so that it ends
        exactly where the requested chunk begins.  If the predecessor is
        already cached the requested chunk is aligned to its tail instead.

        :param chunk_logical_id: logical index of the chunk to create.
        :type chunk_logical_id: int
        :param y: estimated screen row for the requested chunk (used when no
            predecessor is cached).
        :type y: int

        :return: the newly created chunk at *chunk_logical_id*, or ``None``
            if the wrap width is zero or the id is out of range.
        :rtype: Optional[:py:class:`_WrapChunk`]
        '''
        prev_id = chunk_logical_id - 1
        if prev_id >= 0:
            # Check whether the predecessor is already cached.
            idx = bisect_right(self._chunks, prev_id, key=lambda _ch: _ch.id)
            prev_chunk = self._chunks[idx - 1] if idx > 0 else None
            if prev_chunk is None or prev_chunk.id != prev_id:
                # Predecessor is missing — wrap it first with a placeholder y.
                prev_chunk = self._makeChunk(chunk_logical_id=prev_id, y=0)
                if prev_chunk is not None:
                    # Back-calculate its real screen position so it ends at y.
                    prev_chunk.y = max(0, y - prev_chunk.size)
                    ins = idx
                    self._chunks.insert(ins, prev_chunk)
                    self._chunksSize += prev_chunk.size
            # Align the requested chunk to immediately follow the predecessor.
            if prev_chunk is not None:
                y = prev_chunk.y + prev_chunk.size
        chunk = self._makeChunk(chunk_logical_id=chunk_logical_id, y=y)
        if chunk is not None:
            ins = bisect_right(self._chunks, chunk_logical_id, key=lambda _ch: _ch.id)
            self._chunks.insert(ins, chunk)
            self._chunksSize += chunk.size
        return chunk


    def _makeChunk(self, chunk_logical_id: int, y: int) -> Optional[_WrapChunk]:
        '''Wrap a block of document lines into a new :py:class:`_WrapChunk`.

        Reads ``_WRAP_CHUNK_LINES`` document lines starting at
        ``chunk_logical_id * _WRAP_CHUNK_LINES`` and wraps each one.
        The resulting wrapped rows are stored in the chunk buffer,
        anchored at screen row *y*.

        :param chunk_logical_id: chunk index (``first_line // _WRAP_CHUNK_LINES``).
        :type chunk_logical_id: int
        :param y: screen row where this chunk should start.
        :type y: int

        :return: a fully wrapped chunk, or ``None`` if the wrap width is zero.
        :rtype: Optional[:py:class:`_WrapChunk`]
        '''
        if not (w := self._wrapState.size):
            return None
        line = chunk_logical_id * _WRAP_CHUNK_LINES
        num_lines = self._wrapState.textDocument.lineCount()
        # Past the end of the document — return an empty chunk
        if line >= num_lines:
            return None
        buffer: List[_WrapLine] = []
        # enumerate with start=line so _wrapLine receives the document line index
        for i,l in enumerate(self._wrapState.textDocument.dataLines(slice(line, line+_WRAP_CHUNK_LINES)), start=line):
            buffer.extend(self._wrapLine(w,i,l))
        return _WrapChunk(
            id=chunk_logical_id,
            y=y,
            first_line=line,
            last_line=i,
            size=len(buffer),
            buffer=buffer
        )
