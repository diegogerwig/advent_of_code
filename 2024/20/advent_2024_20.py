'''
--- Day 20: Race Condition ---
The Historians are quite pixelated again. This time, a massive, black building looms over you - you're right outside the CPU!

While The Historians get to work, a nearby program sees that you're idle and challenges you to a race. Apparently, you've arrived just in time for the frequently-held race condition festival!

The race takes place on a particularly long and twisting code path; programs compete to see who can finish in the fewest picoseconds. The winner even gets their very own mutex!

They hand you a map of the racetrack (your puzzle input). For example:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
The map consists of track (.) - including the start (S) and end (E) positions (both of which also count as track) - and walls (#).

When a program runs through the racetrack, it starts at the start position. Then, it is allowed to move up, down, left, or right; each such move takes 1 picosecond. The goal is to reach the end position as quickly as possible. In this example racetrack, the fastest time is 84 picoseconds.

Because there is only a single path from the start to the end and the programs all go the same speed, the races used to be pretty boring. To make things more interesting, they introduced a new rule to the races: programs are allowed to cheat.

The rules for cheating are very strict. Exactly once during a race, a program may disable collision for up to 2 picoseconds. This allows the program to pass through walls as if they were regular track. At the end of the cheat, the program must be back on normal track again; otherwise, it will receive a segmentation fault and get disqualified.

So, a program could complete the course in 72 picoseconds (saving 12 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...12....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Or, a program could complete the course in 64 picoseconds (saving 20 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...12..#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
This cheat saves 38 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.####1##.###
#...###.2.#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
This cheat saves 64 picoseconds and takes the program directly to the end:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..21...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Each cheat has a distinct start position (the position where the cheat is activated, just before the first move that is allowed to go through walls) and end position; cheats are uniquely identified by their start position and end position.

In this example, the total number of cheats (grouped by the amount of time they save) are as follows:

There are 14 cheats that save 2 picoseconds.
There are 14 cheats that save 4 picoseconds.
There are 2 cheats that save 6 picoseconds.
There are 4 cheats that save 8 picoseconds.
There are 2 cheats that save 10 picoseconds.
There are 3 cheats that save 12 picoseconds.
There is one cheat that saves 20 picoseconds.
There is one cheat that saves 36 picoseconds.
There is one cheat that saves 38 picoseconds.
There is one cheat that saves 40 picoseconds.
There is one cheat that saves 64 picoseconds.
You aren't sure what the conditions of the racetrack will be like, so to give yourself as many options as possible, you'll need a list of the best cheats. How many cheats would save you at least 100 picoseconds?

--- Part Two ---
The programs seem perplexed by your list of cheats. Apparently, the two-picosecond cheating rule was deprecated several milliseconds ago! The latest version of the cheating rule permits a single cheat that instead lasts at most 20 picoseconds.

Now, in addition to all the cheats that were possible in just two picoseconds, many more cheats are possible. This six-picosecond cheat saves 76 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#1#####.#.#.###
#2#####.#.#...#
#3#####.#.###.#
#456.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Because this cheat has the same start and end positions as the one above, it's the same cheat, even though the path taken during the cheat is different:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S12..#.#.#...#
###3###.#.#.###
###4###.#.#...#
###5###.#.###.#
###6.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Cheats don't need to use all 20 picoseconds; cheats can last any amount of time up to and including 20 picoseconds (but can still only end when the program is on normal track). Any cheat time not used is lost; it can't be saved for another cheat later.

You'll still need a list of the best cheats, but now there are even more to choose between. Here are the quantities of cheats in this example that save 50 picoseconds or more:

There are 32 cheats that save 50 picoseconds.
There are 31 cheats that save 52 picoseconds.
There are 29 cheats that save 54 picoseconds.
There are 39 cheats that save 56 picoseconds.
There are 25 cheats that save 58 picoseconds.
There are 23 cheats that save 60 picoseconds.
There are 20 cheats that save 62 picoseconds.
There are 19 cheats that save 64 picoseconds.
There are 12 cheats that save 66 picoseconds.
There are 14 cheats that save 68 picoseconds.
There are 12 cheats that save 70 picoseconds.
There are 22 cheats that save 72 picoseconds.
There are 4 cheats that save 74 picoseconds.
There are 3 cheats that save 76 picoseconds.
Find the best cheats using the updated cheating rules. How many cheats would save you at least 100 picoseconds?
'''


