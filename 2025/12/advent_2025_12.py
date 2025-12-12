#!/usr/bin/python3

'''
--- Day 12: Christmas Tree Farm ---

You're almost out of time, but there can't be much left to decorate. Although there are no stairs, elevators, escalators, tunnels, chutes, teleporters, firepoles, or conduits here that would take you deeper into the North Pole base, there is a ventilation duct. You jump in.

After bumping around for a few minutes, you emerge into a large, well-lit cavern full of Christmas trees!

There are a few Elves here frantically decorating before the deadline. They think they'll be able to finish most of the work, but the one thing they're worried about is the presents for all the young Elves that live here at the North Pole. It's an ancient tradition to put the presents under the trees, but the Elves are worried they won't fit.

The presents come in a few standard but very weird shapes. The shapes and the regions into which they need to fit are all measured in standard units. To be aesthetically pleasing, the presents need to be placed into the regions in a way that follows a standardized two-dimensional unit grid; you also can't stack presents.

As always, the Elves have a summary of the situation (your puzzle input) for you. First, it contains a list of the presents' shapes. Second, it contains the size of the region under each tree and a list of the number of presents of each shape that need to fit into that region. For example:

0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2

The first section lists the standard present shapes. For convenience, each shape starts with its index and a colon; then, the shape is displayed visually, where # is part of the shape and . is not.

The second section lists the regions under the trees. Each line starts with the width and length of the region; 12x5 means the region is 12 units wide and 5 units long. The rest of the line describes the presents that need to fit into that region by listing the quantity of each shape of present; 1 0 1 0 3 2 means you need to fit one present with shape index 0, no presents with shape index 1, one present with shape index 2, no presents with shape index 3, three presents with shape index 4, and two presents with shape index 5.

Presents can be rotated and flipped as necessary to make them fit in the available space, but they have to always be placed perfectly on the grid. Shapes can't overlap (that is, the # part from two different presents can't go in the same place on the grid), but they can fit together (that is, the . part in a present's shape's diagram does not block another present from occupying that space on the grid).

The Elves need to know how many of the regions can fit the presents listed. In the above example, there are six unique present shapes and three regions that need checking.

The first region is 4x4:

....
....
....
....

In it, you need to determine whether you could fit two presents that have shape index 4:

###
#..
###

After some experimentation, it turns out that you can fit both presents in this region. Here is one way to do it, using A to represent one present and B to represent the other:

AAA.
ABAB
ABAB
.BBB

The second region, 12x5: 1 0 1 0 2 2, is 12 units wide and 5 units long. In that region, you need to try to fit one present with shape index 0, one present with shape index 2, two presents with shape index 4, and two presents with shape index 5.

It turns out that these presents can all fit in this region. Here is one way to do it, again using different capital letters to represent all the required presents:

....AAAFFE.E
.BBBAAFFFEEE
DDDBAAFFCECE
DBBB....CCC.
DDD.....C.C.

The third region, 12x5: 1 0 1 0 3 2, is the same size as the previous region; the only difference is that this region needs to fit one additional present with shape index 4. Unfortunately, no matter how hard you try, there is no way to fit all of the presents into this region.

So, in this example, 2 regions can fit all of their listed presents.

Consider the regions beneath each tree and the presents the Elves would like to fit into each of them. How many of the regions can fit all of the presents listed?


--- Part Two ---

The Elves thank you profusely for the help and start rearranging the oddly-shaped presents. As you look up, you notice that a lot more Elves have arrived here at the Christmas tree farm.

In fact, many of these new arrivals look familiar: they're the Elves you helped while decorating the North Pole base. Right on schedule, each group seems to have brought a star to put atop one of the Christmas trees!

Before any of them can find a ladder, a particularly large Christmas tree suddenly flashes brightly when a large star magically appears above it! As your eyes readjust, you think you notice a portly man with a white beard disappear into the crowd.

You go look for a ladder; only 23 stars to go.
'''

