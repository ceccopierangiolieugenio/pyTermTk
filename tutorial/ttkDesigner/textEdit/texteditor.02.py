from TermTk import TTkUtil, TTkUiLoader, TTk
from TermTk import pyTTkSlot

# Data generated using ttkDesigner
# "textEditWindow" is the object defined using ttkDesigner
textEditWindow = TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
    "eJytVltvG0UUXtvrXV96yYVSICBWFVIdJCwHoRLUvCSmMXTr1koMFarysNkd+Yy63rV2Z0ODVKniyalGPMCg8FYBggd+AU/8pv4Ezsyur0lQEuGV5T3znTnzfd/c/EL/" +
    "+ZuKpj7PRY2bBySKaRgIXlyrN+oNwQssoUJCRdd34ljwcrf79DENvPBbwY2BEzn9WOH6Q6dPBL+KWJc8Y/c8ysJI8FInjCmTJfdEzdbtPOH6Lv2OqPBL+wbh5TYNrMfU" +
    "YyDsPK/I6AtCe8CErSPoPMvAdn4BUQwztK0vcLPjeB4Neqpawc7Jh3DjgXMYJgzJINdWRL1RbH5NY7rvEzHk5r3AwTdPvnbD0O/SgeD6ypNGH2VthZFHIoSKXcownVsS" +
    "kN92ZEl1FlHyLOv1q19+SDtdSU2xtn2nF4v72gutlHDDT0dGg6AIb4L5HB1pkbBPWHSIlDV8WvYiEzEvuUB9LyLKKJWvrN5KGEPzZM8alLm5xYKvcBwBVSl5ydYIXJVv" +
    "FbtA4LptwIJdgMX7mpbTYAlfl/eyYTSZekPVzOyAm0N46wjehne4LkUJvjCSKYdQsmBlyMtNIO5T6ZY44qYK0LejBN5PZX0kycGtdBjkgWrggz2R8EKEi8TWeMENfWEX" +
    "uIlxPHACYee4iW3Ze5KWuT2tcYeMNb471lg9TWP6MycTOY3FQX2iS5Yd6YLGEaydoaI6UQF3bA0+tXVYt3Pw2Um2BrJtSjcV2dvzE1I8N9lhRvb6iCxWPQ/XygmuxbO4" +
    "Smeb4eAwI7t2eWeH887Kspdz1jiLbQnZdpyYkYzuxjxd88J0F0d0Vd3L8TVn+fJl3FHb1CfpTu1Q3B3RzH59NMBNnUrQxhKMVIKeSkATLmb361c/fT9Ln+sdB09Jnqvj" +
    "Odd0BurM5VXJzPqcOn7Yw3aMGJ7weDJu+r4lsdiqfbiKeZuuSwbMaocekVu2rPqlUe50Z4wTzmhzM9mbdmHXORhNpPH/ufDjP7MuQAAhDGZlQzQvFxjyTGztvMJyc1P+" +
    "Bk55M/TD6NQ5L6ldhmgm98q83PyF5OJ3PMfFtC6/tvLkk/W7H99t4HNnvS/OKyQ/J6SKQka39YT/pCVbtIWMf8u+JvlryF/7z303ps+rD2hArIdJf19dqOUd4njWo8A/" +
    "xLuk0k58Ri2ZIYaSYm5qEZUSkiS86oZBQFy5mOPsYuRGTAJ5PcMxL0XEJfRABqvYTnuB4wu+nOD1tXngUF9eWrV9vN5xieuxH8o7LiYsu/szRHnxKxzDb7ABv/PliJzs" +
    "DX/An1neKuYdY17Z9eW8ezWJckOOWRsX20iT4C8JyYITqDUFFd2ETZCd6U4uHqgTaG8KMgfy8KrNEH+JhN5zkwj/PzC1RprgBD0kN1qpiuQSalfRVHNW5GWm6qYrm3eJ" +
    "j6ZfvDv8jWkVTNsO3SSWFElS/xfnLV9T"))

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
