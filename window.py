import curses


class Window:

    def __init__(self, name: str, layout: curses.window, special_edge_characters=None) -> None:
        self._name = name
        self._layout = layout

        if special_edge_characters is not None:
            for special_edge_character in special_edge_characters:
                layout.addstr(special_edge_character.pos_y,
                              special_edge_character.pos_x, special_edge_character.character)
            self._special_edge_characters = special_edge_characters
        else:
            self._special_edges_characters = None

        return None

    @property
    def name(self) -> str:
        return self._name

    @property
    def layout(self) -> curses.window:
        return self._layout

    @property
    def special_edges(self):
        return self._special_edge_characters


class Room(Window):
    def __init__(self, name: str = None, width: int = 5, height: int = 5,
                 pos_y: int = 0, pos_x: int = 0, open_sides: list = []) -> None:
        self._width = width
        self._height = height
        self._pos_x = pos_x
        self._pos_y = pos_y
        layout = curses.newwin(height, width + 1, pos_y, pos_x)
        for i in range(0, height-1):
            for j in range(0, width):
                layout.addstr(i, j, '*')
        layout.box()
        if open_sides is not None:
            for special_edge_character in open_sides:
                layout.addstr(special_edge_character.pos_y,
                              special_edge_character.pos_x, special_edge_character.character)
        super().__init__(name, layout)

    @property
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width


class PassageWay(Window):
    def __init__(self, name: str, layout: curses.window) -> None:
        super().__init__(name, layout)
