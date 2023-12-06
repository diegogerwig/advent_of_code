#!/usr/bin/python3

import pathlib
import os
from colorama import init, Fore
init(autoreset=True)

def parse_data(puzzle_input):
    """Parse input and convert ranges to [start, stop) notation."""
    blocks = [lines.split("\n") for lines in puzzle_input.split("\n\n")]
    seeds = [int(seed) for seed in blocks[0][0].split()[1:]]
    transforms = [
        [(src, src + num, dst - src) for dst, src, num in [map(int, line.split()) for line in lines[1:]]]
        for lines in blocks[1:]
    ]
    return seeds, transforms

def part1(data):
    """Solve part 1."""
    seeds, transforms = data
    locations = plant_seed_ranges([(seed, seed + 1) for seed in seeds], transforms)
    return min(locations)[0]

def part2(data):
    """Solve part 2."""
    seeds, transforms = data
    locations = plant_seed_ranges(
        [(seed, seed + num) for seed, num in zip(seeds[::2], seeds[1::2])], transforms
    )
    return min(locations)[0]

def plant_seed_ranges(seeds, transforms):
    """Plant ranges of seeds."""
    for transform in transforms:
        seeds = [new_seed for seed, num in seeds for new_seed in grow_range(seed, num, transform)]
    return seeds

def grow_range(seed_start, seed_stop, transform):
    """Grow a range of seeds one stage."""
    if seed_stop <= seed_start:
        return []

    for start, stop, offset in transform:
        if start <= seed_start < stop and start < seed_stop <= stop:
            return [(seed_start + offset, seed_stop + offset)]

        if seed_stop <= start or seed_start >= stop:
            continue

        return (
            grow_range(seed_start, start, transform)
            + [(max(seed_start, start) + offset, min(seed_stop, stop) + offset)]
            + grow_range(stop, seed_stop, transform)
        )

    return [(seed_start, seed_stop)]

def solve(input_file):
    """Solve the puzzle for the given input."""
    data = parse_data(input_file)
    yield part1(data)
    yield part2(data)

if __name__ == "__main__":
    dir_input = "./input"

    file_input = os.listdir(dir_input)

    for file_name in file_input:
        file_path = os.path.join(dir_input, file_name)

        print(f"\n{Fore.YELLOW}{file_path}:")
        input_file = pathlib.Path(file_path).read_text().rstrip()
        solutions = solve(input_file)
        print("\n".join(str(solution) for solution in solutions))
        print("\n****************************************************")