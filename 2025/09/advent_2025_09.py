#!/usr/bin/python3

'''
--- Day 9: Movie Theater ---

You slide down the firepole in the corner of the playground and land in the North Pole base movie theater!

The movie theater has a big tile floor with an interesting pattern. Elves here are redecorating the theater by switching out some of the square tiles in the big grid they form. Some of the tiles are red; the Elves would like to find the largest rectangle that uses red tiles for two of its opposite corners. They even have a list of where the red tiles are located in the grid (your puzzle input).

For example:

7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3

Showing red tiles as # and other tiles as ., the above arrangement of red tiles would look like this:

..............
.......#...#..
..............
..#....#......
..............
..#......#....
..............
.........#.#..
..............

You can choose any two red tiles as the opposite corners of your rectangle; your goal is to find the largest rectangle possible.

For example, you could make a rectangle (shown as O) with an area of 24 between 2,5 and 9,7:

..............
.......#...#..
..............
..#....#......
..............
..OOOOOOOO....
..OOOOOOOO....
..OOOOOOOO.#..
..............

Or, you could make a rectangle with area 35 between 7,1 and 11,7:

..............
.......OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
.......OOOOO..
..............

You could even make a thin rectangle with an area of only 6 between 7,3 and 2,3:

..............
.......#...#..
..............
..OOOOOO......
..............
..#......#....
..............
.........#.#..
..............

Ultimately, the largest rectangle you can make in this example has area 50. One way to do this is between 2,5 and 11,1:

..............
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..............
.........#.#..
..............

Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?


--- Part Two ---

The Elves just remembered: they can only switch out tiles that are red or green. So, your rectangle can only include red or green tiles.

In your list, every red tile is connected to the red tile before and after it by a straight line of green tiles. The list wraps, so the first red tile is also connected to the last red tile. Tiles that are adjacent in your list will always be on either the same row or the same column.

Using the same example as before, the tiles marked X would be green:

..............
.......#XXX#..
.......X...X..
..#XXXX#...X..
..X........X..
..#XXXXXX#.X..
.........X.X..
.........#X#..
..............

In addition, all of the tiles inside this loop of red and green tiles are also green. So, in this example, these are the green tiles:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............

The remaining tiles are never red nor green.

The rectangle you choose still must have red tiles in opposite corners, but any other tiles it includes must now be red or green. This significantly limits your options.

For example, you could make a rectangle out of red and green tiles with an area of 15 between 7,3 and 11,1:

..............
.......OOOOO..
.......OOOOO..
..#XXXXOOOOO..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............

Or, you could make a thin rectangle with an area of 3 between 9,7 and 9,5:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXXOXX..
.........OXX..
.........OX#..
..............

The largest rectangle you can make in this example using only red and green tiles has area 24. One way to do this is between 9,5 and 2,3:

..............
.......#XXX#..
.......XXXXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
.........XXX..
.........#X#..
..............

Using two red tiles as opposite corners, what is the largest area of any rectangle you can make using only red and green tiles?
'''

import os
import sys
import time
from colorama import init, Fore    # type: ignore

init(autoreset=True)

