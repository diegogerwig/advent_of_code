'''
--- Day 17: Chronospatial Computer ---
The Historians push the button on their strange device, but this time, you all just feel like you're falling.

"Situation critical", the device announces in a familiar voice. "Bootstrapping process failed. Initializing debugger...."

The small handheld device suddenly unfolds into an entire computer! The Historians look around nervously before one of them tosses it to you.

This seems to be a 3-bit computer: its program is a list of 3-bit numbers (0 through 7), like 0,1,2,3. The computer also has three registers named A, B, and C, but these registers aren't limited to 3 bits and can instead hold any integer.

The computer knows eight instructions, each identified by a 3-bit number (called the instruction's opcode). Each instruction also reads the 3-bit number after it as an input; this is called its operand.

A number called the instruction pointer identifies the position in the program from which the next opcode will be read; it starts at 0, pointing at the first 3-bit number in the program. Except for jump instructions, the instruction pointer increases by 2 after each instruction is processed (to move past the instruction's opcode and its operand). If the computer tries to read an opcode past the end of the program, it instead halts.

So, the program 0,1,2,3 would run the instruction whose opcode is 0 and pass it the operand 1, then run the instruction having opcode 2 and pass it the operand 3, then halt.

There are two types of operands; each instruction specifies the type of its operand. The value of a literal operand is the operand itself. For example, the value of the literal operand 7 is the number 7. The value of a combo operand can be found as follows:

Combo operands 0 through 3 represent literal values 0 through 3.
Combo operand 4 represents the value of register A.
Combo operand 5 represents the value of register B.
Combo operand 6 represents the value of register C.
Combo operand 7 is reserved and will not appear in valid programs.
The eight instructions are as follows:

The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

Here are some examples of instruction operation:

If register C contains 9, the program 2,6 would set register B to 1.
If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
If register B contains 29, the program 1,7 would set register B to 26.
If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
The Historians' strange device has finished initializing its debugger and is displaying some information about the program it is trying to run (your puzzle input). For example:

Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
Your first task is to determine what the program is trying to output. To do this, initialize the registers to the given values, then run the given program, collecting any output produced by out instructions. (Always join the values produced by out instructions with commas.) After the above program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

Using the information provided by the debugger, initialize the registers to the given values, then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?

--- Part Two ---
Digging deeper in the device's manual, you discover the problem: this program is supposed to output another copy of the program! Unfortunately, the value in register A seems to have been corrupted. You'll need to find a new value to which you can initialize register A so that the program's output instructions produce an exact copy of the program itself.

For example:

Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
This program outputs a copy of itself if register A is instead initialized to 117440. (The original initial value of register A, 2024, is ignored.)

What is the lowest positive initial value for register A that causes the program to output a copy of itself?
'''

#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time
from tqdm import tqdm

init(autoreset=True)

CURRENT_FILEPATH = ""

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

TEST_SOLUTIONS = {
    ".test_I.txt": {
        "part1": {
            "value": '4,6,3,5,6,3,5,2,1,0',
            "verified": True
        },
        "part2": {
            "value": 0,
            "verified": False
        }
    },
    "input_I.txt": {
        "part1": {
            "value": '6,7,5,2,1,3,5,1,7',
            "verified": True
        },
        "part2": {
            "value": '216549846240877',
            "verified": True
        }
    }
}


