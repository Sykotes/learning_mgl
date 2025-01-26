import glm
import pygame


class Camera:
    def __init__(self, position: glm.vec3 = glm.vec3(0, 0, 0)) -> None:
        self.position: glm.vec3 = position

        self.yaw: float = -0.75 * glm.pi()
        self.pitch: float = 0.0

        self.forward: glm.vec3 = glm.vec3(0, 0, 1)
        self.right: glm.vec3 = glm.vec3(1, 0, 0)
        self.up: glm.vec3 = glm.vec3(0, 1, 0)

        self.v_fov: float = glm.radians(60.0)
        self.near: float = 0.1
        self.far: float = 100.0

        self.sensitivity = 0.002
        self.speed = 1

        self.m_view: glm.mat4 = glm.lookAt(
            self.position, self.position + self.forward, self.up
        )
        self.m_proj: glm.mat4 = glm.perspective(
            self.v_fov, self._aspect, self.near, self.far
        )
        self.m_model: glm.mat4 = glm.mat4()

    def update(self, dt: float) -> None:
        self._rotate()

        self.forward.x = glm.cos(self.pitch) * glm.cos(self.yaw)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.cos(self.pitch) * glm.sin(self.yaw)
        self.forward = glm.normalize(self.forward)

        self.right = glm.normalize(glm.cross(self.up, self.forward))

        self.m_view: glm.mat4 = glm.lookAt(
            self.position, self.position + self.forward, self.up
        )
        self.m_proj: glm.mat4 = glm.perspective(
            self.v_fov, self._aspect, self.near, self.far
        )

        self._move(dt)

    def _rotate(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_rel()

        self.yaw += mouse_x * self.sensitivity
        self.pitch -= mouse_y * self.sensitivity
        self.pitch = max(min(self.pitch, glm.pi() / 2), -glm.pi() / 2)

    def _move(self, dt: float) -> None:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w]:
            self.position += self.forward * self.speed * dt
        if keys_pressed[pygame.K_s]:
            self.position -= self.forward * self.speed * dt
        if keys_pressed[pygame.K_a]:
            self.position += self.right * self.speed * dt
        if keys_pressed[pygame.K_d]:
            self.position -= self.right * self.speed * dt
        if keys_pressed[pygame.K_SPACE]:
            self.position += self.up * self.speed * dt
        if keys_pressed[pygame.K_LSHIFT]:
            self.position -= self.up * self.speed * dt

    @property
    def _aspect(self) -> float:
        width, height = pygame.display.get_window_size()
        ratio = width / height

        return ratio
