#!/usr/bin/python3

'''
--- Day 11: Reactor ---

You hear some loud beeping coming from a hatch in the floor of the factory, so you decide to check it out. Inside, you find several large electrical conduits and a ladder.

Climbing down the ladder, you discover the source of the beeping: a large, toroidal reactor which powers the factory above. Some Elves here are hurriedly running between the reactor and a nearby server rack, apparently trying to fix something.

One of the Elves notices you and rushes over. "It's a good thing you're here! We just installed a new server rack, but we aren't having any luck getting the reactor to communicate with it!" You glance around the room and see a tangle of cables and devices running from the server rack to the reactor. She rushes off, returning a moment later with a list of the devices and their outputs (your puzzle input).

For example:

aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out

Each line gives the name of a device followed by a list of the devices to which its outputs are attached. So, bbb: ddd eee means that device bbb has two outputs, one leading to device ddd and the other leading to device eee.

The Elves are pretty sure that the issue isn't due to any specific device, but rather that the issue is triggered by data following some specific path through the devices. Data only ever flows from a device through its outputs; it can't flow backwards.

After dividing up the work, the Elves would like you to focus on the devices starting with the one next to you (an Elf hastily attaches a label which just says you) and ending with the main output to the reactor (which is the device with the label out).

To help the Elves figure out which path is causing the issue, they need you to find every path from you to out.

In this example, these are all of the paths from you to out:

Data could take the connection from you to bbb, then from bbb to ddd, then from ddd to ggg, then from ggg to out.
Data could take the connection to bbb, then to eee, then to out.
Data could go to ccc, then ddd, then ggg, then out.
Data could go to ccc, then eee, then out.
Data could go to ccc, then fff, then out.
In total, there are 5 different paths leading from you to out.

How many different paths lead from you to out?


--- Part Two ---

Thanks in part to your analysis, the Elves have figured out a little bit about the issue. They now know that the problematic data path passes through both dac (a digital-to-analog converter) and fft (a device which performs a fast Fourier transform).

They're still not sure which specific path is the problem, and so they now need you to find every path from svr (the server rack) to out. However, the paths you find must all also visit both dac and fft (in any order).

For example:

svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out

This new list of devices contains many paths from svr to out:

svr,aaa,fft,ccc,ddd,hub,fff,ggg,out
svr,aaa,fft,ccc,ddd,hub,fff,hhh,out
svr,aaa,fft,ccc,eee,dac,fff,ggg,out
svr,aaa,fft,ccc,eee,dac,fff,hhh,out
svr,bbb,tty,ccc,ddd,hub,fff,ggg,out
svr,bbb,tty,ccc,ddd,hub,fff,hhh,out
svr,bbb,tty,ccc,eee,dac,fff,ggg,out
svr,bbb,tty,ccc,eee,dac,fff,hhh,out

However, only 2 paths from svr to out visit both dac and fft.

Find all of the paths that lead from svr to out. How many of those paths visit both dac and fft?
'''

import os
import sys
import time
import threading
from collections import defaultdict, deque
from colorama import init, Fore, Style

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 5,
        "part2": None,  
    },
    "test_II.txt": {
        "part1": None,  
        "part2": 2,
    },
    "input_I.txt": {
        "part1": 472, 
        "part2": 526811953334940,  
    }
}

TEST_STATUS = {
    "PASSED": "PASSED",
    "FAILED": "FAILED", 
    "IN_PROGRESS": "IN_PROGRESS",
    "NOT_APPLICABLE": "NOT_APPLICABLE",  
    "UNKNOWN": "UNKNOWN"
}

STATUS_COLORS = {
    TEST_STATUS["PASSED"]: Fore.GREEN,
    TEST_STATUS["FAILED"]: Fore.RED,
    TEST_STATUS["IN_PROGRESS"]: Fore.YELLOW,
    TEST_STATUS["NOT_APPLICABLE"]: Fore.LIGHTBLACK_EX,  
    TEST_STATUS["UNKNOWN"]: Fore.BLUE
}

# Global variables for progress tracking
progress_lock = threading.Lock()
progress_count = 0
progress_start_time = 0
progress_active = False
progress_interval = 0.5


