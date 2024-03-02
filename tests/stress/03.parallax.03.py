#!/usr/bin/env python3

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

import sys, os
import time, math

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

HouseBG_1_1 = ttk.TTkUtil.base64_deflate_2_obj(
    "eJxrYJmayM0ABrVTNHpYUhJLEqfETtEAoh5GhSkZLJiwh/nRtKYpIHIaVnkETAWagqaX5cP8te1TwFTLFAyZ6TAhNvxGgRSv2QMxpgtCNWJ3CxumgZiuwuJHkAX70I0U" +
    "IN4A4oNkCOhN7WFLzs/JLyqGpgw/v7YpxOIedmULUwsTS5Mp6BxSTEHHqQRcgcdWBI8KHJweIsmnuHyD2xc09BIqB6eXKAwfghFJQz9RHM/0sgc9nAY8GEYOZzS8R8N7" +
    "OHNGw5vO4Z1aqgcAL7yIzQ==")

HouseBG_1_2 = ttk.TTkUtil.base64_deflate_2_obj(
    "eJxrYJn6lY8BDGqnaPSwpCSWJE6JnaIBRD2MClMyWHDBHuZH0xqngMgmPKoQMBVoIk6zWD7MX7toCprARLDpzVNAnDV7wdTaBpx2YTcfZML0KRlsQDYHFl2cGWxg0/dg" +
    "MRaHgSBXLCfKxzgM44AbM504Y/hAnpgGUcsG8VLLlAxR/EGKH4LMaJ2SIU7It6TDQWdOag9bcn5OflExNFX7+bVNIQf3sCtbmFqYWJpMQeeQayI6TiXDdagOQfDI4+D2" +
    "I/V8T6wv8dtIXX/TMKxoFiQD4mkqc8gIGyLDAHccDLyvaZfysAcSwfQJDuMB99aw5uCJAEqNHo29ocwZjb2hzBmNvaHMSU0t1QMAlN+srA==")

HouseBG_2_1 = ttk.TTkUtil.base64_deflate_2_obj(
    "eJztl8FKw0AQhhXTFBHBYw4eBC89eRGiT9E38FA1kINQqHoUaoWqGPSybUEoBb3qG/g0PoGPYHYbjEs26e5mk9nAdFrKx6abf+ef2U2HzmTkr7HXDelEznnvqkdOSCd+" +
    "R+t7JHT0Itr4nt6SsEW/RyRyfhafQ+3J8iKIRcqKmSd3Z1IW/+FNoIsNzAn94bMh2dJi6a0fCIcz46nT0ucyMU9LO8dSmuilH19Fl7qGRUoHNTeuyW3BWHupil4xYUVw" +
    "R0IvbNWtkIutgrEdTVVeHKL1pzmiTj8K7WND9yw7L0bKU6Bx08C8K3PzFy5dy1SwFk4ZzZmB1cpErGf2TsLdhGjCX4vkFZWITsinThCVNYJ6eKlpVqjK+GSFqkygqsar" +
    "CiL3rH/RH1wmj3Td7pjU/Yna+/6hf3x0SuQBQqfKJzCYS37hKRVBbrJ0JjMLzTAV2kA5N0EM5MECr0z6Jrv/GM8beCuWr2xLLQVrBXBLle3RKXjI4xtLw+S+Df9sALKJ" +
    "6RSUTp0DOGuZowobArjWGp9/VhWdZS4ilNibwCWVrOtyZ7qo0iVmhM8GgnLhwCup8LjSbX+F/sBdHyFbROByLADdwwZeOQKCHVD+/yy2FwJCfnvxjVPtvVgvwq8aAQFB" +
    "BbBxERAaCNi4CAgNBGxcBIQGQhBcH/wCnyVIJQ==")

HouseBG_2_2= ttk.TTkUtil.base64_deflate_2_obj(
    "eJxrYJm6hI8BDGqnaPSwpCSWJE6JnaIBRD2MClMyWNBhD/Ojab0QcVZMWUyYCjQJuylTp4DIbpBZ7BkcQDGWD/PXtk8BUWv2QW0Gc/ZMgWlpmZLBA6L7p+C1ghNoIFj9" +
    "BLAVnVOAIvwgVtcUqDWNUzIEYeav7ULzJliwbwp248GSi7AEDC4I1tCD3TRe4o0BQnEg5kYxgwcISTEBEjhgs7DHC2lw0JiR2sOWnJ+TX1QMTbp+fm1TiME97MpmxmYW" +
    "5klTCAlSilOJdBWK5RguoUSWeD8TZw6xviPXzSQ4ibCDUQURPGpz8IYWrlCil+OGJofkIMXUMOB+GGQc/BkIJWyJM2M0BVM9VohThj+ORjmDgTMaR4OfMxpHg5+Tmlqq" +
    "BwBHZ7KE")

