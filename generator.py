import math
import random
import generation_algroitms as g
from pathlib import Path
import image_manager
BASE_DIR = Path(__file__).absolute().parent

bush_percent = 0.7
start_position = (0,0)
iteration = 15
split_iteration = 6
walk_length = 15
start_randomly_each_iteration = True
corridor_count = 10
corridor_length = 10
room_percent = 0.8
h_ratio = 0.46
w_ratio = 0.46
discard_by_ratio = True
offset = 2
random_walk_rooms = True

collision_points = set()
start = [0,0]
working_zone = set()

def distance_from_start(point):
    x, y = point
    return math.sqrt(x ** 2 + y ** 2)





def run_generation(size):
    create_splitted_rooms(size)

def run_random_walk(position):
    current_position = position
    floor_positions = set()
    for i in range(iteration):
        path = g.simple_random_walk(current_position, walk_length)
        floor_positions |= path
        if start_randomly_each_iteration and len(floor_positions)-2>0:
            r = random.randint(1, len(floor_positions)-2)
            for _ in range(0, r):
                current_position = next(iter(floor_positions))
    return floor_positions


def find_closest_point(current_room_center, room_centers):
    closest = None
    min_distance = float('inf')

    for position in room_centers:
        distance = math.sqrt((position.x - current_room_center.x) ** 2 + (position.y - current_room_center.y) ** 2)

        if distance < min_distance:
            closest = position
            min_distance = distance

    return closest

#def find_closest_point(current_room_center, room_centers):
    # closest = (0, 0)
    # distance = 100000
    # for position in room_centers:
    #     current_distance = (abs(position.x - current_room_center.x),
    #                         abs(position.x - current_room_center.x))
    #
    #     if isinstance(distance, tuple):
    #         if current_distance[0] < distance[0] and current_distance[1] < distance[1]:
    #             distance = (current_distance[0], current_distance[1])
    #             closest = position
    #     else:
    #         if current_distance[0] < distance and current_distance[1] < distance:
    #             distance = (current_distance[0], current_distance[1])
    #             closest = position
    # return closest


def create_corridor(current_room_center, destination):
    corridor = set()
    position = current_room_center
    corridor.add((position.x, position.y))

    while position.y != destination.y:
        position.y += 1 if destination.y > position.y else -1
        corridor.add((position.x, position.y))

    while position.x != destination.x:
        position.x += 1 if destination.x > position.x else -1
        corridor.add((position.x, position.y))

    return corridor
def connect_rooms(room_centers):
    corridors = []
    current_room_center = room_centers.pop(random.randint(0, len(room_centers)-1))

    while len(room_centers) > 0:
        closest = find_closest_point(current_room_center, room_centers)
        room_centers.remove(closest)
        new_corridor = create_corridor(current_room_center, closest)
        current_room_center = closest
        #тут ошибка так как коридоры сливаются в единый а не остаются по разным словарям
        corridors.append(new_corridor)
    return corridors


def create_rooms_randomly(rooms):
    floor = set()
    for room in rooms.get_leafs():
        room_bounds = room.leaf
        room_center = room.leaf.center
        room_floor = run_random_walk((room_center.x, room_center.y))
        for position in room_floor:
            if position[0] >= room_bounds.x + offset and position[0] <= room_bounds.x + room_bounds.w - offset and position[1] >= room_bounds.y + offset and position[1] <= room_bounds.y + room_bounds.h - offset:
                floor.add(position)
    return floor


def make_component_for_image(floor, empty_space):
    import numpy as np
    component_grass = np.array(list(floor), dtype=np.int32)
    basic_wall_positions = find_walls_in_direction(floor, g.cardinal_directions)
    component_walls = np.array(list(basic_wall_positions), dtype=np.int32)
    new_empty_space = empty_space - basic_wall_positions
    component_dirt = np.array(list(new_empty_space), dtype=np.int32)
    component_trees = random_bushes_fill(new_empty_space, fill_percent=bush_percent) #dictionary
    component_dict = {BASE_DIR / "resources" / "images" / "tiles" / "dirt.jpeg": component_dirt,
                      BASE_DIR / "resources" / "images" / "tiles" / "bush.jpeg": component_walls,
                      BASE_DIR / "resources" / "images" / "tiles" / "grass.jpg":  component_grass
                      }
    component_dict |= component_trees



    return component_dict


