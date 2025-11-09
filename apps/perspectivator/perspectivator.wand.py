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

from PIL import ImageDraw, ImageFilter

import numpy as np

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

# from PIL import Image, ImageDraw, ImageFilter




sys.path.append(os.path.join(sys.path[0],'../..'))

import TermTk as ttk

@dataclass
class RenderData:
    cameraY: int
    cameraAngle: float
    bgColor: Tuple[int,int,int,int]
    resolution: Tuple[int,int]

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

def project_3d_to_2d(observer, look_at, fov_h, fov_v, screen_width, screen_height, point_3d):
    """
    Project a 3D point onto a 2D screen.

    Args:
        observer: The observer's position in 3D space (x, y, z).
        look_at: The point the observer is looking at in 3D space (x, y, z).
        fov_h: Horizontal field of view in radians.
        fov_v: Vertical field of view in radians.
        screen_width: Width of the 2D screen.
        screen_height: Height of the 2D screen.
        point_3d: The 3D point to project (x, y, z).

    Returns:
        The 2D coordinates of the projected point (x, y) on the screen.
    """
    # Step 1: Calculate the forward, right, and up vectors
    def normalize(v):
        length = math.sqrt(sum(coord ** 2 for coord in v))
        return tuple(coord / length for coord in v)

    forward = normalize((look_at[0] - observer[0], look_at[1] - observer[1], look_at[2] - observer[2]))
    right = normalize((
        forward[1] * 0 - forward[2] * 1,
        forward[2] * 0 - forward[0] * 0,
        forward[0] * 1 - forward[1] * 0
    ))
    up = (
        right[1] * forward[2] - right[2] * forward[1],
        right[2] * forward[0] - right[0] * forward[2],
        right[0] * forward[1] - right[1] * forward[0]
    )

    # Step 2: Transform the 3D point into the observer's coordinate system
    relative_point = (
        point_3d[0] - observer[0],
        point_3d[1] - observer[1],
        point_3d[2] - observer[2]
    )
    x_in_view = sum(relative_point[i] * right[i] for i in range(3))
    y_in_view = sum(relative_point[i] * up[i] for i in range(3))
    z_in_view = sum(relative_point[i] * forward[i] for i in range(3))

    # Step 3: Perform perspective projection
    if z_in_view <= 0:
        raise ValueError("The point is behind the observer and cannot be projected.")

    aspect_ratio = screen_width / screen_height
    tan_fov_h = math.tan(fov_h / 2)
    tan_fov_v = math.tan(fov_v / 2)

    ndc_x = x_in_view / (z_in_view * tan_fov_h * aspect_ratio)
    ndc_y = y_in_view / (z_in_view * tan_fov_v)

    # Step 4: Map normalized device coordinates (NDC) to screen coordinates
    screen_x = (ndc_x + 1) / 2 * screen_width
    screen_y = (1 - ndc_y) / 2 * screen_height

    return int(screen_x), int(screen_y)

class _Image():
    __slots__ = ('x','y','size','tilt','fileName', 'box', 'data')
    x:int
    y:int
    size:int
    tilt:float
    fileName:str
    data:Dict
    box:Tuple[int,int,int,int]
    def __init__(self,x:int,y:int,size:int,tilt:float,fileName:str):
        if not os.path.isfile(fileName):
            raise ValueError(f"{fileName} is not a file")
        self.x = x
        self.y = y
        self.size = size
        self.tilt = tilt
        self.fileName = fileName
        self.data={}
        self._updateBox()

    def _updateBox(self):
        size:float = float(self.size)
        w:float = 1 + 2*size*abs(math.cos(self.tilt))
        h:float = 1 +   size*abs(math.sin(self.tilt))
        self.box = (
                int(self.x-w/2),
                int(self.y-h/2),
                int(w), int(h),
            )

    def getBox(self) -> Tuple[int,int,int,int]:
        return self.box

