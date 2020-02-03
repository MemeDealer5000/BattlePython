import unittest
import gameobject as go
import settings as s
import pygame
import tank
import client as cl
import datetime


cliient = cl.Client(0)


class GameObjectTest(unittest.TestCase):
    def test_test(self):
        self.assertTrue(1 == 1)

    def test_initialization(self):
        game_object = go.GameObject(50, 50, 50)
        self.assertTrue(isinstance(game_object, go.GameObject))

    def test_terrain_init(self):
        terrain = go.Terrain(0, 0, 25, 'WATER')
        self.assertTrue(isinstance(terrain, go.Terrain))

    def test_terrain_equality(self):
        water = go.Terrain(50, 50, 50, 'WATER')
        iron = go.Terrain(50, 50, 50, 'IRON')
        self.assertFalse(water == iron)

    def test_camera_init(self):
        camera = go.Camera(500, 500)
        self.assertTrue(isinstance(camera, go.Camera))

    def test_castle_init(self):
        castle = go.Castle(50, 50, 50, 'alive', 'friendly')
        self.assertTrue(isinstance(castle, go.Castle))
        self.assertTrue(castle.hp == 500)

    def test_tower_init(self):
        tower = go.Tower(50, 50, 50,  'friendly')
        self.assertTrue(isinstance(tower, go.Tower))
        self.assertTrue(tower.hp == 300)

    def test_crossing_func(self):
        game_object_1 = go.GameObject(50, 50, 50)
        game_object_2 = go.GameObject(50, 50, 50)
        result = go.has_crossing(game_object_1, game_object_2, 16)
        self.assertTrue(result)
        game_object_1 = go.GameObject(50, 51, 50)
        game_object_2 = go.GameObject(50, 100, 50)
        result = go.has_crossing(game_object_1, game_object_2, 16)
        self.assertFalse(result)

    def test_gameobject_explosion(self):
        camera = go.Camera(500, 500)
        game_object_1 = go.GameObject(50, 50, 50)
        game_display = s.GAME_DISPLAY
        game_object_1.draw_explosion(game_display, camera)
        self.assertTrue(True)

    def test_camera_update(self):
        camera = go.Camera(500, 500)
        game_object_1 = go.GameObject(50, 50, 50)
        camera.update(game_object_1)
        self.assertTrue(True)

    def test_terrain_draw(self):
        game_display = s.GAME_DISPLAY
        camera = go.Camera(500, 500)
        water = go.Terrain(0, 0, 25, 'WATER')
        iron = go.Terrain(0, 0, 25, 'iron')
        bush = go.Terrain(0, 0, 25, 'BUSH')
        brick = go.Terrain(0, 0, 25, 'BRICK')
        iron_floor = go.Terrain(0, 0, 25, "IRON_FLOOR")
        water.draw(game_display, camera)
        iron.draw(game_display, camera)
        bush.draw(game_display, camera)
        brick.draw(game_display, camera)
        iron_floor.draw(game_display, camera)
        self.assertTrue(True)

    def test_castle_draw(self):
        game_display = s.GAME_DISPLAY
        camera = go.Camera(500, 500)
        castle = go.Castle(0, 0, 16, "alive", "dire")
        castle.draw(game_display, camera)
        castle.state = "destroyed"
        castle.draw(game_display, camera)
        self.assertTrue(True)

    def test_replay_saving(self):
        action = "NONE"
        cl.save_replay([action], "rep_test.txt")
        with open("rep_test.txt", "r") as file:
            self.assertIsNotNone(file.read())

    def test_replay_loading(self):
        data = cl.load_replay()
        self.assertIsNotNone(data)

    def test_itembar_drawing(self):
        result = False
        game_display = s.GAME_DISPLAY
        cliient.draw_itembar(game_display)
        result = True
        cliient.player.gold = 800
        cliient.draw_itembar(game_display)
        cliient.draw_items(game_display)
        self.assertTrue(result)

    def test_text_rendering(self):
        res = cliient.text_objects("Test", s.BLACK)
        self.assertTrue(isinstance(res, tuple))

    def test_minimap_draw(self):
        cliient.draw_mini_map()
        self.assertTrue(True)

    def test_description_draw(self):
        cliient.show_description(0, (0, 0))
        cliient.player.items.append("dick")
        cliient.show_description(0, (0, 0))
        self.assertTrue(True)

    def test_random_explosion(self):
        game_display = s.GAME_DISPLAY
        camera = go.Camera(500, 500)
        cliient.draw_explosion(game_display, 0, 0, camera)
        self.assertTrue(True)

    def test_score_blit(self):
        cliient.score(40)
        self.assertTrue(True)

    def test_main_score_blit(self):
        player = tank.Player(0, 0, 0, 20, 100, "radiant")
        player2 = tank.Player(0, 0, 0, 20, 100, "dire")
        cliient.show_kills(player, player2)
        cliient.show_kills(player2, player)
        self.assertTrue(True)

    def test_cur_inside_button(self):
        button = pygame.Rect(0, 0, 20, 20)
        cur = (1, 1)
        res = cliient.cursor_inside_button(cur, button)
        self.assertTrue(res)
        cur = (50, 50)
        res = cliient.cursor_inside_button(cur, button)
        self.assertFalse(res)

    def test_button_drawing(self):
        done = False
        cur1 = (20, 300)
        cur2 = (180, 300)
        cur3 = (340, 300)
        cliient.draw_button(cur1)
        cliient.draw_button(cur2)
        cliient.draw_button(cur3)
        done = True
        self.assertTrue(done)

    def test_bullets_movement(self):
        player = tank.Player(0, 0, 0, 20, 100, "radiant")
        enemy = tank.Enemy(30, 30, 0, "regular")
        missile = go.Missile(0, 0, 16, 2, 2)
        player.missiles.append(missile)
        game_display = s.GAME_DISPLAY
        camera = go.Camera(500, 500)
        castle = go.Castle(20, 20, 16, "alive", "dire")
        cliient.move_bullets(player, enemy, castle, game_display, camera)
        missile1 = go.Missile(30, 30, 16, 2, 2)
        player.missiles.append(missile1)
        cliient.move_bullets(player, enemy, castle, game_display, camera)
        missile2 = go.Missile(20, 20, 16, 2, 2)
        player.missiles.append(missile2)
        cliient.move_bullets(player, enemy, castle, game_display, camera)
        self.assertTrue(True)

    def test_castle_check(self):
        camera = go.Camera(500, 500)
        castle = go.Castle(20, 20, 16, "alive", "dire")
        castle.hp = 0
        result = cliient.check_castle(castle, camera)
        self.assertTrue(True)

    def test_mes_to_scr(self):
        cl.message_to_screen("BATTLE CITY", s.RED,
                             s.DISPLAY_WIDTH, s.DISPLAY_HEIGHT, -50)
        self.assertTrue(True)

    def test_button_drawing_cl(self):
        done = False
        cur1 = (20, 300)
        cur2 = (180, 300)
        cur3 = (340, 300)
        cl.draw_button(cur1)
        cl.draw_button(cur2)
        cl.draw_button(cur3)
        done = True
        self.assertTrue(done)

    def test_move_bullets_cl(self):
        game_map = cliient.game_map
        player = tank.Player(0, 0, 0, 20, 100, "radiant")
        missile = go.Missile(1, 1, 16, 2, 2)
        missile2 = go.Missile(20, 20, 16, 2, 2)
        missile3 = go.Missile(0, 0, 2500, 2, 2)
        player.missiles.append(missile2)
        game_display = s.GAME_DISPLAY
        camera = go.Camera(500, 500)
        castle = go.Castle(20, 20, 16, "alive", "dire")
        cl.move_bullets(player, castle, game_display, camera, game_map)
        player.missiles.append(missile)
        cl.move_bullets(player, castle, game_display, camera, game_map)
        player.missiles.append(missile3)
        cl.move_bullets(player, castle, game_display, camera, game_map)
        self.assertTrue(True)

    def test_kills_show_cl(self):
        cl.show_kills(0)
        self.assertTrue(True)

    def test_draw_item_cl(self):
        player = tank.Player(0, 0, 0, 20, 100, "radiant")
        player.gold = 800
        game_display = s.GAME_DISPLAY
        res = cl.draw_itembar(player, game_display)
        self.assertTrue(res)

    def test_draw_items_cl(self):
        player = tank.Player(0, 0, 0, 20, 100, "radiant")
        player.items.append("dick")
        game_display = s.GAME_DISPLAY
        cl.draw_items(player, game_display)
        self.assertTrue(True)

    def test_draw_item_cl(self):
        player = tank.Player(0, 0, 0, 20, 100, "radiant")
        game_display = s.GAME_DISPLAY
        cl.draw_mini_map(player)
        self.assertTrue(True)

    def test_time_calc(self):
        time = datetime.datetime.now()
        delta = cl.calculate_time(time)
        self.assertTrue(delta == 0)

    def test_cl_control_check(self):
        player = tank.Player(1, 1, 0, 20, 100, "radiant")
        keys = ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_SPACE"]
        res = cl.check_controls(player, keys, True)
        self.assertIsNotNone(res)

    def test_map_collision(self):
        player = tank.Player(0, 0, 0, 20, 100, "radiant")
        camera = go.Camera(500, 500)
        game_map = cliient.game_map
        res = cl.check_map_collision(game_map, player, camera)
        self.assertTrue(res)

    def test_castle_preparation(self):
        game_map = cliient.game_map
        c1, c2 = cl.prepare_castles(game_map)
        self.assertTrue(isinstance(c1, go.Castle))
        self.assertTrue(isinstance(c2, go.Castle))

    def test_replay_loop(self):
        cl.play_replay("full_rep_test.txt", True)
        self.assertTrue(True)

    def test_main_game_loop_cl(self):
        cl.game_loop(True)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
