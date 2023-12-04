#!/usr/bin/python3

from collections import defaultdict
from string import digits

# with open("inp_test_a.txt") as f:
#     lines = f.read().split('\n')

# with open("inp_test_b.txt") as f:
#     lines = f.read().split('\n')

with open("inp.txt") as f:
    lines = f.read().split('\n')


#########################
###      PART A      ####
#########################

answer_a = 0
sd = defaultdict(bool)
symbols = {'#', '$', '%', '&', '*', '+', '-', '/', '=', '@'}

for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c in symbols:
            sd[(i, j)] = True

seen = set()
k = ''
pos = []

def _check_adjacencies():
    adjs = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ]
    for x, y in pos:
        for a, b in adjs:
            if (x + a, y + b) in sd:
                return int(k)

    return 0

for i, line in enumerate(lines):
    if k:
        answer_a += _check_adjacencies()
        k = ''
        pos = []
    for j, c in enumerate(line):
        if c in symbols or c == '.':
            answer_a += _check_adjacencies()
            k = ''
            pos = []
        if c in digits:
            k += c
            pos.append((i, j))

print('ANSWER Part A -> ', answer_a)


#########################
###      PART B      ####
#########################

answer_b = 0
sd = defaultdict(bool)
gears = []
numbers = []

for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == '*':
            gears.append((i, j))

seen = set()
k = ''
pos = []

for i, line in enumerate(lines):
    if k:
        numbers.append((k, list(pos)))
        k = ''
        pos = []
    for j, c in enumerate(line):
        if k and c not in digits:
            numbers.append((k, list(pos)))
            k = ''
            pos = []
        if c in digits:
            k += c
            pos.append((i, j))

def _check_adjacencies(xg, yg):
    tmp = []
    adjs = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ]
    for number, positions in numbers:
        for a, b in adjs:
            if (xg + a, yg + b) in positions:
                tmp.append(int(number))
                break
    return tmp

for gear in gears:
    x = _check_adjacencies(*gear)
    if len(x) == 2:
        answer_b += (x[0] * x[1])

print('ANSWER Part B -> ', answer_b)