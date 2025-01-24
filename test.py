import moderngl
import numpy as np
from PIL import Image

ctx = moderngl.create_context(standalone=True)

program = ctx.program(
    vertex_shader="""
        #version 330

        in vec2 in_vert;
        in vec3 in_color;

        uniform float scale;

        out vec3 v_color;

        void main() {
            v_color = in_color;
            gl_Position = vec4(in_vert * scale, 0.0, 1.0);
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

# fmt: off
vertices = np.asarray([

     -0.75, -0.75,  1, 0, 0, 
     0.75, -0.75,  0, 1, 0, 
     0.0, 0.649,  0, 0, 1
     
], dtype="f4")
# fmt: on

vertex_buffer_object = ctx.buffer(vertices.tobytes())
vertex_array_object = ctx.vertex_array(
    program, vertex_buffer_object, "in_vert", "in_color"
)

framebuffer_object = ctx.framebuffer(color_attachments=[ctx.texture((1920, 1080), 3)])
framebuffer_object.use()
framebuffer_object.clear(0.0, 0.0, 0.0, 1.0)

vertex_array_object.program["scale"] = 2

vertex_array_object.render()  # "mode" is moderngl.TRIANGLES by default

image = Image.frombytes(
    "RGB",
    framebuffer_object.size,
    framebuffer_object.color_attachments[0].read(),  # type: ignore
    "raw",
    "RGB",
    0,
    -1,
)

image.show()