HouseBG_3_1 = ttk.TTkUtil.base64_deflate_2_obj(
    "eJztV81OGzEQLmpISzjApSeKRBSJRkqJIjZU4coD5A045GeRD5WQWnpEavmJetgW2k6qSqgFCYlTeYS+DE/AnQu2dzebdXaDN2uzTjWZON7vs/fbyXjGcT7m+ndbT/hr" +
    "H8pOrtvaa8E2lOnbmVkBkpMxJ3d7fv0ZWPf3n+Q9yc2mPknMm+Xe9Lg31wcw8O+Ly3wDks/At1nynMyNsAUyr9YbyRhpt4f8cJ7e/OzHZgobPVGaR9MSF7IQO7L4uPHg" +
    "xfIjchH40B/FdS63QvzRF24l/4IQe+my4aximUT3gCVBZ4nxn4B9HiX8HpJ+UuVLGEZnwnO4s9998sVgoBhilhU4NbrtTGTc4a8S0TKp1mjk4Zitc/8UyCvWX9F+YOXI" +
    "62h2FI0bjb5eNSk2bmKw3DwEUuH8S2qsr7iYjR0DeT3M8TnCPDrDNZET7xO0e0DWfI94ev0G7ljRnwBAany4JtHLcjI9s9LQYolfeM1z3Od9XPEsjhN14vR8PlisYoAz" +
    "sgIvKLZMSfdMDVY1qpIy94L6YTv5zu7b3XfvveN7s9kDlc15VrIsa91qgAhUP0l3sxVFJz4i4fAESACyAlPQ0sQ0dRzVgilfldTZ/UhhnggYEF/tFWBAmOVqI+uIYwWY" +
    "1bACTGlpK8Cw1ZiKmKuIe1MMt/zxQ/bclOxW2RzJ5pikN9zjiyLqdhVllMCFFILalmiSJTFst0GgAChPsIlqPfMwINALFCUW1WxsNOqbdZa3bau93qm5OYwsssgii6wx" +
    "LD8IDBMIECBQBLzTUGunZbc7/v+x6KnO4CBGr+pdZrEsquhUQb9RxWyVsfrBZpNs9+nazMQjQwSLKjpV0G9UMVslwe4jf1+w/73hr1gWVXSqoN+oYraK+n9eCBAgSPzb" +
    "jtWFAIGu6sreJQQI/keA1YUAgbbqsj9U7wEuEcBK")

