# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys,os
import math
import argparse
from dataclasses import dataclass
from typing import Optional,Tuple,List,Dict

import numpy as np

from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

sys.path.append(os.path.join(sys.path[0],'../..'))

import TermTk as ttk

@dataclass
class RenderData:
    cameraY: int
    cameraAngle: float
    fogNear: float
    fogFar: float
    bgColor: Tuple[int,int,int,int]
    resolution: Tuple[int,int]


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

def project_point(camera_position, look_at, point_3d):
    """
    Project a 3D point into a normalized projection matrix.

    Args:
        camera_position: The 3D position of the camera (x, y, z).
        look_at: The 3D position the camera is looking at (x, y, z).
        point_3d: The 3D point to project (x, y, z).

    Returns:
        The 2D coordinates of the projected point in normalized space.
    """
    # Step 1: Calculate the forward, right, and up vectors
    def normalize(v):
        return v / np.linalg.norm(v)

    forward = normalize(np.array(look_at) - np.array(camera_position))
    right = normalize(np.cross(forward, [0, 1, 0]))
    up = np.cross(right, forward)

    # Step 2: Create the view matrix
    view_matrix = np.array([
        [   right[0] ,    right[1] ,    right[2] , -np.dot(  right , camera_position)],
        [      up[0] ,       up[1] ,       up[2] , -np.dot(     up , camera_position)],
        [-forward[0] , -forward[1] , -forward[2] ,  np.dot(forward , camera_position)],
        [          0 ,          0  ,          0  ,  1]
    ])

    # Step 3: Create the projection matrix
    near = 1.0  # Near plane normalized to 1
    width = 1.0  # Width of the near plane
    height = 1.0  # Height of the near plane
    aspect_ratio = width / height

    projection_matrix = np.array([
        [1 / aspect_ratio, 0,  0,  0],
        [               0, 1,  0,  0],
        [               0, 0, -1, -2 * near],
        [               0, 0, -1,  0]
    ])

    # Step 4: Transform the 3D point into clip space
    point_3d_homogeneous = np.array([point_3d[0], point_3d[1], point_3d[2], 1])
    view_space_point = view_matrix @ point_3d_homogeneous
    clip_space_point = projection_matrix @ view_space_point

    # Step 5: Perform perspective divide to get normalized device coordinates (NDC)
    if clip_space_point[3] == 0:
        raise ValueError("Invalid projection: w component is zero.")
    ndc_x = clip_space_point[0] / clip_space_point[3]
    ndc_y = clip_space_point[1] / clip_space_point[3]

    return ndc_x, ndc_y

@dataclass
class _Movable():
    x:int
    y:int
    z:int
    data = {}

    def _updateBox(self):
        pass

class _Image(_Movable):
    __slots__ = ('size','tilt','fileName', 'box')
    size:int
    tilt:float
    fileName:str
    image:Image
    box:Tuple[int,int,int,int]
    def __init__(self,size:int,tilt:float,fileName:str, **kwargs):
        super().__init__(**kwargs)
        if not os.path.isfile(fileName):
            raise ValueError(f"{fileName} is not a file")
        try:
            self.image = Image.open(fileName).convert("RGBA")
        except FileNotFoundError:
            raise ValueError(f"Failed to open {fileName}")
        self.size = size
        self.tilt = tilt
        self.fileName = fileName
        self._updateBox()

    def _updateBox(self):
        size = float(self.size)
        w = 1 + 2*size*abs(math.cos(self.tilt))
        h = 1 +   size*abs(math.sin(self.tilt))
        self.box = (
                int(self.x-w/2),
                int(self.y-h/2),
                int(w), int(h),
            )

    def getBox(self) -> Tuple[int,int,int,int]:
        return self.box

class _Camera(_Movable):
    tilt:int = 0

@dataclass
class _State():
    camera: _Camera
    images: List[_Image]
    currentMovable: Optional[_Movable] = None
    highlightedMovable: Optional[_Movable] = None

