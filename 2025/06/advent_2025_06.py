#!/usr/bin/python3

'''
--- Day 6: Trash Compactor ---
'''

import os
import sys
import time
from colorama import init, Fore    # type: ignore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": '4277556',
        "part2": '3263827',
    },
    "input_I.txt": {
        "part1": '4405895212738', 
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


def parse_worksheet(content, right_to_left=False):
    """
    Parse the worksheet content into separate problems.
    
    Args:
        content: Worksheet content as string
        right_to_left: If True, read numbers right-to-left within each column
    """
    lines = content.rstrip('\n').split('\n')
    
    # Remove completely empty lines
    lines = [line for line in lines if line.strip() != '']
    
    if not lines:
        return []
    
    # Find the operation line (contains + or *)
    op_line_idx = -1
    for idx, line in enumerate(lines):
        if '+' in line or '*' in line:
            op_line_idx = idx
            break
    
    if op_line_idx == -1:
        return []
    
    # Separate number lines and operation line
    num_lines = lines[:op_line_idx]
    op_line = lines[op_line_idx]
    
    # Determine maximum width
    all_lines = num_lines + [op_line]
    max_width = max(len(line) for line in all_lines)
    
    # Pad all lines to max_width
    padded_lines = [line.ljust(max_width) for line in num_lines]
    padded_op_line = op_line.ljust(max_width)
    
    problems = []
    col = 0
    
    while col < max_width:
        # Skip leading spaces
        while col < max_width and all(
            col >= len(line) or line[col] == ' ' 
            for line in padded_lines + [padded_op_line]
        ):
            col += 1
        
        if col >= max_width:
            break
        
        # Start of a problem
        problem_numbers = []
        problem_op = None
        
        # For each number in the problem, we need to collect its digits
        # A number spans multiple columns
        num_count = len(padded_lines)  # Each row is a number in the problem
        
        # Initialize digit collection for each number
        # Each number's digits will be collected across columns
        number_digits = [[] for _ in range(num_count)]
        
        # Process columns until we hit a separator or end
        while col < max_width:
            # Check operation line
            if col < len(padded_op_line) and padded_op_line[col] in ('+', '*'):
                problem_op = padded_op_line[col]
            
            # For right-to-left reading, we need to handle digits differently
            # In normal left-to-right: digits are collected left to right
            # In right-to-left: digits within each column represent different positions
            
            if right_to_left:
                # For Part 2: Digits in a column represent the number read top-to-bottom
                # But each column is a digit position from right to left
                # So we need to reverse how we build numbers
                pass  # We'll handle this differently
            
            # Check number lines and collect digits
            for row_idx, line in enumerate(padded_lines):
                if col < len(line) and line[col].isdigit():
                    number_digits[row_idx].append(line[col])
            
            col += 1
            
            # Check if next column is a separator or end
            if col >= max_width:
                break
            
            # Check if next column is empty for all lines
            next_col_empty = True
            if col < len(padded_op_line) and padded_op_line[col] != ' ':
                next_col_empty = False
            for line in padded_lines:
                if col < len(line) and line[col] != ' ':
                    next_col_empty = False
                    break
            
            if next_col_empty:
                break
        
        # Build numbers from collected digits
        for digits in number_digits:
            if digits:  # Check if we collected any digits
                if right_to_left:
                    # For Part 2: The digits in the list are from left to right columns
                    # But they represent the number written right-to-left
                    # So we need to reverse the digits to get the correct number
                    digits_str = ''.join(digits)
                    # The number is written with most significant digit at top
                    # So we just need to join them in the order we collected
                    try:
                        problem_numbers.append(int(digits_str))
                    except ValueError:
                        pass
                else:
                    # For Part 1: Simple join of digits
                    digits_str = ''.join(digits)
                    try:
                        problem_numbers.append(int(digits_str))
                    except ValueError:
                        pass
        
        # Add problem if valid
        if problem_numbers and problem_op:
            problems.append({
                'numbers': problem_numbers,
                'operation': problem_op
            })
        
        # Skip the separator column
        col += 1
    
    return problems


def solve_problems(problems):
    """
    Solve each problem and return the grand total.
    """
    total_sum = 0
    results = []
    
    for problem in problems:
        numbers = problem['numbers']
        operation = problem['operation']
        
        if not numbers:
            continue
        
        if operation == '+':
            result = sum(numbers)
        elif operation == '*':
            result = 1
            for num in numbers:
                result *= num
        else:
            continue
        
        results.append({
            'numbers': numbers,
            'operation': operation,
            'result': result
        })
        total_sum += result
    
    return total_sum, results


def parse_worksheet_vertical(content, right_to_left=False):
    """
    New approach: Parse worksheet considering numbers are written vertically.
    Each number occupies multiple columns, one column per digit.
    """
    lines = content.rstrip('\n').split('\n')
    
    # Remove completely empty lines
    lines = [line for line in lines if line.strip() != '']
    
    if not lines:
        return []
    
    # Find the operation line
    op_line_idx = -1
    for idx, line in enumerate(lines):
        if '+' in line or '*' in line:
            op_line_idx = idx
            break
    
    if op_line_idx == -1:
        return []
    
    # Separate number lines and operation line
    num_lines = lines[:op_line_idx]
    op_line = lines[op_line_idx]
    
    # Determine maximum width
    max_width = max(max(len(line) for line in num_lines), len(op_line))
    
    # Pad all lines
    padded_lines = [line.ljust(max_width) for line in num_lines]
    padded_op_line = op_line.ljust(max_width)
    
    problems = []
    col = 0
    
    # First, identify problem boundaries by finding operation symbols
    # Operation symbols mark the end (or middle) of problems
    op_positions = []
    for c in range(max_width):
        if c < len(padded_op_line) and padded_op_line[c] in ('+', '*'):
            op_positions.append(c)
    
    # Group operation positions into problems
    # Problems are separated by columns with only spaces
    problem_ranges = []
    if op_positions:
        current_start = op_positions[0]
        for i in range(1, len(op_positions)):
            # Check if there's a gap (separator) between operations
            has_gap = True
            for check_pos in range(op_positions[i-1] + 1, op_positions[i]):
                # Check if any line has non-space in this column
                for line in padded_lines + [padded_op_line]:
                    if check_pos < len(line) and line[check_pos] != ' ':
                        has_gap = False
                        break
                if not has_gap:
                    break
            
            if has_gap:
                # End of current problem
                problem_ranges.append((current_start, op_positions[i-1]))
                current_start = op_positions[i]
        
        # Add the last problem
        problem_ranges.append((current_start, op_positions[-1]))
    
    # For each problem range, extract the numbers
    for start_col, end_col in problem_ranges:
        # Find the operation in this range
        operation = None
        for c in range(start_col, end_col + 1):
            if c < len(padded_op_line) and padded_op_line[c] in ('+', '*'):
                operation = padded_op_line[c]
                break
        
        if not operation:
            continue
        
        # For each number line (row), extract the number
        numbers = []
        for row_idx in range(len(padded_lines)):
            digits = []
            for col_idx in range(start_col, end_col + 1):
                if col_idx < len(padded_lines[row_idx]) and padded_lines[row_idx][col_idx].isdigit():
                    digits.append(padded_lines[row_idx][col_idx])
            
            if digits:
                if right_to_left:
                    # For Part 2: The number is written right-to-left
                    # So we need to read the digits as-is (they're already in correct order)
                    num_str = ''.join(digits)
                else:
                    # For Part 1: The number is written left-to-right normally
                    num_str = ''.join(digits)
                
                if num_str:
                    try:
                        numbers.append(int(num_str))
                    except ValueError:
                        pass
        
        if numbers:
            problems.append({
                'numbers': numbers,
                'operation': operation
            })
    
    return problems


def parse_worksheet_final(content, right_to_left=False):
    """
    Final parser based on the actual description.
    The key insight: Each problem has numbers written vertically.
    For Part 2, each number is written right-to-left in columns.
    """
    lines = content.rstrip('\n').split('\n')
    
    # Remove empty lines
    lines = [line for line in lines if line.strip() != '']
    
    if not lines:
        return []
    
    # Find operation line
    op_line_idx = -1
    for idx, line in enumerate(lines):
        if '+' in line or '*' in line:
            op_line_idx = idx
            break
    
    if op_line_idx == -1:
        return []
    
    num_lines = lines[:op_line_idx]
    op_line = lines[op_line_idx]
    
    # Pad to same width
    max_width = max(max(len(l) for l in num_lines), len(op_line))
    padded_lines = [l.ljust(max_width) for l in num_lines]
    padded_op_line = op_line.ljust(max_width)
    
    # Find all operation positions
    op_cols = []
    for c in range(max_width):
        if c < len(padded_op_line) and padded_op_line[c] in ('+', '*'):
            op_cols.append(c)
    
    # Group into problems (operations separated by empty columns)
    problems = []
    i = 0
    while i < len(op_cols):
        start = op_cols[i]
        # Find end of this problem
        j = i
        while j + 1 < len(op_cols) and op_cols[j+1] - op_cols[j] == 1:
            j += 1
        
        end = op_cols[j]
        
        # Get operation (should be the same for all columns in problem)
        operation = padded_op_line[start]
        
        # Extract numbers for this problem
        numbers = []
        for row in range(len(padded_lines)):
            digits = []
            for col in range(start, end + 1):
                if col < len(padded_lines[row]) and padded_lines[row][col].isdigit():
                    digits.append(padded_lines[row][col])
            
            if digits:
                if right_to_left:
                    # For Part 2: Reverse the digits
                    # Actually, let's think: In the example "64" becomes "46" when read right-to-left
                    # So we need to reverse the order of digits within each number
                    digits.reverse()
                
                num_str = ''.join(digits)
                if num_str:
                    try:
                        numbers.append(int(num_str))
                    except ValueError:
                        pass
        
        if numbers and operation:
            problems.append({
                'numbers': numbers,
                'operation': operation
            })
        
        i = j + 1
    
    return problems


def parse_worksheet_part1(content):
    """Parser for Part 1 (left-to-right reading)"""
    return parse_worksheet_final(content, right_to_left=False)


def parse_worksheet_part2(content):
    """Parser for Part 2 (right-to-left reading)"""
    return parse_worksheet_final(content, right_to_left=True)


def part1(content):
    """
    Solution for Part 1: Solve the problems on the math worksheet (left-to-right).
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Solving worksheet problems (left-to-right)...")
    
    # Parse the worksheet
    problems = parse_worksheet_part1(content)
    
    print(f"{Fore.YELLOW}Number of problems found: {len(problems)}")
    
    if not problems:
        print(f"{Fore.RED}No problems found in worksheet!")
        return {
            "value": 0,
            "execution_time": time.time() - start_time,
            "problems_count": 0,
            "results": []
        }
    
    # Solve each problem
    grand_total, results = solve_problems(problems)
    
    # Print detailed results
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Worksheet Solutions Summary (Part 1):")
    print(f"{Fore.CYAN}{'-'*60}")
    
    max_to_show = min(5, len(results))
    for i in range(max_to_show):
        result = results[i]
        nums = result['numbers']
        op = result['operation']
        res = result['result']
        
        if op == '+':
            expr = ' + '.join(str(n) for n in nums)
        else:
            expr = ' * '.join(str(n) for n in nums)
        
        print(f"{Fore.GREEN}Problem {i+1}: {expr} = {res:,}")
    
    if len(results) > max_to_show:
        print(f"{Fore.YELLOW}... and {len(results) - max_to_show} more problems")
    
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Grand Total: {grand_total:,}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": grand_total,
        "execution_time": time.time() - start_time,
        "problems_count": len(problems),
        "results": results
    }


def part2(content):
    """
    Solution for Part 2: Solve the problems reading numbers right-to-left.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Solving worksheet problems (right-to-left)...")
    
    # Parse the worksheet with right-to-left reading
    problems = parse_worksheet_part2(content)
    
    print(f"{Fore.YELLOW}Number of problems found: {len(problems)}")
    
    if not problems:
        print(f"{Fore.RED}No problems found in worksheet!")
        return {
            "value": 0,
            "execution_time": time.time() - start_time,
            "problems_count": 0,
            "results": []
        }
    
    # Solve each problem
    grand_total, results = solve_problems(problems)
    
    # Print detailed results
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Worksheet Solutions Summary (Part 2):")
    print(f"{Fore.CYAN}{'-'*60}")
    
    max_to_show = min(5, len(results))
    for i in range(max_to_show):
        result = results[i]
        nums = result['numbers']
        op = result['operation']
        res = result['result']
        
        if op == '+':
            expr = ' + '.join(str(n) for n in nums)
        else:
            expr = ' * '.join(str(n) for n in nums)
        
        print(f"{Fore.GREEN}Problem {i+1}: {expr} = {res:,}")
    
    if len(results) > max_to_show:
        print(f"{Fore.YELLOW}... and {len(results) - max_to_show} more problems")
    
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Grand Total: {grand_total:,}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": grand_total,
        "execution_time": time.time() - start_time,
        "problems_count": len(problems),
        "results": results
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
                if isinstance(value, int):
                    value_str = str(value)
                else:
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