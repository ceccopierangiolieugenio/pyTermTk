    #!/usr/bin/env python3

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

    import os
    import sys
    import argparse
    from PIL import Image

    sys.path.append(os.path.join(sys.path[0],'../..'))
    import TermTk as ttk

    ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

    def load_imageFile_to_TTkImage(file_name:str,ttkImage:ttk.TTkImage) -> None:
        pilImage = Image.open(file_name)
        pilImage = pilImage.convert('RGBA')
        data = list(pilImage.getdata())
        rgbList = [(r*a//255,g*a//255,b*a//255) for r,g,b,a in data]
        width, height = pilImage.size
        imageList = [rgbList[i:i+width] for i in range(0, len(rgbList), width)]
        ttkImage.setData(imageList)

    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('filename', type=str,
                        help='the image to display')
        args = parser.parse_args()

        root = ttk.TTk()
        window = ttk.TTkWindow(parent=root, size=(30,10), layout=ttk.TTkGridLayout())
        image = ttk.TTkImage(parent=window)

        load_imageFile_to_TTkImage(file_name=args.filename, ttkImage=image)

        root.mainloop()

    if __name__ == '__main__':
        main()


