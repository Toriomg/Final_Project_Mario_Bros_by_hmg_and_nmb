"""
@author: Héctor Molina Garde & Nicolás Maire Bravo
Mario Bros Arcade
"""
import pyxel

import Constants as c
from platform import platform


class Enemy:
    def __init__(self, coord: list, sprite: list, hitbox: list) -> None:
        self.__coord = coord
        self.__coord_initials = self.__coord.copy()
        self.__sprite = sprite
        self.__alive = True  # enemy alive
        self.__spawned = False
        self.__rage = 0
        self.__v = [0, 0]
        self.__killed_coord = []
        self.__hitbox = hitbox
        if self.__coord_initials[0] < c.Width / 2:
            self.__looking_R = True
        else:
            self.__looking_R = False
        self.__vulnerable = False
        self.in_air = True
        self.animation_time = 0
        self.__sound_dying = False
        self.__splash_animation_number = 0

    @property
    def sprite(self) -> list:
        return self.__sprite

    @sprite.setter
    def sprite(self, new_sprite: list):
        if type(new_sprite) != list:
            raise ValueError("sprite must be a list")
        elif len(new_sprite) != 6:
            raise ValueError("list must have 6 elements")
        else:
            self.__sprite = new_sprite

    @property
    def hitbox(self) -> list:
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, new_hitbox):
        if type(new_hitbox) != list:
            raise ValueError("hitbox. must be a list")
        elif len(new_hitbox) != 2:
            raise ValueError('List must have only 2 elements')
        else:
            self.__hitbox = new_hitbox

    @property
    def coord(self) -> list:
        return self.__coord

    @coord.setter
    def coord(self, new_coord):
        if type(new_coord) != list:
            raise ValueError("Coords. must be a list")
        elif len(new_coord) != 2:
            raise ValueError('List must have only 2 elements')
        else:
            self.__coord = new_coord

    @property
    def coord_initials(self) -> list:
        return self.__coord_initials

    @coord_initials.setter
    def coord_initials(self, new_coord_initials):
        if type(new_coord_initials) != list:
            raise ValueError("Coords. must be a list")
        elif len(new_coord_initials) != 2:
            raise ValueError('List must have only 2 elements')
        else:
            self.__coord_initials = new_coord_initials

    @property
    def v(self) -> list:
        return self.__v

    @v.setter
    def v(self, new_v):
        if type(new_v) != list:
            raise ValueError("Coords. must be a list")
        elif len(new_v) != 2:
            raise ValueError('List must have only 2 elements')
        else:
            self.__v = new_v

    @property
    def looking_R(self) -> bool:
        return self.__looking_R

    @looking_R.setter
    def looking_R(self, value):
        self.__looking_R = value

    @property
    def alive(self) -> bool:
        return self.__alive

    @alive.setter
    def alive(self, value):
        self.__alive = value

    @property
    def spawned(self) -> bool:
        return self.__spawned

    @spawned.setter
    def spawned(self, value):
        self.__spawned = value

    @property
    def killed_coord(self) -> list:
        return self.__killed_coord

    @killed_coord.setter
    def killed_coord(self, new_coord):
        if isinstance(new_coord, list):
            self.__killed_coord = new_coord
        else:
            raise ValueError("killed_coord must be a list")

    @property
    def vulnerable(self):
        return self.__vulnerable

    @vulnerable.setter
    def vulnerable(self, value):
        if not isinstance(value, bool):
            raise ValueError("vulnerable must be a boolean")
        self.__vulnerable = value

    @property
    def rage(self):
        return self.__rage

    @rage.setter
    def rage(self, value):
        if not isinstance(value, int):
            raise ValueError("rage must be an integer")
        self.__rage = value

    @property
    def splash_animation_number(self):
        return self.__splash_animation_number

    @splash_animation_number.setter
    def splash_animation_number(self, value):
        if not isinstance(value, int):
            raise ValueError("splash_animation_number must be an integer")
        self.__splash_animation_number = value

    @staticmethod
    def get_animation_time(time):
        """It is used to get the value of pyxel.frame_count setting the value """
        return time

    def position(self):
        """Change position of enemy"""
        self.coord[0] += self.v[0]
        self.coord[1] += self.v[1]

    def side_change(self):
        """For change of side if the window"""
        if self.__coord[0] > c.Width:
            self.__coord[0] = c.extra_distance_side_change
        if self.__coord[0] < c.extra_distance_side_change:
            self.__coord[0] = c.Width

    def collision(self, entity, blocks_as_collision: bool):
        """Generic method for colliding based in axis-aligned bonding boxes"""
        box11 = self.coord  # Top left corner
        box12 = [self.coord[0] + self.__hitbox[0] + 1, self.coord[1] + self.__hitbox[1] + 1]  # Bottom right corner
        box21 = entity.coord  # Top left corner
        box22 = [entity.coord[0] + entity.hitbox[0] + 1, entity.coord[1] + entity.hitbox[1] + 1]  # Bottom right corner

        # Check for overlap
        if (box21[0] <= box12[0] and box22[0] >= box11[0] and box21[1] <= box12[1] and box22[1] >= box11[1]):
            # Determine the side of the collision
            overlap_x = min(box12[0], box22[0]) - max(box11[0], box21[0])
            overlap_y = min(box12[1], box22[1]) - max(box11[1], box21[1])

            # Check if collision is more in the horizontal or vertical direction
            if overlap_x < overlap_y:
                # Collision is more in the horizontal direction
                if entity.coord[0] + entity.hitbox[0] / 2 < self.coord[0] + self.__hitbox[0] / 2:
                    # Collision on the left side of self
                    # Handle left side collision
                    if blocks_as_collision:
                        return False
                    else:
                        return True
                else:
                    # Collision on the right side of self
                    # Handle right side collision
                    if blocks_as_collision:
                        return False
                    else:
                        return True
            else:
                # Collision is more in the vertical direction
                if box21[1] + entity.hitbox[1] / 2 < self.coord[1] + self.__hitbox[1] / 2:
                    # Collision on the top side of self
                    # Handle top side collision
                    if blocks_as_collision:
                        return False
                    else:
                        return True
                else:
                    # Collision on the bottom side of self
                    # Handle bottom side collision
                    return True
        else:
            return False

    def colliding_blocks(self, blocks: list):
        """Collision for blocks"""
        for i in blocks:
            if self.collision(i, True):
                self.coord[1] = i.coord[1] - self.__hitbox[1]
                self.__v[1] = 0
                self.in_air = False
                if isinstance(i, platform) and i.platform_up:
                    # If the platform is hit by mario
                    self.__vulnerable = True
                    self.animation_time = pyxel.frame_count
                    self.get_animation_time(self.animation_time)
        if (self.coord[0] >= c.Width - 42 or self.coord[0] <= 42) and self.coord[1] <= 33:
            self.__coord[1] = 48 - self.__hitbox[1]
            self.__v[1] = 0

    def change_of_color(self):
        """For enemy turning around and activating
         the rage mode to go faster and change the color"""
        if self.__vulnerable and self.get_animation_time(self.animation_time) + c.T_vulnerable_off <= pyxel.frame_count:
            self.__vulnerable = False
            self.__rage = 1

    def colliding_enemies(self, enemies: list):
        """Collision for enemies"""
        for i in enemies:
            if (self.collision(i, False)
                    and not (self.coord[0] >= c.Width - 16 or self.coord[0] <= 16)
                    and not self.vulnerable
                    and not i.vulnerable
                    and self.__looking_R != i.looking_R
            ):
                if self.__looking_R:#Change direction of itself
                    self.__looking_R = False
                    self.coord[0] = self.coord[0] - self.__hitbox[0]
                else:
                    self.__looking_R = True
                    self.coord[0] += 2

    def return_to_pipes(self):
        """Once the enemy is down, it comes up again to the initial pipes"""
        if self.coord[1] >= c.Pipe_bot and (self.coord[0] >= c.Pipe_right):
            self.looking_R = False
            self.coord = [c.Pipe_right + 2, c.Pipe_top]
            self.sprite = c.change_direction_spr(self.sprite)
        if self.coord[1] >= c.Pipe_bot and (self.coord[0] <= c.Pipe_left):
            self.looking_R = True
            self.coord = [c.Pipe_left - 2, c.Pipe_top]
        if (self.coord[0] >= c.Pipe_right - 2 or self.coord[0] <= c.Pipe_left + 2) and self.coord[1] <= c.Pipe_top:
            # Avoid the falling from the top pipes, so there is a collision
            self.coord[1] = c.Pipe_top + c.L_M - self.hitbox[1]
            self.v[1] = 0

    def gravity(self):
        """Gravity method"""
        self.v[1] += c.V_gravity

    def animation_dying(self):
        """Animation once the enmy is dying and falling"""
        if not self.__sound_dying:
            pyxel.stop(1)
            pyxel.play(1, c.snd_from_assets + len(c.music) + 2)#sound
            self.__sound_dying = True
        self.__v[1] += 0.1#falls
        if self.__coord[1] >= c.Height - self.__hitbox[1]:#when falls start the animation
            self.__v[1] = 0
            self.coord[1] = c.Height - self.__hitbox[1]
            if pyxel.frame_count % 6 == 0:
                self.sprite = c.Spr_splash_out(self.__splash_animation_number)
                self.__splash_animation_number += 1
            if self.__splash_animation_number > 5:
                self.sprite = c.Spr_blank # When the sprite is in blank, the enemy is deleated
