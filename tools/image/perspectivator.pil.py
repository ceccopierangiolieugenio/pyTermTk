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
from typing import Optional,Tuple,List,Dict,Any

import numpy as np,array

from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

sys.path.append(os.path.join(sys.path[0],'../..'))

import TermTk as ttk

@dataclass
class RenderData:
    fogNear: float
    fogFar: float
    bgColor: Tuple[int,int,int,int]
    resolution: Tuple[int,int]
    outFile: str
    show: bool = False


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
    if np.all(np.isnan(right)):
        right = [0,1,0]
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

class _Movable():
    __slots__ = ('_x','_y','_z','data', 'selected', 'name','widget', 'updated')
    _x:int
    _y:int
    _z:int
    data:Dict[str,Any]
    selected:ttk.pyTTkSignal
    updated:ttk.pyTTkSignal
    name:ttk.TTkLabel
    widget:ttk.TTkWidget

    def __init__(self, x:int=0,y:int=0,z:int=0, name:str=""):
        self.selected = ttk.pyTTkSignal(_Movable)
        self.updated = ttk.pyTTkSignal()
        self.data = {}
        self._x = x
        self._y = y
        self._z = z
        self.name = ttk.TTkLabel(text=ttk.TTkString(name),maxHeight=1)
        self.widget = ttk.TTkWidget()

    def x(self) -> int:
        return self._x
    def setX(self, value:int):
        self._x = value
        self._updateBox()
        self.updated.emit()

    def y(self) -> int:
        return self._y
    def setY(self, value:int):
        self._y = value
        self._updateBox()
        self.updated.emit()

    def z(self) -> int:
        return self._z
    def setZ(self, value:int):
        self._z = value
        self._updateBox()
        self.updated.emit()

    def getBox(self) -> Tuple[int,int,int,int]:
        return (self.x-1,self._y,4,1)

    def _updateBox(self):
        pass

class _Image(_Movable):
    __slots__ = ('_size','_tilt','fileName', 'box', 'image')
    _size:int
    _tilt:float
    fileName:str
    image:Image
    box:Tuple[int,int,int,int]
    def __init__(self,size:int,tilt:float,fileName:str, **kwargs):
        super().__init__(**kwargs)
        self.widget = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"t.image.tui.json"))
        if not os.path.isfile(fileName):
            raise ValueError(f"{fileName} is not a file")
        try:
            self.image = Image.open(fileName).convert("RGBA")
        except FileNotFoundError:
            raise ValueError(f"Failed to open {fileName}")
        self._size = size
        self._tilt = tilt
        self.fileName = fileName
        self._updateBox()
        self.widget.getWidgetByName("SB_X").valueChanged.connect(self.setX)
        self.widget.getWidgetByName("SB_Y").valueChanged.connect(self.setY)
        self.widget.getWidgetByName("SB_Z").valueChanged.connect(self.setZ)
        self.widget.getWidgetByName("SB_Tilt").valueChanged.connect(self.setTilt)
        self.widget.getWidgetByName("SB_Size").valueChanged.connect(self.setSize)
        self.updated.connect(self._updated)
        self._updated()

    @ttk.pyTTkSlot()
    def _updated(self):
        self.widget.getWidgetByName("SB_X").setValue(self._x)
        self.widget.getWidgetByName("SB_Y").setValue(self._y)
        self.widget.getWidgetByName("SB_Z").setValue(self._z)
        self.widget.getWidgetByName("SB_Tilt").setValue(self._tilt)
        self.widget.getWidgetByName("SB_Size").setValue(self._size)

    def size(self) -> int:
        return self._size
    def setSize(self, value:int):
        self._size = value
        self._updateBox()
        self.updated.emit()

    def tilt(self) -> float:
        return self._tilt
    def setTilt(self, value:float):
        self._tilt = value
        self._updateBox()
        self.updated.emit()

    def _updateBox(self):
        size = float(self._size)
        w = 1 + 2*size*abs(math.cos(self._tilt))
        h = 1 +   size*abs(math.sin(self._tilt))
        self.box = (
                int(self._x-w/2),
                int(self._y-h/2),
                int(w), int(h),
            )

    def getBox(self) -> Tuple[int,int,int,int]:
        return self.box

