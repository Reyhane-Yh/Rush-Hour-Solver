from structure.gamestate import GameState


class Node:
    def __init__(self, state, depth, came_from=None, move=None):
        self.state = state
        self.depth = depth
        self.came_from = came_from
        self.move = move

    def priority(self):
        return self.depth + self.state.heuristic()

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state and self.priority() == other.priority()

    def __lt__(self, other):
        return self.priority() < other.priority()

    def generate_successor(self):
        successors = []

        for car in self.state.cars:

            car_idx = self.state.cars.index(car)

            # move up if not blocked
            if car.orientation == 'v':
                blocked_dirs = self.state.blocked_directions(car)

                if 'u' not in blocked_dirs:
                    moves = GameState.max_up(self.state, car)

                    if moves > 0:
                        new_state_up = self.state.go_up(car, moves)

                        if new_state_up:
                            move = f"Car {car_idx} at ({car.row}, {car.col}) moved up {moves} spaces."
                            successors.append(Node(new_state_up, self.depth + 1, self, move))

                # move down if not blocked
                if 'd' not in blocked_dirs:
                    moves = GameState.max_down(self.state, car)
                    if moves > 0:
                        new_state_down = self.state.go_down(car, moves)
                        if new_state_down:
                            move = f"Car {car_idx} at ({car.row}, {car.col}) moved down {moves} spaces."
                            successors.append(Node(new_state_down, self.depth + 1, self, move))

            elif car.orientation == 'h':
                blocked_dirs = self.state.blocked_directions(car)

                # move left if not blocked
                if 'l' not in blocked_dirs:
                    moves = GameState.max_left(self.state, car)
                    if moves > 0:
                        new_state_left = self.state.go_left(car, moves)
                        if new_state_left:
                            move = f"Car {car_idx} at ({car.row}, {car.col}) moved left {moves} spaces."
                            successors.append(Node(new_state_left, self.depth + 1, self, move))

                # move right if not blocked
                if 'r' not in blocked_dirs:
                    moves = GameState.max_right(self.state, car)
                    if moves > 0:
                        new_state_right = self.state.go_right(car, moves)
                        if new_state_right:
                            move = f"Car {car_idx} at ({car.row}, {car.col}) moved right {moves} spaces."
                            successors.append(Node(new_state_right, self.depth + 1, self, move))

        return successors

    def reconstruct_path(self):
        """
        Reconstructs the path from the initial state to the current state.

        Returns:
        tuple: A tuple containing the path of states and the moves taken.
        """

        path = []
        moves = []
        current = self

        while current:
            path.append(current.state)
            moves.append(current.move)
            # move to the previous node in the path
            current = current.came_from

        path.reverse()
        moves.reverse()
        return path, moves
