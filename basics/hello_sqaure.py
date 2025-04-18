import moderngl as mgl
import numpy as np
from PIL import Image

ctx = mgl.create_context(standalone=True)

program = ctx.program(
    vertex_shader="""
        #version 330

        in vec3 in_vert;
        in vec3 in_color;

        out vec3 v_color;

        void main() {
            // v_color = vec3(1.0, 1.0, 1.0);
            v_color = in_color;
            gl_Position = vec4(in_vert, 1.0);
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

     0.5, 0.5, 0.0,
     0.5, -0.5, 0.0,
     -0.5, -0.5, 0.0,
     -0.5, 0.5, 0.0,

], dtype="f4")
indices = np.asarray([

    0, 1, 3,
    1, 2, 3,
        
], dtype="u4")
colors = np.asarray([

    255, 0, 0,
    0, 255, 0,
    0, 0, 255,
    0, 0, 0,
    
], dtype="u1")
# fmt: on

vertex_buffer_object = ctx.buffer(vertices.tobytes())
index_buffer_object = ctx.buffer(indices.tobytes())
color_buffer_object = ctx.buffer(colors.tobytes())

vertex_array_object = ctx.vertex_array(
    program,
    [
        (vertex_buffer_object, "3f", "in_vert"),
        (color_buffer_object, "3f1", "in_color"),
    ],
    index_buffer_object,
)

framebuffer_object = ctx.framebuffer(color_attachments=[ctx.texture((512, 512), 3)])
framebuffer_object.use()
framebuffer_object.clear(0.0, 0.0, 0.0, 1.0)

vertex_array_object.render()

texture = framebuffer_object.color_attachments[0]
data = texture.read()  # type: ignore

image = Image.frombytes(
    "RGB",
    framebuffer_object.size,
    data,
    "raw",
    "RGB",
    0,
    -1,
)

image.show()
