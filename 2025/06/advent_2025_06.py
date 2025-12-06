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
    Parse worksheet with proper handling of multi-digit numbers.
    
    The key insight: Each problem consists of numbers written vertically.
    Problems are separated by empty columns.
    """
    lines = content.rstrip('\n').split('\n')
    
    # Remove empty lines
    lines = [line.rstrip('\n') for line in lines if line.strip() != '']
    
    if not lines:
        return []
    
    # Find operation line (has + or *)
    op_line_idx = -1
    for i, line in enumerate(lines):
        if '+' in line or '*' in line:
            op_line_idx = i
            break
    
    if op_line_idx == -1:
        return []
    
    # Get number lines and operation line
    num_lines = lines[:op_line_idx]
    op_line = lines[op_line_idx]
    
    # Find maximum width
    max_len = max(max(len(line) for line in num_lines), len(op_line))
    
    # Pad all lines to max_len
    padded_nums = [line.ljust(max_len) for line in num_lines]
    padded_op = op_line.ljust(max_len)
    
    # First, identify all operation positions
    op_positions = []
    for col in range(max_len):
        if col < len(padded_op) and padded_op[col] in ('+', '*'):
            op_positions.append(col)
    
    # Group operation positions into problems
    problems = []
    if op_positions:
        # Sort operation positions
        op_positions.sort()
        
        # Group consecutive operation positions (same problem)
        current_group = [op_positions[0]]
        for i in range(1, len(op_positions)):
            # Check if positions are consecutive (same problem)
            if op_positions[i] == op_positions[i-1] + 1:
                current_group.append(op_positions[i])
            else:
                # Check if there's content between them
                has_content_between = False
                for check_col in range(op_positions[i-1] + 1, op_positions[i]):
                    if check_col < len(padded_op) and padded_op[check_col] != ' ':
                        has_content_between = True
                        break
                    for num_line in padded_nums:
                        if check_col < len(num_line) and num_line[check_col] != ' ':
                            has_content_between = True
                            break
                    if has_content_between:
                        break
                
                if has_content_between:
                    # Different problem, process current group
                    process_problem_group(current_group, problems, padded_nums, padded_op, max_len, right_to_left)
                    current_group = [op_positions[i]]
                else:
                    # Same problem, continue grouping
                    current_group.append(op_positions[i])
        
        # Process the last group
        process_problem_group(current_group, problems, padded_nums, padded_op, max_len, right_to_left)
    
    return problems


def process_problem_group(op_cols, problems, padded_nums, padded_op, max_len, right_to_left):
    """Process a group of operation columns as a single problem."""
    if not op_cols:
        return
    
    # Get the operation (should be same for all columns in group)
    operation = None
    for col in op_cols:
        if col < len(padded_op) and padded_op[col] in ('+', '*'):
            operation = padded_op[col]
            break
    
    if not operation:
        return
    
    # Find the full extent of this problem
    # Problem spans from first column with content to last column with content
    start_col = min(op_cols)
    end_col = max(op_cols)
    
    # Expand left to find all content
    while start_col > 0:
        col_has_content = False
        if start_col - 1 < len(padded_op) and padded_op[start_col - 1] != ' ':
            col_has_content = True
        else:
            for num_line in padded_nums:
                if start_col - 1 < len(num_line) and num_line[start_col - 1] != ' ':
                    col_has_content = True
                    break
        
        if not col_has_content:
            break
        start_col -= 1
    
    # Expand right to find all content
    while end_col < max_len - 1:
        col_has_content = False
        if end_col + 1 < len(padded_op) and padded_op[end_col + 1] != ' ':
            col_has_content = True
        else:
            for num_line in padded_nums:
                if end_col + 1 < len(num_line) and num_line[end_col + 1] != ' ':
                    col_has_content = True
                    break
        
        if not col_has_content:
            break
        end_col += 1
    
    # Now extract numbers
    # Each row in padded_nums is a separate number in the problem
    numbers = []
    for row_idx in range(len(padded_nums)):
        # Collect all digits for this number across the problem columns
        digits = []
        for col in range(start_col, end_col + 1):
            if col < len(padded_nums[row_idx]) and padded_nums[row_idx][col].isdigit():
                digits.append(padded_nums[row_idx][col])
        
        if digits:
            if right_to_left:
                # For Part 2: The number is written right-to-left
                # So we need to reverse the order of digits
                digits.reverse()
            
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


def debug_example():
    """Debug the example to understand the format better."""
    example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}DEBUGGING EXAMPLE")
    print(f"{Fore.MAGENTA}{'='*60}")
    
    lines = example.split('\n')
    print(f"{Fore.CYAN}Lines:")
    for i, line in enumerate(lines):
        print(f"  {i}: '{line}'")
    
    # Find operation line
    op_line_idx = -1
    for i, line in enumerate(lines):
        if '+' in line or '*' in line:
            op_line_idx = i
            break
    
    print(f"\n{Fore.CYAN}Operation line index: {op_line_idx}")
    
    if op_line_idx >= 0:
        num_lines = lines[:op_line_idx]
        op_line = lines[op_line_idx]
        
        print(f"\n{Fore.CYAN}Number lines ({len(num_lines)}):")
        for i, line in enumerate(num_lines):
            print(f"  {i}: '{line}'")
        
        print(f"\n{Fore.CYAN}Operation line: '{op_line}'")
        
        # Show column by column
        max_len = max(max(len(l) for l in num_lines), len(op_line))
        print(f"\n{Fore.CYAN}Column analysis (max_len={max_len}):")
        for col in range(max_len):
            col_chars = []
            for i in range(len(num_lines)):
                if col < len(num_lines[i]):
                    col_chars.append(num_lines[i][col])
                else:
                    col_chars.append(' ')
            
            op_char = op_line[col] if col < len(op_line) else ' '
            
            print(f"  Col {col:2d}: nums={''.join(col_chars)} op={op_char}")


def part1(content):
    """
    Solution for Part 1: Solve the problems on the math worksheet.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Solving worksheet problems...")
    
    # For debugging
    if "test_I.txt" in content[:100]:
        debug_example()
    
    # Parse the worksheet
    problems = parse_worksheet(content, right_to_left=False)
    
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
    
    # Print summary
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
    Solution for Part 2: Solve the problems with numbers read right-to-left.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Solving worksheet problems (right-to-left)...")
    
    # Parse the worksheet with right-to-left reading
    problems = parse_worksheet(content, right_to_left=True)
    
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
    
    # Print summary
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