class Perspectivator(ttk.TTkWidget):
    __slots__ = ('_state')
    _state:_State
    def __init__(self, state:_State, **kwargs):
        self._state = state
        super().__init__(**kwargs)
        self.setFocusPolicy(ttk.TTkK.ClickFocus)

    def mousePressEvent(self, evt):
        self._state.highlightedMovable = None
        self._state.currentMovable = None
        cx,cy = self._state.camera.x,self._state.camera.y
        if cx-1 <= evt.x <= cx+2 and cy-1 <= evt.y <= cy+1:
            self._state.currentMovable = self._state.camera
            self._state.camera.data = {
                'mx':self._state.camera.x-evt.x,
                'my':self._state.camera.y-evt.y}
        else:
            for image in self._state.images:
                ix,iy,iw,ih = image.getBox()
                if ix <= evt.x < ix+iw and iy <= evt.y < iy+ih:
                    image.data = {
                        'mx':image.x-evt.x,
                        'my':image.y-evt.y}
                    self._state.currentMovable = image
                    index = self._state.images.index(image)
                    self._state.images.pop(index)
                    self._state.images.append(image)
                    break
        self.update()
        return True

    def mouseMoveEvent(self, evt:ttk.TTkMouseEvent):
        self._state.highlightedMovable = None
        cx,cy = self._state.camera.x,self._state.camera.y
        if cx-1 <= evt.x <= cx+2 and cy-1 <= evt.y <= cy+1:
            self._state.highlightedMovable = self._state.camera
        else:
            for image in self._state.images:
                ix,iy,iw,ih = image.getBox()
                if ix <= evt.x < ix+iw and iy <= evt.y < iy+ih:
                    self._state.highlightedMovable = image
                    break
        self.update()
        return True

    def mouseReleaseEvent(self, evt:ttk.TTkMouseEvent):
        self._state.highlightedMovable = None
        self._state.currentMovable = None
        self.update()
        return True

    def mouseDragEvent(self, evt:ttk.TTkMouseEvent):
        if not (movable:=self._state.currentMovable):
            pass
        elif evt.key == ttk.TTkK.RightButton and isinstance(movable,_Image):
            x = evt.x-movable.x
            y = evt.y-movable.y
            movable.tilt = math.atan2(x,y*2)
            movable._updateBox()
            self.update()
        elif evt.key == ttk.TTkK.LeftButton:
            mx,my = movable.data['mx'],movable.data['my']
            movable.x = evt.x+mx
            movable.y = evt.y+my
            movable._updateBox()
            self.update()
        return True

    def wheelEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        if not (image:=self._state.highlightedMovable):
            pass
        elif evt.evt == ttk.TTkK.WHEEL_Up:
            image.size = min(image.size+1,50)
            image._updateBox()
            self.update()
        elif evt.evt == ttk.TTkK.WHEEL_Down:
            image.size = max(image.size-1,5)
            image._updateBox()
            self.update()
        return True

    @ttk.pyTTkSlot(RenderData)
    def render(self, data:RenderData):
        outImage = self.getImage(data)
        # outImage.save(filename='outImage.png')
        outImage.save('outImage.png')

    def getImage(self, data:RenderData) -> Image:
        return self.getImagePil(data)

    def getImagePil(self, data:RenderData) -> Image:
        ww,wh = self.size()
        cam_x,cam_y = self._state.camera.x,self._state.camera.y
        observer = (cam_x , -data.cameraY , cam_y )  # Observer's position
        # observer = (ww/2 , -data.cameraY , wh-3 )  # Observer's position
        dz = 10*math.cos(math.pi + math.pi * data.cameraAngle/360)
        dy = 10*math.sin(math.pi + math.pi * data.cameraAngle/360)
        look_at  = (cam_x , dy-data.cameraY , cam_y+    dz)  # Observer is looking along the positive Z-axis
        screen_width, screen_height = data.resolution
        w,h = screen_width,screen_height
        prw,prh = screen_width/2, screen_height/2

        # step1, sort Images based on the distance
        images = sorted(self._state.images,key=lambda img:img.getBox()[1])
        znear,zfar = 0xFFFFFFFF,-0xFFFFFFFF
        for img in images:
            ix,iy,iw,ih = img.getBox()
            ih-=1
            znear=min(znear,iy,iy+ih)
            zfar=max(zfar,iy,iy+ih)
            isz = img.size*2
            if math.pi/2 <= img.tilt < math.pi or -math.pi <= img.tilt < 0:
                zleft = iy
                zright = iy+ih
                ip1x,ip1y =  project_point(observer,look_at,(ix+iw , -isz , iy+ih ))
                ip2x,ip2y =  project_point(observer,look_at,(ix    , -isz , iy    ))
                ip3x,ip3y =  project_point(observer,look_at,(ix+iw ,  0   , iy+ih ))
                ip4x,ip4y =  project_point(observer,look_at,(ix    ,  0   , iy    ))
                ip5x,ip5y =  project_point(observer,look_at,(ix+iw ,  isz , iy+ih ))
                ip6x,ip6y =  project_point(observer,look_at,(ix    ,  isz , iy    ))
                ip7x,ip7y =  project_point(observer,look_at,(ix+iw ,  0   , iy+ih ))
                ip8x,ip8y =  project_point(observer,look_at,(ix    ,  0   , iy    ))
            else:
                zleft = iy+ih
                zright = iy
                ip1x,ip1y =  project_point(observer,look_at,(ix+iw , -isz , iy    ))
                ip2x,ip2y =  project_point(observer,look_at,(ix    , -isz , iy+ih ))
                ip3x,ip3y =  project_point(observer,look_at,(ix+iw ,  0   , iy    ))
                ip4x,ip4y =  project_point(observer,look_at,(ix    ,  0   , iy+ih ))
                ip5x,ip5y =  project_point(observer,look_at,(ix+iw ,  isz , iy    ))
                ip6x,ip6y =  project_point(observer,look_at,(ix    ,  isz , iy+ih ))
                ip7x,ip7y =  project_point(observer,look_at,(ix+iw ,  0.1 , iy    ))
                ip8x,ip8y =  project_point(observer,look_at,(ix    ,  0.1 , iy+ih ))
            img.data = {
                'zleft':zleft,
                'zright':zright,
                'top' : {
                    'p1':(int((ip1x+1)*prw) , int((ip1y+1)*prh)),
                    'p2':(int((ip2x+1)*prw) , int((ip2y+1)*prh)),
                    'p3':(int((ip3x+1)*prw) , int((ip3y+1)*prh)),
                    'p4':(int((ip4x+1)*prw) , int((ip4y+1)*prh)),
                },
                'bottom' : {
                    'p1':(int((ip5x+1)*prw) , int((ip5y+1)*prh)),
                    'p2':(int((ip6x+1)*prw) , int((ip6y+1)*prh)),
                    'p3':(int((ip7x+1)*prw) , int((ip7y+1)*prh)),
                    'p4':(int((ip8x+1)*prw) , int((ip8y+1)*prh)),
                }

            }

        # step2, get all the layers and masks for alla the images
        for img in images:
            image = img.image

            imageTop = image.copy()
            imageBottom = image.copy()
            imageTopAlpha = imageTop.split()[-1]
            imageBottomAlpha = imageBottom.split()[-1]

            imw, imh = image.size

            # Create a gradient mask for the mirrored image
            gradient = Image.new("L", (imw, imh), 0)
            draw = ImageDraw.Draw(gradient)
            for i in range(imh):
                alpha = int((i / imh) * 204)  # alpha goes from 0 to 204
                draw.rectangle((0, i, imw, i), fill=alpha)
            # Apply the mirror mask to the image
            imageBottomAlphaGradient = ImageChops.multiply(imageBottomAlpha, gradient)

            # Create a gradient mask for the fog
            gradient = Image.new("L", (imw, imh), 0)
            draw = ImageDraw.Draw(gradient)
            for i in range(imw):
                an = 255-data.fogNear
                af = 255-data.fogFar
                zl = img.data['zleft']
                zr = img.data['zright']
                zi = (i/imw)*(zr-zl)+zl
                znorm = (zi-znear)/(zfar-znear)
                alpha = znorm*(an-af)+af
                draw.rectangle((i, 0, i, imh), fill=int(alpha))
            # resultAlpha.show()
            imageTop.putalpha(ImageChops.multiply(imageTopAlpha, gradient))
            imageBottom.putalpha(ImageChops.multiply(imageBottomAlphaGradient, gradient))

            # Define the source and destination points
            src_points = [(imw, 0), (0, 0), (imw, imh), (0, imh)]
            dst_top = [
                img.data['top']['p1'],
                img.data['top']['p2'],
                img.data['top']['p3'],
                img.data['top']['p4'],
            ]
            dst_bottom = [
                img.data['bottom']['p1'],
                img.data['bottom']['p2'],
                img.data['bottom']['p3'],
                img.data['bottom']['p4'],
            ]
            def _transform(_img:Image, _dst:List) -> Image:
                return _img.transform(
                    (w, h), Image.Transform.PERSPECTIVE,
                    find_coeffs(_dst, src_points),
                    Image.Resampling.BICUBIC)
            img.data['imageTop'] = _transform(imageTop, dst_top)
            img.data['imageBottom'] = _transform(imageBottom, dst_bottom).filter(ImageFilter.BoxBlur(4))
            img.data['imageTopAlpha'] = _transform(imageTopAlpha, dst_top)
            img.data['imageBottomAlpha'] = _transform(imageBottomAlpha, dst_bottom).filter(ImageFilter.BoxBlur(4))

            def _customBlur(_img:Image, _alpha:Image) -> Image:
                thresholds = [(0,70), (70,150), (150,255)]
                blur_radius = [7, 4, 0]
                _out = Image.new("RGBA", _img.size, (0, 0, 0, 0))
                # Create a new image to store the blurred result
                for (_f,_t),_r in zip(thresholds,blur_radius):
                    # Create a mask for the current threshold
                    _mask = _alpha.point(lambda p: p if _f < p <= _t else 0)
                    # Apply Gaussian blur to the image using the mask
                    _blurred = _img.filter(ImageFilter.BoxBlur(radius=_r))
                    _blurred.putalpha(_mask)
                    # Composite the blurred image with the original image using the mask
                    _out = Image.alpha_composite(_out,_blurred)
                    #_alpha.show()
                    #_mask.show()
                    #_blurred.show()
                    #_out.show()
                    pass
                return _out

            img.data['imageBottom'] = _customBlur(
                img.data['imageBottom'], img.data['imageBottom'].split()[-1])

            # return image
            # Apply blur to the alpha channel
            # alpha = image.split()[-1]
            # alpha = alpha.filter(ImageFilter.GaussianBlur(radius=5))
            # image.putalpha(alpha)
            # image = image.filter(ImageFilter.GaussianBlur(radius=3))

            # Paste the processed image onto the output image

        # Create a new image with a transparent background
        outImage = Image.new("RGBA", (w, h), data.bgColor)

        # Apply the masks and Draw all the images
        for img in images:
            imageTop = img.data['imageTop']
            imageBottom = img.data['imageBottom']
            imageTopAlpha = imageTop.split()[-1]
            imageBottomAlpha = imageBottom.split()[-1]
            for maskImg in reversed(images):
                if img==maskImg:
                    break
                maskTop = ImageOps.invert(maskImg.data['imageTopAlpha'])
                maskBottom = ImageOps.invert(maskImg.data['imageBottomAlpha'])
                imageTopAlpha = ImageChops.multiply(imageTopAlpha, maskTop)
                imageBottomAlpha = ImageChops.multiply(imageBottomAlpha, maskTop)
                imageBottomAlpha = ImageChops.multiply(imageBottomAlpha, maskBottom)


            imageTop.putalpha(imageTopAlpha)
            imageBottom.putalpha(imageBottomAlpha)

            # imageBottom.show()

            # outImage.paste(imageBottom,box=None,mask=imageBottom)
            # outImage.paste(imageTop,box=None,mask=imageTop)

            outImage = Image.alpha_composite(outImage,imageBottom)
            outImage = Image.alpha_composite(outImage,imageTop)
            # imageBottom.show()

        return outImage

    def paintEvent(self, canvas):
        w,h = self.size()
        cx,cy=self._state.camera.x,self._state.camera.y
        canvas.drawTTkString(pos=(cx,cy),text=ttk.TTkString("😎"))
        # Draw Fov
        for y in range(cy):
            canvas.drawChar(char='/', pos=(cx+cy-y+1,y))
            canvas.drawChar(char='\\',pos=(cx-cy+y,y))
        for image in self._state.images:
            ix,iy,iw,ih = image.getBox()
            canvas.drawText(pos=(ix,iy-1),text=f"{image.tilt:.2f}", color=ttk.TTkColor.YELLOW)
            canvas.drawText(pos=(ix+5,iy-1),text=f"{image.fileName}", color=ttk.TTkColor.BLUE)
            if image == self._state.highlightedMovable:
                canvas.fill(pos=(ix,iy),size=(iw,ih),char='+',color=ttk.TTkColor.GREEN)
            elif image == self._state.currentMovable:
                canvas.fill(pos=(ix,iy),size=(iw,ih),char='+',color=ttk.TTkColor.YELLOW)
            else:
                canvas.fill(pos=(ix,iy),size=(iw,ih),char='+')
            if ih > iw > 1:
                for dy in range(ih):
                    dx = iw*dy//ih
                    if (
                        math.pi/2  < image.tilt < math.pi or
                        -math.pi/2 < image.tilt < 0 ):
                        canvas.drawChar(char='X',pos=(ix+dx,iy+dy))
                    else:
                        canvas.drawChar(char='X',pos=(ix+iw-dx,iy+dy))
            elif iw >= ih > 1:
                for dx in range(iw):
                    dy = ih*dx//iw
                    if (
                        math.pi/2  < image.tilt < math.pi or
                        -math.pi/2 < image.tilt < 0 ):
                        canvas.drawChar(char='X',pos=(ix+dx,iy+dy))
                    else:
                        canvas.drawChar(char='X',pos=(ix+iw-dx,iy+dy))

