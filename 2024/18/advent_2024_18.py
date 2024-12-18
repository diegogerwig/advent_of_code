'''
--- Day 18: RAM Run ---
You and The Historians look a lot more pixelated than you remember. You're inside a computer at the North Pole!

Just as you're about to check out your surroundings, a program runs up to you. "This region of memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is pushing whole bytes down on top of us! Run!"

The algorithm is fast - it's going to cause a byte to fall into your memory space once every nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid with coordinates that range from 0 to 6 and the following list of incoming byte positions:

5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of your memory space and Y is the distance from the top edge of your memory space.

You and The Historians are currently in the top left corner of the memory space (at 0,0) and need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in this example). You'll need to simulate the falling bytes to plan out where it will be safe to run; for now, simulate just the first few bytes falling into your memory space.

As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory coordinates cannot be entered by you or The Historians, so you'll need to plan your route carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach the exit.

In the above example, if you were to draw the memory space after the first 12 bytes have fallen (using . for safe and # for corrupted), it would look like this:

...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....
You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in your memory space, the shortest path from the top left corner to the exit would take 22 steps. Here (marked with O) is one such path:

OO.#OOO
.O#OO#O
.OOO#OO
...#OO#
..#OO#.
.#.O#..
#.#OOOO
Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the minimum number of steps needed to reach the exit?

--- Part Two ---
The Historians aren't as used to moving around in this pixelated universe as you are. You're afraid they're not going to be fast enough to make it to the exit before the path is completely blocked.

To determine how fast everyone needs to go, you need to determine the first byte that will cut off the path to the exit.

In the above example, after the byte at 1,1 falls, there is still a path to the exit:

O..#OOO
O##OO#O
O#OO#OO
OOO#OO#
###OO##
.##O###
#.#OOOO
However, after adding the very next byte (at 6,1), there is no longer a path to the exit:

...#...
.##..##
.#..#..
...#..#
###..##
.##.###
#.#....
So, in this example, the coordinates of the first byte that prevents the exit from being reachable are 6,1.

Simulate more of the bytes that are about to corrupt your memory space. What are the coordinates of the first byte that will prevent the exit from being reachable from your starting position? (Provide the answer as two integers separated by a comma with no other characters.)
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
        "part1": 22,
        "part2": '6,1',
        "verified": True  # Indicates if the solution is verified
    },
    "input_I.txt": {
        "part1": 334,
        "part2": '20,12',
        "verified": True
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



def get_valid_neighbors(x, y, target, corrupted):
    """Get valid neighbors for a position avoiding corrupted cells."""
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:  # right, down, left, up
        new_x = x + dx
        new_y = y + dy
        if (0 <= new_x <= target[0] and 
            0 <= new_y <= target[1] and 
            (new_x, new_y) not in corrupted):
            yield (new_x, new_y)


def has_path_to_exit(start, target, corrupted):
    """Check if there's a path to exit with given corrupted cells."""
    from collections import deque
    queue = deque([start])
    seen = {start}
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == target:
            return True
            
        for next_pos in get_valid_neighbors(x, y, target, corrupted):
            if next_pos not in seen:
                seen.add(next_pos)
                queue.append(next_pos)
    
    return False


def part1(content):
    """
    Solution for Part 1 of RAM Run puzzle.
    Find shortest path from (0,0) to (target,target) avoiding falling bytes.
    """
    from collections import deque
    import time
    
    start_time = time.time()
    
    # Parse input into list of (x,y) coordinates
    data = [line.strip() for line in content.splitlines() if line.strip()]
    falling_bytes = []
    for line in data:
        if ',' in line:
            x, y = map(int, line.split(','))
            falling_bytes.append((x, y))
    
    # Determine if we're using test input (0-6) or full input (0-70)
    is_test = all(x <= 6 and y <= 6 for x, y in falling_bytes)
    target = (6, 6) if is_test else (70, 70)
    bytes_to_simulate = 12 if is_test else 1024
    
    # Create set of corrupted coordinates
    corrupted = set(falling_bytes[:bytes_to_simulate])
    
    # BFS implementation
    start = (0, 0)
    queue = deque([(0, start)])  # (steps, position)
    seen = {start}
    
    while queue:
        steps, pos = queue.popleft()
        x, y = pos
        
        if pos == target:
            return {
                "value": steps,
                "execution_time": time.time() - start_time
            }
        
        for next_pos in get_valid_neighbors(x, y, target, corrupted):
            if next_pos not in seen:
                seen.add(next_pos)
                queue.append((steps + 1, next_pos))
    
    return {
        "value": -1,  # No path found
        "execution_time": time.time() - start_time
    }


def part2(content):
    """
    Solution for Part 2 of RAM Run puzzle.
    Find the first byte that makes the exit unreachable.
    """
    from collections import deque
    import time
    
    start_time = time.time()
    
    # Parse input into list of (x,y) coordinates
    data = [line.strip() for line in content.splitlines() if line.strip()]
    falling_bytes = []
    for line in data:
        if ',' in line:
            x, y = map(int, line.split(','))
            falling_bytes.append((x, y))
    
    # Determine if we're using test input (0-6) or full input (0-70)
    is_test = all(x <= 6 and y <= 6 for x, y in falling_bytes)
    target = (6, 6) if is_test else (70, 70)
    start = (0, 0)
    
    # Check each byte in sequence until we find the one that blocks all paths
    corrupted = set()
    for byte in falling_bytes:
        corrupted.add(byte)
        if not has_path_to_exit(start, target, corrupted):
            x, y = byte
            return {
                "value": f"{x},{y}",
                "execution_time": time.time() - start_time
            }
    
    return {
        "value": "No blocking byte found",
        "execution_time": time.time() - start_time
    }


def determine_test_status(result, expected, verified):
    """
    Determine the test status based on the result and expected value
    """
    if not verified:
        if expected == 0:
            return TEST_STATUS["IN_PROGRESS"]
        return TEST_STATUS["UNKNOWN"]
    
    if result["value"] == expected:
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
            verified = test_solution.get("verified", False)
            
            # Add status to results
            part1_result["status"] = determine_test_status(
                part1_result, 
                test_solution.get("part1", 0),
                verified
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", 0),
                verified
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