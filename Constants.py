# --------------------GAME START--------------------
Width: int = 256
Height = 223
Fps = 60
Assets_path = "sprites.pyxres"
Highscores_path = "highscores.txt"

# ----------------------Global Variables-------------------------------
under_ice = {'c': False, 'l': False, 'r': False}

# ----------------------HIT BOXES and other properties-------------------------------
mario_hitbox = [14, 21]
turtle_hitbox = [16, 16]
crab_hitbox = [16, 16]
fly_hitbox = [16, 16]
icepice_hitbox = [16, 16]
coin_hitbox = [8, 10]
fire_ball_hitbox = [8, 8]
collision_tolerance = 1.5
collision_range = 10
Pow_usages = 3
fire_ball_x = 0
fire_ball_y = (40, 86, 136, 180)
max_fireballs = 4
# ----------------------------Lengths & Positions-----------------------------
# normal sizes
L_S = 8
L_M = 16
L_L = 32
Height_interface = 6
interface_x = 16
Pipe_top = 32
Pipe_bot = Height - 32
Pipe_left = 0
Pipe_right = Width - 16
mario_position = [48, Height - L_M - mario_hitbox[1]]
POW_position = [120, 160]

# platforms
L_y_plat = 48
L_y_plat_init = 64
L_y_plat_init_h = 12
L_y_plat2 = 120
interval_plat_row2 = 7
Row_plat = (
    [13, Width // L_S - 14], [interval_plat_row2, Width // L_S - interval_plat_row2 - 1], [10, Width // L_S - 11])
Row_plat2 = [3, Width // L_S - 4]
ice_spikes_position_y = L_y_plat_init + L_S
ice_spikes_position_x = [3 * L_S, 7 * L_S, 11 * L_S, Width - (12 * L_S), Width - (4 * L_S), Width - (8 * L_S)]
# icepice positions
center_of_plat = ((Width / 2), ((0 + 10 * L_S) / 2), ((((Width // L_S) - 9) * L_S + Width) / 2))
coin_stage_position = (
    (36, Pipe_top), ((Width - 35 - L_M), Pipe_top),
    (20, (L_y_plat_init + L_S + 7)), ((Width - 20 - L_M), (L_y_plat_init + L_S + 7)),
    ((42 + 4), (L_y_plat_init + L_S + 7)), ((Width - 42 - 3 - L_M), (L_y_plat_init + L_S + 7)),
    (80, (L_y_plat_init + L_y_plat + L_S + 7)), ((Width - 79 - L_M), (L_y_plat_init + L_y_plat + L_S + 7)),
    ((32 + 4), (L_y_plat_init + 2 * L_y_plat + L_S + 4)), ((Width - 32 - 3 - L_M), (L_y_plat_init + 2 * L_y_plat + L_S + 4))
)


def ice_plat_x(number):
    return [(center_of_plat[number] - 2 * L_S), center_of_plat[number] + 2 * L_S]


ice_central_plat_y = L_y_plat_init + L_y_plat
ice_bot_plat_y = L_y_plat_init + 2 * L_y_plat
# sizes texts
Text_Game_over = [Width / 2 - 35, Height / 2 - 20]
Text_Win = [Width / 2 - 30, Height / 2 - 20]
Text_Score = [interface_x, Height_interface + 2]
score_x = interface_x + 24
live_x = interface_x + 76
live_mario_head_x = interface_x + 92
highsc_x = interface_x + 146
highscore_x = interface_x + 185


# sizes rectangles
def rectang_centered(rect: list):
    return (Width / 2) - rect[0] / 2, (Height / 2) - rect[1] / 2 + rect[2], rect[0], rect[1]


# homecreen
Home_screen_coord = Width / 2 - 80, Height / 2 - 50
H_rct_bck1 = (195, 95, -20)
H_rct_bck2 = (180, 80, -20)
H_separ = 6  # Separation from borders
H_trgl_x = (Width / 2 - 16, Width / 2 + 15, Width / 2)
H_trgl_y = (195, 195, 205)

H_text = (((Width / 2) - 47, (Width / 2) - 82, (Width / 2) - 30), (185, Height / 2, Height / 2 + 10))
H_mario = [12, 183]

# screen menu
M_screen_coord = Width / 2 - 80, Height / 2 - 80
M_rct_bck1 = (215, 145, -30)
M_rct_bck2 = (195, 75, -60)
M_text = ((-50, -34, -18, -82), (20, 50, -10))

extra_distance_side_change = -5


# ----------------------------COLORS-----------------------------
# from typing import List

Black = 0
Blue4 = 1  # the higher the number after the color the darker it is
Purple = 2
Green2 = 3
Brown = 4
Blue3 = 5
Blue1 = 6
White = 7
Red = 8
Orange = 9
Yellow = 10
Green1 = 11
Blue2 = 12
Gray = 13
Pink = 14
Beige = 15
Colkey = 0  # transparent color
# ----------------------------music & sounds-----------------------------
snd_from_assets: int = 3
music: tuple = (("e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
                 "p",
                 "3",
                 "vffn fnff vffs vfnn",
                 25,),
                ("r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
                 "s",
                 "3",
                 "nnff vfff vvvv vfff svff vfff vvvv svnn",
                 25,),
                ("c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1" "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
                 "t",
                 "3",
                 "n",
                 25,),
                ("f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1" "f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
                 "t",
                 "3",
                 "n",
                 25,),
                ("f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "4411 4411 4411 4311", "f", 25,))

sounds = (
    ("D0 A0 G0", "t", "7", "f", 17,),  # snd_walk
    ("c3 d2", "t", "7", "n", 30,),  # snd_coin
    ("C4 G2 C2", "n", "4", "f", 40,),  # snd_enemy_dying
    ("C4 E4 G3 c2 g1", "n", "7", "v", 20,),  # snd_POW_block
    ("C1 E2 G2", "p", "7", "s", 20,),  # snd_jump
    ("a4 d3 c4 g2", "n", "5", "v", 20,),  # snd_frost_plat
    ("C1 E2 G2 E2 C2 c0", "p", "4", "s", 7,)  # snd_plat
)
# ---------------------------PHYSICS------------------------------
V_gravity = 0.25
V_gravity_fly = 0.05
V_jump = 5
V_jump_fly = 1.5
V_friction = 0.15
V_friction_ice = 0.05
V_walk = 0.2
V_player_max_x = 1.75
V_player_max_y = 2
V_fly = 0.4
V_turtle = 0.65
V_crab = 0.75
V_icepice = 0.80
V_angry_turtle = V_turtle + 0.25
V_coins = 1
Punct_mov = 22
# Harmonic wave speed equation
Amplitude = 0.2
Angular_speed = 0.5 * 2 * 3.14
# kx = 0
# ----------------------------Time-----------------------------
T_vulnerable_off = T_vulneable_off = 250  # It is typed wrong in the code
T_vulnerable_off_extra = 25
T_H_flipflop = 20
T_coin_stage = 1200
T_spawn_gen = 180
T_spawn_fireballs = 360
T_spawn_ice_spikes = 150
T_mar_die1 = 0.35*60
T_mar_die2 = 120
T_mar_die3 = 3*60
T_frost_platform = 90

# ----------------------PUNCTUATION------------------------------
max_punctuation = 999999
"""-------------------------SPRITES-----------------------------"""
# spr means sprite
# It will be a list for the sprites who change

Spr_blank = [0, 0, 0, 8, 8, 0]

# MARIO
Spr_mario_being_still: list[int] = [0, 0, 11, 16, 21, Colkey]
Spr_mario_jumping = [0, 96, 8, 16, 24, Colkey]
Spr_mario_braking1 = [0, 112, 11, 16, 23, Colkey]
Spr_mario_braking2 = [0, 122, 8, 16, 23, Colkey]


def Spr_mario_running(number: int):  # function to short constants
    """The sprite depending on a variable
       from 0 to 4"""
    sprite: list[int] = [0, 16 + 16 * number, 11, 16, 21, Colkey]
    return sprite


def Spr_mario_dyeing(number: int):
    """The sprite depending on a variable
       from 9 to 13"""
    sprite: list[int] = [0, 144 + 16 * number, 8, 16, 24, Colkey]
    return sprite


# Turtle
def Spr_turtle(number: int, color: int):
    """The sprite of the ice spike depending on a variable
    For 0-2: turtle walking
    For 3-7: turtle upside down animation
    For 8: dying
    For 9-10: turning around"""
    sprite: list[int] = [2 * color, 16 * number, 32, 16, 16, Colkey]
    return sprite


# Crabs
def Spr_crab(number: int, color: int):
    """The sprite of the ice spike depending on a variable
    For 0-3: crab walking
    For 4-5: crab upside down animation
    For 6-9: crab angry walking
    For 10-11: crab turning around"""
    sprite: list[int] = [color, 16 * number, 48, 16, 16, Colkey]
    return sprite


# Flies
def Spr_fly(number: int, color: int):
    """The sprite of the ice spike depending on a variable
    For 0-3: fly walking
    For 4-5: fly upside down animation
    For 6-7: fly_turning_around"""
    sprite: list[int] = [color, 16 * number, 64, 16, 16, Colkey]
    return sprite


# Fireballs
def Spr_fireball(number: int, color: int):
    """The sprite of the ice spike depending on a variable
    For 0-4 moving
    For 4-8 dyeing fireball
    Color: 0: red, 1: green"""
    sprite: list[int] = [0, 8 * number + 72 * color, 80, 8, 8, Colkey]
    return sprite


# Icepìces
def Spr_icepice(number: int):
    """The sprite of the ice spike depending on a variable
    For 0-5: charging ones
    For 6-7: death animation"""
    sprite: list[int] = [0, 16 * number, 152, 16, 16, Colkey]
    return sprite


Spr_frosting1 = [0, 128, 152, 16, 8, Colkey]
Spr_frosting2 = [0, 128, 160, 16, 8, Colkey]


# Ice spike
def Spr_ice_spike(number: int):
    """The sprite of the ice spike depending on a variable
    For 0-5 :animation"""
    sprite: list[int] = [0, 144 + 16 * number, 152, 16, 16, Colkey]
    return sprite


# Splash out
def Spr_splash_out(number: int):  # 0-5
    """The sprite of the splash depending on a variable
    goes linearly"""
    sprite: list[int] = [0, 16 * number, 168, 16, 16, Colkey]
    return sprite


"""BLOCKS"""

Spr_brick1 = [0, 48, 104, 16, 16, Colkey]
Spr_brick2 = [0, 64, 104, 16, 16, Colkey]


# POW
def Spr_POW(number: int, color: int):  # 0-2
    """The sprite of the Pow block depending on a variable"""
    sprite: list[int] = [0, 16 * number, 104 + color * 16, 16, 16, Colkey]
    return sprite


# Plat1
Spr_plat1 = [0, 56, 144, 8, 8, Colkey]

# Plat2
Spr_plat2 = [0, 72, 144, 8, 8, Colkey]
Spr_plat2R = [0, 80, 144, 8, 8, Colkey]
Spr_plat2L = [0, 64, 144, 8, 8, Colkey]

# Plat 3
Spr_plat3 = [0, 104, 144, 8, 8, Colkey]
Spr_plat3R = [0, 112, 144, 8, 8, Colkey]
Spr_plat3L = [0, 96, 144, 8, 8, Colkey]

# Plat4
Spr_plat4 = [0, 144, 144, 8, 8, Colkey]
pr_plat4_up1R = [0, 144, 125, 8, 10, Colkey]

# plat 5
Spr_plat5 = [0, 48, 144, 8, 8, Colkey]

# Ice plat
Spr_plat_ice = [0, 128, 144, 8, 8, Colkey]
Spr_plat_iceR = [0, 136, 144, 8, 8, Colkey]
Spr_plat_iceL = [0, 120, 144, 8, 8, Colkey]


def Spr_platform_up(type: int, position: int, step: int):
    """The sprite depending on a variable
       Type:
           0-4 type of platform
       Position:
           0 left
           1 centre
           2 right
       Step:
           0 low up
           1 high up"""
    sprite: list[int] = [0, (8 * type) + (40 * position), 205 + 16 * step, 8, 12, Colkey]
    return sprite


"""END BLOCKS"""


# Pipes
def Spr_pipe(number: int):
    """The sprite of the ice spike depending on a variable
    For 0-3: Pipe animation"""
    sprite: list[int] = [0, 128 + 8 * number, 104, 16,
                         16]  # it doesnt has colkey because the enemy would be back from it
    return sprite


Spr_pipe_corner1 = [0, 80, 104, 16, 16, Colkey]
Spr_pipe_corner2 = [0, 112, 104, 16, 16]

Spr_pipe_straight: list[int] = [0, 96, 104, 16, 16, Colkey]

# Punctuation
Spr_live = [0, 8, 0, 8, 8, Colkey]
Spr_punt1 = [0, 16, 0, 16, 8, Colkey]


def Spr_score(number: int):
    """The sprite of the coin depending on a variable
    0-9: for every number"""
    sprite: list[int] = [0, 96 + 8 * number, 0, 8, 8, Colkey]
    return sprite
Spr_time_counter = [0, 0, 184, 24, 16, Colkey]

# Coins
def Spr_coin(number: int):  # until 10
    """The sprite of the coin depending on a variable
    0-5: Coin moving, 2 has to be repeated twice
    rest for animation for obtaining it"""
    sprite: list[int] = [0, 16 * number, 93, 16, 10, Colkey]
    return sprite


# Home Screen
Spr_home_screen1 = [1, 0, 0, 20 * 8, 5 * 8, Colkey]
Spr_home_screen2 = [1, 0, 40, 20 * 8, 5 * 8, Colkey]


def change_direction_spr(list: list):
    """this change the direction of the sprites"""
    sprite = list.copy()
    sprite[3] = -sprite[3]
    return sprite
