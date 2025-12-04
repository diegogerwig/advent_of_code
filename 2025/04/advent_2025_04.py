#!/usr/bin/python3

'''
--- Day 4: Printing Department ---
You ride the escalator down to the printing department. They're clearly getting 
ready for Christmas; they have lots of large rolls of paper everywhere, and 
there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really 
need is a way to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. 
"We're pretty sure there's a cafeteria on the other side of the back wall. If we could 
break through the wall, you'd be able to keep moving. It's too bad all of our forklifts 
are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare 
to break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram 
(your puzzle input) indicating where everything is located.

The forklifts can only access a roll of paper if there are fewer than four rolls of paper 
in the eight adjacent positions. If you can figure out which rolls of paper the forklifts 
can access, they'll spend less time looking and more time breaking down the wall to the cafeteria.

In the example, there are 13 rolls of paper that can be accessed by a forklift.
'''

import os
import sys
import time
from colorama import init, Fore   

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 13,
        "part2": 43,  
    },
    "input_I.txt": {
        "part1": 1384, 
        "part2": "N/A",
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
    return [line.strip() for line in lines if line.strip()]


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
    Returns count of accessible rolls and a visual representation.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    count = 0
    visual_grid = [list(row) for row in grid]
    
    print(f"{Fore.YELLOW}Processing grid of size {rows}x{cols}...")
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                adjacent_rolls = count_adjacent_rolls(grid, r, c)
                
                # Forklift can access if fewer than 4 adjacent rolls
                if adjacent_rolls < 4:
                    count += 1
                    # Mark accessible roll (keep original character in visual)
                    visual_grid[r][c] = f"{Fore.GREEN}x{Fore.RESET}"
                else:
                    # Keep inaccessible roll as '@'
                    visual_grid[r][c] = f"{Fore.RED}@{Fore.RESET}"
            else:
                # Empty space
                visual_grid[r][c] = f"{Fore.BLUE}.{Fore.RESET}"
    
    # Create visual representation as string
    visual_str = ""
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            if visual_grid[r][c].startswith('\x1b'):
                # Colorama escape sequence - just append
                row_str += visual_grid[r][c]
            else:
                row_str += visual_grid[r][c]
        visual_str += row_str + "\n"
    
    return count, visual_str


def part1(content):
    """
    Solution for Part 1: Count rolls of paper accessible by forklifts.
    A roll is accessible if it has fewer than 4 adjacent rolls (@) in the 8 positions around it.
    """
    start_time = time.time()
    
    grid = parse_input(content)
    
    print(f"{Fore.YELLOW}Part 1: Finding accessible rolls of paper...")
    print(f"{Fore.YELLOW}A roll is accessible if it has fewer than 4 adjacent rolls (@)")
    
    accessible_count, visual_grid = find_accessible_rolls(grid)
    
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


def part2(content):
    """
    Solution for Part 2: Placeholder for now.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Not implemented yet")
    
    return {
        "value": "N/A",
        "execution_time": time.time() - start_time
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