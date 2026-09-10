from Enemy import Enemy
import Constants as c
import pyxel
from platform import platform


class Icepice(Enemy):
    def __init__(self, coord: list) -> None:
        super().__init__(
            coord=coord, sprite=c.Spr_icepice(0), hitbox=c.icepice_hitbox)
        self.v[0] = 0
        self.__number = 0
        self.__frost_time = 0
        self.__let_movement = True
        self.__platform_frost = False
        self.__frosting_coord = []

    @property
    def platform_frost(self) -> bool:
        return self.__platform_frost

    @platform_frost.setter
    def platform_frost(self, value):
        self.__platform_frost = value

    @property
    def frosting_coord(self):
        return self.__frosting_coord

    @frosting_coord.setter
    def frosting_coord(self, value):
        self.__frosting_coord = value

    def update_status(self, blocks: list, enemies: list):
        """Update icepice"""
        if not self.vulnerable:
            if self.__let_movement:
                self.position()
            else:
                self.__defrost(blocks)
            self.__icepice_movement()
            self.colliding_blocks(blocks)
            self.return_to_pipes()
            self.side_change()
            self.__defrosting_trigger(blocks)
            self.gravity()
        else:
            self.__sound()
        self.__animation()

    def __icepice_movement(self):
        """Let the icepice move"""
        if self.looking_R:
            self.v[0] = c.V_icepice
        else:
            self.v[0] = -c.V_icepice

    def __defrosting_trigger(self, blocks):
        """Set the state of frosting a platform active and which platform is being active"""
        if (
                c.ice_plat_x(0)[0] < self.coord[0] < c.ice_plat_x(0)[1] and self.coord[1] == c.ice_central_plat_y -
                self.hitbox[1] and not c.under_ice["c"]
        ):
            self.__let_movement = False
            self.__platform_frost = True
            c.under_ice["c"] = True # set which platform is being active
        elif (
                c.ice_plat_x(1)[0] < self.coord[0] < c.ice_plat_x(1)[1] and self.coord[1] == c.ice_bot_plat_y -
                self.hitbox[1] and not c.under_ice["l"]
        ):
            self.__let_movement = False
            self.__platform_frost = True
            c.under_ice["l"] = True
        elif (
                c.ice_plat_x(2)[0] < self.coord[0] < c.ice_plat_x(2)[1] and self.coord[1] == c.ice_bot_plat_y -
                self.hitbox[1] and not c.under_ice["r"]
        ):
            self.__let_movement = False
            self.__platform_frost = True
            c.under_ice["r"] = True

    def __defrost(self, blocks):
        """Active the frost of the icepice"""
        self.__frosting_coord = [self.coord[0], self.coord[1] + self.hitbox[1]]
        if self.__frost_time >= c.T_frost_platform:
            for i in (plat for plat in blocks if# Frost every plat of the row
                      isinstance(plat, platform) and plat.coord[1] == self.coord[1] + self.hitbox[1]):

                if i.coord[1] == c.ice_central_plat_y and c.under_ice["c"]:
                    i.platform_frost = True
                elif i.coord[1] == c.ice_bot_plat_y:
                    if 0 <= i.coord[0] <= c.Row_plat[2][0] * c.L_S and c.under_ice["l"]:# checks whether is the left
                        # or right platform the one frost
                        i.platform_frost = True
                    elif c.Row_plat[2][1] * c.L_S <= i.coord[0] <= c.Width and c.under_ice["r"]:
                        i.platform_frost = True

            self.vulnerable = True# destruction of the icepice
            self.animation_time = pyxel.frame_count
            self.get_animation_time(self.animation_time)

        self.__frost_time += 1

    def __animation(self):
        """Animates the icepice"""
        if self.vulnerable:
            if self.get_animation_time(self.animation_time) + 6 <= pyxel.frame_count:
                self.sprite = c.Spr_blank
            elif self.get_animation_time(self.animation_time) + 3 <= pyxel.frame_count:
                self.sprite = c.Spr_icepice(7)
            else:
                self.sprite = c.Spr_icepice(6)
        else:
            self.sprite = c.Spr_icepice(self.__number)
            if pyxel.frame_count % 6 == 0:
                self.__number += 1
            if self.__number > 5:
                self.__number = 0

    def __sound(self):
        """Icepice sound once it dies"""
        if self.get_animation_time(self.animation_time) + 5 <= pyxel.frame_count or pyxel.play_pos(1) is None:
            pyxel.stop(1)
            pyxel.play(1, c.snd_from_assets + len(c.music) + 5)
