'''
--- Day 19: Linen Layout ---
Today, The Historians take you up to the hot springs on Gear Island! Very suspiciously, absolutely nothing goes wrong as they begin their careful search of the vast field of helixes.

Could this finally be your chance to visit the onsen next door? Only one way to find out.

After a brief conversation with the reception staff at the onsen front desk, you discover that you don't have the right kind of money to pay the admission fee. However, before you can leave, the staff get your attention. Apparently, they've heard about how you helped at the hot springs, and they're willing to make a deal: if you can simply help them arrange their towels, they'll let you in for free!

Every towel at this onsen is marked with a pattern of colored stripes. There are only a few patterns, but for any particular pattern, the staff can get you as many towels with that pattern as you need. Each stripe can be white (w), blue (u), black (b), red (r), or green (g). So, a towel with the pattern ggr would have a green stripe, a green stripe, and then a red stripe, in that order. (You can't reverse a pattern by flipping a towel upside-down, as that would cause the onsen logo to face the wrong way.)

The Official Onsen Branding Expert has produced a list of designs - each a long sequence of stripe colors - that they would like to be able to display. You can use any towels you want, but all of the towels' stripes must exactly match the desired design. So, to display the design rgrgr, you could use two rg towels and then an r towel, an rgr towel and then a gr towel, or even a single massive rgrgr towel (assuming such towel patterns were actually available).

To start, collect together all of the available towel patterns and the list of desired designs (your puzzle input). For example:

r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
The first line indicates the available towel patterns; in this example, the onsen has unlimited towels with a single red stripe (r), unlimited towels with a white stripe and then a red stripe (wr), and so on.

After the blank line, the remaining lines each describe a design the onsen would like to be able to display. In this example, the first design (brwrr) indicates that the onsen would like to be able to display a black stripe, a red stripe, a white stripe, and then two red stripes, in that order.

Not all designs will be possible with the available towels. In the above example, the designs are possible or impossible as follows:

brwrr can be made with a br towel, then a wr towel, and then finally an r towel.
bggr can be made with a b towel, two g towels, and then an r towel.
gbbr can be made with a gb towel and then a br towel.
rrbgbr can be made with r, rb, g, and br.
ubwu is impossible.
bwurrg can be made with bwu, r, r, and g.
brgr can be made with br, g, and r.
bbrgwb is impossible.
In this example, 6 of the eight designs are possible with the available towel patterns.

To get into the onsen as soon as possible, consult your list of towel patterns and desired designs carefully. How many designs are possible?

--- Part Two ---
The staff don't really like some of the towel arrangements you came up with. To avoid an endless cycle of towel rearrangement, maybe you should just give them every possible option.

Here are all of the different ways the above example's designs can be made:

brwrr can be made in two different ways: b, r, wr, r or br, wr, r.

bggr can only be made with b, g, g, and r.

gbbr can be made 4 different ways:

g, b, b, r
g, b, br
gb, b, r
gb, br
rrbgbr can be made 6 different ways:

r, r, b, g, b, r
r, r, b, g, br
r, r, b, gb, r
r, rb, g, b, r
r, rb, g, br
r, rb, gb, r
bwurrg can only be made with bwu, r, r, and g.

brgr can be made in two different ways: b, r, g, r or br, g, r.

ubwu and bbrgwb are still impossible.

Adding up all of the ways the towels in this example could be arranged into the desired designs yields 16 (2 + 1 + 4 + 6 + 1 + 2).

They'll let you into the onsen as soon as you have the list. What do you get if you add up the number of different ways you could make each design?
'''


#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time

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
        "part1": 6,
        "part2": 16,
        "verified": True  # Indicates if the solution is verified
    },
    "input_I.txt": {
        "part1": 324,
        "part2": '',
        "verified": True
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
    """
    Parse the input content into patterns and designs
    """
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    
    # First line contains the patterns
    patterns = [p.strip() for p in lines[0].split(',')]
    # Remaining lines are the designs
    designs = lines[1:]
    
    return patterns, designs


def can_make_design(design, patterns, memo=None):
    """
    Check if a design can be made using the available patterns
    Using dynamic programming with memoization to avoid redundant calculations
    """
    if memo is None:
        memo = {}
    
    # Base case: empty design means we've successfully used all stripes
    if not design:
        return True
        
    # Check memoized result
    if design in memo:
        return memo[design]
    
    # Try each pattern as a potential start of the design
    for pattern in patterns:
        if design.startswith(pattern):
            # Recursively check if we can make the rest of the design
            remaining = design[len(pattern):]
            if can_make_design(remaining, patterns, memo):
                memo[design] = True
                return True
    
    memo[design] = False
    return False


def part1(content):
    """
    Solution for Part 1 - count how many designs are possible
    """
    start_time = time.time()
    
    # Parse input
    patterns, designs = parse_input(content)
    
    # Count possible designs
    possible_count = sum(1 for design in designs if can_make_design(design, patterns))
    
    execution_time = time.time() - start_time
    
    return {
        "value": possible_count,
        "execution_time": execution_time,
        "status": "UNKNOWN"
    }


def count_ways(design, patterns, memo=None):
    """
    Count all different ways a design can be made using the available patterns
    Using dynamic programming with memoization
    """
    if memo is None:
        memo = {}
        
    # Base case: empty design means we found one valid way
    if not design:
        return 1
        
    # Check memoized result
    if design in memo:
        return memo[design]
    
    total_ways = 0
    # Try each pattern as a potential start of the design
    for pattern in patterns:
        if design.startswith(pattern):
            # Add the number of ways to make the remaining design
            remaining = design[len(pattern):]
            total_ways += count_ways(remaining, patterns, memo)
    
    memo[design] = total_ways
    return total_ways


def part2(content):
    """
    Solution for Part 2 - sum up all different ways to make each possible design
    """
    start_time = time.time()
    
    # Parse input
    patterns, designs = parse_input(content)
    
    # For each design that's possible, count all different ways it can be made
    total_ways = 0
    for design in designs:
        # First check if the design is possible at all
        if can_make_design(design, patterns):
            # If it is possible, count all different ways to make it
            ways = count_ways(design, patterns)
            total_ways += ways
    
    return {
        "value": total_ways,
        "execution_time": time.time() - start_time,
        "status": "UNKNOWN"
    }


def determine_test_status(result, expected, verified):
    """
    Determine the test status based on the result and expected value
    """
    if not verified:
        if expected == 0:
            return TEST_STATUS["IN_PROGRESS"]
        return TEST_STATUS["UNKNOWN"]
    
    if result["value"] == expected:
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
                test_solution.get("part1", 0),
                verified
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", 0),
                verified
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