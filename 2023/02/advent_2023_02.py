#!/usr/bin/env python3

from collections import defaultdict

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
game_wrong = set()

for line in lines:
    game_num, rounds = line.split(':')
    game_id = int(game_num[5:])

    answer_a += game_id

    rounds = rounds.split(';')
    for round in rounds:
        round = [r.strip().split() for r in round.split(',')]
        for k, color in round:
            if color == 'red' and int(k) > 12:
                game_wrong.add(game_id)
            if color == 'green' and int(k) > 13:
                game_wrong.add(game_id)
            if color == 'blue' and int(k) > 14:
                game_wrong.add(game_id)

print('ANSWER Part A -> ', answer_a - sum(game_wrong))


#########################
###      PART B     ####
#########################

answer_b = 0

for line in lines:
    game_num, rounds = line.split(':')
    game_id = int(game_num[5:])

    rounds = rounds.split(';')

    d = defaultdict(int)

    for round in rounds:
        round = [r.strip().split() for r in round.split(',')]
        for k, color in round:
            d[color] = max(d[color], int(k))
    power = d['red'] * d['green'] * d['blue']
    answer_b += power

print('ANSWER Part B -> ', answer_b)