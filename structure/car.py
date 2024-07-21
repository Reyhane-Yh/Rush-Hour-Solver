class Car:
    def __init__(self, row, col, orientation, length):
        self.row = row
        self.col = col
        self.orientation = orientation
        self.length = length

    def front(self):
        """ returns the opposite end of the car."""
        if self.orientation == 'v':
            return self.row + self.length
        else:
            return self.col + self.length