def print_header(filename, part):
    """Simple header printing function"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Part {part}")
    print(f"{Fore.CYAN}{'='*80}\n")


def parse_input(content):
    """Parse the graph from input."""
    graph = defaultdict(list)
    lines = content.strip().split('\n')
    
    for line in lines:
        if not line.strip():
            continue
            
        parts = line.split(':')
        if len(parts) < 2:
            continue
            
        device = parts[0].strip()
        outputs = [out.strip() for out in parts[1].strip().split()]
        
        for output in outputs:
            graph[device].append(output)
    
    return graph


def count_paths_dag(graph, start, end):
    """Count paths in a Directed Acyclic Graph using DP."""
    if start not in graph:
        return 0
    
    # First check if graph is acyclic by doing topological sort
    indegree = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1
    
    # Find all nodes reachable from start
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, []):
            queue.append(neighbor)
    
    # Only consider nodes reachable from start
    reachable_nodes = list(visited)
    
    # Try to do topological sort on reachable subgraph
    topo_order = []
    zero_indegree = deque([start])
    local_indegree = defaultdict(int)
    
    # Recalculate indegree for reachable nodes
    for node in reachable_nodes:
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                local_indegree[neighbor] += 1
    
    while zero_indegree:
        node = zero_indegree.popleft()
        topo_order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                local_indegree[neighbor] -= 1
                if local_indegree[neighbor] == 0:
                    zero_indegree.append(neighbor)
    
    # If we couldn't get all nodes, graph has cycles
    if len(topo_order) != len(reachable_nodes):
        return None  # Graph has cycles
    
    # DP on topological order
    dp = defaultdict(int)
    dp[start] = 1
    
    for node in topo_order:
        if dp[node] > 0:
            for neighbor in graph.get(node, []):
                if neighbor in visited:
                    dp[neighbor] += dp[node]
    
    return dp.get(end, 0)


def count_paths_with_cycles(graph, start, end):
    """Count all paths in a directed graph that may have cycles."""
    if start not in graph:
        return 0
    
    # Use DFS with visited tracking to avoid infinite loops
    count = 0
    sys.setrecursionlimit(10000)
    
    def dfs(node, visited):
        nonlocal count
        
        if node == end:
            count += 1
            return
        
        if node in visited:
            return
        
        visited.add(node)
        
        for neighbor in graph.get(node, []):
            dfs(neighbor, visited)
        
        visited.remove(node)
    
    dfs(start, set())
    return count


def count_paths_with_cycles_iterative(graph, start, end):
    """Count all paths in a directed graph using iterative DFS."""
    if start not in graph:
        return 0
    
    count = 0
    stack = [(start, set([start]))]
    
    while stack:
        node, visited = stack.pop()
        
        if node == end:
            count += 1
            continue
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                new_visited = visited.copy()
                new_visited.add(neighbor)
                stack.append((neighbor, new_visited))
    
    return count


def count_paths_with_required(graph, start, end, required):
    """Count paths with SMART GRAPH DECOMPOSITION."""
    if start not in graph:
        return 0
    
    if not required:
        result = count_paths_dag(graph, start, end)
        if result is not None:
            return result
        return count_paths_with_cycles_iterative(graph, start, end)
    
    # Map required nodes to bit positions
    node_to_bit = {node: i for i, node in enumerate(sorted(required))}
    all_required_mask = (1 << len(required)) - 1
    
    print(f"{Fore.CYAN}Analyzing graph structure...")
    
    # Check if graph is DAG - if so, we can use DP!
    indegree = defaultdict(int)
    all_nodes = set(graph.keys())
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1
            all_nodes.add(neighbor)
    
    # Try topological sort
    topo_order = []
    queue = deque([n for n in all_nodes if indegree[n] == 0])
    local_indegree = indegree.copy()
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph.get(node, []):
            local_indegree[neighbor] -= 1
            if local_indegree[neighbor] == 0:
                queue.append(neighbor)
    
    is_dag = len(topo_order) == len(all_nodes)
    
    if is_dag:
        print(f"{Fore.GREEN}✓ Graph is a DAG! Using dynamic programming...")
        return count_paths_dag_with_required(graph, start, end, required, node_to_bit, all_required_mask, topo_order)
    
    print(f"{Fore.YELLOW}Graph has cycles, using optimized DFS...")
    
    # Pre-compute reachability
    reachable_required = {}
    for node in all_nodes:
        mask = 0
        visited = {node}
        queue = deque([node])
        while queue:
            curr = queue.popleft()
            if curr in node_to_bit:
                mask |= (1 << node_to_bit[curr])
            for neighbor in graph.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        reachable_required[node] = mask
    
    count = 0
    visited = set()
    total_iterations = 0
    last_print = time.time()
    start_time = time.time()
    
    def dfs_backtrack(node, mask, depth=0):
        nonlocal count, total_iterations, last_print
        
        total_iterations += 1
        
        if total_iterations % 100000 == 0:
            current_time = time.time()
            if current_time - last_print > 0.5:
                elapsed = current_time - start_time
                rate = total_iterations / elapsed if elapsed > 0 else 0
                eta_str = f"{elapsed:.0f}s elapsed"
                
                if elapsed > 60 and count > 10000000:
                    eta_str = f"{Fore.RED}Problem may have >1B solutions!"
                
                print(f"\r{Fore.CYAN}[{Fore.YELLOW}{total_iterations:,}{Fore.CYAN}] "
                      f"iter | {Fore.GREEN}{count:,}{Fore.CYAN} paths | "
                      f"{Fore.MAGENTA}{rate:,.0f}{Fore.CYAN}/s | {eta_str}", 
                      end="", flush=True)
                last_print = current_time
        
        current_mask = mask
        if node in node_to_bit:
            current_mask = mask | (1 << node_to_bit[node])
        
        if node == end:
            if current_mask == all_required_mask:
                count += 1
            return
        
        needed_mask = all_required_mask ^ current_mask
        if needed_mask != 0:
            if (reachable_required.get(node, 0) & needed_mask) != needed_mask:
                return
        
        if depth > 250:
            return
        
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_backtrack(neighbor, current_mask, depth + 1)
        visited.remove(node)
    
    dfs_backtrack(start, 0)
    print("\r" + " " * 120 + "\r", end="", flush=True)
    return count


def count_paths_dag_with_required(graph, start, end, required, node_to_bit, all_required_mask, topo_order):
    """DP for DAGs with required nodes - MUCH FASTER!"""
    # dp[node][mask] = number of paths from node to end with mask of required nodes visited
    dp = defaultdict(lambda: defaultdict(int))
    
    # Process in reverse topological order
    for node in reversed(topo_order):
        if node == end:
            # Base case: at end, count only if all required visited
            for mask in range(1 << len(node_to_bit)):
                dp[node][mask] = 1 if mask == all_required_mask else 0
        else:
            # Aggregate from all neighbors
            for mask in range(1 << len(node_to_bit)):
                current_mask = mask
                if node in node_to_bit:
                    current_mask = mask | (1 << node_to_bit[node])
                
                for neighbor in graph.get(node, []):
                    dp[node][mask] += dp[neighbor][current_mask]
    
    return dp[start][0]


def optimize_graph_for_start(graph, start):
    """Remove nodes not reachable from start and their edges."""
    if start not in graph:
        return graph
    
    # Find all nodes reachable from start
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, []):
            stack.append(neighbor)
    
    # Create new graph with only reachable nodes
    new_graph = defaultdict(list)
    for node in visited:
        if node in graph:
            for neighbor in graph[node]:
                if neighbor in visited:
                    new_graph[node].append(neighbor)
    
    return new_graph


def part1(content):
    """Solution for Part 1: Count all paths from 'you' to 'out'."""
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Counting all paths from 'you' to 'out'...")
    
    graph = parse_input(content)
    
    # Check if we have the required nodes
    if 'you' not in graph:
        print(f"{Fore.RED}Error: Starting node 'you' not found in graph!")
        return {
            "value": 0,
            "execution_time": time.time() - start_time,
            "status": TEST_STATUS["FAILED"]
        }
    
    # Optimize graph
    optimized_graph = optimize_graph_for_start(graph, 'you')
    print(f"{Fore.YELLOW}Original graph: {len(graph)} nodes")
    print(f"{Fore.YELLOW}Optimized graph: {len(optimized_graph)} reachable nodes from 'you'")
    
    # Try DAG algorithm first
    print(f"{Fore.CYAN}Trying DAG algorithm...")
    result = count_paths_dag(optimized_graph, 'you', 'out')
    
    if result is None:
        print(f"{Fore.YELLOW}Graph has cycles, using iterative DFS...")
        result = count_paths_with_cycles_iterative(optimized_graph, 'you', 'out')
    
    elapsed = time.time() - start_time
    
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Part 1 Summary:")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Total paths from 'you' to 'out': {result:,}")
    print(f"{Fore.CYAN}Total time: {elapsed:.3f}s")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": elapsed,
        "graph_size": len(graph),
        "optimized_size": len(optimized_graph)
    }


def part2(content):
    """Solution for Part 2: Count all paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Counting paths from 'svr' to 'out' visiting both 'dac' and 'fft'...")
    
    graph = parse_input(content)
    
    # Check if we have the required nodes
    required_nodes = {'dac', 'fft'}
    
    # First, optimize graph to only include nodes reachable from 'svr'
    if 'svr' not in graph:
        print(f"{Fore.RED}Error: Starting node 'svr' not found in graph!")
        return {
            "value": 0,
            "execution_time": time.time() - start_time,
            "status": TEST_STATUS["FAILED"]
        }
    
    optimized_graph = optimize_graph_for_start(graph, 'svr')
    print(f"{Fore.YELLOW}Original graph: {len(graph)} nodes")
    print(f"{Fore.YELLOW}Optimized graph: {len(optimized_graph)} reachable nodes from 'svr'")
    print(f"{Fore.YELLOW}Required nodes: {required_nodes}")
    
    # Check if required nodes are in optimized graph
    missing_required = []
    for node in required_nodes:
        if node not in optimized_graph and node != 'out':
            # Check if node might be reachable (as a leaf)
            found = False
            for src in optimized_graph:
                if node in optimized_graph[src]:
                    found = True
                    break
            if not found and node != 'out':
                missing_required.append(node)
    
    if missing_required:
        print(f"{Fore.YELLOW}Warning: Some required nodes not reachable from 'svr': {missing_required}")
        return {
            "value": 0,
            "execution_time": time.time() - start_time,
            "status": TEST_STATUS["FAILED"]
        }
    
    print(f"{Fore.CYAN}Starting path counting with iterative DFS and bitmask tracking...")
    print(f"{Fore.CYAN}This may take a while for large graphs...")
    
    result = count_paths_with_required(optimized_graph, 'svr', 'out', required_nodes)
    
    elapsed = time.time() - start_time
    
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Part 2 Summary:")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Paths from 'svr' to 'out' visiting both 'dac' and 'fft': {result:,}")
    print(f"{Fore.CYAN}Total time: {elapsed:.1f}s")
    
    if elapsed > 0:
        print(f"{Fore.CYAN}Processing rate: {result/elapsed:,.0f} paths counted/second")
    
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": elapsed,
        "graph_size": len(graph),
        "optimized_size": len(optimized_graph)
    }


