import Constants
from Block import block
class pipe(block):
    def __init__(self, coord: list, sprite) -> None:
        super().__init__(coord, sprite, Constants.turtle_hitbox)