


from random import randint

import generator
from container import Container
from tree import Tree
cardinal_directions = [(-1,0),(1,0),(0,-1),(0,1)]
                        #  up           right          down            left

def random_direction():
    return cardinal_directions[randint(0,3)]


def simple_random_walk(start_position, walk_length):
    path = {}
    path[start_position] = True  # Помечаем начальную позицию
    previous_position = start_position
    for i in range(walk_length):
        new_position = (previous_position[0] + random_direction()[0], (previous_position[1] + random_direction()[1]))
        path[new_position] = True
        previous_position = new_position
    return set(path.keys())


def random_walk_corridor(start_position, length):
    import numpy as np
    corridor = np.array([list(start_position)])  # Преобразуем кортеж в список и создаем numpy.array
    direction = np.array(list(random_direction()), dtype=np.int32)  # Преобразуем кортеж в список и создаем numpy.array
    current_position = np.array(start_position, dtype=np.int32)
    for i in range(length):
        current_position = current_position + direction
        corridor = np.append(corridor, [list(current_position)], axis=0)  # Преобразуем кортеж в список и добавляем в массив
    corridor = generator.increase_corridor_size_by_one(corridor)
    return corridor



def split_container(container, iteration, if_ratio, h_r, w_r):
    root = Tree(container)
    if iteration != 0:
        sr = random_split(container, if_ratio, h_r, w_r, 0, 10)
        root.lchild = split_container(sr[0], iteration-1, if_ratio, h_r, w_r)
        root.rchild = split_container(sr[1], iteration-1, if_ratio, h_r, w_r)
    return root

def random_split(container, discard_by_ratio, h_ratio, w_ratio, depth=0, max_depth=10):
    if depth >= max_depth:
        return [container, container]

    if container.w >= 2 and container.h >= 2:
        if randint(0, 1) == 0:
            r1 = Container(
                container.x, container.y,
                randint(1, container.w), container.h
            )
            r2 = Container(
                container.x + r1.w, container.y,
                container.w - r1.w, container.h
            )
            if discard_by_ratio:
                r1_w_ratio = r1.w / r1.h
                r2_w_ratio = r2.w / r2.h
                if r1_w_ratio < w_ratio or r2_w_ratio < w_ratio:
                    return random_split(container, discard_by_ratio, h_ratio, w_ratio, depth+1, max_depth)
        else:
            r1 = Container(
                container.x, container.y,
                container.w, randint(1, container.h)
            )
            r2 = Container(
                container.x, container.y + r1.h,
                container.w, container.h - r1.h
            )
            if discard_by_ratio:
                r1_h_ratio = r1.h / r1.w
                r2_h_ratio = r2.h / r2.w
                if r1_h_ratio < h_ratio or r2_h_ratio < h_ratio:
                    return random_split(container, discard_by_ratio, h_ratio, w_ratio, depth+1, max_depth)
        return [r1, r2]
    else:
        return [container, container]

