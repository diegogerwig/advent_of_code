#!/usr/bin/python3

'''
--- Day 8: Playground ---
'''

import os
import sys
import time
import math
from colorama import init, Fore    # type: ignore
from heapq import heappush, heappop

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": '40',  
        "part2": '25272',  
    },
    "input_I.txt": {
        "part1": '66912', 
        "part2": '724454082',  
    }
}

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


def print_header(filename, part):
    """Simple header printing function"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Part {part}")
    print(f"{Fore.CYAN}{'='*80}\n")


def parse_input(content):
    """
    Parse junction box positions.
    Returns list of (x, y, z) tuples.
    """
    lines = content.strip().split('\n')
    positions = []
    for line in lines:
        if line.strip():
            x, y, z = map(int, line.strip().split(','))
            positions.append((x, y, z))
    return positions


def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def find_parent(parent, x):
    """Find parent with path compression"""
    if parent[x] != x:
        parent[x] = find_parent(parent, parent[x])
    return parent[x]


def union_sets(parent, size, x, y):
    """Union two sets"""
    root_x = find_parent(parent, x)
    root_y = find_parent(parent, y)
    
    if root_x == root_y:
        return False  # Already in same set
    
    # Union by size
    if size[root_x] < size[root_y]:
        root_x, root_y = root_y, root_x
    
    parent[root_y] = root_x
    size[root_x] += size[root_y]
    return True


def get_component_sizes(parent, n):
    """Get sizes of all components"""
    roots = {}
    for i in range(n):
        root = find_parent(parent, i)
        if root not in roots:
            # Count all nodes with this root
            count = 0
            for j in range(n):
                if find_parent(parent, j) == root:
                    count += 1
            roots[root] = count
    return list(roots.values())


def solve_part1(positions, target_pairs):
    """
    Solve Part 1: Consider target_pairs shortest pairs and multiply sizes of 3 largest circuits.
    """
    n = len(positions)
    
    # Create priority queue of all distances
    heap = []
    
    # Calculate all pairwise distances
    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_distance(positions[i], positions[j])
            # Use a tuple with distance and indices for consistent ordering
            heappush(heap, (dist, i, j))
    
    # Initialize Union-Find arrays
    parent = list(range(n))
    size = [1] * n
    
    # Process target_pairs shortest pairs
    pairs_considered = 0
    
    while heap and pairs_considered < target_pairs:
        dist, i, j = heappop(heap)
        pairs_considered += 1
        
        # Try to connect (whether successful or not)
        union_sets(parent, size, i, j)
    
    # Get component sizes and find 3 largest
    component_sizes = get_component_sizes(parent, n)
    component_sizes.sort(reverse=True)
    
    # Multiply 3 largest
    if len(component_sizes) >= 3:
        result = component_sizes[0] * component_sizes[1] * component_sizes[2]
    else:
        # If less than 3 components, multiply all
        result = 1
        for sz in component_sizes:
            result *= sz
    
    return result


def count_components(parent, n):
    """Count number of components"""
    unique_roots = set()
    for i in range(n):
        root = find_parent(parent, i)
        unique_roots.add(root)
    return len(unique_roots)


def solve_part2(positions, debug=False):
    """
    Solve Part 2: Connect until all boxes are in one circuit, then return product of X coordinates
    of the last connection that completed the circuit.
    """
    n = len(positions)
    
    # Create priority queue of all distances
    heap = []
    
    # Calculate all pairwise distances
    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_distance(positions[i], positions[j])
            # Use a tuple with distance and indices for consistent ordering
            heappush(heap, (dist, i, j))
    
    # Initialize Union-Find arrays
    parent = list(range(n))
    size = [1] * n
    
    last_connection_info = None
    connection_count = 0
    
    if debug:
        print(f"{Fore.MAGENTA}Debug - Looking for last connection that completes the circuit...")
        initial_components = count_components(parent, n)
        print(f"{Fore.MAGENTA}Initial components: {initial_components}")
    
    # Keep connecting until all are in one circuit
    while heap and count_components(parent, n) > 1:
        dist, i, j = heappop(heap)
        
        # Try to connect
        if union_sets(parent, size, i, j):
            # This was a successful connection
            connection_count += 1
            
            # Check if this completed the circuit
            if count_components(parent, n) == 1:
                # Store info about this connection (the one that completed the circuit)
                last_connection_info = (i, j, dist, connection_count)
                
                if debug:
                    print(f"{Fore.MAGENTA}  Final connection #{connection_count}:")
                    print(f"{Fore.MAGENTA}    Box {i}: {positions[i]} (X={positions[i][0]})")
                    print(f"{Fore.MAGENTA}    Box {j}: {positions[j]} (X={positions[j][0]})")
                    print(f"{Fore.MAGENTA}    Distance: {dist:.2f}")
                    print(f"{Fore.MAGENTA}    Product of X coordinates: {positions[i][0] * positions[j][0]}")
    
    # After loop, all boxes should be in one circuit
    if last_connection_info:
        i, j, dist, conn_num = last_connection_info
        # Multiply X coordinates of the last connection
        result = positions[i][0] * positions[j][0]
        
        if debug:
            print(f"{Fore.MAGENTA}Debug - Found last connection:")
            print(f"{Fore.MAGENTA}  Connection #{conn_num}")
            print(f"{Fore.MAGENTA}  Between boxes {i} and {j}")
            print(f"{Fore.MAGENTA}  Positions: {positions[i]} and {positions[j]}")
            print(f"{Fore.MAGENTA}  X coordinates: {positions[i][0]} and {positions[j][0]}")
            print(f"{Fore.MAGENTA}  Product: {result}")
        
        return result
    else:
        # Should not happen if n > 1
        return 0


def part1(content):
    """
    Solution for Part 1: Consider 1000 shortest pairs and multiply sizes of 3 largest circuits.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Connecting junction boxes...")
    
    # Parse junction box positions
    positions = parse_input(content)
    n = len(positions)
    
    print(f"{Fore.YELLOW}Number of junction boxes: {n}")
    
    # Determine number of pairs to consider
    target_pairs = 1000  # Default for main input
    
    # For test file, use 10 pairs
    if n == 20:  # Test file has 20 boxes
        target_pairs = 10
        print(f"{Fore.YELLOW}Test file detected - considering {target_pairs} shortest pairs")
    
    print(f"{Fore.YELLOW}Target pairs to consider: {target_pairs}")
    
    # Solve
    result = solve_part1(positions, target_pairs)
    
    # Print summary
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Junction Box Connection Summary (Part 1):")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Three largest circuits product: {result}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": time.time() - start_time,
        "problems_count": 1,
        "results": [{"product": result}]
    }


