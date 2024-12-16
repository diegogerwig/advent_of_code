'''
--- Day 16: Reindeer Maze ---
It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where the Reindeer compete for the lowest score.

You and The Historians arrive to search for the Chief right as the event is about to start. It wouldn't hurt to watch a little, right?

The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).

To figure out the best place to sit, you start by grabbing a map (your puzzle input) from a nearby kiosk. For example:

###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
There are many paths through this maze, but taking any of the best paths would incur a score of only 7036. This can be achieved by taking a total of 36 steps forward and turning 90 degrees a total of 7 times:


###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############
Here's a second example:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
In this maze, the best paths cost 11048 points; following one such path would look like this:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################
Note that the path shown above includes one 90 degree turn as the very first move, rotating the Reindeer from facing East to facing North.

Analyze your map carefully. What is the lowest score a Reindeer could possibly get?

--- Part Two ---
Now that you know what the best paths look like, you can figure out the best spot to sit.

Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile. While determining which of these tiles would be the best spot to sit depends on a whole bunch of factors (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar blocking your view, etc.), the most important factor is whether the tile is on one of the best paths through the maze. If you sit somewhere else, you'd miss all the action!

So, you'll need to determine which tiles are part of any best path through the maze, including the S and E tiles.

In the first example, there are 45 tiles (marked O) that are part of at least one of the various best paths through the maze:

###############
#.......#....O#
#.#.###.#.###O#
#.....#.#...#O#
#.###.#####.#O#
#.#.#.......#O#
#.#.#####.###O#
#..OOOOOOOOO#O#
###O#O#####O#O#
#OOO#O....#O#O#
#O#O#O###.#O#O#
#OOOOO#...#O#O#
#O###.#.#.#O#O#
#O..#.....#OOO#
###############
In the second example, there are 64 tiles that are part of at least one of the best paths:

#################
#...#...#...#..O#
#.#.#.#.#.#.#.#O#
#.#.#.#...#...#O#
#.#.#.#.###.#.#O#
#OOO#.#.#.....#O#
#O#O#.#.#.#####O#
#O#O..#.#.#OOOOO#
#O#O#####.#O###O#
#O#O#..OOOOO#OOO#
#O#O###O#####O###
#O#O#OOO#..OOO#.#
#O#O#O#####O###.#
#O#O#OOOOOOO..#.#
#O#O#O#########.#
#O#OOO..........#
#################
Analyze your map further. How many tiles are part of at least one of the best paths through the maze?
'''


#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time
from tqdm import tqdm

init(autoreset=True)

CURRENT_FILEPATH = ""

