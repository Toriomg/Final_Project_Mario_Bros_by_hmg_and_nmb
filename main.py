"""
@author: Héctor Molina Garde & Nicolás Maire Bravo
Mario Bros Arcade
"""

# /// script
# requires-python = ">=3.10"
# dependencies = ["pyxel>=2.0"]
# ///

import pyxel
import random
from mario_module import Mario
from platform import platform
from brick_floor import brick
from POW import POW_block
from pipe import pipe
from turtle import Turtle
from crab import Crab
from Fly import Fly
from icepice import Icepice
from ice_spikes import Ice_spikes
from Fire_ball import Fire_ball
from Coin import Coin
from Highscore import highscore
import Constants as c


class Game:
    def __init__(self) -> None:
        pyxel.init(c.Width, c.Height, title="MARIO BROS. ARCADE by Héctor Molina and Nicolás Maire", fps=60)
        pyxel.load(c.Assets_path)
        self.__init_variables()
        # creation of objects and lists fo objects
        self.mario = Mario()
        self.highscore = highscore()
        self.__generate_stage()
        self.__generate_pipes()
        self.__generate_enemies()
        self.update()
        self.draw()
        pyxel.run(self.update, self.draw)  # start game

    def update(self):
        self.__music()  # sound music
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()  # close game
        else:
            if self.in_menu:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.in_menu = False  # Start enter screen
            elif self.mario.game_over:
                # lose
                self.highscore.write_score()
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.__reset_game()
            elif self.__screens > 9:
                # win
                self.__game_won = True
                self.highscore.write_score()
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.__reset_game()
            elif self.__screen_end:  # next stage screen
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.__screen_end = False  # start screen
            else:
                self.highscore.sort_highscore()
                self.__spawn_enemies()
                # print(len(self.__active_enemies), len(self.__enemies[self.__screens]), self.__killed_enemies) #to check the enemies alive
                self.mario.update_status(self.__stage, self.__active_enemies)  # update os objects
                self.__block_update()
                self.__enemy_update()
                if self.__killed_enemies == len(self.__enemies[self.__screens]):  # end screen
                    self.__next_level()

    def draw(self):
        if pyxel.frame_count % c.T_H_flipflop == 0:  # this is for time-based aniamtions
            if self.__flip_flop == 0:
                self.__flip_flop = 1
            elif self.__flip_flop == 1:
                self.__flip_flop = 0

        if self.in_menu:
            self.__initial_menu()
        elif self.mario.game_over:
            self.__end_screen(False)
        elif self.__game_won or self.__screens > 9:
            self.__end_screen(True)
        elif self.__screen_end:
            self.__screen_menu()
        else:
            pyxel.cls(c.Black)  # Set color black
            # draw stage
            for i in range(len(self.__stage)):
                pyxel.blt(*self.__stage[i].coord, *self.__stage[i].sprite)
                if isinstance(i, POW_block) and i.POW_active:
                    pyxel.cls(c.White)  # animation for POW
                    i.POW_active = True
            # draw enemies
            for i in range(len(self.__active_enemies)):
                pyxel.blt(*self.__active_enemies[i].coord, *self.__active_enemies[i].sprite)

                if self.__active_enemies[i].killed_coord:  # draw punctuation when killing enemy
                    pyxel.blt(*self.__active_enemies[i].killed_coord, *c.Spr_punt1)

                if isinstance(self.__active_enemies[i], Icepice) and self.__active_enemies[
                    i].frosting_coord:  # frosting plat animation
                    pyxel.blt(*self.__active_enemies[i].frosting_coord,
                              *c.Spr_frosting1 if self.__flip_flop else c.Spr_frosting2)
            # draw pipes
            for i in range(len(self.__pipes)):
                pyxel.blt(*self.__pipes[i].coord, *self.__pipes[i].sprite)
            # draw fireball again so the pipes do not oversize it
            for i in range(len(self.__active_enemies)):
                if isinstance(self.__active_enemies[i], Fire_ball):
                    pyxel.blt(*self.__active_enemies[i].coord, *self.__active_enemies[i].sprite)

            # Mario draw
            pyxel.blt(self.mario.coord[0] - 1, self.mario.coord[1], *self.mario.sprite)

            # interface draw
            self.__HUD_draw()

    def __init_variables(self):
        """set all the variables to be more readable the init method"""
        self.in_menu = True
        self.__game_won = False
        self.__stage = []
        self.__enemies = []
        self.__active_enemies = []
        self.__killed_enemies = 0
        self.__screens = 0
        self.__screen_end = True
        self.__time_per_screen = 0
        self.__spawn_counter = 0
        self.__spawn_counter_ice_spikes = 0
        self.__flip_flop = 0
        for i in range(len(c.music)):  # set the music
            pyxel.sound(i + c.snd_from_assets).set(*c.music[i])  # there are 3 snds already
        for i in range(len(c.sounds)):
            pyxel.sound(i + c.snd_from_assets + len(c.music)).set(*c.sounds[i])
        c.under_ice = {'c': False, 'l': False, 'r': False}  # reset the frost plats
        for block in (plat for plat in self.__stage if isinstance(plat, platform)):
            block.platform_frost = False

    def __reset_game(self):
        """reset all as the init to start again"""
        pyxel.stop(2)
        pyxel.stop(3)
        del self.mario
        del (self.highscore)
        self.__init_variables()
        self.mario = Mario()
        self.highscore = highscore()
        self.__generate_stage()
        self.__generate_pipes()
        self.__generate_enemies()

    def __next_level(self):
        """flags that change once the level has been cleared"""
        self.__active_enemies.clear()
        self.__screen_end = True
        self.__screens += 1
        self.__time_per_screen = 0
        self.__spawn_counter = 0
        self.__spawn_counter_ice_spikes = 0
        self.__killed_enemies = 0
        c.under_ice = {'c': False, 'l': False, 'r': False}
        for block in (plat for plat in self.__stage if isinstance(plat, platform)):
            block.platform_frost = False
        if self.mario.lives < 5:
            self.mario.lives += 1
        self.mario.coord = c.mario_position[:]  # reset mario coords

    def __generate_stage(self):
        """generates the stage's basic stuff"""
        self.__stage.append(POW_block(c.POW_position))
        for i in range(c.Width // c.L_M):  # generation of bricks
            self.__stage.append(brick([c.L_M * i, c.Height - c.L_M]))
        for i in range(c.Width // c.L_S):
            # generation of platforms
            for j in range(3):
                if i == c.Row_plat[j][0]:  # this is for corners fo plats
                    if j == 1:
                        self.__stage.append(platform([c.L_S * i, c.L_y_plat_init + j * c.L_y_plat], self.__screens, 2))
                    else:
                        self.__stage.append(platform([c.L_S * i, c.L_y_plat_init + j * c.L_y_plat], self.__screens, 1))
                elif i == c.Row_plat[j][1]:
                    if j == 1:
                        self.__stage.append(platform([c.L_S * i, c.L_y_plat_init + j * c.L_y_plat], self.__screens, 1))
                    else:
                        self.__stage.append(platform([c.L_S * i, c.L_y_plat_init + j * c.L_y_plat], self.__screens, 2))

                elif (
                        (j == 0 and (c.Row_plat[j][0] > i or c.Row_plat[j][1] < i)) or
                        (j == 1 and c.Row_plat[1][0] < i < c.Row_plat[1][1]) or
                        (j == 2 and (c.Row_plat[j][0] > i or c.Row_plat[j][1] < i))
                ):
                    # that if is for not generate a row full of plats
                    self.__stage.append(platform([c.L_S * i, c.L_y_plat_init + j * c.L_y_plat], self.__screens, 0))
            if i == c.Row_plat2[0]:
                self.__stage.append(platform([c.L_S * i, c.L_y_plat2], self.__screens, 1))
            elif i == c.Row_plat2[1]:
                self.__stage.append(platform([c.L_S * i, c.L_y_plat2], self.__screens, 2))
            elif c.Row_plat2[0] > i or c.Row_plat2[1] < i:
                self.__stage.append(platform([c.L_S * i, c.L_y_plat2], self.__screens, 0))

    def __generate_pipes(self):
        """unlike it is in the block mother class it is generated isolated, so it doesn't collide"""
        self.__pipes = [
            pipe([c.Pipe_right, c.Pipe_bot], c.Spr_pipe(0)),  # Bottom right
            pipe([c.Pipe_right, c.Pipe_top], c.Spr_pipe_corner2),
            pipe([c.Pipe_right, c.Pipe_top + c.L_M], c.Spr_pipe_corner1),
            pipe([c.Pipe_right - c.L_M, c.Pipe_top], c.Spr_pipe(0)),  # Top right
            pipe([c.Pipe_left, c.Pipe_bot], c.change_direction_spr(c.Spr_pipe(0))),  # Bottom left
            pipe([c.Pipe_left, c.Pipe_top], c.change_direction_spr(c.Spr_pipe_corner2)),
            pipe([c.Pipe_left, c.Pipe_top + c.L_M], c.change_direction_spr(c.Spr_pipe_corner1)),
            pipe([c.Pipe_left + c.L_M, c.Pipe_top], c.change_direction_spr(c.Spr_pipe(0)))
        ]

    def __generate_enemies(self):
        """generate all enemies from the list depending on difficulty"""
        self.__enemies = [
            [
                # LEVEL 1
                Turtle([c.Pipe_right, c.Pipe_top]), Coin([c.Pipe_right, c.Pipe_top], True),
                Turtle([c.Pipe_left, c.Pipe_top]), Turtle([c.Pipe_left, c.Pipe_top])
            ],
            [
                # LEVEL 2
                Turtle([c.Pipe_left, c.Pipe_top]), Turtle([c.Pipe_left, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True),
                Turtle([c.Pipe_right, c.Pipe_top]), Coin([c.Pipe_right, c.Pipe_top], True),
                Turtle([c.Pipe_left, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True), Turtle([c.Pipe_right, c.Pipe_top])
            ],
            [
                # LEVEL 3
                # coin stage
            ],
            [
                # LEVEL 4
                Crab([c.Pipe_right, c.Pipe_top]), Crab([c.Pipe_left, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True),
                Crab([c.Pipe_right, c.Pipe_top]), Coin([c.Pipe_right, c.Pipe_top], True),
                Crab([c.Pipe_left, c.Pipe_top])
            ],
            [
                # LEVEL 5
                Crab([c.Pipe_left, c.Pipe_top]), Crab([c.Pipe_right, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True),
                Coin([c.Pipe_right, c.Pipe_top], True), Turtle([c.Pipe_right, c.Pipe_top]),
                Crab([c.Pipe_left, c.Pipe_top]),
                Turtle([c.Pipe_right, c.Pipe_top])
            ],
            [
                Fly([c.Pipe_right, c.Pipe_top]), Fly([c.Pipe_left, c.Pipe_top]), Coin([c.Pipe_right, c.Pipe_top], True),
                Coin([c.Pipe_right, c.Pipe_top], True), Fly([c.Pipe_right, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True),
                Fly([c.Pipe_right, c.Pipe_top]),
            ],
            [
                # coin stage 2
            ],
            [
                Fly([c.Pipe_left, c.Pipe_top]), Fly([c.Pipe_right, c.Pipe_top]), Coin([c.Pipe_right, c.Pipe_top], True),
                Coin([c.Pipe_right, c.Pipe_top], True), Fly([c.Pipe_left, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True),
                Fly([c.Pipe_right, c.Pipe_top]), Turtle([c.Pipe_right, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True),
                Turtle([c.Pipe_right, c.Pipe_top])
            ],
            [
                Icepice([c.Pipe_right, c.Pipe_top]), Fly([c.Pipe_left, c.Pipe_top]), Turtle([c.Pipe_right, c.Pipe_top]),
                Icepice([c.Pipe_right, c.Pipe_top]), Turtle([c.Pipe_left, c.Pipe_top]),
                Icepice([c.Pipe_right, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True), Turtle([c.Pipe_right, c.Pipe_top])
            ],
            [
                Icepice([c.Pipe_right, c.Pipe_top]), Turtle([c.Pipe_right, c.Pipe_top]),
                Coin([c.Pipe_right, c.Pipe_top], True),
                Icepice([c.Pipe_right, c.Pipe_top]), Crab([c.Pipe_left, c.Pipe_top]), Crab([c.Pipe_right, c.Pipe_top]),
                Icepice([c.Pipe_right, c.Pipe_top]), Coin([c.Pipe_right, c.Pipe_top], True),
                Crab([c.Pipe_left, c.Pipe_top]),
                Icepice([c.Pipe_right, c.Pipe_top]), Crab([c.Pipe_right, c.Pipe_top]), Fly([c.Pipe_left, c.Pipe_top])
            ]
        ]
        for i in range(len(c.coin_stage_position)):  # append for coins in coins stage
            self.__enemies[2].append(Coin([*c.coin_stage_position[i]], False))
            self.__enemies[6].append(Coin([*c.coin_stage_position[i]], False))

    def __spawn_enemies(self):
        """this is for spawning enemies progressively depending on time"""
        self.__time_per_screen += 1
        if self.__screens == 2 or self.__screens == 6:  # coin stages
            if self.__killed_enemies + len(self.__active_enemies) != len(
                    self.__enemies[self.__screens]):  # spawn them all at once
                for coin in range(len(self.__enemies[self.__screens])):
                    self.__active_enemies.append(self.__enemies[self.__screens][coin])
            if self.__time_per_screen >= c.T_coin_stage:  # For end due to time and not to dead enemies
                self.__killed_enemies = len(self.__enemies[self.__screens])
        else:
            if self.__spawn_counter < len(
                    self.__enemies[self.__screens]) and self.__time_per_screen >= self.__spawn_counter * c.T_spawn_gen:
                # For general spawn
                self.__active_enemies.append(self.__enemies[self.__screens][self.__spawn_counter])
                self.__spawn_counter += 1
            elif (len(
                    self.__enemies[
                        self.__screens]) <= self.__spawn_counter < len(
                self.__enemies[
                    self.__screens]) + c.max_fireballs and self.__time_per_screen >= self.__spawn_counter * c.T_spawn_fireballs):
                # for spawn fireballs
                self.__active_enemies.append(
                    Fire_ball([c.fire_ball_x, random.choice(c.fire_ball_y)], random.randint(0, 1)))
                self.__spawn_counter += 1
            # generation of ice spikes in a different way than the rest
            if self.__screens >= len(
                    self.__enemies) - 2 and self.__time_per_screen >= self.__spawn_counter_ice_spikes * c.T_spawn_ice_spikes:
                self.__active_enemies.append(Ice_spikes(random.choice(c.ice_spikes_position_x)))
                self.__spawn_counter_ice_spikes += 1

    def __block_update(self):
        """Update all the blocks"""
        for block in self.__stage:  # update for blocks
            if isinstance(block, brick):  # Brick animation
                block.update_status(self.__flip_flop)
            if isinstance(block, platform):  # Platform change
                block.update_status(self.__screens)
            if isinstance(block, POW_block):  # POW functionality
                block.update_status(self.__flip_flop)
                if block.POW_state <= 0:
                    pyxel.pal()
                    self.__stage.remove(block)  # Remove POW once it is used maximally

    def __enemy_update(self):
        """update all the enemies & coins, as they are taken into account as enemies"""
        for enemy in self.__active_enemies:  # update for enemies
            enemy.update_status(self.__stage,
                                (other_enemy for other_enemy in self.__active_enemies if other_enemy != enemy and not
                                (isinstance(other_enemy, Icepice) or isinstance(other_enemy, Fire_ball) or isinstance(
                                    other_enemy, Ice_spikes))
                                 # Append all the list of enemies unless: itself, icepices, fire balls and Ice_spikes
                                 ))

            if enemy.sprite == c.Spr_blank and not isinstance(enemy, Ice_spikes):  # Remove enemy from list
                self.__active_enemies.remove(enemy)
                if not isinstance(enemy, Coin) or (isinstance(enemy, Coin) and enemy.collected_by_mario):
                    self.highscore.score += 500
                if not isinstance(enemy, Fire_ball):  # For end screen
                    self.__killed_enemies += 1

    def __initial_menu(self):
        """animation for the initial menu"""
        pyxel.cls(c.Black)
        for i in range(c.Width // c.L_S):
            for j in range(5):
                pyxel.blt(c.L_S * i, c.L_y_plat_init_h + j * c.L_y_plat, *c.Spr_plat1)  # Background plats

        pyxel.text(c.H_text[0][0], c.H_text[1][0], "[ press SPACE to start ]", c.White if self.__flip_flop else c.Gray)
        pyxel.tri(c.H_trgl_x[0], c.H_trgl_y[0] + self.__flip_flop * 5,
                  c.H_trgl_x[1], c.H_trgl_y[1] + self.__flip_flop * 5,
                  c.H_trgl_x[2], c.H_trgl_y[2] + self.__flip_flop * 5,
                  c.Orange if self.__flip_flop else c.Yellow)  # triangle
        pyxel.rect(*c.rectang_centered(c.H_rct_bck1), c.Purple)

        for i in range(3):  # generation of animated borders
            pyxel.rectb((c.Width - c.H_rct_bck1[0] + c.H_separ - i * c.H_separ) / 2,
                        (c.Height - c.H_rct_bck1[1] + c.H_separ - i * c.H_separ) / 2 + c.H_rct_bck1[2],
                        c.H_rct_bck1[0] - c.H_separ + i * c.H_separ,
                        c.H_rct_bck1[1] - c.H_separ + i * c.H_separ,
                        c.Red if self.__flip_flop else c.Blue3)

        pyxel.rect(*c.rectang_centered(c.H_rct_bck2), c.Red)  # generation of the title part
        pyxel.bltm(*c.Home_screen_coord, *(c.Spr_home_screen2 if self.__flip_flop else c.Spr_home_screen1))
        pyxel.text(c.H_text[0][1], c.H_text[1][1], "CREATED BY: Hector Molina & Nicolas Maire", c.White)
        pyxel.text(c.H_text[0][2], c.H_text[1][2], "- Uc3m Leganes -", c.White)
        pyxel.blt(*c.H_mario, *c.Spr_mario_being_still)

    def __screen_menu(self):
        """animation for the screen menu"""
        pyxel.pal()
        pyxel.cls(c.Blue4)

        pyxel.rectb(0, 0, c.Width, c.Height, c.Blue3)
        pyxel.rect(*c.rectang_centered(c.M_rct_bck1), c.Blue3)
        pyxel.rectb(*c.rectang_centered(c.M_rct_bck1), c.Blue1 if self.__flip_flop else c.Blue2)
        pyxel.rect(*c.rectang_centered(c.M_rct_bck2), c.Orange)
        pyxel.rectb(*c.rectang_centered(c.M_rct_bck2),
                    c.White if self.__flip_flop else c.Yellow)  # generation for the rectangles

        pyxel.bltm(*c.M_screen_coord, *c.Spr_home_screen1)  # rest of text
        pyxel.text(c.Width / 2 + c.M_text[0][0], c.Height / 2, "G E T   R E A D Y   F O R",
                   c.Yellow if self.__flip_flop else c.Orange)
        pyxel.text(c.Width / 2 + c.M_text[0][1], c.Height / 2 + c.M_text[1][0],
                   f"-- S T A G E  {self.__screens + 1} --", c.Yellow if self.__flip_flop else c.Orange)
        pyxel.text(c.Width / 2 + c.M_text[0][2], c.Height / 2 + c.M_text[1][1], "Press SPACE",
                   c.Beige if self.__flip_flop else c.Pink)
        pyxel.text(c.Width / 2 + c.M_text[0][3], c.Height + c.M_text[1][2], "CREATED BY: Hector Molina & Nicolas Maire",
                   c.Green1)

    def __end_screen(self, won_game: bool):
        """animation for the end menu"""
        if won_game:
            pyxel.cls(c.White)
            pyxel.text(*c.Text_Win, "-Y O U   W I N-", c.Blue4)
        else:
            pyxel.cls(c.Black)
            pyxel.text(*c.Text_Game_over, "G A M E   O V E R", c.Red)
        for i in range(4):
            pyxel.text(c.Text_Game_over[0], c.Text_Game_over[1] + (i + 1) * 20,
                       f"Highscore {i + 1}:{str(self.highscore.list[i]).zfill(6)}", c.Black if won_game else c.White)
        pyxel.text(c.Text_Game_over[0] - 3, c.Text_Game_over[1] + 100, "PRESS SPACE TO RESET", c.Orange)

    def __HUD_draw(self):
        """Interface draw"""

        def counter_procedure(score, x_pos):  # local function
            counter = 0
            if score < c.max_punctuation:
                score_draw = str(score).zfill(6)
            else:
                score_draw = str(c.max_punctuation)
            for i in score_draw:
                pyxel.blt(x_pos + c.L_S * counter, c.Height_interface, *c.Spr_score(int(i)))
                counter += 1

        # Score draw
        pyxel.text(*c.Text_Score, "MARIO:", c.White)
        counter_procedure(self.highscore.score, c.score_x)
        # Life counter draw
        pyxel.text(c.live_x, c.Height_interface + 2, "[L]:", c.White)
        for i in range(self.mario.lives):
            pyxel.blt(c.live_mario_head_x + c.L_S * i, c.Height_interface, *c.Spr_live)

        if self.mario.advice_comment:
            pyxel.text(c.Width / 2 + 15, 20, "<- press SPACE to fall", c.White)
        # Highscore draw
        pyxel.text(c.highsc_x, c.Height_interface + 2, "HIGHSCORE:", c.White)
        counter_procedure(self.highscore.list[0], c.highscore_x)
        if self.__screens == 2 or self.__screens == 6:
            pyxel.blt(c.Width / 2 - 12, 25, *c.Spr_time_counter)
            pyxel.text(c.Width / 2 - 8, 30, str(round((1200 - self.__time_per_screen) / 60, 1)), c.White)

    def __music(self):
        """Music setting"""
        if self.mario.game_over:
            if pyxel.play_pos(2) is None:
                pyxel.stop(2)
                pyxel.stop(3)
                pyxel.play(2, 0)
        elif pyxel.play_pos(2) is None and pyxel.play_pos(2) is None:
            pyxel.play(2, [c.snd_from_assets, c.snd_from_assets + 1], loop=True)
            pyxel.play(3, [c.snd_from_assets + 2, c.snd_from_assets + 3], loop=True)


Game()
