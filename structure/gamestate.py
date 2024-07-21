from structure.car import Car


class GameState:
    def __init__(self, cars, num_rows, num_cols):
        self.cars = cars
        self.num_rows = num_rows
        self.num_cols = num_cols

    def __eq__(self, other):
        # compare each car's attributes for all cars
        return isinstance(other, GameState) \
               and all(c1.row == c2.row and c1.col == c2.col and c1.orientation == c2.orientation
                       for c1, c2 in zip(self.cars, other.cars))

    def __hash__(self):
        # create a hash based on the tuple of all relevant car properties
        return hash(tuple((car.row, car.col, car.orientation, car.length) for car in self.cars))

    def is_goal(self):
        red_car = self.cars[0]

        if red_car.orientation == 'h':
            exit_col = red_car.col + red_car.length

            # the goal is reached when the red car reaches the right boundary
            if exit_col >= self.num_cols - 1:
                return True

        elif red_car.orientation == 'v':
            # the goal is reached when the red car reaches the top boundary
            if red_car.col <= 0:
                return True

        return False

    def heuristic(self):
        """
        The heuristic value is the number of cars blocking the way of the red car to the exit.
        """
        if self.is_goal():
            return 0

        # at least one car is blocking the way
        blocking = 1

        red_car = self.cars[0]

        if red_car.orientation == 'h':
            for car in self.cars:
                if car == red_car or car.col < red_car.col:
                    continue

                # both cars are on the same row
                if car.orientation == 'h' and car.row == red_car.row:
                    blocking += 1
                    continue

                # the vertically oriented car intersects with the red car's path
                elif car.orientation == 'v' and red_car.row in interval(car.row, car.length):
                    blocking += 1

        elif red_car.orientation == 'v':
            for car in self.cars:
                if car == red_car or car.row > red_car.row + red_car.length:
                    continue

                # both cars are on the same column
                if car.orientation == 'v' and car.col == red_car.col:
                    blocking += 1

                # the horizontally oriented car intersects with the red car's path
                elif car.orientation == 'h' and red_car.col in interval(car.col, car.length):
                    blocking += 1

        return blocking

    def max_up(self, car):
        """
        This function calculates the maximum number of spaces the given car can move upwards.
        """

        # car is on the first row
        if car.row == 0:
            return 0

        free_spaces = set()

        for other_car in self.cars:
            if other_car == car:
                # skip the car itself
                continue

            if other_car.orientation == 'h' and car.col in interval(other_car.col, other_car.length):
                # other_car is in the way at some point; could be above or below the car
                if other_car.row < car.row:
                    # other_car is above the car
                    free_spaces.add(car.row - (other_car.row + 1))

            elif other_car.orientation == 'v' and other_car.col == car.col:
                # other_car is in the way at some point; could be over or under the car
                if other_car.row + other_car.length < car.row:
                    # other_car is above the car
                    free_spaces.add(car.row - (other_car.row + other_car.length))

        if free_spaces:
            moves = min(free_spaces)
            return moves

        else:
            # if no cars are blocking the way, the car can move up to the first row
            return car.row

    def max_down(self, car):
        """This function calculates the maximum number of spaces the given car can move downwards."""

        if car.row + car.length == self.num_rows:
            # the car is at the bottom of the grid
            return 0

        free_spaces = set()
        for other_car in self.cars:
            if other_car == car:
                # skip the car itself
                continue

            if other_car.orientation == 'h' and car.col in interval(other_car.col, other_car.length):
                # other_car is in the way at some point; could be above or below the car
                if other_car.row >= car.row + car.length:
                    # other_car is below the car
                    free_spaces.add((other_car.row - (car.row + car.length)))

            elif other_car.orientation == 'v' and other_car.col == car.col:
                if other_car.row > car.row:
                    # other_car is below the car
                    free_spaces.add((other_car.row - (car.row + car.length)))

        if free_spaces:
            moves = min(free_spaces)

        else:
            # if no cars are blocking the way, the car can move down to the last row
            moves = self.num_rows - (car.row + car.length)

        return moves

    def max_right(self, car):
        """
        This function calculates the maximum number of spaces the given car can move to the right.
        """

        if car.col + car.length == self.num_cols:
            # car is at the far right of the grid
            return 0

        free_spaces = set()
        car_front = car.col + car.length

        for other_car in self.cars:
            if other_car == car:
                # skip the car itself
                continue

            if other_car.orientation == 'h' and other_car.row == car.row:
                # both cars are on the same row
                if car_front <= other_car.col:
                    # other_car is to the right of the car
                    free_spaces.add(other_car.col - car_front)

            elif other_car.orientation == 'v' and car.row in interval(other_car.row, other_car.length):
                # other_car is in the way of car at some point
                if other_car.col >= car_front:
                    # other_car is to the right of the car
                    free_spaces.add(other_car.col - car_front)

        if free_spaces:
            moves = min(free_spaces)
            return moves

        else:
            # if no cars are blocking, the car can move right to the last column
            moves = self.num_cols - car_front

        return moves

    def max_left(self, car):
        """
        This function calculates the maximum number of spaces the given car can move to the left.
        """

        if car.col == 0:
            # car is at the far left of the grid
            return 0

        free_spaces = set()

        for other_car in self.cars:
            if other_car == car:
                # skip the car itself
                continue

            if other_car.orientation == 'h' and other_car.row == car.row:
                # other_car is on the same row as the car
                if other_car.col + other_car.length <= car.col:
                    # other_car is to the left of the car
                    free_spaces.add(car.col - (other_car.col + other_car.length))

            elif other_car.orientation == 'v' and car.row in interval(other_car.row, other_car.length):
                # other_car is on the same row as the car
                if other_car.col + 1 <= car.col:
                    # other_car is to the left of the car
                    free_spaces.add(car.col - (other_car.col + 1))

        if free_spaces:
            moves = min(free_spaces)
            return moves

        else:
            # if no cars are blocking the way, the car can move left to the first column
            return car.col

    def go_up(self, car, moves):
        """
        makes a new GameState where the given car moves up by the specified number of moves.
        returns the new GameState.
        """

        car_index = self.cars.index(car)

        # copying the cars in the current state
        new_cars = [Car(c.row, c.col, c.orientation, c.length) for c in self.cars]

        # move the car upwards in the new list of cars
        new_cars[car_index].row -= moves

        # return a new GameState with the new configuration of cars
        return GameState(new_cars, self.num_rows, self.num_cols)

    def go_down(self, car, moves):
        """
        makes a new GameState where the given car moves down by the specified number of moves.
        returns the new GameState.
        """

        car_index = self.cars.index(car)

        # copying the cars in the current state
        new_cars = [Car(c.row, c.col, c.orientation, c.length) for c in self.cars]

        # move the car downwards in the new list of cars
        new_cars[car_index].row += moves

        # return a new GameState with the new configuration of cars
        return GameState(new_cars, self.num_rows, self.num_cols)

    def go_right(self, car, moves):
        """
        makes a new GameState where the given car moves right by the specified number of moves.
        returns the new GameState.
        """

        car_index = self.cars.index(car)

        # copying the cars in the current state
        new_cars = [Car(c.row, c.col, c.orientation, c.length) for c in self.cars]

        # move the car to the right in the new list of cars
        new_cars[car_index].col += moves

        # return a new GameState with the new configuration of cars
        return GameState(new_cars, self.num_rows, self.num_cols)

    def go_left(self, car, moves):
        """
        makes a new GameState where the given car moves left by the specified number of moves.
        returns the new GameState.
        """

        car_index = self.cars.index(car)

        # copying the cars in the current state
        new_cars = [Car(c.row, c.col, c.orientation, c.length) for c in self.cars]

        # move the car to the left in the new list of cars
        new_cars[car_index].col -= moves

        # return a new GameState with the new configuration of cars
        return GameState(new_cars, self.num_rows, self.num_cols)

    def blocked_directions(self, car):
        """
        returns a list of blocked directions.
        """

        blocked_directions = set()

        if car.orientation == 'h':
            # the car is horizontal -> possible directions are :l(left) and r(right)
            if car.col == 0:
                # car is at the far left of the grid
                blocked_directions.add('l')

            if car.front() == self.num_cols-1:
                # car is at the far right of the grid
                blocked_directions.add('r')

            for other_car in self.cars:
                if other_car == car:
                    # skip the car itself
                    continue

                if 'l' in blocked_directions and 'r' in blocked_directions:
                    # if both directions are already blocked, no need to check further
                    break

                if other_car.orientation == 'h' and car.row == other_car.row:
                    # both cars are on the same row
                    if car.col == other_car.front():
                        # the left side of car is overlapping with the right side of other_car
                        blocked_directions.add('l')

                    elif car.front() == other_car.col:
                        # the car's front is overlapping with the start of other_car
                        blocked_directions.add('r')

                elif other_car.orientation == 'v' and car.row in interval(other_car.row, other_car.length):
                    # other car is in the way at some point
                    if car.col == other_car.col + 1:
                        # the start of the car is overlapping with the right side of other_car
                        blocked_directions.add('l')

                    elif car.front() == other_car.col:
                        # the car's front is overlapping with the left side of other_car
                        blocked_directions.add('r')

        elif car.orientation == 'v':

            if car.row == 0:
                # the car is on the first row
                blocked_directions.add('u')

            if car.front() == self.num_rows-1:
                # the car is at the bottom of the grid
                blocked_directions.add('d')

            # the car is vertical -> possible directions are :u(up) and d(down)
            for other_car in self.cars:

                if other_car == car:
                    # skip the car itself
                    continue

                if 'u' in blocked_directions and 'd' in blocked_directions:
                    # if both directions are already blocked, no need to check further
                    break

                if other_car.orientation == 'h' and car.col in interval(other_car.col, other_car.length):
                    # other_car is in the way of the car at some point
                    if car.row == other_car.row + 1:
                        # the top of the car is overlapping with the bottom of other_car
                        blocked_directions.add('u')

                    elif car.front() == other_car.row:
                        # the bottom of the car is overlapping with the top of other_car
                        blocked_directions.add('d')

                if other_car.orientation == 'v' and car.col == other_car.col:
                    # other_car is  in the way of the car at some point
                    if car.row == other_car.front():
                        # the top of the car is overlapping with the bottom of other_car
                        blocked_directions.add('u')

                    elif car.front() == other_car.row:
                        # bottom of the car is overlapping with the top of other_car
                        blocked_directions.add('d')

        return blocked_directions


def interval(start, length):
    """
    returns a set of integers representing the range from start to start + length - 1.
    """
    return set(range(start, start + length))
