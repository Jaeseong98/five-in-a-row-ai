MAX_SIZE = 15

class GameBoard(object):
    array = list()
    turn = True

    def __init__(self):
        self.array = [
            [
                0 for i in range(MAX_SIZE)
            ] for j in range(MAX_SIZE)
        ]
