import random
import os
import math
import datetime
import pygame
import pygame.locals
from settings import *
from tank import *
from gameobject import *
from server_tcp.network import Network
from main_server import *
import pickle

pygame.init()

clientNumber = 0
CLOCK = pygame.time.Clock()


def save_replay(actions, filename='replay.txt'):
    with open(filename, 'w') as file:
        for action in actions:
            file.write(action + '\n')
    print('Replay saved')


def load_replay(filename='replay.txt'):
    data = []
    with open(filename, 'r') as file:
        data = file.read().split('\n')
    return data


def load_level():
    filename = 'levels/' + '1'
    if not os.path.isfile(filename):
        raise AssertionError()
    level = []
    game_map = []
    file = open(filename, 'r')
    data = file.read().split('\n')
    file.close()
    x, y = 0, 0
    for row in data:
        for char in row:
            if char == '#':
                game_map.append(Terrain(x, y, OBJ_SIZE, 'BRICK'))
            elif char == '@':
                game_map.append(Terrain(x, y, OBJ_SIZE, 'iron'))
            elif char == '%':
                game_map.append(Terrain(x, y, OBJ_SIZE, 'WATER'))
            elif char == '~':
                game_map.append(Terrain(x, y, OBJ_SIZE, 'BUSH'))
            elif char == '-':
                game_map.append(Terrain(x, y, OBJ_SIZE, 'IRON_FLOOR'))
            elif char == 'C':
                game_map.append(Castle(x, y, OBJ_SIZE*2, 'alive', 'friendly'))
            elif char == 'E':
                game_map.append(Castle(x, y, OBJ_SIZE*2, 'alive', 'enemy'))
            x += OBJ_SIZE
        x = 0
        y += OBJ_SIZE
    return game_map


