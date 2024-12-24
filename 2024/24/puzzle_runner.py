from aocd import submit
from aocd.models import Puzzle
import os
import time
import importlib
from input_manager import get_input_data, download_and_store_data
import traceback

def test_with_example(year, day, solve_part_one, solve_part_two, expected_output_part_one=None, expected_output_part_two=None):
    """
    Test the solutions for part one and part two with example data.

    Args:
        year (int): The year of the puzzle.
        day (int): The day of the puzzle.
        solve_part_one (function): The function to solve part one.
        solve_part_two (function): The function to solve part two.
        expected_output_part_one (optional): The expected output for part one.
        expected_output_part_two (optional): The expected output for part two.
    """
    print(f"Year: {year}, Day: {day}")
    # Fetch the puzzle for the specified day
    base_dir = os.path.join(os.path.dirname(__file__), str(year), f'day_{day:02}')
    try:
        download_and_store_data(year, day, base_dir)
        example_data, input_data = get_input_data(base_dir)
    except Exception as e:
        print("Error fetching puzzle data:")
        traceback.print_exc()
        return

    # Use provided expected outputs if available
    try:
        puzzle = Puzzle(year=year, day=day)
        expected_answer_a = expected_output_part_one if expected_output_part_one is not None else int(puzzle.examples[0].answer_a)
        expected_answer_b = expected_output_part_two if expected_output_part_two is not None else (int(puzzle.examples[0].answer_b) if puzzle.examples[0].answer_b is not None else None)
    except Exception as e:
        print("Error processing expected answers:")
        traceback.print_exc()
        return

    # Test part one with timing
    start_time = time.perf_counter_ns()
    try:
        example_part_one_result = solve_part_one(example_data)
    except Exception as e:
        print("Error solving Part One:")
        traceback.print_exc()
        return
    example_part_one_time = (time.perf_counter_ns() - start_time) / 1e9
    if example_part_one_result is not None and example_part_one_result == expected_answer_a:
        print(f"\033[1;92mPart One Example Test Passed!: {example_part_one_result}\033[0m")
    else:
        print(f"\033[1;91mPart One Example Test Failed: Expected {expected_answer_a}, Got {example_part_one_result}\033[0m")
    print(f"Part One Example Time: {example_part_one_time:.9f} seconds")

    # Test part two with timing
    start_time = time.perf_counter_ns()
    try:
        example_part_two_result = solve_part_two(example_data)
    except Exception as e:
        print("Error solving Part Two:")
        traceback.print_exc()
        return
    example_part_two_time = (time.perf_counter_ns() - start_time) / 1e9
    if example_part_two_result is not None and example_part_two_result == expected_answer_b:
        print(f"\033[1;92mPart Two Example Test Passed!: {example_part_two_result}\033[0m")
    else:
        print(f"\033[1;91mPart Two Example Test Failed: Expected {expected_answer_b}, Got {example_part_two_result}\033[0m")
    print(f"Part Two Example Time: {example_part_two_time:.9f} seconds")


