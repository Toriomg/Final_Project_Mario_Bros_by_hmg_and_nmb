import pyxel
import Constants as c
from Enemy import Enemy


class Coin(Enemy):
    def __init__(self, coord: list, coin_moves: bool) -> None:
        super().__init__(
            coord=coord, sprite=c.Spr_coin(0), hitbox=c.coin_hitbox)
        self.__coin_moves = coin_moves
        self.v[0] = 0
        self.__number = 0
        self.__collect_coin_animation_number = 0
        self.__collected_by_mario = False

    @property
    def collected_by_mario(self):
        return self.__collected_by_mario

    @collected_by_mario.setter
    def collected_by_mario(self, value):
        if not isinstance(value, bool):
            raise ValueError("vulnerable must be a boolean")
        self.__collected_by_mario = value

    @property
    def collect_coin_animation_number(self):
        return self.__collect_coin_animation_number

    @collect_coin_animation_number.setter
    def collect_coin_animation_number(self, value):
        # You can add validation or custom logic here if needed
        self.__collect_coin_animation_number = value

    def update_status(self, blocks: list, enemies: list):
        """Update the coin"""
        self.position()
        if self.alive:
            if self.__coin_moves:
                self.gravity()
                self.__coins_movement()
                self.colliding_blocks(blocks)
                self.return_to_pipes()
                self.__coin_colliding_enemies(enemies)
                self.side_change()
        self.__coin_animation()

    def __coins_movement(self):
        """move coins"""
        if self.alive:
            if self.looking_R:
                self.v[0] = c.V_coins
            else:
                self.v[0] = -c.V_coins

    def __coin_colliding_enemies(self, enemies: list):
        """collision with more entities"""
        for i in enemies:
            if (self.collision(i, False)
                    and not (self.coord[0] >= c.Width - 16 or self.coord[0] <= 16)
                    and not i.vulnerable):
                if not isinstance(i, Coin):
                    self.alive = False
                    self.sprite = c.Spr_blank
                else:
                    if self.__looking_R:
                        self.__looking_R = False
                        self.coord[0] = self.coord[0] - self.__hitbox[0]
                    else:
                        self.__looking_R = True

    def __coin_animation(self):
        if self.alive:
            if pyxel.frame_count % 8 == 0:
                if self.looking_R:
                    self.sprite = c.Spr_coin(self.__number)
                else:
                    self.sprite = c.change_direction_spr(c.Spr_coin(self.__number))
                self.__number += 1
            if self.__number > 5:
                self.__number = 0
        else:
            if self.__collected_by_mario:
                self.v[0] = 0
                self.v[1] = -0.3
                if pyxel.frame_count % 9 == 0:
                    self.sprite = c.Spr_coin(self.__collect_coin_animation_number)
                    self.__collect_coin_animation_number += 1
                if self.__collect_coin_animation_number > 11:
                    pyxel.stop(1)
                    pyxel.play(1, c.snd_from_assets + len(c.music) + 1)
                    self.sprite = c.Spr_blank
