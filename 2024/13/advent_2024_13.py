'''
--- Day 13: Claw Contraption ---
Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.
The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

--- Part Two ---
As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
'''

#!/usr/bin/python3

import os
from colorama import init, Fore
from tqdm import tqdm
import inspect
import time

init(autoreset=True)

CURRENT_FILEPATH = ""


def print_processing_header(filename, function_name):
    """
    Prints a formatted header for the current processing operation
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Function: {Fore.YELLOW}{function_name}")
    print(f"{Fore.CYAN}{'='*80}\n")


def tokens(file_content):
    """
    Calculates the minimum total tokens needed to win all possible prizes from the claw machines.
    Use brute force to find the minimum number of tokens needed to win all possible prizes.
    """
    start_time = time.time()

    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 1 - {current_func}")

    # List to store all machines
    machines = []
    # Temporary dictionary to store current machine data
    current_machine = {}
    
    # Read file line by line
    for line in file_content.split('\n'):
        # Skip empty lines
        if not line.strip():
            continue
            
        # If we find Button A information
        if line.startswith('Button A:'):
            current_machine = {}  # Start a new machine
            # Example line: "Button A: +2, +4"
            x, y = line.split(':')[1].strip().split(',')
            current_machine['Ax'] = int(x.split('+')[1])  # Save the 2
            current_machine['Ay'] = int(y.split('+')[1])  # Save the 4
            
        # If we find Button B information
        elif line.startswith('Button B:'):
            # Example line: "Button B: +3, -1"
            x, y = line.split(':')[1].strip().split(',')
            current_machine['Bx'] = int(x.split('+')[1])
            current_machine['By'] = int(y.split('+')[1])
            
        # If we find Prize information
        elif line.startswith('Prize:'):
            # Example line: "Prize: x=10, y=2"
            x, y = line.split(':')[1].strip().split(',')
            current_machine['target_x'] = int(x.split('=')[1])
            current_machine['target_y'] = int(y.split('=')[1])
            # Save the complete machine in our list
            machines.append(current_machine)

    # Initialize variables for calculating total
    total_tokens = 0
    max_attempts = 100  # Maximum number of times we can press each button

    print("\nResults:")
    print("-" * 80)
    print(f"{'Machine':<10} {'Button A':<12} {'Button B':<12} {'Tokens':<12} {'Target X':<12} {'Target Y':<12}")
    print("-" * 80)

    # For each machine in our list
    for number, machine in enumerate(machines, 1):
        found_solution = False
        min_tokens = float('inf')  # Start with infinity value to find the cheapest solution
        best_solution = None
        
        # Try all possible combinations of pressing A and B
        for presses_a in range(max_attempts + 1):
            for presses_b in range(max_attempts + 1):
                # Calculate final position after pressing buttons
                position_x = presses_a * machine['Ax'] + presses_b * machine['Bx']
                position_y = presses_a * machine['Ay'] + presses_b * machine['By']
                
                # If we reach the target position
                if position_x == machine['target_x'] and position_y == machine['target_y']:
                    # Calculate how many tokens we spent (A costs 3, B costs 1)
                    tokens_used = presses_a * 3 + presses_b * 1
                    # If this is the cheapest solution so far
                    if tokens_used < min_tokens:
                        min_tokens = tokens_used
                        best_solution = (presses_a, presses_b)
                        found_solution = True
        
        # If we found a solution for this machine
        if found_solution:
            total_tokens += min_tokens
            presses_a, presses_b = best_solution
            print(f"{number:<10} {presses_a:<12} {presses_b:<12} {min_tokens:<12} {machine['target_x']:<12} {machine['target_y']:<12}")
        else:
            print(f"{Fore.RED}{number:<10} {'-':<12} {'-':<12} {'-':<12} {machine['target_x']:<12} {machine['target_y']:<12}")

    execution_time = time.time() - start_time
    return total_tokens, execution_time


def gcd(a, b):
    """
    Calculate Greatest Common Divisor
    Greatest Common Divisor is the largest number that divides both numbers
    """
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    """
    Calculate Least Common Multiple
    Least Common Multiple is the smallest number that is divisible by both numbers
    """
    return abs(a * b) // gcd(a, b)


def determinant(ax, ay, bx, by):
    """
    Calculate determinant of the system
    Determinant means the area of the parallelogram formed by the two vectors
    """
    return ax * by - ay * bx


def solve_machine_large(ax, ay, bx, by, tx, ty):
    """
    Solve for large numbers without press limit.
    Uses Cramer's rule to solve the system of equations:
    ax * n + bx * m = tx
    ay * n + by * m = ty
    """
    # Calculate determinant
    # If the determinant is zero, there is no solution
    det = determinant(ax, ay, bx, by)
    if det == 0:
        return None
    
    # Check if solution exists using GCD
    # If target positions are not divisible by the GCD of the button values, there is no solution
    gcd_x = gcd(ax, bx)
    gcd_y = gcd(ay, by)
    
    if tx % gcd_x != 0 or ty % gcd_y != 0:
        return None
    
    # Use Cramer's rule to find solution
    # If the solution is valid, return it
    try:
        # Calculate A presses (n)
        n = (by * tx - bx * ty) // det
        # Calculate B presses (m)
        m = (ax * ty - ay * tx) // det
        
        # Check if solution is valid (non-negative)
        if n >= 0 and m >= 0:
            # Verify solution
            if (n * ax + m * bx == tx and 
                n * ay + m * by == ty):
                return (n, m)
    except:
        return None
        
    return None


def tokens_offset(content):
    """
    Calculates the minimum total tokens needed to win all possible prizes from the claw machines with a large offset.
    Uses Cramer's rule to solve the system of equations
    """
    start_time = time.time()

    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 2 - {current_func}")

    machines = []
    current_machine = {}
    OFFSET = 10000000000000  # 10^13
    # OFFSET = 0  # For testing   

    # Parse input
    for line in content.strip().split('\n'):
        if not line.strip():
            continue
        if line.startswith('Button A:'):
            current_machine = {}
            x, y = line.split(':')[1].strip().split(',')
            current_machine['Ax'] = int(x.split('+')[1])
            current_machine['Ay'] = int(y.split('+')[1])
        elif line.startswith('Button B:'):
            x, y = line.split(':')[1].strip().split(',')
            current_machine['Bx'] = int(x.split('+')[1])
            current_machine['By'] = int(y.split('+')[1])
        elif line.startswith('Prize:'):
            x, y = line.split(':')[1].strip().split(',')
            current_machine['target_x'] = int(x.split('=')[1]) + OFFSET
            current_machine['target_y'] = int(y.split('=')[1]) + OFFSET
            machines.append(current_machine)

    total_tokens = 0

    print("\nResults:")
    print("-" * 80)
    print(f"{'Machine':<10} {'A Presses':<12} {'B Presses':<12} {'Tokens':<12} {'Target X':<12} {'Target Y':<12}")
    print("-" * 80)

    for i, machine in enumerate(machines, 1):
        solution = solve_machine_large(
            machine['Ax'], machine['Ay'],
            machine['Bx'], machine['By'],
            machine['target_x'], machine['target_y']
        )
            
        if solution:
            a_presses, b_presses = solution
            tokens = a_presses * 3 + b_presses * 1
            total_tokens += tokens
            print(f"{i:<10} {a_presses:<12} {b_presses:<12} {tokens:<12} {machine['target_x']:<12} {machine['target_y']:<12}")
        else:
            print(f"{Fore.RED}{i:<10} {'-':<12} {'-':<12} {'-':<12} {machine['target_x']:<12} {machine['target_y']:<12}")

    execution_time = time.time() - start_time
    return total_tokens, execution_time


def process_file(filepath):
    """
    Process a single input file through both parts of the puzzle
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result, time1 = tokens(content)
        part2_result, time2 = tokens_offset(content)
        return part1_result, part2_result, time1, time2


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
            part1_result, part2_result, time1, time2 = process_file(filepath)
            results[file] = (True, part1_result, part2_result, time1, time2)
        except Exception as e:
            results[file] = (False, str(e))
    
    return results


if __name__ == "__main__":
    input_dir = "./input/"
    results = process_directory(input_dir)

    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    for file, result in results.items():
        if result[0]:  # Successfully processed
            part1, part2, time1, time2 = result[1], result[2], result[3], result[4]
            print(f"{Fore.BLUE}{file}:")
            print(f"  {Fore.YELLOW}Part 1 (Tokens):        {Fore.GREEN}{part1:<15}   {Fore.CYAN}Time: {time1:.3f}s")
            print(f"  {Fore.YELLOW}Part 2 (Tokens Offset): {Fore.GREEN}{part2:<15}   {Fore.CYAN}Time: {time2:.3f}s")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
