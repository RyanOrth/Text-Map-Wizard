

class SpecialEdgeCharacter:
    def __init__(self, name: str, pos_y: int, pos_x: int, character: str):
        self._name = name
        self._pos_y = pos_y
        self._pos_x = pos_x
        self._character = character

    @property
    def name(self) -> str:
        return self._name

    @property
    def pos_y(self) -> int:
        return self._pos_y

    @property
    def pos_x(self) -> int:
        return self._pos_x

    @property
    def character(self) -> str:
        return self._character
