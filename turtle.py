import pyxel
import Constants as c
from Enemy import Enemy


class Turtle(Enemy):
    def __init__(self, coord: list) -> None:
        super().__init__(
            coord=coord, sprite=c.Spr_turtle(0, 0), hitbox=c.turtle_hitbox)
        self.v[0] = 0
        self.__number = 0
        self.rage = 0

    def update_status(self, blocks: list, enemies: list):
        """update the turtle"""
        self.position()
        if self.alive:
            self.__turtle_movement()
            self.colliding_blocks(blocks)
            self.return_to_pipes()
            self.colliding_enemies(enemies)
            self.side_change()
            self.__animation()
            self.change_of_color()
            self.gravity()
        else:
            self.animation_dying()

    def __turtle_movement(self):
        """turtle moves"""
        if self.vulnerable:
            self.v[0] = 0
        else:
            if self.rage == 1:
                if self.looking_R:
                    self.v[0] = c.V_angry_turtle
                else:
                    self.v[0] = -c.V_angry_turtle
            else:
                if self.looking_R:
                    self.v[0] = c.V_turtle
                else:
                    self.v[0] = -c.V_turtle

    def __animation(self):
        """animate the turtle"""
        if self.vulnerable:
            if self.get_animation_time(self.animation_time) + 25 <= pyxel.frame_count:
                if pyxel.frame_count % 25 == 0:
                    if self.__number == 6:
                        self.__number = 7
                    else:
                        self.__number = 6
                self.sprite = c.Spr_turtle(self.__number, self.rage)
            elif self.get_animation_time(self.animation_time) + 15 <= pyxel.frame_count:
                self.__number = 6
                self.sprite = c.Spr_turtle(4, self.rage)
            else:
                self.sprite = c.Spr_turtle(3, self.rage)

        else:
            if self.looking_R:
                self.sprite = c.Spr_turtle(self.__number, self.rage)
            else:
                self.sprite = c.change_direction_spr(c.Spr_turtle(self.__number, self.rage))
            if pyxel.frame_count % 15 == 0:
                self.__number += 1
            if self.__number > 2:
                self.__number = 0