class Client():
    def __init__(self, id):
        self.game_id = id
        self.game_over = False
        self.ready = False
        self.game_map = load_level()
        self.player = Player(50, 50, 3, 16, 100, 'radiant')
        self.player_2 = Player(600, 600, 3, 16, 100, 'dire')
        self.kill_score = {'dire': 0, 'radiant': 0}

    def text_objects(self, text, color):
        text_surface = FONT.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def update_net_key(self, start_key, net):
        self.player.data = start_key
        self.player.value = start_key['player']
        self.player.side = start_key['side']
        self.player.x = start_key['x']
        self.player.y = start_key['y']
        player_2_key = net.send(self.player.data)
        self.player_2.value = player_2_key['player']
        self.player_2.side = player_2_key['side']
        self.player_2.x = player_2_key['x']
        self.player_2.y = player_2_key['y']
        return True

    def update_enemy_info(self, player_2_key):
        self.player_2.x = player_2_key['x']
        self.player_2.y = player_2_key['y']
        self.player_2.angle = player_2_key['angle']
        self.player_2.hp = player_2_key['hp']
        self.player_2.enemies_killed = player_2_key['enemies_killed']
        self.player_2.items = player_2_key['items']
        return True

    def enemy_bull_check(self, player_2_key):
        for mis in player_2_key['missiles']:
            if not client.player_2.missiles \
                    and len(client.player_2.missiles) < 1:
                temp_missile = Missile.from_dict(mis)
                client.player_2.missiles.append(temp_missile)
        return True

    def draw_itembar(self, game_display):
        game_display.blit(HUD, [0, 18*OBJ_SIZE])
        game_display.blit(TOP_HUD, [0, 0])
        if self.player.gold > 700:
            if len(self.player.items) < 6:
                self.player.items.append('dick')
                self.player.gold -= 700

    def draw_items(self, game_display):
        counter = 5
        for item in self.player.items:
            path = f'images/{item}.png'
            t = pygame.image.load(path)
            x = DISPLAY_WIDTH - 105 - int(counter % 3)*23
            y = DISPLAY_HEIGHT - 40 + int(counter / 3)*18
            game_display.blit(t, [x, y])
            counter -= 1

    def draw_mini_map(self):
        player_x = self.player.x
        player_y = self.player.y
        mini_x = 10 + player_x / 97 * 7
        mini_y = DISPLAY_HEIGHT - 90 + player_y / 97 * 7
        player2_x = self.player_2.x
        player2_y = self.player_2.y
        mini2_x = 10 + player2_x / 97 * 7
        mini2_y = DISPLAY_HEIGHT - 90 + player2_y / 97 * 7
        player1_sprite = pygame.transform.scale(
            pygame.transform.rotate(PLAYER_SPRITE, self.player.angle + 270),
            (8, 8))
        player2_sprite = pygame.transform.scale(
            pygame.transform.rotate(PLAYER_SPRITE, self.player_2.angle + 270),
            (8, 8))
        GAME_DISPLAY.blit(player1_sprite, [mini_x, mini_y])
        GAME_DISPLAY.blit(player2_sprite, [mini2_x, mini2_y])

    def show_description(self, number, cur, filename='images/no_item.png'):
        try:
            curr_item = self.player.items[number]
        except:
            curr_item = ''
        finally:
            check = isinstance(curr_item, str)
        if curr_item != '':
            filename = f'images/{curr_item}_description.png'
        desc = pygame.image.load(filename)
        GAME_DISPLAY.blit(desc, [cur[0], cur[1] - OBJ_SIZE * 4])

    def draw_item_description(self):
        cur = pygame.mouse.get_pos()
        number = 0
        if cur[1] >= 380 and cur[1] <= 398:
            if cur[0] >= 489 and cur[0] <= 511:
                number = 3
                self.show_description(number, cur)
            elif cur[0] >= 512 and cur[0] <= 534:
                number = 4
                self.show_description(number, cur)
            elif cur[0] >= 535 and cur[0] <= 558:
                number = 5
                self.show_description(number, cur)
        if cur[1] >= 399 and cur[1] <= 417:
            if cur[0] >= 489 and cur[0] <= 511:
                number = 0
                self.show_description(number, cur)
            elif cur[0] >= 512 and cur[0] <= 534:
                number = 1
                self.show_description(number, cur)
            elif cur[0] >= 535 and cur[0] <= 558:
                number = 2
                self.show_description(number, cur)

    def draw_explosion(self, game_display, x, y, camera):
        img = pygame.image.load('images/Explosion.png')
        second = pygame.image.load('images/exp_1.png')
        third = pygame.image.load('images/exp_2.png')
        images = []
        images.append(img)
        images.append(second)
        images.append(third)
        for image in images:
            game_display.blit(image, [x, y])

    def draw_button(self, cur=None):
        if cur is None:
            cur = pygame.mouse.get_pos()
        if cur[1] >= 300 and cur[1] <= 350:
            if cur[0] >= 20 and cur[0] <= 140:
                pygame.draw.rect(GAME_DISPLAY, LIGHT_GREEN, (20, 300, 120, 50))
            elif cur[0] >= 180 and cur[0] <= 320:
                pygame.draw.rect(GAME_DISPLAY, YELLOW, (180, 300, 120, 50))
            elif cur[0] >= 340 and cur[0] <= 480:
                pygame.draw.rect(GAME_DISPLAY, RED_DARK, (340, 300, 120, 50))

    def score(self, score):
        text = SMALL_FONT.render(str(score), True, YELLOW)
        GAME_DISPLAY.blit(text,
                          [DISPLAY_WIDTH - 4 * OBJ_SIZE,
                           DISPLAY_HEIGHT - 3.7 * OBJ_SIZE])

    def show_kills(self, friends, enemies):
        dire = 0
        radiant = 0
        if friends.side == 'radiant':
            radiant = friends.enemies_killed
            dire = enemies.enemies_killed
        else:
            dire = friends.enemies_killed
            radiant = enemies.enemies_killed
        self.kill_score['dire'] = dire
        self.kill_score['radiant'] = radiant
        right = FONT.render(str(dire), True, WHITE)
        left = FONT.render(str(radiant), True, WHITE)
        GAME_DISPLAY.blit(left, [DISPLAY_WIDTH / 2 - 4 * OBJ_SIZE, 0])
        GAME_DISPLAY.blit(right, [DISPLAY_WIDTH / 2 + 4 * OBJ_SIZE, 0])

    def show_time(self, time):
        text = FONT.render(str(int(time / 60)) + ":" + str(int(time % 60)),
                           True, WHITE)
        GAME_DISPLAY.blit(text, [DISPLAY_WIDTH / 2 - OBJ_SIZE, 0])

    def button_click(self, button):
        click = pygame.mouse.get_pressed()
        cur = pygame.mouse.get_pos()
        if button.x + button.width > cur[0] > button.x:
            if button.y + button.height > cur[1] > button.y:
                if click[0] == 1:
                    return True
        return False

    def cursor_inside_button(self, cur, button):
        if button.x + button.width > cur[0] > button.x:
            if button.y + button.height > cur[1] > button.y:
                return True
        return False

    def message_to_screen(self, msg, color,
                          width, height, y_displace=0, x_displace=0):
        text_surface, text_rect = text_objects(msg, color)
        text_rect.center = (width / 2) + x_displace, (height / 2) + y_displace
        GAME_DISPLAY.blit(text_surface, text_rect)

    def has_crossing(self, obj_1, obj_2, block_size):
        if obj_1.x >= obj_2.x \
                and obj_1.x <= obj_2.x + block_size \
                or obj_1.x + block_size > obj_2.x \
                and obj_1.x + block_size < obj_2.x + block_size:
            if obj_1.y >= obj_2.y \
                    and obj_1.y <= obj_2.y + block_size:
                return True
        return False

    def inside_boundaries(object):
        return object.x + object.dx > 0 \
            and object.x < DISPLAY_WIDTH*2 \
            and object.y + object.dy > 0 \
            and object.y < DISPLAY_HEIGHT*2

    def move_bullets(self, character, enemy, enemy_castle,
                     game_display, camera):
        for bullet in character.missiles:
            bullet.draw_missile(game_display, bullet.angle, camera)
            for cell in self.game_map:
                if self.has_crossing(bullet, cell, OBJ_SIZE):
                    if cell.kind == 'BRICK':
                        self.game_map.remove(cell)
                        bullet.draw_explosion(game_display, camera)
                        character.missiles.remove(bullet)
                    elif cell.kind == 'iron':
                        bullet.draw_explosion(game_display, camera)
                        character.missiles.remove(bullet)
                    break

            if character.missiles:
                if self.has_crossing(bullet, enemy, OBJ_SIZE):
                    character.missiles.remove(bullet)
                    enemy.draw_explosion(game_display, camera)
                    if isinstance(character, Player):
                        character.gold += 280
                        character.enemies_killed += 1
                        kind = ENEMY_TYPES[random.randrange(0, 3)]
                elif self.has_crossing(bullet, enemy_castle, OBJ_SIZE*2):
                    character.missiles.remove(bullet)
                    enemy_castle.hp -= 10

    def check_castle(self, castle, camera):
        game_over = False
        if castle.hp <= 0:
            castle.state = 'destroyed'
            castle.draw_explosion(GAME_DISPLAY, camera)
            game_over = True
        return game_over

    def calculate_time(self, timer):
        delta = datetime.datetime.now() - timer
        delta_time = delta.seconds
        self.show_time(delta_time)
        return delta_time


