#!/usr/bin/python3

'''
--- Day 5: Cafeteria ---
'''

import os
import sys
import time
from colorama import init, Fore    # type: ignore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 3,
        "part2": 'N/A',  
    },
    "input_I.txt": {
        "part1": 739, 
        "part2": 'N/A',
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
    Parse the input content into ranges and ingredient IDs.
    Format: ranges, blank line, then IDs.
    """
    sections = content.strip().split('\n\n')
    
    if len(sections) < 2:
        # Try alternative: split by empty line
        lines = content.strip().split('\n')
        separator_idx = None
        for i, line in enumerate(lines):
            if line.strip() == '':
                separator_idx = i
                break
        
        if separator_idx is None:
            raise ValueError("No blank line found in input")
        
        ranges_section = lines[:separator_idx]
        ids_section = lines[separator_idx+1:]
    else:
        ranges_section = sections[0].strip().split('\n')
        ids_section = sections[1].strip().split('\n')
    
    # Parse ranges
    ranges = []
    for line in ranges_section:
        line = line.strip()
        if not line:
            continue
        if '-' in line:
            parts = line.split('-')
            start = int(parts[0].strip())
            end = int(parts[1].strip())
            ranges.append((start, end))
    
    # Parse ingredient IDs
    ingredient_ids = []
    for line in ids_section:
        line = line.strip()
        if not line:
            continue
        ingredient_ids.append(int(line))
    
    return ranges, ingredient_ids


def is_id_fresh(ingredient_id, ranges):
    """
    Check if an ingredient ID is fresh (within any range).
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def part1(content):
    """
    Solution for Part 1: Count how many ingredient IDs are fresh.
    """
    start_time = time.time()
    
    ranges, ingredient_ids = parse_input(content)
    
    print(f"{Fore.YELLOW}Part 1: Counting fresh ingredient IDs...")
    print(f"{Fore.YELLOW}Number of ranges: {len(ranges)}")
    print(f"{Fore.YELLOW}Number of ingredient IDs to check: {len(ingredient_ids)}")
    
    # Count fresh IDs
    fresh_count = 0
    fresh_ids = []
    spoiled_ids = []
    
    for ingredient_id in ingredient_ids:
        if is_id_fresh(ingredient_id, ranges):
            fresh_count += 1
            fresh_ids.append(ingredient_id)
        else:
            spoiled_ids.append(ingredient_id)
    
    # Print detailed results
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Detailed Results:")
    print(f"{Fore.CYAN}{'-'*60}")
    
    if fresh_ids:
        print(f"{Fore.GREEN}✓ Fresh IDs ({len(fresh_ids)}):")
        # Show in groups of 10 for readability
        for i in range(0, len(fresh_ids), 10):
            print(f"  {', '.join(map(str, fresh_ids[i:i+10]))}")
    
    if spoiled_ids:
        print(f"{Fore.RED}✗ Spoiled IDs ({len(spoiled_ids)}):")
        for i in range(0, len(spoiled_ids), 10):
            print(f"  {', '.join(map(str, spoiled_ids[i:i+10]))}")
    
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Total fresh ingredients: {fresh_count}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": fresh_count,
        "execution_time": time.time() - start_time,
        "ranges_count": len(ranges),
        "ids_count": len(ingredient_ids),
        "fresh_ids_count": len(fresh_ids),
        "spoiled_ids_count": len(spoiled_ids)
    }


def part2(content):
    """
    Solution for Part 2: Not defined in the problem statement yet.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Not implemented yet for this problem.")
    
    # For now, just return N/A
    return {
        "value": 'N/A',
        "execution_time": time.time() - start_time,
        "note": "Part 2 not defined in problem statement"
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
            
            # Show more details for failed tests
            if "fresh_ids_count" in result:
                print(f"{Fore.RED}  Fresh IDs count: {result['fresh_ids_count']}")
                print(f"{Fore.RED}  Spoiled IDs count: {result['spoiled_ids_count']}")
            
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
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{part_result['value']:<10} "
                      f"{status_color}{status_text:<20} "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
                
                # Solo mostrar información adicional si el test falló
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    expected_value = TEST_SOLUTIONS.get(file, {}).get(part_name, "N/A")
                    print(f"       {Fore.RED}Expected: {expected_value}")
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
        sys.exit(1)


if __name__ == "__main__":
    main()