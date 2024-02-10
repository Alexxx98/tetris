from settings import BLACK, GREY, RED, BLUE

from typing import List, Tuple


class Node:
    def __init__(self, row, col, width, height):
        self.row = row
        self.col = col
        self.x = row * width + 20
        self.y = col * height + 20
        self.width = width
        self.height = height
        self.color = BLACK

    def __repr__(self):
        return f"{self.row, self.col}"

    def get_pos(self) -> Tuple[int, int]:
        return (self.row, self.col)

    def turn_right(self):
        self.row -= 1

    def make_frame(self):
        self.color = GREY

    def make_block(self):
        self.color = RED

    def make_empty(self):
        self.color = BLACK

    def make_open(self):
        self.color = BLUE

    def is_frame(self):
        return self.color == GREY

    def is_block(self):
        return self.color == RED

    def is_empty(self):
        return self.color == BLACK


class Shape:
    def __init__(self, shape: list) -> None:
        self.shape = shape

    def get_blocks(self):
        return self.shape

    def update_block(self, index: int, block: Node) -> None:
        self.shape[index] = block

    def get_side_blocks(self, nodes: List[List[Node]], direction: str) -> List[Node]:
        result: List[Node] = []
        for block in self.shape:
            pos1, pos2 = block.get_pos()
            match direction:
                case "left":
                    if not nodes[pos1 - 1][pos2].is_block():
                        result.append(block)
                case "right":
                    if not nodes[pos1 + 1][pos2].is_block():
                        result.append(block)
                case "down":
                    if not nodes[pos1][pos2 + 1].is_block():
                        result.append(block)

        return result

    def update_side_blocks(self, nodes: list, direction: str, blocks: tuple) -> list:
        new_blocks = []
        for index, line in enumerate(blocks):
            new_blocks.append([])
            for block in line:
                pos1, pos2 = block.get_pos()
                match direction:
                    case "left":
                        new_blocks[index].append(nodes[pos1 - 1][pos2])
                    case "right":
                        new_blocks[index].append(nodes[pos1 + 1][pos2])
                    case "down":
                        new_blocks[index].append(nodes[pos1][pos2 + 1])

        return new_blocks
