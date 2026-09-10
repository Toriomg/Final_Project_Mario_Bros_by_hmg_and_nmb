from Enemy import Enemy
from platform import platform
import Constants as c
import pyxel
import random


class Fire_ball(Enemy):
    def __init__(self, coord: list, color: int):
        super().__init__(
            coord=coord, sprite=c.Spr_fireball(0, color), hitbox=c.fire_ball_hitbox)
        self.__number = 0
        self.__time = 0
        self.__color = color
        self.__acc = 0
        if self.coord[0] != c.Width:
            self.looking_R = False
        if self.__color == 0:
            self.v = [1, 1]
        else:
            if self.__time >= 10 * c.Fps:
                self.alive = False
            else:
                self.v[1] = c.Amplitude * c.Angular_speed * pyxel.cos(c.Angular_speed * self.__time)
                self.v[0] = c.V_angry_turtle / 2

    def update_status(self, blocks: list, enemies: list):
        if self.alive:
            self.position()
            self.__bounce()
            self.__movement()
            self.__being_hit_by_plat(blocks)
            if self.vulnerable:
                self.alive = False
            self.__time += 1
        self.__animation()

    def __movement(self):
        """Change the direction like the DvD screensaver"""
        if self.coord[0] > c.Width - self.hitbox[0]:
            self.v[0] = -self.v[0]
            self.looking_R = False
            self.coord[0] = c.Width - self.hitbox[0]
        if self.coord[0] < 0:
            self.v[0] = -self.v[0]
            self.looking_R = True
            self.coord[0] = 0
        if self.coord[1] > c.Height - c.L_M - self.hitbox[1]:
            self.v[1] = -self.v[1]
            self.coord[1] = c.Height - c.L_M - self.hitbox[1]
        if self.coord[1] < 0:
            self.v[1] = -self.v[1]
            self.coord[1] = 0

    def __bounce(self):
        """movement of fire ball"""
        if self.__color == 1:
            if self.__time >= random.randint(10, 20) * c.Fps:
                self.alive = False
            else:
                # Harmonic wave movement
                self.v[1] = c.Amplitude * c.Angular_speed * pyxel.cos(c.Angular_speed * self.__time)
                if self.looking_R:  # change direction
                    self.v[0] = c.V_angry_turtle / 2
                else:
                    self.v[0] = -c.V_angry_turtle / 2

    def __being_hit_by_plat(self, blocks: list):
        """the ball is killed if it is hit"""
        for i in blocks:
            if self.collision(i, False):
                if isinstance(i, platform) and i.platform_up:
                    self.alive = False
                    self.animation_time = pyxel.frame_count
                    self.get_animation_time(self.animation_time)

    def __animation(self):
        """Animation of the fireball"""
        if not self.alive:
            #death animation
            if pyxel.frame_count % 7 == 0:
                self.sprite = c.Spr_fireball(self.__number, self.__color)
                self.__number += 1
            if self.__number > 9:
                self.sprite = c.Spr_blank
        else:
            if pyxel.frame_count % 4 == 0:
                self.__number += 1
                if self.__number > 3:
                    self.__number = 0
            self.sprite = c.Spr_fireball(self.__number, self.__color)