def message_to_screen(msg, color, width, height, y_displace=0, x_displace=0):
    text_surface, text_rect = text_objects(msg, color)
    text_rect.center = (width / 2) + x_displace, (height / 2) + y_displace
    GAME_DISPLAY.blit(text_surface, text_rect)


def text_objects(text, color):
    text_surface = FONT.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_button(cur=None):
    if cur is None:
        cur = pygame.mouse.get_pos()
    if cur[1] >= 300 and cur[1] <= 350:
        if cur[0] >= 20 and cur[0] <= 140:
            pygame.draw.rect(GAME_DISPLAY, LIGHT_GREEN, (20, 300, 120, 50))
        elif cur[0] >= 180 and cur[0] <= 320:
            pygame.draw.rect(GAME_DISPLAY, YELLOW, (180, 300, 120, 50))
        elif cur[0] >= 340 and cur[0] <= 480:
            pygame.draw.rect(GAME_DISPLAY, RED_DARK, (340, 300, 120, 50))


def button_click(button):
    click = pygame.mouse.get_pressed()
    cur = pygame.mouse.get_pos()
    if button.x + button.width > cur[0] > button.x:
        if button.y + button.height > cur[1] > button.y:
            if click[0] == 1:
                return True
    return False


def move_bullets(character, enemy_castle,
                 game_display, camera, game_map):
    for bullet in character.missiles:
        bullet.draw_missile(game_display, bullet.angle, camera)
        for cell in game_map:
            if has_crossing(bullet, cell, OBJ_SIZE):
                if cell.kind == 'BRICK':
                    game_map.remove(cell)
                    bullet.draw_explosion(game_display, camera)
                    character.missiles.remove(bullet)
                elif cell.kind == 'iron':
                    bullet.draw_explosion(game_display, camera)
                    character.missiles.remove(bullet)
                break
            elif has_crossing(bullet, enemy_castle, OBJ_SIZE*2):
                character.missiles.remove(bullet)
                enemy_castle.hp -= 10
                break


