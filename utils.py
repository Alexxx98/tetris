from settings import ROW_INDECIES, COL_INDECIES
from models import Node, Shape

from typing import List, Tuple
import random


def get_rows(nodes: list) -> list:
    rows: list = [[] for _ in range(0, COL_INDECIES - 1)]
    for line_index, line in enumerate(nodes):
        if line_index in range(1, ROW_INDECIES - 1):
            for node_index, node in enumerate(line):
                if node_index in range(1, COL_INDECIES - 1) and node.is_empty():
                    rows[node_index].append(node)

    return rows


def get_shape(current_block: Node, nodes: List[List[Node]]) -> Shape:
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
        6: [
            current_block,
            nodes[pos1][pos2 + 1],
            nodes[pos1][pos2 + 2],
            nodes[pos1 - 1][pos2 + 2],
        ],  # J
    }

    return Shape(shapes[random.randint(1, len(shapes))])


def create_shape(nodes: List[List[Node]]) -> Shape:
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
                    raise IndexError
                if node.is_block():
                    quit()
        except IndexError:
            continue
        else:
            break

    for node in shape.get_blocks():
        node.make_block()

    return shape


def is_movable(shape: list, nodes: List[List[Node]], direction: str) -> bool:
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


def move(
    current_shape: List[Node],
    nodes: List[List[Node]],
    direction: str,
    blocks: Tuple[List[Node]],
) -> List[List[Node]]:
    new_shape = []
    for node in current_shape.get_blocks():
        pos1, pos2 = node.get_pos()
        match direction:
            case "left":
                next_node = nodes[pos1 - 1][pos2]
            case "right":
                next_node = nodes[pos1 + 1][pos2]
            case "down":
                next_node = nodes[pos1][pos2 + 1]
        node.make_empty()
        new_shape.append(next_node)

    for index, node in enumerate(new_shape):
        node.make_block()
        current_shape.update_block(index, node)

    return current_shape.update_side_blocks(nodes, direction, blocks)


def check_lines(rows: List[List[Node]], nodes: List[List[Node]]) -> None:
    empty_nodes = 0

    # Look for empty rows
    for row in rows:
        for node in row:
            if node.is_empty():
                empty_nodes += 1

        # Clear all nodes if row full of blocks
        if empty_nodes == 0:
            for block in row:
                block.make_empty()

            # Move every blocks above by one node down
            new_blocks = []
            for row in rows[: rows.index(row)]:
                for node in row:
                    if node.is_block():
                        pos1, pos2 = node.get_pos()
                        node.make_empty()
                        new_blocks.append(nodes[pos1][pos2 + 1])
            for node in new_blocks:
                node.make_block()

        empty_nodes = 0


def check_end(nodes: List[List[Node]]) -> None:
    counter = 0
    for row in nodes:
        for node in row:
            if node.is_empty():
                counter += 1

    if counter == 0:
        return True
    return False
