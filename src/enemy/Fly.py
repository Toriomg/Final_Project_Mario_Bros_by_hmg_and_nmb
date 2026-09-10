import Constants as c
from Enemy import Enemy
from platform import platform
import pyxel


class Fly(Enemy):
    def __init__(self, coord: list) -> None:
        super().__init__(
            coord=coord, sprite=c.Spr_fly(0, 0), hitbox=c.fly_hitbox)
        self.__number = 0
        self.rage = 0
        self.__jumping = False
        self.__initial_forces()

    def update_status(self, blocks: list, enemies: list):
        self.position()
        if self.alive:
            self.__fly_gravity()
            self.__fly_movement()
            self.__fly_colliding_blocks(blocks)
            self.return_to_pipes()
            self.colliding_enemies(enemies)
            self.side_change()
            self.change_of_color()
            self.__animation()
        else:
            self.animation_dying()

    def __initial_forces(self):
        """Set initial values for the forces"""
        self.__v = [0, 0]

    def __fly_movement(self):
        if self.vulnerable:
            self.v[0] = 0
        else:
            if self.rage == 1:
                if self.looking_R:
                    self.v[0] = c.V_fly + 0.25
                else:
                    self.v[0] = -c.V_fly - 0.25
            else:
                if self.looking_R:
                    self.v[0] = c.V_fly
                else:
                    self.v[0] = -c.V_fly
            if not self.in_air:
                # Jumps if
                self.v[1] = -c.V_jump_fly
                self.in_air = True

    def __fly_colliding_blocks(self, blocks: list):

        for i in blocks:
            if self.collision(i, True):
                self.coord[1] = i.coord[1] - self.hitbox[1]
                self.in_air = False
                if isinstance(i, platform) and i.platform_up:
                    self.vulnerable = True
                    self.animation_time = pyxel.frame_count
                    self.get_animation_time(self.animation_time)


    def __fly_gravity(self):
        if not self.in_air:
            self.v[1] = 0
        else:
            self.v[1] += c.V_gravity_fly

    def __animation(self):
        if self.vulnerable:
            if pyxel.frame_count % 15 == 0:
                if self.__number == 4:
                    self.__number = 5
                else:
                    self.__number = 4
            self.sprite = c.Spr_fly(self.__number, self.rage)
        else:
            if pyxel.frame_count % 10 == 0:
                self.__number += 1
            if self.__number > 3:
                self.__number = 0
            self.sprite = c.Spr_fly(self.__number, self.rage)