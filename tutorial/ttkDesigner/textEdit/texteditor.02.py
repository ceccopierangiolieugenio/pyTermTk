from TermTk import TTkUtil, TTkUiLoader, TTk
from TermTk import pyTTkSlot

# Data generated using ttkDesigner
# "textEditWindow" is the object defined using ttkDesigner
textEditWindow = TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
    "eJytVltvG0UUXtvrXV96yYVSICBWCKkOEpaDUAlqXhLTGNi6tRJDhao8bHZHPqOud63d2dAgVUI8OdWIBxgU3ipA8MAv4Inf1J/Amdn1NQmKq3pleWe+M2e+75vL8ff6" +
    "L99UNPV5KmrcPCJRTMNA8OJGvVFvCF5gCRUSKrq+E8eCl7vdxw9p4IXfCm4MnMjpxwrX7zt9IvhVxLrkCbvrURZGgpc6YUyZTHkgarZu5wnX9+l3RDW/sG8QXm7TwHpI" +
    "PQbCzvOKbH1OaA+YsHUEnScZ2M4vIYrNDG3rS9zsOJ5Hg57KVrBz8iHcuOcchwlDMsi1FVFv1Da/pjE99IkYcvNu4OCbJ1+7Yeh36UBwfe1Ro4+ydsLIIxFCxS5lGM4t" +
    "CchvO7KkOosoeZb14vmvP6aDrqSmWLu+04vFl2hoKeGGn86MBkERXgfzKTrSImGfsOgYKWv4tOxlJmJecoH6XkSUUSpeWb2TMIbmyZE1KHNzhwVf4TwCqlLyiq0RuCrf" +
    "KnaBwHXbgCW7AMs4fU6DFXxdPcim0WToDZUzswNuDuGNIbwJb3FdihJ8aSRTTqFkwdqQl5tA3MfSLXHCTdVA304SeDeV9aEkB++l0yAPVAPvH4iEFyLcJLbGC27oC7vA" +
    "TWzHAycQdo6b2Je9J2maW9Ma98hY49tjjdXzNKY/czKR01gc1Ce6ZNqRLmicwMYFKqoTFXDb1uATW4dNOwefnmVrINumdFORvTW/IMWFyV4fkcWsl+FaOcO1eBFX6Wwz" +
    "HBxnZDdeobMy7cs5a1zEtoRsO07MSEZ3a56uuTDd5RFdlffl+JqzfPkqnqhd6pP0pHYono5o5rw+GOChTiVoYwlGKkFPJaAJi9n94vnPP8zS53rHwVuS5+p4zzWdgbpz" +
    "eVUysz6jjh/2sB9bDG94vBm3fd+SWGzVPljHuG3XJQNmtUOPyCNbVuPSVu58Z4wzzmhzK9mbdmHfORotpPHqXPjp31kXIIAQBrOyIZqXCwx5JrZ2WWG5uSV/DZe8Gfph" +
    "dO6al9QpQzSTe2Vebn4hufgdr3ExzcuvrT36ePPOR3ca+Nze7IvLCsnPCamikFG1nvCf9GSbtpDxb9nXJH8N+Wv/e+4mlaV6jwbEup/0D1VBLe8Rx7MeBP4x1pJKO/EZ" +
    "tWSEGEqKualNVEpIkvCqGwYBceVmjrPCyI2YBLI8wykvRcQl9Eg21rGf9gLHF3w1wfK1feRQXxat2iGWd9zieuyHssbFhGW1P0OUF7/BKfwOW/AHX43I2dHwJ/yVxa1j" +
    "3CnGlV1frrtXkyg35Jy1cbKtNAj+lpBMOIFaU1DRTdgE2Zse5OKFOoEOpiBzIC+v2gzxZ0joHTeJ8P8DU3ukCU7QQ3KjnapIrqB21ZrqzpI8y1TddGX3PvHR9MWHwz8Y" +
    "VsGw3dBNYkmRJPX/AFIIXtE="))

# Retrieve the widgets that we need to use
btnOpen  = textEditWindow.getWidgetByName("BtnOpen")
btnSave  = textEditWindow.getWidgetByName("BtnSave")
textEdit = textEditWindow.getWidgetByName("TextEdit")

# This is a generic routine to open/read a file
# and push the content to the "TextEdit" widget
pyTTkSlot(str)
def openRoutine(fileName):
    with open(fileName) as fp:
        textEdit.setText(fp.read())

# Connect the open routine to the (open)"filePicked" event
btnOpen.filePicked.connect(openRoutine)

# This is a generic routine to save the content of
# the "TextEdit" widget to the chosen file
pyTTkSlot(str)
def saveRoutine(fileName):
    with open(fileName, 'w') as fp:
        fp.write(textEdit.toPlainText())

# Connect the save routine to the (save)"filePicked" event
btnSave.filePicked.connect(saveRoutine)

# Initialize TTK, add the window widget, and start the main loop
root=TTk()
root.layout().addWidget(textEditWindow)
root.mainloop()
