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
    get_active_node,
    is_movable,
)


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Create new user events
# Add block falling event
block_falling = pygame.USEREVENT + 0
pygame.time.set_timer(block_falling, 100)


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
                pos1, pos2 = active_node.get_pos()
                if moving and nodes[pos1][pos2 + 1].is_empty():
                    new_shape = []
                    for node in current_shape:
                        pos1, pos2 = node.get_pos()
                        next_node = nodes[pos1][pos2 + 1]
                        node.make_empty()
                        new_shape.append(next_node)
                    for node in new_shape:
                        node.make_block()
                    current_shape = new_shape

                    active_node = get_active_node(current_shape)
                else:
                    moving = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_movable(
                    current_shape, nodes, "left"
                ):
                    new_shape = []
                    for node in current_shape:
                        pos1, pos2 = node.get_pos()
                        next_node = nodes[pos1 - 1][pos2]
                        node.make_empty()
                        new_shape.append(next_node)
                    for node in new_shape:
                        node.make_block()
                    current_shape = new_shape

                    active_node = get_active_node(current_shape)

                if event.key == pygame.K_RIGHT and is_movable(
                    current_shape, nodes, "right"
                ):
                    new_shape = []
                    for node in current_shape:
                        pos1, pos2 = node.get_pos()
                        next_node = nodes[pos1 + 1][pos2]
                        node.make_empty()
                        new_shape.append(next_node)
                    for node in new_shape:
                        node.make_block()
                    current_shape = new_shape

                    active_node = get_active_node(current_shape)

        if not moving:
            check_lines(rows)
            current_shape = create_shape(nodes)
            active_node = get_active_node(current_shape)
            moving = True

        if check_end(nodes):
            running = False

        WINDOW.fill(DARK_BLUE)
        draw_game_grid(nodes)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def get_game_grid() -> list:
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
