#!/usr/bin/python3

'''
--- Day 3: Mull It Over ---
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its content (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's content has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted content:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted content for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

--- Part Two ---
As you scan through the corrupted content, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted content is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
'''

import os
from colorama import init, Fore

init(autoreset=True)


import re

def sum_valid_mul_results(content: str) -> int:
    """
    Computes the sum of valid `mul(X,Y)` operations in the given conetnt string.
    """
    # Regex pattern to match multiplication operations:
        # 1. 'mul' - literal text
        # 2. '(' - opening parenthesis
        # 3. (\d{1,3}) - first number (1-3 digits)
        # 4. ',' - comma separator
        # 5. (\d{1,3}) - second number (1-3 digits)
        # 6. ')' - closing parenthesis
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    
    # Find all matches
    matches = re.findall(pattern, content)

    total_sum = 0

    for x, y in matches:
        total_sum += int(x) * int(y)
    
    return total_sum


def sum_valid_mul_results_with_control(content: str) -> int:
    """
    Computes the sum of valid and enabled `mul(X,Y)` operations in the given content string,
    considering the effect of `do()` and `don't()` instructions.
    """
    pos = 0
    enabled = True  # Instructions start enabled
    total_sum = 0
    
    while pos < len(content):
        # Check for do()
        if content[pos:].startswith('do()'):
            enabled = True
            pos += 4
            continue
            
        # Check for don't() - be careful not to match 'undo()'
        if content[pos:].startswith("don't()"):
            enabled = False
            pos += 7
            continue
            
        # Check for mul(X,Y)
        if content[pos:].startswith('mul('):
            pos += 4
            # Extract numbers
            num1 = ''
            while pos < len(content) and content[pos].isdigit():
                num1 += content[pos]
                pos += 1
                
            # Must be followed by comma
            if pos < len(content) and content[pos] == ',':
                pos += 1
                num2 = ''
                while pos < len(content) and content[pos].isdigit():
                    num2 += content[pos]
                    pos += 1
                    
                # Must be followed by closing parenthesis
                if pos < len(content) and content[pos] == ')' and num1 and num2:
                    if enabled:
                        total_sum += int(num1) * int(num2)
                    pos += 1
                    continue
                    
        pos += 1
        
    return total_sum


def process_file(filepath):
    """
    Processes a single file containing reports and counts:
    - Total sum of all mul operations
    - Total sum of enabled mul operations considering do/don't controls
    """
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = sum_valid_mul_results(content)
        part2_result = sum_valid_mul_results_with_control(content)
        return part1_result, part2_result


def process_directory(input_dir="./input/"):
    """
    Processes all files in the specified directory.
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    results = {}
    
    for file in files:
        filepath = os.path.join(input_dir, file)
        try:
            part1_result, part2_result = process_file(filepath)
            results[file] = (True, part1_result, part2_result)
        except Exception as e:
            results[file] = (False, str(e))
    
    return results


if __name__ == "__main__":
    input_dir = "./input/"
    results = process_directory(input_dir)
    
    for file, result in results.items():
        if result[0]:  # Successfully processed
            part1, part2 = result[1], result[2]
            print(f"{Fore.BLUE}{file}:")
            print(f"  {Fore.YELLOW}Part 1 (Sum valid mul results): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Sum valid mul results with control): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