def submit_solutions(year, day, solve_part_one, solve_part_two):
    """
    Submit the solutions for part one and part two after testing with actual input data.

    Args:
        year (int): The year of the puzzle.
        day (int): The day of the puzzle.
        solve_part_one (function): The function to solve part one.
        solve_part_two (function): The function to solve part two.
    """
    print("\033[90mSubmitting solutions...\n=======================\033[0m")
    # Determine base directory for inputs
    base_dir = os.path.join(os.path.dirname(__file__), str(year), f'day_{day:02}')
    try:
        download_and_store_data(year, day, base_dir)
    except Exception as e:
        print("Error fetching puzzle data:")
        traceback.print_exc()
        return

    # Read input data
    try:
        example_data, input_data = get_input_data(base_dir)
    except Exception as e:
        print("Error reading input data:")
        traceback.print_exc()
        return

    # Solve part one with timing
    start_time = time.perf_counter_ns()
    try:
        part_one_result = solve_part_one(input_data)
    except Exception as e:
        print("Error solving Part One:")
        traceback.print_exc()
        return
    part_one_time = (time.perf_counter_ns() - start_time) / 1e9
    print(f"\033[1mPart One Result: {part_one_result}\033[0m")
    print(f"Part One Time: {part_one_time:.9f} seconds")

    # Solve part two with timing
    start_time = time.perf_counter_ns()
    try:
        part_two_result = solve_part_two(input_data)
    except Exception as e:
        print("Error solving Part Two:")
        traceback.print_exc()
        return
    part_two_time = (time.perf_counter_ns() - start_time) / 1e9
    print(f"\033[1mPart Two Result: {part_two_result}\033[0m")
    print(f"Part Two Time: {part_two_time:.9f} seconds")

    # Ask for confirmation before submitting part one result
    confirm = input("Submit Part One result? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            submit(part_one_result, part="a", day=day, year=year)
            print("\033[1;92mPart One Submission Successful!\033[0m")
        except Exception as e:
            print(f"\033[1;91mPart One Submission Failed: {e}\033[0m")
            traceback.print_exc()

    # Fetch the puzzle for the specified day
    try:
        puzzle = Puzzle(year=year, day=day)
    except Exception as e:
        print("Error fetching puzzle:")
        traceback.print_exc()
        return

    # Check if example answer for part b is available
    # if puzzle.examples[0].answer_b is not None:
    if 1:
        # Ask for confirmation before submitting part two result
        confirm = input("Submit Part Two result? (y/n): ").strip().lower()
        if confirm == 'y':
            try:
                submit(part_two_result, part="b", day=day, year=year)
                print("\033[1;92mPart Two Submission Successful!\033[0m")
            except Exception as e:
                print(f"\033[1;91mPart Two Submission Failed: {e}\033[0m")
                traceback.print_exc()
    else:
        print("\033[1;93mExample answer for part b is not available. Skipping Part Two submission.\033[0m")


def run_day_solutions(year, day):
    """
    Automatically retrieve and run both solution functions for a given day, returning their execution times and correctness.

    Args:
        year (int): The year of the puzzle.
        day (int): The day of the puzzle.

    Returns:
        tuple: A tuple containing the execution times for part one and part two, and their correctness.
    """
    # Fetch the puzzle for the specified day
    try:
        puzzle = Puzzle(year=year, day=day)
    except Exception as e:
        print("Error fetching puzzle:")
        traceback.print_exc()
        return None

    # Determine base directory for inputs
    base_dir = os.path.join(os.path.dirname(__file__), str(year), f'day_{day:02}')
    try:
        download_and_store_data(year, day, base_dir)
    except Exception as e:
        print("Error fetching puzzle data:")
        traceback.print_exc()
        return None

    # Read example data from example.txt
    try:
        example_data, input_data = get_input_data(base_dir)
    except Exception as e:
        print("Error reading input data:")
        traceback.print_exc()
        return None

    # Attempt to import the module dynamically
    module_name = f'{year}.day_{day:02}.day{day:02}'
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Module for day {day} not found.")
        return None

    # Retrieve solution functions
    solve_part_one = getattr(module, 'solve_part_one', None)
    solve_part_two = getattr(module, 'solve_part_two', None)

    # Check if both functions exist
    if not solve_part_one or not solve_part_two:
        print(f"Solution functions for day {day} are missing.")
        return None

    # Retrieve optional expected outputs from the module
    expected_output_part_one = getattr(module, 'expected_output_part_one', None)
    expected_output_part_two = getattr(module, 'expected_output_part_two', None)

    # Solve part one with timing and correctness
    start_time = time.perf_counter_ns()
    try:
        part_one_example_result = solve_part_one(example_data)
    except Exception as e:
        print("Error solving Part One:")
        traceback.print_exc()
        return None
    part_one_input_result = solve_part_one(input_data)
    part_one_time = (time.perf_counter_ns() - start_time) / 1e9

    expected_answer_a = expected_output_part_one if expected_output_part_one is not None else int(puzzle.examples[0].answer_a)
    part_one_correct_example = part_one_example_result == expected_answer_a
    try:
        part_one_correct_input = part_one_input_result == int(puzzle.answer_a)
    except AttributeError:
        part_one_correct_input = False

    # Solve part two with timing and correctness
    start_time = time.perf_counter_ns()
    try:
        part_two_example_result = solve_part_two(example_data)
    except Exception as e:
        print("Error solving Part Two:")
        traceback.print_exc()
        return None
    part_two_input_result = solve_part_two(input_data)
    part_two_time = (time.perf_counter_ns() - start_time) / 1e9

    expected_answer_b = expected_output_part_two if expected_output_part_two is not None else (int(puzzle.examples[0].answer_b) if puzzle.examples[0].answer_b is not None else None)
    part_two_correct_example = part_two_example_result == expected_answer_b
    try:
        part_two_correct_input = part_two_input_result == int(puzzle.answer_b)
    except AttributeError:
        part_two_correct_input = False

    return ((part_one_time, part_one_correct_example, part_one_correct_input),
            (part_two_time, part_two_correct_example, part_two_correct_input))
