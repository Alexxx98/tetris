import pygame
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    WHITE,
    BLACK,
    GREY,
    DARK_BLUE,
    NODE_HEIGHT,
    NODE_WIDTH,
    ROW_INDECIES,
    COL_INDECIES,
    SB_WIDTH,
    SB_HEIGHT,
    SB_X,
    SB_Y,
)
from models import Node, Shape
from utils import (
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

# Create block falling event
block_falling = pygame.USEREVENT + 0
pygame.time.set_timer(block_falling, 300)


def main():
    running: bool = True
    nodes = get_game_grid()
    rows = get_rows(nodes)
    moving: bool = False
    current_shape: Shape = None
    score = 0
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

                # Rotate the shape
                if event.key == pygame.K_UP:
                    current_shape.rotate()

                    left_blocks = current_shape.get_side_blocks(nodes, "left")
                    right_blocks = current_shape.get_side_blocks(nodes, "right")
                    bottom_blocks = current_shape.get_side_blocks(nodes, "down")

        if not moving:
            if current_shape:
                score += check_lines(current_shape, rows, nodes)
            current_shape = create_shape(rows, nodes)
            left_blocks = current_shape.get_side_blocks(nodes, "left")
            right_blocks = current_shape.get_side_blocks(nodes, "right")
            bottom_blocks = current_shape.get_side_blocks(nodes, "down")
            moving = True

        WINDOW.fill(DARK_BLUE)
        draw_game_grid(nodes)
        draw_score_board(score)
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

    # Add col from right side to fix I shape variant problem
    nodes.append([])
    for col in range(COL_INDECIES):
        nodes[-1].append(Node(ROW_INDECIES, col, NODE_WIDTH, NODE_HEIGHT))

    return nodes


def draw_game_grid(nodes: List[List[Node]]) -> None:
    for row in nodes[:-1]:
        for node in row:
            pygame.draw.rect(
                WINDOW, node.color, pygame.Rect(node.x, node.y, node.width, node.height)
            )

            pygame.draw.rect(
                WINDOW, BLACK, pygame.Rect(node.x, node.y, node.width, node.height), 1
            )


def draw_score_board(score):
    # Draw background and frame
    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(SB_X, SB_Y, SB_WIDTH, SB_HEIGHT))
    pygame.draw.rect(WINDOW, GREY, pygame.Rect(SB_X, SB_Y, SB_WIDTH, SB_HEIGHT), 2)

    # Draw score content
    font = pygame.font.Font("UrbanBlockerSolid.ttf", 38)
    score_text = font.render("Score:", True, WHITE)

    font = pygame.font.SysFont("arial", 38)
    score_value = font.render(str(score), True, WHITE)

    text_position = (SB_X + SB_WIDTH // 3, SB_Y + SB_HEIGHT // 2 - 50)
    value_position = (SB_X + SB_WIDTH // 3, SB_Y + SB_HEIGHT // 2)

    WINDOW.blit(score_text, text_position)
    WINDOW.blit(score_value, value_position)


if __name__ == "__main__":
    main()
