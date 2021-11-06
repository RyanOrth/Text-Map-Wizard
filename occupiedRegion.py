from window import Room


class OccuppiedRegion:
    def __init__(self, window: Room):
        self._name = window.name
        self._min_y = window.pos_y
        self._min_x = window.pos_x
        self._max_y = window.pos_y + window.height
        self._max_x = window.pos_x + window.width

    @property
    def name(self):
        return self.name

    @property
    def min_y(self):
        return self._min_y

    @property
    def min_x(self):
        return self._min_x

    @property
    def max_y(self):
        return self._max_y

    @property
    def max_x(self):
        return self._max_x
