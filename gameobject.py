import pygame
from settings import *


def has_crossing(obj_1, obj_2, block_size):
    if obj_1.x >= obj_2.x \
            and obj_1.x <= obj_2.x + block_size \
            or obj_1.x + block_size > obj_2.x \
            and obj_1.x + block_size < obj_2.x + block_size:
        if obj_1.y >= obj_2.y \
                and obj_1.y <= obj_2.y + block_size:
            return True
    return False


class GameObject():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, game_display, color):
        """Draws the game_object to your screen"""
        pygame.draw.rect(game_display, color,
                         [self.x, self.y, self.size, self.size])

    def draw_explosion(self, game_display, camera):
        """Draws the game_object explosion to your screen"""
        img = pygame.image.load('images/Explosion.png')
        second = pygame.image.load('images/exp_1.png')
        third = pygame.image.load('images/exp_2.png')
        images = []
        images.append(img)
        images.append(second)
        images.append(third)
        for image in images:
            game_display.blit(image, camera.follow(self))


class Camera():
    def __init__(self, width, height):
        self.camera = pygame.Rect(DISPLAY_WIDTH/4,
                                  DISPLAY_HEIGHT - 2*OBJ_SIZE,
                                  width,
                                  height)
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def follow(self, game_object):

        rect = pygame.Rect(game_object.x,
                           game_object.y,
                           game_object.size,
                           game_object.size)
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.x + int(DISPLAY_WIDTH/2)
        y = -target.y + int(DISPLAY_HEIGHT/2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(DISPLAY_WIDTH-self.width+64), x)  # right
        y = max(-(DISPLAY_HEIGHT - self.height)+320, y)  # bottom 375
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Terrain(GameObject):
    def __init__(self, x, y, size, kind):
        GameObject.__init__(self, x, y, size)
        self.kind = kind

    def __eq__(self, other):
        return self.x == other.y \
            and self.y == other.y \
            and self.kind == other.kind

    def draw(self, game_display, camera):
        if self.kind == 'iron':
            game_display.blit(IRON_BRICK, camera.follow(self))
        elif self.kind == 'BUSH':
            game_display.blit(BUSH, camera.follow(self))
        elif self.kind == 'BRICK':
            game_display.blit(BRICK, camera.follow(self))
        elif self.kind == 'IRON_FLOOR':
            game_display.blit(IRON_FLOOR, camera.follow(self))
        elif self.kind == 'WATER':
            game_display.blit(WATER, camera.follow(self))


class Missile(GameObject):
    def __init__(self, x, y, size, direction_x, direction_y):
        GameObject.__init__(self, x, y, size)
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.velocity_x = 3 * (direction_x + 0.1)
        self.velocity_y = 3 * (direction_y + 0.1)
        self.angle = 0

    @classmethod
    def from_dict(cls, dict):
        return cls(dict['x'],
                   dict['y'],
                   dict['size'],
                   dict['direction_x'],
                   dict['direction_y'])

    def draw_missile(self, game_display, angle, camera):
        img = pygame.image.load('images/missile.png')
        t = pygame.transform.rotate(img, angle)
        game_display.blit(t, camera.follow(self))

    def __str__(self):
        return str(self.direction_x) + '|' + str(self.direction_y)


class Tower(GameObject):
    def __init__(self, x, y, size, side, hp=300):
        GameObject.__init__(self, x, y, size)
        self.side = side
        self.hp = hp

    def draw(self, game_display, camera):
        game_display.blit(TOWER_IMG, camera.follow(self))


class Castle(GameObject):
    def __init__(self, x, y, size, state, side, hp=500):
        GameObject.__init__(self, x, y, size)
        self.state = state
        self.kind = 'castle'
        self.side = side
        self.hp = hp

    def draw(self, game_display, camera):
        b_up_t = pygame.image.load('images/5.png')
        b_down = pygame.image.load('images/8.png')
        b_up = pygame.transform.scale2x(b_up_t)
        if self.state == 'alive':
            game_display.blit(b_up, camera.follow(self))
        if self.state == 'destroyed':
            game_display.blit(b_down, camera.follow(self))
