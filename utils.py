from settings import NUM_OF_ROWS
from models import Node

import random


def create_shape(nodes: list) -> Node:
    starting_nodes: list = [
        node
        for row in nodes
        for node in row
        if nodes.index(row) in range(1, NUM_OF_ROWS - 1) and row.index(node) == 1
    ]

    starting_block = starting_nodes[random.randint(1, NUM_OF_ROWS - 2)]
    starting_block.make_block()
    return starting_block


def fall(node: Node, nodes: list) -> bool:
    pos1, pos2 = node.get_pos()
    next_node = nodes[pos1][pos2 + 1]
    if not next_node.is_block() and not next_node.is_frame():
        node.make_empty()
        next_node.make_block()
        return True
    return False


def check_end(nodes: list) -> None:
    counter = 0
    for row in nodes:
        for node in row:
            if node.is_empty():
                counter += 1

    if counter == 0:
        return True
    return False
