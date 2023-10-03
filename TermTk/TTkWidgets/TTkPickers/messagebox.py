# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkMessageBox']

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.signal import pyTTkSignal,pyTTkSlot
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.util import TTkUtil
from TermTk.TTkCore.string import TTkString
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.window import TTkWindow
from TermTk.TTkWidgets.image import TTkImage
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.button import TTkButton

class TTkMessageBox(TTkWindow):
    class Icon(int):
        NoIcon      = 0
        '''the message box does not have any icon.'''
        Question    = 4
        '''an icon indicating that the message is asking a question.'''
        Information = 1
        '''an icon indicating that the message is nothing out of the ordinary.'''
        Warning     = 2
        '''an icon indicating that the message is a warning, but can be dealt with.'''
        Critical    = 3
        '''an icon indicating that the message represents a critical problem.'''

    class StandardButton(int):
        Ok       = 0x00000400
        '''An "OK" button defined with the AcceptRole.'''
        Open     = 0x00002000
        '''An "Open" button defined with the AcceptRole.'''
        Save     = 0x00000800
        '''A "Save" button defined with the AcceptRole.'''
        Cancel   = 0x00400000
        '''A "Cancel" button defined with the RejectRole.'''
        Close    = 0x00200000
        '''A "Close" button defined with the RejectRole.'''
        Discard  = 0x00800000
        '''A "Discard" or "Don't Save" button, depending on the platform, defined with the DestructiveRole.'''
        Apply    = 0x02000000
        '''An "Apply" button defined with the ApplyRole.'''
        Reset    = 0x04000000
        '''A "Reset" button defined with the ResetRole.'''
        RestoreDefaults = 0x08000000
        '''A "Restore Defaults" button defined with the ResetRole.'''
        Help     = 0x01000000
        '''A "Help" button defined with the HelpRole.'''
        SaveAll  = 0x00001000
        '''A "Save All" button defined with the AcceptRole.'''
        Yes      = 0x00004000
        '''A "Yes" button defined with the YesRole.'''
        YesToAll = 0x00008000
        '''A "Yes to All" button defined with the YesRole.'''
        No       = 0x00010000
        '''A "No" button defined with the NoRole.'''
        NoToAll  = 0x00020000
        '''A "No to All" button defined with the NoRole.'''
        Abort    = 0x00040000
        '''An "Abort" button defined with the RejectRole.'''
        Retry    = 0x00080000
        '''A "Retry" button defined with the AcceptRole.'''
        Ignore   = 0x00100000
        '''An "Ignore" button defined with the AcceptRole.'''
        NoButton = 0x00000000
        '''An invalid button.'''

    # Icons from:
    #  /usr/share/icons/mate/16x16/actions
    _compressed_data = {
        Icon.NoIcon : "",
        Icon.Question :
            "eJydlUtsjFEYhusScVuQWFE7I1aWjajLQmrzLtw1EiajzUTjWkJVdUwlY6aKSqZTqpSilGhEpi6rRixYNxYiKmxYVUMpdUla73f8nzmOf6ZGnyZP/jM557zn+885f93E" +
            "5pLJBeZvS2oB/1EgJFIYJ9BzBLoYS7GYLsFKrMjhJaTY6zfbGkfHHcNhO4POXUo20jUCfYRELEdILb2PVNJhbEM5XYZyhHJ4A1lPBzAfAXq84GTQdevc1QJdRQ5Y3ond" +
            "2EFHcRRR+rZAd5N0FnfTXQJdS2pMlgDmeRkmCGwLYSuC9EmcwnHjxpxOIoXTdBsu4jx9g1yj9yKGc8Zx4+1M20K3owOdVmapyzovQxEWoYhtd3HP5P4q0KNkJItH6WHB" +
            "9Ltv1nmBWVrpm6TTcjUaTMY4U7dbdfHekclwmLU5aM09RD7R78kAfRk9eEFfxUP00S14gOd0P38ftPol0YRG+pZAx7w5JUOb1e6XQWur6/tIPlgedJ678Biv6Ed4ijdW" +
            "Px1Hai3vPch9dcZ6Vv9Lhs9kyMc96MVbk+EJXpt6/Wp3M9wRcjiToUz2n28Gqe2wj+u5jmc+7W6GtECv5a5MWs9qzRDKkeGHkIe13wmep3prDrWbQc/FJlL6e09GcIht" +
            "3wV6RPBxFa6g16fdzVDB01hh3Qdupj2szy56luCczW6esrSVRcd27Wb4JiTkHo2a+9Mbm3syiM30ddLx9178467WO0qzaF30HTXjLJroL4JPpks8vXL2CjEXhZmxMZ1M" +
            "y9QcrUJmL/p+L7JZx44jgRj9DgPo99mL2fpPEujVWINVpj4hU598MqhnkhkJ+U7UmZr34aW5s3QfjNVf672cLPvPDOqpZAq9n1SaM9uAY3n0d77t4fDCnx3noWM=" ,
        Icon.Information :
            "eJy1lO1PzWEYx9OpTlI5PZ46lJ5LEdIqIYWIrxcSK6ZUOsNaD1OtrFE2UtMIZabF9IJJy9NGvIpFXhgzzy/YYsy89gf43le/ezvLOcxMV9tnv+vcD9/r4b7aPfryvd3k" +
            "r7Q3if9wU3as9xd6wSQsRTJmkL0ogDc5imKYDXo7+EuRIuv0PlfnTqPdmYYkBAivoVDuespb1pEfMIGD5CdMYpD8ii+4RX7HewyRH3FDfh/GFtGkz/kbDYnGnhGUwI98" +
            "izuoIm/TU0xWoh4h5EqUwYtcxnWe5E5UI5x8iDH0kD+o7jl5F3ZEOZz7Ow06d/3MqTrzFa5iG9mJ40giN6JO4kpDFnzlzPmIJFcjH9lkJrIRTOahXPafwBkUkN8YxbCc" +
            "u0E0u6iRaNiEGPGNogkJ5E1cQC65Ga3wIeciElYyThl5SBn5mTYp+2jkIixBMrkeNVLD+7iHBvIR+lBE6nucaWhgfEr/M5xCDrkPRxFAZjAyfzJWGRmjzEFLvzLykjJy" +
            "lTIyndVS+dqDdqnRa2ppJBuNe5xp6OReE33veGY+WYIe6YcYJEj99Z2hCJFvP5qvA8MRhjCHddGkWleII/L7G4yjRWo7dY8zDW1YDnfRcFri2IGzoiGOdbcaeVDxB9Is" +
            "Ulcvo75T1H69LpYvIpTcim455wVrZSfbsELucaahAgvlt8dowQKymnvVmVnsJcV4mqpFMIIQRM6i+ThQ+/W6DHaERWraJb06jnOS3wqkutSQBZv4LlK5yuF17k0kd3Gv" +
            "v/EOosko2jwyyLhTU/v1uu3Mp4p/COeRTg5STbTEZHPZkya4i68eS2XOPWGXxpMdrKDKaTkGMJvMZYXVdwr7P8KB2l9qaO7AScyRedGFNLKBr9eD9GfezC40aJ8NvsID" +
            "nD4qZxOcC0r/CHtLxVnLeam07MYVyXUlLst3LeO2SNzd0pMPWHk1Vw5jDWaSXWiWWRfDN24jzewjDxcapmup51RSeRngpPCXuPZKfC/ZN3HSa62SrzGqiJB1RaJpPzvC" +
            "JPnLE+3NjKVK8tOGJjKCN6i8edBMLjRo6hrpOpYx++6S23T51tR+vU7nPIxvWc2ZbCyWfNax26tkTtQIbbAi8A8a/pVmeMpMsvLlWKRnY2XGr0UOMmWuhKqe/q8aND2Z" +
            "UVWbUGOOGHczS0Hq225P/Ql34Le7" ,
        Icon.Critical :
            "eJyVlUlslVUYhqEUUiBlCAumIi2UhhlBaBAKSKKJyaOBUKoYqdiYbqgURECkDghCIRJXmLhQNCYkJiwYRKNLjYrGjQkYh7S9WrhSLnSgrXARF773/c8f/wJW7GnytGf4" +
            "znu+6d+d/9ZDBQP8U314un4ZkBuNh/+VkxnMYHEroxktHmM848UfmMhE8SwTmCB+yBjGiJsYxjCxmEEM6sduYG1/Gp5hFKPEC8xipngJeFi8rJWnzJfYYTaw3es1rBfP" +
            "8yArrXEcY8UaCigQB/4PDUcZ67O/MZ97fUctNeZjVPquFSwT25jDbPFiYBvLqfB6FWuCpmprKWWq+D5DGXq7lj4anmY4w8VmZjNLzPAk62y7nIXiFdbYdi+f8LGY1Ytb" +
            "E4znM6xlrfg7C/yGNtZRJX7PJMeuum+MrOGeMPdziGuGVTzid9/HAvEqB2gUb3Cd6+JNjT/FvzRuJhjP35CqrNjJId6wn+YyR0yHWH4X/FGU0FAXcqg17L3MSh4Q26m0" +
            "77Nc45p4gIPsF19nH3vF7twQu3JDbFB+vCge4k3fnQ2aM4pNlf2xzLH6kWmOTR155AUNHzCCEfbdYsq9N8qDbk7zkW1lbWs7L7BNrOJxa3uebWwRn9NfmxPzr7GXVxPn" +
            "uvmMT53bUd6kgv33Iv9bw7cUUmifxblWRpnjm6JF1Gvsh0u54dqrpy5xZ8wtqt56+1Ejca5XUbhgDSWU2N8VLBG/SMTi65CLaa0tNUspFXtooUn8Q6M3aGgTN+vlm+6g" +
            "YWvwR05DJnGuR7e3+u5iil1vkb+TGt5lCEO8FvkqzUxmiB2c4Lht9DjuL/MKDYk76/XyZ4NfNibmG7RzV+Jch+rltO2XMU1sYgbTHYt/NNSqYgdq7idlapF9ttD1kFZ9" +
            "rHJddNEh7maP47yDnc6LdPDx+VCbu5STO8X9NDpnr2p0el+la7pVeTBPPKfeNU7c2Kc2o/7wFfnkW285i3wm6i0XlWN7XGsdXDE7rakraIsZz+fY7nNRTf/KFOdBikXu" +
            "M19G9aBvwO09an3gGdVJobUs5X6fncoUa3rUfSPDSceoPeRLzAynOOFzq1ndmOt1JSH+S1icsLuhnz4Z99C3A79hJCPFlmAjpZ413/9H/mkO366mwOYwnwr9sTnk3plg" +
            "50iwm3cX34tYyxOBse/OKmqTxF+Y517WolquSDCeP6eeXJQ4t+HOd9/VdzNm6KlxDvFO4Oe38Mgt+yb/h91YQ+3cvwEUh1KT",
        Icon.Warning :
            "eJy1lUlIVXEUxlWkDMwgCiIIKoNskVQGYkGLqBb+sMEWoiWl9szAcgiUsszAeFg0mVptQlECxSaKWjQQZZOkkVkI1qKJNhKJTfo0Ovd7VxOSUNP3Hvzg3HvP+c53zv2/" +
            "ouDy1SEB+iSXRdiPAOfrLRs25zFVfMZ2go0PSCHQOIuwEeVx6RmNhnukMtH4gyrijN84B8aLJEjTeGpYyWzxMyeINnZb1W3iBVIVP0KkcSkzxlxDoMsWdhKqmpdIN/Zw" +
            "gzzxGjnypZbNxgbS5NNYaognQuzgFMul4TIZxl5TVSU2c1bxevnRwVEWGVcx9781BBMkviKbyerzPAlu37uMv3jPTfGd6Ghz/Plue7Le2MwO+RHkODlKDVuJFD9wmMXG" +
            "n1Qrdy9NlBl3k0OmmC328oRjuq9SO/qWYhYYN7o+jkTDJHPA4Qt3/l85wwr1WUeS+n5NrdHLAe1BCUXkKt6ueLf5FW/sopwYvcMZhBgnuL4OR0MmS8Q37GOOZmC7rj4f" +
            "UWzso41KY5W9H85OVlNKvhv378d9CvVcqfainXxmGtNcX/+lYYopddiER3Pssg7D5W0Va1SjhVKxlQrjXWoo8DpnVK1qOvHT4nNO6rkKooyd7Nc+NbJF+UNdn4fSkEe0" +
            "2GbzDdNueaXfZ9WylbsJr8sS8SmHxEYOio+lqY+H8sfHVRK9zhm2R3lbrTeHOUT9pWG6bYD//NskdlIgH5w+Fipng6vhD3OG2LE+cyR30PU+m0mWZnJcM/1iXfrrJInT" +
            "/HWloZBlir10dfbr9tlZtFa8RYrmfJs08Q4evS/1OpMcJrvx9EHXfe79PXaOxg7hx15iBjTUEafYJ5vBYA3jxY9kiTXEDmhIZL5iV1gnXmfDuLK/Thzho/7fHGN6PJG/" +
            "AT+dCtg=" ,
        }

    __slots__=('_icon', '_text', '_detailedText',  '_standardButtons', '_defaultButton'
               '_widImage', '_widLabel', '_widBtnLayout',
               # Signal
               'buttonSelected')
    def __init__(self, *args, **kwargs):
        self.buttonSelected = pyTTkSignal(TTkMessageBox.StandardButton)
        TTkWindow.__init__(self, *args, **kwargs|{'layout':TTkGridLayout()})
        self._icon = kwargs.get('icon', TTkMessageBox.Icon.NoIcon)
        self._text = TTkString(kwargs.get('text', ''))
        self._detailedText = TTkString(kwargs.get('detailedText', ''))
        self._standardButtons = kwargs.get('standardButtons', TTkMessageBox.StandardButton.Ok)
        self._defaultButton = kwargs.get('defaultButton', TTkMessageBox.StandardButton.NoButton)

        compressedData = TTkMessageBox._compressed_data.get(self._icon,'')
        self._widImage = TTkImage(rasteriser=TTkImage.HALFBLOCK)
        self.layout().addWidget(self._widImage,0,0,4,1)
        if compressedData:
            data = TTkUtil.base64_deflate_2_obj(compressedData)
            self._widImage.setData(data)
            self._widImage.setMinimumSize(16,8)

        self.layout().addItem(TTkLayout(),0,1,1,3)
        self.layout().addItem(TTkLayout(),2,1,1,3)

        self._widLabel = TTkLabel(text=self._text)
        self._widLabel.setMinimumSize(*self._widLabel.size())
        self.layout().addWidget(self._widLabel,1,2)

        self._widBtnLayout = TTkHBoxLayout()
        self.layout().addItem(self._widBtnLayout,3,1,1,3)

        def _genClickedSlot(sb):
            @pyTTkSlot()
            def _clicked():
                self.close()
                self.buttonSelected.emit(sb)
            return _clicked

        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Help):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Help"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Reset):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Reset"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.RestoreDefaults):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Restore Default"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Apply):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Apply"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Discard): # Don't Save
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Don't Save"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Ignore):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Ignore"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Retry):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Retry"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Open):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Open"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.SaveAll):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="SaveAll"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Save):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Save"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Cancel):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Cancel"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Close):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Close"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Abort):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Abort"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Ok):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="OK"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.NoToAll):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="No to All"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.No):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="No"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.YesToAll):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Yes to All"))
            _btn.clicked.connect(_genClickedSlot(sb))
        if sb := (self._standardButtons & TTkMessageBox.StandardButton.Yes):
            self._widBtnLayout.addWidget(_btn := TTkButton(border=True, text="Yes"))
            _btn.clicked.connect(_genClickedSlot(sb))

        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        self.resize(w+2,h+4)

    # def setText(self, text):pass
    # def setDetailedText(self, text):
    # def setStandardButtons(self, buttons):pass
    # def setDefaultButton(self, button):pass