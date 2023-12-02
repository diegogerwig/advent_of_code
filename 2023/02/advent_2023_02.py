from collections import defaultdict

# with open("inp_test_a.txt") as f:
#     lines = f.read().split('\n')

# with open("inp_test_b.txt") as f:
#     lines = f.read().split('\n')

with open("inp.txt") as f:
    lines = f.read().split('\n')

answer_a = 0
bads = set()

for line in lines:
    gn, rounds = line.split(':')
    gid = int(gn[5:])

    answer_a += gid

    rounds = rounds.split(';')
    for round in rounds:
        round = [r.strip().split() for r in round.split(',')]
        for k, color in round:
            if color == 'red' and int(k) > 12:
                bads.add(gid)
            if color == 'green' and int(k) > 13:
                bads.add(gid)
            if color == 'blue' and int(k) > 14:
                bads.add(gid)

print('ANSWER Part A -> ', answer_a - sum(bads))

######################################################

answer_b = 0
for line in lines:
    gn, rounds = line.split(':')
    gid = int(gn[5:])

    rounds = rounds.split(';')

    d = defaultdict(int)

    for round in rounds:
        round = [r.strip().split() for r in round.split(',')]
        for k, color in round:
            d[color] = max(d[color], int(k))
    power = d['red'] * d['green'] * d['blue']
    answer_b += power

print('ANSWER Part B -> ', answer_b)