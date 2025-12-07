#!/usr/bin/python3

'''
--- Day 7: Laboratories ---

You thank the cephalopods for the help and exit the trash compactor, finding yourself in the familiar halls of a North Pole research wing.

Based on the large sign that says "teleporter hub", they seem to be researching teleportation; you can't help but try it for yourself and step onto the large yellow teleporter pad.

Suddenly, you find yourself in an unfamiliar room! The room has no doors; the only way out is the teleporter. Unfortunately, the teleporter seems to be leaking magic smoke.

Since this is a teleporter lab, there are lots of spare parts, manuals, and diagnostic equipment lying around. After connecting one of the diagnostic tools, it helpfully displays error code 0H-N0, which apparently means that there's an issue with one of the tachyon manifolds.

You quickly locate a diagram of the tachyon manifold (your puzzle input). A tachyon beam enters the manifold at the location marked S; tachyon beams always move downward. Tachyon beams pass freely through empty space (.). However, if a tachyon beam encounters a splitter (^), the beam is stopped; instead, a new tachyon beam continues from the immediate left and from the immediate right of the splitter.

For example:

.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............

In this example, the incoming tachyon beam (|) extends downward from S until it reaches the first splitter:

.......S.......
.......|.......
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............

At that point, the original beam stops, and two new beams are emitted from the splitter:

.......S.......
.......|.......
......|^|......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............

Those beams continue downward until they reach more splitters:

.......S.......
.......|.......
......|^|......
......|.|......
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............

At this point, the two splitters create a total of only three tachyon beams, since they are both dumping tachyons into the same place between them:

.......S.......
.......|.......
......|^|......
......|.|......
.....|^|^|.....
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............

This process continues until all of the tachyon beams reach a splitter or exit the manifold:

.......S.......
.......|.......
......|^|......
......|.|......
.....|^|^|.....
.....|.|.|.....
....|^|^|^|....
....|.|.|.|....
...|^|^|||^|...
...|.|.|||.|...
..|^|^|||^|^|..
..|.|.|||.|.|..
.|^|||^||.||^|.
.|.|||.||.||.|.
|^|^|^|^|^|||^|
|.|.|.|.|.|||.|

To repair the teleporter, you first need to understand the beam-splitting properties of the tachyon manifold. In this example, a tachyon beam is split a total of 21 times.

Analyze your manifold diagram. How many times will the beam be split?


--- Part Two ---

With your analysis of the manifold complete, you begin fixing the teleporter. However, as you open the side of the teleporter to replace the broken manifold, you are surprised to discover that it isn't a classical tachyon manifold - it's a quantum tachyon manifold.

With a quantum tachyon manifold, only a single tachyon particle is sent through the manifold. A tachyon particle takes both the left and right path of each splitter encountered.

Since this is impossible, the manual recommends the many-worlds interpretation of quantum tachyon splitting: each time a particle reaches a splitter, it's actually time itself which splits. In one timeline, the particle went left, and in the other timeline, the particle went right.

To fix the manifold, what you really need to know is the number of timelines active after a single particle completes all of its possible journeys through the manifold.

In the above example, there are many timelines. For instance, there's the timeline where the particle always went left:

.......S.......
.......|.......
......|^.......
......|........
.....|^.^......
.....|.........
....|^.^.^.....
....|..........
...|^.^...^....
...|...........
..|^.^...^.^...
..|............
.|^...^.....^..
.|.............
|^.^.^.^.^...^.
|..............

Or, there's the timeline where the particle alternated going left and right at each splitter:

.......S.......
.......|.......
......|^.......
......|........
......^|^......
.......|.......
.....^|^.^.....
......|........
....^.^|..^....
.......|.......
...^.^.|.^.^...
.......|.......
..^...^|....^..
.......|.......
.^.^.^|^.^...^.
......|........

Or, there's the timeline where the particle ends up at the same point as the alternating timeline, but takes a totally different path to get there:

.......S.......
.......|.......
......|^.......
......|........
.....|^.^......
.....|.........
....|^.^.^.....
....|..........
....^|^...^....
.....|.........
...^.^|..^.^...
......|........
..^..|^.....^..
.....|.........
.^.^.^|^.^...^.
......|........

In this example, in total, the particle ends up on 40 different timelines.

Apply the many-worlds interpretation of quantum tachyon splitting to your manifold diagram. In total, how many different timelines would a single tachyon particle end up on?
'''

