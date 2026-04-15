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
from .text_wrap_data import _WrapLine, _ReWrapData, _WrapState

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

_WRAP_CHUNK_SIZE: Final[int] = 128

@dataclass
class _WrapChunk():
    id: int
    y: int
    first_line: int
    size: int
    buffer: List[_WrapLine]

class _WrapEngine_FastWrap(_WrapEngine_Interface):
    '''Placeholder for a future incremental/chunk-based wrap engine.

    This class intentionally delegates behavior to
    :py:class:`_WrapEngine_Interface` until a dedicated fast implementation
    is introduced.
    '''
    __slots__ = ('_chunks', '_chunksLock')

    _chunks: List[_WrapChunk]

    def __init__(self, state:_WrapState):
        self._chunks = []
        self._chunksLock = RLock()
        super().__init__(state)

    def size(self) -> int:
        with self._chunksLock:
            chunks = self._chunks
            num_all_lines = self._wrapState.textDocument.lineCount()
            if not chunks:
                return num_all_lines
            num_valid_chunks = len(chunks)
            num_all_chunks = math.ceil(num_all_lines / _WRAP_CHUNK_SIZE)
            chunks_size = sum(len(_c.buffer) for _c in chunks)
            estimated_size = num_all_chunks * chunks_size / num_valid_chunks
            return estimated_size

    def rewrap(self, data: Optional[_ReWrapData]=None) -> None:
        if not (w := self._wrapState.size):
            return
        with self._chunksLock:
            num_of_chunks = math.ceil(self._wrapState.textDocument.lineCount() / _WRAP_CHUNK_SIZE)
            if isinstance(data, _ReWrapData):
                # TODO: improve this with a partial reconstruction of the affected chunk
                line = data.line
                chunk = math.floor(line / _WRAP_CHUNK_SIZE)
                self._chunks = self._chunks[chunk:]
            else:
                self._chunks = []

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        return 0, 0

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        return 0, 0

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        return 0, 0

    def screenRows(self, y:int, h:int) -> List[_WrapLine]:
        with self._chunksLock:
            ret: List[_WrapChunk] = []
            for chunk in self._get_chunks_from_range(y,y+h):
                lo = max(0,y-chunk.y)
                hi = min(chunk.size,y+h-chunk.y)
                ret.extend(chunk.buffer[lo:hi])
            return ret

    def _find_next_chunk_index_to_screen_position(self, y:int) -> int:
        chunk_id = bisect_left(self._chunks, y, key=lambda _ch:_ch.y)
        return chunk_id

    def _find_next_chunk_index_to_line(self, line:int) -> int:
        chunk_id = bisect_left(self._chunks, line, key=lambda _ch:_ch.first_line)
        return chunk_id

    def _get_chunk_from_position(self, y:int) -> _WrapChunk:
        with self._chunksLock:
            chunk_index = self._find_next_chunk_index_to_line(y)

            if not chunk_index:
                estimated_chunk_id = math.floor(y/_WRAP_CHUNK_SIZE)
                chunk = self._makeChunk(chunk_logical_id=estimated_chunk_id, y=y)
                self._chunks = [chunk]
                return chunk

            chunk = self._chunks[chunk_index-1]
            if chunk.y < y < chunk.y + chunk.size:
                # Chunk hit
                return chunk

            self._chunks = self._chunks[:chunk_index]
            top_chunk= self._chunks[-1]
            top_chunk_id = top_chunk.id
            last_y_position = top_chunk.y + top_chunk.size

            if y < last_y_position + _WRAP_CHUNK_SIZE:
                # The y position surely fits the next chunk
                chunk = self._makeChunk(chunk_logical_id=top_chunk_id+1, y=last_y_position)
                self._chunks.append(chunk)
                return chunk

            estimated_chunk_id = top_chunk_id + math.floor((y-last_y_position) / _WRAP_CHUNK_SIZE)
            chunk = self._makeChunk(chunk_logical_id=estimated_chunk_id, y=y)
            self._chunks.append(chunk)
            return chunk

    def _get_chunks_from_range(self, y_start:int, y_stop:int) -> List[_WrapChunk]:
        ret: List[_WrapChunk] = []
        with self._chunksLock:
            y = y_start
            while y < y_stop:
                chunk = self._get_chunk_from_position(y)
                ret.append(chunk)
                y = chunk.y + chunk.size
            return ret

    def _makeChunk(self, chunk_logical_id: int, y: int) -> _WrapChunk:
        if not (w := self._wrapState.size):
            return
        line = chunk_logical_id * _WRAP_CHUNK_SIZE
        buffer: List[_WrapLine] = []
        for i,l in enumerate(self._wrapState.textDocument.dataLines(slice(line, line+_WRAP_CHUNK_SIZE)), start=y):
            buffer.extend(self._wrapLine(w,i,l))
        return _WrapChunk(
            id=chunk_logical_id,
            y=y,
            first_line=line,
            size=len(buffer),
            buffer=buffer
        )
