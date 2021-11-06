from window import Room, Window
from specialCharacters import SpecialEdgeCharacter
import random
from constants import MIN_ROOM_SIZE, MAX_ROOM_SIZE

class GenerateMap:
    def __init__(self, map_height: int, map_width: int, screen: Window):
        self._map_height = map_height
        self._map_width = map_width
        self._screen = screen
        
        return self._generate_map()

    def _generate_map(self):
        return self._generate_room(1)

    def _generate_room(self, index: int):
        height = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        width = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        pos_y = random.randrange(0, self._screen.getmaxyx()[0])
        pos_x = random.randrange(0, self._screen.getmaxyx()[1])
        return Room(f'room{index}', height, width, pos_y, pos_x, self._generate_doors())

    def _generate_doors(self, room: Room):
        doors = []
        num_doors_options = list(range(1, 5))
        num_doors = random.choices(
            num_doors_options, weights=(60, 80, 20, 10), k=4)

        for i in range(0, num_doors):
            pos_y, pos_x = self._generate_random_door_position(room)
            doors.append(SpecialEdgeCharacter(f'door{i}', pos_y, pos_x, '+'))
        
        return doors

    def _generate_random_door_position(self, room: Room):
        pos_x = random.randrange(0, room.width)
        pos_y = None
        if(pos_x == 0 or pos_x == room.width):
            pos_y = random.randrange(0, room.height)
        else:
            pos_y = random.choice([0, room.height])
        return (pos_y, pos_x)
