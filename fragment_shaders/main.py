import os
import threading
import time

import glm
import moderngl as mgl
import pygame

WIDTH: int = 800
HEIGHT: int = 800

frag_path = "./shaders/shader.frag"
should_reload = threading.Event()


def detect_file_change_thread() -> None:
    last_modified_time = os.path.getmtime(frag_path)

    while True:
        time.sleep(0.2)
        current_modified_time = os.path.getmtime(frag_path)
        if current_modified_time != last_modified_time and not should_reload.is_set():
            should_reload.set()
            last_modified_time = current_modified_time


def get_new_shader() -> str:
    with open(frag_path) as file:
        fragment_shader = file.read()

    return fragment_shader


def main() -> None:
    _ = pygame.init()
    _ = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

    ctx = mgl.create_context()
    ctx.gc_mode = "auto"

    with open("./shaders/shader.vert") as file:
        vertex_shader = file.read()

    with open(frag_path) as file:
        fragment_shader = file.read()

    program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    thread = threading.Thread(target=detect_file_change_thread, daemon=True)
    thread.start()

    vao = ctx.vertex_array(program, [])

    running = True
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if should_reload.is_set():
            print("reload")
            reloaded = False
            while not reloaded:
                try:
                    program = ctx.program(
                        vertex_shader=vertex_shader, fragment_shader=get_new_shader()
                    )
                    reloaded = True
                except Exception as e:
                    print(f"Shader Error: {e}")
                    time.sleep(1.0)

            vao = ctx.vertex_array(program, [])
            should_reload.clear()

        t = time.time() - start_time

        mouse_pos = pygame.mouse.get_pos()
        mouse: glm.vec2 = glm.vec2(mouse_pos[0], HEIGHT - mouse_pos[1])

        ctx.clear(0.39, 0.67, 0.96)
        vao.render(mgl.TRIANGLES, vertices=3)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