#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time

init(autoreset=True)

CURRENT_FILEPATH = ""

TEST_STATUS = {
    "PASSED": "PASSED",
    "FAILED": "FAILED", 
    "IN_PROGRESS": "IN PROGRESS",
    "UNKNOWN": "UNKNOWN"
}

STATUS_COLORS = {
    TEST_STATUS["PASSED"]: Fore.GREEN,
    TEST_STATUS["FAILED"]: Fore.RED,
    TEST_STATUS["IN_PROGRESS"]: Fore.YELLOW,
    TEST_STATUS["UNKNOWN"]: Fore.BLUE
}

TEST_SOLUTIONS = {
    ".test_I.txt": {
        "part1": 0,
        "part2": 0,
    },
    "input_I.txt": {
        "part1": 1463,
        "part2": 985332,
    }
}

def print_header(filename, part):
    """
    Simple header printing function
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Part {part}")
    print(f"{Fore.CYAN}{'='*80}\n")


def parse_input(content):
    """
    Parse the input content 
    """
    # Split the content into lines
    lines = content.splitlines()
    
    # Create empty list for result
    result = []
    
    # Process each line
    for line in lines:
        # Remove whitespace
        clean_line = line.strip()
        
        # Only keep non-empty lines
        if clean_line:
            result.append(clean_line)
            
    return result


def get_phase_ends(grid, x, y, W, H):
    """
    Get all positions reachable by crossing at most 2 walls in a row
    """
    phase_ends = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # If hit wall, try going one more step in same direction
        if grid[ny][nx] == "#":
            nx, ny = nx + dx, ny + dy
            # Check if end position is valid and not a wall
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] != "#":
                phase_ends.append((ny, nx))
    
    return phase_ends


def find_start_end(grid):
    """
    Find start (S) and end (E) positions in grid
    """
    W, H = len(grid[0]), len(grid)
    start = end = None
    
    for y in range(H):
        for x in range(W):
            if grid[y][x] == 'S':
                start = (x, y)
            elif grid[y][x] == 'E':
                end = (x, y)
            if start and end:
                return start, end
                
    return start, end


def calculate_distances(grid, end_pos):
    """
    Calculate distances from end position to all reachable positions
    """
    from collections import deque
    W, H = len(grid[0]), len(grid)
    
    queue = deque([(*end_pos, 0)])  # x, y, distance
    distances = [[1000000000] * W for _ in range(H)]
    
    while queue:
        x, y, d = queue.popleft()
        if distances[y][x] <= d:
            continue
        distances[y][x] = d
        
        # Check all 4 directions
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if grid[ny][nx] != "#":
                queue.append((nx, ny, d + 1))
    
    return distances


def part1(content):
    """
    Calculate shortest paths from end to all points, then find all possible 2-step wall crossings and count how many save at least 100 steps.
    """
    import time
    from collections import defaultdict
    start_time = time.time()
    
    # Parse input
    grid = [line.strip() for line in content.splitlines() if line.strip()]
    W, H = len(grid[0]), len(grid)
    
    # Find start and end positions
    start, end = find_start_end(grid)
    
    # Calculate distances from end to all positions
    distances = calculate_distances(grid, end)
    
    # Count savings for each possible cheat
    time_savings = defaultdict(int)
    
    for y in range(H):
        for x in range(W):
            if grid[y][x] != "#":
                current_dist = distances[y][x]  # Distance from this point to end
                # Try all possible 2-step wall crossings from this point
                phase_ends = get_phase_ends(grid, x, y, W, H)
                
                for ny, nx in phase_ends:
                    new_dist = distances[ny][nx]  # Distance from landing point to end
                    if new_dist < current_dist:  # If this cheat helps
                        time_savings[current_dist - new_dist - 2] += 1  # -2 for the cheat moves
    
    # Count cheats that save >= 100 steps
    result = sum(count for saving, count in time_savings.items() if saving >= 100)
    
    print(f"\nFound cheats with savings:", dict(time_savings))
    print(f"Found {result} cheats that save at least 100 picoseconds")
    
    return {
        "value": result,
        "execution_time": time.time() - start_time
    }


def get_phase_ends_20(grid, x, y, W, H):
    """
    Get all positions reachable within 20 steps manhattan distance
    """
    phase_ends = []
    
    # Check all positions within manhattan distance of 20
    for ny in range(max(0, y - 20), min(H-1, y + 21)):
        # Calculate remaining steps available after vertical movement
        remaining_steps = 20 - abs(ny - y)
        # Check horizontal positions within remaining steps
        for nx in range(max(0, x - remaining_steps), min(W-1, x + remaining_steps + 1)):
            if grid[ny][nx] != "#":
                manhattan_dist = abs(ny - y) + abs(nx - x)
                if manhattan_dist > 0:  # Don't include starting position
                    phase_ends.append((ny, nx, manhattan_dist))
    
    return phase_ends


def part2(content):
    """
    Calculate shortest paths allowing up to 20-step cheats instead of just 2-step ones
    """
    import time
    from collections import defaultdict
    start_time = time.time()
    
    # Parse input
    grid = [line.strip() for line in content.splitlines() if line.strip()]
    W, H = len(grid[0]), len(grid)
    
    # Find start and end positions
    start, end = find_start_end(grid)
    
    # Calculate distances from end to all positions
    distances = calculate_distances(grid, end)
    
    # Count savings for each possible cheat
    time_savings = defaultdict(int)
    
    for y in range(H):
        for x in range(W):
            if grid[y][x] != "#":
                current_dist = distances[y][x]  # Distance from this point to end
                # Try all possible positions within 20 steps
                phase_ends = get_phase_ends_20(grid, x, y, W, H)
                
                for ny, nx, cheat_dist in phase_ends:
                    new_dist = distances[ny][nx]  # Distance from landing point to end
                    if new_dist < current_dist:  # If this cheat helps
                        time_savings[current_dist - new_dist - cheat_dist] += 1
    
    # Count cheats that save >= 100 steps
    result = sum(count for saving, count in time_savings.items() if saving >= 100)
    
    print(f"\nFound cheats with savings:", dict(time_savings))
    print(f"Found {result} cheats that save at least 100 picoseconds")
    
    return {
        "value": result,
        "execution_time": time.time() - start_time
    }






















def determine_test_status(result, expected):
    """
    Determine the test status based on the result and expected value.
    IN_PROGRESS solo cuando es N/A.
    Soporta comparaciones entre int, float y string.
    """
    if expected == 'N/A':
        return TEST_STATUS["IN_PROGRESS"]
    
    # Convert both values to strings for comparison to handle mixed types
    result_str = str(result["value"])
    expected_str = str(expected)
    
    if result_str == expected_str:
        return TEST_STATUS["PASSED"]
    return TEST_STATUS["FAILED"]

def get_status_color(status):
    """
    Get the appropriate color for each status
    """
    return STATUS_COLORS.get(status, Fore.WHITE)

def process_file(filepath):
    """
    Process a single file and validate results against test solutions
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            
            print_header(filename, 1)
            part1_result = part1(content)
            
            print_header(filename, 2)
            part2_result = part2(content)
            
            # Get test solutions if available
            test_solution = TEST_SOLUTIONS.get(filename, {})
            
            # Add status to results
            part1_result["status"] = determine_test_status(
                part1_result, 
                test_solution.get("part1", 0)
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", 0)
            )
            
            return True, {
                "part1": part1_result,
                "part2": part2_result
            }
            
    except Exception as e:
        return False, str(e)

def process_directory(input_dir="./input/"):
    """Process all files in the specified directory"""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    print(f"\n{Fore.CYAN}Processing files in directory: {Fore.YELLOW}{input_dir}")
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    results = {}
    
    for file in files:
        filepath = os.path.join(input_dir, file)
        success, result = process_file(filepath)
        results[file] = (success, result)
    
    return results

def print_results(results):
    """Print results with enhanced status display"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    for file, (success, result) in results.items():
        print(f"\n{Fore.BLUE}{file}:")
        
        if success:
            for part_name, part_result in result.items():
                status_color = get_status_color(part_result["status"])
                status_text = f"[{part_result['status']}]"
                
                # Add expected value for FAILED status
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    status_text += f" (Expected: {TEST_SOLUTIONS[file][part_name]})"
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{part_result['value']:<15} "
                      f"{status_color}{status_text}  "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
        else:
            print(f"  {Fore.RED}Error - {result}")

def main():
    try:
        input_dir = "./input/"
        results = process_directory(input_dir)
        print_results(results)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()