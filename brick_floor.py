import Constants as c
from Block import block


class brick(block):
    def __init__(self, coord: list) -> None:
        super().__init__(coord, c.Spr_brick1, [16,16])

    def update_status(self, number):
        """Basically animation of the brick for shining"""
        if number == 0:
            self.sprite = c.Spr_brick1
        else:
            self.sprite = c.Spr_brick2
