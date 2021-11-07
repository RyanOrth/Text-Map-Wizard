from window import PassageWay, Room, Window
from specialCharacters import SpecialEdgeCharacter
import random
from constants import MIN_ROOM_SIZE, MAX_ROOM_SIZE
from occupiedRegion import OccuppiedRegion

class GenerateMap:
    def __init__(self, map_height: int, map_width: int):
        self._map_height = map_height
        self._map_width = map_width
        self._map = []
        self._paths = []
        self._occupied_regions = []
        self._special_characters = []
        self._max_room_index = None

    @property
    def paths(self):
        return self._paths

    def generate_map(self):
        for i in range(1, random.randrange(30, 40)):
            room = self._generate_room(i)
            if(self._window_is_not_overlapping(room)):
                self._map.append(room)
                self._occupied_regions.append(OccuppiedRegion(room))
            self._max_room_index = i
        self._connect_passageways()
        return self._map

    def _window_is_not_overlapping(self, candidate_window: Room) -> bool:
        candidate_region = OccuppiedRegion(candidate_window)

        for occupied_region in self._occupied_regions:
            if(candidate_region.min_x in range(occupied_region.min_x, occupied_region.max_x + 1)):
                if(candidate_region.min_y in range(occupied_region.min_y, occupied_region.min_y + 1)):
                    return False
                elif(candidate_region.max_y in range(occupied_region.min_y, occupied_region.max_y + 1)):
                    return False
            elif (candidate_region.max_x in range(occupied_region.min_x, occupied_region.max_x + 1)):
                if(candidate_region.min_y in range(occupied_region.min_y, occupied_region.min_y + 1)):
                    return False
                elif(candidate_region.max_y in range(occupied_region.min_y, occupied_region.max_y + 1)):
                    return False
        return True

    def _connect_passageways(self):
        # for i in range(0, self._max_room_index):
        #     room = list(filter(lambda x: f'room{i}' is x.name, rooms))
        #     room2 = list(filter(lambda x: room.specialpos_x is x.pos_x, rooms))
        #     for special_edge_chracter in room.special_edge_characters:
        #         # special_edge_character_1 = self._special_characters.get(f'room{i}-door{i}')
        #         pass
        # for room in rooms:
        #     for special_edge_character in room.special_edge_characters:
        #         list(filter(lambda x: special_edge_character.pos_x is x.name, self._special_characters))))
        for i in range(0, len(self._special_characters)):
            for j in range (i + 1, len(self._special_characters)):
                start_coords = (self._special_characters[i].pos_y, self._special_characters[i].pos_x)
                end_coords = (self._special_characters[j].pos_y, self._special_characters[j].pos_x)
                if(start_coords[0] == end_coords[0] or start_coords[1] == end_coords[1]):
                    passageway_pos_y = start_coords[0]
                    passageway_pos_x = start_coords[1]
                    if(end_coords[0] < start_coords[0] or end_coords[1] < start_coords[1]):
                        passageway_pos_y = end_coords[0]
                        passageway_pos_x = end_coords[1]

                    self._paths.append(PassageWay(f'path{i}-{j}', abs(end_coords[0] - start_coords[0]), abs(end_coords[1] - start_coords[1]), passageway_pos_y, passageway_pos_x))
        

    def _generate_room(self, room_index: int):
        height = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        width = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        pos_y = random.randrange(0, self._map_height - height)
        pos_x = random.randrange(0, self._map_width - width)
        return Room(f'room{room_index}', height, width, pos_y, pos_x, self._generate_doors(room_index=room_index, room_height=height, room_width=width))

    def _generate_doors(self, room_index: int, room_height: int, room_width: int):
        doors = []
        num_doors_options = [1, 2, 3, 4]
        num_doors_list = random.choices(
            num_doors_options, weights=(60, 80, 20, 10))

        for i in range(0, num_doors_list[0]):
            pos_y, pos_x = self._generate_random_door_position(room_height, room_width)
            special_character = SpecialEdgeCharacter(f'room{room_index}-door{i}', pos_y, pos_x, '+')
            doors.append(special_character)
            self._special_characters.append(special_character)

        return doors

    def _generate_random_door_position(self, room_height, room_width):
        pos_x = random.randrange(0, room_width)
        pos_y = None
        if(pos_x == 0 or pos_x == room_width):
            pos_y = random.randrange(0, room_height)
        else:
            pos_y = random.choice([0, room_height - 1])
        return (pos_y, pos_x)
