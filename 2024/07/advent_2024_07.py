#!/usr/bin/python3

'''
--- Day 7: Bridge Repair ---
The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

--- Part Two ---
The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
192: 17 8 14 can be made true using 17 || 8 + 14.
Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
'''

import os
from colorama import init, Fore

init(autoreset=True)

from itertools import product
from tqdm import tqdm


def evaluate_expression(numbers, operators):
    """
    Evaluates an expression given numbers and operators.
    Operates left-to-right, ignoring precedence rules.
    """
    result = numbers[0]
    
    for i in range(len(operators)):
        if operators[i] == '+':
            result += numbers[i + 1]
        elif operators[i] == '*':
            result *= numbers[i + 1]
        elif operators[i] == '||':
            # Concatenate numbers as strings, then convert back to integer
            result = int(str(result) + str(numbers[i + 1]))
    
    return result


def is_valid_equation(target, numbers, include_concat=False):
    """
    Checks if any combination of operators between numbers evaluates to the target.
    By default, includes only addition (+) and multiplication (*).
    If include_concat is True, also includes concatenation (||).
    """
    operators = ['+', '*']
    if include_concat:
        operators.append('||')
    
    num_operators = len(numbers) - 1
    combinations = product(operators, repeat=num_operators)

    for operator in combinations:
        if evaluate_expression(numbers, operator) == target:
            return True

    return False


def calibration(content):
    """
    Processes the input and calculates the total calibration result.
    Includes only addition (+) and multiplication (*).
    """
    total = 0
    lines = content.split('\n')

    for line in tqdm(lines, desc="Calibration", unit="line"):
        if ':' in line:
            parts = line.split(':')
            target = int(parts[0].strip())

            numbers = []
            for n in parts[1].strip().split():
                numbers.append(int(n))

            if is_valid_equation(target, numbers, include_concat=False):
                total += target

    return total


def calibration_concat(content):
    """
    Processes the input and calculates the total calibration result,
    including addition (+), multiplication (*), and concatenation (||).
    """
    total = 0
    lines = content.split('\n')

    for line in tqdm(lines, desc="Calibration", unit="line"):
        if ':' in line:
            parts = line.split(':')
            target = int(parts[0].strip())

            numbers = []
            for n in parts[1].strip().split():
                numbers.append(int(n))

            if is_valid_equation(target, numbers, include_concat=True):
                total += target

    return total


def process_file(filepath):
    """
    Processes the specified file.
    -
    - Returns the total calibration result using add (+) and multiply (*) operators.
    - Returns the total calibration result using add (+) and multiply (*) operators, as well as the concatenation operator (||).
    """
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = calibration(content)
        part2_result = calibration_concat(content)
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
            print(f"  {Fore.YELLOW}Part 1 (Calibration Result): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Calibration Result with concat values): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
