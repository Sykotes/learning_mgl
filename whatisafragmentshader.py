# nothing perminant simply attemting to run examples from https://thebookofshaders.com

import time

import glm
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

        uniform vec2 u_resolution;
        uniform vec2 u_mouse;
        uniform float u_time;

        void main() {
            vec2 st = gl_FragCoord.xy / u_resolution;
            gl_FragColor = vec4(st.x,st.y,0.0,1.0);
        }
    """,
)

vao = ctx.vertex_array(program, [])

running = True
start_time = time.time()
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    width, height = pygame.display.get_window_size()
    program["u_resolution"] = glm.vec2(width, height)

    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # program["u_mouse"] = glm.vec2(mouse_x, mouse_y)

    # program["u_time"] = time.time() - start_time

    ctx.clear(0.0, 0.0, 0.0, 1.0)
    vao.render(mgl.TRIANGLES, vertices=3)

    pygame.display.flip()
    _ = clock.tick(60)

pygame.quit()
