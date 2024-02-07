import pygame
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    BLACK,
    DARK_BLUE,
    NODE_HEIGHT,
    NODE_WIDTH,
    NUM_OF_ROWS,
    NUM_OF_COLS,
)
from models import Node
from utils import fall, check_end, create_shape


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Create new user events

# Add block falling event
block_falling = pygame.USEREVENT + 0
pygame.time.set_timer(block_falling, 1000)


def main():
    running = True
    nodes = get_game_grid()
    moved = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == block_falling:
                pos1, pos2 = current_block.get_pos()
                moved = fall(current_block, nodes)
                current_block = nodes[pos1][pos2 + 1]
            if event.type == pygame.KEYDOWN:
                pos1, pos2 = current_block.get_pos()
                if event.key == pygame.K_LEFT:
                    next_block = nodes[pos1 - 1][pos2]
                    if not next_block.is_frame() and not next_block.is_block():
                        current_block.make_empty()
                        current_block = next_block
                        current_block.make_block()
                if event.key == pygame.K_RIGHT:
                    next_block = nodes[pos1 + 1][pos2]
                    if not next_block.is_frame() and not next_block.is_block():
                        current_block.make_empty()
                        current_block = next_block
                        current_block.make_block()
        if not moved:
            current_block = create_shape(nodes)
            moved = True

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


if __name__ == "__main__":
    main()
