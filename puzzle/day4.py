#!/usr/bin/env python3

import sys

LARGE_NUMBER = 100000

class Board:
    def __init__(self, values):
        # values is a list of N strings of M space-seperated numbers
        self.values=[]
        for val_string in values:
            self.values.append([int(x) for x in val_string.split()])
        self.row_scores=[0] * len(self.values)
        self.col_scores=[0] * len(self.values[0])
    def add_num(self, num):
        for row in range(len(self.row_scores)):
            for col in range(len(self.col_scores)):
                if num == self.values[row][col]:
                    self.values[row][col] = LARGE_NUMBER # for scoring; can't use 0 as that is a valid number
                    self.row_scores[row]+=1
                    self.col_scores[col]+=1
                    return (self.row_scores[row] == len(self.row_scores) or self.col_scores[col] == len(self.col_scores))
        return False
    def get_score(self):
        score = 0
        for value_row in self.values:
            score += sum(value_row)
        return score % LARGE_NUMBER

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

scoring_values = None
board_array = []
boards = []
with open(sys.argv[1]) as file:
    for line in file:
        if scoring_values is None:
            scoring_values = [int(x) for x in line.rstrip().split(",")]
        elif line.rstrip() != "":
            board_array.append(line.rstrip())
        elif len(board_array) > 0:
            boards.append(Board(board_array))
            board_array = []
if len(board_array) > 0:
            boards.append(Board(board_array))

to_remove = []
for value in scoring_values:
    if len(to_remove) > 0:
        for board in to_remove:
            boards.remove(board)        
        to_remove = []
    for board in boards:
        if board.add_num(value):
            print("Board wins: score {}, value {}, total {}".format(board.get_score(), value, board.get_score()*value))
            to_remove.append(board)