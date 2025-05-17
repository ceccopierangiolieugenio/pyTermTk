from PIL import Image

img = Image.open('img5.png')

w,h = img.size
out = img.transform((800,600), Image.Transform.QUAD, [100, 100, 500, 600, 400, 700, 50])

out.show()
