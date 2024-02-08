from settings import BLACK, GREY, RED, BLUE


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

    def get_pos(self):
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

    def get_left_blocks(self) -> list:
        pos1, pos2 = self.shape[0].get_pos()
        most_left = pos1

        # Check for most left position of the shape
        for block in self.shape:
            block_pos1, block_pos2 = block.get_pos()
            if pos1 > block_pos1:
                most_left = block_pos1

        # check how many blocks are on that position
        result = []
        for block in self.shape:
            pos1, pos2 = block.get_pos()
            if pos1 == most_left:
                result.append(block)

        return result

    def get_right_blocks(self) -> list:
        pos1, pos2 = self.shape[0].get_pos()
        most_right = pos1

        # Check for most left position of the shape
        for block in self.shape:
            block_pos1, block_pos2 = block.get_pos()
            if pos1 < block_pos1:
                most_right = block_pos1

        # check how many blocks are on that position
        result = []
        for block in self.shape:
            pos1, pos2 = block.get_pos()
            if pos1 == most_right:
                result.append(block)

        return result

    def get_bottom_blocks(self) -> list:
        pos1, pos2 = self.shape[0].get_pos()
        most_bottom = pos2

        # Check for most left position of the shape
        for block in self.shape:
            block_pos1, block_pos2 = block.get_pos()
            if pos2 < block_pos2:
                most_bottom = block_pos2

        # check how many blocks are on that position
        result = []
        for block in self.shape:
            pos1, pos2 = block.get_pos()
            if pos2 == most_bottom:
                result.append(block)

        return result
