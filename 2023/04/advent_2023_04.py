#!/usr/bin/python3

import time

start_time = time.time()

from collections import deque

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

for line in lines:
    _, numbers = line.split(':')
    winner, ours = numbers.split('|')
    ws = set(winner.split())
    os = set(ours.split())
    matches = ws & os
    if matches:
        answer_a += 2 ** (len(matches) - 1)

print('ANSWER Part A -> ', answer_a)


#########################
###      PART B      ####
#########################

answer_b = 0
d = {}
q = deque()

for line in lines:
    cid, numbers = line.split(':')
    cid = int(cid[4:])
    winner, ours = numbers.split('|')
    ws = set(winner.split())
    os = set(ours.split())
    matches = ws & os
    d[cid] = len(matches)
    q.append(cid)

while q:
    answer_b += 1
    k = q.popleft()
    q.extend(range(k + 1, k + d[k] + 1))

print('ANSWER Part B ->', answer_b)


end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")