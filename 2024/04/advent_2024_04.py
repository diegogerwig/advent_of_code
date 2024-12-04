#!/usr/bin/python3

'''
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?

--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
'''

import os
from colorama import init, Fore

init(autoreset=True)


def parse_grid(content):
    """
    Converts a string containing multiple lines into a 2D grid (matrix) of characters.
    """
    lines = content.strip().split("\n")
    
    grid = []
    for line in lines:
        row = list(line.strip())
        grid.append(row)
    
    return grid


def search_xmas(grid):
    """
    Count all occurrences of the word 'XMAS' in all directions in the grid.
    """
    total_rows = len(grid)
    total_columns = len(grid[0])
    total_found = 0
    
    # Define all possible directions to check
    directions = [
        (0, 1),    # Right
        (1, 0),    # Down
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
        (0, -1),   # Left
        (-1, 0),   # Up
        (-1, -1),  # Diagonal up-left
        (-1, 1),   # Diagonal up-right
    ]
    
    # Find X positions first
    for row in range(total_rows):
        for column in range(total_columns):
            if grid[row][column] == 'X':
                
                # For each X found, check all directions
                for dir_row, dir_column in directions:
                    # Calculate positions for M, A, S
                    row1 = row + dir_row
                    col1 = column + dir_column
                    row2 = row + 2*dir_row
                    col2 = column + 2*dir_column
                    row3 = row + 3*dir_row
                    col3 = column + 3*dir_column
                    
                    # Check if positions are within grid and form 'MAS'
                    if (0 <= row1 < total_rows and 0 <= col1 < total_columns and
                        0 <= row2 < total_rows and 0 <= col2 < total_columns and
                        0 <= row3 < total_rows and 0 <= col3 < total_columns and
                        grid[row1][col1] == 'M' and
                        grid[row2][col2] == 'A' and
                        grid[row3][col3] == 'S'):
                        
                        total_found += 1
    
    return total_found


def search_xmas_x(grid):
    """
    Count all occurrences of the "X-MAS" pattern in the grid.
    The "X-MAS" pattern consists of two intersecting "MAS" sequences forming an 'X'.
    """
    total_rows = len(grid)
    total_columns = len(grid[0])
    total_found = 0
    
    # Define diagonal directions for checking X pattern
    diagonals = [
        # (row1, col1, row2, col2) - relative positions from center 'A'
        (-1, -1, 1, 1),   # top-left to bottom-right
        (-1, 1, 1, -1)    # top-right to bottom-left
    ]
    
    # Check each position in grid (excluding edges)
    for row in range(1, total_rows - 1):
        for col in range(1, total_columns - 1):
            
            # Only check positions with 'A' as center
            if grid[row][col] == 'A':
                valid_x_pattern = True
                
                # Check both diagonals that form the X
                for d1_row, d1_col, d2_row, d2_col in diagonals:
                    # Calculate actual positions
                    pos1_row = row + d1_row
                    pos1_col = col + d1_col
                    pos2_row = row + d2_row
                    pos2_col = col + d2_col
                    
                    # Check if positions are valid and form M-S or S-M pattern
                    pos1_valid = (0 <= pos1_row < total_rows and 
                                0 <= pos1_col < total_columns)
                    pos2_valid = (0 <= pos2_row < total_rows and 
                                0 <= pos2_col < total_columns)
                    
                    if not (pos1_valid and pos2_valid):
                        valid_x_pattern = False
                        break
                        
                    # Check if diagonal has valid M-S or S-M pattern
                    valid_pattern = (
                        (grid[pos1_row][pos1_col] == "M" and 
                         grid[pos2_row][pos2_col] == "S") or
                        (grid[pos1_row][pos1_col] == "S" and 
                         grid[pos2_row][pos2_col] == "M")
                    )
                    
                    if not valid_pattern:
                        valid_x_pattern = False
                        break
                
                # If both diagonals form valid patterns, count it
                if valid_x_pattern:
                    total_found += 1
    
    return total_found


def process_file(filepath):
    """
    Processes a single file containing a word search grid:
    - Counts all occurrences of 'XMAS'.
    - Counts all occurrences of 'X-MAS' patterns.
    """
    with open(filepath, 'r') as file:
        content = file.read()
        grid = parse_grid(content)
        part1_result = search_xmas(grid)
        part2_result = search_xmas_x(grid)
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
            print(f"  {Fore.YELLOW}Part 1 (Occurrences of 'XMAS':): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Occurrences of 'X-MAS':): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