def score(score):
    text = SMALL_FONT.render(str(score), True, YELLOW)
    GAME_DISPLAY.blit(text,
                      [DISPLAY_WIDTH - 4*OBJ_SIZE,
                       DISPLAY_HEIGHT - 3.7*OBJ_SIZE])


def show_kills(friends):
    dire = 0
    radiant = 0
    right = FONT.render(str(dire), True, WHITE)
    left = FONT.render(str(radiant), True, WHITE)
    GAME_DISPLAY.blit(left, [DISPLAY_WIDTH/2 - 4*OBJ_SIZE, 0])
    GAME_DISPLAY.blit(right, [DISPLAY_WIDTH/2 + 4*OBJ_SIZE, 0])


def draw_itembar(player, game_display):
    game_display.blit(HUD, [0, 18*OBJ_SIZE])
    game_display.blit(TOP_HUD, [0, 0])
    if player.gold > 700:
        if len(player.items) < 6:
            player.items.append('dick')
            player.gold -= 700
    return True


def draw_items(player, game_display):
    counter = 5
    for item in player.items:
        path = f'images/{item}.png'
        t = pygame.image.load(path)
        x = DISPLAY_WIDTH - 105 - int(counter % 3) * 23
        y = DISPLAY_HEIGHT - 40 + int(counter / 3) * 18
        game_display.blit(t, [x, y])
        counter -= 1


def draw_mini_map(player):
    player_x = player.x
    player_y = player.y
    mini_x = 10 + player_x / 97 * 7
    mini_y = DISPLAY_HEIGHT - 90 + player_y / 97 * 7
    player1_sprite = pygame.transform.scale(
        pygame.transform.rotate(PLAYER_SPRITE, player.angle + 270),
        (8, 8))
    GAME_DISPLAY.blit(player1_sprite, [mini_x, mini_y])


def calculate_time(timer):
    delta = datetime.datetime.now() - timer
    delta_time = delta.seconds
    show_time(delta_time)
    return delta_time


def show_time(time):
    text = FONT.render(str(int(time / 60)) + ":" + str(int(time % 60)),
                       True, WHITE)
    GAME_DISPLAY.blit(text, [DISPLAY_WIDTH / 2 - OBJ_SIZE, 0])


def start_screen():
    global MUSIC
    pygame.mixer.Sound(MUSIC['start']).play()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        GAME_DISPLAY.fill(BLACK)
        message_to_screen("BATTLE CITY", RED,
                          DISPLAY_WIDTH, DISPLAY_HEIGHT, -50)
        message_to_screen("Actually just a crappy one", WHITE,
                          DISPLAY_WIDTH, DISPLAY_HEIGHT, 50)
        message_to_screen("Update: replay added : ", WHITE,
                          DISPLAY_WIDTH, DISPLAY_HEIGHT, 70)
        pygame.draw.rect(GAME_DISPLAY, GREEN, (20, 300, 120, 50))
        start_button = pygame.Rect(20, 300, 120, 50)
        pygame.draw.rect(GAME_DISPLAY, LIGHT_YELLOW, (180, 300, 120, 50))
        double_button = pygame.Rect(180, 300, 120, 50)
        pygame.draw.rect(GAME_DISPLAY, RED, (340, 300, 120, 50))
        exit_button = pygame.Rect(340, 300, 120, 50)
        draw_button()
        if button_click(start_button):
            game_loop()
        if button_click(double_button):
            play_replay()
        elif button_click(exit_button):
            pygame.quit()
            quit()
        message_to_screen('Online', WHITE, 120, 50, 300, 20)
        message_to_screen('Replay', WHITE, 120, 50, 300, 180)
        message_to_screen('exit', WHITE, 120, 50, 300, 340)
        pygame.display.update()
        CLOCK.tick(FPS)


def prepare_buttons(keys):
    res = [False for i in range(300)]
    for key in keys:
        if key == "K_LEFT":
            res[pygame.locals.K_LEFT] = True
        elif key == "K_RIGHT":
            res[pygame.locals.K_RIGHT] = True
        elif key == "K_UP":
            res[pygame.locals.K_UP] = True
        elif key == "K_DOWN":
            res[pygame.locals.K_DOWN] = True
        elif key == "K_SPACE":
            res[pygame.locals.K_SPACE] = True
    return res


