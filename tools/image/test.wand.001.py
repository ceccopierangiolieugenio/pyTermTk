import sys,os
import math
import argparse
from typing import Optional,Tuple,List,Dict

import numpy as np

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

sys.path.append(os.path.join(sys.path[0],'../..'))

import TermTk as ttk


screen_width = 800  # Screen width
screen_height = 600  # Screen height
w,h = screen_width,screen_height

with Image(width=w, height=h, background=Color('yellow'), pseudo='pattern:crosshatch') as outImage:
    with Image(filename="img2.png") as image:
        image.resize(150,100)
        outImage.composite(image,150,10)

    with Image(width=100, height=100, pseudo='gradient:red-transparent') as gradient:
        outImage.composite(gradient,320,10)

    with Image(width=100, height=100, pseudo='gradient:rgba(0,0,0,0.5)-rgba(1,1,1,1)') as gradient:
        outImage.composite(gradient,430,10)

    with Image(width=100, height=100, pseudo='gradient:rgba(0,255,0,0)-rgba(1,1,1,0.5)') as gradient:
        outImage.composite(gradient,540,10)

    with Image(width=100, height=100, pseudo='gradient:rgba(0,255,0,1)-rgba(255,0,0,1)') as gradient:
        outImage.composite(gradient,650,10)

    with Image(width=100, height=100, pseudo='gradient:transparent-black') as gradient:
        outImage.composite(gradient,10,10)
        g2 = gradient.clone()
        g2.alpha_channel = "extract"
        outImage.composite(g2,10,140)
        with Drawing() as draw:
            draw.fill_color = Color('black')  # Opaque
            draw.fill_opacity = 1.0  # Fully opaque
            points = [(30,50),(50,80),(30,80)]
            draw.polygon(points)
            draw(g2)
        outImage.composite(g2,120,140)
        with Image(width=100, height=100, pseudo='gradient:#FFFFFF-#777777') as newGradient:
            newGradient.rotate(90)
            outImage.composite(newGradient,120,250)
            g2.composite(newGradient,left=0,top=0,operator='multiply')
        outImage.composite(g2,230,140)
        g2.alpha_channel = "copy"
        outImage.composite(g2,340,140)
        with Image(width=100, height=100, background=Color('blue')) as g3:
            g3.composite_channel(channel='alpha', image=g2, operator='copy_alpha')
            outImage.composite(g3,340,250)


    outImage.save(filename='outImage.png')
