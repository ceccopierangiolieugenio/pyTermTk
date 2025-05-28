import moderngl
import numpy as np
from PIL import Image

# Create a standalone OpenGL context
ctx = moderngl.create_standalone_context()

# Framebuffer size
width, height = 100, 100

# Create an offscreen framebuffer
fbo = ctx.framebuffer(color_attachments=[ctx.texture((width, height), 4)])

# Triangle vertices (x, y)
vertices = np.array([
    -0.5, -0.5,
     0.5, -0.5,
     0.0,  0.5,
], dtype='f4')

# Create buffer and shaders
vbo = ctx.buffer(vertices.tobytes())
prog = ctx.program(
    vertex_shader='''
        #version 330
        in vec2 in_vert;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    ''',
    fragment_shader='''
        #version 330
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red
        }
    '''
)
vao = ctx.vertex_array(prog, [(vbo, '2f', 'in_vert')])

# Render
fbo.use()
ctx.clear(0.0, 0.0, 0.0, 1.0)
vao.render(moderngl.TRIANGLES)

# Read pixels
data = fbo.read(components=3)
image = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))

# Save or inspect
img = Image.fromarray(image, 'RGB')
img.show()
print("Triangle rendered and saved to triangle.png")
print("Sample RGB at center:", image[height // 2, width // 2])