def check_controls(player, keys, replay=False):
    res = ""
    if replay:
        keys = prepare_buttons(keys)
    if keys[pygame.K_LEFT] and player.x > 0:
        res += 'K_LEFT '
        player.angle += TURN_RATIO
        player.dx = 0
        player.dy = 0
    if keys[pygame.K_RIGHT]:
        res += 'K_RIGHT '
        player.angle -= TURN_RATIO
        player.dx = 0
        player.dy = 0
    if keys[pygame.K_UP] and player.y > 0:
        res += 'K_UP '
        player.dx = math.cos(math.radians(player.angle))*2
        player.dy = -math.sin(math.radians(player.angle))*2
    if keys[pygame.K_DOWN]:
        res += 'K_DOWN '
        player.dx = -math.cos(math.radians(player.angle))*2
        player.dy = math.sin(math.radians(player.angle))*2
    if keys[pygame.K_SPACE]:
        res += 'K_SPACE '
        missile = Missile(player.x, player.y,
                          2, player.dx, player.dy)
        missile.angle = player.angle + 270
        if not player.missiles and len(player.missiles) < 1:
            player.missiles.append(missile)
    else:
        res += 'NONE '
    return res


def check_map_collision(game_map, player, camera):
    for cell in game_map:
        pl_temp = pygame.Rect(player.x + player.dx,
                              player.y + player.dy,
                              OBJ_SIZE,
                              OBJ_SIZE)
        if has_crossing(pl_temp, cell, OBJ_SIZE):
            if cell.kind == 'BRICK' \
                    or cell.kind == 'iron' \
                    or cell.kind == 'WATER':
                player.dx = 0
                player.dy = 0
        camera.follow(cell)
        cell.draw(GAME_DISPLAY, camera)
    return True


def prepare_castles(game_map):
    for cell in game_map:
        if cell.kind == 'castle':
            if cell.side == 'friendly':
                castle = Castle(cell.x, cell.y,
                                OBJ_SIZE*2, 'alive', 'friendly')
            else:
                enemy_castle = Castle(cell.x, cell.y,
                                      OBJ_SIZE*2, 'alive', 'enemy')
    return castle, enemy_castle


def game_loop(test_mode=False):
    global MUSIC
    actions = []
    # HOST = input('ENTER IP OF THE SERVER: ')
    # PORT = input('ENTER PORT IP OF THE SERVER: ')
    PORT = 10030
    if not test_mode:
        net = Network(get_host_ip(), PORT)
    else:
        net = Network("192.168.0.62", PORT)
    song = pygame.mixer.Sound(MUSIC['daisuke'])
    song.play(loops=20)
    game_exit = False
    game_over = False
    shop_active = False
    client = Client(0)
    start_key = net.get_key()
    client.update_net_key(start_key, net)
    timer = datetime.datetime.now()
    camera = Camera(MAP_WIDTH, MAP_HEIGHT)
    castle = Castle(0, 0, OBJ_SIZE, 'alive', 'friendly')
    enemy_castle = Castle(50, 50, OBJ_SIZE, 'alive', 'enemy')
    client.enemy = Enemy(100, 100, 16, 'regular')
    castle, enemy_castle = prepare_castles(client.game_map)

    while not game_exit:
        CLOCK.tick(FPS)
        GAME_DISPLAY.fill(BLACK)
        # while game_over:
        #     GAME_DISPLAY.fill(BLACK)
        #     message_to_screen("Game over", RED,
        #                       DISPLAY_WIDTH, DISPLAY_HEIGHT, -50)
        #     message_to_screen('Press c to play again', WHITE,
        #                       DISPLAY_WIDTH, DISPLAY_HEIGHT, 50)
        #     message_to_screen(' or Q to quit ', WHITE,
        #                       DISPLAY_WIDTH, DISPLAY_HEIGHT, 70)
        #     pygame.display.update()
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             song.stop()
        #             game_exit = True
        #             game_over = False
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_q:
        #                 game_exit = True
        #                 game_over = False
        #             elif event.key == pygame.K_c:
        #                 song.stop()
        #                 game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_replay(actions)
                game_exit = True
        keys = pygame.key.get_pressed()
        res = check_controls(client.player, keys)
        game_over = client.check_castle(castle, camera)
        game_over = client.check_castle(enemy_castle, camera)
        check_map_collision(client.game_map, client.player, camera)
        castle.draw(GAME_DISPLAY, camera)
        enemy_castle.draw(GAME_DISPLAY, camera)
        player_2_key = net.send(client.player.data)
        client.update_enemy_info(player_2_key)
        client.player.bullet_check()
        client.player_2.bullet_check()
        client.enemy_bull_check(player_2_key)
        camera.update(client.player)
        client.player.modify(GAME_DISPLAY, camera, PLAYER_SPRITE)
        client.player_2.modify(GAME_DISPLAY, camera, PLAYER_SPRITE)
        client.move_bullets(client.player, client.player_2,
                            enemy_castle, GAME_DISPLAY,
                            camera)
        client.move_bullets(client.player_2, client.player,
                            castle, GAME_DISPLAY,
                            camera)
        client.draw_itembar(GAME_DISPLAY)
        client.draw_items(GAME_DISPLAY)
        delta_time = client.calculate_time(timer)
        client.show_kills(client.player, client.player_2)
        camera.update(client.player)
        client.score(client.player.gold)
        client.draw_item_description()
        client.draw_mini_map()
        actions.append(res)
        pygame.display.flip()
        t_delta = datetime.datetime.now() - timer
        if t_delta.seconds - delta_time is 1:
            client.player.gold += 2
    if test_mode:
        return
    pygame.quit()
    quit()


