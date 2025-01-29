import glm
import moderngl as mgl
import numpy as np
import pygame

FOV = 60


class Camera:
    def __init__(self) -> None:
        self.position = glm.vec3(2, 0, 2)

        self.pitch: float = 0
        self.yaw = -0.75 * glm.pi()

        self.up = glm.vec3(0, 1, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.right = glm.vec3(0, 0, 0)
        self.update_forward()

        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)
        self.m_proj = glm.perspective(glm.radians(FOV), self.aspect_ratio, 0.1, 100)
        self.m_model = glm.mat4()

    def update_forward(self) -> None:
        self.forward.x = glm.cos(self.pitch) * glm.cos(self.yaw)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.cos(self.pitch) * glm.sin(self.yaw)
        self.forward = glm.normalize(self.forward)

        self.right = glm.normalize(glm.cross(self.up, self.forward))

    def update(self) -> None:
        self.move()
        self.rotate()
        self.update_forward()
        self.m_proj = glm.perspective(glm.radians(FOV), self.aspect_ratio, 0.1, 100)
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def rotate(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_rel()

        sensitivity = 0.002

        self.yaw += mouse_x * sensitivity
        self.pitch -= mouse_y * sensitivity
        self.pitch = max(min(self.pitch, glm.pi() / 2), -glm.pi() / 2)

        self.update_forward()

    def move(self) -> None:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w]:
            self.position += self.forward * 0.01
        if keys_pressed[pygame.K_s]:
            self.position -= self.forward * 0.01
        if keys_pressed[pygame.K_a]:
            self.position += self.right * 0.01
        if keys_pressed[pygame.K_d]:
            self.position -= self.right * 0.01
        if keys_pressed[pygame.K_SPACE]:
            self.position += self.up * 0.01
        if keys_pressed[pygame.K_LSHIFT]:
            self.position -= self.up * 0.01

    @property
    def aspect_ratio(self) -> float:
        width, height = pygame.display.get_window_size()
        return width / height


class Game:
    def __init__(self) -> None:
        _ = pygame.init()
        _ = pygame.display.set_mode(
            (800, 600), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
        )

        self.ctx = mgl.create_context()
        self.ctx.gc_mode = "auto"

        self.camera = Camera()
        self.setup_render()

        self.clock = pygame.Clock()
        self.running = True

    def setup_render(self) -> None:
        self.program = self.ctx.program(
            vertex_shader="""
                #version 330

                in vec3 in_vert;

                uniform mat4 view;
                uniform mat4 model;
                uniform mat4 proj;

                out vec3 v_color;

                void main() {
                    v_color = vec3(1.0, 1.0, 1.0);
                    gl_Position = proj * view * model * vec4(in_vert, 1.0);
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

        vertices = [
            (0.0, 0.5, 0.0),  # Top vertex
            (-0.5, -0.5, 0.0),  # Bottom-left vertex
            (0.5, -0.5, 0.0),  # Bottom-right vertex
        ]

        vertices_array = np.array(vertices, dtype="f4")

        vbo = self.ctx.buffer(vertices_array.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program,
            [(vbo, "3f", "in_vert")],
        )

    def render(self) -> None:
        self.ctx.clear(0.17, 0.2, 0.3)

        self.program["model"].write(self.camera.m_model)  # type: ignore
        self.program["proj"].write(self.camera.m_proj)  # type: ignore
        self.program["view"].write(self.camera.m_view)  # type: ignore

        self.vao.render()
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if pygame.mouse.get_focused():
                _ = pygame.mouse.set_visible(False)
                pygame.mouse.set_pos(400, 300)
            else:
                _ = pygame.mouse.set_visible(True)

            self.camera.update()
            self.render()

            _ = self.clock.tick(144)

        pygame.quit()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
