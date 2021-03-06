from occupiedRegion import OccuppiedRegion
from window import PassageWay, Room


class RenderMap:
    '''Contains windows to be rendered'''

    def __init__(self, screen):
        self.screen = screen
        self._rooms = []
        self._passageways = []
        self._room_positions = []
        self._passageway_positions = []

    def _window_is_not_overlapping(self, candidate_room: Room) -> bool:
        ''' Checks whether a room is overlapping with other already genrated rooms
        :param candidate_room: room to check if it overlaps with any other room already made
        :returns: boolean on whether it overlaps or not
        '''
        candidate_region = OccuppiedRegion(candidate_room)

        for window_position in self._room_positions:
            if(candidate_region.min_x in range(window_position.min_x, window_position.max_x + 1)):
                if(candidate_region.min_y in range(window_position.min_y, window_position.min_y + 1)):
                    return False
                elif(candidate_region.max_y in range(window_position.min_y, window_position.max_y + 1)):
                    return False
            elif (candidate_region.max_x in range(window_position.min_x, window_position.max_x + 1)):
                if(candidate_region.min_y in range(window_position.min_y, window_position.min_y + 1)):
                    return False
                elif(candidate_region.max_y in range(window_position.min_y, window_position.max_y + 1)):
                    return False
        return True

    def add_room(self, room: Room) -> bool:
        '''Adding a new window to the windows list'''
        if self._window_is_not_overlapping(room):
            self._rooms.append(room)
            self._room_positions.append(OccuppiedRegion(room))
            return True
        return False

    def add_passageWay(self, passage: PassageWay) -> bool:
        '''Adding a new passage way to the passageway list to be rendered'''
        self._passageways.append(passage)
        self._passageway_positions.append(OccuppiedRegion(passage))
        return True

    def replace_room(self, room: Room = None):
        '''Update or remove a room in the rooms list'''
        self._rooms.pop(self._rooms.index(room))
        self._room_positions.pop(self._windows_positions.index(
            list(filter(lambda x: room.name is x.name, self._room_positions))))
        if room is not None:
            self._rooms.append(room)
            self._room_positions.append(OccuppiedRegion(room))

    def replace_passageway(self, passageway: PassageWay = None):
        '''Update or remove a passageway in the passageways list'''
        self._passageways.pop(self._passageways.index(passageway))
        self._passageway_positions.pop(self._windows_positions.index(
            list(filter(lambda x: passageway.name is x.name, self._passageway_positions))))
        if passageway is not None:
            self._passageways.append(passageway)
            self._passageway_positions.append(OccuppiedRegion(passageway))

    def render(self):
        '''Render screen function'''
        self.screen.erase()
        self.screen.refresh()
        # data = ''
        for window in self._rooms:
            window.layout.refresh()
        for passageway in self._passageways:
            passageway.layout.refresh()

    @property
    def rooms(self) -> list:
        return self._rooms

    @property
    def passageways(self) -> list:
        return self._passageways
