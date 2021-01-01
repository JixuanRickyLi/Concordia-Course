class Node:
    """
    A small class to house the common properties related to a node in our state tree.
    """

    def __init__(self, node_state, parent_node, total_cost_from_root, move_to_get_here_from_parent,
                 move_cost, moved_tile, heuristic_value=0, f_value=0):
        """
        Define the node object.
        :param node_state: The state that this node contains.
        :param parent_node: The state of the parent node.
        :param total_cost_from_root: The total cost to get to this node from the root g(n).
        :param move_to_get_here_from_parent: The type of move that was taken to reach this node.
        :param move_cost: The cost of the move.
        :param moved_tile: The tile that was moved to get to this state.
        :param heuristic_value: The heuristic h(n) value attached to this node.
        :param f_value: The f(n) value attached to this node.
        """
        self.state = node_state
        self.parent_node = parent_node
        self.cost = total_cost_from_root            # g(n)
        self.move = move_to_get_here_from_parent
        self.move_cost = move_cost
        self.moved_tile = moved_tile
        self.heuristic_value = heuristic_value      # h(n)
        self.f_value = f_value                      # f(n)
    # end: __init__
# end: class Node
