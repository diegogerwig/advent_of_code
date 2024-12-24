from collections import defaultdict, deque

values = [item.strip() for item in open('input.txt').read().split('\n\n')]
registers = defaultdict(int)
all_vals = []

for item in values[1].split('\n'):
    a, _, b, _, c = item.split()
    all_vals.append(a)
    all_vals.append(b)
    all_vals.append(c)
print(all_vals)

for item in values[1].split('\n'):
    a, op, b, _, c = item.split()
    if (a[0] == 'x' or a[0] == 'y') and (b[0] == 'x' or b[0] == 'y'):
        if op == 'XOR':
            print(a, op, b, c)
            print(all_vals.count(c))
        if op == 'OR':
            print(a, op, b, c)
            print(all_vals.count(c))