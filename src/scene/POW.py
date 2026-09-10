"""
@author: Héctor Molina Garde & Nicolás Maire Bravo
Mario Bros Arcade
"""
from Block import block
import Constants as c
import pyxel

class POW_block(block):
    def __init__(self, coord: list) -> None:
        super().__init__(coord, c.Spr_POW(0, 0), [16,16])#same hitbox as a turtle
        self.POW_state = 3
        self.POW_active = False
        self.__number = 0

    def hit_Pow(self, enemies: list):
        """The POW is hit and it makes all enemies vulnerable"""
        for i in enemies:
            i.vulnerable = True
            i.animation_time = pyxel.frame_count
            i.get_animation_time(i.animation_time)
            pyxel.stop(1)
            pyxel.play(1, c.snd_from_assets + len(c.music) + 3)
        self.POW_state -= 1
        self.POW_active = True


    def update_status(self, number):
        """Update the pow state"""
        if self.POW_state == 3:
            self.sprite = c.Spr_POW(0, number)
            self.hitbox[1] = 16
        elif self.POW_state == 2:
            self.sprite = c.Spr_POW(1, number)
            self.hitbox[1] = 13#size of sprites
        elif self.POW_state == 1:
            self.sprite = c.Spr_POW(2, number)
            self.hitbox[1] = 9#size of sprites
        if self.POW_active:
            for i in range(16):
                if i != 15:
                    pyxel.pal(i + 1, i)
                else:
                    pyxel.pal(0, i)
            self.POW_active = False
        else:
            pyxel.pal()
