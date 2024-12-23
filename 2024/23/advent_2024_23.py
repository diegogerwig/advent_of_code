'''



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
        "part1": 'N/A',
        "part2": 'N/A',
    },
    "input_I.txt": {
        "part1": 'N/A',
        "part2": 'N/A',
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
    Parse the input content removing empty lines and whitespace
    """
    lines = content.splitlines()  # split by newlines
    result = []
    
    for line in lines:
        clean_line = line.strip()  # remove whitespace at start and end
        if clean_line:  # if line is not empty
            result.append(clean_line)
            
    return result

def part1(content):
    """
    Solution for Part 1
    """
    start_time = time.time()
    
    # Parse input
    data = parse_input(content)
    
    # Your solution logic here
    result = 0
    
    return {
        "value": result,
        "execution_time": time.time() - start_time
    }

def part2(content):
    """
    Solution for Part 2
    """
    start_time = time.time()
    
    # Parse input
    data = parse_input(content)
    
    # Your solution logic here
    result = 0
    
    return {
        "value": result,
        "execution_time": time.time() - start_time
    }

def determine_test_status(result, expected):
    """
    Determine the test status based on the result and expected value.
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
    files = []
    for f in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, f)):
            files.append(f)
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