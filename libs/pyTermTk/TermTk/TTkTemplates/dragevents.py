# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TDragEvents']

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TermTk.TTkGui.drag import TTkDnDEvent
else:
    class TTkDnDEvent(): ...

class TDragEvents():
    def dragEnterEvent(self, evt:TTkDnDEvent) -> bool:
        '''
        This event handler, can be reimplemented in a subclass to receive drag events for the widget.

        .. note:: Reimplement this function to handle this event

        :param evt: The drop event
        :type evt: :py:class:`TTkDnDEvent`

        :return: **True** if the event has been handled
        :rtype: bool
        '''
        return False

    def dragLeaveEvent(self, evt:TTkDnDEvent) -> bool:
        '''
        This event handler, can be reimplemented in a subclass to receive drag events for the widget.

        .. note:: Reimplement this function to handle this event

        .. note:: This event is triggered only if :py:meth:`TDragEvents.dragEnterEvent` or :py:meth:`TDragEvents.dragMoveEvent` were previously handled inside this widget.

        :param evt: The drop event
        :type evt: :py:class:`TTkDnDEvent`

        :return: **True** if the event has been handled
        :rtype: bool
        '''
        return False

    def dragMoveEvent(self, evt:TTkDnDEvent) -> bool:
        '''
        This event handler, can be reimplemented in a subclass to receive drag events for the widget.

        .. note:: Reimplement this function to handle this event

        :param evt: The drop event
        :type evt: :py:class:`TTkDnDEvent`

        :return: **True** if the event has been handled
        :rtype: bool
        '''
        return False

    def dropEvent(self, evt:TTkDnDEvent) -> bool:
        '''
        This event handler, can be reimplemented in a subclass to receive drag events for the widget.

        .. note:: Reimplement this function to handle this event

        :param evt: The drop event
        :type evt: :py:class:`TTkDnDEvent`

        :return: **True** if the event has been handled
        :rtype: bool
        '''
        return False