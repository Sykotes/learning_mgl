import time

import glm
import moderngl as mgl
import pygame

WIDTH: int = 800
HEIGHT: int = 600


def auto_reload_program() -> mgl.Program: ...


def main() -> None:
    _ = pygame.init()
    _ = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

    ctx = mgl.create_context()
    ctx.gc_mode = "auto"

    with open("./shaders/shader.vert") as file:
        vertex_shader = file.read()

    with open("./shaders/shader.frag") as file:
        fragment_shader = file.read()

    program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    vao = ctx.vertex_array(program, [])

    running = True
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t = time.time() - start_time

        mouse_pos = pygame.mouse.get_pos()
        mouse: glm.vec2 = glm.vec2(mouse_pos[0], HEIGHT - mouse_pos[1])

        ctx.clear(0.39, 0.67, 0.96)
        vao.render(mgl.TRIANGLES, vertices=3)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
