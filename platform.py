from Block import block
import Constants as c
import pyxel


class platform(block):
    def __init__(self, coord: list, phase: int, position: int) -> None:
        super().__init__(coord, c.Spr_plat1, [8, 8])
        self.__animation_time = 0
        self.__phase = phase
        self.__position = position
        self.__platform_up = False
        self.__position_collision = ""
        self.__platform_frost = False

    @property
    def phase(self) -> int:
        return self.__phase

    @phase.setter
    def phase(self, new_phase):
        self.__phase = new_phase

    @property
    def position(self) -> int:
        return self.__position

    @position.setter
    def position(self, new_position):
        self.__position = new_position

    @property
    def platform_up(self) -> bool:
        return self.__platform_up

    @platform_up.setter
    def platform_up(self, new_platform_up):
        self.__platform_up = new_platform_up

    @property
    def platform_frost(self) -> bool:
        return self.__platform_frost

    @platform_frost.setter
    def platform_frost(self, value):
        self.__platform_frost = value

    def eq_R(self, other):
        """Check for a platform on the right side"""
        if isinstance(other, platform):
            return self.coord[0] + 8 == other.coord[0] and self.coord[1] == other.coord[1]

    def eq_L(self, other):
        """Check for a platform on the left side"""
        if isinstance(other, platform):
            return self.coord[0] - 8 == other.coord[0] and self.coord[1] == other.coord[1]

    def __phasing_sprite(self, normal_plat: bool):
        """Give the sprite it should to the platform in neutral collision"""
        if self.__platform_frost:  # frost plat
            if self.__position == 0:
                return c.Spr_plat_ice
            elif self.__position == 1:
                return c.Spr_plat_iceR
            elif self.__position == 2:
                return c.Spr_plat_iceL
        else:
            if 0 <= self.__phase <= 1:
                if normal_plat:
                    return c.Spr_plat1
                else:
                    return 0
            elif 3 <= self.__phase <= 4:
                if normal_plat:
                    return c.Spr_plat4
                else:
                    return 3
            if 5 == self.__phase or 7 == self.__phase:
                if normal_plat:
                    return c.Spr_plat5
                else:
                    return 4
            elif self.__phase <= 2:
                if normal_plat:
                    if self.__position == 0:
                        return c.Spr_plat2
                    elif self.__position == 1:
                        return c.Spr_plat2R
                    elif self.__position == 2:
                        return c.Spr_plat2L
                else:
                    return 1
            elif 8 <= self.__phase <= 9:  # coin stage
                if normal_plat:
                    if self.__position == 0:
                        return c.Spr_plat3
                    elif self.__position == 1:
                        return c.Spr_plat3R
                    elif self.__position == 2:
                        return c.Spr_plat3L
                else:
                    return 2

    def update_status(self, phase):
        """Update the state of the platform"""
        self.__phase = phase
        if phase == 6:
            self.__platform_frost = True
            self.sprite = self.__phasing_sprite(True)
        # just animate platform
        if self.__platform_up:
            """Animation of being hit up"""
            animation_time = self.__animation(self.__animation_time)

            if pyxel.frame_count >= animation_time + 15:
                self.sprite = self.__phasing_sprite(True)
                self.__reset_platform()
            elif pyxel.frame_count >= animation_time + 10:
                if self.__position_collision == "Center":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 1, 0)
                elif self.__position_collision == "Left":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 0, 0)
                elif self.__position_collision == "Right":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 2, 0)
                self.coord[1] = self.coord_initials[1] - 3
                self.hitbox[1] = 11

            elif pyxel.frame_count >= animation_time + 3:
                if self.__position_collision == "Center":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 1, 1)
                elif self.__position_collision == "Left":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 0, 1)
                elif self.__position_collision == "Right":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 2, 1)
                self.coord[1] = self.coord_initials[1] - 4
                self.hitbox[1] = 12
            else:
                if self.__position_collision == "Center":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 1, 0)
                elif self.__position_collision == "Left":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 0, 0)
                elif self.__position_collision == "Right":
                    self.sprite = c.Spr_platform_up(self.__phasing_sprite(False), 2, 0)
        else:
            self.sprite = self.__phasing_sprite(True)  # normal sprite

    @staticmethod
    def __animation(time):
        """It is used to get the value of pyxel.frame_count setting the value """
        return time

    def hit_platform(self, blocks):
        """R right, C center, L left.
        Set the platform as if it was hit itself, left and right one changing its properties for collisions"""
        if not self.__platform_up:
            self.__animation_time = pyxel.frame_count

            self.__platform_up = True
            self.__position_collision = "Center"
            for i in blocks:  # look for the right and the left ones
                if self.eq_L(i):
                    i.__position_collision = "Left"
                elif self.eq_R(i):
                    i.__position_collision = "Right"
                if self.eq_R(i) or self.eq_L(i):
                    i.__animation_time = pyxel.frame_count
                    i.__animation(i.__animation_time)
                    i.__platform_up = True
                    i.coord[1] = i.coord_initials[1] - 3
                    i.hitbox[1] = 11

            self.__animation(self.__animation_time)
            self.coord[1] = self.coord_initials[1] - 3
            self.hitbox[1] = 11

    def __reset_platform(self):
        """Reset the platform to it's initial values after being hit up"""
        self.__animation_time = 0
        self.coord[1] = self.coord_initials[1]
        self.hitbox[1] = 8
        self.__platform_up = False
        self.__position_collision = ""