class Layer():
    def __init__(self, imageData) -> None:
        self.processData(imageData)
        self._h = len(imageData['data'])
        self._w = len(imageData['data'][0])

    def size(self):
        return self._w, self._h

    def processData(self, imageData):
        # Trying to extract for each line the slices that can be copied and the slices that are transparent (nobg is defined)
        data = imageData['data']
        colors = imageData['colors']
        opaques = []
        transparents = []
        for rowd,rowc in zip(data,colors):
            slicesOpaque = []
            slicesTrans  = []
            pixOpaque = []
            pixTrans  = []
            curSlice = []
            transparent = False

            def _pushSlice(t, cs, so=slicesOpaque, st=slicesTrans, po=pixOpaque, pt=pixTrans):
                if not cs: return
                xa,xb = cs[0]
                if transparent:
                    pix = pt
                    sl = st
                else:
                    pix = po
                    sl = so
                if xa==xb:
                    cs[0] = xa
                    cs[1] = cs[1][0]
                    cs[2] = cs[2][0]
                    pix.append(tuple(cs))
                else:
                    # cs[0] = slice(xa,xb+1)
                    cs[0] = (xa,xb+1)
                    sl.append(tuple(cs))
                cs.clear()

            for x, (ch,(fg,bg)) in enumerate(zip(rowd,rowc)):
                if ch == ' ' and fg==bg==None: # Fully transparent space
                    _pushSlice(transparent,curSlice)
                    continue
                if bg and transparent:
                    _pushSlice(transparent,curSlice)
                    transparent = False
                elif not bg and not transparent:
                    _pushSlice(transparent,curSlice)
                    transparent = True
                if not curSlice:
                    curSlice = [[x,x],[],[]]
                curSlice[0][1]=x
                curSlice[1].append(ch)
                if fg and bg:
                    curSlice[2].append(ttk.TTkColor.fg(fg)+ttk.TTkColor.bg(bg))
                elif fg:
                    curSlice[2].append(ttk.TTkColor.fg(fg))
                elif bg:
                    curSlice[2].append(ttk.TTkColor.bg(bg))
                else:
                    curSlice[2].append(ttk.TTkColor.RST)
            _pushSlice(transparent,curSlice)
            transparents.append(list([slicesTrans,pixTrans]))
            opaques.append(list([slicesOpaque,pixOpaque]))
        self._data = {'opaque':     tuple(opaques),
                      'transparent':tuple(transparents)}

    def drawInCanvas(self, pos, canvas:ttk.TTkCanvas):
        x,y = pos
        w,h = canvas.size()
        if y>=h or x>=w: return
        for ly,sls in enumerate(self._data['opaque'][0:h-y],y):
            for sl in sls[0]:
                a,b = sl[0]
                if x+a>=w or x+b<0 : continue
                ca = max(0,min(w,x+a))
                cb = max(0,min(w,x+b))
                da = ca-(x+a)
                db = cb-ca+da
                # canvas._data[  ly][ca:cb] = ['X']*(cb-ca)# sl[1][da:db]
                canvas._data[  ly][ca:cb] = sl[1][da:db]
                canvas._colors[ly][ca:cb] = sl[2][da:db]
            for sl in sls[1]:
                a = sl[0]
                if not (0 <= x+a < w): continue
                canvas._data[ly][x+sl[0]] = sl[1]
                if type(sl[2]) != ttk.TTkColor:
                    pass
                canvas._colors[ly][x+sl[0]] = sl[2]
        for ly,sls in enumerate(self._data['transparent'][0:h-y],y):
            for sl in sls[0]:
                a,b = sl[0]
                if x+a>=w or x+b<0 : continue
                ca = max(0,min(w,x+a))
                cb = max(0,min(w,x+b))
                da = ca-(x+a)
                db = cb-ca+da
                canvas._data[  ly][ca:cb] = sl[1][da:db]
                for mcx,mc in enumerate(zip(canvas._colors[ly][ca:cb],sl[2][da:db]),ca):
                    canvas._colors[ly][mcx] = mc[0] + mc[1]
            for sl in sls[1]:
                a = sl[0]
                if not (0 <= x+a < w): continue
                canvas._data[ly][x+sl[0]] = sl[1]
                canCol = canvas._colors[ly][x+sl[0]]
                newCol = canCol + sl[2]
                canvas._colors[ly][x+sl[0]] = newCol

