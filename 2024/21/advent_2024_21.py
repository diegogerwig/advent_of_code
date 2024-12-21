'''
--- Day 21: Keypad Conundrum ---
As you teleport onto Santa's Reindeer-class starship, The Historians begin to panic: someone from their search party is missing. A quick life-form scan by the ship's computer reveals that when the missing Historian teleported, he arrived in another part of the ship.

The door to that area is locked, but the computer can't open it; it can only be opened by physically typing the door codes (your puzzle input) on the numeric keypad on the door.

The numeric keypad has four rows of buttons: 789, 456, 123, and finally an empty gap followed by 0A. Visually, they are arranged like this:

+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
Unfortunately, the area outside the door is currently depressurized and nobody can go near the door. A robot needs to be sent instead.

The robot has no problem navigating the ship and finding the numeric keypad, but it's not designed for button pushing: it can't be told to push a specific button directly. Instead, it has a robotic arm that can be controlled remotely via a directional keypad.

The directional keypad has two rows of buttons: a gap / ^ (up) / A (activate) on the first row and < (left) / v (down) / > (right) on the second row. Visually, they are arranged like this:

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
When the robot arrives at the numeric keypad, its robotic arm is pointed at the A button in the bottom right corner. After that, this directional keypad remote control must be used to maneuver the robotic arm: the up / down / left / right buttons cause it to move its arm one button in that direction, and the A button causes the robot to briefly move forward, pressing the button being aimed at by the robotic arm.

For example, to make the robot type 029A on the numeric keypad, one sequence of inputs on the directional keypad you could use is:

< to move the arm from A (its initial position) to 0.
A to push the 0 button.
^A to move the arm to the 2 button and push it.
>^^A to move the arm to the 9 button and push it.
vvvA to move the arm to the A button and push it.
In total, there are three shortest possible sequences of button presses on this directional keypad that would cause the robot to type 029A: <A^A>^^AvvvA, <A^A^>^AvvvA, and <A^A^^>AvvvA.

Unfortunately, the area containing this directional keypad remote control is currently experiencing high levels of radiation and nobody can go near it. A robot needs to be sent instead.

When the robot arrives at the directional keypad, its robot arm is pointed at the A button in the upper right corner. After that, a second, different directional keypad remote control is used to control this robot (in the same way as the first robot, except that this one is typing on a directional keypad instead of a numeric keypad).

There are multiple shortest possible sequences of directional keypad button presses that would cause this robot to tell the first robot to type 029A on the door. One such sequence is v<<A>>^A<A>AvA<^AA>A<vAAA>^A.

Unfortunately, the area containing this second directional keypad remote control is currently -40 degrees! Another robot will need to be sent to type on that directional keypad, too.

There are many shortest possible sequences of directional keypad button presses that would cause this robot to tell the second robot to tell the first robot to eventually type 029A on the door. One such sequence is <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A.

Unfortunately, the area containing this third directional keypad remote control is currently full of Historians, so no robots can find a clear path there. Instead, you will have to type this sequence yourself.

Were you to choose this sequence of button presses, here are all of the buttons that would be pressed on your directional keypad, the two robots' directional keypads, and the numeric keypad:

<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
v<<A>>^A<A>AvA<^AA>A<vAAA>^A
<A^A>^^AvvvA
029A
In summary, there are the following keypads:

One directional keypad that you are using.
Two directional keypads that robots are using.
One numeric keypad (on a door) that a robot is using.
It is important to remember that these robots are not designed for button pushing. In particular, if a robot arm is ever aimed at a gap where no button is present on the keypad, even for an instant, the robot will panic unrecoverably. So, don't do that. All robots will initially aim at the keypad's A key, wherever it is.

To unlock the door, five codes will need to be typed on its numeric keypad. For example:

029A
980A
179A
456A
379A

For each of these, here is a shortest sequence of button presses you could type to cause the desired code to be typed on the numeric keypad:

029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
The Historians are getting nervous; the ship computer doesn't remember whether the missing Historian is trapped in the area containing a giant electromagnet or molten lava. You'll need to make sure that for each of the five codes, you find the shortest sequence of button presses necessary.

The complexity of a single code (like 029A) is equal to the result of multiplying these two values:

The length of the shortest sequence of button presses you need to type on your directional keypad in order to cause the code to be typed on the numeric keypad; for 029A, this would be 68.
The numeric part of the code (ignoring leading zeroes); for 029A, this would be 29.
In the above example, complexity of the five codes can be found by calculating 68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379. Adding these together produces 126384.

Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door to type each code. What is the sum of the complexities of the five codes on your list?

--- Part Two ---
Just as the missing Historian is released, The Historians realize that a second member of their search party has also been missing this entire time!

A quick life-form scan reveals the Historian is also trapped in a locked area of the ship. Due to a variety of hazards, robots are once again dispatched, forming another chain of remote control keypads managing robotic-arm-wielding robots.

This time, many more robots are involved. In summary, there are the following keypads:

One directional keypad that you are using.
25 directional keypads that robots are using.
One numeric keypad (on a door) that a robot is using.
The keypads form a chain, just like before: your directional keypad controls a robot which is typing on a directional keypad which controls a robot which is typing on a directional keypad... and so on, ending with the robot which is typing on the numeric keypad.

The door codes are the same this time around; only the number of robots and directional keypads has changed.

Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door to type each code. What is the sum of the complexities of the five codes on your list?
'''




