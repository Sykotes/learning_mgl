# version 330 core

uniform float u_time;
uniform vec2 u_mouse;
uniform vec2 u_resolution;

void main() {
	vec2 st = gl_FragCoord.xy/u_resolution;
  float mt = (u_mouse.x / u_resolution.x / 2.0) + (u_mouse.y / u_resolution.y / 2.0);

	gl_FragColor = vec4(mt, mt, mt, 1.0);
}