TEST_SOLUTIONS = {
    ".test_I.txt": {
        "part1": 7036,
        "part2": 45
    },
        ".test_II.txt": {
        "part1": 11048,
        "part2": 0
    },
    "input_I.txt": {
        "part1": 101492 ,
        "part2": 543
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
    return [line.strip() for line in content.splitlines() if line.strip()]


def part1(content):
    """
    Find lowest possible score for reindeer to reach end
    """
    start_time = time.time()
    
    # Parse input
    grid = parse_input(content)
    
    # Find start and end positions
    start_pos = None
    end_pos = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                start_pos = (x, y)
            elif grid[y][x] == 'E':
                end_pos = (x, y)
    
    # Directions: 0=East, 1=South, 2=West, 3=North
    directions = [(1,0), (0,1), (-1,0), (0,-1)]
    
    # Priority queue for A* search - (priority, (x, y, direction))
    from heapq import heappush, heappop
    queue = [(0, (start_pos[0], start_pos[1], 0))]  # Start facing East
    
    # Keep track of visited states and their costs
    visited = {}
    
    while queue:
        cost, (x, y, direction) = heappop(queue)
        
        # Check if we reached the end
        if (x, y) == end_pos:
            return cost, time.time() - start_time
        
        # Skip if we've seen this state with a better cost
        state = (x, y, direction)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        
        # Try turning left or right (costs 1000)
        for turn in [-1, 1]:  # -1 for left, 1 for right
            new_dir = (direction + turn) % 4
            new_state = (x, y, new_dir)
            new_cost = cost + 1000
            if new_state not in visited or new_cost < visited[new_state]:
                heappush(queue, (new_cost, new_state))
        
        # Try moving forward (costs 1)
        dx, dy = directions[direction]
        new_x, new_y = x + dx, y + dy
        
        # Check if new position is valid
        if (0 <= new_y < len(grid) and 
            0 <= new_x < len(grid[0]) and 
            grid[new_y][new_x] != '#'):
            new_state = (new_x, new_y, direction)
            new_cost = cost + 1
            if new_state not in visited or new_cost < visited[new_state]:
                heappush(queue, (new_cost, new_state))
    
    return -1, time.time() - start_time  # No path found


def part2(content):
    """
    Find number of tiles that are part of any optimal path
    """
    from tqdm import tqdm
    start_time = time.time()
    
    # Parse input
    grid = parse_input(content)
    total_cells = len(grid) * len(grid[0])  # Total number of cells for progress estimation
    
    # Find start and end positions
    start_pos = None
    end_pos = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                start_pos = (x, y)
            elif grid[y][x] == 'E':
                end_pos = (x, y)
    
    # Directions: 0=East, 1=South, 2=West, 3=North
    directions = [(1,0), (0,1), (-1,0), (0,-1)]
    
    # Forward search from start
    from heapq import heappush, heappop
    forward_costs = {}  # (x, y, dir) -> cost
    forward_queue = [(0, (start_pos[0], start_pos[1], 0))]  # Start facing East
    
    print("Performing forward search...")
    with tqdm(total=total_cells, desc="Forward search") as pbar:
        visited_positions = set()
        while forward_queue:
            cost, (x, y, direction) = heappop(forward_queue)
            state = (x, y, direction)
            pos = (x, y)
            
            if pos not in visited_positions:
                visited_positions.add(pos)
                pbar.update(1)
            
            if state in forward_costs and forward_costs[state] <= cost:
                continue
            forward_costs[state] = cost
            
            # Try turning
            for turn in [-1, 1]:
                new_dir = (direction + turn) % 4
                new_state = (x, y, new_dir)
                new_cost = cost + 1000
                if new_state not in forward_costs or new_cost < forward_costs[new_state]:
                    heappush(forward_queue, (new_cost, new_state))
            
            # Try moving forward
            dx, dy = directions[direction]
            new_x, new_y = x + dx, y + dy
            if (0 <= new_y < len(grid) and 
                0 <= new_x < len(grid[0]) and 
                grid[new_y][new_x] != '#'):
                new_state = (new_x, new_y, direction)
                new_cost = cost + 1
                if new_state not in forward_costs or new_cost < forward_costs[new_state]:
                    heappush(forward_queue, (new_cost, new_state))
    
    # Backward search from end
    backward_costs = {}  # (x, y, dir) -> cost
    backward_queue = []
    # Try all possible directions at end
    for dir in range(4):
        heappush(backward_queue, (0, (end_pos[0], end_pos[1], dir)))
    
    print("\nPerforming backward search...")
    with tqdm(total=total_cells, desc="Backward search") as pbar:
        visited_positions = set()
        while backward_queue:
            cost, (x, y, direction) = heappop(backward_queue)
            state = (x, y, direction)
            pos = (x, y)
            
            if pos not in visited_positions:
                visited_positions.add(pos)
                pbar.update(1)
            
            if state in backward_costs and backward_costs[state] <= cost:
                continue
            backward_costs[state] = cost
            
            # Try turning
            for turn in [-1, 1]:
                new_dir = (direction + turn) % 4
                new_state = (x, y, new_dir)
                new_cost = cost + 1000
                if new_state not in backward_costs or new_cost < backward_costs[new_state]:
                    heappush(backward_queue, (new_cost, new_state))
            
            # Try moving backward
            dx, dy = directions[(direction + 2) % 4]
            new_x, new_y = x + dx, y + dy
            if (0 <= new_y < len(grid) and 
                0 <= new_x < len(grid[0]) and 
                grid[new_y][new_x] != '#'):
                new_state = (new_x, new_y, direction)
                new_cost = cost + 1
                if new_state not in backward_costs or new_cost < backward_costs[new_state]:
                    heappush(backward_queue, (new_cost, new_state))
    
    print("\nFinding optimal paths...")
    # Find minimum total cost
    min_total_cost = float('inf')
    for state, forward_cost in tqdm(forward_costs.items(), desc="Finding min cost"):
        x, y, dir = state
        if (x, y) == end_pos:
            min_total_cost = min(min_total_cost, forward_cost)
    
    # Find all tiles that are part of an optimal path
    optimal_tiles = set()
    total_combinations = len(forward_costs) * len(backward_costs)
    with tqdm(total=total_combinations, desc="Finding optimal tiles") as pbar:
        for state, forward_cost in forward_costs.items():
            x, y, forward_dir = state
            for backward_state, backward_cost in backward_costs.items():
                bx, by, backward_dir = backward_state
                if (x, y) == (bx, by):
                    if forward_cost + backward_cost == min_total_cost:
                        optimal_tiles.add((x, y))
                pbar.update(1)
    
    print(f"\nFound {len(optimal_tiles)} optimal tiles")
    return len(optimal_tiles), time.time() - start_time


def process_file(filepath):
    """Process a single file and validate results against test solutions"""
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            
            print_header(filename, 1)
            part1_result, time1 = part1(content)
            
            print_header(filename, 2)
            part2_result, time2 = part2(content)
            
            # Validate against test solutions if available
            test_results = {
                "part1": {
                    "result": part1_result,
                    "time": time1,
                    "passed": None
                },
                "part2": {
                    "result": part2_result,
                    "time": time2,
                    "passed": None
                }
            }
            
            if filename in TEST_SOLUTIONS:
                test_results["part1"]["passed"] = part1_result == TEST_SOLUTIONS[filename]["part1"]
                test_results["part2"]["passed"] = part2_result == TEST_SOLUTIONS[filename]["part2"]
            
            return True, test_results
            
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
    """Print results with test validation"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    for file, (success, result) in results.items():
        print(f"\n{Fore.BLUE}{file}:")
        
        if success:
            # Part 1 results
            part1_info = result["part1"]
            status = ""
            if part1_info["passed"] is not None:
                status = (f"{Fore.GREEN}[PASSED]" if part1_info["passed"] 
                         else f"{Fore.RED}[FAILED]")
                if not part1_info["passed"]:
                    status += f" (Expected: {TEST_SOLUTIONS[file]['part1']})"
            
            print(f"  {Fore.YELLOW}Part 1: {Fore.GREEN}{part1_info['result']:<15} {status}  "
                  f"{Fore.CYAN}Time: {part1_info['time']:.6f}s")
            
            # Part 2 results
            part2_info = result["part2"]
            status = ""
            if part2_info["passed"] is not None:
                status = (f"{Fore.GREEN}[PASSED]" if part2_info["passed"] 
                         else f"{Fore.RED}[FAILED]")
                if not part2_info["passed"]:
                    status += f" (Expected: {TEST_SOLUTIONS[file]['part2']})"
            
            print(f"  {Fore.YELLOW}Part 2: {Fore.GREEN}{part2_info['result']:<15} {status}  "
                  f"{Fore.CYAN}Time: {part2_info['time']:.6f}s")
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