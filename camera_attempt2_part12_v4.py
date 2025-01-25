import glm
import moderngl as mgl
import numpy as np
import pygame


class Camera:
    def __init__(self) -> None:
        self.position = glm.vec3(2, 0, 2)
        self.pitch = glm.radians(-90)
        self.yaw = 0
        self.up = glm.vec3(0, 1, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.right = glm.vec3(1, 0, 0)

        self.view = glm.lookAt(self.position, glm.vec3(0), self.up)
        self.proj = glm.perspective(glm.radians(60), 4 / 3, 0.1, 100)
        self.model = glm.mat4()


class Game:
    def __init__(self) -> None:
        pygame.init()
        _ = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.ctx = mgl.create_context()

        self.camera = Camera()

        self.setup_render()

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

        self.program["model"].write(self.camera.model)
        self.program["proj"].write(self.camera.proj)
        self.program["view"].write(self.camera.view)

        self.vao.render()
        pygame.display.flip()

    def run(self) -> None:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.render()

        pygame.quit()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
