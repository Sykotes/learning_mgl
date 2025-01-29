import time

import moderngl as mgl
import pygame

WIDTH, HEIGHT = 512, 512

_ = pygame.init()
_ = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

ctx = mgl.create_context()
ctx.gc_mode = "auto"

program = ctx.program(
    vertex_shader="""
        # version 330 core
        vec2 positions[3] = vec2[](
            vec2(-1.0, -1.0),
            vec2( 3.0, -1.0),
            vec2(-1.0,  3.0)
        );

        void main() {
            gl_Position = vec4(positions[gl_VertexID], 0.0, 1.0);
        }
    """,
    fragment_shader="""
        # version 330 core
        uniform float u_time;
        out vec4 fragColor;

        void main() {
            float mod = abs(sin(u_time));
            fragColor = vec4(mod, 0.0, 0.0, 1.0);
        }
    """,
)

vao = ctx.vertex_array(program, [])

running = True
start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    program["u_time"] = time.time() - start_time

    ctx.clear(0.0, 0.0, 0.0, 1.0)
    vao.render(mgl.TRIANGLES, vertices=3)

    pygame.display.flip()

pygame.quit()
