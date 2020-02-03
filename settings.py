import configparser
import pygame

pygame.init()


def parse_config(file):
    config_parser = configparser.RawConfigParser()
    config_parser.read(file)
    width = config_parser.get('info', 'Width')
    height = config_parser.get('info', 'Height')
    name = config_parser.get('info', 'Name')
    fps = config_parser.get('info', 'FPS')
    return (width, height, name, fps)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (122, 0, 0)
RED_DARK = (255, 0, 0)
GREEN = (0, 135, 0)
LIGHT_GREEN = (0, 255, 0)
YELLOW = (200, 200, 0)
LIGHT_YELLOW = (100, 100, 0)
GREY = (220, 220, 220)

OBJ_SIZE = 16
CONST_SPEED = 1
MAP_WIDTH = 27
MAP_HEIGHT = 27
TURN_RATIO = 15

ENEMY_TYPES = ['regular', 'heavy', 'fast']

MUSIC = dict(daisuke='sounds/background.ogg',
             start='sounds/gamestart.ogg',
             ooof='sounds/mine.ogg')

GAME_SETTINGS = parse_config('text/config.cfg')
DISPLAY_WIDTH = int(GAME_SETTINGS[0])
DISPLAY_HEIGHT = int(GAME_SETTINGS[1])
FPS = int(GAME_SETTINGS[3])

PLAYER_SPRITE = pygame.image.load('images/player/player_up.png')
ENEMY_HEAVY_SPRITE = pygame.image.load('images/enemy_heavy.png')

HUD = pygame.image.load('images/hud.png')
TOP_HUD = pygame.image.load('images/top_hud.png')
BRICK = pygame.image.load('images/brick.png')
BUSH = pygame.image.load('images/bush.png')
IRON_BRICK = pygame.image.load('images/iron.png')
IRON_FLOOR = pygame.image.load('images/iron_floor.png')
WATER = pygame.image.load('images/water.png')
TOWER_IMG = pygame.image.load('images/tower.png')
SHOP_BUTTON = pygame.image.load('images/StartButton1.png')

SMALL_FONT = pygame.font.Font("fonts/prstart.ttf", 10)
FONT = pygame.font.Font("fonts/prstart.ttf", 14)
BIG_FONT = pygame.font.Font("fonts/prstart.ttf", 17)

GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                       pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption('Tanks client')
pygame.display.set_icon(PLAYER_SPRITE)
