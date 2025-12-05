#!/usr/bin/python3

'''
--- Day 5: Cafeteria ---

As the forklifts break through the wall, the Elves are delighted to discover that there was a cafeteria on the other side after all.

You can hear a commotion coming from the kitchen. "At this rate, we won't have any time left to put the wreaths up in the dining hall!" Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system right before Christmas!" another Elf exclaims. You ask what's going on.

The Elves in the kitchen explain the situation: because of their complicated new inventory management system, they can't figure out which of their ingredients are fresh and which are spoiled. When you ask how it works, they give you a copy of their database (your puzzle input).

The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs. For example:

3-5
10-14
16-20
12-18

1
5
8
11
17
32
The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.

The Elves are trying to determine which of the available ingredient IDs are fresh. In this example, this is done as follows:

Ingredient ID 1 is spoiled because it does not fall into any range.
Ingredient ID 5 is fresh because it falls into range 3-5.
Ingredient ID 8 is spoiled.
Ingredient ID 11 is fresh because it falls into range 10-14.
Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
Ingredient ID 32 is spoiled.
So, in this example, 3 of the available ingredient IDs are fresh.

Process the database file from the new inventory management system. How many of the available ingredient IDs are fresh?


--- Part Two ---

The Elves start bringing their spoiled inventory to the trash chute at the back of the kitchen.

So that they can stop bugging you when they get new inventory, the Elves would like to know all of the IDs that the fresh ingredient ID ranges consider to be fresh. An ingredient ID is still considered fresh if it is in any range.

Now, the second section of the database (the available ingredient IDs) is irrelevant. Here are the fresh ingredient ID ranges from the above example:

3-5
10-14
16-20
12-18
The ingredient IDs that these ranges consider to be fresh are 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20. So, in this example, the fresh ingredient ID ranges consider a total of 14 ingredient IDs to be fresh.

Process the database file again. How many ingredient IDs are considered to be fresh according to the fresh ingredient ID ranges?
'''

import os
import sys
import time
from colorama import init, Fore    # type: ignore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 3,
        "part2": 14,
    },
    "input_I.txt": {
        "part1": 739, 
        "part2": 344486348901788,  
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


def parse_input(content, include_ids=True):
    """
    Parse the input content into ranges and optionally ingredient IDs.
    Format: ranges, blank line, then IDs.
    """
    # First, try to split by double newline
    sections = content.strip().split('\n\n')
    
    if len(sections) >= 2:
        # We have a clear separation with double newline
        ranges_section = sections[0].strip()
        ids_section = sections[1].strip() if include_ids and len(sections) > 1 else ""
    
    # Parse ranges
    ranges = []
    for line in ranges_section.split('\n'):
        line = line.strip()
        if not line:
            continue
        if '-' in line:
            parts = line.split('-')
            try:
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                ranges.append((start, end))
            except ValueError:
                continue
        elif include_ids:
            continue
    
    # Parse ingredient IDs 
    ingredient_ids = []
    if include_ids and ids_section:
        for line in ids_section.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                ingredient_ids.append(int(line))
            except ValueError:
                continue
    
    return ranges, ingredient_ids


def is_id_fresh(ingredient_id, ranges):
    """
    Check if an ingredient ID is fresh (within any range).
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def merge_ranges(ranges):
    """
    Merge overlapping ranges to get non-overlapping ranges.
    Returns a list of merged ranges.
    """
    if not ranges:
        return []
    
    # Sort ranges by start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    
    merged = []
    current_start, current_end = sorted_ranges[0]
    
    for start, end in sorted_ranges[1:]:
        if start <= current_end + 1:  # Ranges overlap or are adjacent
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    
    merged.append((current_start, current_end))
    return merged


def count_fresh_ids_from_ranges(ranges):
    """
    Count all unique ingredient IDs that are within any range.
    """
    if not ranges:
        return 0
    
    # Merge ranges to avoid counting overlaps multiple times
    merged = merge_ranges(ranges)
    
    # Count total IDs in all merged ranges
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    
    return total


def get_min_max_ids(ranges):
    """
    Get minimum and maximum IDs from ranges without creating huge lists.
    """
    if not ranges:
        return None, None
    
    min_id = float('inf')
    max_id = float('-inf')
    
    for start, end in ranges:
        if start < min_id:
            min_id = start
        if end > max_id:
            max_id = end
    
    return min_id, max_id


def part1(content):
    """
    Solution for Part 1: Count how many available ingredient IDs are fresh.
    """
    start_time = time.time()
    
    ranges, ingredient_ids = parse_input(content, include_ids=True)
    
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
    Solution for Part 2: Count all ingredient IDs considered fresh by the ranges.
    Ignores the available ingredient IDs list.
    """
    start_time = time.time()
    
    # For part 2, we only need the ranges
    ranges, _ = parse_input(content, include_ids=False)
    
    print(f"{Fore.YELLOW}Part 2: Counting all fresh ingredient IDs from ranges...")
    print(f"{Fore.YELLOW}Number of ranges: {len(ranges)}")
    
    # Merge ranges for efficiency
    merged_ranges = merge_ranges(ranges)
    
    print(f"{Fore.YELLOW}Number of merged ranges: {len(merged_ranges)}")
    
    # Count all unique IDs in ranges
    total_fresh = count_fresh_ids_from_ranges(ranges)
    
    # Print detailed results
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Ranges Analysis:")
    print(f"{Fore.CYAN}{'-'*60}")
    
    if merged_ranges:
        print(f"{Fore.GREEN}Merged ranges ({len(merged_ranges)}):")
        for i, (start, end) in enumerate(merged_ranges):
            range_size = end - start + 1
            print(f"  {i+1:3d}. {start:,}-{end:,} ({range_size:,} IDs)")
    
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Total fresh ingredient IDs from all ranges: {total_fresh:,}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": total_fresh,
        "execution_time": time.time() - start_time,
        "ranges_count": len(ranges),
        "merged_ranges_count": len(merged_ranges)
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
            print(f"{Fore.RED}  Expected: {expected_value:,}")
            print(f"{Fore.RED}  Got: {result_value:,}")
            
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
                
                # Mostrar números sin comas
                value_str = str(part_result['value'])
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{value_str:<20} "
                      f"{status_color}{status_text:<20} "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
                
                # Solo mostrar información adicional si el test falló
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