class Perspectivator(ttk.TTkWidget):
    __slots__ = ('_images','_currentImage','_highlightedImage')
    _highlightedImage:Optional[_Image]
    _currentImage:Optional[_Image]
    _images:List[_Image]
    def __init__(self, **kwargs):
        self._highlightedImage = None
        self._currentImage = None
        self._images = []
        super().__init__(**kwargs)
        self.setFocusPolicy(ttk.TTkK.ClickFocus)

    def addImage(self, fileName:str):
        d=len(self._images)*2
        image = _Image(x=25+d,y=5+d, size=5, tilt=0,fileName=fileName)
        self._images.append(image)
        self.update()

    def mousePressEvent(self, evt):
        self._highlightedImage = None
        self._currentImage = None
        for image in self._images:
            ix,iy,iw,ih = image.getBox()
            if ix <= evt.x < ix+iw and iy <= evt.y < iy+ih:
                image.data = {
                    'mx':image.x-evt.x,
                    'my':image.y-evt.y}
                self._currentImage = image
                index = self._images.index(image)
                self._images.pop(index)
                self._images.append(image)
                break
        self.update()
        return True

    def mouseMoveEvent(self, evt:ttk.TTkMouseEvent):
        self._highlightedImage = None
        for image in self._images:
            ix,iy,iw,ih = image.getBox()
            if ix <= evt.x < ix+iw and iy <= evt.y < iy+ih:
                self._highlightedImage = image
                break
        self.update()
        return True

    def mouseReleaseEvent(self, evt:ttk.TTkMouseEvent):
        self._highlightedImage = None
        self._currentImage = None
        self.update()
        return True

    def mouseDragEvent(self, evt:ttk.TTkMouseEvent):
        if not (image:=self._currentImage):
            pass
        elif evt.key == ttk.TTkK.RightButton:
            x = evt.x-image.x
            y = evt.y-image.y
            image.tilt = math.atan2(x,y*2)
            image._updateBox()
            self.update()
        elif evt.key == ttk.TTkK.LeftButton:
            mx,my = image.data['mx'],image.data['my']
            image.x = evt.x+mx
            image.y = evt.y+my
            image._updateBox()
            self.update()
        return True

    def wheelEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        if not (image:=self._highlightedImage):
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
        outImage.save(filename='outImage.png')
        # outImage.save('outImage.png')

    def getImage(self, data:RenderData) -> Image:
        return self.getImageWand(data)

    def getImageWand(self, data:RenderData) -> Image:
        ww,wh = self.size()
        observer = (ww/2 , -data.cameraY , wh-3 )  # Observer's position
        dz = 10*math.cos(math.pi + math.pi * data.cameraAngle/360)
        dy = 10*math.sin(math.pi + math.pi * data.cameraAngle/360)
        look_at  = (ww/2 , dy-data.cameraY , wh-3+dz)  # Observer is looking along the positive Z-axis
        screen_width, screen_height = data.resolution
        w,h = screen_width,screen_height
        prw,prh = screen_width/2, screen_height/2

        # step1, sort Images based on the distance
        images = sorted(self._images,key=lambda img:img.getBox()[1])
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

        # with Image(width=w, height=h, background=Color('yellow')) as outImage:
        # with Image(width=w, height=h, background=Color(f'rgba{data.bgColor}')) as outImage:
        # with Image(width=w, height=h) as outImage:
        outImage = Image(width=w, height=h, background=Color(f'rgba{data.bgColor}'))

        # step2, render the mirrored images
        for img in images:
            with Image(filename=img.fileName) as image:
                image.background_color = Color('transparent')
                image.virtual_pixel = 'background'
                imw,imh = image.width, image.height
                # with Image(width=imw, height=imh) as gradient:
                with Image(width=imw, height=imh, pseudo='gradient:rgba(0,0,0,0)-rgba(1,1,1,0.8)') as gradient:
                    gradient.alpha_channel = 'activate'
                    # outImage.composite(gradient,0,0)
                    gradient.transparent_color(Color('white'), alpha=0.0, fuzz=0)
                    # Apply the mask to the image
                    image.composite_channel('alpha', gradient, 'copy_alpha', 0, 0)
                prw,prh = screen_width/2, screen_height/2
                image.distort('perspective', [
                    #   From:   to:
                        imw , 0   , *img.data['bottom']['p1'] ,
                        0   , 0   , *img.data['bottom']['p2'] ,
                        imw , imh , *img.data['bottom']['p3'] ,
                        0   , imh , *img.data['bottom']['p4']
                        ])
                # # Mask the image
                # image.alpha_channel = 'activate'
                # for maskImg in reversed(images):
                #     if img==maskImg:
                #         break
                #     with Drawing() as draw:
                #         # draw.fill_color = Color('rgba(0, 0, 1, 0.5)')
                #         draw.fill_color = Color('transparent')
                #         draw.fill_opacity = 0.1  # Fully opaque
                #         points = [
                #                 maskImg.data['bottom']['p1'],
                #                 maskImg.data['bottom']['p2'],
                #                 maskImg.data['bottom']['p4'],
                #                 maskImg.data['bottom']['p3'],
                #             ]
                #         draw.polygon(points)
                #         draw(image)
                # Mask the image
                image.alpha_channel = 'activate'
                for maskImg in reversed(images):
                    if img==maskImg:
                        break
                    with Image(width=imw, height=imh, background=Color('transparent')) as transparent_img:
                        with Drawing() as draw:
                            draw.fill_color = Color('black')  # Opaque
                            draw.fill_opacity = 1.0  # Fully opaque
                            draw.stroke_color = Color('black')
                            draw.stroke_width = 0
                            points = [
                                    maskImg.data['top']['p1'],
                                    maskImg.data['top']['p2'],
                                    maskImg.data['top']['p4'],
                                    maskImg.data['top']['p3'],
                                ]
                            draw.polygon(points)
                            points = [
                                    maskImg.data['bottom']['p1'],
                                    maskImg.data['bottom']['p2'],
                                    maskImg.data['bottom']['p4'],
                                    maskImg.data['bottom']['p3'],
                                ]
                            draw.polygon(points)
                            draw(transparent_img)
                        image.composite(transparent_img, left=0, top=0, operator='dst_out')


                # Blur the mirrored image based on the alpha
                alpha_channel = image.clone()
                alpha_channel.alpha_channel = 'extract'
                alpha_channel.blur(radius=5, sigma=3)
                image.composite_channel(channel='alpha', image=alpha_channel, operator='copy_alpha')
                image.blur(radius=5, sigma=3)

                outImage.composite(image,0,0)

        # step3, render the top images
        for img in images:
            with Image(filename=img.fileName) as image:
                image.background_color = Color('transparent')
                image.virtual_pixel = 'background'
                imw,imh = image.width, image.height

                if zfar-znear != 0:
                    zl = 180 + 75*(img.data['zleft']-znear )/(zfar-znear)
                    zr = 180 + 75*(img.data['zright']-znear)/(zfar-znear)
                else:
                    zl=zr=255

                # apply gradient transparency based on the distance
                with Image(width=imh, height=imw, pseudo=f'gradient:rgba({zl},{zl},{zl},1)-rgba({zr},{zr},{zr},1)') as gradient:
                    gradient.rotate(-90)
                    # image.composite(gradient)
                    alphaImage = image.clone()
                    alphaImage.alpha_channel = 'extract'
                    alphaImage.composite(gradient,left=0,top=0,operator='multiply')
                    alphaImage.alpha_channel = 'copy'
                    image.composite_channel(channel='alpha', image=alphaImage, operator='copy_alpha')

                prw,prh = screen_width/2, screen_height/2
                image.distort('perspective', [
                    #   From:   to:
                        imw , 0   , *img.data['top']['p1'] ,
                        0   , 0   , *img.data['top']['p2'] ,
                        imw , imh , *img.data['top']['p3'] ,
                        0   , imh , *img.data['top']['p4']
                        ])

                image.alpha_channel = 'activate'
                for maskImg in reversed(images):
                    if img==maskImg:
                        break
                    with Image(width=imw, height=imh, background=Color('transparent')) as transparent_img:
                        with Drawing() as draw:
                            draw.fill_color = Color('black')  # Opaque
                            draw.fill_opacity = 1.0  # Fully opaque
                            draw.stroke_color = Color('black')
                            draw.stroke_width = 0
                            points = [
                                    maskImg.data['top']['p1'],
                                    maskImg.data['top']['p2'],
                                    maskImg.data['top']['p4'],
                                    maskImg.data['top']['p3'],
                                ]
                            draw.polygon(points)
                            draw(transparent_img)
                        image.composite(transparent_img, left=0, top=0, operator='dst_out')

                outImage.composite(image,0,0)
        return outImage


    def getImagePil(self, data:RenderData) -> Image:
        ww,wh = self.size()
        observer = (ww/2 , -data.cameraY , wh-3 )  # Observer's position
        dz = 10*math.cos(math.pi + math.pi * data.cameraAngle/360)
        dy = 10*math.sin(math.pi + math.pi * data.cameraAngle/360)
        look_at  = (ww/2 , dy-data.cameraY , wh-3+dz)  # Observer is looking along the positive Z-axis
        screen_width, screen_height = data.resolution
        w,h = screen_width,screen_height
        prw,prh = screen_width/2, screen_height/2

        # step1, sort Images based on the distance
        images = sorted(self._images,key=lambda img:img.getBox()[1])
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

        # Create a new image with a transparent background
        outImage = Image.new("RGBA", (w, h), data.bgColor)

        # step2, render the mirrored images
        for img in images:
            try:
                image = Image.open(img.fileName).convert("RGBA")
            except FileNotFoundError:
                print(f"Error: File not found: {img.fileName}")
                continue

            imw, imh = image.size

            # Create a gradient mask
            gradient = Image.new("L", (imw, imh), 0)
            draw = ImageDraw.Draw(gradient)
            for i in range(imh):
                alpha = int((i / imh) * 204)  # alpha goes from 0 to 204
                draw.rectangle((0, i, imw, i), fill=alpha)

            # Apply the gradient mask to the image
            image.putalpha(gradient)

            # Perspective distortion
            points_bottom = [
                img.data['bottom']['p1'][0], img.data['bottom']['p1'][1],
                img.data['bottom']['p2'][0], img.data['bottom']['p2'][1],
                img.data['bottom']['p3'][0], img.data['bottom']['p3'][1],
                img.data['bottom']['p4'][0], img.data['bottom']['p4'][1]
            ]
            image = image.transform((w, h), Image.PERSPECTIVE, points_bottom, Image.BILINEAR)

            # Apply blur to the alpha channel
            alpha = image.split()[-1]
            alpha = alpha.filter(ImageFilter.GaussianBlur(radius=5))
            image.putalpha(alpha)
            image = image.filter(ImageFilter.GaussianBlur(radius=3))

            # Paste the processed image onto the output image
            outImage.paste(image, (0, 0), image)
        return outImage
        # step3, render the top images
        for img in images:
            try:
                image = Image.open(img.fileName).convert("RGBA")
            except FileNotFoundError:
                print(f"Error: File not found: {img.fileName}")
                continue

            imw, imh = image.size

            if zfar-znear != 0:
                zl = 180 + 75*(img.data['zleft']-znear )/(zfar-znear)
                zr = 180 + 75*(img.data['zright']-znear)/(zfar-znear)
            else:
                zl=zr=255

            # apply gradient transparency based on the distance
            gradient = Image.new("L", (imw, imh), 0)
            draw = ImageDraw.Draw(gradient)
            for i in range(imh):
                alpha = int(zl + (zr - zl) * (i / imh))
                draw.rectangle((0, i, imw, i), fill=alpha)
            image.putalpha(gradient)

            # Perspective distortion
            points_top = [
                img.data['top']['p1'][0], img.data['top']['p1'][1],
                img.data['top']['p2'][0], img.data['top']['p2'][1],
                img.data['top']['p3'][0], img.data['top']['p3'][1],
                img.data['top']['p4'][0], img.data['top']['p4'][1]
            ]
            image = image.transform((w, h), Image.PERSPECTIVE, points_top, Image.BILINEAR)

            # Mask the image
            for maskImg in reversed(images):
                if img==maskImg:
                    break
                mask = Image.new("L", (imw, imh), 0)
                draw = ImageDraw.Draw(mask)
                points = [
                    maskImg.data['top']['p1'],
                    maskImg.data['top']['p2'],
                    maskImg.data['top']['p4'],
                    maskImg.data['top']['p3'],
                    maskImg.data['bottom']['p1'],
                    maskImg.data['bottom']['p2'],
                    maskImg.data['bottom']['p4'],
                    maskImg.data['bottom']['p3'],
                ]
                draw.polygon(points, fill=255)
                image.putalpha(mask)

            # Paste the processed image onto the output image
            outImage.paste(image, (0, 0), image)

        return outImage

    def paintEvent(self, canvas):
        w,h = self.size()
        canvas.drawTTkString(pos=(w//2,h-3),text=ttk.TTkString("😎"))
        # Draw Fov
        for y in range(h-3):
            canvas.drawChar(char='/', pos=(w//2+(h-3)-y,y))
            canvas.drawChar(char='\\',pos=(w//2-(h-3)+y,y))
        for image in self._images:
            ix,iy,iw,ih = image.getBox()
            canvas.drawText(pos=(ix,iy-1),text=f"{image.tilt:.2f}", color=ttk.TTkColor.YELLOW)
            canvas.drawText(pos=(ix+5,iy-1),text=f"{image.fileName}", color=ttk.TTkColor.BLUE)
            if image == self._highlightedImage:
                canvas.fill(pos=(ix,iy),size=(iw,ih),char='+',color=ttk.TTkColor.GREEN)
            elif image == self._currentImage:
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
        self._canvasImage = ttk.TTkCanvas()
        super().__init__(**kwargs)

    def updateCanvas(self, img:Image):
        w,h = img.width, img.height
        self._canvasImage.resize(w,h//2)
        self._canvasImage.updateSize()
        for x in range(img.width):
            for y in range(img.height//2):
                bg = 100 if (x//4+y//2)%2 else 150
                p1 = img[x,y*2]
                p2 = img[x,y*2+1]
                def _c2hex(p) -> str:
                    a = p.alpha
                    r = int(bg*(1-a)+255*a*p.red)
                    g = int(bg*(1-a)+255*a*p.green)
                    b = int(bg*(1-a)+255*a*p.blue)
                    return f"#{r<<16|g<<8|b:06x}"
                c = ttk.TTkColor.fgbg(_c2hex(p2),_c2hex(p1))
                self._canvasImage.drawChar(pos=(x,y), char='▄', color=c)
        self._canvasImage.drawText(pos=(0,1), text="Eugenio")

        self.update()

    def paintEvent(self, canvas):
        w,h = self.size()
        canvas.paintCanvas(self._canvasImage, (0,0,w,h), (0,0,w,h), (0,0,w,h))
        canvas.drawText(pos=(0,0), text="Eugenio")

class ControlPanel(ttk.TTkContainer):
    __slots__ = (
        'previewPressed','renderPressed','_toolbox', '_previewImage')
    def __init__(self, **kwargs):
        self.previewPressed = ttk.pyTTkSignal(RenderData)
        self.renderPressed = ttk.pyTTkSignal(RenderData)
        super().__init__(**kwargs|{'layout':ttk.TTkGridLayout()})
        self._previewImage = _Preview(minHeight=20,maxHeight=20)

        self._toolbox = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"toolbox.tui.json"))
        self._toolbox.getWidgetByName("Btn_Render").clicked.connect(self._renderClicked)
        self._toolbox.getWidgetByName("Btn_Preview").clicked.connect(self._previewClicked)
        # self._toolbox.getWidgetByName("SB_CamY")
        # self._toolbox.getWidgetByName("SB_CamA")
        # self._toolbox.getWidgetByName("CB_Bg")
        # self._toolbox.getWidgetByName("BG_Color")
        self.layout().addWidget(self._previewImage,0,0)
        self.layout().addWidget(self._toolbox,1,0)
        self.layout().addItem(ttk.TTkLayout(),2,0)

    def drawPreview(self, img:Image):
        self._previewImage.updateCanvas(img)

    @ttk.pyTTkSlot()
    def _renderClicked(self):
        if self._toolbox.getWidgetByName("CB_Bg").isChecked():
            btnColor = self._toolbox.getWidgetByName("BG_Color").color()
            color = (*btnColor.fgToRGB(),1)
        else:
            color = (0,0,0,0)
        data = RenderData(
            cameraAngle=self._toolbox.getWidgetByName("SB_CamA").value(),
            cameraY=self._toolbox.getWidgetByName("SB_CamY").value(),
            bgColor=color,
            resolution=(800,600)
        )
        self.renderPressed.emit(data)

    @ttk.pyTTkSlot()
    def _previewClicked(self):
        w,h = self.size()
        if self._toolbox.getWidgetByName("CB_Bg").isChecked():
            btnColor = self._toolbox.getWidgetByName("BG_Color").color()
            color = (*btnColor.fgToRGB(),1)
        else:
            color = (0,0,0,0)
        data = RenderData(
            cameraAngle=self._toolbox.getWidgetByName("SB_CamA").value(),
            cameraY=self._toolbox.getWidgetByName("SB_CamY").value(),
            bgColor=color,
            resolution=(w,40)
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
            title="TTkode")

    perspectivator = Perspectivator()
    controlPanel = ControlPanel()

    at = ttk.TTkAppTemplate()
    at.setWidget(widget=perspectivator,position=at.MAIN)
    at.setWidget(widget=controlPanel,position=at.RIGHT, size=30)

    for file in args.filename:
        perspectivator.addImage(file)

    root.layout().addWidget(at)

    def _preview(data):
        img = perspectivator.getImage(data)
        controlPanel.drawPreview(img)

    controlPanel.renderPressed.connect(perspectivator.render)
    controlPanel.previewPressed.connect(_preview)

    root.mainloop()

if __name__ == '__main__':
    main()