def determine_test_status(result, expected, filename, part_name):
    """Determine the test status based on the result and expected value."""
    if expected is None:
        return TEST_STATUS["NOT_APPLICABLE"]
    
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
            return TEST_STATUS["FAILED"]
    except ValueError:
        return TEST_STATUS["UNKNOWN"]


def get_status_color(status):
    """Get the appropriate color for each status"""
    return STATUS_COLORS.get(status, Fore.WHITE)


def process_file(filepath):
    """Process a single file and validate results against test solutions"""
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            
            print_header(filename, 1)
            part1_result = part1(content)
            
            print_header(filename, 2)
            part2_result = part2(content)
            
            test_solution = TEST_SOLUTIONS.get(filename, {})
            
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
    
    files = []
    for f in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, f)):
            files.append(f)
    
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
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.3f}s")
                
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    expected_value = TEST_SOLUTIONS.get(file, {}).get(part_name, "N/A")
                    expected_str = str(expected_value)
                    print(f"       {Fore.RED}Expected: {expected_str}")
                    all_tests_passed = False

        else:
            print(f"  {Fore.RED}Error - {result}")
            all_tests_passed = False
    
    print(f"\n{Fore.CYAN}{'='*80}")
    if all_tests_passed:
        print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"{Fore.RED}❌ SOME TESTS FAILED")
    print(f"{Fore.CYAN}{'='*80}")


def main():
    """Main function with improved error handling and command line support"""
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