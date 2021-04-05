#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

class TMouseEvents():
    def mouseDoubleClickEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse click events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False

    def mouseMoveEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse move events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False

    def mouseDragEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse drag events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False

    def mousePressEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse press events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False

    def mouseReleaseEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse release events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False

    def wheelEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse wheel events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False

    def enterEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse enter events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False

    def leaveEvent(self, evt) -> bool :
        '''
        This event handler, can be reimplemented in a subclass to receive mouse leave events for the widget.

        .. note:: Reimplement this function to handle this event

        Args:
            evt ([TermTk.libbpytop.input.MouseEvent]): the mouse event
        Returns:
            bool: True if the event has been handled
        '''
        return False
