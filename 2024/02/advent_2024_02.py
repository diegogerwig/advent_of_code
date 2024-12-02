#!/usr/bin/python3

'''
--- Day 2: Red-Nosed Reports ---
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
'''

import os
from colorama import init, Fore

init(autoreset=True)


def is_safe_report(levels):
    """
    Determines if a single report is safe.
    A report is safe if:
    - Levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least 1 and at most 3.
    """
    diffs = []
    
    for i in range(len(levels) - 1):
        # Calculate the difference between the current level and the next
        diff = levels[i + 1] - levels[i]
        diffs.append(diff)

    # Check if the differences are all valid for a strictly decreasing sequence
    if all(-3 <= diff <= -1 for diff in diffs):
        return True

    # Check if the differences are all valid for a strictly increasing sequence
    if all(1 <= diff <= 3 for diff in diffs):
        return True
    
    return False


def can_be_safe_with_one_removal(levels):
    """
    Determines if removing a single level can make the report safe.
    """
    for i in range(len(levels)):
        # Create a new list excluding the i-th level
        modified_levels = levels[:i] + levels[i + 1:]
        if is_safe_report(modified_levels):
            return True
    return False


def process_file(filepath):
    """
    Processes a single file containing reports and counts:
    - Safe reports.
    - Reports that become safe after removing one level.
    """
    with open(filepath, 'r') as file:
        lines = file.readlines()
        safe_count = 0
        safe_with_removal_count = 0
        
        for line in lines:
            levels = list(map(int, line.strip().split()))
            if is_safe_report(levels):
                safe_count += 1
            elif can_be_safe_with_one_removal(levels):
                safe_with_removal_count += 1
        
        total_safe = safe_count + safe_with_removal_count
        return safe_count, total_safe


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
            print(f"  {Fore.YELLOW}Part 1 (Safe reports): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Safe reports with one removal): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