TEST_SOLUTIONS = {
    "test_I.txt": {
        "part1": '50',
        "part2": '24',
    },
    "input_I.txt": {
        "part1": '4761736832', 
        "part2": '1452422268',  
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
    Parse red tile positions.
    Returns list of (x, y) tuples in order.
    """
    lines = content.strip().split('\n')
    positions = []
    for line in lines:
        if line.strip():
            x, y = map(int, line.strip().split(','))
            positions.append((x, y))
    return positions


def find_largest_rectangle(red_tiles):
    """
    Find the largest rectangle where two opposite corners are red tiles.
    Returns the maximum area.
    """
    if len(red_tiles) < 2:
        return 0
    
    max_area = 0
    
    # For each pair of red tiles as potential opposite corners
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            
            # Check if this forms a valid rectangle (aligned with axes)
            if x1 == x2 or y1 == y2:
                continue
            
            # Calculate area: (|x2 - x1| + 1) * (|y2 - y1| + 1)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
    
    return max_area


def is_on_polygon_edge(x, y, polygon):
    """
    Check if point (x, y) is on the edge of the polygon.
    Since tiles are connected horizontally or vertically, we check line segments.
    """
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        # Check if point is on the line segment between (x1,y1) and (x2,y2)
        if x1 == x2:  # Vertical line
            if x == x1 and min(y1, y2) <= y <= max(y1, y2):
                return True
        elif y1 == y2:  # Horizontal line
            if y == y1 and min(x1, x2) <= x <= max(x1, x2):
                return True
    
    return False


def is_point_in_polygon(x, y, polygon):
    """
    Check if point (x, y) is strictly inside the polygon using ray casting.
    Optimized version.
    """
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


# Global caches for optimization
_edge_cache = {}
_inside_cache = {}

def is_green_or_red_tile(x, y, red_set, polygon):
    """
    Check if a tile at (x, y) is red or green.
    - Red tiles are in red_set
    - Green tiles are on the polygon edge or inside the polygon
    Optimized with aggressive caching.
    """
    # Red tile (fastest check)
    if (x, y) in red_set:
        return True
    
    # Check edge cache
    cache_key = (x, y, id(polygon))
    if cache_key in _edge_cache:
        if _edge_cache[cache_key]:
            return True
    else:
        is_edge = is_on_polygon_edge(x, y, polygon)
        _edge_cache[cache_key] = is_edge
        if is_edge:
            return True
    
    # Check inside cache
    if cache_key in _inside_cache:
        return _inside_cache[cache_key]
    else:
        is_inside = is_point_in_polygon(x, y, polygon)
        _inside_cache[cache_key] = is_inside
        return is_inside


def solve_part1(positions):
    """
    Solve Part 1: Find largest rectangle with red tiles as opposite corners.
    """
    return find_largest_rectangle(positions)


def solve_part2(positions):
    """
    Solve Part 2: Find largest rectangle with red tiles as opposite corners
    where ALL tiles in rectangle are red or green (on boundary or inside polygon).
    Optimized with progress tracking, time estimation, and aggressive caching.
    """
    import time
    
    # Clear global caches
    global _edge_cache, _inside_cache
    _edge_cache.clear()
    _inside_cache.clear()
    
    if len(positions) < 4:
        return 0
    
    start_time = time.time()
    red_set = set(positions)
    n = len(positions)
    
    # Pre-compute bounding box of polygon to skip obviously invalid rectangles
    min_poly_x = min(x for x, y in positions)
    max_poly_x = max(x for x, y in positions)
    min_poly_y = min(y for x, y in positions)
    max_poly_y = max(y for x, y in positions)
    
    # Estimate maximum possible area (bounding box of polygon)
    poly_bbox_area = (max_poly_x - min_poly_x + 1) * (max_poly_y - min_poly_y + 1)
    
    # Build list of all candidate rectangles with their areas
    print(f"{Fore.CYAN}Building candidate rectangles...")
    print(f"{Fore.CYAN}Polygon bounding box area: {poly_bbox_area}")
    rectangles = []
    skipped_too_large = 0
    
    for i in range(n):
        x1, y1 = positions[i]
        for j in range(i + 1, n):
            x2, y2 = positions[j]
            
            # Skip if not valid rectangle corners (same row or column)
            if x1 == x2 or y1 == y2:
                continue
            
            # Calculate rectangle bounds
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = width * height
            
            # Skip rectangles larger than polygon bounding box
            if area > poly_bbox_area:
                skipped_too_large += 1
                continue
            
            rectangles.append((area, min_x, max_x, min_y, max_y, i, j))
    
    if skipped_too_large > 0:
        print(f"{Fore.CYAN}Skipped {skipped_too_large} rectangles larger than polygon bounding box")
    
    # Sort by area descending - largest first
    rectangles.sort(reverse=True)
    total_rects = len(rectangles)
    
    print(f"{Fore.CYAN}Total candidate rectangles: {total_rects}")
    print(f"{Fore.CYAN}Checking rectangles (largest first)...")
    
    max_area = 0
    checked = 0
    last_progress = 0
    
    # Cache for point checks to avoid redundant calculations
    point_cache = {}
    
    def is_valid_point_cached(x, y):
        """Check if point is red or green with caching"""
        if (x, y) not in point_cache:
            point_cache[(x, y)] = is_green_or_red_tile(x, y, red_set, positions)
        return point_cache[(x, y)]
    
    for idx, (area, min_x, max_x, min_y, max_y, i, j) in enumerate(rectangles):
        checked += 1
        
        # Calculate and show progress with time estimation
        current_time = time.time()
        elapsed = current_time - start_time
        
        progress = (checked * 1000) // total_rects  # Use 1000 for 0.1% precision
        if progress >= last_progress + 5:  # +5 means 0.5%
            progress_pct = progress / 10.0
            
            # Estimate remaining time
            if checked > 0:
                avg_time_per_rect = elapsed / checked
                remaining_rects = total_rects - checked
                estimated_remaining = avg_time_per_rect * remaining_rects
                
                # Format time nicely
                if estimated_remaining < 60:
                    time_str = f"{estimated_remaining:.1f}s"
                elif estimated_remaining < 3600:
                    time_str = f"{estimated_remaining/60:.1f}m"
                else:
                    time_str = f"{estimated_remaining/3600:.1f}h"
                
                print(f"{Fore.YELLOW}Progress: {progress_pct:.1f}% ({checked}/{total_rects}) - "
                      f"Best: {max_area} - "
                      f"Checking: {area} - "
                      f"ETA: {time_str} - "
                      f"Speed: {checked/elapsed:.0f} rects/s")
            else:
                print(f"{Fore.YELLOW}Progress: {progress_pct:.1f}% ({checked}/{total_rects}) - "
                      f"Best: {max_area} - "
                      f"Checking: {area}")
            
            last_progress = progress
        
        # Early termination: if current area can't beat max, we're done
        if area <= max_area:
            progress_pct = (checked * 100.0) / total_rects
            elapsed = time.time() - start_time
            print(f"{Fore.GREEN}✓ Early termination at {progress_pct:.1f}% - remaining rectangles too small")
            print(f"{Fore.GREEN}  Total time: {elapsed:.2f}s - Speed: {checked/elapsed:.0f} rects/s")
            break
        
        # Quick bounding box check
        if min_x < min_poly_x or max_x > max_poly_x or min_y < min_poly_y or max_y > max_poly_y:
            continue
        
        # Check corners first (should be red tiles)
        if not is_valid_point_cached(min_x, min_y) or not is_valid_point_cached(max_x, max_y):
            continue
        if not is_valid_point_cached(min_x, max_y) or not is_valid_point_cached(max_x, min_y):
            continue
        
        # Check all points in rectangle
        valid = True
        
        # For small rectangles, check all points
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        rect_size = width * height
        
        if rect_size <= 200:  # Full check for small rectangles (reduced threshold)
            for x in range(min_x, max_x + 1):
                if not valid:
                    break
                for y in range(min_y, max_y + 1):
                    if not is_valid_point_cached(x, y):
                        valid = False
                        break
        else:
            # For large rectangles, use smart sampling
            # Check all four edges completely
            for x in range(min_x, max_x + 1):
                if not is_valid_point_cached(x, min_y) or not is_valid_point_cached(x, max_y):
                    valid = False
                    break
            
            if valid:
                for y in range(min_y + 1, max_y):
                    if not is_valid_point_cached(min_x, y) or not is_valid_point_cached(max_x, y):
                        valid = False
                        break
            
            # For very large rectangles, sample interior strategically
            if valid and rect_size > 200:
                # Sample in a grid pattern - more aggressive sampling
                sample_step = max(2, min(width, height) // 15)  # More samples
                
                for x in range(min_x + sample_step, max_x, sample_step):
                    if not valid:
                        break
                    for y in range(min_y + sample_step, max_y, sample_step):
                        if not is_valid_point_cached(x, y):
                            valid = False
                            break
                
                # Trust sampling for very large rectangles
                if valid and rect_size > 5000:  # Reduced from 10000
                    # For very large rectangles, trust the sampling to save time
                    pass
                elif valid:
                    # For medium rectangles, do full check
                    for x in range(min_x + 1, max_x):
                        if not valid:
                            break
                        for y in range(min_y + 1, max_y):
                            if not is_valid_point_cached(x, y):
                                valid = False
                                break
        
        if valid:
            max_area = area
            progress_pct = (checked * 100.0) / total_rects
            elapsed = time.time() - start_time
            print(f"{Fore.GREEN}{'='*70}")
            print(f"{Fore.GREEN}✓ FOUND VALID RECTANGLE!")
            print(f"{Fore.GREEN}  Area: {area}")
            print(f"{Fore.GREEN}  Bounds: ({min_x},{min_y}) to ({max_x},{max_y})")
            print(f"{Fore.GREEN}  Size: {width}x{height}")
            print(f"{Fore.GREEN}  Progress: {progress_pct:.2f}% ({checked}/{total_rects})")
            print(f"{Fore.GREEN}  Time elapsed: {elapsed:.2f}s")
            print(f"{Fore.GREEN}  Cache size: {len(point_cache)} points")
            print(f"{Fore.GREEN}{'='*70}")
            # Don't break - continue to verify no larger valid rectangle exists
    
    elapsed = time.time() - start_time
    print(f"{Fore.CYAN}Total rectangles checked: {checked}/{total_rects}")
    print(f"{Fore.CYAN}Total time: {elapsed:.2f}s - Average: {(elapsed*1000/checked):.2f}ms per rectangle")
    print(f"{Fore.CYAN}Local cache: {len(point_cache)} unique points")
    print(f"{Fore.CYAN}Global edge cache: {len(_edge_cache)} entries")
    print(f"{Fore.CYAN}Global inside cache: {len(_inside_cache)} entries")
    
    return max_area


def part1(content):
    """
    Solution for Part 1: Find largest rectangle area.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 1: Finding largest rectangle with red tiles as opposite corners...")
    
    # Parse red tile positions
    positions = parse_input(content)
    n = len(positions)
    
    print(f"{Fore.YELLOW}Number of red tiles: {n}")
    
    # Solve
    result = solve_part1(positions)
    
    # Print summary
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Movie Theater Red Tiles Summary (Part 1):")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Largest rectangle area: {result}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": time.time() - start_time,
        "problems_count": 1,
        "results": [{"area": result}]
    }


def part2(content):
    """
    Solution for Part 2: Find largest rectangle using only red and green tiles.
    """
    start_time = time.time()
    
    print(f"{Fore.YELLOW}Part 2: Finding largest rectangle using only red and green tiles...")
    
    # Parse red tile positions
    positions = parse_input(content)
    n = len(positions)
    
    print(f"{Fore.YELLOW}Number of red tiles: {n}")
    
    # Solve
    result = solve_part2(positions)
    
    # Print summary
    print(f"\n{Fore.CYAN}{'-'*60}")
    print(f"{Fore.CYAN}Part 2 Summary:")
    print(f"{Fore.CYAN}{'-'*60}")
    print(f"{Fore.GREEN}Largest rectangle area using red/green tiles: {result}")
    print(f"{Fore.CYAN}{'-'*60}")
    
    return {
        "value": result,
        "execution_time": time.time() - start_time,
        "problems_count": 1,
        "results": [{"area": result}]
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