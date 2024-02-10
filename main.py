import pygame
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    BLACK,
    DARK_BLUE,
    NODE_HEIGHT,
    NODE_WIDTH,
    ROW_INDECIES,
    COL_INDECIES,
)
from models import Node
from utils import (
    check_end,
    create_shape,
    get_rows,
    check_lines,
    is_movable,
    move,
)

from typing import List


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Create new user events
# Add block falling event
block_falling = pygame.USEREVENT + 0
pygame.time.set_timer(block_falling, 300)


def main():
    running = True
    nodes = get_game_grid()
    rows = get_rows(nodes)
    moving = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == block_falling:
                direction = "down"
                if moving and is_movable(bottom_blocks, nodes, direction):
                    left_blocks, right_blocks, bottom_blocks = move(
                        current_shape,
                        nodes,
                        direction,
                        (left_blocks, right_blocks, bottom_blocks),
                    )
                else:
                    moving = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_movable(
                    left_blocks, nodes, "left"
                ):
                    left_blocks, right_blocks, bottom_blocks = move(
                        current_shape,
                        nodes,
                        "left",
                        (left_blocks, right_blocks, bottom_blocks),
                    )

                if event.key == pygame.K_RIGHT and is_movable(
                    right_blocks, nodes, "right"
                ):
                    left_blocks, right_blocks, bottom_blocks = move(
                        current_shape,
                        nodes,
                        "right",
                        (left_blocks, right_blocks, bottom_blocks),
                    )

                if event.key == pygame.K_DOWN and is_movable(
                    bottom_blocks, nodes, "down"
                ):
                    left_blocks, right_blocks, bottom_blocks = move(
                        current_shape,
                        nodes,
                        "down",
                        (left_blocks, right_blocks, bottom_blocks),
                    )

        if not moving:
            check_lines(rows, nodes)
            current_shape = create_shape(nodes)
            left_blocks = current_shape.get_side_blocks(nodes, "left")
            right_blocks = current_shape.get_side_blocks(nodes, "right")
            bottom_blocks = current_shape.get_side_blocks(nodes, "down")
            moving = True

        # if check_end(nodes):
        #     running = False

        WINDOW.fill(DARK_BLUE)
        draw_game_grid(nodes)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def get_game_grid() -> List[List[Node]]:
    nodes = []
    for row in range(ROW_INDECIES):
        nodes.append([])
        for col in range(COL_INDECIES):
            nodes[row].append(Node(row, col, NODE_WIDTH, NODE_HEIGHT))

    frames = (
        nodes[0][:-1]
        + nodes[-1][:-1]
        + [
            node
            for row in nodes
            for node in row
            if row.index(node) == 0 or row.index(node) == COL_INDECIES - 1
        ]
    )
    for node in frames:
        node.make_frame()

    return nodes


def draw_game_grid(nodes: List[List[Node]]) -> None:
    for row in nodes:
        for node in row:
            pygame.draw.rect(
                WINDOW, node.color, pygame.Rect(node.x, node.y, node.width, node.height)
            )

            pygame.draw.rect(
                WINDOW, BLACK, pygame.Rect(node.x, node.y, node.width, node.height), 1
            )


if __name__ == "__main__":
    main()
