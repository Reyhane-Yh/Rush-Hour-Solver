from structure.car import Car


def get_data():
    t = int(input())

    parking_areas = []

    for i in range(t):

        n, m, v = map(int, input().split())

        cars = []
        for j in range(v):
            row, column, orientation, length = input().split()
            row = int(row) - 1
            column = int(column) - 1
            length = int(length)
            cars.append(Car(row, column, orientation, length))

        parking_areas.append((cars, n, m))

    return parking_areas
