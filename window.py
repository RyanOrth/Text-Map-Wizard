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
        '''Name identifier of the window'''
        return self._name

    @property
    def layout(self) -> curses.window:
        '''Window itself'''
        return self._layout

    @property
    def special_edges(self):
        '''The special cases of the the window'''
        return self._special_edge_characters


class Room(Window):
    '''
        A part or division of a building enclosed by walls, floor, and ceiling. -
        Definition from Oxford Languages
    '''

    def __init__(self, name: str = None, height: int = 5, width: int = 5,
                 pos_y: int = 0, pos_x: int = 0, special_edge_characters: list = None) -> None:
        self._width = width
        self._height = height
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._special_edge_characters = special_edge_characters
        
        layout = curses.newwin(height, width + 1, pos_y, pos_x)
        for i in range(0, height-1):
            for j in range(0, width):
                layout.addstr(i, j, '.')
        layout.box()
        if special_edge_characters is not None:
            for special_edge_character in special_edge_characters:
                layout.addstr(special_edge_character.pos_y,
                              special_edge_character.pos_x, special_edge_character.character)
        super().__init__(name, layout)

    @property
    def pos_x(self):
        ''' X position of upper left corner of the room'''
        return self._pos_x

    @property
    def pos_y(self):
        ''' Y position of upper left corner of the room'''
        return self._pos_y

    @property
    def height(self):
        ''' height of the room'''
        return self._height

    @property
    def width(self):
        '''width of the room'''
        return self._width

    @property
    def special_edge_characters(self):
        '''list of special edge characters'''
        return self._special_edge_characters


class PassageWay(Window):
    '''
        A hallway or room intended to connect other rooms and/or passageways to 
        reach a destination. \n
        Extends Window
    '''

    def __init__(self, name: str = None, height: int = 5, width: int = 5,
                 pos_y: int = 0, pos_x: int = 0) -> None:
        self._pos_y = pos_y
        self._pos_x = pos_x
        self._width = width
        self._height = height
        layout = curses.newwin(height, width + 1, pos_y, pos_x)
        for i in range(0, height-1):
            for j in range(0, width):
                layout.addstr(i, j, '.')
        if width >= height:
            layout.border(32, 32, curses.ACS_HLINE, curses.ACS_HLINE,
                          curses.ACS_LLCORNER, curses.ACS_LRCORNER,
                          curses.ACS_ULCORNER, curses.ACS_URCORNER)
        else:
            layout.border(curses.ACS_VLINE, curses.ACS_VLINE, 32, 32,
                          curses.ACS_ULCORNER, curses.ACS_URCORNER,
                          curses.ACS_LLCORNER, curses.ACS_LRCORNER)
        super().__init__(name, layout)

    @property
    def pos_y(self) -> int:
        ''' Y position of upper left corner of the passageway'''
        return self._pos_y

    @property
    def pos_x(self) -> int:
        ''' X position of upper left corner of the passageway'''
        return self._pos_x

    @property
    def width(self) -> int:
        ''' width of passageway'''
        return self._width

    @property
    def height(self) -> int:
        ''' height of passageway'''
        return self._height
