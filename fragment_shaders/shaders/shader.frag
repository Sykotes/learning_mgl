# version 330 core

uniform float u_time;
uniform vec2 u_mouse;
uniform vec2 u_resolution;

float plotFunction(float x) {
    return pow(x * 2, 2.0) + (0.4 * x) - 0.5; // Example function
}

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution;
    uv = uv * 2.0 - 1.0; // Convert to range [-1,1]
    uv.x *= u_resolution.x / u_resolution.y; // Maintain aspect ratio

    float y = plotFunction(uv.x);
    float lineWidth = 0.01;

    // Draw the function curve
    float graph = smoothstep(lineWidth, 0.0, abs(uv.y - y));

    // Draw the x and y axes
    float axisWidth = 0.005;
    float xAxis = smoothstep(axisWidth, 0.0, abs(uv.y));
    float yAxis = smoothstep(axisWidth, 0.0, abs(uv.x));

    float smallAxisWidth = 0.002;
    float xSmallAxis = smoothstep(smallAxisWidth, 0.0, abs(uv.y + 0.5)) + smoothstep(smallAxisWidth, 0.0, abs(uv.y - 0.5));
    float ySmallAxis = smoothstep(smallAxisWidth, 0.0, abs(uv.x + 0.5)) + smoothstep(smallAxisWidth, 0.0, abs(uv.x - 0.5));
    // float xSmallAxis = smoothstep(smallAxisWidth, 0.0, abs(uv.y - 0.5));
    // float xSmallAxis = smoothstep(smallAxisWidth, 0.0, abs(uv.y - 0.5));
    
    vec3 color = vec3(1.0) - vec3(graph); // Graph in black
    color = mix(color, vec3(0.5), xAxis);
    color = mix(color, vec3(0.5), yAxis);
    color = mix(color, vec3(0.5), xSmallAxis);
    color = mix(color, vec3(0.5), ySmallAxis);
    
    gl_FragColor = vec4(color, 1.0);
}
