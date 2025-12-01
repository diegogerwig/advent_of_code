#!/usr/bin/python3

'''
--- Day 1: Secret Entrance ---
[Full problem description remains the same...]
'''

import os
import sys
import time
from colorama import init, Fore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 3,
        "part2": 6,
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
    Parse the input content into rotation commands.
    Each line starts with L or R followed by a number.
    """
    rotations = []
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    
    for line in lines:
        direction = line[0]  # First character: L or R
        distance = int(line[1:])  # Rest of the string is the number
        rotations.append((direction, distance))
    
    return rotations


def part1(content):
    """
    Solution for Part 1: Count how many times the dial points to 0 AFTER any rotation.
    The dial starts at 50.
    """
    start_time = time.time()
    
    rotations = parse_input(content)
    current_position = 50  # Starting position
    zero_count = 0
    
    print(f"{Fore.YELLOW}Processing Part 1 with {len(rotations)} rotations...")
    
    for direction, distance in rotations:
        # Apply rotation
        if direction == 'R':
            current_position = (current_position + distance) % 100
        else:  # 'L'
            current_position = (current_position - distance) % 100
        
        # Check if dial points to 0 after rotation
        if current_position == 0:
            zero_count += 1
    
    return {
        "value": zero_count,
        "execution_time": time.time() - start_time
    }


def part2_correct(content):
    """
    CORRECT solution for Part 2.
    Count zeros DURING rotation (excluding the final position if it's 0).
    Also count zeros AFTER rotation (if final position is 0).
    """
    start_time = time.time()
    
    rotations = parse_input(content)
    current_position = 50
    total_zero_count = 0
    
    print(f"{Fore.YELLOW}Processing Part 2 with {len(rotations)} rotations...")
    
    for direction, distance in rotations:
        start_pos = current_position
        
        # Count zeros DURING the rotation (excluding final position)
        zeros_during = 0
        
        if direction == 'R':
            # Moving right: check positions from start_pos+1 to start_pos+distance-1
            # (exclude final position which we'll check separately)
            for step in range(1, distance):  # Note: range(1, distance) excludes the final step
                pos = (start_pos + step) % 100
                if pos == 0:
                    zeros_during += 1
            
            # Update position
            current_position = (start_pos + distance) % 100
            
        else:  # 'L'
            # Moving left: check positions from start_pos-1 to start_pos-distance+1
            for step in range(1, distance):  # Exclude final position
                pos = (start_pos - step) % 100
                if pos == 0:
                    zeros_during += 1
            
            # Update position
            current_position = (start_pos - distance) % 100
        
        # Count if ends at 0 (AFTER rotation)
        if current_position == 0:
            total_zero_count += 1  # Count ending at 0
        
        total_zero_count += zeros_during  # Count zeros during rotation
    
    return {
        "value": total_zero_count,
        "execution_time": time.time() - start_time
    }


def part2_optimized(content):
    """
    Optimized version for large distances.
    """
    start_time = time.time()
    
    rotations = parse_input(content)
    current_position = 50
    total_zero_count = 0
    
    print(f"{Fore.YELLOW}Processing Part 2 (optimized) with {len(rotations)} rotations...")
    
    for direction, distance in rotations:
        start_pos = current_position
        
        # Count zeros DURING rotation (excluding final position)
        zeros_during = 0
        
        if direction == 'R':
            if distance > 1:  # Need at least 2 steps to have positions during rotation
                # We're checking positions: start_pos+1 to start_pos+distance-1
                first_check = start_pos + 1
                last_check = start_pos + distance - 1
                
                # Find first multiple of 100 in range
                first_multiple = ((first_check + 99) // 100) * 100
                
                if first_multiple <= last_check:
                    # Count multiples of 100 in the range
                    zeros_during = 1 + (last_check - first_multiple) // 100
            
            current_position = (start_pos + distance) % 100
            
        else:  # 'L'
            if distance > 1:
                # We're checking positions: start_pos-1 down to start_pos-distance+1
                # Equivalent to checking when (start_pos - step) % 100 == 0
                # for step in range(1, distance)
                
                # First step that gives position 0
                first_step = start_pos % 100
                if first_step == 0:
                    first_step = 100  # Next occurrence
                
                if first_step < distance:  # Note: < not <= because we exclude step=distance
                    zeros_during = 1 + (distance - 1 - first_step) // 100
            
            current_position = (start_pos - distance) % 100
        
        # Count if ends at 0
        if current_position == 0:
            total_zero_count += 1
        
        total_zero_count += zeros_during
    
    return {
        "value": total_zero_count,
        "execution_time": time.time() - start_time
    }


def verify_example():
    """
    Manually verify the example from the problem
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Verifying Example from Problem")
    print(f"{Fore.CYAN}{'='*80}")
    
    example = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
    
    rotations = parse_input(example)
    
    # Expected from problem description:
    # 1. L68: during=1, end=0
    # 2. L30: during=0, end=0
    # 3. R48: during=0, end=1 (ends at 0)
    # 4. L5: during=0, end=0
    # 5. R60: during=1, end=0
    # 6. L55: during=0, end=1 (ends at 0)
    # 7. L1: during=0, end=0
    # 8. L99: during=0, end=1 (ends at 0)
    # 9. R14: during=0, end=0
    # 10. L82: during=1, end=0
    
    current = 50
    total = 0
    
    print(f"Start: {current}")
    
    moves_info = [
        ("L68", 1, 0), ("L30", 0, 0), ("R48", 0, 1), 
        ("L5", 0, 0), ("R60", 1, 0), ("L55", 0, 1),
        ("L1", 0, 0), ("L99", 0, 1), ("R14", 0, 0),
        ("L82", 1, 0)
    ]
    
    for i, ((direction, distance), (exp_during, exp_end)) in enumerate(zip(rotations, moves_info)):
        start = current
        during = 0
        
        # Count zeros during (excluding final position)
        if direction == 'R':
            for step in range(1, distance):
                if (start + step) % 100 == 0:
                    during += 1
            current = (start + distance) % 100
        else:
            for step in range(1, distance):
                if (start - step) % 100 == 0:
                    during += 1
            current = (start - distance) % 100
        
        end = 1 if current == 0 else 0
        
        # Verify
        status = "✓" if during == exp_during and end == exp_end else "✗"
        color = Fore.GREEN if status == "✓" else Fore.RED
        
        print(f"{color}{status} Move {i+1}: {direction}{distance}")
        print(f"  From {start} to {current}")
        print(f"  Zeros during: {during} (expected: {exp_during})")
        print(f"  Ends at zero: {end} (expected: {exp_end})")
        
        total += during + end
    
    print(f"\n{Fore.YELLOW}Total zeros: {total} (expected: 6)")
    return total == 6


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
            # Use optimized version for efficiency
            part2_result = part2_optimized(content)
            
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
            
            # Special verification for test_I.txt
            if filename == "test_I.txt":
                print(f"\n{Fore.YELLOW}Verifying example from problem...")
                if verify_example():
                    print(f"{Fore.GREEN}✓ Example verification passed!")
                else:
                    print(f"{Fore.RED}✗ Example verification failed!")
            
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
        # Verify the example first
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}Initial Verification")
        print(f"{Fore.CYAN}{'='*80}")
        verify_example()
        
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