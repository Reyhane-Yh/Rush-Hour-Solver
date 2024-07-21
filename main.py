from structure.gamestate import GameState
from structure.get_inp import get_data
from structure.search import a_star


def main():
    parking_areas = get_data()

    for i, (cars, rows, columns) in enumerate(parking_areas):
        initial_state = GameState(cars, rows, columns)

        print(f"Test #{i + 1}: ", end="")
        sol = a_star(initial_state)
        if sol:
            solution_path, moves = sol
            moves_num = 0
            for state, move in zip(solution_path, moves):
                if move:
                    moves_num += 1
                    # uncomment these lines if you want to see the moves taken at each state
                    # print(move)

            print(moves_num)
            # print("".join(["-"] * 50))
        else:
            print("No solution found.")


if __name__ == "__main__":
    main()
