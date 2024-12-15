'''
--- Day 15: Warehouse Woes ---
You appear back inside your own mini submarine! Each Historian drives their mini submarine in a different direction; maybe the Chief has his own submarine down here somewhere as well?

You look up to see a vast school of lanternfish swimming past you. On closer inspection, they seem quite anxious, so you drive your mini submarine over to see if you can help.

Because lanternfish populations grow rapidly, they need a lot of food, and that food needs to be stored somewhere. That's why these lanternfish have built elaborate warehouse complexes operated by robots!

These lanternfish seem so anxious because they have lost control of the robot that operates one of their most important warehouses! It is currently running amok, pushing around boxes in the warehouse with no regard for lanternfish logistics or lanternfish inventory management strategies.

Right now, none of the lanternfish are brave enough to swim up to an unpredictable robot so they could shut it off. However, if you could anticipate the robot's movements, maybe they could find a safe option.

The lanternfish already have a map of the warehouse and a list of movements the robot will attempt to make (your puzzle input). The problem is that the movements will sometimes fail as boxes are shifted around, making the actual movements of the robot difficult to predict.

For example:

##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
As the robot (@) attempts to move, if there are any boxes (O) in the way, the robot will also attempt to push those boxes. However, if this action would cause the robot or a box to move into a wall (#), nothing moves instead, including the robot. The initial positions of these are shown on the map at the top of the document the lanternfish gave you.

The rest of the document describes the moves (^ for up, v for down, < for left, > for right) that the robot will attempt to make, in order. (The moves form a single giant sequence; they are broken into multiple lines just to make copy-pasting easier. Newlines within the move sequence should be ignored.)

Here is a smaller example to get started:

########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
Were the robot to attempt the given sequence of moves, it would push around the boxes as follows:

Initial state:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move <:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
The larger example has many more moves; after the robot has finished those moves, the warehouse would look like this:

##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########
The lanternfish use their own custom Goods Positioning System (GPS for short) to track the locations of the boxes. The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus its distance from the left edge of the map. (This process does not stop at wall tiles; measure all the way to the edges of the map.)

So, the box shown below has a distance of 1 from the top edge of the map and 4 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 4 = 104.

#######
#...O..
#......
The lanternfish would like to know the sum of all boxes' GPS coordinates after the robot finishes moving. In the larger example, the sum of all boxes' GPS coordinates is 10092. In the smaller example, the sum is 2028.

Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving, what is the sum of all boxes' GPS coordinates?

--- Part Two ---
The lanternfish use your information to find a safe moment to swim in and turn off the malfunctioning robot! Just as they start preparing a festival in your honor, reports start coming in that a second warehouse's robot is also malfunctioning.

This warehouse's layout is surprisingly similar to the one you just helped. There is one key difference: everything except the robot is twice as wide! The robot's list of movements doesn't change.

To get the wider warehouse's map, start with your original map and, for each tile, make the following changes:

If the tile is #, the new map contains ## instead.
If the tile is O, the new map contains [] instead.
If the tile is ., the new map contains .. instead.
If the tile is @, the new map contains @. instead.
This will produce a new warehouse map which is twice as wide and with wide boxes that are represented by []. (The robot does not change size.)

The larger example from before would now look like this:

####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
Because boxes are now twice as wide but the robot is still the same size and speed, boxes can be aligned such that they directly push two other boxes at once. For example, consider this situation:

#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
After appropriately resizing this map, the robot would push around these boxes as follows:

Initial state:
##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############

Move <:
##############
##......##..##
##..........##
##...[][]@..##
##....[]....##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[].@..##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.......@..##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##......@...##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.....@....##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##....@.....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##...@......##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##...@[]....##
##..........##
##..........##
##############

Move ^:
##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############
This warehouse also uses GPS to locate the boxes. For these larger boxes, distances are measured from the edge of the map to the closest edge of the box in question. So, the box shown below has a distance of 1 from the top edge of the map and 5 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 5 = 105.

##########
##...[]...
##........
In the scaled-up version of the larger example from above, after the robot has finished all of its moves, the warehouse would look like this:

####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################
The sum of these boxes' GPS coordinates is 9021.

Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of all boxes' final GPS coordinates?

'''

#!/usr/bin/python3

