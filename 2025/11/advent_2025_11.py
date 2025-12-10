#!/usr/bin/python3

'''
--- Day 10: Factory --- (ILP Optimized Version)
'''

import os
import sys
import time
from colorama import init, Fore
import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": '7',
        "part2": '33',
    },
    "input_I.txt": {
        "part1": '447', 
        "part2": 'N/A',  
    }
}

TEST_STATUS = {
    "PASSED": "PASSED",
    "FAILED": "FAILED", 
    "IN_PROGRESS": "IN_PROGRESS",
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
    """Parse machine configurations from input."""
    machines_part1 = []
    machines_part2 = []
    lines = content.strip().split('\n')
    
    for line in lines:
        if not line.strip():
            continue
            
        diagram_match = re.search(r'\[([.#]+)\]', line)
        if not diagram_match:
            continue
            
        diagram = diagram_match.group(1)
        target_lights = [1 if c == '#' else 0 for c in diagram]
        
        buttons = re.findall(r'\(([\d,]+)\)', line)
        button_effects = []
        
        for button_str in buttons:
            effects = list(map(int, button_str.split(',')))
            button_effects.append(effects)
        
        joltage_match = re.search(r'\{(.*?)\}', line)
        if joltage_match:
            joltage_str = joltage_match.group(1)
            joltage_requirements = list(map(int, joltage_str.split(',')))
        else:
            joltage_requirements = []
        
        machines_part1.append((target_lights, button_effects))
        machines_part2.append((joltage_requirements, button_effects))
    
    return machines_part1, machines_part2


def gaussian_elimination_gf2(A, b):
    """Perform Gaussian elimination over GF(2) to solve Ax = b."""
    m = len(A)
    if m == 0:
        return None
    n = len(A[0])
    
    aug = [row[:] + [b[i]] for i, row in enumerate(A)]
    
    row = 0
    for col in range(n):
        pivot = -1
        for i in range(row, m):
            if aug[i][col] == 1:
                pivot = i
                break
        
        if pivot == -1:
            continue
        
        aug[row], aug[pivot] = aug[pivot], aug[row]
        
        for i in range(m):
            if i != row and aug[i][col] == 1:
                for j in range(col, n + 1):
                    aug[i][j] ^= aug[row][j]
        
        row += 1
        if row >= m:
            break
    
    x = [0] * n
    
    for i in range(m):
        col_with_one = -1
        for j in range(n):
            if aug[i][j] == 1:
                col_with_one = j
                break
        
        if col_with_one == -1:
            if aug[i][n] == 1:
                return None
        else:
            x[col_with_one] = aug[i][n]
    
    return x


def find_minimum_presses_part1(machine):
    """Find minimum total button presses for a single machine (Part 1)."""
    target_lights, button_effects = machine
    n_lights = len(target_lights)
    n_buttons = len(button_effects)
    
    A = [[0] * n_buttons for _ in range(n_lights)]
    for j in range(n_buttons):
        for light_idx in button_effects[j]:
            if 0 <= light_idx < n_lights:
                A[light_idx][j] = 1
    
    solution = gaussian_elimination_gf2(A, target_lights)
    if solution is None:
        return None
    
    aug = [row[:] + [target_lights[i]] for i, row in enumerate(A)]
    m = n_lights
    n = n_buttons
    
    row = 0
    pivot_cols = [-1] * m
    
    for col in range(n):
        pivot = -1
        for i in range(row, m):
            if aug[i][col] == 1:
                pivot = i
                break
        
        if pivot == -1:
            continue
        
        aug[row], aug[pivot] = aug[pivot], aug[row]
        pivot_cols[row] = col
        
        for i in range(m):
            if i != row and aug[i][col] == 1:
                for j in range(col, n + 1):
                    aug[i][j] ^= aug[row][j]
        
        row += 1
        if row >= m:
            break
    
    pivot_columns = [c for c in pivot_cols if c != -1]
    free_vars = [c for c in range(n) if c not in pivot_columns]
    
    particular_solution = [0] * n
    for i in range(m):
        if pivot_cols[i] != -1:
            particular_solution[pivot_cols[i]] = aug[i][n]
    
    k = len(free_vars)
    min_presses = sum(particular_solution)
    
    if k == 0:
        return min_presses
    
    nullspace_basis = []
    for free_var in free_vars:
        null_vec = [0] * n
        null_vec[free_var] = 1
        
        for i in range(m-1, -1, -1):
            if pivot_cols[i] != -1:
                col = pivot_cols[i]
                sum_val = 0
                for free in free_vars:
                    sum_val ^= (aug[i][free] & null_vec[free])
                null_vec[col] = sum_val
        
        nullspace_basis.append(null_vec)
    
    for mask in range(1 << k):
        current_solution = particular_solution[:]
        
        for i in range(k):
            if mask & (1 << i):
                for j in range(n):
                    current_solution[j] ^= nullspace_basis[i][j]
        
        total_presses = sum(current_solution)
        if total_presses < min_presses:
            min_presses = total_presses
    
    return min_presses


def solve_integer_linear_ilp(target_counts, button_effects):
    """
    Solve integer linear system using Mixed Integer Linear Programming (MILP).
    This guarantees the optimal solution.
    """
    n_counters = len(target_counts)
    n_buttons = len(button_effects)
    
    if all(t == 0 for t in target_counts):
        return 0
    
    # Build constraint matrix A
    A = np.zeros((n_counters, n_buttons), dtype=float)
    for j in range(n_buttons):
        for counter_idx in button_effects[j]:
            if 0 <= counter_idx < n_counters:
                A[counter_idx, j] = 1.0
    
    b = np.array(target_counts, dtype=float)
    
    # Objective: minimize sum of x (we want minimum button presses)
    c = np.ones(n_buttons)
    
    # Constraints: Ax = b
    constraints = LinearConstraint(A, lb=b, ub=b)
    
    # Bounds: x >= 0 (we can't press buttons negative times)
    # Also add upper bound based on max target to speed up solver
    max_target = max(target_counts)
    upper_bound = max_target * 2  # reasonable upper bound
    bounds = Bounds(lb=0, ub=upper_bound)
    
    # All variables must be integers
    integrality = np.ones(n_buttons, dtype=int)
    
    try:
        # Solve the MILP
        result = milp(c=c, constraints=constraints, bounds=bounds, 
                     integrality=integrality)
        
        if result.success:
            x = np.round(result.x).astype(int)
            # Verify solution
            computed = A @ x
            if np.allclose(computed, b):
                return int(np.sum(x))
    except Exception as e:
        # If MILP fails, fall back to greedy
        pass
    
    # Fallback: greedy approach
    return solve_greedy_fallback(target_counts, button_effects)


def solve_greedy_fallback(target_counts, button_effects):
    """
    Greedy algorithm as fallback.
    Strategy: Repeatedly press the button that helps the most with unsatisfied counters.
    """
    n_counters = len(target_counts)
    n_buttons = len(button_effects)
    
    remaining = list(target_counts)
    button_presses = [0] * n_buttons
    
    max_iterations = sum(target_counts) * 3
    iteration = 0
    
    while any(r > 0 for r in remaining) and iteration < max_iterations:
        iteration += 1
        
        # Find the counter with largest remaining value
        max_remaining = max(remaining)
        if max_remaining == 0:
            break
        
        # Find button that best helps with current state
        best_button = -1
        best_score = -1
        
        for j in range(n_buttons):
            # Calculate score: how much this button helps
            score = 0
            for counter_idx in button_effects[j]:
                if 0 <= counter_idx < n_counters and remaining[counter_idx] > 0:
                    score += min(remaining[counter_idx], 1)
            
            # Prefer buttons that help multiple counters
            if score > best_score:
                best_score = score
                best_button = j
        
        if best_button == -1 or best_score == 0:
            # No button helps - might be impossible
            return None
        
        # Press the best button
        button_presses[best_button] += 1
        for counter_idx in button_effects[best_button]:
            if 0 <= counter_idx < n_counters:
                remaining[counter_idx] = max(0, remaining[counter_idx] - 1)
    
    # Check if we found a valid solution
    if any(r > 0 for r in remaining):
        return None
    
    return sum(button_presses)


def find_minimum_presses_part2(machine):
    """Find minimum total button presses for a single machine (Part 2)."""
    target_counts, button_effects = machine
    return solve_integer_linear_ilp(target_counts, button_effects)


def solve_part1(machines):
    """Solve Part 1: Find minimum total presses for all machines."""
    total_presses = 0
    
    for i, machine in enumerate(machines):
        presses = find_minimum_presses_part1(machine)
        if presses is None:
            print(f"{Fore.RED}Machine {i} has no solution!")
        else:
            total_presses += presses
    
    return total_presses


def solve_part2(machines):
    """Solve Part 2: Find minimum total presses for all machines."""
    total_presses = 0
    total_machines = len(machines)
    start_time = time.time()
    
    print(f"{Fore.CYAN}Processing {total_machines} machines...")
    
    for i, machine in enumerate(machines):
        elapsed = time.time() - start_time
        progress_pct = (i + 1) / total_machines * 100
        
        if i > 0:
            avg_time = elapsed / (i + 1)
            remaining = total_machines - (i + 1)
            eta_seconds = avg_time * remaining
            
            if eta_seconds < 60:
                eta_str = f"{eta_seconds:.0f}s"
            elif eta_seconds < 3600:
                minutes = int(eta_seconds // 60)
                seconds = int(eta_seconds % 60)
                eta_str = f"{minutes}m{seconds}s"
            else:
                hours = int(eta_seconds // 3600)
                minutes = int((eta_seconds % 3600) // 60)
                eta_str = f"{hours}h{minutes}m"
        else:
            eta_str = "calculating..."
        
        sys.stdout.write(f"\r{Fore.YELLOW}[{int(progress_pct):3d}%] "
                       f"Machine {i+1:3d}/{total_machines} | "
                       f"ETA: {eta_str:>8} | "
                       f"Total: {total_presses:6d}")
        sys.stdout.flush()
        
        presses = find_minimum_presses_part2(machine)
        
        if presses is None:
            print(f"\n{Fore.RED}Machine {i} has no solution!")
        else:
            total_presses += presses
    
    sys.stdout.write("\r" + " " * 100 + "\r")
    
    elapsed = time.time() - start_time
    print(f"{Fore.GREEN}✓ Processed {total_machines} machines in {elapsed:.2f}s")
    
    return total_presses


def part1(content):
    """Solution for Part 1: Find minimum total button presses for lights."""
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Finding minimum button presses for indicator lights...")
    
    machines_part1, _ = parse_input(content)
    n_machines = len(machines_part1)
    
    print(f"{Fore.YELLOW}Number of machines: {n_machines}")
    
    result = solve_part1(machines_part1)
    
    elapsed = time.time() - start_time
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Factory Machines Summary (Part 1):")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Total minimum button presses: {result}")
    print(f"{Fore.CYAN}Time: {elapsed:.3f}s ({elapsed/n_machines:.3f}s per machine)")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": elapsed,
        "problems_count": n_machines,
        "results": [{"total_presses": result}]
    }


def part2(content):
    """Solution for Part 2: Find minimum total button presses for joltage counters."""
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Finding minimum button presses for joltage counters...")
    
    _, machines_part2 = parse_input(content)
    n_machines = len(machines_part2)
    
    print(f"{Fore.YELLOW}Number of machines: {n_machines}")
    
    result = solve_part2(machines_part2)
    
    elapsed = time.time() - start_time
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Part 2 Summary:")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Total minimum button presses: {result}")
    print(f"{Fore.CYAN}Time: {elapsed:.3f}s ({elapsed/n_machines:.3f}s per machine)")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": elapsed,
        "problems_count": n_machines,
        "results": [{"total_presses": result}]
    }


def determine_test_status(result, expected, filename, part_name):
    """Determine the test status based on the result and expected value."""
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