def print_header(filename, part):
    """
    Simple header printing function
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Part {part}")
    print(f"{Fore.CYAN}{'='*80}\n")


def parse_input(content):
    """Parse the input to get register values and program"""
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    registers = {'A': 0, 'B': 0, 'C': 0}
    program = []
    
    for line in lines:
        if line.startswith('Register'):
            reg, value = line.split(': ')
            registers[reg.split()[-1]] = int(value)
        elif line.startswith('Program:'):
            program = [int(x) for x in line.split(': ')[1].split(',')]
            
    return registers, program


def get_combo_value(operand, registers):
    """Get value for combo operand"""
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    return 0  # operand 7 is reserved


def part1(content):
    """Simulate the 3-bit computer and return comma-separated output"""
    start_time = time.time()
    
    registers, program = parse_input(content)
    output = []
    ip = 0  # instruction pointer
    
    while ip < len(program) - 1:  # -1 because we need space for operand
        opcode = program[ip]
        operand = program[ip + 1]
        
        if opcode == 0:  # adv
            power = get_combo_value(operand, registers)
            registers['A'] = registers['A'] // (2 ** power)
            ip += 2
        elif opcode == 1:  # bxl
            registers['B'] ^= operand
            ip += 2
        elif opcode == 2:  # bst
            registers['B'] = get_combo_value(operand, registers) % 8
            ip += 2
        elif opcode == 3:  # jnz
            if registers['A'] != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            registers['B'] ^= registers['C']
            ip += 2
        elif opcode == 5:  # out
            value = get_combo_value(operand, registers) % 8
            output.append(str(value))
            ip += 2
        elif opcode == 6:  # bdv
            power = get_combo_value(operand, registers)
            registers['B'] = registers['A'] // (2 ** power)
            ip += 2
        elif opcode == 7:  # cdv
            power = get_combo_value(operand, registers)
            registers['C'] = registers['A'] // (2 ** power)
            ip += 2
        else:
            ip += 2
    
    return {
        "value": ','.join(output),
        "execution_time": time.time() - start_time
    }


def part2(content):
    """
    Find the lowest positive initial value for register A that causes the program 
    to output a copy of itself.

    The solution works by constructing the value backwards from right to left, 
    3 bits at a time, ensuring each step produces the desired program sequence.

    Args:
        content (str): Input string containing register values and program

    Returns:
        dict: Dictionary containing the result value and execution time
    """
    start_time = time.time()
    
    # Parse input to get registers and program
    registers, program = parse_input(content)
    
    # Initialize variables for instruction pattern matching
    v1 = program[3]  # First XOR operand after initial sequence
    v3 = None  # Will store second XOR operand
    
    # Find the second XOR operation in the program
    for ip in range(4, len(program), 2):
        if program[ip] == 1:
            v3 = program[ip + 1]
            break
    
    # If we can't find v3, return early to avoid errors
    if v3 is None:
        return {
            "value": "0",
            "execution_time": time.time() - start_time
        }
    
    def transpiled(a, v1, v3):
        """
        Simulate the core program operation using bit manipulation.
        
        Args:
            a (int): Current value being tested
            v1 (int): First XOR operand
            v3 (int): Second XOR operand
            
        Returns:
            int: Result of the operation (0-7)
        """
        b = (a & 0b111) ^ v1  # Extract bottom 3 bits and XOR with v1
        return ((b ^ (a >> b)) ^ v3) & 0b111  # Apply core transformation
    
    # Build solution from right to left
    cur = [0]  # Start with 0 as base
    for wanted in reversed(program):
        next = []
        for p in cur:
            # Try each possible 3-bit value
            for i in range(8):
                a = (p << 3) + i  # Add new 3 bits on the left
                if transpiled(a, v1, v3) == wanted:
                    next.append(a)
        cur = next
    
    # Find the first value that generates the correct number of digits
    cur.sort()  # Ensure we get the lowest valid value
    for c in cur:
        a = c
        digit = 0
        while a > 0 and digit < len(program):
            digit += 1
            a >>= 3
        if digit == len(program):
            return {
                "value": str(c),
                "execution_time": time.time() - start_time
            }
    
    # If no solution is found
    return {
        "value": "0",
        "execution_time": time.time() - start_time
    }


def determine_test_status(result, expected_solution):
    """
    Determine the test status based on the result and expected value
    """
    if not expected_solution["verified"]:
        if expected_solution["value"] == 0:
            return TEST_STATUS["IN_PROGRESS"]
        return TEST_STATUS["UNKNOWN"]
    
    if result["value"] == expected_solution["value"]:
        return TEST_STATUS["PASSED"]
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
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
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
            verified = test_solution.get("verified", False)
            
            # Add status to results
            part1_result["status"] = determine_test_status(
                part1_result, 
                test_solution.get("part1", {"value": 0, "verified": False})
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", {"value": 0, "verified": False})
            )
            
            return True, {
                "part1": part1_result,
                "part2": part2_result
            }
            
    except Exception as e:
        return False, str(e)


def process_directory(input_dir="./input/"):
    """Process all files in the specified directory"""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    print(f"\n{Fore.CYAN}Processing files in directory: {Fore.YELLOW}{input_dir}")
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
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
    
    for file, (success, result) in results.items():
        print(f"\n{Fore.BLUE}{file}:")
        
        if success:
            for part_name, part_result in result.items():
                status_color = get_status_color(part_result["status"])
                status_text = f"[{part_result['status']}]"
                
                # Add expected value for FAILED status
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    status_text += f" (Expected: {TEST_SOLUTIONS[file][part_name]['value']})"
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{part_result['value']:<15} "
                      f"{status_color}{status_text}  "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
        else:
            print(f"  {Fore.RED}Error - {result}")


def main():
    try:
        input_dir = "./input/"
        results = process_directory(input_dir)
        print_results(results)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()