def play_replay(filename='replay.txt', test_mode=False):
    global MUSIC
    song = pygame.mixer.Sound(MUSIC['daisuke'])
    song.play(loops=20)
    game_exit = False
    game_over = False
    shop_active = False
    game_map = load_level()
    actions = load_replay(filename)
    start_key = {
        'x': 50,
        'y': 50,
        'player': 0,
        'hp': 100,
        'missiles': [],
        'items': [],
        'enemies_killed': 0,
        'angle': 0,
        'speed': 3,
        'gold': 600,
        'side': 'radiant'
    }
    player = Player(50, 50, 3, 16, 100, 'radiant')
    player.data = start_key
    player.value = start_key['player']
    timer = datetime.datetime.now()
    camera = Camera(MAP_WIDTH, MAP_HEIGHT)
    castle = Castle(0, 0, OBJ_SIZE, 'alive', 'friendly')
    enemy_castle = Castle(50, 50, OBJ_SIZE, 'alive', 'enemy')
    castle, enemy_castle = prepare_castles(game_map)

    for action in actions:
        CLOCK.tick(FPS)
        GAME_DISPLAY.fill(BLACK)
        # while game_over:
        #     GAME_DISPLAY.fill(BLACK)
        #     message_to_screen("Game over", RED,
        #                       DISPLAY_WIDTH, DISPLAY_HEIGHT, -50)
        #     message_to_screen('Press c to play again', WHITE,
        #                       DISPLAY_WIDTH, DISPLAY_HEIGHT, 50)
        #     message_to_screen(' or Q to quit ', WHITE,
        #                       DISPLAY_WIDTH, DISPLAY_HEIGHT, 70)
        #     pygame.display.update()
        #
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             song.stop()
        #             game_exit = True
        #             game_over = False
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_q:
        #                 game_exit = True
        #                 game_over = False
        #             elif event.key == pygame.K_c:
        #                 song.stop()
        #                 game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
        keys = action.split(" ")
        check_controls(player, keys, True)
        check_map_collision(game_map, player, camera)
        castle.draw(GAME_DISPLAY, camera)
        enemy_castle.draw(GAME_DISPLAY, camera)
        player.bullet_check()
        camera.update(player)
        player.modify(GAME_DISPLAY, camera, PLAYER_SPRITE)
        move_bullets(player, enemy_castle, GAME_DISPLAY, camera, game_map)
        draw_itembar(player, GAME_DISPLAY)
        draw_items(player, GAME_DISPLAY)
        delta_time = calculate_time(timer)
        show_kills(player)
        camera.update(player)
        score(player.gold)
        pygame.display.flip()
        t_delta = datetime.datetime.now() - timer
        if t_delta.seconds - delta_time is 1:
            player.gold += 2
    if test_mode:
        return
    pygame.quit()
    quit()


if __name__ == '__main__':
    # start_screen()
    start_screen()