def create_splitted_rooms(size, c_p = collision_points, w_z=working_zone):
    #tracemalloc.start()
    container = g.Container(start_position[0],
                                          start_position[1],
                                          65,
                                          40)
    rooms = g.split_container(container, split_iteration,
                              discard_by_ratio,
                              h_ratio,
                              w_ratio)
    floor = set()
    available_space = set()

    if random_walk_rooms:
        floor = create_rooms_randomly(rooms)
    else:
        floor = create_simple_rooms(rooms)

    room_centers = [room.leaf.center for room in rooms.get_leafs()]

    corridors = connect_rooms(room_centers)
    for cor in corridors:
        for point in cor:
            floor.add(point)
    #ОБРАТБОТКА ОШИБКИ ТУПИКА
    if not is_connected(rooms, corridors):
        create_exits(rooms,corridors, room_centers)
    empty_space = fill_empty_space(floor, container)
    components = make_component_for_image(floor, empty_space)
    image_manager.make_image(container, size, components)

    #print(tracemalloc.get_traced_memory())
    #tracemalloc.stop()
    c_p |= empty_space
    w_z.update([(p[0] * size[0], p[1] * size[1]) for p in floor])
    start[0], start[1] = sorted(w_z, key=distance_from_start)[0]
    #start[0], start[1] = move_player_to_exit((start[0],start[1]),rooms)

    #serializer.write(floor)
def move_player_to_exit(player_position, rooms):
    exit_found = False
    for room in rooms.get_leafs():
        room_center = room.leaf.center
        if room_center.x != player_position[0] and room_center.y != player_position[1]:
            # Переместите игрока в центр ближайшей комнаты
            player_position = room_center
            exit_found = True
            break
    return player_position.x, player_position.y

def create_exits(rooms, corridors, room_centers):
    isolated_rooms = []
    for room in rooms.get_leafs():
        room_center = room.leaf.center
        exits = 0
        for direction in g.cardinal_directions:
            neighbor = (room_center.x + direction[0], room_center.y + direction[1])
            if neighbor in corridors:
                exits += 1
        if exits == 0:
            # Создайте выход в случайном направлении
            isolated_rooms.append(room)
    for room in isolated_rooms:
        # Находим ближайшую соединенную комнату
        closest = find_closest_point(room.leaf.center, room_centers)
        if closest:
            new_corridor = create_corridor(room, closest)
            corridors.append(new_corridor) 

def is_connected(rooms, corridors):
    graph = {}
    
    # Добавляем комнаты в граф
    for room in rooms.get_leafs():
        room_center = (room.leaf.center.x, room.leaf.center.y)
        graph[room_center] = []

    # Добавляем коридоры в граф
    for corridor in corridors:
        for point in corridor:
            if point not in graph:
                graph[point] = []

    # Соединяем коридоры с комнатами
    for room in rooms.get_leafs():
        room_center = (room.leaf.center.x, room.leaf.center.y)
        for corridor in corridors:
            for point in corridor:
                # Если коридор находится рядом с комнатой, соединяем их
                if is_near(room_center, point):
                    graph[room_center].append(point)
                    graph[point].append(room_center)

    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    # Начинаем обход с первой комнаты
    #start_node = (start_node = (rooms.get_leafs()[0].leaf.center.x, rooms.get_leafs()[0].leaf.center.y)
    for room in rooms.get_leafs():
        start_node = (room.leaf.center.x, room.leaf.center.y) = (room.leaf.center.x, room.leaf.center.y)
        dfs(start_node)
        break
    

    # Проверяем, что все комнаты и коридоры посещены
    leaf_rooms = list(rooms.get_leafs())  # Convert the generator to a list
    num_leaf_rooms = len(leaf_rooms)  # Get the number of leaf rooms

    # Calculate the total number of corridor points
    total_corridor_points = sum(len(corridor) for corridor in corridors)

    # Sum the number of leaf rooms and corridor points
    total_nodes = num_leaf_rooms + total_corridor_points
    return len(visited) == total_nodes

def is_near(room_center, point):
    # Определяем, насколько близко коридор должен быть к комнате, чтобы считать их связанными
    threshold = 1  # Например, если коридор находится в пределах 1 единицы от комнаты
    return (abs(room_center[0] - point[0]) <= threshold and
            abs(room_center[1] - point[1]) <= threshold)

