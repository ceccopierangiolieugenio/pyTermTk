# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TextDocumentHighlight']

from pygments import highlight
from pygments.util import ClassNotFound
from pygments.styles import get_all_styles
from pygments.lexers import guess_lexer, guess_lexer_for_filename, get_lexer_by_name, special, get_all_lexers
from pygments.formatters import TerminalFormatter, Terminal256Formatter, TerminalTrueColorFormatter
from pygments.formatter import Formatter
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Whitespace

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.timer import TTkTimer

from TermTk.TTkGui.textdocument import TTkTextDocument

class _TTkFormatter(Formatter):
    class Data():
        __slots__=('lines', 'block', 'error', 'multiline')
        def __init__(self, lines, block):
            self.lines = lines
            self.block = block
            self.error = None
            self.multiline = False

    __slots__ = ('_dl', '_blockNum', '_highlightStyles', '_defaultColor')
    def __init__(self, *args, **kwargs):
        self._defaultColor = TTkColor.RST
        super().__init__(*args, **kwargs)
        self._highlightStyles = {}
        self._blockNum = 1
        for token, style in self.style:
            # Token = Token.Comment.PreprocFile
            # style = {
            #   'color': '6272a4',
            #   'bgcolor': None,
            #   'bold': False, 'italic': False, 'underline': False,
            #   'border': None,
            #   'roman': None, 'sans': None, 'mono': None,
            #   'ansicolor': None, 'bgansicolor': None}

            # TTkLog.debug(f"{token=} {style=}")
            color = TTkColor.RST
            if style['color']:
                color += TTkColor.fg(f"#{style['color']}")
            if style['bgcolor']:
                color += TTkColor.bg(f"#{style['bgcolor']}")
            if style['bold']:
                color += TTkColor.BOLD
            if style['italic']:
                color += TTkColor.ITALIC
            if style['underline']:
                color += TTkColor.UNDERLINE
            self._highlightStyles[token] = color

    def setDl(self,dl):
        self._dl = dl

    def setDefaultColor(self, color:TTkColor) -> None:
        self._defaultColor = color

    def format(self, tokensource, _):
        multiline = False
        multilineId = 0
        for ttype, value in tokensource:
            if ttype == Error and self._dl.error is None:
                self._dl.error = len(self._dl.lines)-1
            # self._dl.multiline = ttype == Comment.Multiline
            multiline = ttype == Comment.Multiline

            while ttype not in self._highlightStyles:
                ttype = ttype.parent
            # TTkLog.debug (f"{ttype=}")
            # TTkLog.debug (f"{value=}")
            color:TTkColor = self._highlightStyles[ttype]
            if not color.hasForeground():
               color += self._defaultColor

            values = value.split('\n')

            self._dl.lines[-1] += TTkString(values[0],color)
            self._dl.lines += [TTkString(t,color) for t in values[1:]]
            self._dl.block[-1] = self._blockNum
            self._dl.block += [self._blockNum]*(len(values)-1)

            # self._dl.lines += [TTkString(t) for t in value.split('\n')]

            # multiline = len(values)>1 if self._dl.lines[-1]._text == values[-1] else self._dl.multiline
            # if self._dl.lines[-1]._text == '' or not multiline:
            #     self._blockNum += 1
            #     multilineId = len(self._dl.lines)

            if multiline:
                multilineId += len(values)
            else:
                multilineId = 0
                self._blockNum += 1

        if multiline:
            self._dl.multiline = multilineId