def part2(content):
    """
    Solution for Part 2: Connect until all in one circuit, then multiply X coordinates
    of the last connection.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Connecting until all boxes are in one circuit...")
    
    # Parse junction box positions
    positions = parse_input(content)
    n = len(positions)
    
    print(f"{Fore.YELLOW}Number of junction boxes: {n}")
    
    # Determine if this is test file for debugging
    debug = (n == 20)  # Test file has 20 boxes
    
    # Solve
    result = solve_part2(positions, debug)
    
    # Print summary
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Part 2 Summary:")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Product of X coordinates of last connection: {result}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": time.time() - start_time,
        "problems_count": 1,
        "results": [{"product": result}]
    }


def determine_test_status(result, expected, filename, part_name):
    """
    Determine the test status based on the result and expected value.
    """
    if expected == 'N/A':
        return TEST_STATUS["IN_PROGRESS"]
    
    try:
        result_value = result["value"]
        if isinstance(result_value, str) and result_value == 'N/A':
            return TEST_STATUS["IN_PROGRESS"]
        
        expected_value = int(expected)
        
        if result_value == expected_value:
            return TEST_STATUS["PASSED"]
        else:
            print(f"{Fore.RED}✗ TEST FAILED for {filename} {part_name}")
            print(f"{Fore.RED}  Expected: {expected_value}")
            print(f"{Fore.RED}  Got: {result_value}")
            
            if "problems_count" in result:
                print(f"{Fore.RED}  Problems count: {result['problems_count']}")
            
            return TEST_STATUS["FAILED"]
    except ValueError:
        return TEST_STATUS["UNKNOWN"]


def get_status_color(status):
    """
    Get the appropriate color for each status
    """
    return STATUS_COLORS.get(status, Fore.WHITE)


def process_file(filepath):
    """
    Process a single file and validate results against test solutions
    """
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
            
            # Add status to results with detailed checking
            part1_result["status"] = determine_test_status(
                part1_result, 
                test_solution.get("part1", "N/A"),
                filename,
                "Part 1"
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", "N/A"),
                filename, 
                "Part 2"
            )
            
            return True, {
                "part1": part1_result,
                "part2": part2_result
            }
            
    except Exception as e:
        print(f"{Fore.RED}Error processing {filename}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, str(e)


def process_directory(input_dir="./input/"):
    """Process all files in the specified directory, tests first"""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    print(f"\n{Fore.CYAN}Processing files in directory: {Fore.YELLOW}{input_dir}")
    
    # Get all files and sort them to process test files first
    files = []
    for f in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, f)):
            files.append(f)
    
    # Sort files: test files first, then input files
    def sort_key(filename):
        if filename.startswith('test'):
            return (0, filename)
        elif filename.startswith('input'):
            return (1, filename)
        else:
            return (2, filename)
    
    files.sort(key=sort_key)
    
    results = {}
    
    for file in files:
        filepath = os.path.join(input_dir, file)
        print(f"\n{Fore.YELLOW}Processing: {file}")
        success, result = process_file(filepath)
        results[file] = (success, result)
    
    return results


def print_results(results):
    """Print results with enhanced status display"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    # Print test files first, then input files
    sorted_files = sorted(results.keys(), key=lambda x: (0 if x.startswith('test') else 1, x))
    
    all_tests_passed = True
    
    for file in sorted_files:
        success, result = results[file]
        print(f"\n{Fore.BLUE}{file}:")
        
        if success:
            for part_name, part_result in result.items():
                status_color = get_status_color(part_result["status"])
                status_text = f"[{part_result['status']}]"
                
                value = part_result['value']
                value_str = str(value)
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{value_str:<20} "
                      f"{status_color}{status_text:<20} "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
                
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    expected_value = TEST_SOLUTIONS.get(file, {}).get(part_name, "N/A")
                    expected_str = str(expected_value)
                    print(f"       {Fore.RED}Expected: {expected_str}")
                    all_tests_passed = False

        else:
            print(f"  {Fore.RED}Error - {result}")
            all_tests_passed = False
    
    # Print overall test summary
    print(f"\n{Fore.CYAN}{'='*80}")
    if all_tests_passed:
        print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"{Fore.RED}❌ SOME TESTS FAILED")
    print(f"{Fore.CYAN}{'='*80}")


def main():
    """
    Main function with improved error handling and command line support
    """
    try:
        input_dir = "./input/"
        if len(sys.argv) > 1:
            input_dir = sys.argv[1]
        
        results = process_directory(input_dir)
        print_results(results)
        
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()