import os
import sys
import time
from collections import defaultdict
from colorama import init, Fore, Style

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": 2,
        "part2": None,  
    },
    "test_II.txt": {
        "part1": None,  
        "part2": None,
    },
    "input_I.txt": {
        "part1": 526, 
        "part2": None,  
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


def print_header(filename, part):
    """Simple header printing function"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Part {part}")
    print(f"{Fore.CYAN}{'='*80}\n")


def parse_input(content):
    """Parse shapes and regions from input."""
    lines = content.strip().split('\n')
    
    shapes = {}
    regions = []
    current_shape = None
    shape_lines = []
    
    i = 0
    n = len(lines)
    
    # First parse shapes
    while i < n:
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
            
        # Check if this is a shape definition (starts with digit:)
        if ':' in line and line[0].isdigit() and line.split(':')[0].strip().isdigit():
            if current_shape is not None and shape_lines:
                shapes[current_shape] = shape_lines
                shape_lines = []
            
            shape_id = int(line.split(':')[0].strip())
            current_shape = shape_id
            
            # Check if shape definition continues on same line
            shape_def = line.split(':', 1)[1].strip()
            if shape_def:
                shape_lines.append(shape_def)
            
            i += 1
            
            # Continue reading shape lines
            while i < n and lines[i].strip() and (lines[i].strip()[0] == '#' or lines[i].strip()[0] == '.'):
                shape_lines.append(lines[i].strip())
                i += 1
        else:
            # Not a shape line, break out of shape parsing
            break
    
    # Parse regions
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
            
        if 'x' in line and ':' in line:
            parts = line.split(':')
            if len(parts) < 2:
                i += 1
                continue
                
            size_part = parts[0].strip()
            counts_part = parts[1].strip()
            
            # Parse size
            if 'x' in size_part:
                try:
                    width, height = map(int, size_part.split('x'))
                except ValueError:
                    i += 1
                    continue
                
                # Parse counts
                try:
                    counts = list(map(int, counts_part.split()))
                    regions.append((width, height, counts))
                except ValueError:
                    i += 1
                    continue
        i += 1
    
    # Don't forget the last shape
    if current_shape is not None and shape_lines:
        shapes[current_shape] = shape_lines
    
    return shapes, regions


def rotate_shape(shape):
    """Rotate shape 90 degrees clockwise."""
    rows = len(shape)
    cols = len(shape[0])
    rotated = []
    for c in range(cols):
        new_row = []
        for r in range(rows-1, -1, -1):
            new_row.append(shape[r][c])
        rotated.append(''.join(new_row))
    return rotated


def flip_shape(shape):
    """Flip shape horizontally."""
    return [row[::-1] for row in shape]


def get_all_orientations(shape_grid):
    """Get all 8 orientations (rotations and flips) of a shape."""
    orientations = []
    current = shape_grid
    
    for _ in range(4):
        orientations.append(current)
        orientations.append(flip_shape(current))
        current = rotate_shape(current)
    
    # Remove duplicates
    unique_orientations = []
    seen = set()
    for orient in orientations:
        key = tuple(orient)
        if key not in seen:
            seen.add(key)
            unique_orientations.append(orient)
    
    return unique_orientations


def get_shape_cells(shape_grid):
    """Get list of (r, c) coordinates for '#' cells relative to top-left."""
    cells = []
    for r, row in enumerate(shape_grid):
        for c, ch in enumerate(row):
            if ch == '#':
                cells.append((r, c))
    return cells


def solve_exact_cover(shapes_data, width, height, counts):
    """Solve using exact cover algorithm (simplified)."""
    # This is a specialized solver for this specific problem
    
    # Precompute all possible placements
    placements_by_shape = []
    
    for shape_id, (cells_list, _) in enumerate(shapes_data):
        if counts[shape_id] == 0:
            placements_by_shape.append([])
            continue
            
        placements = []
        for cells in cells_list:
            # Get bounds
            min_r = min(r for r, _ in cells)
            max_r = max(r for r, _ in cells)
            min_c = min(c for _, c in cells)
            max_c = max(c for _, c in cells)
            shape_h = max_r - min_r + 1
            shape_w = max_c - min_c + 1
            
            # Normalize cells
            normalized = [(r - min_r, c - min_c) for r, c in cells]
            
            # Generate all positions
            for r in range(height - shape_h + 1):
                for c in range(width - shape_w + 1):
                    placed_cells = [(r + dr, c + dc) for dr, dc in normalized]
                    placements.append(placed_cells)
        
        placements_by_shape.append(placements)
    
    # Use backtracking with intelligent ordering
    grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Order shapes by fewest placement options first
    shape_order = []
    for shape_id, count in enumerate(counts):
        if count > 0:
            placements = placements_by_shape[shape_id]
            if not placements:
                return False  # Shape can't be placed at all
            shape_order.append((shape_id, len(placements)))
    
    shape_order.sort(key=lambda x: x[1])
    shape_order = [shape_id for shape_id, _ in shape_order]
    
    def backtrack(idx, remaining_counts):
        if idx >= len(shape_order):
            return True
            
        shape_id = shape_order[idx]
        
        if remaining_counts[shape_id] == 0:
            return backtrack(idx + 1, remaining_counts)
        
        # Try placements for this shape
        for cells in placements_by_shape[shape_id]:
            # Check if placement is valid
            valid = True
            for r, c in cells:
                if grid[r][c] != 0:
                    valid = False
                    break
            
            if valid:
                # Place shape
                for r, c in cells:
                    grid[r][c] = shape_id + 1
                
                new_counts = remaining_counts.copy()
                new_counts[shape_id] -= 1
                
                next_idx = idx
                if new_counts[shape_id] == 0:
                    next_idx = idx + 1
                
                if backtrack(next_idx, new_counts):
                    return True
                
                # Remove shape
                for r, c in cells:
                    grid[r][c] = 0
        
        return False
    
    return backtrack(0, counts.copy())


def part1(content):
    """Solution for Part 1: Count regions that can fit all presents."""
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Counting regions that can fit all presents...")
    
    shapes, regions = parse_input(content)
    
    print(f"{Fore.YELLOW}Found {len(shapes)} unique shapes")
    print(f"{Fore.YELLOW}Found {len(regions)} regions to check")
    
    if not shapes:
        print(f"{Fore.RED}No shapes found in input!")
        elapsed = time.time() - start_time
        return {
            "value": 0,
            "execution_time": elapsed,
            "num_shapes": 0,
            "num_regions": len(regions),
            "region_results": []
        }
    
    # Pre-process shapes with all orientations
    max_shape_id = max(shapes.keys())
    shapes_data = []
    
    for shape_id in range(max_shape_id + 1):
        if shape_id in shapes:
            shape_grid = shapes[shape_id]
            orientations = get_all_orientations(shape_grid)
            
            # Convert to cell lists
            cell_orientations = []
            for orient in orientations:
                cells = get_shape_cells(orient)
                cell_orientations.append(cells)
            
            # Get shape size
            cells = cell_orientations[0]
            size = len(cells)
            shapes_data.append((cell_orientations, size))
        else:
            shapes_data.append(([], 0))
    
    # Check each region
    feasible_count = 0
    region_results = []
    
    total_regions = len(regions)
    
    for i, (width, height, counts) in enumerate(regions):
        print(f"{Fore.CYAN}Checking region {i+1}/{total_regions}: {width}x{height} with counts {counts}")
        
        # Extend counts list if needed
        if len(counts) <= max_shape_id:
            counts = counts + [0] * (max_shape_id - len(counts) + 1)
        
        start_check = time.time()
        
        # First do quick checks
        # 1. Area check
        total_area = width * height
        needed_area = 0
        for shape_id, count in enumerate(counts):
            if count > 0 and shape_id < len(shapes_data):
                needed_area += shapes_data[shape_id][1] * count
        
        if needed_area > total_area:
            print(f"{Fore.RED}  ✗ Area too small ({needed_area} > {total_area})")
            region_results.append(False)
            continue
        
        # 2. Try to solve
        fits = solve_exact_cover(shapes_data, width, height, counts)
        
        check_time = time.time() - start_check
        
        if fits:
            print(f"{Fore.GREEN}  ✓ Region fits ({check_time:.2f}s)")
            feasible_count += 1
            region_results.append(True)
        else:
            print(f"{Fore.RED}  ✗ Region does not fit ({check_time:.2f}s)")
            region_results.append(False)
        
        # Progress update for large inputs
        if total_regions > 10 and (i + 1) % 10 == 0:
            elapsed_total = time.time() - start_time
            est_total = elapsed_total * total_regions / (i + 1)
            remaining = est_total - elapsed_total
            print(f"{Fore.MAGENTA}  Progress: {i+1}/{total_regions} ({elapsed_total:.1f}s elapsed, ~{remaining:.1f}s remaining)")
    
    elapsed = time.time() - start_time
    
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Part 1 Summary:")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Regions that fit: {feasible_count} out of {len(regions)}")
    print(f"{Fore.CYAN}Total time: {elapsed:.3f}s")
    
    if elapsed > 0 and len(regions) > 0:
        print(f"{Fore.CYAN}Average time per region: {elapsed/len(regions):.3f}s")
    
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": feasible_count,
        "execution_time": elapsed,
        "num_shapes": len(shapes),
        "num_regions": len(regions),
        "region_results": region_results
    }


def part2(content):
    """Solution for Part 2 (if applicable)."""
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Not applicable for this puzzle")
    
    elapsed = time.time() - start_time
    
    return {
        "value": 'N/A',
        "execution_time": elapsed,
        "status": TEST_STATUS["NOT_APPLICABLE"]
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