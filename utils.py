from settings import ROW_INDECIES, COL_INDECIES
from models import Node, Shape

import random


def get_rows(nodes: list) -> list:
    rows: list = [[] for _ in range(0, COL_INDECIES - 1)]
    for line_index, line in enumerate(nodes):
        if line_index in range(1, ROW_INDECIES - 1):
            for node_index, node in enumerate(line):
                if node_index in range(1, COL_INDECIES - 1) and node.is_empty():
                    rows[node_index].append(node)

    return rows


def get_shape(current_block: Node, nodes: list) -> Shape:
    pos1, pos2 = current_block.get_pos()
    shapes: dict = {
        1: [
            current_block,
            nodes[pos1 + 1][pos2],
            nodes[pos1 + 1][pos2 + 1],
            nodes[pos1][pos2 + 1],
        ],  # O
        2: [
            current_block,
            nodes[pos1][pos2 + 1],
            nodes[pos1][pos2 + 2],
            nodes[pos1 + 1][pos2 + 2],
        ],  # L
        3: [
            current_block,
            nodes[pos1][pos2 + 1],
            nodes[pos1][pos2 + 2],
            nodes[pos1][pos2 + 3],
        ],  # I
        4: [
            current_block,
            nodes[pos1 + 1][pos2],
            nodes[pos1 + 1][pos2 + 1],
            nodes[pos1 + 2][pos2 + 1],
        ],  # Z
        5: [
            current_block,
            nodes[pos1 + 1][pos2],
            nodes[pos1][pos2 + 1],
            nodes[pos1 - 1][pos2 + 1],
        ],  # S
    }

    return Shape(shapes[random.randint(1, len(shapes))])


def create_shape(nodes: list) -> Shape:
    starting_nodes: list = [
        node
        for row in nodes
        for node in row
        if nodes.index(row) in range(1, ROW_INDECIES - 1) and row.index(node) == 1
    ]

    # Get shape starting point and check if it fits within the grid
    while True:
        try:
            starting_block: Node = starting_nodes[
                random.randint(0, len(starting_nodes) - 1)
            ]
            shape: Shape = get_shape(starting_block, nodes)
            for node in shape.get_blocks():
                if node.is_frame():
                    continue
                if node.is_block():
                    quit()
        except IndexError:
            continue
        else:
            break

    for node in shape.get_blocks():
        node.make_block()

    return shape


def is_movable(shape: list, nodes: list, direction: str) -> bool:
    for node in shape:
        pos1, pos2 = node.get_pos()
        if direction == "right":
            if not nodes[pos1 + 1][pos2].is_empty():
                return False
        elif direction == "left":
            if not nodes[pos1 - 1][pos2].is_empty():
                return False
        elif direction == "down":
            if not nodes[pos1][pos2 + 1].is_empty():
                return False
    return True


def check_lines(rows: list) -> None:
    counter = 0
    for row in rows:
        for node in row:
            if node.is_empty():
                counter += 1

        if counter == 0:
            for node in row:
                node.make_empty()

        counter = 0


def check_end(nodes: list) -> None:
    counter = 0
    for row in nodes:
        for node in row:
            if node.is_empty():
                counter += 1

    if counter == 0:
        return True
    return False
