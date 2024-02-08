from settings import ROW_INDECIES, COL_INDECIES
from models import Node

import random


def get_rows(nodes: list) -> list:
    rows: list = [[] for _ in range(0, COL_INDECIES - 1)]
    for line_index, line in enumerate(nodes):
        if line_index in range(1, ROW_INDECIES - 1):
            for node_index, node in enumerate(line):
                if node_index in range(1, COL_INDECIES - 1):
                    rows[node_index].append(node)

    rows.pop(0)

    return rows


def get_shape(current_block: Node, nodes: list) -> list:
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
    }

    return shapes[random.randint(1, len(shapes))]


def create_shape(nodes: list) -> Node:
    starting_nodes: list = [
        node
        for row in nodes
        for node in row
        if nodes.index(row) in range(1, ROW_INDECIES - 1) and row.index(node) == 1
    ]

    # Get shape starting point and check if it fits within the grid
    while True:
        try:
            starting_block: Node = starting_nodes[random.randint(1, ROW_INDECIES - 3)]
            shape: list = get_shape(starting_block, nodes)
            for node in shape:
                if node.is_frame():
                    continue
            break
        except IndexError:
            continue

    for node in shape:
        node.make_block()

    return shape


def get_active_node(shape: list) -> Node:
    active_node = shape[0]
    for node in shape:
        active_pos1, active_pos2 = active_node.get_pos()
        node_pos1, node_pos2 = node.get_pos()

        # if node is below the active node, make node new active node
        if active_pos2 < node_pos2:
            active_node = node

    return active_node


def is_movable(shape: list, nodes: list, direction: str) -> bool:
    for node in shape:
        pos1, pos2 = node.get_pos()
        if direction == "rigth":
            if nodes[pos1 + 1][pos2].is_frame():
                return False
        elif direction == "left":
            if nodes[pos1 - 1][pos2].is_frame():
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
