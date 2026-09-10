from Enemy import Enemy
import Constants as c
import pyxel


class Ice_spikes(Enemy):
    def __init__(self, coord_x: int):
        super().__init__(
            coord=[coord_x, c.ice_spikes_position_y], sprite=c.Spr_ice_spike(0), hitbox=c.icepice_hitbox)
        self.__number = 0
        self.__time = 0

    def update_status(self, blocks: list, enemies: list):
        self.position()
        self.__animation()
        self.__falling()
        self.__time += 1


    def __falling(self):
        """Ice spike falls"""
        if self.coord[1] >= c.Height:
            # It gets destroyed once it reaches the end of the screen
            self.sprite = c.Spr_blank
        elif self.__time >= 2*c.Fps:
            # Once a time has passed it falls
            self.v[1] += 0.1

    def __animation(self):
        if self.__number > 2:
            if pyxel.frame_count % 15 == 0:
                self.__number += 1
                if self.__number > 5:
                    self.__number = 3
            self.sprite = c.Spr_ice_spike(self.__number)
        else:
            if pyxel.frame_count % 20 == 0:
                self.__number += 1
            self.sprite = c.Spr_ice_spike(self.__number)