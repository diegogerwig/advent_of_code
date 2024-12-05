#!/usr/bin/python3

'''
--- Day 5: Print Queue ---
Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.
Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13
These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?

--- Part Two ---
While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
'''

import os
from colorama import init, Fore

init(autoreset=True)


def parse_input(content):
    """
    Converts input text into two parts:
    - rules: list of number pairs
    - updates: list of number lists
    """
    # Split content into two parts using double line break
    parts = content.strip().split("\n\n")
    rules_section = parts[0]
    updates_section = parts[1]
    
    # Process rules
    rules = []
    for line in rules_section.split("\n"):
        # Convert each line "x|y" into a tuple of numbers (x,y)
        numbers = line.split("|")
        x = int(numbers[0])
        y = int(numbers[1])
        rules.append((x, y))
    
    # Process updates
    updates = []
    for line in updates_section.split("\n"):
        # Convert each line "a,b,c" into a list of numbers [a,b,c]
        numbers = line.split(",")
        # Convert each text number to integer
        number_list = []
        for num in numbers:
            number_list.append(int(num))
        updates.append(number_list)
    
    return rules, updates


def is_valid_update(update, rules):
    """
    Checks if an update follows all rules.
    A rule (x,y) means x must appear before y in the update.
    """
    # Create dictionary where key is the page and value is list of pages that must come before it
    dependencies = {}
    for before, after in rules:
        # Only consider rules where both pages are in the update
        if before in update and after in update:
            # If page is not in dictionary, create empty list
            if after not in dependencies:
                dependencies[after] = []
            # Add page that must come before
            dependencies[after].append(before)
    
    # Check each page in the update
    for position, page in enumerate(update):
        # If the page has dependencies
        if page in dependencies:
            # Check each required page
            for required_page in dependencies[page]:
                # Find position of required page
                required_position = update.index(required_page)
                # If required page comes after, update is not valid
                if required_position > position:
                    return False
    
    return True


def find_middle(update):
    """
    Finds the middle page in an update.
    For odd length list, it's the center element.
    For even length list, it's the element to the left of center.
    """
    middle_position = len(update) // 2  # Integer division
    return update[middle_position]


def sum_middle_page_numbers(content):
    """
    Part 1: Process content and return sum of middle pages from valid updates.
    """
    rules, updates = parse_input(content)

    # Find valid updates
    valid_updates = []
    for update in updates:
        if is_valid_update(update, rules):
            valid_updates.append(update)
    
    middle_sum = 0
    for update in valid_updates:
        value = find_middle(update)
        middle_sum += value

    return middle_sum


def find_correct_order(update, rules):
    """
    Find the correct order for a given update based on the rules.
    Uses a simple topological sort approach.
    """
    # Create a dictionary of dependencies
    depends_on = {page: set() for page in update}
    for x, y in rules:
        if x in update and y in update:
            depends_on[y].add(x)
    
    # Create ordered result
    result = []
    used = set()
    
    while len(result) < len(update):
        # Find a page that has all dependencies satisfied
        for page in update:
            if page not in used:
                # Check all dependencies for this page
                all_deps_satisfied = True
                for dep in depends_on[page]:
                    if dep not in used:
                        all_deps_satisfied = False
                        break
                
                if all_deps_satisfied:
                    result.append(page)
                    used.add(page)
                    break
        
    return result


def sum_middle_page_numbers_after_sorting(content):
    """
    Part 2: Process incorrect updates, fix their order, and return sum of middle pages.
    """
    rules, updates = parse_input(content)
    
    # Find invalid updates
    invalid_updates = []
    for update in updates:
        if not is_valid_update(update, rules):
            invalid_updates.append(update)
    
    middle_sum = 0
    for update in invalid_updates:
        fixed_update = find_correct_order(update, rules)
        middle_sum += find_middle(fixed_update)
    
    return middle_sum


def process_file(filepath):
    """
    Process a single file and return results for both parts:
    - Sum of middle page numbers from correct order rules
    - Sum of middle page numbers after sorting incorrect order rules
    """
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = sum_middle_page_numbers(content)
        part2_result = sum_middle_page_numbers_after_sorting(content)
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
            print(f"  {Fore.YELLOW}Part 1 (Sum of middle page numbers from correct order rules): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Sum of middle page numbers after sorting incorrect order rules): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