class _Camera(_Movable):
    __slots__= ('_tilt')
    _tilt:float
    def __init__(self, tilt:float=0, **kwargs):
        super().__init__(**kwargs)
        self.widget = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"t.camera.tui.json"))
        self._tilt = tilt
        self.widget.getWidgetByName("SB_X").valueChanged.connect(self.setX)
        self.widget.getWidgetByName("SB_Y").valueChanged.connect(self.setY)
        self.widget.getWidgetByName("SB_Z").valueChanged.connect(self.setZ)
        self.widget.getWidgetByName("SB_Tilt").valueChanged.connect(self.setTilt)
        self.updated.connect(self._updated)
        self._updated()

    @ttk.pyTTkSlot()
    def _updated(self):
        self.widget.getWidgetByName("SB_X").setValue(self._x)
        self.widget.getWidgetByName("SB_Y").setValue(self._y)
        self.widget.getWidgetByName("SB_Z").setValue(self._z)
        self.widget.getWidgetByName("SB_Tilt").setValue(self._tilt)

    def tilt(self) -> float:
        return self._tilt
    def setTilt(self, value:float):
        self._tilt = value
        self.updated.emit()

class _State():
    __slots__ = (
        'camera','images',
        '_currentMovable','highlightedMovable',
        'currentMovableUpdated','updated')
    camera: _Camera
    images: List[_Image]
    _currentMovable: Optional[_Movable]
    highlightedMovable: Optional[_Movable]
    currentMovableUpdated: ttk.pyTTkSignal
    updated: ttk.pyTTkSignal
    def __init__(self, camera: _Camera, images: List[_Image]):
        self.currentMovableUpdated = ttk.pyTTkSignal(_Movable)
        self.updated = ttk.pyTTkSignal()
        self.camera = camera
        self.images = images
        self._currentMovable = None
        self.highlightedMovable = None
        self.camera.updated.connect(self.updated.emit)
        for img in images:
            img.updated.connect(self.updated.emit)

    @property
    def currentMovable(self) -> Optional[_Movable]:
        return self._currentMovable
    @currentMovable.setter
    def currentMovable(self, value: Optional[_Movable]):
        if self._currentMovable != value:
            self._currentMovable = value
        if value:
            self.currentMovableUpdated.emit(value)

