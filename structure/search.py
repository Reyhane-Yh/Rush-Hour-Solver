import heapq
from structure.node import Node


def a_star(initial_state):
    """
    Performs the A* search algorithm to find the shortest path to the goal state.

    Parameters:
    initial_state (GameState): The initial state of the game.

    Returns:
    list: The path to the goal state if found, otherwise None.
    """

    # initialize the priority queue with the starting node
    start_node = Node(initial_state, 0)
    open_set = []
    heapq.heappush(open_set, start_node)

    # use a dictionary to track the lowest cost to each visited state
    visited = {}

    while open_set:
        # get the node with the lowest cost from the priority queue
        current_node = heapq.heappop(open_set)

        # check if the current state is the goal state
        if current_node.state.is_goal():
            return current_node.reconstruct_path()

        # update the visited dictionary with the current node
        if current_node.state not in visited or visited[current_node.state] > current_node.depth:
            visited[current_node.state] = current_node.depth

            # generate successors for the current state
            for successor in current_node.generate_successor():
                new_cost = successor.depth
                if successor.state not in visited or visited[successor.state] > new_cost:
                    heapq.heappush(open_set, successor)

    # if no solution is found
    return None
