#!/usr/bin/python3

'''
--- Day 4: Printing Department ---

You ride the escalator down to the printing department. They're clearly getting ready for Christmas; they have lots of large rolls of paper everywhere, and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions. If you can figure out which rolls of paper the forklifts can access, they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
Consider your complete diagram of the paper roll locations. How many rolls of paper can be accessed by a forklift?


--- Part Two ---

Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be removed. Once a roll of paper is removed, the forklifts might be able to access more rolls of paper, which they might also be able to remove. How many total rolls of paper could the Elves remove if they keep repeating this process?

Starting with the same example as above, here is one way you could remove as many rolls of paper as possible, using highlighted @ to indicate that a roll of paper is about to be removed, and using x to indicate that a roll of paper was just removed:

Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
Stop once no more rolls of paper are accessible by a forklift. In this example, a total of 43 rolls of paper can be removed.

Start with your original diagram. How many rolls of paper in total can be removed by the Elves and their forklifts?
'''

import os
import sys
import time
from colorama import init, Fore    # type: ignore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 13,
        "part2": 43,  
    },
    "input_I.txt": {
        "part1": 1384, 
        "part2": 8013,
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
    Parse the input content into a grid.
    Each line represents a row of the grid with '.' and '@' characters.
    """
    lines = content.strip().split('\n')
    return [list(line.strip()) for line in lines if line.strip()]


def count_adjacent_rolls(grid, row, col):
    """
    Count the number of '@' in the 8 adjacent positions around (row, col).
    """
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    # Check all 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr = row + dr
            nc = col + dc
            
            # Check if within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == '@':
                    count += 1
    
    return count


def find_accessible_rolls(grid):
    """
    Find all rolls of paper (@) that have fewer than 4 adjacent rolls.
    Returns list of (row, col) positions of accessible rolls.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    accessible = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                adjacent_rolls = count_adjacent_rolls(grid, r, c)
                
                # Forklift can access if fewer than 4 adjacent rolls
                if adjacent_rolls < 4:
                    accessible.append((r, c))
    
    return accessible


def create_visual_grid(grid, accessible_positions, removed_positions):
    """
    Create a visual representation of the grid.
    Accessible rolls are marked with 'x', removed rolls with '.', 
    and inaccessible rolls remain as '@'.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    visual_grid = [list(row) for row in grid]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                if (r, c) in accessible_positions:
                    # Mark as accessible (about to be removed)
                    visual_grid[r][c] = f"{Fore.GREEN}x{Fore.RESET}"
                elif (r, c) in removed_positions:
                    # Mark as removed
                    visual_grid[r][c] = f"{Fore.YELLOW}x{Fore.RESET}"
                else:
                    # Mark as inaccessible
                    visual_grid[r][c] = f"{Fore.RED}@{Fore.RESET}"
            else:
                # Empty space or previously removed
                visual_grid[r][c] = f"{Fore.BLUE}.{Fore.RESET}"
    
    # Convert to string
    visual_str = ""
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            if visual_grid[r][c].startswith('\x1b'):
                # Colorama escape sequence
                row_str += visual_grid[r][c]
            else:
                row_str += visual_grid[r][c]
        visual_str += row_str + "\n"
    
    return visual_str


def part1(content):
    """
    Solution for Part 1: Count rolls of paper accessible by forklifts.
    A roll is accessible if it has fewer than 4 adjacent rolls (@) in the 8 positions around it.
    """
    start_time = time.time()
    
    grid = parse_input(content)
    
    print(f"{Fore.YELLOW}Part 1: Finding accessible rolls of paper...")
    print(f"{Fore.YELLOW}A roll is accessible if it has fewer than 4 adjacent rolls (@)")
    
    accessible = find_accessible_rolls(grid)
    accessible_count = len(accessible)
    
    # Create visualization
    visual_grid = create_visual_grid(grid, accessible, set())
    
    print(f"\n{Fore.CYAN}Grid visualization (accessible rolls marked with 'x'):")
    print(f"{Fore.CYAN}{'='*40}")
    print(visual_grid)
    print(f"{Fore.CYAN}{'='*40}")
    
    print(f"\n{Fore.GREEN}Total accessible rolls: {accessible_count}")
    
    return {
        "value": accessible_count,
        "execution_time": time.time() - start_time,
        "visualization": visual_grid
    }


def simulate_removal_process(grid):
    """
    Simulate the iterative removal process:
    1. Find accessible rolls (< 4 neighbors)
    2. Remove them
    3. Repeat until no accessible rolls remain
    Returns total rolls removed and list of visualizations for each iteration.
    """
    # Create a copy to modify
    current_grid = [row.copy() for row in grid]
    rows = len(grid)
    cols = len(grid[0])
    
    total_removed = 0
    iterations = []
    iteration_number = 1
    
    print(f"\n{Fore.YELLOW}Starting iterative removal process...")
    
    while True:
        # Find accessible rolls in current grid
        accessible = find_accessible_rolls(current_grid)
        
        if not accessible:
            print(f"{Fore.CYAN}No more accessible rolls. Process complete.")
            break
        
        # Remove accessible rolls
        removed_this_iteration = 0
        for r, c in accessible:
            current_grid[r][c] = '.'
            removed_this_iteration += 1
        
        total_removed += removed_this_iteration
        
        # Create visualization for this iteration
        removed_set = set()
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@' and current_grid[r][c] == '.':
                    removed_set.add((r, c))
        
        visual = create_visual_grid(grid, accessible, removed_set)
        
        iterations.append({
            "iteration": iteration_number,
            "removed": removed_this_iteration,
            "total_removed": total_removed,
            "visualization": visual
        })
        
        print(f"{Fore.CYAN}Iteration {iteration_number}: Removed {removed_this_iteration} rolls "
              f"(Total: {total_removed})")
        
        iteration_number += 1
    
    return total_removed, iterations


def part2(content):
    """
    Solution for Part 2: Simulate iterative removal process.
    Keep removing accessible rolls until no more can be removed.
    Count total rolls removed.
    """
    start_time = time.time()
    
    grid = parse_input(content)
    
    print(f"{Fore.YELLOW}Part 2: Simulating iterative removal process...")
    print(f"{Fore.YELLOW}Each iteration: remove accessible rolls, then check again")
    
    total_removed, iterations = simulate_removal_process(grid)
    
    # Print summary of iterations
    print(f"\n{Fore.CYAN}{'='*40}")
    print(f"{Fore.CYAN}Iteration Summary:")
    print(f"{Fore.CYAN}{'='*40}")
    
    for i, iteration in enumerate(iterations[:]): 
        print(f"\n{Fore.YELLOW}Iteration {iteration['iteration']}:")
        print(f"{Fore.GREEN}  Removed: {iteration['removed']}")
        print(f"{Fore.GREEN}  Total so far: {iteration['total_removed']}")
        if i < 2:  # Show visuals for first 2 iterations
            print(f"{Fore.CYAN}  Visualization:")
            print(iteration['visualization'])
    
    if iterations:
        last_iteration = iterations[-1]
        print(f"\n{Fore.CYAN}Final state:")
        print(last_iteration['visualization'])
    
    print(f"\n{Fore.GREEN}Total rolls removed: {total_removed}")
    
    return {
        "value": total_removed,
        "execution_time": time.time() - start_time,
        "iterations": len(iterations),
        "iterations_detail": iterations[:3] if iterations else []
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
            print(f"{Fore.RED}TEST FAILED for {filename} {part_name}")
            print(f"{Fore.RED}  Expected: {expected_value}")
            print(f"{Fore.RED}  Got: {result_value}")
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
    
    print(f"{Fore.CYAN}Processing order: {', '.join(files)}")
    
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
                
                # Add expected value for FAILED status
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    expected_value = TEST_SOLUTIONS.get(file, {}).get(part_name, "N/A")
                    status_text += f" (Expected: {expected_value})"
                    all_tests_passed = False
                elif part_result["status"] == TEST_STATUS["PASSED"]:
                    # Only count test files for overall pass/fail
                    if file.startswith('test'):
                        print(f"{Fore.GREEN}✓ Test {part_name} passed!")
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{part_result['value']:<15} "
                      f"{status_color}{status_text}  "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
                
                # Print additional info for part2
                if part_name == "part2" and "iterations" in part_result:
                    print(f"     {Fore.CYAN}Iterations: {part_result['iterations']}")
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
        sys.exit(1)


if __name__ == "__main__":
    main()