import glm
import moderngl as mgl
import numpy as np
import pygame

NEAR = 0.1
FAR = 1000
FOV = 90
SPEED = 0.1


class Camera:
    def __init__(self) -> None:
        self.position: glm.vec3 = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_view = self.get_projection_matrix()
        self.m_proj = self.get_view_matrix()

    def get_view_matrix(self) -> glm.mat4:
        return glm.lookAt(self.position, glm.vec3(0), self.up)

    def get_projection_matrix(self) -> glm.mat4:
        return glm.perspective(glm.radians(FOV), self._aspect_ratio, NEAR, FAR)

    @property
    def _aspect_ratio(self) -> float:
        window_size = pygame.display.get_window_size()
        aspect_ratio = window_size[0] / window_size[1]
        return aspect_ratio

    @property
    def _v_fov(self) -> float:
        v_fov = 2 * glm.atan(glm.tan(glm.radians(FOV) / 2) / self._aspect_ratio)
        return v_fov


pygame.init()
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)

ctx = mgl.create_context()
ctx.gc_mode = "auto"

program = ctx.program(
    vertex_shader="""
        #version 330

        in vec3 in_vert;
        in vec3 in_color;

        uniform mat4 projection;
        uniform mat4 view;
        uniform mat4 model;

        out vec3 v_color;

        void main() {
            // v_color = vec3(1.0, 1.0, 1.0);
            v_color = in_color;
            gl_Position = model * view * projection * vec4(in_vert, 1.0);
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

     6.5, 6.5, -100.0,
     6.5, -6.5, -100.0,
     -6.5, -6.5, -100.0,
     -6.5, 6.5, -100.0,

], dtype="f4")
indices = np.asarray([

    0, 1, 3,
    1, 2, 3,
        
], dtype="u4")
colors = np.asarray([

    255, 0, 0,
    0, 255, 0,
    0, 0, 255,
    0, 255, 0,
    
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

clock = pygame.Clock()

camera = Camera()
running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera.position.z += 0.03

    ctx.clear()

    program["model"].write(glm.mat4())  # type: ignore
    program["projection"].write(camera.m_proj)  # type: ignore
    program["view"].write(camera.m_view)  # type: ignore

    print(camera.position)

    ctx.enable(ctx.DEPTH_TEST)
    vertex_array_object.render()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
