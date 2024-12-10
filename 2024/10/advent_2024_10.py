#!/usr/bin/python3

'''
--- Day 10: Hoof It ---
You all arrive at a Lava Production Facility on a floating island in the sky. As the others begin to search the massive industrial complex, you feel a small nose boop your leg and look down to discover a reindeer wearing a hard hat.

The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly.

Perhaps you can help fill in the missing hiking trails?

The topographic map indicates the height at each position using a scale from 0 (lowest) to 9 (highest). For example:

0123
1234
8765
9876
Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).

You look up from the map and notice that the reindeer has helpfully begun to construct a small pile of pencils, markers, rulers, compasses, stickers, and other equipment you might need to update the map with hiking trails.

A trailhead is any position that starts one or more hiking trails - here, these positions will always have height 0. Assembling more fragments of pages, you establish that a trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail. In the above example, the single trailhead in the top left corner has a score of 1 because it can reach a single 9 (the one in the bottom left).

This trailhead has a score of 2:

...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
(The positions marked . are impassable tiles to simplify these examples; they do not appear on your actual topographic map.)

This trailhead has a score of 4 because every 9 is reachable via a hiking trail except the one immediately to the left of the trailhead:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....
This topographic map contains two trailheads; the trailhead at the top has a score of 1, while the trailhead at the bottom has a score of 2:

10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
Here's a larger example:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
This larger example has 9 trailheads. Considering the trailheads in reading order, they have scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5. Adding these scores together, the sum of the scores of all trailheads is 36.

The reindeer gleefully carries over a protractor and adds it to the pile. What is the sum of the scores of all trailheads on your topographic map?

--- Part Two ---
The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper.

The paper describes a second way to measure a trailhead called its rating. A trailhead's rating is the number of distinct hiking trails which begin at that trailhead. For example:

.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
The above map has a single trailhead; its rating is 3 because there are exactly three distinct hiking trails which begin at that position:

.....0.   .....0.   .....0.
..4321.   .....1.   .....1.
..5....   .....2.   .....2.
..6....   ..6543.   .....3.
..7....   ..7....   .....4.
..8....   ..8....   ..8765.
..9....   ..9....   ..9....
Here is a map containing a single trailhead with rating 13:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....
This map contains a single trailhead with rating 227 (because there are 121 distinct hiking trails that lead to the 9 on the right edge and 106 that lead to the 9 on the bottom edge):

012345
123456
234567
345678
4.6789
56789.
Here's the larger example from before:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
Considering its trailheads in reading order, they have ratings of 20, 24, 10, 4, 1, 4, 5, 8, and 5. The sum of all trailhead ratings in this larger example topographic map is 81.

You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks and bits of paper and is using them to mark trailheads on your topographic map. What is the sum of the ratings of all trailheads?
'''

import os
from colorama import init, Fore, Style
from tqdm import tqdm
import inspect

init(autoreset=True)

CURRENT_FILEPATH = ""