import os
import sys
import time
from colorama import init, Fore    # type: ignore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": '21',
        "part2": '40',
    },
    "input_I.txt": {
        "part1": '1566', 
        "part2": '5921061943075',  
    }
}

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


def print_header(filename, part):
    """Simple header printing function"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Part {part}")
    print(f"{Fore.CYAN}{'='*80}\n")


def parse_input(content):
    """
    Parse the tachyon manifold diagram.
    Returns grid, start position, and dimensions.
    """
    lines = content.rstrip('\n').split('\n')
    
    # Find start position
    start_pos = None
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
    
    # Convert to grid
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    return grid, start_pos, rows, cols


def simulate_beam_part1(grid, start_pos, rows, cols):
    """
    Part 1: Count total beam splits.
    
    Counting each time a beam encounters a splitter.
    When a beam hits a splitter, it creates two new beams.
    """
    # Track active beams at each row
    beams = [set() for _ in range(rows)]
    
    # Initial beam from S (starts moving from row below S)
    start_r, start_c = start_pos
    if start_r + 1 < rows:
        beams[start_r + 1].add(start_c)
    
    total_splits = 0
    
    # Process rows from top to bottom
    for r in range(rows):
        current_beams = beams[r]
        
        for c in current_beams:
            # Check what's at this position
            if grid[r][c] == '^':
                # Beam hits a splitter
                total_splits += 1
                
                # Create new beams at left and right
                left_c = c - 1
                right_c = c + 1
                
                # These beams will move to the next row
                if 0 <= left_c < cols and r + 1 < rows:
                    beams[r + 1].add(left_c)
                
                if 0 <= right_c < cols and r + 1 < rows:
                    beams[r + 1].add(right_c)
            else:
                # Beam continues downward
                if r + 1 < rows:
                    beams[r + 1].add(c)
    
    return total_splits


def count_timelines_part2(grid, start_pos, rows, cols):
    """
    Part 2: Count total number of possible timelines (paths).
    
    Counting all possible paths from S to any final position.
    """
    # Initialize table
    dp = [[0 for _ in range(cols)] for _ in range(rows)]
        
    # Initial beam starts at row below S
    start_r, start_c = start_pos
    if start_r + 1 < rows:
        dp[start_r + 1][start_c] = 1
    
    # Process rows from top to bottom
    for r in range(rows):
        for c in range(cols):
            if dp[r][c] == 0:
                continue
            
            if grid[r][c] == '^':
                # Splitter: timelines go left and right
                left_c = c - 1
                right_c = c + 1
                
                if 0 <= left_c < cols and r + 1 < rows:
                    dp[r + 1][left_c] += dp[r][c]
                
                if 0 <= right_c < cols and r + 1 < rows:
                    dp[r + 1][right_c] += dp[r][c]
            else:
                # Empty space or starting position: continue downward
                if r + 1 < rows:
                    dp[r + 1][c] += dp[r][c]
    
    # Sum all timelines in the last row (where beams exit)
    total_timelines = sum(dp[rows - 1])

    print(f"{Fore.YELLOW}DP Table of timelines (final):")
    for r in range(rows):
        row_str = ''.join(f"{dp[r][c]:5}" for c in range(cols))
        print(f"{Fore.YELLOW}{row_str}")
    
    return total_timelines


def part1(content):
    """
    Solution for Part 1: Count total beam splits in tachyon manifold.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Simulating tachyon beam splitting...")
    
    # Parse the manifold diagram
    grid, start_pos, rows, cols = parse_input(content)
    
    if not start_pos:
        print(f"{Fore.RED}No starting position 'S' found!")
        return {
            "value": 0,
            "execution_time": time.time() - start_time,
            "problems_count": 0,
            "results": []
        }
    
    print(f"{Fore.YELLOW}Grid size: {rows} x {cols}")
    print(f"{Fore.YELLOW}Start position: {start_pos}")
    
    # Simulate beam propagation
    total_splits = simulate_beam_part1(grid, start_pos, rows, cols)
    
    # Print summary
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Tachyon Beam Simulation Summary (Part 1):")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Total beam splits: {total_splits}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": total_splits,
        "execution_time": time.time() - start_time,
        "problems_count": 1,
        "results": [{"total_splits": total_splits}]
    }


