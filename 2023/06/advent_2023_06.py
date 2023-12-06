#!/usr/bin/python3

import time
import pathlib
import os
import math
from colorama import init, Fore
init(autoreset=True)

def parse_data(puzzle_input):
    part1 = [
        [int(num) for num in line.split()[1:]] for line in puzzle_input.split("\n")
    ]
    part2 = tuple(
        int(line.split(":")[1].replace(" ", "")) for line in puzzle_input.split("\n")
    )

    return list(zip(*part1)), part2

def part1(data):
    records, _ = data
    return math.prod(find_num_records(time, distance) for time, distance in records)

def part2(data):
    _, (time, distance) = data
    return find_num_records(time, distance)

def find_num_records(time, distance):
    """Find the number of records.
    The boat runs a speed of t for (T - t) seconds where T = time, resulting in
    a distance of t * (T - t). The formula d(t) = t * (T - t) = Tt - t² is zero
    at 0 and T and symmetric between.
    Use a binary search to find the smallest t such that d(t) > distance. During
    the search, low will always be less than t while high will always be greater
    than or equal than t. At the end of the search, high represents the smallest
    t such that d(t) > distance.
    We want the number of records. If first is the smallest t such that d(t) >
    distance and last is the greatest t such that d(t) > distance, then the
    number of records is (last - first + 1). Because of symmetry last = time / 2
    + time / 2 - first = time - first. The number of records can therefore be
    calculated as (last - first + 1) = time - 2*first + 1.
    ## Example:
    >>> find_num_records(8, 12)
    3
    """

    low, high = 0, time // 2

    while low + 1 < high:
        mid = (high + low) // 2
        if mid * (time - mid) > distance:
            high = mid
        else:
            low = mid

    return time - 2 * high + 1

def solve(input_file):
    data = parse_data(input_file)
    yield part1(data)
    yield part2(data)

if __name__ == "__main__":
    dir_input = "./input"

    file_input = os.listdir(dir_input)

    for file_name in file_input:
        start_time = time.time()

        file_path = os.path.join(dir_input, file_name)

        print(f"{Fore.YELLOW}{file_path}:")
        
        try:
            input_file = pathlib.Path(file_path).read_text().rstrip()
            if not input_file:
                print("⚠️  Input file is empty.")
            else:
                solutions = solve(input_file)
                print("\n".join(str(solution) for solution in solutions))
        except Exception as e:
            print(f"🔴  Error reading or processing the file: {e}")

        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_rounded = "{:.4f}".format(execution_time)
        print(f"Execution time: {execution_time_rounded} s")

        print("*" * 50)