def fill_empty_space(floor, container):
    empty_space = set()
    for x in range(container.w):
        for y in range(container.h):
            if (x, y) not in floor:
                empty_space.add((x, y))
    return empty_space

def create_simple_rooms(rooms):
    floor = set()
    for leaf in rooms.get_leafs():
        room = leaf.leaf
        for col in range(offset, room.w - offset):
            for row in range(offset, room.h - offset):
                position = (room.x + col, room.y + row)
                floor.add(position)
    return floor



def find_walls_in_direction(floor_positions, direction_list):
    wall_positions = set()
    for position in floor_positions:
        for direction in direction_list:
            neighbour_position = (position[0] + direction[0], position[1] + direction[1])
            if neighbour_position not in floor_positions:
                wall_positions.add(neighbour_position)
    return wall_positions


def increase_corridor_size_by_one(corridor):
    new_corridor = []
    preview_direction = (0,0)
    for i in range(1, len(corridor)):
        direction_from_cell = (corridor[i][0] - corridor[i-1][0],
                               corridor[i][1] - corridor[i-1][1])
        if preview_direction != (0,0) and direction_from_cell != preview_direction:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    new_corridor.append((corridor[i-1][0] + x,
                                         corridor[i-1][1] + y))
        else:
            new_corridor_tile_offset = get_direction_90_from(direction_from_cell)
            new_corridor.append(corridor[i-1])
            new_corridor.append((new_corridor[i-1][0] + new_corridor_tile_offset[0],
                                new_corridor[i-1][1] + new_corridor_tile_offset[1]))
    return new_corridor


def get_direction_90_from(direction):
    if direction == g.cardinal_directions[0]:
        return g.cardinal_directions[1]
    if direction == g.cardinal_directions[1]:
        return g.cardinal_directions[2]
    if direction == g.cardinal_directions[2]:
        return g.cardinal_directions[3]
    if direction == g.cardinal_directions[3]:
        return g.cardinal_directions[0]


def increase_corridor_size_by_three(corridor):
    new_corridor = []
    for i in range(1, len(corridor)):
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_corridor.append((corridor[i-1][0] + x, corridor[i-1][1]+y))
    return new_corridor


def generate_corridor(tilemap_main, tilemap_walls):
    floor_positions = set()
    potential_room_positions = set()

    corridors = create_corridors(floor_positions, potential_room_positions)

    room_positions = create_rooms(potential_room_positions)
    dead_ends = find_all_dead_ends(floor_positions)
    create_room_at_dead_end(dead_ends, room_positions)
    floor_positions |= room_positions

    for corridor in corridors:
        corridor = increase_corridor_size_by_three(corridor)
        floor_positions |= corridor



def create_rooms(potential_room_positions):
    room_positions = set()
    room_to_create_count = round(len(potential_room_positions) * room_percent)

    room_to_create = random.sample(potential_room_positions, room_to_create_count)

    for room_position in room_to_create:
        room_floor = run_random_walk(room_position)
        room_positions |= room_floor
    return room_positions



def create_corridors(floor_positions, potential_room_positions):
    current_position = start_position
    potential_room_positions.add((current_position))
    corridors = []
    for i in range(corridor_count):
        corridor = g.random_walk_corridor(current_position, corridor_length)
        corridors.append(corridor)
        current_position = corridor[len(corridor) - 1]
        potential_room_positions.add(current_position)
        floor_positions |= corridor
    return corridors


def find_all_dead_ends(floor_positions):
    dead_ends = []
    for position in floor_positions:
        neighbours_count = 0
        for direction in g.cardinal_directions:
            if (position[0] + direction[0], position[1] + direction[1]) in floor_positions:
                neighbours_count += 1

        if neighbours_count == 1:
            dead_ends.append(position)
    return dead_ends


def create_room_at_dead_end(dead_ends, room_floors):
    for position in dead_ends:
        if position not in room_floors:
            room = run_random_walk(position)
            room_floors |= room


def random_bushes_fill(floor, fill_percent):
    filled = {}

    for x, y in floor:
        if random.uniform(0.0, 1.0) <= fill_percent:
            image_index = random.randint(1, 40)
            filled.setdefault(f"{BASE_DIR}/resources/images/bushes/{image_index}.png", []).append((x, y))

    return filled