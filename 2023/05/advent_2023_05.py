#!/usr/bin/python3

import time

start_time = time.time()

from collections import defaultdict

# with open("inp_test_a.txt") as f:
#     lines = f.read().split('\n')
#     lines = [line for line in lines if line]

with open("inp_test_b.txt") as f:
    lines = f.read().split('\n')
    lines = [line for line in lines if line]

# with open("inp.txt") as f:
#     lines = f.read().split('\n')
#     lines = [line for line in lines if line]


#########################
###      PART A      ####
#########################

answer_a = 0

d = defaultdict(dict)

seeds = [int(k) for k in lines[0][7:].split()]
for line in lines[1:]:
    if 'map' in line:
        src, _, dst = line[:-5].split('-')
        continue

    dst_base, src_base, lenght = [int(k) for k in line.split()]
    d[src][src_base] = (dst_base, lenght)


def _get_mapping(value, resource):
    mappings = sorted(d[resource].items())
    for src, (dst, l) in mappings:
        if value >= src and value < src + l:
            return dst + value - src
    return value


answer_a = float('inf')
for seed in seeds:
    soil = _get_mapping(seed, 'seed')
    fertilizer = _get_mapping(soil, 'soil')
    water = _get_mapping(fertilizer, 'fertilizer')
    light = _get_mapping(water, 'water')
    temperature = _get_mapping(light, 'light')
    humidity = _get_mapping(temperature, 'temperature')
    location = _get_mapping(humidity, 'humidity')
    answer_a = min(answer_a, location)

print('ANSWER Part A ->', answer_a)


#########################
###      PART B      ####
#########################

answer_b = 0



print('ANSWER Part B ->', answer_b)


end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")