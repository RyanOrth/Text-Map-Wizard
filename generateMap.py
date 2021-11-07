from window import PassageWay, Room, Window
from specialCharacters import SpecialEdgeCharacter
import random
from constants import MIN_ROOM_SIZE, MAX_ROOM_SIZE, MAX_ITERATIONS, MAX_ROOM_COUNT, MAP_X, MAP_Y
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

    def generate_map(self) -> list:
        i = 0
        max_iter = MAX_ITERATIONS
        while i < MAX_ROOM_COUNT and max_iter > 0:
            room = self._generate_room(i)
            if(self._window_is_not_overlapping(room)):
                self._map.append(room)
                self._occupied_regions.append(OccuppiedRegion(room))
                i += 1
            max_iter -= 1
        return self._map

    def _window_is_not_overlapping(self, candidate_window: Room) -> bool:
        candidate_region = OccuppiedRegion(candidate_window)
        for occupied_region in self._occupied_regions:
            # If the inside x is inside a  x bound
            min_x_in_xbounds = candidate_region.min_x in range(
                occupied_region.min_x, occupied_region.max_x + 1)
            # If the outside x is inside a  x bound
            max_x_in_xbounds = candidate_region.max_x in range(
                occupied_region.min_x, occupied_region.max_x + 1)
            # If the inside y is inside a  y bound
            min_y_in_ybounds = candidate_region.min_y in range(
                occupied_region.min_y, occupied_region.max_y + 1)
            # If the outside y is inside a  y bound
            max_y_in_ybounds = candidate_region.max_y in range(
                occupied_region.min_y, occupied_region.max_y + 1)

            if((min_x_in_xbounds or max_x_in_xbounds) or (min_y_in_ybounds or max_y_in_ybounds)):
                return False
            # if(candidate_region.min_x in range(occupied_region.min_x, occupied_region.max_x + 1)):
            #     if(candidate_region.min_y in range(occupied_region.min_y, occupied_region.min_y + 1)):
            #         return False
            #     elif(candidate_region.max_y in range(occupied_region.min_y, occupied_region.max_y + 1)):
            #         return False
            # elif (candidate_region.max_x in range(occupied_region.min_x, occupied_region.max_x + 1)):
            #     if(candidate_region.min_y in range(occupied_region.min_y, occupied_region.min_y + 1)):
            #         return False
            #     elif(candidate_region.max_y in range(occupied_region.min_y, occupied_region.max_y + 1)):
            #         return False
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
        return Room(f'room{room_index}', height, width, pos_y, pos_x, self._generate_doors(room_index=room_index, room_height=height, room_width=width, room_pos_y=pos_y, room_pos_x=pos_x))

    def _generate_doors(self, room_index: int, room_height: int, room_width: int, room_pos_y: int, room_pos_x: int) -> list:
        doors = []
        num_doors_options = [1, 2, 3, 4]
        num_doors_list = random.choices(
            num_doors_options, weights=(60, 80, 20, 10))

        i = 0
        while i < num_doors_list[0]:
            pos_y, pos_x = self._generate_random_door_position(
                room_height, room_width)
            not_on_top = not (room_pos_y == 0 and pos_y == 0)
            not_on_left = not (room_pos_x == 0 and pos_x == 0)
            not_on_bottom = not (room_pos_y + room_height ==
                                 MAP_Y and pos_y == room_height)
            not_on_right = not(room_pos_x + room_width ==
                               MAP_X and pos_x == room_width)
            if not_on_top and not_on_right and not_on_left and not_on_bottom:
                special_character = SpecialEdgeCharacter(
                    f'room{room_index}-door{i}', pos_y, pos_x, '+')
                doors.append(special_character)
                self._special_characters.append((special_character))
                i += 1

        return doors

    def _generate_random_door_position(self, room_height, room_width) -> tuple:
        xrange = list(range(0, room_width+1))
        weights = ((
            room_height-2) if (i == 0 or i == room_width) else 1.0 for i in range(0, room_width+1))
        pos_x = random.choices(xrange, weights=weights)[0]
        pos_y = None
        if(pos_x == 0 or pos_x == room_width):
            pos_y = random.randrange(1, room_height-1)
        else:
            pos_y = random.choice([0, room_height - 1])
        return (pos_y, pos_x)
