"""
@author: Héctor Molina Garde & Nicolás Maire Bravo
Mario Bros Arcade
"""
from platform import platform
from POW import POW_block
from Coin import Coin
from Fire_ball import Fire_ball
from ice_spikes import Ice_spikes
import Constants as c
import pyxel


class Mario:

    def __init__(self) -> None:
        self.__sprite = c.Spr_mario_being_still
        self.__hitbox = c.mario_hitbox
        self.__coord = c.mario_position[:]#copy the position
        self.__set_variables()
        self.__initial_forces()
        self.__lives = 3

    # Setters and Getters
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
    def lives(self) -> int:
        return self.__lives

    @lives.setter
    def lives(self, new_lives: int):
        self.__lives = new_lives

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
    def looking_right(self) -> bool:
        return self.__looking_right

    @staticmethod
    def __get_time_from_frame_count(time):
        """It is used to get the value of pyxel.frame_count setting the value """
        return time

    # End of Setters and Getters

    def __initial_forces(self):
        """Set initial values for the forces"""
        self.__v = [0, 0]

    def __set_variables(self):
        # boolean variables
        self.__in_air = True
        self.__moving = False
        self.__jumping = False
        self.__braking = False
        self.__let_control = True
        self.__looking_right = True
        self.mario_dead = False
        self.game_over = False
        self.__blink = True
        self.__collision_R = False
        self.__collision_L = False
        self.__collision_over = False
        self.__collision_under = False
        self.advice_comment = False
        self.__under_ice = False
        self.__platform_hit = False
        self.__jump_sound = False
        self.__dead_by_fire = False
        # int variables
        self.__number = 0


    def __position(self):
        """Change position of mario"""
        self.coord[0] += self.__v[0]
        self.coord[1] += self.__v[1]

    def __mario_die(self):
        """Mario die method"""
        self.lives -= 1
        self.mario_dead = True
        pyxel.stop(0)

    def __mario_game_over(self):
        """Game over method"""
        self.__let_control = False
        pyxel.stop(2)
        pyxel.stop(0)
        self.game_over = True

    def __mario_reviving(self):
        """Once Mario is dead, this process is made, so he revives"""
        if (self.__get_time_from_frame_count(self.__animation_death) + c.T_mar_die3 <= pyxel.frame_count
                and pyxel.btnp(pyxel.KEY_SPACE)):
            self.mario_dead = False
            self.__in_air = True
            self.__let_control = True
            self.advice_comment = False
            self.__dead_by_fire = False
        elif self.__get_time_from_frame_count(self.__animation_death) + c.T_mar_die2 <= pyxel.frame_count:
            if self.lives <= 0:
                self.__mario_game_over()
            else:
                """Mario start blinking so it seems like he is respawning"""
                self.__v[1] = 0
                self.advice_comment = True
                self.sprite = c.Spr_mario_being_still
                if pyxel.frame_count % 3 == 0:
                    #blink part
                    if self.__blink:
                        self.__blink = False
                        self.sprite = c.Spr_mario_being_still
                    else:
                        self.__blink = True
                        self.sprite = c.Spr_blank
                self.__let_control = False
                self.coord = [(c.Width - self.__hitbox[0]) / 2, 20]

        elif self.__get_time_from_frame_count(self.__animation_death) + c.T_mar_die1 <= pyxel.frame_count:
            """Mario falls to the end"""
            if self.__dead_by_fire:
                self.sprite = c.Spr_mario_dyeing(3)
            else:
                self.sprite = c.Spr_mario_dyeing(1)
            self.__v[1] += 0.1

        else:
            """Goes up a little"""
            self.__let_control = False
            if self.__looking_right:
                if self.__dead_by_fire:
                    self.sprite = c.Spr_mario_dyeing(2)
                else:
                    self.sprite = c.Spr_mario_dyeing(0)
            else:
                if self.__dead_by_fire:
                    self.sprite = c.Spr_mario_dyeing(2)
                else:
                    self.sprite = c.Spr_mario_dyeing(0)
            self.__v[1] -= 0.1

    def update_status(self, blocks: list, enemies: list):
        """Update mario behaviourr"""
        self.__position()
        self.__mario_music()
        if self.mario_dead:
            self.__mario_reviving()
        else:
            self.__side_change()
            self.__colliding_stage(blocks, enemies)
            self.__colliding_enemies(enemies)
            self.__gravity()
            self.__movement()
            self.__animation()

    def __side_change(self):
        """For change of side if the window"""
        if self.__coord[0] > c.Width:
            self.__coord[0] = -5
        if self.__coord[0] < -5:
            self.__coord[0] = c.Width
        if self.__coord[1] > c.Height - 16 - self.__hitbox[1]:
            self.__coord[1] = c.Height - 16 - self.__hitbox[1]
        if self.__coord[1] < 0:
            self.__coord[1] = 0

    def __gravity(self):
        """Gravity method"""
        if self.__let_control:  # and not self.__collision_under:
            self.__v[1] += c.V_gravity
        else:
            self.__v[1] = 0

    def __colliding_(self, entity):
        """Generic method for colliding based in axis-aligned bonding boxes"""
        box11 = self.coord
        box12 = [self.coord[0] + self.__hitbox[0] + 1, self.coord[1] + self.__hitbox[1] + 1]
        box21 = entity.coord
        box22 = [entity.coord[0] + entity.hitbox[0] + 1, entity.coord[1] + entity.hitbox[1] + 1]

        # Check for overlap
        if (box21[0] <= box12[0] and
                box22[0] >= box11[0] and
                box21[1] <= box12[1] and
                box22[1] >= box11[1]):
            return True
        else:
            return False

    def __colliding_stage(self, blocks: list, enemies: list):
        """Collision for blocks"""
        self.__collision_R = False
        self.__collision_L = False
        self.__collision_over = False
        self.__collision_under = False
        self.__in_air = True  # Assuming is in the air

        for i in blocks:
            box11 = self.coord # Top left corner
            box12 = [self.coord[0] + self.__hitbox[0] + 1, self.coord[1] + self.__hitbox[1] + 1]# Bottom right corner
            box21 = i.coord
            box22 = [i.coord[0] + i.hitbox[0] + 1, i.coord[1] + i.hitbox[1] + 1]

            # Check for overlap
            if box21[0] <= box12[0] and box22[0] >= box11[0] and box21[1] <= box12[1] and box22[1] >= box11[1]:
                # Determine the side of the collision
                overlap_x = min(box12[0], box22[0]) - max(box11[0], box21[0])
                overlap_y = min(box12[1], box22[1]) - max(box11[1], box21[1])

                # Check if collision is more in the horizontal or vertical direction
                if overlap_x < overlap_y:
                    if not (abs(i.coord[1] - (self.coord[1] + self.__hitbox[1])) <= self.__hitbox[1]):
                        # Collision is more in the horizontal direction
                        if i.coord[0] + i.hitbox[0] / 2 < self.coord[0] + self.__hitbox[0] / 2:
                            # Collision on the left side of self
                            # Handle left side collision
                            self.__v[0] = -self.__v[0]
                        else:
                            # Collision on the right side of self
                            # Handle right side collision
                            self.__v[0] = -self.__v[0]
                else:
                    # Collision is more in the vertical direction
                    if box21[1] + i.hitbox[1] / 2 < self.coord[1] + self.__hitbox[1] / 2:
                        # Collision on the top side of self
                        # Handle top side collision
                        if self.coord[1] - 1 <= i.coord[1] + i.hitbox[1]:
                            if isinstance(i, platform) and not i.platform_frost:
                                i.hit_platform(blocks)
                                self.__platform_hit = True
                            elif isinstance(i, POW_block):
                                i.hit_Pow(enemies)
                        self.__v[1] = 2 * c.V_gravity  # this makes mario fall
                        self.coord[1] = i.coord_initials[1] + i.hitbox[
                            1] + c.collision_tolerance  # this make mario can fall and does not get stuck due to the tolerance
                        self.__collision_over = True
                    else:
                        # Collision on the bottom side of self
                        # Handle bottom side collision
                        self.coord[1] = i.coord[1] - self.__hitbox[1]
                        if isinstance(i, platform) and i.platform_frost:
                            self.__under_ice = True
                        else:
                            self.__under_ice = False
                        self.__collision_under = True
                        self.__in_air = False

                        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_W)) and not self.__in_air:
                            self.__jumping = True
                            self.__jump_sound = True
                            self.__v[1] = -c.V_jump
                            self.__in_air = True
                        else:
                            self.__jumping = False
                            self.__v[1] = 0

    def __colliding_enemies(self, enemies: list):
        """Collision for enemies"""
        for i in enemies:
            if self.__colliding_(i) and i.alive:
                if not i.vulnerable and not isinstance(i, Coin):
                    if not (
                            ((i.coord[0] >= c.Width - 34 or i.coord[0] <= 34) and i.coord[1] <= 32) or
                            i.coord[1] >= c.Height - 32 and (i.coord[0] >= c.Width - 16 or i.coord[0] <= 16)
                            # this avoids mario from a collision in pipes (not really functional)
                            and not (isinstance(i, Ice_spikes) and i.v[1] == 0) #If ice spike is not falling, it wont kill
                    ):
                        if isinstance(i, Fire_ball):
                            self.__dead_by_fire = True
                        self.__v = [0, 0]
                        self.__animation_death = pyxel.frame_count
                        self.__get_time_from_frame_count(self.__animation_death)
                        self.__mario_die()
                else:
                    # Kill the enemy
                    if isinstance(i, Coin):
                        i.collected_by_mario = True
                    i.alive = False
                    i.killed_coord = i.coord.copy()
                    i.killed_coord[1] -= c.Punct_mov

    def __movement(self):
        # This is for Mario's movement
        if self.__let_control:
            if pyxel.btn(pyxel.KEY_D) and not pyxel.btn(
                    pyxel.KEY_A) and not self.__collision_R:  # For moving to the right
                if self.__v[0] < 0:
                    self.__braking = True
                self.__moving = True
                if self.__v[0] < c.V_player_max_x:
                    self.__v[0] += c.V_walk
                else:
                    self.__v[0] = c.V_player_max_x
                self.__looking_right = True
            elif not pyxel.btn(pyxel.KEY_A) and self.__looking_right:
                # This happens so mario gets friction
                self.__moving = False
                if self.__v[0] > 0:
                    if self.__under_ice:
                        self.__v[0] -= c.V_friction_ice
                    else:
                        self.__v[0] -= c.V_friction
                else:
                    self.__v[0] = 0

            if pyxel.btn(pyxel.KEY_A) and not pyxel.btn(
                    pyxel.KEY_D) and not self.__collision_L:  # For moving to the left
                if self.__v[0] > 0:
                    self.__braking = True
                self.__moving = True
                if self.__v[0] > -c.V_player_max_x:
                    self.__v[0] -= c.V_walk
                else:
                    self.__v[0] = -c.V_player_max_x
                self.__looking_right = False
            elif not pyxel.btn(pyxel.KEY_D) and not self.__looking_right:
                self.__moving = False
                if self.__v[0] < 0:
                    if self.__under_ice:
                        self.__v[0] += c.V_friction_ice
                    else:
                        self.__v[0] += c.V_friction
                else:
                    self.__v[0] = 0

    def __animation(self):
        """animates MArio"""
        def change_direction(sprite):
            """local function to change the direction of the sprite to avoid lines"""
            if self.looking_right:
                self.__sprite = sprite
            else:
                self.__sprite = c.change_direction_spr(sprite)

        if self.__jumping:
            change_direction(c.Spr_mario_jumping)

        else:
            if self.__moving:
                if self.__braking:
                    change_direction(c.Spr_mario_braking1)
                if pyxel.frame_count % 4 == 0:
                    change_direction(c.Spr_mario_running(self.__number))
                    self.__number += 1
                    self.__braking = False
                if self.__number > 4:
                    self.__number = 0
            else:
                change_direction(c.Spr_mario_being_still)

    def __mario_music(self):
        """Mario music"""
        if self.mario_dead:
            """Mario dead"""
            pyxel.stop(2)
            pyxel.stop(3)
            if pyxel.play_pos(0) is None: # this conditional is to not repeat the sound until it is finished
                pyxel.play(0, 2)
        if self.__platform_hit:
            """Mario hit platform"""
            pyxel.stop(0)
            if pyxel.play_pos(0) is None:
                pyxel.play(0, c.snd_from_assets + len(c.music) + 6)
            self.__platform_hit = False
        elif self.__jumping and self.__jump_sound:
            """Mario jumps"""
            pyxel.stop(0)
            self.__jump_sound = False
            if pyxel.play_pos(0) is None:
                pyxel.play(0, c.snd_from_assets + len(c.music) + 4)
        elif self.__moving:
            if pyxel.play_pos(0) is None:
                pyxel.play(0, c.snd_from_assets + len(c.music))
