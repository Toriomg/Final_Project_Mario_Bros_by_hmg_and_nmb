class block:
    """It is just properties and setter"""
    def __init__(self, coord: list, sprite: list, hitbox) -> None:
        """coord is a list of 2 values: x and y
        the size of the class is to measure the collisions"""
        self.__coord = coord
        self.__coord_initials = self.__coord.copy()
        self.__sprite = sprite
        self.__hitbox = hitbox
        self.__exist = True

    @property
    def coord(self) -> list:
        return self.__coord

    @coord.setter
    def coord(self, new_coord: list):
        if type(new_coord) != list:
            raise ValueError("sprite must be a list")
        elif len(new_coord) != 2:
            raise ValueError("list must have  elements")
        else:
            self.__coord = new_coord
    @property
    def sprite(self) -> list:
        return self.__sprite

    @sprite.setter
    def sprite(self, new_sprite: list):
        if type(new_sprite) != (list or tuple):
            raise ValueError("sprite must be a tuple or list")
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
