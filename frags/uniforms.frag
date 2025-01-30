# version 330 core

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;


void main() {
    vec2 st = gl_FragCoord.xy / u_resolution;
    float norm = 0.5 * ((u_mouse.x / u_resolution.x) + (u_mouse.y / u_resolution.y));
    float blue = abs(sin(u_time)) * norm;
    gl_FragColor = vec4(st.x, st.y, blue, 1.0);
}
