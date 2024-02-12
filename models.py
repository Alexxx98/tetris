from settings import BLACK, GREY, RED, BLUE, GREEN, YELLOW, PURPLE, CYAN, BROWN

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

    def make_block(self, shape_color: Tuple[int, int, int]):
        self.color = shape_color

    def make_empty(self):
        self.color = BLACK

    def make_open(self):
        self.color = BLUE

    def is_frame(self):
        return self.color == GREY

    def is_block(self):
        return self.color in (RED, GREEN, BLUE, YELLOW, BROWN, PURPLE, CYAN)

    def is_empty(self):
        return self.color == BLACK


class Shape:
    def __init__(
        self, shapes: Tuple[List[Node]], shape: int, color: Tuple[int, int, int]
    ) -> None:
        self.shapes = shapes
        self.shape = shapes[shape]
        self.color = color

    def get_shapes(self):
        return self.shapes

    def get_current_shape(self):
        return self.shape

    def get_variant_nodes(self, variant: int):
        return self.shapes[variant]

    def get_color(self):
        return self.color

    def rotate(self):
        # Choose next shape
        if self.shape == self.shapes[-1]:
            next_shape = self.shapes[0]
        else:
            next_shape = self.shapes[(self.shapes.index(self.shape) + 1)]

        # Check if next shape
        for block in next_shape:
            if block.is_frame() or (block.is_block() and block not in self.shape):
                return

        for block in self.shape:
            block.make_empty()

        self.shape = next_shape

        for node in self.shape:
            node.make_block(self.color)

    def update_block(self, variant: int, node: int, block: Node) -> None:
        self.shapes[variant][node] = block

    def get_side_blocks(self, nodes: List[List[Node]], direction: str) -> List[Node]:
        result: List[Node] = []
        for block in self.shape:
            pos1, pos2 = block.get_pos()
            match direction:
                case "left":
                    if nodes[pos1 - 1][pos2] not in self.shape:
                        result.append(block)
                case "right":
                    if nodes[pos1 + 1][pos2] not in self.shape:
                        result.append(block)
                case "down":
                    if nodes[pos1][pos2 + 1] not in self.shape:
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