def print_processing_header(filename, function_name):
    """
    Prints a formatted header for the current processing operation
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Function: {Fore.YELLOW}{function_name}")
    print(f"{Fore.CYAN}{'='*80}\n")


def create_grid(content):
    """
    Convert text input into a 2D grid of numbers
    """
    grid = []
    for line in content.strip().split('\n'):
        if line and not line.startswith("'"):
            row = []
            for char in line.strip():
                row.append(int(char))
            grid.append(row)
    return grid


def find_reachable_nines(grid, start_row, start_col):
    """
    Find all height-9 positions that can be reached from a starting position
    following a path that increases by 1 at each step.
    Returns the number of unique height-9 positions found.
    """
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    # Keep track of positions we've visited and height-9 positions found
    visited_positions = set()
    height_9_positions = set()
    positions_to_check = [(start_row, start_col, 0)]  # (row, col, current_height)
    
    # Explore all possible paths from this position
    while positions_to_check:
        current_row, current_col, current_height = positions_to_check.pop(0)
        
        # If we found a height-9 position, add it to our set
        if grid[current_row][current_col] == 9:
            height_9_positions.add((current_row, current_col))
            continue
        
        # Check each neighboring position (up, down, left, right)
        neighbor_positions = [
            (current_row - 1, current_col),  # up
            (current_row + 1, current_col),  # down
            (current_row, current_col - 1),  # left
            (current_row, current_col + 1)   # right
        ]
        
        # Check each neighbor
        for next_row, next_col in neighbor_positions:
            # Skip if position is outside grid
            if not (0 <= next_row < grid_height and 0 <= next_col < grid_width):
                continue
            
            # Skip if we've already visited this position
            if (next_row, next_col) in visited_positions:
                continue
            
            # Skip if height doesn't increase by exactly 1
            if grid[next_row][next_col] != current_height + 1:
                continue
            
            # Add valid position to our queue and mark as visited
            visited_positions.add((next_row, next_col))
            positions_to_check.append((next_row, next_col, current_height + 1))
    
    return len(height_9_positions)


def trailheads_scores(content):
    """
    Calculate sum of scores for all trailheads.
    Score = number of height-9 positions reachable from each trailhead.
    """
    # Get function name and file for header (keep original logging)
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 1 - {current_func}")

    # Create the grid from input
    grid = create_grid(content)
    
    # Initialize variables
    total_score = 0
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    # Find all trailheads (positions with height 0)
    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 0:
                # Calculate score for this trailhead
                score = find_reachable_nines(grid, row, col)
                total_score += score
    
    return total_score


def find_all_paths(grid, start_row, start_col):
    """
    Helper function to find all possible paths from a starting position to height 9.
    Returns the number of unique complete paths found.
    """
    # Initialize variables
    complete_paths = []
    paths_to_explore = [[(start_row, start_col)]]
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    # Continue while we have paths to explore
    while paths_to_explore:
        current_path = paths_to_explore.pop(0)
        current_row, current_col = current_path[-1]
        current_height = grid[current_row][current_col]
        
        # If we reached height 9, we found a complete path
        if current_height == 9:
            complete_paths.append(current_path)
            continue
        
        # Check each neighboring position
        neighbor_positions = [
            (current_row - 1, current_col),  # up
            (current_row + 1, current_col),  # down
            (current_row, current_col - 1),  # left
            (current_row, current_col + 1)   # right
        ]
        
        # Explore each valid neighbor
        for next_row, next_col in neighbor_positions:
            # Skip if position is outside grid
            if not (0 <= next_row < grid_height and 0 <= next_col < grid_width):
                continue
            
            # Skip if position is already in current path
            if (next_row, next_col) in current_path:
                continue
            
            # Skip if height doesn't increase by exactly 1
            if grid[next_row][next_col] != current_height + 1:
                continue
            
            # Create new path by adding this position
            new_path = current_path + [(next_row, next_col)]
            paths_to_explore.append(new_path)
    
    # Return number of unique complete paths found
    return len(complete_paths)


def trailheads_ratings(content):
    """
    Calculate sum of ratings for all trailheads.
    Rating = number of different possible paths from each trailhead.
    """
    # Get function name and file for header (keep original logging)
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 2 - {current_func}")

    # Create the grid from input
    grid = create_grid(content)
    
    # Initialize variables
    total_rating = 0
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    # Find all trailheads (positions with height 0)
    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 0:
                # Add number of possible paths from this trailhead to total
                rating = find_all_paths(grid, row, col)
                total_rating += rating
    
    return total_rating


def process_file(filepath):
    """
    Process a single input file through both parts of the puzzle
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = trailheads_scores(content)
        part2_result = trailheads_ratings(content)
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

    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    for file, result in results.items():
        if result[0]:  # Successfully processed
            part1, part2 = result[1], result[2]
            print(f"{Fore.BLUE}{file}:")
            print(f"  {Fore.YELLOW}Part 1 (Trailheads Scores): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Trailheads Ratings): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
