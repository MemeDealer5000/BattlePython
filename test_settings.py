import unittest
import client as t
import gameobject as g
import tank
import settings as s
import pygame
import datetime


class TyperTest(unittest.TestCase):
    def test_config_parser(self):
        configs = s.parse_config('test_texts/config.cfg')
        self.assertTrue(configs[0] == "480")  # was 640
        self.assertTrue(configs[1] == "416")
        self.assertTrue(configs[2] == "Battle City")
        self.assertTrue(configs[3] == "25")

    def test_level_loading(self):
        level = t.load_level()
        self.assertTrue(level is not None)
        self.assertTrue(isinstance(level, list))

    def test_client_init(self):
        client = t.Client(0)
        self.assertTrue(isinstance(client, t.Client))

    def test_client_inside_boundaries(self):
        client = t.Client(0)
        enemy = tank.Enemy(50, 50, 50, 'regular')
        self.assertTrue(t.inside_boundaries(enemy))

    def test_crossing_function(self):
        client = t.Client(0)
        enemy = tank.Enemy(50, 50, 50, 'regular')
        player = tank.Player(50, 50, 8, 50, 100, 'radiant')
        self.assertTrue(client.has_crossing(enemy, player, 50))

    def test_check_castle(self):
        client = t.Client(0)
        castle = g.Castle(50, 50, 50, 'alive', 'friendly')
        camera = g.Camera(500, 500)
        self.assertFalse(client.check_castle(castle, camera))

    def test_timer(self):
        clock = datetime.datetime.now()
        client = t.Client(0)
        self.assertLess(client.calculate_time(clock), 1)

    def test_tank(self):
        enemy = tank.Enemy(50, 50, 50, 'regular')
        camera = g.Camera(100, 100)
        game_display = s.GAME_DISPLAY
        enemy.draw(game_display, s.ENEMY_HEAVY_SPRITE, camera)
        self.assertTrue(True)

    def test_tank_explodes(self):
        enemy = tank.Enemy(50, 50, 50, 'regular')
        camera = g.Camera(100, 100)
        game_display = s.GAME_DISPLAY
        enemy.draw_explosion(game_display, camera)
        self.assertTrue(True)

    def test_tank_player(self):
        player = tank.Player(50, 50, 50, 'regular', 100, 'dire')
        camera = g.Camera(100, 100)
        player.modify(s.GAME_DISPLAY, camera, s.PLAYER_SPRITE, True)
        self.assertTrue(True)

    def test_tank_player_shoot(self):
        player = tank.Player(50, 50, 50, 'regular', 100, 'dire')
        camera = g.Camera(100, 100)
        player.missiles.append(g.Missile(10, 10, 10, 10, 10))
        player.missiles.append(g.Missile(-10, -10, 10, 10, 10))
        player.bullet_check()
        self.assertTrue(True)

    def test_enemy_diff(self):
        enemy_fast = tank.Enemy(10, 10, 10, "fast")
        enemy_heavy = tank.Enemy(10, 10, 10, "heavy")
        self.assertTrue(len(enemy_fast.missiles) == 0)

    def test_enemy_movement(self):
        enemy_regular = tank.Enemy(10, 12, 10, "regular")
        enemy_fast = tank.Enemy(10, 10, 10, "fast")
        enemy_heavy = tank.Enemy(12, 10, 10, "heavy")
        dir = enemy_fast.make_move(enemy_heavy)
        self.assertTrue(dir == "left")
        dir = enemy_heavy.make_move(enemy_fast)
        self.assertTrue(dir == "right")
        dir = enemy_regular.make_move(enemy_fast)
        self.assertTrue(dir == "up")
        dir = enemy_fast.make_move(enemy_regular)
        self.assertTrue(dir == "down")

    def test_enemy_shooting(self):
        enemy_regular = tank.Enemy(10, 12, 10, "regular")
        enemy_fast = tank.Enemy(10, 10, 10, "fast")
        enemy_heavy = tank.Enemy(12, 10, 10, "heavy")
        enemy_fast.shoot(enemy_regular, "up")
        self.assertTrue(len(enemy_fast.missiles) == 1)
        enemy_fast.shoot(enemy_regular, "left")
        self.assertTrue(len(enemy_fast.missiles) == 1)
        enemy_fast.shoot(enemy_regular, "right")
        self.assertTrue(len(enemy_fast.missiles) == 1)
        enemy_fast.shoot(enemy_regular, "down")
        self.assertTrue(len(enemy_fast.missiles) == 1)


if __name__ == '__main__':
    unittest.main()
