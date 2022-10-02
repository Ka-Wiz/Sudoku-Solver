import math
import tkinter.filedialog
import random


class Square:
    row = None
    col = None
    val = None

    poss = None  # state data for search

    def __init__(self, r, c, v):
        self.row = r
        self.col = c
        self.val = v

    def getpossible(self):
        self.poss = [hex(h)[2].upper() for h in range(size)]
        self.poss.reverse()

        # if mrv == 'random': random.shuffle(self.poss)

        for other in puzzle[self.row]:
            self.remposs(other)

        for other in [row[self.col] for row in puzzle]:
            self.remposs(other)

        prow = math.floor(self.row/dim)
        pcol = math.floor(self.col/dim)
        for other in [sqr for row in puzzle[prow * dim:prow * dim + dim] for sqr in row[pcol * dim:pcol * dim + dim]]:
            self.remposs(other)

        return self.poss

    def remposs(self, other):
        if other.val != '-' and other.val in self.poss:
            self.poss.remove(other.val)


def getnextvar():
    if mrv == 'y':
        # get unassigned variable with fewest possibilities
        return sorted([v for v in variables if v not in workvars], key=lambda v: len(v.getpossible()))[0]
    elif mrv == 'random':
        return random.choice([v for v in variables if v not in workvars])
    else:
        return variables[len(workvars)]  # vars already stored left->right top->bot


def printpuzzle():
    for r, row in enumerate(puzzle):
        if r % dim == 0: print('-------------------------------------------------')
        print(' | '.join('  '.join(s.val for s in ps) for ps in [row[i*dim:i*dim+dim] for i in range(dim)]))
    print()


file = None
while file is None:
    file = tkinter.filedialog.askopenfile(mode='r')

puzzle = [[Square(row, col, val) for col, val in enumerate(trow)] for row, trow in enumerate(file.read().split('\n'))]
variables = [sqr for row in puzzle for sqr in row if sqr.val == '-']
size = len(puzzle)
dim = int(math.sqrt(size))

print("\nHi! Welcome to Sudoku Solver '98. Your puzzle is:")
printpuzzle()

mrv = input("Solving, use MRV? y\\n\\random: ")
trace = input("Show trace? y\\n: ")

workvars = []  # stack for current path
assignments = 0

while len(workvars) != len(variables):
    curv = getnextvar()
    curv.getpossible()

    while len(curv.poss) == 0:
        if trace == 'y': print(f"no poss for {curv.row},{curv.col}, backtracking")
        curv.val = '-'
        curv = workvars.pop()

    if trace == 'y': print(f"{curv.row},{curv.col} trying next poss, out of {[p for p in reversed(curv.poss)]}")
    curv.val = curv.poss.pop()
    assignments += 1
    workvars.append(curv)

print(f"\ncompleted with {assignments} assignments tried from {len(variables)} variables!")
printpuzzle()
