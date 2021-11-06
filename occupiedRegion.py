from window import Room, Window


class OccuppiedRegion:
    def __init__(self, window: Window):
        self._name = window.name
        self._min_y = window.pos_y
        self._min_x = window.pos_x
        self._max_y = window.pos_y + window.height
        self._max_x = window.pos_x + window.width

    @property
    def name(self) -> str:
        return self.name

    @property
    def min_y(self) -> int:
        return self._min_y

    @property
    def min_x(self) -> int:
        return self._min_x

    @property
    def max_y(self) -> int:
        return self._max_y

    @property
    def max_x(self) -> int:
        return self._max_x