class Parallax(ttk.TTkWidget):
    COLOR1 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#AFAEBC")
    COLOR2 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#858494")
    COLOR3 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#63687B")
    COLOR4 = ttk.TTkColor.fg("#9694A1")+ttk.TTkColor.bg("#B3B2C0")
    COLOR5 = ttk.TTkColor.fg("#333238")+ttk.TTkColor.bg("#B3B2C0")
    COLOR6 = ttk.TTkColor.fg("#333238")+ttk.TTkColor.bg("#333238")

    def __init__(self, *args, **kwargs):
        self._baseTime = time.time()
        self._l11 = l11 = Layer(HouseBG_1_1)
        self._l12 = l12 = Layer(HouseBG_1_2)
        self._l21 = l21 = Layer(HouseBG_2_1)
        self._l22 = l22 = Layer(HouseBG_2_2)
        self._l31 = l31 = Layer(HouseBG_3_1)

        w11,h11 = l11.size()
        w12,h12 = l12.size()
        w21,h21 = l21.size()
        w22,h22 = l22.size()
        w31,h31 = l31.size()
        self._layer1 = {'size':w11+w12+w11+w11+w12,'layers':(l11,l12,l11,l11,l12),'off':(4,3,4,4,3)}
        self._layer2 = {'size':w21+w22+w21        ,'layers':(l21,l22,l21),'off':[4,8,4]}
        self._layer3 = {'size':w31+30             ,'layers':[l31]        ,'off':[5]}

        super().__init__(*args, **kwargs)
        ttk.TTkHelper._rootWidget.paintExecuted.connect(self._refreshAnimation)
        self._refreshAnimation()

    @ttk.pyTTkSlot()
    def _refreshAnimation(self):
        self.update()

    # 1) 11 11 11 11-11 11 11 11-11 11 ..
    # 2) 22 11 11 11-22 11 11 11-22 11 ..
    # 3) 33 33 11 11-33 33 11 11-33 33 ..
    # 4) 44 44 44 11-44 44 44 11-44 44 ..
    # 5) 44 44 44 44-44 44 44 44-44 44 ..

    def paintEvent(self, canvas: ttk.TTkCanvas):
        w,h = self.size()
        diff = int(200*(time.time() - self._baseTime))

        secH  = h//5
        # draw the bgColor
        canvas.fill(pos=(0,0), size=(w,secH*4), color=Parallax.COLOR1)
        # # draw the 2nd section
        # for x in range(0,w+8,16):
        #     x += (diff%(32*4))//8
        #     canvas.fill(pos=(w-x,  secH), size=(3,secH*3), color=Parallax.COLOR2)
        #     canvas.fill(pos=(w-x-2,secH+2), size=(6,secH*3), color=Parallax.COLOR2)
        #     canvas.fill(pos=(w-x,  secH+3), size=(10,secH*3), color=Parallax.COLOR2)
        # canvas.fill(    pos=(0,3*secH+3), size=(w,secH*3), color=Parallax.COLOR2)
        # # draw the 3nd section
        # for x in range(0,w+16,32):
        #     x += (diff%(32*6))//6
        #     canvas.fill(pos=(w-x,2*secH), size=(12,secH*3), color=Parallax.COLOR3)
        #     canvas.fill(pos=(w-x+12,5*secH//2), size=(4,secH*3), color=Parallax.COLOR3)

        # lw1,lh = self.l11.size()
        # lw2,lh = self.l12.size()
        # lw3,lh = self.l21.size()
        # lw=lw1
        # self.l11.drawInCanvas(pos=((        (-diff)//8)%(w+lw)-lw,4),canvas=canvas)
        # self.l11.drawInCanvas(pos=((lw1+lw2+(-diff)//8)%(w+lw)-lw,4),canvas=canvas)
        # lw=lw2
        # self.l12.drawInCanvas(pos=((lw1+      (-diff)//8)%(w+lw)-lw,3),canvas=canvas)
        # self.l12.drawInCanvas(pos=((2*lw1+lw2+(-diff)//8)%(w+lw)-lw,3),canvas=canvas)
        # canvas.fill(pos=(0,9), size=(w,h-9), color=Parallax.COLOR2)
        # lw=lw3
        # self.l21.drawInCanvas(pos=((        (-diff)//4)%(w+lw)-lw,5),canvas=canvas)
        # self.l21.drawInCanvas(pos=((lw3+    (-diff)//4)%(w+lw)-lw,5),canvas=canvas)
        # self.l21.drawInCanvas(pos=((lw3+lw3+(-diff)//4)%(w+lw)-lw,5),canvas=canvas)

        # draw the Layers:
        def _drawLayer(_l,_d,canvas=canvas):
            _lw  = _l['size']
            _la  = _l['layers']
            _off = _l['off']
            _x = _d
            for _ll,_lo in zip(_la,_off):
                __w,__h = _ll.size()
                _ll.drawInCanvas(pos=((_x    )%(w+_lw)-_lw,_lo),canvas=canvas)
                _ll.drawInCanvas(pos=((_x+_lw)%(w+_lw)-_lw,_lo),canvas=canvas)
                _x += __w

        _drawLayer(self._layer1,(-diff)//8)
        canvas.fill(pos=(0,9),  size=(w,h-9),  color=Parallax.COLOR2)
        _drawLayer(self._layer2,(-diff)//4)
        canvas.fill(pos=(0,17), size=(w,h-17), color=Parallax.COLOR3)
        _drawLayer(self._layer3,(-diff)//2)

        # # draw the 4nd section
        # for x in range(0,w+20,50):
        #     x += (diff%(50*2))//2
        #     canvas.fill(    pos=(w-x+15,2*secH-3), color=Parallax.COLOR6, size=(1,secH*3) )
        #     canvas.fill(    pos=(w-x+10,3*secH-4), color=Parallax.COLOR6, size=(10,secH*3) )
        #     canvas.drawText(pos=(w-x,   3*secH+0), color=Parallax.COLOR5, text='▀'*43)
        #     canvas.drawText(pos=(w-x,   3*secH+1), color=Parallax.COLOR4, text=f'┌{"─╥"*20}─┐')
        #     canvas.drawText(pos=(w-x,   3*secH+2), color=Parallax.COLOR4, text=f'└{"─╨"*20}─┘')
        #     canvas.drawText(pos=(w-x,   3*secH+3), color=Parallax.COLOR5, text=f'  {"███ "*10} ')
        #     canvas.drawText(pos=(w-x,   3*secH+4), color=Parallax.COLOR5, text=f'  {"███ "*10} ')
        #     canvas.fill(    pos=(w-x,   3*secH+5), color=Parallax.COLOR4, size=(43,secH) )
        # # draw the 5nd section
        # canvas.fill(pos=(0,4*secH+2), size=(w,secH), color=Parallax.COLOR4)


root = ttk.TTk(title="TTKanabalt")
Parallax(parent=root, pos=(5,2), size=(100,25))
root.mainloop()

