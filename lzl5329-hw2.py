############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Luwei Lei"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
import math
from collections import deque

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    f = math.factorial
    return f(n*n) / f(n) / f(n*n-n)

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):
    result = [x for x in board if board.count(x) > 1]
    if len(result) != 0:
        return False
    for i in range(0, len(board)):
        leftlist = board[0:i]
        rightlist = board[i+1:]
        difference = 0
        for j in leftlist[::-1]:
            difference = difference + 1
            if abs(board[i] - j) == difference:
                return False
        difference = 0
        for j in rightlist:
            difference = difference + 1
            if abs(board[i] - j) == difference:
                return False
    return True


def n_queens_helper(n, board):
    if len(board) == n:
        newBoard.append(board)
    else:
        for i in range(0, n):
            if n_queens_valid(board + [i]):
                n_queens_helper(n, board + [i])

def n_queens_solutions(n):
    global newBoard
    newBoard = []
    n_queens_helper(n, [])
    result = (i for i in newBoard)
    return result

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = list(board)

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if (row-1) >= 0:
            self.board[row-1][col] = not self.board[row-1][col]
        if (row +1) < len(self.board):
            self.board[row+1][col] = not self.board[row+1][col]
        if (col -1) >= 0:
            self.board[row][col-1] = not self.board[row][col-1]
        if (col+1) < len(self.board[0]):
            self.board[row][col+1] = not self.board[row][col+1]
        return self.board

    def scramble(self):
        for row in range(0, len(self.board) ):
            for col in range(0, len(self.board[row])):
                value = random.random() < 0.5
                if value == True:
                    self.perform_move(row, col)
        return self.board

    def is_solved(self):
        return (not any(x for y in self.board for x in y))

    def copy(self):
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                newBoard = self.copy()
                newBoard.perform_move(row, col)
                yield (row, col), newBoard

    def find_solution(self):
        explored = set()
        path = []
        layer = deque([(path,self)])
        boards = []

        while len(layer) > 0:
            current = layer.popleft()
            currentPath = current[0]
            currentPuzzle = current[1]
            currentPuzzleBoard = currentPuzzle.get_board()
            explored.add(tuple(tuple(i) for i in currentPuzzleBoard))
            for move, puzzle in currentPuzzle.successors():
                path = currentPath + [move]
                if (puzzle.is_solved() == True):
                    return path
                puzzleBoard = puzzle.get_board()
                newBoard = tuple(tuple(i) for i in puzzleBoard)
                if newBoard not in explored and puzzleBoard not in boards:
                    layer.append((path, puzzle))
                    boards.append(puzzleBoard)
        return None

def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for i in range(cols)]] * rows)

############################################################
# Section 3: Linear Disk Movement
############################################################

def is_identical_solved(listOfCell ,l, n):
    start = all(i == listOfCell[0] for i in listOfCell[l-n:])
    end = all(i == listOfCell[-1] for i in listOfCell[:l-n])
    if start and not end:
        return True
    return False

def successors(listOfCell , length):
    for i in range(0, length):
        temp = copy.deepcopy(listOfCell)
        if i+1 < length and listOfCell[i] == 1 and listOfCell[i+1] == 0:
            listOfCell[i], listOfCell[i+1] = listOfCell[i+1], listOfCell[i]
            yield ((i, i+1), listOfCell)
            listOfCell = copy.deepcopy(temp)

        if i+2 < length and listOfCell[i] == 1 and listOfCell[i+1] == 1 and listOfCell[i+2] == 0:
            listOfCell[i], listOfCell[i+2] = listOfCell[i+2], listOfCell[i]
            yield ((i, i+2), listOfCell)
            listOfCell = copy.deepcopy(temp)


def solve_identical_disks(length, n):
    initial = [1 if i < n else 0 for i in range(0, length)]
    final = [0 if i < length - n else 1 for i in range(0, length)]

    path = []
    explored = set()
    frontier = deque([(path, initial)])
    existing_path = set()

    while len(frontier) > 0:
        current = frontier.popleft()
        currentPath = current[0]
        currentPuzzle = current[1]
        explored.add(tuple(currentPuzzle))

        for move, puzzle in successors(currentPuzzle, length):
            path = currentPath + [move]
            if initial == final:
                return path
            newlist = tuple(puzzle)
            if newlist not in explored and newlist not in existing_path:
                frontier.append((path, puzzle))
                existing_path.add(newlist)
    return None



def distinct_successors(listOfCell , length):
    for i in range(0, length):
        temp = copy.deepcopy(listOfCell)
        if i+1 < length and temp[i+1] == 0:
            temp[i], temp[i+1] = temp[i+1], temp[i]
            yield ((i, i+1), temp)
            temp = copy.deepcopy(listOfCell)

        if i-1 >= 0 and temp[i-1] == 0:
            temp[i-1], temp[i] = temp[i], temp[i-1]
            yield ((i, i-1), temp)
            temp = copy.deepcopy(listOfCell)

        if i+2 < length and temp[i+1] != 0 and listOfCell[i+2] == 0:
            temp[i], temp[i+2] = temp[i+2], temp[i]
            yield ((i, i+2), temp)
            temp = copy.deepcopy(listOfCell)

        if i-2 >= 0 and temp[i-1] != 0 and temp[i-2] ==0:
            temp[i-2], temp[i] = temp[i], temp[i-2]
            yield ((i, i-2), temp)
            temp = copy.deepcopy(listOfCell)


def solve_distinct_disks(length, n):
    initial = [i+1 if i<n else 0 for i in range(0, length)]
    final = [0 if i < length-n else length-i for i in range(0, length)]
    path = []
    explored = set()
    frontier = deque([(path, initial)])
    existing_path = set()

    while frontier:
        current = frontier.popleft()
        currentPath = current[0]
        currentPuzzle = current[1]
        explored.add(tuple(currentPuzzle))
        for move, puzzle in distinct_successors(currentPuzzle, length):
            path = currentPath + [move]
            if (puzzle == final):
                return path
            newlist = tuple(puzzle)
            if newlist not in explored and newlist not in existing_path:
                frontier.append((path, puzzle))
                existing_path.add(newlist)
    return None


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
I spent almost 19 hours on this assignment.
"""

feedback_question_2 = """
Implement the recursive call with help function was challenging to me.
"""

feedback_question_3 = """
If the problems could be shorter, that will be nice.
"""
