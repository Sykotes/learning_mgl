import glm
import moderngl as mgl
import numpy as np
import pygame

NEAR = 0.1
FAR = 1000
FOV = 90


class Camera:
    def __init__(
        self,
        position: tuple[float, float, float] = (0, 0, 0),
        yaw: float = 90,
        pitch: float = 0,
    ) -> None:
        # Position X, Y, Z
        self.position: tuple[float, float, float] = position

        # Camera/ Head angle in radians
        self.yaw: float = yaw
        self.pitch: float = pitch

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.projection: glm.mat4x4 = glm.perspective(
            self._v_fov, self._aspect_ratio, NEAR, FAR
        )
        self.view: glm.mat4x4 = glm.mat4()

    def update(self) -> None:
        self.view = glm.lookAt(self.position, self.position + self.forward, self.up)

        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(self.right)
        self.up = glm.normalize(glm.cross(self.forward, self.right))

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

     0.5, 0.5, -10.0,
     0.5, -0.5, -10.0,
     -0.5, -0.5, -10.0,
     -0.5, 0.5, -10.0,

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

camera = Camera((0, 0, 0))
running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera.update()
    ctx.clear()

    program["model"].write(glm.mat4())  # type: ignore
    program["projection"].write(camera.projection)  # type: ignore
    program["view"].write(camera.view)  # type: ignore

    ctx.enable(ctx.DEPTH_TEST)
    vertex_array_object.render()
    pygame.display.flip()

pygame.quit()