class _Preview(ttk.TTkWidget):
    __slots__ = ('_canvasImage')
    def __init__(self, **kwargs):
        self._canvasImage = ttk.TTkCanvas(width=20,height=3)
        self._canvasImage.drawText(pos=(0,0),text="Preview...")
        super().__init__(**kwargs)

    def updateCanvas(self, img:Image):
        w,h = img.size
        pixels = img.load()
        self._canvasImage.resize(w,h//2)
        self._canvasImage.updateSize()
        for x in range(w):
            for y in range(h//2):
                bg = 100 if (x//4+y//2)%2 else 150
                p1 = pixels[x,y*2]
                p2 = pixels[x,y*2+1]
                def _c2hex(p) -> str:
                    a = p[3]/255
                    r = int(bg*(1-a)+a*p[0])
                    g = int(bg*(1-a)+a*p[1])
                    b = int(bg*(1-a)+a*p[2])
                    return f"#{r<<16|g<<8|b:06x}"
                c = ttk.TTkColor.fgbg(_c2hex(p2),_c2hex(p1))
                self._canvasImage.drawChar(pos=(x,y), char='▄', color=c)
        self.update()

    def paintEvent(self, canvas):
        w,h = self.size()
        canvas.paintCanvas(self._canvasImage, (0,0,w,h), (0,0,w,h), (0,0,w,h))

class ControlPanel(ttk.TTkSplitter):
    __slots__ = (
        'previewPressed','renderPressed','_toolbox', '_previewImage')
    def __init__(self, **kwargs):
        self.previewPressed = ttk.pyTTkSignal(RenderData)
        self.renderPressed = ttk.pyTTkSignal(RenderData)
        super().__init__(**kwargs|{"orientation":ttk.TTkK.VERTICAL})
        self._previewImage = _Preview()

        self._toolbox = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"toolbox.tui.json"))
        self._toolbox.getWidgetByName("Btn_Render").clicked.connect(self._renderClicked)
        self._toolbox.getWidgetByName("Btn_Preview").clicked.connect(self._previewClicked)
        # self._toolbox.getWidgetByName("SB_CamY")
        # self._toolbox.getWidgetByName("SB_CamA")
        # self._toolbox.getWidgetByName("CB_Bg")
        # self._toolbox.getWidgetByName("BG_Color")
        self.addWidget(self._previewImage,size=5)
        self.addWidget(self._toolbox)
        self.addItem(ttk.TTkLayout())

    def drawPreview(self, img:Image):
        self._previewImage.updateCanvas(img)

    @ttk.pyTTkSlot()
    def _renderClicked(self):
        if self._toolbox.getWidgetByName("CB_Bg").isChecked():
            btnColor = self._toolbox.getWidgetByName("BG_Color").color()
            color = (*btnColor.fgToRGB(),255)
        else:
            color = (0,0,0,0)
        data = RenderData(
            cameraAngle=self._toolbox.getWidgetByName("SB_CamA").value(),
            cameraY=self._toolbox.getWidgetByName("SB_CamY").value(),
            fogNear=self._toolbox.getWidgetByName("SB_Fog_Near").value(),
            fogFar=self._toolbox.getWidgetByName("SB_Fog_Far").value(),
            bgColor=color,
            resolution=(800,600)
        )
        self.renderPressed.emit(data)

    @ttk.pyTTkSlot()
    def _previewClicked(self):
        if self._toolbox.getWidgetByName("CB_Bg").isChecked():
            btnColor = self._toolbox.getWidgetByName("BG_Color").color()
            color = (*btnColor.fgToRGB(),255)
        else:
            color = (0,0,0,0)
        w,h = self._previewImage.size()
        data = RenderData(
            cameraAngle=self._toolbox.getWidgetByName("SB_CamA").value(),
            cameraY=self._toolbox.getWidgetByName("SB_CamY").value(),
            fogNear=self._toolbox.getWidgetByName("SB_Fog_Near").value(),
            fogFar=self._toolbox.getWidgetByName("SB_Fog_Far").value(),
            bgColor=color,
            resolution=(w,h*2)
        )
        self.previewPressed.emit(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs='*',
                    help='the filename/s')
    args = parser.parse_args()

    ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

    root = ttk.TTk(
            layout=ttk.TTkGridLayout(),
            title="TTkode",
            mouseTrack=True)

    _images = []
    _camera = _Camera(x=25,y=25,z=5)
    for fileName in args.filename:
        d=len(_images)*2
        image = _Image(x=25+d,y=15+d, z=0, size=5, tilt=0,fileName=fileName)
        _camera.x += 1
        _camera.y += 1
        _images.append(image)

    _state = _State(
        camera=_camera,
        images=_images)

    perspectivator = Perspectivator(state=_state)
    controlPanel = ControlPanel()

    at = ttk.TTkAppTemplate()
    at.setWidget(widget=perspectivator,position=at.MAIN)
    at.setWidget(widget=controlPanel,position=at.RIGHT, size=30)

    root.layout().addWidget(at)

    def _preview(data):
        img = perspectivator.getImage(data)
        controlPanel.drawPreview(img)

    controlPanel.renderPressed.connect(perspectivator.render)
    controlPanel.previewPressed.connect(_preview)

    root.mainloop()

if __name__ == '__main__':
    main()