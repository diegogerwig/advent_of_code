'''
--- Day 23: LAN Party ---
As The Historians wander around a secure area at Easter Bunny HQ, you come across posters for a LAN party scheduled for today! Maybe you can find it; you connect to a nearby datalink port and download a map of the local network (your puzzle input).

The network map provides a list of every connection between two computers. For example:

kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
Each line of text in the network map represents a single connection; the line kh-tc represents a connection between the computer named kh and the computer named tc. Connections aren't directional; tc-kh would mean exactly the same thing.

LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of connected computers. Start by looking for sets of three computers where each computer in the set is connected to the other two computers.

In this example, there are 12 such sets of three inter-connected computers:

aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq
If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away. You're pretty sure his computer's name starts with t, so consider only sets of three computers where at least one computer's name starts with t. That narrows the list down to 7 sets of three inter-connected computers:

co,de,ta
co,ka,ta
de,ka,ta
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
Find all the sets of three inter-connected computers. How many contain at least one computer with a name that starts with t?

--- Part Two ---
There are still way too many results to go through them all. You'll have to find the LAN party another way and go there yourself.

Since it doesn't seem like any employees are around, you figure they must all be at the LAN party. If that's true, the LAN party will be the largest set of computers that are all connected to each other. That is, for each computer at the LAN party, that computer will have a connection to every other computer at the LAN party.

In the above example, the largest set of computers that are all connected to each other is made up of co, de, ka, and ta. Each computer in this set has a connection to every other computer in the set:

ka-co
ta-co
de-co
ta-ka
de-ta
ka-de
The LAN party posters say that the password to get into the LAN party is the name of every computer at the LAN party, sorted alphabetically, then joined together with commas. (The people running the LAN party are clearly a bunch of nerds.) In this example, the password would be co,de,ka,ta.

What is the password to get into the LAN party?
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
        "part1": 7,
        "part2": 'co,de,ka,ta',
    },
    "input_I.txt": {
        "part1": 1119,
        "part2": 'N/A',
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
    Parse the input content removing empty lines and whitespace
    """
    lines = content.splitlines()
    result = []
    for line in lines:
        clean_line = line.strip()
        if clean_line and '-' in clean_line:  # Only keep lines with connections
            result.append(clean_line)
    return result


def build_graph(connections):
    """
    Build an adjacency dictionary from the connections
    """
    graph = {}
    for connection in connections:
        a, b = connection.split('-')
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph


def find_triplets(graph):
    """
    Find all sets of three fully interconnected computers
    """
    computers = sorted(graph.keys())
    triplets = set()
    
    for i in range(len(computers)):
        for j in range(i + 1, len(computers)):
            # Check if first two computers are connected
            if computers[j] not in graph[computers[i]]:
                continue
                
            for k in range(j + 1, len(computers)):
                # Check if third computer is connected to both others
                if (computers[k] in graph[computers[i]] and 
                    computers[k] in graph[computers[j]]):
                    # Sort to ensure consistent ordering
                    triplet = tuple(sorted([computers[i], computers[j], computers[k]]))
                    triplets.add(triplet)
                    
    return triplets


def count_t_triplets(triplets):
    """
    Count triplets containing at least one computer starting with 't'
    """
    count = 0
    for triplet in triplets:
        if any(comp.startswith('t') for comp in triplet):
            count += 1
    return count


def part1(content):
    """
    Find all sets of three inter-connected computers and count those
    containing at least one computer with a name starting with 't'
    """
    start_time = time.time()
    
    # Parse input and build graph
    connections = parse_input(content)
    graph = build_graph(connections)
    
    # Find all triplets
    triplets = find_triplets(graph)
    
    # Count triplets with 't' computers
    result = count_t_triplets(triplets)
    
    return {
        "value": result,
        "execution_time": time.time() - start_time
    }


def is_clique(graph, nodes):
    """
    Check if all nodes in the set are connected to each other
    """
    for node in nodes:
        # For each node, check if it's connected to all other nodes
        for other in nodes:
            if other != node and other not in graph[node]:
                return False
    return True

def find_maximal_cliques(graph, current_clique, candidates, excluded):
    """Find all maximal cliques using Bron-Kerbosch algorithm with pivoting"""
    if not candidates and not excluded:
        return [current_clique]
    
    # Choose a pivot vertex to optimize
    pivot = None
    max_connections = -1
    for vertex in candidates.union(excluded):
        connections = len(graph[vertex])
        if connections > max_connections:
            max_connections = connections
            pivot = vertex
            
    pivot_neighbors = graph[pivot] if pivot else set()
    
    result = []
    candidates_copy = candidates.copy()
    for v in candidates - pivot_neighbors:
        new_candidates = candidates.intersection(graph[v])
        new_excluded = excluded.intersection(graph[v])
        new_result = find_maximal_cliques(
            graph,
            current_clique.union({v}),
            new_candidates,
            new_excluded
        )
        result.extend(new_result)
        candidates_copy.remove(v)
        excluded.add(v)
    
    return result


def find_largest_clique(graph):
    """
    Find the largest set of computers that are all connected to each other.
    Returns the set of computer names in the largest clique.
    """
    # Start with all nodes as candidates
    all_nodes = set(graph.keys())
    cliques = find_maximal_cliques(graph, set(), all_nodes, set())
    
    # Find the largest clique
    largest_clique = max(cliques, key=len)
    return largest_clique


def part2(content):
    """
    Find the largest set of fully connected computers and return their names
    as a comma-separated string in alphabetical order
    """
    start_time = time.time()
    
    # Parse input and build graph
    connections = parse_input(content)
    graph = build_graph(connections)
    
    # Find the largest clique
    largest_clique = find_largest_clique(graph)
    
    # Sort the computer names alphabetically and join with commas
    result = ",".join(sorted(largest_clique))
    
    return {
        "value": result,
        "execution_time": time.time() - start_time
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
    files = []
    for f in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, f)):
            files.append(f)
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