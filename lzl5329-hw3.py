############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Luwei Lei"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
from Queue import PriorityQueue
import itertools
import math

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = []
    temp = []
    for i in range(1, rows*cols):
        if len(temp) < cols:
            temp.append(i)
        else:
            board.append(temp)
            temp =[]
            temp.append(i)
    temp.append(0)
    board.append(temp)
    return TilePuzzle(board)

class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.dimension = [len(board), len(board[0])]
        for row in board:
            if 0 in row:
                self.location = [board.index(row), row.index(0)]

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        row, col = self.location[0], self.location[1]
        if direction == "up" and (row-1) >= 0 :
            self.board[row][col], self.board[row-1][col] = self.board[row-1][col], self.board[row][col]
            self.location = [row-1, col]
            return True
        elif direction =="down" and (row +1) < len(self.board):
            self.board[row][col], self.board[row+1][col] = self.board[row+1][col], self.board[row][col]
            self.location = [row+1, col]
            return True
        elif direction == "left" and (col -1) >= 0:
            self.board[row][col], self.board[row][col-1] = self.board[row][col-1], self.board[row][col]
            self.location = [row, col-1]
            return True
        elif direction == "right" and (col+1) < len(self.board[0]):
            self.board[row][col], self.board[row][col+1] = self.board[row][col+1], self.board[row][col]
            self.location = [row, col+1]
            return True
        else:
            return False

    def scramble(self, num_moves):
        seq = ["up", "down", "left", "right"]
        for i in range(0, num_moves):
            self.perform_move(random.choice(seq))

    def is_solved(self):
        row_d, col_d = self.dimension[0], self.dimension[1]
        board = create_tile_puzzle(row_d, col_d).get_board()
        if self.board == board:
            return True
        else:
            return False

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        seq = ["up", "down", "left", "right"]
        for i in seq:
            newBoard = self.copy()
            if newBoard.perform_move(i):
                yield i, newBoard

    # Required
    def iddfs_helper(self, limit, moves):
        if limit == 0 and self.is_solved():
            yield moves
        elif limit > 0:
            for move, puzzle in self.successors():
                for i in puzzle.iddfs_helper(limit-1, moves+[move]):
                    if i is not None:
                        yield i
        yield None

    def find_solutions_iddfs(self):
        depth = 1
        bool = False
        while not bool:
            for i in self.iddfs_helper(depth, []):
                if i is not None:
                    yield i
                    bool = True
            depth = depth +1

    # Required
    def Manhattan(self):
        distance = 0
        row_d, col_d = self.dimension[0], self.dimension[1]
        #board = create_tile_puzzle(row_d, col_d).get_board()
        for i in range(0, row_d):
            for j in range(0, col_d):
                current = self.board[i][j]
                distance = distance + abs((current -1)//row_d -i) + abs((current -1)%col_d - j)
        return distance

    def find_solution_a_star(self):
        queue = PriorityQueue()

        explored = set()
        gscore = 0
        fscore = self.Manhattan()
        cameFrom = []
        queue.put((fscore, gscore, cameFrom, self))

        while not queue.empty():
            fscore, gscore, cameFrom, current = queue.get()
            explored.add(tuple(tuple(i) for i in current.get_board()))

            if current.is_solved():
                return cameFrom
            for move, puzzle in current.successors():
                if tuple(tuple(i) for i in puzzle.get_board()) not in explored:
                    queue.put((puzzle.Manhattan()+gscore+1, gscore+1, cameFrom + [move], puzzle))

############################################################
# Section 2: Grid Navigation
############################################################
def grid_successors(scene, pos):
    row, col = pos[0], pos[1]

    #up
    if (row-1) >= 0 and not scene[row-1][col]:
        yield (row-1, col)
    #down
    if (row +1) < len(scene) and not scene[row+1][col]:
        yield (row+1, col)
    #left
    if (col -1) >= 0 and not scene[row][col-1]:
        yield (row, col-1)
    #right
    if (col+1) < len(scene[0]) and not scene[row][col+1]:
        yield (row, col+1)
    #up-left
    if (row-1) >= 0 and (col -1) >= 0 and not scene[row-1][col-1]:
        yield (row-1, col-1)
    #up-right
    if (row-1) >= 0 and (col+1) < len(scene[0]) and not scene[row-1][col+1]:
        yield (row-1, col+1)
    #down-right
    if (row +1) < len(scene) and (col+1) < len(scene[0]) and not scene[row+1][col+1]:
        yield (row+1, col+1)
    #down-left
    if (row +1) < len(scene) and (col -1) >= 0 and not scene[row+1][col-1]:
        yield (row+1, col-1)


def Euclidean(start, goal):
    return math.sqrt(math.pow((start[0] - goal[0]),2) + math.pow((start[1] - goal[1]),2))

def find_path(start, goal, scene):
    queue = PriorityQueue()

    explored = set()
    gscore = 0
    fscore = Euclidean(start, goal)
    cameFrom = [start]
    queue.put((fscore, gscore, cameFrom, start))

    while not queue.empty():
        fscore, gscore, cameFrom, current = queue.get()
        explored.add(current)

        if current == goal:
            return cameFrom
        for move in grid_successors(scene, current):
            if move not in explored:
                queue.put((Euclidean(current, goal) + gscore, gscore+1, cameFrom+[move], move))
    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################
def distinct_successors(listOfCell, length):
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

def heuristic(length, listOfCell):
    distance = 0
    for i, value in enumerate(listOfCell):
        if value is not None:
            distance = distance + (length-value-1-i)//2
    return distance

def solve_distinct_disks(length, n):
    initial = [i+1 if i<n else 0 for i in range(0, length)]
    final = [0 if i < length-n else length-i for i in range(0, length)]

    queue = PriorityQueue()

    explored = set()
    gscore = 0
    fscore = heuristic(length, initial)
    cameFrom = []
    queue.put((fscore, gscore, cameFrom, initial))

    while not queue.empty():
        fscore, gscore, cameFrom, current = queue.get()
        explored.add(tuple(current))

        if current == final:
            return cameFrom
        for move, puzzle in distinct_successors(current, length):
            if move not in explored:
                queue.put((heuristic(length, puzzle) + gscore, gscore+1, cameFrom+[move], puzzle))
    return None

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False for i in range(cols)] for j in range(rows)])

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        #self.leaf_count = 0
        self.postion = None

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False for i in range(len(self.board[0]))]] * len(self.board)
        return self.board

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if (row+1) < len(self.board) and not self.board[row+1][col] and not self.board[row][col]:
                return True
            else:
                return False
        else:
            if (col+1) < len(self.board[0]) and not self.board[row][col] and not self.board[row][col+1]:
                return True
            else:
                return False

    def legal_moves(self, vertical):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        if vertical:
            self.board[row][col] = True
            self.board[row+1][col] = True
        else:
            self.board[row][col+1] = True
            self.board[row][col] = True

    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) == 0:
            return True
        else:
            return False

    def copy(self):
        return copy.deepcopy(self)

    def successors(self, vertical):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.is_legal_move(i, j, vertical):
                    newBoard = self.copy()
                    newBoard.perform_move(i, j, vertical)
                    yield (i, j), newBoard

    def get_random_move(self, vertical):
        seq = [self.legal_moves(vertical)]
        return self.perform_move(random.choice(seq))

    def evaluate_board(self, vertical):
        return len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical)))

    # Required
    leaf_count = 0

    def alpha_beta(self, limit, maximizingPlayer, alpha, beta, vertical, origin):
        if limit == 0 or self.game_over(vertical):
             DominoesGame.leaf_count += 1
             return self.evaluate_board(origin)

        if maximizingPlayer:
            bestVal = float("-inf")
            for move, puzzle in self.successors(vertical):
                value = puzzle.alpha_beta(limit-1, False, alpha, beta, not vertical, origin)
                if value > bestVal:
                    bestVal = max(bestVal, value)
                    self.postion = move
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break
                #leaf_count += 1
            return bestVal
        else:
            bestVal = float("inf")
            for move, puzzle in self.successors(vertical):
                value = puzzle.alpha_beta(limit-1, True, alpha, beta, not vertical, origin)
                if value < bestVal:
                    bestVal = min(bestVal, value)
                    self.postion = move
                beta = min(beta, bestVal)
                if beta <= alpha:
                    break
                #leaf_count += 1
            return bestVal


    def get_best_move(self, vertical, limit):
        DominoesGame.leaf_count = 0
        value = self.alpha_beta(limit, True, float("-inf"), float("inf"), vertical, vertical)
        return (self.postion, value, DominoesGame.leaf_count)


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
I spent approximately 15 hrs on this assignment.
"""

feedback_question_2 = """
The iddfs_helper is the most confusing one. But after I read some
pseudo code for iterative deepening DFS online, it became more clear.
"""

feedback_question_3 = """
I liked the suggested structure for each problem. And I liked it repeats
several times so I could be master on it.
"""
