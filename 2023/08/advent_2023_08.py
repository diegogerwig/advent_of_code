#!/usr/bin/python3

import os
import time
import pathlib
import sys

import itertools
from colorama import init, Fore
init(autoreset=True)

def parse_data(puzzle_input):
    # Split the puzzle input into path and nodes
    path, nodes = puzzle_input.split("\n\n")
    
    # Convert the path string into a list of 0s and 1s, where "L" becomes 0 and anything else becomes 1
    path_list = [0 if ch == "L" else 1 for ch in path]
    
    # Convert the nodes string into a dictionary using the parse_node function
    nodes_dict = dict(parse_node(node) for node in nodes.split("\n"))

    return path_list, nodes_dict

def parse_node(node):
    # Split the node into starting point and targets
    start, targets = node.split(" = ")
    
    # Remove parentheses and split targets into a tuple
    target_tuple = tuple(targets.replace("(", "").replace(")", "").split(", "))
    
    return start, target_tuple

def gcd(a, b):
    # Calculate the greatest common divisor using Euclid's algorithm
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    # Calculate the least common multiple using the formula lcm(a, b) = (a * b) / gcd(a, b)
    return a * b // gcd(a, b)

def lcm_of_list(lst):
    # Calculate the least common multiple of a list of numbers
    result = lst[0]
    for i in range(1, len(lst)):
        result = lcm(result, lst[i])
    return result

def part1(data):
    # Unpack data into path and nodes
    path, nodes = data
    
    # Call the walk_path function and return the result
    return walk_path(nodes, path)

def part2(data):
    # Unpack data into path and nodes
    path, nodes = data
    
    # Call the walk_ghost_path function and return the result
    return walk_ghost_path(nodes, path)

def walk_path(nodes, path):
    # Start at node "AAA"
    current = "AAA"
    
    # Iterate over the path indefinitely
    for num_steps, turn in enumerate(itertools.cycle(path)):
        # If the current node is "ZZZ," return the number of steps
        if current == "ZZZ":
            return num_steps
        # Update the current node based on the turn
        current = nodes[current][turn]

def walk_ghost_path(nodes, path):
    # Find nodes that end with "A" (initial positions)
    current = [node for node in nodes if node.endswith("A")]
    
    # Initialize a list to store the number of steps for each initial position
    steps = [0 for _ in current]
    
    # Iterate over the path indefinitely
    for num_steps, turn in enumerate(itertools.cycle(path)):
        # Check if any of the current nodes reach "Z" and have not been marked with steps
        for idx, node in enumerate(current):
            if node.endswith("Z") and not steps[idx]:
                # Mark the number of steps for the corresponding initial position
                steps[idx] = num_steps
                # If all initial positions have steps, return the least common multiple
                if all(steps):
                    return lcm_of_list(steps)
        
        # Update the current nodes based on the turn
        current = [nodes[node][turn] for node in current]

def solve(input_file):
    data = parse_data(input_file)
    yield part1(data)
    yield part2(data)

if __name__ == "__main__":
    dir_input = "./input"
    file_input = os.listdir(dir_input)

    for file_name in file_input:
        start_time = time.time()
        file_path = os.path.join(dir_input, file_name)

        print(f"{Fore.YELLOW}{file_path}:")

        try:
            input_file = pathlib.Path(file_path).read_text().rstrip()
            if not input_file:
                print("⚠️  Input file is empty.")
            else:
                solutions = solve(input_file)
                print("\n".join(str(solution) for solution in solutions))
        except Exception as e:
            print(f"🔴  Error reading or processing the file: {e}")

        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_rounded = "{:.4f}".format(execution_time)
        print(f"Execution time: {execution_time_rounded} s")

        print("*" * 50)