class TextDocumentHighlight(TTkTextDocument):
    _linesRefreshed:int = 30
    __slots__ = (
        '_timerRefresh',
        '_blocks', '_changedContent', '_refreshContent',
        '_lexer', '_formatter',
        '_defaultForegroundColor',
        #Signals
        'highlightUpdate')
    def __init__(self, **kwargs):
        self.highlightUpdate = pyTTkSignal()
        self._lexer = None
        self._blocks = []
        self._defaultForegroundColor = TTkColor.RST
        # self._formatter = _TTkFormatter(style='dracula')
        self._formatter = _TTkFormatter(style='gruvbox-dark')
        super().__init__(**kwargs)
        self._timerRefresh = TTkTimer()
        self._timerRefresh.timeout.connect(self._refreshEvent)
        self._changedContent = (0,0,len(self._dataLines))
        self._refreshContent = (0,TextDocumentHighlight._linesRefreshed)
        # self.contentsChange.connect(lambda a,b,c: TTkLog.debug(f"{a=} {b=} {c=}"))
        self.contentsChange.connect(self._saveChangedContent)

        try:
            self._lexer = guess_lexer(self.toPlainText())
            TTkLog.debug(f"Using Lexer: {self._lexer.name}")
        except ClassNotFound:
            self._lexer = special.TextLexer()

        self._timerRefresh.start(0.3)

    @staticmethod
    def getStyles() -> list[str]:
        return sorted(get_all_styles())

    @staticmethod
    def getLexers() -> list[str]:
        return sorted(list(set(b for a in get_all_lexers() for b in a[1])))

    @pyTTkSlot(str)
    def setStyle(self, alias:str) -> None:
        self._formatter = formatter = _TTkFormatter(style=alias)
        if (color:=formatter.style.background_color) and color != "#000000":
            self._backgroundColor = TTkColor.bg(color)
        else:
            self._backgroundColor = TTkColor.RST

        if self._backgroundColor == TTkColor.RST:
            self._defaultForegroundColor = TTkColor.RST
        else:
            r,g,b = self._backgroundColor.bgToRGB()
            if r+g+b < 127*3:
                self._defaultForegroundColor = TTkColor.WHITE
            else:
                self._defaultForegroundColor = TTkColor.BLACK

        TTkLog.debug(f"{color=} {alias=} {formatter.style}")
        self._changedContent = (0,0,len(self._dataLines))
        self._refreshContent = (0,TextDocumentHighlight._linesRefreshed)
        self._timerRefresh.start(0.3)

    @pyTTkSlot(str)
    def setLexer(self, alias:str) -> None:
        try:
            self._lexer = get_lexer_by_name(alias)
            self._changedContent = (0,0,len(self._dataLines))
            self._refreshContent = (0,TextDocumentHighlight._linesRefreshed)
            self._timerRefresh.start(0.3)
            TTkLog.debug(f"Using Lexer: {self._lexer.name}")
        except ClassNotFound:
            self._lexer = special.TextLexer()

    @pyTTkSlot(str)
    def guessLexerFromFilename(self, fileName:str) -> None:
        with open(fileName, 'r') as f:
            content = f.read()
            try:
                self._lexer = guess_lexer_for_filename(fileName, content)
                TTkLog.debug(f"Using Lexer: {self._lexer.name}")
            except ClassNotFound:
                self._lexer = special.TextLexer()

    @pyTTkSlot(int,int,int)
    def _saveChangedContent(self,a,b,c):
        if self._changedContent:
            self._changedContent = TTkTextDocument._mergeChangesSlices(self._changedContent,(a,b,c))
        else:
            self._changedContent = (a,b,c)
        if not self._refreshContent:
            self._refreshContent = (self._changedContent[0], TextDocumentHighlight._linesRefreshed)
        self._timerRefresh.start(0.1)

    @pyTTkSlot()
    def _refreshEvent(self):
        if not self._refreshContent: return
        self._acquire()

        ra,rb = self._refreshContent

        if self._changedContent:
            ca,cb,cc = self._changedContent
            self._changedContent = None
            self._blocks[ca:ca+cb] = [0]*cc
            ra = min(ra,ca)

        # find the beginning of the current block
        # TTkLog.debug(self._blocks)
        if ra and self._blocks:
            blockId = self._blocks[ra]
            for i,v in enumerate(reversed(self._blocks[:ra])):
                # TTkLog.debug(f"{i=}:{v=} {blockId=}")
                if v == blockId or not blockId:
                    blockId = v
                    ra -= 1
                    rb += 1
                else:
                    break

        # TTkLog.debug(f"{ra=} {rb=}")

        eof = False
        if (ra+rb) >= len(self._dataLines):
            rb  = len(self._dataLines)-ra
            eof=True

        tsl = self._dataLines[ra:ra+rb]
        # Find the offset from the first not empty line
        # because pygments autostrip the heading empty lines
        offset = 0
        for i,l in enumerate(tsl):
            if l != '':
                offset = i
                break

        # TTkLog.debug(f"Refresh {self._lexer.name} {ra=} {rb=}")
        tsl1  = [TTkString()]*(offset+1)
        block = [0]*(offset+1)

        kfd = _TTkFormatter.Data(tsl1, block)
        self._formatter.setDl(kfd)
        self._formatter.setDefaultColor(self._defaultForegroundColor)

        rawl = [l._text for l in tsl[offset:]]
        rawt = '\n'.join(rawl)
        highlight(rawt, self._lexer, self._formatter)

        # for ll in tsl:
        #     TTkLog.debug(f"1: -{ll}-")
        # for ll in tsl1:
        #     TTkLog.debug(f"2: -{ll}-")

        tsl1 = tsl1[:rb]
        block = block[:rb]
        self._dataLines[ra:ra+rb] = tsl1 + tsl[len(tsl1):]
        self._blocks[ra:ra+rb] = block + [-1]*(rb-len(block))
        # TTkLog.debug(self._blocks)

        if kfd.error is not None:
            self._refreshContent = (ra+kfd.error,rb<<1)
            # TTkLog.debug(f"Error: {self._refreshContent=}")
        elif kfd.multiline is not None:
            self._refreshContent = (ra+kfd.multiline,rb<<1)
        elif (ra+rb) < len(self._dataLines):
            self._refreshContent = (ra+rb,TextDocumentHighlight._linesRefreshed)
        else:
            self._refreshContent = None
        # TTkLog.debug(f"{self._refreshContent=}")

        if not eof:
            self._timerRefresh.start(0.03)
        else:
            TTkLog.debug(f"Refresh {self._lexer.name} DONE!!!")

        self._release()
        self.highlightUpdate.emit()
        self.formatChanged.emit()
