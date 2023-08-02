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

import sys, os, argparse

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


def demoMessageBox(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    # winFP = ttk.TTkWindow(parent=frame,pos = (0,0), size=(20,10), title="Test File Pickers", border=True)
    btn1 = ttk.TTkButton(parent=frame, pos=(0,0),  border=True, text='Open' )
    title = ttk.TTkTextPicker(parent=frame, pos=(0,3),size=(20,1), text='Test Messagebox', multiLine=False)
    icon = ttk.TTkComboBox(parent=frame,pos=(0,4), size=(20,1), list=['NoIcon','Question','Information','Warning','Critical'],index=3)
    frameList = ttk.TTkFrame(parent=frame, title='Buttons',pos=(0,5), size=(20,15), layout=ttk.TTkGridLayout())
    listWidgetMulti = ttk.TTkList(parent=frameList, selectionMode=ttk.TTkK.MultiSelection)
    for name, val in [
            ('Ok',              ttk.TTkMessageBox.StandardButton.Ok),
            ('Open',            ttk.TTkMessageBox.StandardButton.Open),
            ('Save',            ttk.TTkMessageBox.StandardButton.Save),
            ('Cancel',          ttk.TTkMessageBox.StandardButton.Cancel),
            ('Close',           ttk.TTkMessageBox.StandardButton.Close),
            ('Discard',         ttk.TTkMessageBox.StandardButton.Discard),
            ('Apply',           ttk.TTkMessageBox.StandardButton.Apply),
            ('Reset',           ttk.TTkMessageBox.StandardButton.Reset),
            ('RestoreDefaults', ttk.TTkMessageBox.StandardButton.RestoreDefaults),
            ('Help',            ttk.TTkMessageBox.StandardButton.Help),
            ('SaveAll',         ttk.TTkMessageBox.StandardButton.SaveAll),
            ('Yes',             ttk.TTkMessageBox.StandardButton.Yes),
            ('YesToAll',        ttk.TTkMessageBox.StandardButton.YesToAll),
            ('No',              ttk.TTkMessageBox.StandardButton.No),
            ('NoToAll',         ttk.TTkMessageBox.StandardButton.NoToAll),
            ('Abort',           ttk.TTkMessageBox.StandardButton.Abort),
            ('Retry',           ttk.TTkMessageBox.StandardButton.Retry),
            ('Ignore',          ttk.TTkMessageBox.StandardButton.Ignore),
            ('NoButton',        ttk.TTkMessageBox.StandardButton.NoButton)]:
        listWidgetMulti.addItem(name,val)

    label = ttk.TTkLabel(parent=frame,  pos=(22,0),  text="...")
    text = ttk.TTkTextPicker(parent=frame, pos=(22,1),size=(35,1), autoSize=True, text='Text ln1\nText ln2 😻')

    ttk.pyTTkSlot(ttk.TTkMessageBox.StandardButton)
    def _buttonSelected(btn):
        buttonName = {
            ttk.TTkMessageBox.StandardButton.Ok : 'Ok',
            ttk.TTkMessageBox.StandardButton.Open : 'Open',
            ttk.TTkMessageBox.StandardButton.Save : 'Save',
            ttk.TTkMessageBox.StandardButton.Cancel : 'Cancel',
            ttk.TTkMessageBox.StandardButton.Close : 'Close',
            ttk.TTkMessageBox.StandardButton.Discard : 'Discard',
            ttk.TTkMessageBox.StandardButton.Apply : 'Apply',
            ttk.TTkMessageBox.StandardButton.Reset : 'Reset',
            ttk.TTkMessageBox.StandardButton.RestoreDefaults : 'RestoreDefaults',
            ttk.TTkMessageBox.StandardButton.Help : 'Help',
            ttk.TTkMessageBox.StandardButton.SaveAll : 'SaveAll',
            ttk.TTkMessageBox.StandardButton.Yes : 'Yes',
            ttk.TTkMessageBox.StandardButton.YesToAll : 'YesToAll',
            ttk.TTkMessageBox.StandardButton.No : 'No',
            ttk.TTkMessageBox.StandardButton.NoToAll : 'NoToAll',
            ttk.TTkMessageBox.StandardButton.Abort : 'Abort',
            ttk.TTkMessageBox.StandardButton.Retry : 'Retry',
            ttk.TTkMessageBox.StandardButton.Ignore : 'Ignore',
            ttk.TTkMessageBox.StandardButton.NoButton : 'NoButton'}.get(btn,"???")
        label.setText(f"Selected: {buttonName}")

    def _showDialog():
        iconVal = {
            'NoIcon':ttk.TTkMessageBox.Icon.NoIcon,
            'Question':ttk.TTkMessageBox.Icon.Question,
            'Information':ttk.TTkMessageBox.Icon.Information,
            'Warning':ttk.TTkMessageBox.Icon.Warning,
            'Critical':ttk.TTkMessageBox.Icon.Critical}.get(icon.currentText(),ttk.TTkMessageBox.Icon.NoIcon)
        buttons = sum([item.data() for item in listWidgetMulti.selectedItems()])
        messageBox = ttk.TTkMessageBox(
                title=title.getTTkString(),
                text=text.getTTkString(),
                icon=iconVal,
                standardButtons=buttons)
        messageBox.buttonSelected.connect(_buttonSelected)
        ttk.TTkHelper.overlay(btn1, messageBox, 2, 1, True)

    btn1.clicked.connect(_showDialog)

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

    root = ttk.TTk()
    if args.f:
        root.setLayout(ttk.TTkGridLayout())
        winColor1 = root
    else:
        winColor1 = ttk.TTkWindow(parent=root,pos = (0,0), size=(60,25), title="Test File/Folder Picker", border=True, layout=ttk.TTkGridLayout())

    demoMessageBox(winColor1)

    root.mainloop()

if __name__ == "__main__":
    main()