#!/usr/bin/python3

'''
--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?

--- Part Two ---
Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:


##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
'''

import os
from colorama import init, Fore

init(autoreset=True)

CURRENT_FILEPATH = ""


def parse_grid(content):
    """
    Parses the input grid to find:
    1. Map dimensions (width, height)
    2. Antenna positions for each frequency
    
    Returns:
    - Width of the map
    - Height of the map
    - Dictionary where key is frequency (letter/number) and value is list of (x,y) coordinates
    """
    # Split content into lines
    grid_lines = []
    for line in content.splitlines():  # Split on newlines
        line = line.strip()
        grid_lines.append(line)
    
    # Get map dimensions
    width = len(grid_lines[0])
    height = len(grid_lines)
    
    # Find all antennas and their positions
    antennas = {}
    for y in range(height):
        for x in range(width):
            char = grid_lines[y][x]
            # If character is letter or number, it's an antenna
            if char.isalnum():
                # Initialize list for this frequency if not seen before
                if char not in antennas:
                    antennas[char] = []
                # Add the position to the list for this frequency
                antennas[char].append((x, y))
    
    print(f"{Fore.YELLOW}Parsed grid from input: {CURRENT_FILEPATH} ")
    print(f"    Width map: {width}")
    print(f"    Height map: {height}")
    print(f"    Total number of antennas: {sum(len(v) for v in antennas.values())}")
    print(f"    Antennas frequencies count: {len(antennas)}")
    print(f"    Antennas frequencies: {list(antennas.keys())}")
    print(f"    Antennas locations: {antennas}")

    return width, height, antennas


def get_antinodes(p1, p2, width, height):
    """
    Calculate antinode positions for a pair of antennas
    """
    x1, y1 = p1
    x2, y2 = p2

    # Calculate the differences
    dx = x2 - x1
    dy = y2 - y1
    
    antinodes = set()
    
    # Position 1: beyond p1
    x_anti1 = x1 - dx
    y_anti1 = y1 - dy
    if x_anti1 >= 0 and x_anti1 < width and y_anti1 >= 0 and y_anti1 < height:
        antinodes.add((x_anti1, y_anti1))
        
    # Position 2: beyond p2
    x_anti2 = x2 + dx
    y_anti2 = y2 + dy
    if x_anti2 >= 0 and x_anti2 < width and y_anti2 >= 0 and y_anti2 < height:
        antinodes.add((x_anti2, y_anti2))
    
    return antinodes


def calculate_antinodes(width, height, antennas):
    """
    Find all antinode positions in the grid
    """
    all_antinodes = set()
    
    # For each frequency (letter/number)
    for freq in antennas:
        positions = antennas[freq]

        if len(positions) < 2:  # Skip if only one antenna of this frequency
            continue

        # Check each pair of antennas with same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                p1 = positions[i]
                p2 = positions[j]
                # Get antinodes for this pair and add them to our set
                pair_antinodes = get_antinodes(p1, p2, width, height)
                for antinode in pair_antinodes:
                    all_antinodes.add(antinode)
    
    return all_antinodes


# def is_collinear(p1, p2, p3):
#     """
#     Check if three points are perfectly in line
#     """
#     x1, y1 = p1
#     x2, y2 = p2
#     x3, y3 = p3
#     # Cross product should be 0 for collinear points
#     return (y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)


def get_antinodes_resonant(p1, p2, width, height):
    """
    Calculate antinode positions for a pair of antennas:
    - Points must maintain the same x/y ratio as original points
    """
    x1, y1 = p1
    x2, y2 = p2

    # Calculate the differences
    dx = x2 - x1
    dy = y2 - y1
    
    antinodes = set()
    
    # Add the antenna positions themselves
    antinodes.add(p1)
    antinodes.add(p2)
    
    # Start from first point and extend in both directions
    # Using the exact differences as steps
    current_x = x1 + dx  
    current_y = y1 + dy
    
    # Go forward beyond p2
    while 0 <= current_x < width and 0 <= current_y < height:
        antinodes.add((current_x, current_y))
        current_x += dx
        current_y += dy
    
    # Go backward from p1
    current_x = x1 - dx  
    current_y = y1 - dy
    
    # Go backward beyond p1
    while 0 <= current_x < width and 0 <= current_y < height:
        antinodes.add((current_x, current_y))
        current_x -= dx
        current_y -= dy
    
    return antinodes


def calculate_antinodes_resonant(width, height, antennas):
    """
    Find all antinode positions in the grid using resonance rules
    """
    all_antinodes = set()
    
    # For each frequency
    for freq in antennas:
        positions = antennas[freq]
        if len(positions) < 2:  # Skip if only one antenna of this frequency
            continue
            
        # Check each pair of antennas with same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                p1 = positions[i]
                p2 = positions[j]
                # Get antinodes for this pair and add them to our set
                pair_antinodes = get_antinodes_resonant(p1, p2, width, height)
                all_antinodes.update(pair_antinodes)
    
    return all_antinodes


def antinodes(content):
    """
    Count total number of antinodes
    """
    width, height, antennas = parse_grid(content)
    antinodes = calculate_antinodes(width, height, antennas)
    print(f"{Fore.GREEN}Antinodes locations: {Fore.RESET}{antinodes}")
    return len(antinodes)


def antinodes_resonant(content):
    """
    Count total number of antinodes with resonant rules
    """
    width, height, antennas = parse_grid(content)
    antinodes = calculate_antinodes_resonant(width, height, antennas)
    print(f"{Fore.GREEN}Antinodes locations: {Fore.RESET}{antinodes}")
    return len(antinodes)


def process_file(filepath):
    """
    Processes the file at the specified path using the functions:
    - Counts unique antinode locations within the bounds of the map.
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath

    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = antinodes(content)
        part2_result = antinodes_resonant(content)
        return part1_result, part2_result


def process_directory(input_dir="./input/"):
    """
    Processes all files in the specified directory.
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    results = {}
    
    for file in files:
        filepath = os.path.join(input_dir, file)
        try:
            part1_result, part2_result = process_file(filepath)
            results[file] = (True, part1_result, part2_result)
        except Exception as e:
            results[file] = (False, str(e))
    
    return results


if __name__ == "__main__":
    input_dir = "./input/"
    results = process_directory(input_dir)
    
    for file, result in results.items():
        if result[0]:  # Successfully processed
            part1, part2 = result[1], result[2]
            print(f"{Fore.BLUE}{file}:")
            print(f"  {Fore.YELLOW}Part 1 (Antinodes): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Antinodes Resonant): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