def part2(content):
    """
    Solution for Part 2: Count total timelines in quantum tachyon manifold.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Counting quantum tachyon timelines...")
    
    # Parse the manifold diagram
    grid, start_pos, rows, cols = parse_input(content)
    
    if not start_pos:
        print(f"{Fore.RED}No starting position 'S' found!")
        return {
            "value": 0,
            "execution_time": time.time() - start_time,
            "problems_count": 0,
            "results": []
        }
    
    print(f"{Fore.YELLOW}Grid size: {rows} x {cols}")
    print(f"{Fore.YELLOW}Start position: {start_pos}")
    
    # Count total timelines
    total_timelines = count_timelines_part2(grid, start_pos, rows, cols)
    
    # Print summary
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Quantum Tachyon Timeline Summary (Part 2):")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Total timelines: {total_timelines}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": total_timelines,
        "execution_time": time.time() - start_time,
        "problems_count": 1,
        "results": [{"total_timelines": total_timelines}]
    }


def determine_test_status(result, expected, filename, part_name):
    """
    Determine the test status based on the result and expected value.
    """
    if expected == 'N/A':
        return TEST_STATUS["IN_PROGRESS"]
    
    try:
        result_value = result["value"]
        if isinstance(result_value, str) and result_value == 'N/A':
            return TEST_STATUS["IN_PROGRESS"]
        
        expected_value = int(expected)
        
        if result_value == expected_value:
            return TEST_STATUS["PASSED"]
        else:
            print(f"{Fore.RED}✗ TEST FAILED for {filename} {part_name}")
            print(f"{Fore.RED}  Expected: {expected_value}")
            print(f"{Fore.RED}  Got: {result_value}")
            
            if "problems_count" in result:
                print(f"{Fore.RED}  Problems count: {result['problems_count']}")
            
            return TEST_STATUS["FAILED"]
    except ValueError:
        return TEST_STATUS["UNKNOWN"]


def get_status_color(status):
    """
    Get the appropriate color for each status
    """
    return STATUS_COLORS.get(status, Fore.WHITE)


def process_file(filepath):
    """
    Process a single file and validate results against test solutions
    """
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
            
            # Add status to results with detailed checking
            part1_result["status"] = determine_test_status(
                part1_result, 
                test_solution.get("part1", "N/A"),
                filename,
                "Part 1"
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", "N/A"),
                filename, 
                "Part 2"
            )
            
            return True, {
                "part1": part1_result,
                "part2": part2_result
            }
            
    except Exception as e:
        print(f"{Fore.RED}Error processing {filename}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, str(e)


def process_directory(input_dir="./input/"):
    """Process all files in the specified directory, tests first"""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    print(f"\n{Fore.CYAN}Processing files in directory: {Fore.YELLOW}{input_dir}")
    
    # Get all files and sort them to process test files first
    files = []
    for f in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, f)):
            files.append(f)
    
    # Sort files: test files first, then input files
    def sort_key(filename):
        if filename.startswith('test'):
            return (0, filename)
        elif filename.startswith('input'):
            return (1, filename)
        else:
            return (2, filename)
    
    files.sort(key=sort_key)
    
    results = {}
    
    for file in files:
        filepath = os.path.join(input_dir, file)
        print(f"\n{Fore.YELLOW}Processing: {file}")
        success, result = process_file(filepath)
        results[file] = (success, result)
    
    return results


def print_results(results):
    """Print results with enhanced status display"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    # Print test files first, then input files
    sorted_files = sorted(results.keys(), key=lambda x: (0 if x.startswith('test') else 1, x))
    
    all_tests_passed = True
    
    for file in sorted_files:
        success, result = results[file]
        print(f"\n{Fore.BLUE}{file}:")
        
        if success:
            for part_name, part_result in result.items():
                status_color = get_status_color(part_result["status"])
                status_text = f"[{part_result['status']}]"
                
                value = part_result['value']
                value_str = str(value)
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{value_str:<20} "
                      f"{status_color}{status_text:<20} "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
                
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    expected_value = TEST_SOLUTIONS.get(file, {}).get(part_name, "N/A")
                    expected_str = str(expected_value)
                    print(f"       {Fore.RED}Expected: {expected_str}")
                    all_tests_passed = False

        else:
            print(f"  {Fore.RED}Error - {result}")
            all_tests_passed = False
    
    # Print overall test summary
    print(f"\n{Fore.CYAN}{'='*80}")
    if all_tests_passed:
        print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"{Fore.RED}❌ SOME TESTS FAILED")
    print(f"{Fore.CYAN}{'='*80}")


def main():
    """
    Main function with improved error handling and command line support
    """
    try:
        # Allow specifying input directory via command line
        input_dir = "./input/"
        if len(sys.argv) > 1:
            input_dir = sys.argv[1]
        
        results = process_directory(input_dir)
        print_results(results)
        
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()