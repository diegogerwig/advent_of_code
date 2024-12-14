'''
--- Day 14: Restroom Redoubt ---
One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...
These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........
The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....
To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....
           
..... .....
...12 .....
.1... 1....
In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?

--- Part Two ---
During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
'''

#!/usr/bin/python3

import os
from colorama import init, Fore
from tqdm import tqdm
import inspect
import time

init(autoreset=True)

CURRENT_FILEPATH = ""


def print_processing_header(filename, function_name):
    """
    Prints a formatted header for the current processing operation
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Function: {Fore.YELLOW}{function_name}")
    print(f"{Fore.CYAN}{'='*80}\n")


def print_grid(robots, width, height, message="", hide_center=False):
    """
    Visualize the current state of the robot grid for debugging purposes.
    Uses colors and coordinate frame for better visualization.
    """
    print(f"\n{Fore.CYAN}=== Grid State {message} ===")
    print(f"{Fore.CYAN}Grid size: {Fore.YELLOW}{width}x{height}")
    print(f"{Fore.CYAN}Total robots: {Fore.YELLOW}{len(robots)}")
    
    # Create empty grid and count robots per position
    grid = [['.'] * width for _ in range(height)]
    robot_counts = {}
    
    # Get central lines
    mid_x = width // 2
    mid_y = height // 2
    
    # Fill grid with robot counts
    for pos, _ in robots:
        x, y = pos
        # Skip robots in central lines if hide_center is True
        if hide_center and (x == mid_x or y == mid_y):
            continue
        pos_key = (x, y)
        robot_counts[pos_key] = robot_counts.get(pos_key, 0) + 1
    
    # Fill grid with robot counts
    for (x, y), count in robot_counts.items():
        grid[y][x] = str(count) if count < 10 else '#'
    
    # Clear central lines if hide_center is True
    if hide_center:
        # Clear vertical central line
        for y in range(height):
            grid[y][mid_x] = ' '
        # Clear horizontal central line
        for x in range(width):
            grid[mid_y][x] = ' '

    # Calculate left margin based on maximum row number
    y_width = len(str(height - 1))
    margin = y_width + 2
    margin_str = " " * margin
    
    # Print top border
    print(f"{Fore.BLUE}{margin_str} ┌" + "─" * width + "┐")
    
    # Print column numbers (x coordinates)
    print(f"{Fore.BLUE}{margin_str} │{Fore.YELLOW}", end="")
    row1 = ""
    for x in range(width):
        tens = (x // 10) % 10
        row1 += str(tens)
    print(row1 + f"{Fore.BLUE}│")
    
    # Print ones digit of column numbers
    print(f"{Fore.BLUE}{margin_str} │{Fore.YELLOW}", end="")
    row2 = ""
    for x in range(width):
        ones = x % 10
        row2 += str(ones)
    print(row2 + f"{Fore.BLUE}│")
    
    # Print separator
    print(f"{Fore.BLUE}{margin_str} ├" + "─" * width + "┤")
    
    # Print grid with row numbers (y coordinates)
    for y in range(height):
        print(f"{Fore.BLUE}{y:>{margin}} │", end="")
        for x in range(width):
            cell = grid[y][x]
            if cell == ' ':  # Empty central lines
                print(" ", end="")
            elif cell == '.':
                print(f"{cell}", end="")
            else:
                print(f"{Fore.RED}{cell}{Fore.BLUE}", end="")
        print("│")
    
    # Print bottom border
    print(f"{Fore.BLUE}{margin_str} └" + "─" * width + "┘")
    
    # If hiding center, print robot counts per quadrant
    if hide_center:
        quadrants = [0] * 4
        for pos, _ in robots:
            x, y = pos
            if x == mid_x or y == mid_y:
                continue
            quadrant_idx = (0 if x < mid_x else 1) + (0 if y < mid_y else 2)
            quadrants[quadrant_idx] += 1
            
        print(f"\n{Fore.CYAN}Quadrant counts:")
        quadrant_names = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"]
        for i, name in enumerate(quadrant_names):
            print(f"{Fore.YELLOW}{name}: \t{Fore.RED}{quadrants[i]} robots")
        
        safety_factor = 1
        for count in quadrants:
            safety_factor *= count
        print(f"\n{Fore.CYAN}Safety Factor: {Fore.YELLOW}{safety_factor}")
    

def safety_factor(content):
    """
    Calculate safety factor by tracking robot positions over 100 seconds and 
    multiplying the number of robots in each quadrant.
    """
    start_time = time.time()
    
    # Get function name and file for header
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 1 - {current_func}")

    # Parse input to get initial positions and velocities
    robots = []
    for line in content.strip().split('\n'):
        if not line.startswith('p='):
            continue
        pos, vel = line.split()
        px, py = map(int, pos[2:].split(','))
        vx, vy = map(int, vel[2:].split(','))
        robots.append([(px, py), (vx, vy)])
    
    # Set grid dimensions based on input file
    if filename.startswith('.test_'):
        width, height = 11, 7
    else:
        width, height = 101, 103
    

    print_grid(robots, width, height, "AT START")

    # Simulate 100 seconds
    for _ in range(100):
        for i in range(len(robots)):
            pos, vel = robots[i]
            # Update position
            new_x = (pos[0] + vel[0]) % width  # Wrap around if at edge
            new_y = (pos[1] + vel[1]) % height  # Wrap around if at edge
            robots[i] = [(new_x, new_y), vel]

    print_grid(robots, width, height, "AFTER 100 SECONDS")
    print_grid(robots, width, height, "after 100 seconds (excluding central lines)", hide_center=True)
    
    # Count robots in each quadrant
    mid_x = width // 2
    mid_y = height // 2
    quadrants = [0, 0, 0, 0]   # [top-left, top-right, bottom-left, bottom-right]
    
    for pos, _ in robots:
        x, y = pos
        # Skip robots exactly on the middle lines
        if x == mid_x or y == mid_y:
            continue
        
        # Determine quadrant
        if x < mid_x:
            if y < mid_y:
                quadrants[0] += 1  # top-left
            else:
                quadrants[2] += 1  # bottom-left
        else:
            if y < mid_y:
                quadrants[1] += 1  # top-right
            else:
                quadrants[3] += 1  # bottom-right
    
    # Calculate safety factor (multiply all quadrant counts)
    result = 1
    for count in quadrants:
        result *= count
    
    execution_time = time.time() - start_time
    return result, execution_time


def find_easter_egg(grid, width, height):
    """
    Find a potential pattern by analyzing:
    1. Rectangular frame
    2. Connected hierarchical/triangular groups
    """
    # Find all robot positions
    robot_positions = set()
    for y in range(height):
        for x in range(width):
            if grid[y][x] != '.':
                robot_positions.add((x, y))
    
    if not robot_positions:
        return False, set()
    
    def is_rectangular_frame(positions):
        """
        Detect a rectangular frame based on bounding box perimeter
        """
        # Skip if not enough positions
        if len(positions) < 20:
            return False
        
        # Get bounding box dimensions
        min_x = min(x for x, _ in positions)
        max_x = max(x for x, _ in positions)
        min_y = min(y for _, y in positions)
        max_y = max(y for _, y in positions)
        
        # Calculate bounding box perimeter
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        perimeter = 2 * (width + height)
        
        print(f"\n\n{Fore.GREEN}Frame & Pattern Detection:")
        print(f"  Frame: x({min_x},{max_x}) y({min_y},{max_y})")
        print(f"    Width: {width}")
        print(f"    Height: {height}")
        print(f"    Perimeter: {perimeter}")
        print(f"  Pattern Possitions: {len(positions)}")
        
        return perimeter > 100
        
    def get_connected_groups():
        """
        Find all connected groups of robots using breadth-first search
        """
        visited = set()
        groups = []
        
        def bfs(start): # Breadth-first search
            group = set()
            queue = [start]
            visited.add(start)
            
            while queue:
                x, y = queue.pop(0)
                group.add((x, y))
                
                # Check 4-directional neighbors
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < width and 0 <= ny < height and 
                        (nx, ny) in robot_positions and 
                        (nx, ny) not in visited):
                        queue.append((nx, ny))
                        visited.add((nx, ny))
            
            return group
        
        for x, y in robot_positions:
            if (x, y) not in visited:
                groups.append(bfs((x, y)))
        
        return groups
    
    def find_rectangular_pattern():
        """
        Detect a rectangular frame pattern
        """
        groups = get_connected_groups()
        largest_group = max(groups, key=len) if groups else set()
        
        if largest_group:
            min_x = min(x for x, _ in largest_group)
            max_x = max(x for x, _ in largest_group)
            min_y = min(y for _, y in largest_group)
            max_y = max(y for _, y in largest_group)
            
        # Extract rectangular frame positions        
        if len(largest_group) > 20 and is_rectangular_frame(largest_group):
            return True, largest_group
        
        return False, set()
    
    def find_hierarchical_pattern():
        """
        Detect a connected hierarchical/triangular pattern
        Finds a group of connected robots without a specific shape
        Only detects if the group is larger than 100 positions
        """
        groups = get_connected_groups()
        
        if not groups:
            return False, set()
        
        pattern = max(groups, key=len)
        
        if len(pattern) > 100:
            return True, pattern
        
        return False, set()
    
    # Try rectangular pattern first
    rectangular_result = find_rectangular_pattern()
    if rectangular_result[0]:
        return rectangular_result
    
    # If no rectangular pattern, try hierarchical pattern
    hierarchical_result = find_hierarchical_pattern()
    if hierarchical_result[0]:
        return hierarchical_result
    
    return False, set()


def xmas_tree(content):
    """
    Find the minimum number of seconds needed for robots to form a perfect Christmas tree pattern.
    """
    start_time = time.time()
    
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 2 - {current_func}")

    # Parse input to get initial positions and velocities
    robots = []
    for line in content.strip().split('\n'):
        if not line.startswith('p='):
            continue
        pos, vel = line.split()
        px, py = map(int, pos[2:].split(','))
        vx, vy = map(int, vel[2:].split(','))
        robots.append([(px, py), (vx, vy)])
    
    # Set grid dimensions based on input file
    if filename.startswith('.test_'):
        width, height = 11, 7
    else:
        width, height = 101, 103
    
    # Simulate until we find a Christmas tree pattern or reach max steps
    max_steps = 10000  # I get this value from failed submited solution
    try:
        for second in range(max_steps):
            # Create grid of current positions
            grid = [['.'] * width for _ in range(height)]
            for pos, _ in robots:
                x, y = pos
                grid[y][x] = '*'
            
            # Check for Christmas tree pattern
            pattern_found, pattern_robots = find_easter_egg(grid, width, height)
            if pattern_found:
                print(f"\n{Fore.GREEN}Perfect Christmas tree pattern found after {second} seconds!")
                                
                print_grid(robots, width, height, f"Christmas Tree Pattern at {second} seconds")
                execution_time = time.time() - start_time
                return second, execution_time
            
            # Move robots
            for i in range(len(robots)):
                pos, vel = robots[i]
                new_x = (pos[0] + vel[0]) % width
                new_y = (pos[1] + vel[1]) % height
                robots[i] = [(new_x, new_y), vel]
            
            # Periodic status update
            if second % 100 == 0:
                print(f"\r{Fore.RED}No pattern found after {second} seconds{' ' * 20}", end='', flush=True)
        
        # If we exit the loop without finding a pattern
        print(f"\n{Fore.RED}No Christmas tree pattern found within {max_steps} seconds.")
        execution_time = time.time() - start_time
        return -1, execution_time
    
    except KeyboardInterrupt:
        print("\nSearch interrupted by user.")
        execution_time = time.time() - start_time
        return -1, execution_time


def process_file(filepath):
    """
    Process a single input file through both parts of the puzzle
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result, time1 = safety_factor(content)
        part2_result, time2 = xmas_tree(content)
        return part1_result, part2_result, time1, time2


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
            part1_result, part2_result, time1, time2 = process_file(filepath)
            results[file] = (True, part1_result, part2_result, time1, time2)
        except Exception as e:
            results[file] = (False, str(e))
    
    return results


if __name__ == "__main__":
    input_dir = "./input/"
    results = process_directory(input_dir)

    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    for file, result in results.items():
        if result[0]:  # Successfully processed
            part1, part2, time1, time2 = result[1], result[2], result[3], result[4]
            print(f"{Fore.BLUE}{file}:")
            print(f"  {Fore.YELLOW}Part 1 (Safety Factor):   {Fore.GREEN}{part1:<15} {Fore.CYAN}Time: {time1:.6f}s")
            print(f"  {Fore.YELLOW}Part 2 (Christmas Tree):  {Fore.GREEN}{part2:<15} {Fore.CYAN}Time: {time2:.6f}s")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")