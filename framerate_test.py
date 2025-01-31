import time

import moderngl as mgl
import pygame

_ = pygame.init()
_ = pygame.display.set_mode((600, 600))

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

        void main() {
          gl_FragColor = vec4(1.0);
        }
    """,
)

running = True

start_time = time.time()
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear()
    pygame.display.flip()

    fps = clock.get_fps()
    # pygame.display.set_caption(str(fps))
    clock.tick(0.0)

pygame.quit()
