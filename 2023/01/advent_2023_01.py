from string import digits

# with open("inp_test_a.txt") as f:
#     lines = f.read().split("\n")

# with open("inp_test_b.txt") as f:
#     lines = f.read().split("\n")

with open("inp.txt") as f:
    lines = f.read().split("\n")

answer_a = 0

for line in lines:
    tmp = ""
    for i in line:
        if i in digits:
            tmp += i
            break
    for i in line[::-1]:
        if i in digits:
            tmp += i
            break
    answer_a += int(tmp)

print('ANSWER Part A -> ', answer_a)

######################################################

answer_b = 0
spelled = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

for line in lines:
    numbers = []
    for d in digits:
        idx = line.find(d)
        if idx != -1:
            numbers.append((idx, d))
        idx = line.rfind(d)
        if idx != -1:
            numbers.append((idx, d))
    for d, v in spelled.items():
        idx = line.find(d)
        if idx != -1:
            numbers.append((idx, v))
        idx = line.rfind(d)
        if idx != -1:
            numbers.append((idx, v))

    numbers.sort()
    answer_b += int(f"{numbers[0][1]}{numbers[-1][1]}")

print('ANSWER Part B -> ', answer_b)
