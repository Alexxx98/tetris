def fall(nodes: list) -> None:
    blocks = [node for row in nodes for node in row if node.is_block()]

    for node in blocks:
        node_pos = node.get_pos()
        next_node = nodes[node_pos[0]][node_pos[1] + 1]
        if not next_node.is_block() and not next_node.is_frame():
            node.make_empty()
            next_node.make_block()


def check_end(nodes: list) -> None:
    counter = 0
    for row in nodes:
        for node in row:
            if node.is_empty():
                counter += 1

    if counter == 0:
        return True
    return False
