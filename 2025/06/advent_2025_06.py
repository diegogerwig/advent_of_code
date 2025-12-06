#!/usr/bin/python3

'''
--- Day 6: Trash Compactor ---

After helping the Elves in the kitchen, you were taking a break and helping them re-enact a movie scene when you over-enthusiastically jumped into the garbage chute!

A brief fall later, you find yourself in a garbage smasher. Unfortunately, the door's been magnetically sealed.

As you try to find a way out, you are approached by a family of cephalopods! They're pretty sure they can get the door open, but it will take some time. While you wait, they're curious if you can help the youngest cephalopod with her math homework.

Cephalopod math doesn't look that different from normal math. The math worksheet (your puzzle input) consists of a list of problems; each problem has a group of numbers that need to be either added (+) or multiplied (*) together.

However, the problems are arranged a little strangely; they seem to be presented next to each other in a very long horizontal list. For example:

123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation that needs to be performed. Problems are separated by a full column of only spaces. The left/right alignment of numbers within each problem can be ignored.

So, this worksheet contains four problems:

123 * 45 * 6 = 33210
328 + 64 + 98 = 490
51 * 387 * 215 = 4243455
64 + 23 + 314 = 401
To check their work, cephalopod students are given the grand total of adding together all of the answers to the individual problems. In this worksheet, the grand total is 33210 + 490 + 4243455 + 401 = 4277556.

Of course, the actual worksheet is much wider. You'll need to make sure to unroll it completely so that you can read the problems clearly.

Solve the problems on the math worksheet. What is the grand total found by adding together all of the answers to the individual problems?


--- Part Two ---

The big cephalopods come back to check on how things are going. When they see that your grand total doesn't match the one expected by the worksheet, they realize they forgot to explain how to read cephalopod math.

Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the most significant digit at the top and the least significant digit at the bottom. (Problems are still separated with a column consisting only of spaces, and the symbol at the bottom of the problem is still the operator to use.)

Here's the example worksheet again:

123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
Reading the problems right-to-left one column at a time, the problems are now quite different:

The rightmost problem is 4 + 431 + 623 = 1058
The second problem from the right is 175 * 581 * 32 = 3253600
The third problem from the right is 8 + 248 + 369 = 625
Finally, the leftmost problem is 356 * 24 * 1 = 8544
Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

Solve the problems on the math worksheet again. What is the grand total found by adding together all of the answers to the individual problems?
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
        "part2": '7450962489289',  
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


def parse_worksheet_part1(content):
    """
    Parse worksheet for Part 1 (left-to-right reading).
    Problems are separated by empty columns. Numbers are read horizontally.
    """
    lines = content.rstrip('\n').split('\n')
    lines = [line for line in lines if line.strip() != '']
    
    # Find operation line (has + or *)
    for i, line in enumerate(lines):
        if '+' in line or '*' in line:
            op_line_idx = i
            break
    
    num_lines = lines[:op_line_idx]
    op_line = lines[op_line_idx]
    
    # Pad all lines to same width
    width = max(len(line) for line in num_lines + [op_line])
    num_lines = [line.ljust(width) for line in num_lines]
    op_line = op_line.ljust(width)
    
    problems = []
    col = 0
    
    while col < width:
        # Skip empty columns (problem separators)
        if all(line[col] == ' ' for line in num_lines + [op_line]):
            col += 1
            continue
        
        # Start of a new problem
        start_col = col
        operation = None
        
        # Find where this problem ends
        while col < width:
            if op_line[col] in ('+', '*'):
                operation = op_line[col]
            
            col += 1
            
            if col >= width:
                break
            
            # Check if next column is empty (end of problem)
            next_empty = True
            if op_line[col] != ' ':
                next_empty = False
            else:
                for line in num_lines:
                    if line[col] != ' ':
                        next_empty = False
                        break
            
            if next_empty:
                break
        
        # Extract numbers from this problem area
        numbers = []
        for row in num_lines:
            digits = ''
            for c in range(start_col, col):
                if row[c].isdigit():
                    digits += row[c]
            if digits:
                numbers.append(int(digits))
        
        if numbers and operation:
            problems.append({
                'numbers': numbers,
                'operation': operation
            })
        
        # Skip separator column
        col += 1
    
    return problems


def parse_worksheet_part2_final(content):
    """
    Parse worksheet for Part 2 (right-to-left column reading).
    Problems are separated by empty columns. Numbers are built by reading columns
    from right to left, top to bottom.
    """
    lines = content.rstrip('\n').split('\n')
    lines = [line for line in lines if line.strip() != '']
    
    # Find operation line (has + or *)
    for i, line in enumerate(lines):
        if '+' in line or '*' in line:
            op_line_idx = i
            break
    
    num_lines = lines[:op_line_idx]
    op_line = lines[op_line_idx]
    
    # Pad all lines to same width
    width = max(len(line) for line in num_lines + [op_line])
    num_lines = [line.ljust(width) for line in num_lines]
    op_line = op_line.ljust(width)
    
    problems = []
    col = 0
    
    while col < width:
        # Skip empty columns (problem separators)
        if all(line[col] == ' ' for line in num_lines + [op_line]):
            col += 1
            continue
        
        # Start of a new problem
        start_col = col
        operation = None
        
        # Find where this problem ends
        while col < width:
            if op_line[col] in ('+', '*'):
                operation = op_line[col]
            
            col += 1
            
            if col >= width:
                break
            
            # Check if next column is empty (end of problem)
            next_empty = True
            if op_line[col] != ' ':
                next_empty = False
            else:
                for line in num_lines:
                    if line[col] != ' ':
                        next_empty = False
                        break
            
            if next_empty:
                break
        
        end_col = col - 1
        
        # For Part 2: Read columns from right to left
        # Each column forms one number (digits read top to bottom)
        numbers = []
        
        # Process columns from rightmost to leftmost
        for current_col in range(end_col, start_col - 1, -1):
            digits = ''
            
            # Read digits from top to bottom in this column
            for row in num_lines:
                if row[current_col].isdigit():
                    digits += row[current_col]
            
            if digits:
                numbers.append(int(digits))
        
        if numbers and operation:
            problems.append({
                'numbers': numbers,
                'operation': operation
            })
        
        # Skip separator column
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


def part1(content):
    """
    Solution for Part 1: Solve the problems on the math worksheet.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Solving worksheet problems...")
    
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
    
    # Parse the worksheet
    problems = parse_worksheet_part2_final(content)
    
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