import os
from colorama import init, Fore
from tqdm import tqdm
import inspect
import time
from copy import deepcopy

init(autoreset=True)

CURRENT_FILEPATH = ""

def print_processing_header(filename, function_name):
    """Prints a formatted header for the current processing operation"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Function: {Fore.YELLOW}{function_name}")
    print(f"{Fore.CYAN}{'='*80}\n")

def parse_input(content):
    """Parse input content to get grid and movements"""
    parts = content.split('\n\n')
    map_str = parts[0].strip()
    moves_str = parts[1].strip()
    grid = [list(line) for line in map_str.splitlines() if '#' in line]
    moves = [char for char in moves_str if char in '^v<>']
    return grid, moves

def find_robot(grid):
    """Find robot coordinates in grid"""
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == '@':
                return i, j
    return None

def print_state(grid, step=""):
    """Print the current state of the grid"""
    if step:
        print(f"\nStep {step.upper()}:")
    for row in grid:
        print(''.join(row))
    print()

def grid_rotate(grid):
    """Rotate the grid 90 degrees clockwise"""
    return [list(row) for row in zip(*grid[::-1])]

def grid_rotation_wrapper(func):
    """Decorator to handle grid rotations for different directions"""
    def wrapper(grid, dirr):
        rotations = {
            '^': 3,
            'v': 1,
            '>': 2,
            '<': 0
        }
        
        # Copy grid to avoid modifying original
        working_grid = deepcopy(grid)
        
        # Rotate to standard orientation
        for _ in range(rotations[dirr]):
            working_grid = grid_rotate(working_grid)
            
        # Apply movement
        result = func(working_grid)
        
        # Rotate back
        for _ in range((4 - rotations[dirr]) % 4):
            result = grid_rotate(result)
            
        return result
    return wrapper

def scale_grid(grid):
    """Convert the original grid to one with double width"""
    scaled = []
    for row in grid:
        new_row = []
        for char in row:
            if char == '#':
                new_row.extend(['#', '#'])
            elif char == 'O':
                new_row.extend(['[', ']'])
            elif char == '.':
                new_row.extend(['.', '.'])
            elif char == '@':
                new_row.extend(['@', '.'])
        scaled.append(new_row)
    return scaled

@grid_rotation_wrapper
def move_box_part1(grid):
    """Move boxes in part 1 (single O boxes)"""
    r, c = find_robot(grid)
    if not r or c <= 0:
        return grid
        
    # Find sequence of boxes to move
    boxes = []
    curr_c = c - 1
    while curr_c >= 0 and grid[r][curr_c] == 'O':
        boxes.append(curr_c)
        curr_c -= 1
        
    if boxes and curr_c >= 0 and grid[r][curr_c] == '.':
        # Move boxes one position to the left
        grid[r][curr_c] = 'O'
        for box_c in boxes[:-1]:
            grid[r][box_c-1] = 'O'
            grid[r][box_c] = '.'
        # Move robot
        grid[r][c-1] = '@'
        grid[r][c] = '.'
        
    return grid

@grid_rotation_wrapper
def move_box_part2(grid):
    """Move boxes in part 2 (wide [] boxes)"""
    robot = find_robot(grid)
    if not robot:
        return grid
        
    r, c = robot
    
    def get_box_pair(pr, pc):
        """Get complete box pair from any part"""
        if not (0 <= pr < len(grid) and 0 <= pc < len(grid[0])-1):
            return set()
            
        if grid[pr][pc] == '[' and grid[pr][pc+1] == ']':
            return {(pr, pc, '['), (pr, pc+1, ']')}
        return set()

    # Find connected boxes
    seen = set()
    to_check = get_box_pair(r, c-1)
    boxes = set()
    
    while to_check:
        current = to_check.pop()
        if current in seen:
            continue
            
        seen.add(current)
        r, c, char = current
        
        # Check if we can move left
        if c > 0 and grid[r][c-1] == '#':
            return grid
            
        # Check for connected boxes
        if char == '[':
            next_boxes = get_box_pair(r, c+2)
        else:
            next_boxes = get_box_pair(r, c-2)
            
        to_check.update(next_boxes - seen)
        boxes.update(next_boxes)
    
    if boxes:
        # Clear old positions
        for r, c, _ in seen:
            grid[r][c] = '.'
            
        # Set new positions
        sorted_boxes = sorted(seen, key=lambda x: (x[0], x[1]))
        for r, c, char in sorted_boxes:
            grid[r][c-1] = char
            
        # Move robot
        r, c = robot
        grid[r][c] = '.'
        grid[r][c-1] = '@'
    
    return grid

def try_move_part1(grid, pos, move):
    """Try to move robot and boxes in part 1"""
    r, c = pos
    dr, dc = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }[move]
    
    new_r, new_c = r + dr, c + dc
    
    if not (0 <= new_r < len(grid) and 0 <= new_c < len(grid[0])):
        return grid, pos
    
    if grid[new_r][new_c] == '#':
        return grid, pos
        
    if grid[new_r][new_c] == '.':
        grid[r][c] = '.'
        grid[new_r][new_c] = '@'
        return grid, (new_r, new_c)
    
    if grid[new_r][new_c] == 'O':
        new_grid = move_box_part1(grid, move)
        return new_grid, find_robot(new_grid)
        
    return grid, pos

def try_move_part2(grid, pos, move):
    """Try to move robot and boxes in part 2"""
    r, c = pos
    dr, dc = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }[move]
    
    new_r, new_c = r + dr, c + dc
    
    if not (0 <= new_r < len(grid) and 0 <= new_c < len(grid[0])):
        return grid, pos
    
    if grid[new_r][new_c] == '#':
        return grid, pos
        
    if grid[new_r][new_c] == '.':
        grid[r][c] = '.'
        grid[new_r][new_c] = '@'
        return grid, (new_r, new_c)
    
    if grid[new_r][new_c] in '[]':
        new_grid = move_box_part2(grid, move)
        return new_grid, find_robot(new_grid)
        
    return grid, pos

def calculate_gps_coordinates(grid, box_char='O'):
    """Calculate sum of GPS coordinates"""
    return sum(row * 100 + col 
              for row, line in enumerate(grid)
              for col, char in enumerate(line) 
              if char == box_char)

def box_coords(content):
    """Part 1 solution"""
    start_time = time.time()
    
    filename = os.path.basename(CURRENT_FILEPATH)
    print_processing_header(filename, "Part 1 - Box Coords")
    
    grid, moves = parse_input(content)
    robot_pos = find_robot(grid)
    
    print_state(grid, "Initial")
    
    for move in tqdm(moves, desc="Processing moves"):
        grid, robot_pos = try_move_part1(grid, robot_pos, move)
    
    print_state(grid, "Final")
    
    result = calculate_gps_coordinates(grid, 'O')
    execution_time = time.time() - start_time
    return result, execution_time

def func_2(content):
    """Part 2 solution"""
    start_time = time.time()
    
    filename = os.path.basename(CURRENT_FILEPATH)
    print_processing_header(filename, "Part 2 - Wide Boxes")
    
    grid, moves = parse_input(content)
    scaled_grid = scale_grid(grid)
    robot_pos = find_robot(scaled_grid)
    
    print_state(scaled_grid, "Initial")
    
    for move in tqdm(moves, desc="Processing moves"):
        scaled_grid, robot_pos = try_move_part2(scaled_grid, robot_pos, move)
        print_state(scaled_grid, move)
    
    print_state(scaled_grid, "Final")
    
    result = calculate_gps_coordinates(scaled_grid, '[')
    execution_time = time.time() - start_time
    return result, execution_time

def process_file(filepath):
    """Process a single input file"""
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result, time1 = box_coords(content)
        part2_result, time2 = func_2(content)
        return part1_result, part2_result, time1, time2

def process_directory(input_dir="./input/"):
    """Process all files in directory"""
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
        if result[0]:
            part1, part2, time1, time2 = result[1], result[2], result[3], result[4]
            print(f"{Fore.BLUE}{file}:")
            print(f"  {Fore.YELLOW}Part 1 (GPS box coordinates):        {Fore.GREEN}{part1:<15} {Fore.CYAN}Time: {time1:.6f}s")
            print(f"  {Fore.YELLOW}Part 2 (GPS box coordinates scaled): {Fore.GREEN}{part2:<15} {Fore.CYAN}Time: {time2:.6f}s")
        else:
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")