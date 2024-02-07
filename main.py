import pygame
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    RED,
    BLACK,
    DARK_BLUE,
    WHITE,
    NODE_HEIGHT,
    NODE_WIDTH,
    NUM_OF_ROWS,
    NUM_OF_COLS,
)
from models import Node
from utils import fall, check_end

import random


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Create new user events

# Add block falling event
block_falling = pygame.USEREVENT + 0
pygame.time.set_timer(block_falling, 500)

# Add create new blocks event
create_blocks = pygame.USEREVENT + 1
pygame.time.set_timer(create_blocks, 3000)


def main():
    running = True
    nodes = get_game_grid()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == create_blocks:
                create_shape(nodes)
            if event.type == block_falling:
                fall(nodes)

        if check_end(nodes):
            running = False

        WINDOW.fill(DARK_BLUE)
        draw_game_grid(nodes)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def get_game_grid() -> list:
    nodes = []
    for row in range(NUM_OF_ROWS):
        nodes.append([])
        for col in range(NUM_OF_COLS):
            nodes[row].append(Node(row, col, NODE_WIDTH, NODE_HEIGHT))

    frames = (
        nodes[0][:-1]
        + nodes[-1][:-1]
        + [
            node
            for row in nodes
            for node in row
            if row.index(node) == 0 or row.index(node) == NUM_OF_COLS - 1
        ]
    )
    for node in frames:
        node.make_frame()

    return nodes


def draw_game_grid(nodes: list) -> None:
    for row in nodes:
        for node in row:
            pygame.draw.rect(
                WINDOW, node.color, pygame.Rect(node.x, node.y, node.width, node.height)
            )

            pygame.draw.rect(
                WINDOW, BLACK, pygame.Rect(node.x, node.y, node.width, node.height), 1
            )


def create_shape(nodes):
    starting_nodes = [
        node
        for row in nodes
        for node in row
        if nodes.index(row) in range(1, NUM_OF_ROWS - 1) and row.index(node) == 1
    ]

    for node in starting_nodes:
        node.make_block()


if __name__ == "__main__":
    main()
