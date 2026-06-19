import pygame
from NoIdeaGamePygame.module import SettingsWeapon


class Bullet:
    def __init__(self, x, y, color, width, height, vx, vy):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_off_screen(self, screen_width, screen_height):
        return (self.rect.right < 0 or self.rect.left > screen_width or
                self.rect.bottom < 0 or self.rect.top > screen_height)


def Weapon(start_x, start_y, dx, dy, bullets, bullet_width, bullet_height,
           shoot_sound, current_time):
    speed = SettingsWeapon.BulletSpeed
    color = SettingsWeapon.ColorBullet
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length != 0:
        vx = (dx / length) * speed
        vy = (dy / length) * speed
    else:
        vx, vy = 0, -speed
    bullet = Bullet(start_x, start_y, color, bullet_width, bullet_height, vx, vy)
    bullets.append(bullet)
    if shoot_sound:
        shoot_sound.play()


class TimeStopEffect:
    def __init__(self, sound, duration=2000, max_radius=300):
        self.sound = sound
        self.duration = duration
        self.max_radius = max_radius
        self.active = False
        self.start_time = 0
        self.radius = 0

    def activate(self):
        if not self.active:
            self.sound.play()
            self.active = True
            self.start_time = pygame.time.get_ticks()
            self.radius = 300

    def update(self, current_time):
        if self.active:
            elapsed = current_time - self.start_time
            if elapsed >= self.duration:
                self.active = False
            else:
                progress = elapsed / self.duration
                self.radius = 10 + (self.max_radius - 10) * progress

    def draw(self, screen, center):
        if self.active:
            elapsed = pygame.time.get_ticks() - self.start_time
            alpha = int(150 * (1 - elapsed / self.duration))

            surface = pygame.Surface((self.radius * 2, self.radius * 2))
            surface.set_colorkey((0, 0, 0))
            pygame.draw.circle(surface, (0, 150, 255),
                               (self.radius, self.radius), self.radius, width=3)
            surface.set_alpha(alpha)

            screen.blit(surface, (center[0] - self.radius, center[1] - self.radius))