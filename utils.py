from settings import (
    ROW_INDECIES,
    COL_INDECIES,
    RED,
    BLUE,
    GREEN,
    YELLOW,
    CYAN,
    BROWN,
    PURPLE,
)
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


def get_shapes(current_block: Node, nodes: List[List[Node]]) -> Shape:
    pos1, pos2 = current_block.get_pos()
    shapes: dict = {
        1: (
            [
                current_block,
                nodes[pos1 + 1][pos2],
                nodes[pos1 + 1][pos2 + 1],
                nodes[pos1][pos2 + 1],
            ],
            GREEN,
        ),  # O
        2: (
            [
                nodes[pos1][pos2 - 1],
                current_block,
                nodes[pos1][pos2 + 1],
                nodes[pos1 + 1][pos2 + 1],
            ],
            [
                nodes[pos1 - 1][pos2 + 1],
                nodes[pos1 - 1][pos2],
                current_block,
                nodes[pos1 + 1][pos2],
            ],
            [
                nodes[pos1 - 1][pos2 - 1],
                nodes[pos1][pos2 - 1],
                current_block,
                nodes[pos1][pos2 + 1],
            ],
            [
                nodes[pos1 - 1][pos2],
                current_block,
                nodes[pos1 + 1][pos2],
                nodes[pos1 + 1][pos2 - 1],
            ],
            BLUE,
        ),  # L
        3: (
            [
                nodes[pos1][pos2 - 1],
                current_block,
                nodes[pos1][pos2 + 1],
                nodes[pos1][pos2 + 2],
            ],
            [
                nodes[pos1 - 1][pos2],
                current_block,
                nodes[pos1 + 1][pos2],
                nodes[pos1 + 2][pos2],
            ],
            CYAN,
        ),  # I
        4: (
            [
                nodes[pos1 - 1][pos2],
                current_block,
                nodes[pos1][pos2 + 1],
                nodes[pos1 + 1][pos2 + 1],
            ],
            [
                nodes[pos1][pos2 - 1],
                current_block,
                nodes[pos1 - 1][pos2],
                nodes[pos1 - 1][pos2 + 1],
            ],
            PURPLE,
        ),  # Z
        5: (
            [
                nodes[pos1 + 1][pos2],
                current_block,
                nodes[pos1][pos2 + 1],
                nodes[pos1 - 1][pos2 + 1],
            ],
            [
                nodes[pos1][pos2 - 1],
                current_block,
                nodes[pos1 + 1][pos2],
                nodes[pos1 + 1][pos2 + 1],
            ],
            YELLOW,
        ),  # S
        6: (
            [
                nodes[pos1][pos2 - 1],
                current_block,
                nodes[pos1][pos2 + 1],
                nodes[pos1 - 1][pos2 + 1],
            ],
            [
                nodes[pos1 + 1][pos2],
                current_block,
                nodes[pos1 - 1][pos2],
                nodes[pos1 - 1][pos2 - 1],
            ],
            [
                nodes[pos1][pos2 + 1],
                current_block,
                nodes[pos1][pos2 - 1],
                nodes[pos1 + 1][pos2 - 1],
            ],
            [
                nodes[pos1 - 1][pos2],
                current_block,
                nodes[pos1 + 1][pos2],
                nodes[pos1 + 1][pos2 + 1],
            ],
            RED,
        ),  # J
        7: (
            [
                nodes[pos1 - 1][pos2],
                current_block,
                nodes[pos1 + 1][pos2],
                nodes[pos1][pos2 + 1],
            ],
            [
                nodes[pos1][pos2 - 1],
                current_block,
                nodes[pos1][pos2 + 1],
                nodes[pos1 - 1][pos2],
            ],
            [
                nodes[pos1 + 1][pos2],
                current_block,
                nodes[pos1 - 1][pos2],
                nodes[pos1][pos2 - 1],
            ],
            [
                nodes[pos1][pos2 + 1],
                current_block,
                nodes[pos1][pos2 - 1],
                nodes[pos1 + 1][pos2],
            ],
            BROWN,
        ),  # T
    }

    variant = random.randint(1, len(shapes))
    shape = random.randint(0, len(shapes[variant]) - 2)
    color = shapes[variant][-1]

    return Shape(shapes[variant][:-1], shape, color)


def create_shape(rows: List[List[Node]], nodes: List[List[Node]]) -> Shape:
    starting_rows: list = rows[:3]

    # Get shape starting point and check if it fits within the grid
    done = False
    valid = True
    row_index = 1
    while not done:
        try:
            starting_node_index = random.randint(0, len(starting_rows[1]) - 1)
            starting_node = starting_rows[row_index][starting_node_index]
            shape: Shape = get_shapes(starting_node, nodes)

            for node in shape.get_current_shape():
                if node.is_frame():
                    valid = False

            if valid:
                done = True

            for block in shape.get_current_shape():
                if block.is_frame():
                    raise IndexError

                if node.is_block():
                    quit()
        except IndexError:
            row_index += 1
            if row_index > 3:
                row_index = 0
            continue
        else:
            done = True

    for node in shape.get_current_shape():
        node.make_block(shape.get_color())

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
    current_shape: Shape,
    nodes: List[List[Node]],
    direction: str,
    blocks: Tuple[List[Node]],
) -> List[List[Node]]:

    # Get next nodes for every shape variant
    for variant_index, variant in enumerate(current_shape.get_shapes()):
        new_shape = []
        for node in current_shape.get_variant_nodes(variant_index):
            try:
                pos1, pos2 = node.get_pos()
                match direction:
                    case "left":
                        next_node = nodes[pos1 - 1][pos2]
                    case "right":
                        next_node = nodes[pos1 + 1][pos2]
                    case "down":
                        next_node = nodes[pos1][pos2 + 1]
            except IndexError:
                pass

            if variant == current_shape.get_current_shape():
                node.make_empty()
            new_shape.append(next_node)

        for index, node in enumerate(new_shape):
            if variant == current_shape.get_current_shape():
                node.make_block(current_shape.get_color())
            current_shape.update_block(variant_index, index, node)

    return current_shape.update_side_blocks(nodes, direction, blocks)


def check_lines(
    current_shape: Shape, rows: List[List[Node]], nodes: List[List[Node]]
) -> int:
    empty_nodes = 0
    lines = 0
    points = 0

    # Look for empty rows
    for row in rows[1:]:
        for node in row:
            if node.is_empty():
                empty_nodes += 1

        # Clear all nodes if row full of blocks
        if empty_nodes == 0:
            lines += 1
            points += 100
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
                node.make_block(current_shape.get_color())

        empty_nodes = 0

    return lines * points


def check_end(nodes: List[List[Node]]) -> None:
    counter = 0
    for row in nodes:
        for node in row:
            if node.is_empty():
                counter += 1

    if counter == 0:
        return True
    return False
