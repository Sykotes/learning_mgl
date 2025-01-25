import glm
import moderngl as mgl
import numpy as np
import pygame


class Camera:
    def __init__(self) -> None:
        self.position = glm.vec3(2, 0, 2)  # Initial position of the camera
        direction = glm.vec3(0, 0, 0) - self.position  # Vector to the origin

        # Calculate pitch and yaw to look at the origin
        self.pitch = glm.asin(direction.y / glm.length(direction))  # Pitch angle
        self.yaw = glm.atan(direction.z, direction.x)  # Yaw angle

        print(glm.degrees(self.pitch), glm.degrees(self.yaw))

        self.up = glm.vec3(0, 1, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.update_forward()
        self.view = glm.lookAt(self.position, self.position + self.forward, self.up)
        self.proj = glm.perspective(glm.radians(60), 4 / 3, 0.1, 100)
        self.model = glm.mat4()

    def update_forward(self) -> None:
        self.forward.x = glm.cos(self.pitch) * glm.cos(self.yaw)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.cos(self.pitch) * glm.sin(self.yaw)
        self.forward = glm.normalize(self.forward)

    def update(self) -> None:
        self.move()
        self.update_forward()
        self.view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def move(self) -> None:
        self.position += self.forward * 0.01


# class Camera:
#     def __init__(self) -> None:
#         self.position = glm.vec3(2, 0, 2)
#         self.pitch = glm.radians(-90)
#         self.yaw = 0
#         self.up = glm.vec3(0, 1, 0)
#         self.forward = glm.vec3(0, 0, -1)
#
#         self.view = glm.lookAt(self.position, glm.vec3(0), self.up)
#         self.proj = glm.perspective(glm.radians(60), 4 / 3, 0.1, 100)
#         self.model = glm.mat4()
#
#     def update(self) -> None:
#         self.move()
#         self.view = glm.lookAt(self.position, glm.vec3(0), self.up)
#
#     def move(self) -> None:
#         self.position.xz += 0.001


class Game:
    def __init__(self) -> None:
        _ = pygame.init()
        _ = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.ctx = mgl.create_context()

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

        self.program["model"].write(self.camera.model)  # type: ignore
        self.program["proj"].write(self.camera.proj)  # type: ignore
        self.program["view"].write(self.camera.view)  # type: ignore

        self.vao.render()
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.camera.update()
            self.render()

            _ = self.clock.tick(144)

        pygame.quit()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
