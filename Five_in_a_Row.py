
# Five in a Row
# 15 x 15
# 0: Selectable Blank, 1: Non Seletable Blank 2: Black, 3: White

class OutOfIndexError(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('Size of array is 15 x 15 (0 - 14)')
        
class CanNotSelectError(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('Can not set in this position')
        
array = [ [ 0 for i in range(15) ] for j in range(15)]
for element in array:
        print(element)      
     
isWhiteTurn = False

while True:
    isCorrect = False
    while isCorrect == False:
        try:
            row, col = input("Input(row, col): ").split()
            row = int(row)
            col = int(col)
            if not(0 <=row and row <= 14) and not(0 <= col and col <= 14):
                raise OutOfIndexError
            if array[row][col] == 2 or array[row][col] == 3:
                raise CanNotSelectError
            if isCorrect == False and array[row][col] == 1:
                raise CanNotSelectError
            isCorrect = True
        except Exception as e:
            print("[Exception]", e)

    userIndex = isWhiteTurn + 2
    print(userIndex)
    array[row][col] = userIndex
    
    for element in array:
        print(element)

    for arrayRow in array:
        for value in arrayRow:
            if value == 0:
                _ = 0
                # To Do...
    
    isWhiteTurn = not isWhiteTurn

def detect_unselectable_point(point):
    is_unselectable_point(point)

def is_unselectable_point(point):
    return