#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time
import functools

init(autoreset=True)

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
        "part1": 126384,
        "part2": 'N/A',
    },
    "input_I.txt": {
        "part1": 134120,
        "part2": 167389793580400,
    }
}

# Define the layout of the numeric keypad (the one on the door)
# Each key is mapped to its (x, y) coordinates
NUMERIC_KEYPAD = {
    "7": (0, 0), "8": (1, 0), "9": (2, 0),  # Top row
    "4": (0, 1), "5": (1, 1), "6": (2, 1),  # Middle row
    "1": (0, 2), "2": (1, 2), "3": (2, 2),  # Bottom row
    "X": (0, 3), "0": (1, 3), "A": (2, 3)   # Bottom row with gap (X)
}

# Define the layout of the directional keypad (the one used to control robots)
DIRECTIONAL_KEYPAD = {
    "X": (0, 0), "^": (1, 0), "A": (2, 0),  # Top row
    "<": (0, 1), "v": (1, 1), ">": (2, 1)   # Bottom row
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
    """
    Parse the input content 
    """
    return [line.strip() for line in content.splitlines() if line.strip()]


# Store previous results to avoid recalculating
# This replaces the @functools.cache decorator with a simple dictionary
movement_cache = {}


def get_horizontal_movements(start_x, end_x):
    """
    Calculate the horizontal movements needed to go from start_x to end_x
    Returns: String of '>' or '<' characters
    """
    # If we need to move right
    if end_x > start_x:
        return ">" * (end_x - start_x)
    # If we need to move left
    else:
        return "<" * (start_x - end_x)


def get_vertical_movements(start_y, end_y):
    """
    Calculate the vertical movements needed to go from start_y to end_y
    Returns: String of '^' or 'v' characters
    """
    # If we need to move up
    if end_y < start_y:
        return "^" * (start_y - end_y)
    # If we need to move down
    else:
        return "v" * (end_y - start_y)


def is_safe_move(current_pos, target_pos, gap_pos):
    """
    Check if moving from current position to target position is safe
    (won't hit the gap/empty space)
    """
    current_x, current_y = current_pos
    gap_x, gap_y = gap_pos
    target_x, target_y = target_pos
    
    # Moving horizontally first won't hit gap
    horizontal_safe = not (target_x == gap_x and current_y == gap_y)
    # Moving vertically first won't hit gap
    vertical_safe = not (target_y == gap_y and current_x == gap_x)
    
    return horizontal_safe, vertical_safe


def get_movement_key(code, n):
    """
    Create a unique key for caching movement results
    """
    return f"{code}_{n}"


def direction_command(code, n):
    """
    Calculate the number of button presses needed for n robots to type the directional code
    """
    # Check if we've already calculated this result
    cache_key = get_movement_key(code, n)
    if cache_key in movement_cache:
        return movement_cache[cache_key]
    
    # Base case: if no more robots in chain (n=0), just return code length
    if n == 0:
        movement_cache[cache_key] = len(code)
        return len(code)
    
    total_moves = 0
    
    # Get coordinates of the gap (X) and starting position (A)
    gap_x, gap_y = DIRECTIONAL_KEYPAD["X"]
    current_x, current_y = DIRECTIONAL_KEYPAD["A"]
    
    # Process each button in the code
    for button in code:
        # Get coordinates of target button
        target_x, target_y = DIRECTIONAL_KEYPAD[button]
        
        # Calculate movements needed in each direction
        horizontal_moves = get_horizontal_movements(current_x, target_x)
        vertical_moves = get_vertical_movements(current_y, target_y)
        
        # Check which moves are safe
        horizontal_first_safe, vertical_first_safe = is_safe_move(
            (current_x, current_y),
            (target_x, target_y),
            (gap_x, gap_y)
        )
        
        # Try all possible safe movement combinations
        possible_moves = []
        
        # Try horizontal movement first if safe
        if horizontal_first_safe:
            move_sequence = horizontal_moves + vertical_moves + "A"
            moves = direction_command(move_sequence, n-1)
            possible_moves.append(moves)
        
        # Try vertical movement first if safe
        if vertical_first_safe:
            move_sequence = vertical_moves + horizontal_moves + "A"
            moves = direction_command(move_sequence, n-1)
            possible_moves.append(moves)
        
        # Add the shortest valid sequence to total moves
        total_moves += min(possible_moves)
        
        # Update current position
        current_x, current_y = target_x, target_y
    
    # Cache and return result
    movement_cache[cache_key] = total_moves
    return total_moves


def keyboard_command(code, n):
    """
    Calculate the number of button presses needed to type the numeric code with n robots
    """
    total_moves = 0
    
    # Get coordinates of the gap (X) and starting position (A)
    gap_x, gap_y = NUMERIC_KEYPAD["X"]
    current_x, current_y = NUMERIC_KEYPAD["A"]
    
    # Process each button in the code
    for button in code:
        # Get coordinates of target button
        target_x, target_y = NUMERIC_KEYPAD[button]
        
        # Calculate movements needed in each direction
        horizontal_moves = get_horizontal_movements(current_x, target_x)
        vertical_moves = get_vertical_movements(current_y, target_y)
        
        # Check which moves are safe
        horizontal_first_safe, vertical_first_safe = is_safe_move(
            (current_x, current_y),
            (target_x, target_y),
            (gap_x, gap_y)
        )
        
        # Try all possible safe movement combinations
        possible_moves = []
        
        # Try horizontal movement first if safe
        if horizontal_first_safe:
            move_sequence = horizontal_moves + vertical_moves + "A"
            moves = direction_command(move_sequence, n)
            possible_moves.append(moves)
        
        # Try vertical movement first if safe
        if vertical_first_safe:
            move_sequence = vertical_moves + horizontal_moves + "A"
            moves = direction_command(move_sequence, n)
            possible_moves.append(moves)
        
        # Add the shortest valid sequence to total moves
        total_moves += min(possible_moves)
        
        # Update current position
        current_x, current_y = target_x, target_y
    
    return total_moves


def calculate_complexity(code, num_robots):
    """
    Calculate the complexity of a code based on:
    1. The number of moves needed to type it
    2. The numeric value of the code
    """
    # Calculate total moves needed
    total_moves = keyboard_command(code, num_robots)
    
    # Get numeric value (remove 'A' from end and convert to integer)
    numeric_value = int(code[:-1])
    
    # Calculate complexity
    complexity = total_moves * numeric_value
    
    return complexity


def part1(content):
    """
    Solve part 1: Calculate sum of complexities with 2 robots
    """
    # Record start time
    start_time = time.time()
    
    # Get list of codes from input
    codes = parse_input(content)
    
    # Calculate total complexity
    total = 0
    for code in codes:
        complexity = calculate_complexity(code, 2)
        total += complexity
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    return {
        "value": total,
        "execution_time": execution_time
    }


def part2(content):
    """
    Solve part 2: Calculate sum of complexities with 25 robots
    """
    # Record start time
    start_time = time.time()
    
    # Get list of codes from input
    codes = parse_input(content)
    
    # Calculate total complexity
    total = 0
    for code in codes:
        complexity = calculate_complexity(code, 25)
        total += complexity
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    return {
        "value": total,
        "execution_time": execution_time
    }


def determine_test_status(result, expected):
    """
    Determine the test status based on the result and expected value.
    """
    if expected == 'N/A':
        return TEST_STATUS["IN_PROGRESS"]
    
    # Convert both values to strings for comparison to handle mixed types
    result_str = str(result["value"])
    expected_str = str(expected)
    
    if result_str == expected_str:
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
            
            # Add status to results
            part1_result["status"] = determine_test_status(
                part1_result, 
                test_solution.get("part1", 0)
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", 0)
            )
            
            return True, {
                "part1": part1_result,
                "part2": part2_result
            }
            
    except Exception as e:
        return False, str(e)


def process_directory(input_dir="./input/"):
    """
    Process all files in the specified directory
    """
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
    """
    Print results with enhanced status display
    """
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
                    status_text += f" (Expected: {TEST_SOLUTIONS[file][part_name]})"
                
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