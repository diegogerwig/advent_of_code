#!/usr/bin/python3

'''
--- Day 2: Gift Shop ---

'''

import os
import sys
import time
from colorama import init, Fore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 1227775554,
        "part2": 4174379265,
    },
    "input_I.txt": {
        "part1": 29818212493, 
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
    Parse the input content into ID ranges.
    Each range is separated by commas and has format start-end.
    """
    ranges = []
    # Remove all whitespace and split by commas
    content = content.replace('\n', '').replace(' ', '')
    if not content:
        return ranges
    
    range_strings = content.split(',')
    
    for range_str in range_strings:
        if range_str:
            start, end = map(int, range_str.split('-'))
            ranges.append((start, end))
    
    return ranges


def is_repeated_number_part1(num):
    """
    Check if a number is made only of some sequence of digits repeated exactly twice.
    Examples: 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
    """
    num_str = str(num)
    length = len(num_str)
    
    # A number must have even length to be a repetition of exactly 2 parts
    if length % 2 != 0:
        return False
    
    half_length = length // 2
    first_half = num_str[:half_length]
    second_half = num_str[half_length:]
    
    return first_half == second_half


def is_repeated_number_part2(num):
    """
    Check if a number is made only of some sequence of digits repeated at least twice.
    Examples: 
    - 12341234 (1234 two times)
    - 123123123 (123 three times)
    - 1212121212 (12 five times)
    - 1111111 (1 seven times)
    """
    num_str = str(num)
    length = len(num_str)
    
    # Try all possible pattern lengths from 1 to len(num_str)//2
    # The pattern must repeat at least twice, so max pattern length is length//2
    for pattern_len in range(1, length // 2 + 1):
        # Check if length is divisible by pattern_len
        if length % pattern_len != 0:
            continue
            
        pattern = num_str[:pattern_len]
        repeats = length // pattern_len
        
        # Check if the entire number is the pattern repeated 'repeats' times
        if num_str == pattern * repeats:
            return True
    
    return False


def part1(content):
    """
    Solution for Part 1: Find all invalid IDs that appear in the given ranges.
    Invalid IDs are numbers made of a sequence of digits repeated exactly twice.
    """
    start_time = time.time()
    
    ranges = parse_input(content)
    total_sum = 0
    
    print(f"{Fore.YELLOW}Processing Part 1 with {len(ranges)} ranges...")
    
    for start, end in ranges:
        print(f"{Fore.CYAN}  Processing range {start}-{end}")
        invalid_in_range = 0
        
        for num in range(start, end + 1):
            if is_repeated_number_part1(num):
                total_sum += num
                invalid_in_range += 1
        
        if invalid_in_range > 0:
            print(f"{Fore.GREEN}    Found {invalid_in_range} invalid IDs in this range")
    
    print(f"{Fore.YELLOW}Total sum of invalid IDs: {total_sum}")
    
    return {
        "value": total_sum,
        "execution_time": time.time() - start_time
    }


def part2(content):
    """
    Solution for Part 2: Find all invalid IDs using new rules.
    Invalid IDs are numbers made of a sequence of digits repeated at least twice.
    """
    start_time = time.time()
    
    ranges = parse_input(content)
    total_sum = 0
    
    print(f"{Fore.YELLOW}Processing Part 2 with {len(ranges)} ranges...")
    print(f"{Fore.YELLOW}New rules: sequence repeated at least twice (e.g., 111, 1212, 123123123)")
    
    for start, end in ranges:
        print(f"{Fore.CYAN}  Processing range {start}-{end}")
        invalid_in_range = 0
        
        for num in range(start, end + 1):
            if is_repeated_number_part2(num):
                total_sum += num
                invalid_in_range += 1
        
        if invalid_in_range > 0:
            print(f"{Fore.GREEN}    Found {invalid_in_range} invalid IDs in this range")
    
    print(f"{Fore.YELLOW}Total sum of invalid IDs: {total_sum}")
    
    return {
        "value": total_sum,
        "execution_time": time.time() - start_time
    }


def determine_test_status(result, expected, filename, part_name):
    """
    Determine the test status based on the result and expected value.
    """
    if expected == 'N/A':
        return TEST_STATUS["IN_PROGRESS"]
    
    result_value = result["value"]
    
    if result_value == expected:
        return TEST_STATUS["PASSED"]
    else:
        print(f"{Fore.RED}TEST FAILED for {filename} {part_name}")
        print(f"{Fore.RED}  Expected: {expected}")
        print(f"{Fore.RED}  Got: {result_value}")
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