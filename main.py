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
    NS_WIDTH,
    NS_HEIGHT,
    NS_X,
    NS_Y,
    LVL_WIDTH,
    LVL_HEIGHT,
    LVL_X,
    LVL_Y,
)
from models import Node, Shape
from utils import (
    create_shape,
    get_rows,
    check_lines,
    is_movable,
    move,
)

from typing import List, Tuple
from queue import Queue


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Create block falling event
block_falling = pygame.USEREVENT + 0


def main():
    fall_speed = 1000
    pygame.time.set_timer(block_falling, fall_speed)
    running: bool = True
    nodes = get_game_grid()
    rows = get_rows(nodes)
    moving: bool = False
    current_shape: Shape = None
    shapes: Queue = Queue(2)
    score: int = 0
    next_shape_nodes = get_next_shape_grid()
    level: int = 1
    next_level_threshold: int = 5
    cleared_lines: int = 0
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
                new_score, cleared_lines = check_lines(
                    current_shape, rows, nodes, cleared_lines
                )
                score += new_score * level

            if cleared_lines >= next_level_threshold and level < 10:
                next_level_threshold += 1
                cleared_lines = 0
                level += 1
                fall_speed -= 100
                pygame.time.set_timer(block_falling, fall_speed)

            shapes = create_shape(rows, nodes, shapes)
            current_shape = shapes.get()
            next_shape = shapes.queue[0]
            left_blocks = current_shape.get_side_blocks(nodes, "left")
            right_blocks = current_shape.get_side_blocks(nodes, "right")
            bottom_blocks = current_shape.get_side_blocks(nodes, "down")
            moving = True

        WINDOW.fill(DARK_BLUE)
        draw_game_grid(nodes)
        draw_score_board(score)
        draw_next_shape_area(next_shape_nodes, next_shape)
        draw_level_area(level)
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
    pygame.draw.rect(WINDOW, GREY, pygame.Rect(SB_X, SB_Y, SB_WIDTH, SB_HEIGHT), 5)

    # Draw score content
    font = pygame.font.Font("UrbanBlockerSolid.ttf", 38)
    score_text = font.render("Score:", True, WHITE)

    font = pygame.font.Font("Gemstone.ttf", 38)
    score_value = font.render(str(score), True, WHITE)

    text_position = (SB_X + SB_WIDTH // 3, SB_Y + SB_HEIGHT // 2 - 50)
    value_position = (SB_X + SB_WIDTH // 3, SB_Y + SB_HEIGHT // 2)

    WINDOW.blit(score_text, text_position)
    WINDOW.blit(score_value, value_position)


def get_next_shape_grid():
    nodes = []
    row_indicies = NS_WIDTH // NODE_WIDTH
    col_indicies = NS_HEIGHT // NODE_HEIGHT
    for row in range(row_indicies):
        nodes.append([])
        for col in range(col_indicies):
            nodes[row].append(Node(row, col, NODE_WIDTH, NODE_HEIGHT))

        for node in nodes[row]:
            node.x += NS_X - node.width
            node.y += NS_Y - node.height

    return nodes


def draw_next_shape_area(nodes: List[List[Node]], next_shape: Shape) -> None:
    # Draw grid
    for line in nodes:
        for node in line:
            pygame.draw.rect(
                WINDOW, node.color, pygame.Rect(node.x, node.y, node.width, node.height)
            )
    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(NS_X, NS_Y, NS_WIDTH, NS_HEIGHT))

    # Draw shape
    shape = next_shape.get_current_shape()
    for node in shape:
        x_diff = shape[0].x - node.x
        y_diff = shape[0].y - node.y

        pygame.draw.rect(
            WINDOW,
            next_shape.color,
            pygame.Rect(
                NS_X + NODE_WIDTH * 3 - x_diff,
                NS_Y + NODE_HEIGHT * 3 - y_diff,
                node.width,
                node.height,
            ),
        )

        pygame.draw.rect(
            WINDOW,
            BLACK,
            pygame.Rect(
                NS_X + NODE_WIDTH * 3 - x_diff,
                NS_Y + NODE_HEIGHT * 3 - y_diff,
                node.width,
                node.height,
            ),
            1,
        )

    # Draw frame
    pygame.draw.rect(WINDOW, GREY, pygame.Rect(NS_X, NS_Y, NS_WIDTH, NS_HEIGHT), 5)


def draw_level_area(level: int) -> None:
    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(LVL_X, LVL_Y, LVL_WIDTH, LVL_HEIGHT))
    pygame.draw.rect(WINDOW, GREY, pygame.Rect(LVL_X, LVL_Y, LVL_WIDTH, LVL_HEIGHT), 5)

    font = pygame.font.Font("Gemstone.ttf", 38)
    level = font.render(str(level) + " x", True, WHITE)
    position: Tuple[int, int] = (LVL_X + LVL_WIDTH // 3, LVL_Y + LVL_HEIGHT // 3)
    WINDOW.blit(level, position)


if __name__ == "__main__":
    main()
