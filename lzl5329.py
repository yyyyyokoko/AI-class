############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Luwei Lei"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
import Queue

############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    list = []
    for row in range(0,9):
        for col in range(0,9):
            list.append((row, col))
    return list

def sudoku_arcs():
    arcs = []
    cells = sudoku_cells()
    for i in cells:
        for j in cells:
            if i == j:
                continue
            elif i[0] == j[0]:
                arcs.append((i,j))
            elif i[1] == j[1]:
                arcs.append((i, j))
            elif i[0]/3 == j[0]/3 and i[1]/3 == j[1]/3:
                arcs.append((i,j))
    return arcs

def read_board(path):
    f = open(path, "r").read().split()
    board =[]
    line = []
    for i in f:
        for j in i:
            if j == '*':
                line.append(set([1,2,3,4,5,6,7,8,9]))
            else:
                line.append(set([int(j)]))
                #line.append(int(j))
        board.append(line)
        line = []
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        row, col = cell[0], cell[1]
        return self.board[row][col]

    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1, cell2) in self.ARCS:
            value1 = self.board[cell1[0]][cell1[1]]
            value2 = self.board[cell2[0]][cell2[1]]
            if len(value1) > 1 and len(value2) == 1 and list(value2)[0] in value1:
                value1.remove(list(value2)[0])
                #self.board[cell1[0]][cell1[1]].remove(value)
                self.board[cell1[0]][cell1[1]] = value1
                return True
        else:
            return False

    def infer_ac3(self):
        queue = copy.deepcopy(self.ARCS)
        while queue:
            (x, y) = queue.pop(0)
            if self.remove_inconsistent_values(x,y):
                for i in self.ARCS:
                    if i[1]== x and i[0]!=y:
                        queue.append(i)

    def unique_val(self, cell, val):
        count1=0
        count2=0
        count3=0

        for (i, j) in self.ARCS:
            if cell == i and cell[0] == j[0]:
                if val in self.board[j[0]][j[1]]:
                    count1 = count1 +1
            if cell == i and cell[1] == j[1]:
                if val in self.board[j[0]][j[1]]:
                    count2 = count2 +1
            if cell == i and cell[0]/3 == j[0]/3 and cell[1]/3 == j[1]/3:
                if val in self.board[j[0]][j[1]]:
                    count3 = count3 +1
        if count1>0 and count2>0 and count3>0:
            return False
        else:
            return True

    def infer_improved(self):
        self.infer_ac3()
        a = copy.deepcopy(self.board)
        for (x,y) in self.CELLS:
            if len(self.board[x][y]) > 1:
                for val in self.board[x][y]:
                    if self.unique_val((x, y), val):
                        self.board[x][y] = set([val])
                        break
        self.infer_ac3()
        if a == self.board:
            return
        else:
            self.infer_improved()


    def is_solved(self):
        for i in self.CELLS:
            if len(list(self.board[i[0]][i[1]])) != 1:
                return False
            for (cell1, cell2) in self.ARCS:
                value1 = self.board[cell1[0]][cell1[1]]
                value2 = self.board[cell2[0]][cell2[1]]
                if i == cell1 and value1 == value2:
                    return False
        return True

    def infer_with_guessing(self):
        #self.infer_improved()
        #newBoard = copy.deepcopy(self)
        queue = Queue.LifoQueue()
        queue.put(copy.deepcopy(self))
        while queue:
            newBoard = queue.get()
            newBoard.infer_improved()
            if newBoard.is_solved():
                return newBoard
            for (i, j) in self.CELLS:
                if len(newBoard.board[i][j]) >1:
                    for guess in list(newBoard.board[i][j]):
                        successor = copy.deepcopy(newBoard)
                        successor.board[i][j] = set([guess])
                        successor.infer_improved()
                        if not successor.is_solved():
                            queue.put(successor)
                        else:
                            self.board = successor.board
                            return

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent about 15 hours on this assignment.
"""

feedback_question_2 = """
Figuring out the logic of the code was most difficult.
I spent a lot of time on infer_improved() because I had a logical error.
"""

feedback_question_3 = """
I think this homework is fair. It would be nice that we are provided a solution checker.
"""
