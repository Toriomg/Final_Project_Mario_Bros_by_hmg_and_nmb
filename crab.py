import Constants as c
import pyxel
from Enemy import Enemy
from platform import platform


class Crab(Enemy):
    """Look for documentation in Enemy and in Turtle, only commented non-common parts"""
    def __init__(self, coord: list) -> None:
        super().__init__(
            coord=coord, sprite=c.Spr_crab(0, 0), hitbox=c.crab_hitbox)
        self.v[0] = 0
        self.__number = 0
        self.__crab_angry = False
        self.rage = 0

    def update_status(self, blocks: list, enemies: list):
                self.position()
                if self.alive:
                    self.gravity()
                    self.__crab_movement()
                    self.__crab_colliding_blocks(blocks)
                    self.return_to_pipes()
                    self.colliding_enemies(enemies)
                    self.side_change()
                    self.__animation()
                    self.__crab_change_of_color()
                else:
                    self.animation_dying()

    def __crab_movement(self):
        if self.vulnerable:
            self.v[0] = 0
        else:
            if self.rage == 1:
                if self.looking_R:
                    self.v[0] = c.V_crab + 0.25
                else:
                    self.v[0] = -c.V_crab - 0.25
            else:
                if self.looking_R:
                    self.v[0] = c.V_crab
                else:
                    self.v[0] = -c.V_crab

    def __crab_change_of_color(self):
        if self.vulnerable and self.get_animation_time(self.animation_time) + c.T_vulneable_off <= pyxel.frame_count:
            self.vulnerable = False
            self.rage = 1
            self.__crab_angry = False#diferent for reset the anger of the crab

    def __crab_colliding_blocks(self, blocks: list):

        for i in blocks:
            if self.collision(i, True):
                self.coord[1] = i.coord[1] - self.hitbox[1]
                self.v[1] = 0
                self.in_air = False
                if isinstance(i, platform) and i.platform_up:
                    if not self.__crab_angry:
                        self.__crab_angry = True
                        self.__number = 6
                        self.animation_time = pyxel.frame_count
                        self.get_animation_time(self.animation_time)
                    elif self.get_animation_time(self.animation_time) + 28 <= pyxel.frame_count:
                        self.vulnerable = True #start an anger in the crab
                        self.animation_time = pyxel.frame_count
                        self.get_animation_time(self.animation_time)
        if (self.coord[0] >= c.Width - 42 or self.coord[0] <= 42) and self.coord[1] <= 32:
            self.coord[1] = 48 - self.hitbox[1]
            self.v[1] = 0

    def __animation(self):
        if self.vulnerable:
            if pyxel.frame_count % 30 == 0:
                if self.__number == 4:
                    self.__number = 5
                else:
                    self.__number = 4
            self.sprite = c.Spr_crab(self.__number, self.rage)
        else:
            if not self.__crab_angry:
                if self.looking_R:
                    self.sprite = c.Spr_crab(self.__number, self.rage)
                else:
                    self.sprite = c.change_direction_spr(c.Spr_crab(self.__number, self.rage))
                if pyxel.frame_count % 15 == 0:
                    self.__number += 1
                if self.__number > 3:
                    self.__number = 0
            else:
                if self.looking_R:
                    self.sprite = c.Spr_crab(self.__number, self.rage)
                else:
                    self.sprite = c.change_direction_spr(c.Spr_crab(self.__number, self.rage))
                if pyxel.frame_count % 15 == 0:
                    self.__number += 1
                if self.__number > 9:
                    self.__number = 6
