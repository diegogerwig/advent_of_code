#!/usr/bin/python3

'''
--- Day 1: Historian Hysteria ---
[El contenido del problema permanece igual]
'''

import os
import sys
import time
from colorama import init, Fore
from tqdm import tqdm
from collections import Counter

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 11,
        "part2": 31,
    },
    "input_I.txt": {
        "part1": "N/A", 
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
    Parse the input content into left and right lists.
    Optimized version using list comprehensions.
    """
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    left_list, right_list = [], []
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            left_list.append(int(parts[0]))
            right_list.append(int(parts[1]))
    
    return left_list, right_list


def calculate_min_total_distance_optimized(left_list, right_list):
    """
    Optimized version of calculate_min_total_distance.
    Uses sorted() and zip() for efficient pairing.
    """
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    
    # Use sum with generator expression for memory efficiency
    return sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))


def calculate_similarity_score_optimized(left_list, right_list):
    """
    Optimized version of calculate_similarity_score.
    Uses Counter for efficient frequency counting.
    """
    right_counter = Counter(right_list)
    
    # Use sum with generator expression
    return sum(num * right_counter[num] for num in left_list)


def part1(content):
    """
    Solution for Part 1 with timing and progress indication
    """
    start_time = time.time()
    
    left_list, right_list = parse_input(content)
    
    print(f"{Fore.YELLOW}Processing Part 1 with {len(left_list)} pairs...")
    result_value = calculate_min_total_distance_optimized(left_list, right_list)
    
    return {
        "value": result_value,
        "execution_time": time.time() - start_time
    }


def part2(content):
    """
    Solution for Part 2 with timing and progress indication
    """
    start_time = time.time()
    
    left_list, right_list = parse_input(content)
    
    print(f"{Fore.YELLOW}Processing Part 2 with {len(left_list)} pairs...")
    result_value = calculate_similarity_score_optimized(left_list, right_list)
    
    return {
        "value": result_value,
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


# Keep original functions for backward compatibility
def calculate_min_total_distance(left_list, right_list):
    """Original function maintained for compatibility"""
    return calculate_min_total_distance_optimized(left_list, right_list)


def calculate_similarity_score(left_list, right_list):
    """Original function maintained for compatibility"""
    return calculate_similarity_score_optimized(left_list, right_list)


if __name__ == "__main__":
    main()