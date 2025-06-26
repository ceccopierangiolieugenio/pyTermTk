#!/usr/bin/env python3
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
import json

from dataclasses import dataclass
from typing import Optional,Tuple,List,Dict,Any

import numpy as np,array

from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

sys.path.append(os.path.join(sys.path[0],'../..'))

import TermTk as ttk

@dataclass
class RenderData:
    # fogNear: float
    # fogFar: float
    # bgColor: Tuple[int,int,int,int]
    resolution: Tuple[int,int]
    # outFile: str
    # offY: int
    # show: bool = False
    # mirror: Tuple[int,int]

class _ThreadingData:
    __slots__ = ('timer')
    timer: ttk.TTkTimer
    def __init__(self):
        self.timer = ttk.TTkTimer()

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)

    # Math from:
    #   https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
    #res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    res = np.linalg.solve(A,B)
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

class _Toolbox():
    __slots__ = ('widget', 'updated')
    updated:ttk.pyTTkSignal

    def __init__(self):
        self.updated = ttk.pyTTkSignal()
        self.widget = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"t.toolbox.tui.json"))

        @ttk.pyTTkSlot(str)
        def _presetChanged(preset):
            w,h = preset.split('x')
            self.widget.getWidgetByName("SB_HRes").setValue(int(w))
            self.widget.getWidgetByName("SB_VRes").setValue(int(h))

        pres = self.widget.getWidgetByName("CB_ResPresets")
        pres.addItems([
            '320x200', '320x240', '400x300', '512x384',
            '640x400', '640x480', '800x600', '1024x768',
            '1152x864', '1280x720', '1280x800', '1280x960',
            '1280x1024', '1360x768', '1366x768', '1400x1050',
            '1440x900', '1600x900', '1600x1200', '1680x1050',
            '1920x1080', '1920x1200', '2048x1152', '2048x1536',
            '2560x1080', '2560x1440', '2560x1600', '2880x1800',
            '3200x1800', '3440x1440', '3840x2160', '4096x2160',
            '5120x2880', '7680x4320'])
        pres.setCurrentIndex(6)
        pres.currentTextChanged.connect(_presetChanged)

        aa = self.widget.getWidgetByName("CB_AA")
        aa.addItems(['0X','2X','3X','4X'])
        aa.setCurrentIndex(0)

        self.widget.getWidgetByName("SB_HRes").valueChanged.connect(self._triggerUpdated)
        self.widget.getWidgetByName("SB_VRes").valueChanged.connect(self._triggerUpdated)
        self.widget.getWidgetByName("CB_Bg").stateChanged.connect(self._triggerUpdated)
        self.widget.getWidgetByName("BG_Color").colorSelected.connect(self._triggerUpdated)
        self.widget.getWidgetByName("SB_Fog_Near").valueChanged.connect(self._triggerUpdated)
        self.widget.getWidgetByName("SB_Fog_Far").valueChanged.connect(self._triggerUpdated)
        self.widget.getWidgetByName("SB_OffY").valueChanged.connect(self._triggerUpdated)
        self.widget.getWidgetByName("SB_FadingFrom").valueChanged.connect(self._triggerUpdated)
        self.widget.getWidgetByName("SB_FadingTo").valueChanged.connect(self._triggerUpdated)

    @ttk.pyTTkSlot()
    def _triggerUpdated(self):
        self.updated.emit()

    def mirror(self) -> Tuple[float,float]:
        return (
            self.widget.getWidgetByName("SB_FadingFrom").value() ,
            self.widget.getWidgetByName("SB_FadingTo").value()  )

    def bg(self) -> Tuple[int,int,int,int]:
        if self.widget.getWidgetByName("CB_Bg").isChecked():
            btnColor = self.widget.getWidgetByName("BG_Color").color()
            return (*btnColor.fgToRGB(),255)
        else:
            return (0,0,0,0)

    def fog(self) -> tuple[float,float]:
        return (
            self.widget.getWidgetByName("SB_Fog_Near").value() ,
            self.widget.getWidgetByName("SB_Fog_Far").value()  )

    def resolution(self) -> Tuple[int,int]:
        return(
            self.widget.getWidgetByName("SB_HRes").value(),
            self.widget.getWidgetByName("SB_VRes").value())

    def offset_y(self) -> float:
        return self.widget.getWidgetByName("SB_OffY").value()

    def serialize(self) -> Dict:
        return {
            'bg':self.bg(),
            'fog':self.fog(),
            'resolution':self.resolution(),
            'offset_y': self.offset_y(),
            'mirror': self.mirror(),
        }

    @staticmethod
    def deserialize(data:Dict) -> '_Toolbox':
        ret = _Toolbox()
        ret.widget.getWidgetByName("SB_HRes").setValue(data['resolution'][0])
        ret.widget.getWidgetByName("SB_VRes").setValue(data['resolution'][1])
        if data['bg']==[0,0,0,0]:
            ret.widget.getWidgetByName("CB_Bg").setChecked(False)
        else:
            ret.widget.getWidgetByName("CB_Bg").setChecked(True)
            r = data['bg'][0]
            g = data['bg'][1]
            b = data['bg'][2]
            color = ttk.TTkColor.fg(f"#{r<<16|g<<8|b:06x}")
            ret.widget.getWidgetByName("BG_Color").setColor(color)
        ret.widget.getWidgetByName("SB_Fog_Near").setValue(data['fog'][0])
        ret.widget.getWidgetByName("SB_Fog_Far").setValue(data['fog'][1])
        ret.widget.getWidgetByName("SB_OffY").setValue(data['offset_y'])
        ret.widget.getWidgetByName("SB_OffY").setValue(data['offset_y'])
        ret.widget.getWidgetByName("SB_FadingFrom").setValue(data['mirror'][0])
        ret.widget.getWidgetByName("SB_FadingTo").setValue(data['mirror'][1])
        return ret

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

    def serialize(self) -> Dict:
        return {
            'x':self._x,
            'y':self._y,
            'z':self._z,
            'name': self.name.text().toAscii()
        }

    @staticmethod
    def deserialize(data:Dict) -> '_Movable':
        return _Movable(**data)

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
        self._size = size
        self._tilt = tilt
        self.fileName = fileName
        super().__init__(**kwargs)
        self._loadStuff()

    def _loadStuff(self):
        self.widget = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"t.image.tui.json"))
        if not os.path.isfile(self.fileName):
            raise ValueError(f"{self.fileName} is not a file")
        try:
            self.image = Image.open(self.fileName).convert("RGBA")
        except FileNotFoundError:
            raise ValueError(f"Failed to open {self.fileName}")
        self._updateBox()
        self.widget.getWidgetByName("SB_X").valueChanged.connect(self.setX)
        self.widget.getWidgetByName("SB_Y").valueChanged.connect(self.setY)
        self.widget.getWidgetByName("SB_Z").valueChanged.connect(self.setZ)
        self.widget.getWidgetByName("SB_Tilt").valueChanged.connect(self.setTilt)
        self.widget.getWidgetByName("SB_Size").valueChanged.connect(self.setSize)
        self.updated.connect(self._updated)
        self._updated()

    def serialize(self) -> Dict:
        ret = super().serialize()
        return ret | {
            'size': self._size,
            'tilt': self._tilt,
            'fileName': self.fileName
        }

    @staticmethod
    def deserialize(data:Dict) -> '_Image':
        return _Image(**data)

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
        self._tilt = tilt
        super().__init__(**kwargs)
        self._loadStuff()

    def _loadStuff(self):
        self.widget = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"t.camera.tui.json"))
        self.widget.getWidgetByName("SB_X").valueChanged.connect(self.setX)
        self.widget.getWidgetByName("SB_Y").valueChanged.connect(self.setY)
        self.widget.getWidgetByName("SB_Z").valueChanged.connect(self.setZ)
        self.widget.getWidgetByName("SB_Tilt").valueChanged.connect(self.setTilt)
        self.updated.connect(self._updated)
        self._updated()

    def serialize(self) -> Dict:
        ret = super().serialize()
        return ret | {
            'tilt': self._tilt,
        }

    @staticmethod
    def deserialize(data:Dict) -> '_Camera':
        return _Camera(**data)

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
        'camera','images', 'toolbox',
        '_currentMovable','highlightedMovable',
        'currentMovableUpdated','updated')
    camera: _Camera
    images: List[_Image]
    _currentMovable: Optional[_Movable]
    highlightedMovable: Optional[_Movable]
    currentMovableUpdated: ttk.pyTTkSignal
    updated: ttk.pyTTkSignal
    def __init__(self, camera: _Camera, images: List[_Image], toolbox: Optional[_Toolbox]=None):
        if not toolbox:
            self.toolbox = _Toolbox()
        else:
            self.toolbox = toolbox
        self.currentMovableUpdated = ttk.pyTTkSignal(_Movable)
        self.updated = ttk.pyTTkSignal()
        self.camera = camera
        self.images = images
        self._currentMovable = None
        self.highlightedMovable = None
        self.camera.updated.connect(self.updated.emit)
        self.toolbox.updated.connect(self.updated.emit)
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

    @ttk.pyTTkSlot(str)
    def save(self, fileName):
        data = {
            'camera': self.camera.serialize(),
            'images': [img.serialize() for img in self.images],
            'toolbox': self.toolbox.serialize()
        }
        with open(fileName, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load(fileName) -> '_State':
        with open(fileName, "r") as f:
            data = json.load(f)
            toolbox = _Toolbox.deserialize(data['toolbox'])
            images = []
            for imgData in data['images']:
                images.append(_Image.deserialize(imgData))
            state = _State(
                toolbox=toolbox,
                camera=_Camera.deserialize(data['camera']),
                images=images)

            return state

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
            self._state.camera.data |= {
                'mx':self._state.camera.x()-evt.x,
                'my':self._state.camera.y()-evt.y}
        else:
            for image in self._state.images:
                ix,iy,iw,ih = image.getBox()
                if ix <= evt.x < ix+iw and iy <= evt.y < iy+ih:
                    image.data |= {
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
        screen_width, screen_height = data.resolution
        w,h = screen_width,screen_height

        fog = self._state.toolbox.fog()
        fogNear=fog[0]
        fogFar=fog[1]
        bgColor=self._state.toolbox.bg()
        offY=self._state.toolbox.offset_y()*h/600
        mirror = self._state.toolbox.mirror()

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
            img.data |= {
                'zleft':zleft,
                'zright':zright,
                'top' : {
                    'p1':(int((ip1x+1)*prw) , int(offY+(ip1y+1)*prh)),
                    'p2':(int((ip2x+1)*prw) , int(offY+(ip2y+1)*prh)),
                    'p3':(int((ip3x+1)*prw) , int(offY+(ip3y+1)*prh)),
                    'p4':(int((ip4x+1)*prw) , int(offY+(ip4y+1)*prh)),
                },
                'bottom' : {
                    'p1':(int((ip5x+1)*prw) , int(offY+(ip5y+1)*prh)),
                    'p2':(int((ip6x+1)*prw) , int(offY+(ip6y+1)*prh)),
                    'p3':(int((ip7x+1)*prw) , int(offY+(ip7y+1)*prh)),
                    'p4':(int((ip8x+1)*prw) , int(offY+(ip8y+1)*prh)),
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
            # Fading Math:
            # ----|--f--y___h-----t---
            # av = 1-(y-f)/(t-f)
            # bv = 1-(y+h-f)/(t-f)
            _f,_t = mirror
            if _f == _t:
                _f-=0.01
            _y = img.z()
            _h = img.size()*imh/imw
            _av = 1-(-_y-_f)/(_t-_f)
            _bv = 1-(-_y-_h-_f)/(_t-_f)
            for i in range(imh):
                _p = (i/imh)
                alpha = int(min(1,max(0,((_p)*_av+(1-_p)*_bv)))*255)  # alpha goes from 0 to 204
                draw.rectangle((0, i, imw, i), fill=alpha)
            # Apply the mirror mask to the image
            imageBottomAlphaGradient = ImageChops.multiply(imageBottomAlpha, gradient)

            # Create a gradient mask for the fog
            if zfar != znear:
                gradient = Image.new("L", (imw, imh), 0)
                draw = ImageDraw.Draw(gradient)
                for i in range(imw):
                    an = 255-fogNear
                    af = 255-fogFar
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
            blurRadius = (math.sqrt(w*h)*4/math.sqrt(800*600))
            img.data['imageTop'] = _transform(imageTop, dst_top)
            img.data['imageBottom'] = _transform(imageBottom, dst_bottom).filter(ImageFilter.BoxBlur(blurRadius))
            img.data['imageTopAlpha'] = _transform(imageTopAlpha, dst_top)
            img.data['imageBottomAlpha'] = _transform(imageBottomAlpha, dst_bottom).filter(ImageFilter.BoxBlur(blurRadius))

            # def _customBlur(_img:Image, _alpha:Image) -> Image:
            #     thresholds = [(0,70), (70,150), (150,255)]
            #     blur_radius = [7, 4, 0]
            #     _out = Image.new("RGBA", _img.size, (0, 0, 0, 0))
            #     # Create a new image to store the blurred result
            #     for (_f,_t),_r in zip(thresholds,blur_radius):
            #         # Create a mask for the current threshold
            #         _mask = _alpha.point(lambda p: p if _f < p <= _t else 0)
            #         # Apply Gaussian blur to the image using the mask
            #         _blurred = _img.filter(ImageFilter.BoxBlur(radius=_r))
            #         _blurred.putalpha(_mask)
            #         # Composite the blurred image with the original image using the mask
            #         _out = Image.alpha_composite(_out,_blurred)
            #         #_alpha.show()
            #         #_mask.show()
            #         #_blurred.show()
            #         #_out.show()
            #         pass
            #     return _out

            # img.data['imageBottom'] = _customBlur(
            #     img.data['imageBottom'], img.data['imageBottom'].split()[-1])

            # return image
            # Apply blur to the alpha channel
            # alpha = image.split()[-1]
            # alpha = alpha.filter(ImageFilter.GaussianBlur(radius=5))
            # image.putalpha(alpha)
            # image = image.filter(ImageFilter.GaussianBlur(radius=3))

            # Paste the processed image onto the output image

        # Create a new image with a transparent background
        outImage = Image.new("RGBA", (w, h), bgColor)

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
        'previewPressed','renderPressed','_toolbox', '_previewImage', '_state', '_movableLayout','_threadData')
    def __init__(self, state:_State, **kwargs):
        self._threadData:_ThreadingData = _ThreadingData()
        self.previewPressed = ttk.pyTTkSignal(RenderData)
        self.renderPressed = ttk.pyTTkSignal(RenderData)
        self._movableLayout = ttk.TTkGridLayout()
        self._movableLayout.addItem(ttk.TTkLayout(),2,0)
        self._state = state
        super().__init__(**kwargs|{"orientation":ttk.TTkK.VERTICAL})
        self._previewImage = _Preview()

        self._state.toolbox.widget.getWidgetByName("Btn_Render").clicked.connect(self._renderClicked)
        self._state.toolbox.widget.getWidgetByName("Btn_Preview").clicked.connect(self._previewChanged)
        self._state.toolbox.widget.getWidgetByName("Btn_SaveCfg").clicked.connect(self._saveCfg)
        self._state.updated.connect(self._previewChanged)
        self.addWidget(self._previewImage,size=5)
        self.addWidget(self._state.toolbox.widget)
        self.addItem(self._movableLayout)
        state.currentMovableUpdated.connect(self._movableChanged)
        self._threadData.timer.timeout.connect(self._previewThread)

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
    def _saveCfg(self):
        filePath = os.path.join(os.path.abspath('.'),'perspectivator.cfg.json')
        filePicker = ttk.TTkFileDialogPicker(
                pos = (3,3), size=(80,30),
                acceptMode=ttk.TTkK.AcceptMode.AcceptSave,
                caption="Save As...",
                fileMode=ttk.TTkK.FileMode.AnyFile,
                path=filePath,
                filter="TTk Tui Files (*.cfg.json);;Json Files (*.json);;All Files (*)")
        filePicker.pathPicked.connect(self._state.save)
        ttk.TTkHelper.overlay(None, filePicker, 5, 5, True)

    @ttk.pyTTkSlot()
    def _renderClicked(self):
        w,h = self._state.toolbox.resolution()
        # fog = self._state.toolbox.fog()
        mult = {
            '0X':1,'2X':2,'3X':3,'4X':4}.get(
               self._state.toolbox.widget.getWidgetByName("CB_AA").currentText(),1)
        waa = w*mult
        haa = h*mult
        data = RenderData(
            # outFile=self._state.toolbox.widget.getWidgetByName("LE_OutFile").text().toAscii(),
            # fogNear=fog[0],
            # fogFar=fog[1],
            # bgColor=self._state.toolbox.bg(),
            resolution=(waa,haa),
            # offY=self._state.toolbox.offset_y(),
            # show = self._state.toolbox.widget.getWidgetByName("CB_Show").isChecked(),
            # mirror = self._state.toolbox.mirror()
        )
        self.renderPressed.emit(data)

    @ttk.pyTTkSlot()
    def _previewChanged(self):
        if not self._state.toolbox.widget.getWidgetByName("Btn_Preview").isChecked():
            return
        self._threadData.timer.start()

    def _previewThread(self):
        w,h = self._previewImage.size()
        # fog = self._state.toolbox.fog()
        data = RenderData(
            # outFile=self._state.toolbox.widget.getWidgetByName("LE_OutFile").text().toAscii(),
            # fogNear=fog[0],
            # fogFar=fog[1],
            # bgColor=self._state.toolbox.bg(),
            resolution=(w,h*2),
            # offY=self._state.toolbox.offset_y(),
            # show = self._state.toolbox.widget.getWidgetByName("CB_Show").isChecked(),
            # mirror = self._state.toolbox.mirror()
        )
        self.previewPressed.emit(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs='+',
                    help='the images to compose or the json config file')
    args = parser.parse_args()

    ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

    root = ttk.TTk(
            layout=ttk.TTkGridLayout(),
            title="Perspectivator",
            mouseTrack=True)


    if len(args.filename) == 1 and  args.filename[0].endswith('.json'):
        _state = _State.load(args.filename[0])
    else:
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
    at.setWidget(widget=ttk.TTkLogViewer(),position=at.BOTTOM, size=4)

    root.layout().addWidget(at)

    def _render(data:RenderData):
        outImage = perspectivator.getImage(data)
        # outImage.save(filename='outImage.png')

        bbox = outImage.getbbox()
        if bbox:
            outImage = outImage.crop(bbox)

        outw,outh = _state.toolbox.resolution()
        cropw,croph = outImage.size

        outImage = outImage.resize((outw,outh*croph//cropw), Image.LANCZOS)
        outImage.save(_state.toolbox.widget.getWidgetByName("LE_OutFile").text().toAscii())
        if _state.toolbox.widget.getWidgetByName("CB_Show").isChecked():
            outImage.show()

    def _preview(data):
        img = perspectivator.getImage(data)
        controlPanel.drawPreview(img)

    controlPanel.renderPressed.connect(_render)
    controlPanel.previewPressed.connect(_preview)

    root.mainloop()

if __name__ == '__main__':
    main()