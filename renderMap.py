from occupiedRegion import OccuppiedRegion
from window import Room


class RenderMap:
    '''Contains windows to be rendered'''

    def __init__(self, screen):
        self.screen = screen
        self._windows = []
        self._window_positions = []

    def _window_is_not_overlapping(self, candidate_window: Room):
        candidate_region = OccuppiedRegion(candidate_window)

        for window_position in self._window_positions:
            if(window_position.min_x <= candidate_region.min_x
               <= window_position.max_x):
                if(window_position.min_y <= candidate_region.min_y
                   <= window_position.max_y):
                    return False
                elif(window_position.min_y <= candidate_region.max_y
                     <= window_position.max_y):
                    return False
            elif (window_position.min_x <= candidate_region.max_x
                  <= window_position.max_x):
                if(window_position.min_y <= candidate_region.min_y
                   <= window_position.max_y):
                    return False
                elif(window_position.min_y <= candidate_region.max_y
                     <= window_position.max_y):
                    return False
        return True

    def add_window(self, window: Room):
        '''Adding a new window to the windows list'''
        if self._window_is_not_overlapping(window):
            self._windows.append(window)
            self._window_positions.append(OccuppiedRegion(window))
            return True
        return False

    def replace_window(self, window: Room):
        '''Update or remove a window in the windows list'''
        self._windows.pop(self._windows.index(window))
        self._window_positions.pop(self._windows_positions.index(
            list(filter(lambda x: window.name is x.name, self._window_positions))))
        if window is not None:
            self._windows.append(window)
            self._window_positions.append(OccuppiedRegion(window))

    def render(self):
        '''Render screen function'''
        self.screen.erase()
        self.screen.refresh()
        # data = ''
        for window in self._windows:
            window.layout.refresh()

    @property
    def windows(self) -> list:
        return self._windows
