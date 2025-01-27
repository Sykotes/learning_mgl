import moderngl as mgl
import numpy as np
import pygame
from PIL import Image

_ = pygame.init()
_ = pygame.display.set_mode((600, 600), pygame.OPENGL | pygame.DOUBLEBUF)

ctx = mgl.create_context()
ctx.gc_mode = "auto"

program = ctx.program(
    vertex_shader="""
        #version 330

        in vec2 in_vert;

        out vec3 v_color;

        void main() {
            v_color = vec3(0.0, 0.0, 0.0);
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    """,
    fragment_shader="""
        #version 330

        in vec3 v_color;

        out vec3 f_color;

        void main() {
            f_color = v_color;
        }
    """,
)

r = 0.7
circle_segments = 100
circle_angles = np.linspace(0, 2 * np.pi, circle_segments, endpoint=False)
circle_vertices = np.column_stack(
    (np.cos(circle_angles) * r, np.sin(circle_angles) * r)
).astype("f4")

vbo = ctx.buffer(circle_vertices.tobytes())
vao = ctx.vertex_array(program, [(vbo, "2f", "in_vert")])

fbo = ctx.framebuffer(color_attachments=[ctx.texture((512, 512), 3)])
fbo.use()
fbo.clear(1.0, 1.0, 1.0)

vao.render(mgl.TRIANGLE_FAN)

image = Image.frombytes(
    "RGB",
    fbo.size,
    fbo.color_attachments[0].read(),  # type: ignore
    "raw",
    "RGB",
    0,
    -1,
)

image.save("! circle.png")

# ctx.screen.use()
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     ctx.clear(1.0, 1.0, 1.0)
#     vao.render(mgl.TRIANGLE_FAN)
#     pygame.display.flip()

pygame.quit()