class Perspectivator(ttk.TTkWidget):
    __slots__ = ('_state')
    _state:_State
    def __init__(self, state:_State, **kwargs):
        self._state = state
        super().__init__(**kwargs)
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        state.updated.connect(self.update)

    def mousePressEvent(self, evt):
        self._state.highlightedMovable = None
        self._state.currentMovable = None
        cx,cy = self._state.camera.x(),self._state.camera.y()
        if cx-1 <= evt.x <= cx+2 and cy-1 <= evt.y <= cy+1:
            self._state.currentMovable = self._state.camera
            self._state.camera.data = {
                'mx':self._state.camera.x()-evt.x,
                'my':self._state.camera.y()-evt.y}
        else:
            for image in self._state.images:
                ix,iy,iw,ih = image.getBox()
                if ix <= evt.x < ix+iw and iy <= evt.y < iy+ih:
                    image.data = {
                        'mx':image.x()-evt.x,
                        'my':image.y()-evt.y}
                    self._state.currentMovable = image
                    index = self._state.images.index(image)
                    self._state.images.pop(index)
                    self._state.images.append(image)
                    break
        if self._state.currentMovable:
            self._state.currentMovable.selected.emit(self._state.currentMovable)
        self.update()
        return True

    def mouseMoveEvent(self, evt:ttk.TTkMouseEvent):
        self._state.highlightedMovable = None
        cx,cy = self._state.camera.x(),self._state.camera.y()
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
            x = evt.x-movable.x()
            y = evt.y-movable.y()
            movable.setTilt(math.atan2(x,y*2))
            self.update()
        elif evt.key == ttk.TTkK.LeftButton:
            mx,my = movable.data['mx'],movable.data['my']
            movable.setX(evt.x+mx)
            movable.setY(evt.y+my)
            self.update()
        return True

    def wheelEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        if not ((image:=self._state.highlightedMovable) and isinstance(image,_Image)):
            pass
        elif evt.evt == ttk.TTkK.WHEEL_Up:
            image.setSize(min(image.size()+1,50))
            self.update()
        elif evt.evt == ttk.TTkK.WHEEL_Down:
            image.setSize(max(image.size()-1,5))
            self.update()
        return True

    def getImage(self, data:RenderData) -> Image:
        return self.getImagePil(data)

    def getImagePil(self, data:RenderData) -> Image:
        ww,wh = self.size()
        cam_x = self._state.camera.x()
        cam_y = self._state.camera.y()
        cam_z = self._state.camera.z()
        cam_tilt = self._state.camera.tilt()
        observer = (cam_x , cam_z , cam_y )  # Observer's position
        # observer = (ww/2 , -data.cameraY , wh-3 )  # Observer's position
        dz = 10*math.cos(math.pi * cam_tilt/360)
        dy = 10*math.sin(math.pi * cam_tilt/360)
        look_at  = (cam_x , cam_z-dy, cam_y+dz)  # Observer is looking along the positive Z-axis
        screen_width, screen_height = data.resolution
        w,h = screen_width,screen_height
        prw,prh = screen_width/2, screen_height/2

        # step1, sort Images based on the distance
        images = sorted(self._state.images,key=lambda img:img.getBox()[1])
        znear,zfar = 0xFFFFFFFF,-0xFFFFFFFF
        for img in images:
            ix,iy,iw,ih = img.getBox()
            iz = img.z()
            ih-=1
            znear=min(znear,iy,iy+ih)
            zfar=max(zfar,iy,iy+ih)
            isz = img.size()*2
            if math.pi/2 <= img.tilt() < math.pi or -math.pi <= img.tilt() < 0:
                zleft = iy
                zright = iy+ih
                ip1x,ip1y =  project_point(observer,look_at,(ix+iw ,  iz+isz , iy+ih ))
                ip2x,ip2y =  project_point(observer,look_at,(ix    ,  iz+isz , iy    ))
                ip3x,ip3y =  project_point(observer,look_at,(ix+iw ,  iz     , iy+ih ))
                ip4x,ip4y =  project_point(observer,look_at,(ix    ,  iz     , iy    ))
                ip5x,ip5y =  project_point(observer,look_at,(ix+iw , -iz-isz , iy+ih ))
                ip6x,ip6y =  project_point(observer,look_at,(ix    , -iz-isz , iy    ))
                ip7x,ip7y =  project_point(observer,look_at,(ix+iw , -iz     , iy+ih ))
                ip8x,ip8y =  project_point(observer,look_at,(ix    , -iz     , iy    ))
            else:
                zleft = iy+ih
                zright = iy
                ip1x,ip1y =  project_point(observer,look_at,(ix+iw ,  iz+isz , iy    ))
                ip2x,ip2y =  project_point(observer,look_at,(ix    ,  iz+isz , iy+ih ))
                ip3x,ip3y =  project_point(observer,look_at,(ix+iw ,  iz     , iy    ))
                ip4x,ip4y =  project_point(observer,look_at,(ix    ,  iz     , iy+ih ))
                ip5x,ip5y =  project_point(observer,look_at,(ix+iw , -iz-isz , iy    ))
                ip6x,ip6y =  project_point(observer,look_at,(ix    , -iz-isz , iy+ih ))
                ip7x,ip7y =  project_point(observer,look_at,(ix+iw , -iz     , iy    ))
                ip8x,ip8y =  project_point(observer,look_at,(ix    , -iz     , iy+ih ))
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
        cx,cy=self._state.camera.x(),self._state.camera.y()
        if self._state.highlightedMovable == self._state.camera:
            canvas.drawTTkString(pos=(cx-1,cy),text=ttk.TTkString("<😘>"))
        elif self._state.currentMovable == self._state.camera:
            canvas.drawTTkString(pos=(cx,cy),text=ttk.TTkString("😍"))
        else:
            canvas.drawTTkString(pos=(cx,cy),text=ttk.TTkString("😎"))

        # Draw Fov
        for y in range(cy):
            canvas.drawChar(char='/', pos=(cx+cy-y+1,y))
            canvas.drawChar(char='\\',pos=(cx-cy+y,y))

        # Draw Images
        for image in self._state.images:
            ix,iy,iw,ih = image.getBox()
            canvas.drawText(pos=(ix,iy-1),text=f"{image.tilt():.2f}", color=ttk.TTkColor.YELLOW)
            canvas.drawText(pos=(ix+5,iy-1),text=f"{image.fileName}", color=ttk.TTkColor.CYAN)
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
                        math.pi/2  < image.tilt() < math.pi or
                        -math.pi/2 < image.tilt() < 0 ):
                        canvas.drawChar(char='X',pos=(ix+dx,iy+dy))
                    else:
                        canvas.drawChar(char='X',pos=(ix+iw-dx,iy+dy))
            elif iw >= ih > 1:
                for dx in range(iw):
                    dy = ih*dx//iw
                    if (
                        math.pi/2  < image.tilt() < math.pi or
                        -math.pi/2 < image.tilt() < 0 ):
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
        'previewPressed','renderPressed','_toolbox', '_previewImage', '_state', '_movableLayout')
    def __init__(self, state:_State, **kwargs):
        self.previewPressed = ttk.pyTTkSignal(RenderData)
        self.renderPressed = ttk.pyTTkSignal(RenderData)
        self._movableLayout = ttk.TTkGridLayout()
        self._movableLayout.addItem(ttk.TTkLayout(),2,0)
        self._state = state
        super().__init__(**kwargs|{"orientation":ttk.TTkK.VERTICAL})
        self._previewImage = _Preview()

        self._toolbox = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"t.toolbox.tui.json"))
        self._toolbox.getWidgetByName("Btn_Render").clicked.connect(self._renderClicked)
        self._toolbox.getWidgetByName("Btn_Preview").clicked.connect(self._previewClicked)
        # self._toolbox.getWidgetByName("SB_CamY")
        # self._toolbox.getWidgetByName("SB_CamA")
        # self._toolbox.getWidgetByName("CB_Bg")
        # self._toolbox.getWidgetByName("BG_Color")
        self.addWidget(self._previewImage,size=5)
        self.addWidget(self._toolbox)
        self.addItem(self._movableLayout)
        state.currentMovableUpdated.connect(self._movableChanged)
        pres:ttk.TTkComboBox = self._toolbox.getWidgetByName("CB_ResPresets")

        @ttk.pyTTkSlot(str)
        def _presetChanged(preset):
            w,h = preset.split('x')
            self._toolbox.getWidgetByName("SB_HRes").setValue(int(w))
            self._toolbox.getWidgetByName("SB_VRes").setValue(int(h))

        pres.addItems(['320x240','800x600','1024x768','1280x1024'])
        pres.setCurrentIndex(1)
        pres.currentTextChanged.connect(_presetChanged)

    @ttk.pyTTkSlot(_Movable)
    def _movableChanged(self, movable:_Movable):
        if isinstance(movable,_Movable):
            self._movableLayout.addWidget(movable.name,0,0)
            self._movableLayout.addWidget(movable.widget,1,0)
        else:
            raise ValueError(f"Unknown movable {movable}")

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
            outFile=self._toolbox.getWidgetByName("LE_OutFile").text().toAscii(),
            fogNear=self._toolbox.getWidgetByName("SB_Fog_Near").value(),
            fogFar=self._toolbox.getWidgetByName("SB_Fog_Far").value(),
            bgColor=color,
            resolution=(
                    self._toolbox.getWidgetByName("SB_HRes").value(),
                    self._toolbox.getWidgetByName("SB_VRes").value()),
            show = self._toolbox.getWidgetByName("CB_Show").isChecked()
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
            outFile=self._toolbox.getWidgetByName("LE_OutFile").text().toAscii(),
            fogNear=self._toolbox.getWidgetByName("SB_Fog_Near").value(),
            fogFar=self._toolbox.getWidgetByName("SB_Fog_Far").value(),
            bgColor=color,
            resolution=(w,h*2),
            show = self._toolbox.getWidgetByName("CB_Show").isChecked()
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
    _camera = _Camera(x=25,y=25,z=5, name="Camera")
    for fileName in args.filename:
        d=len(_images)*2
        image = _Image(x=25+d,y=15+d, z=0, size=5, tilt=0,fileName=fileName, name=fileName)
        _camera.setX(_camera.x()+1)
        _camera.setY(_camera.y()+1)
        _images.append(image)

    _state = _State(
        camera=_camera,
        images=_images)

    perspectivator = Perspectivator(state=_state)
    controlPanel = ControlPanel(state=_state)

    at = ttk.TTkAppTemplate()
    at.setWidget(widget=perspectivator,position=at.MAIN)
    at.setWidget(widget=controlPanel,position=at.RIGHT, size=30)

    root.layout().addWidget(at)

    def _render(data:RenderData):
        outImage = perspectivator.getImage(data)
        # outImage.save(filename='outImage.png')
        outImage.save(data.outFile)
        if data.show:
            outImage.show()

    def _preview(data):
        img = perspectivator.getImage(data)
        controlPanel.drawPreview(img)

    controlPanel.renderPressed.connect(_render)
    controlPanel.previewPressed.connect(_preview)

    root.mainloop()

if __name__ == '__main__':
    main()