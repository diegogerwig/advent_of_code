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

import sys
import os
from functools import wraps
from colorama import init, Fore
from tqdm import tqdm
import inspect
import time

init(autoreset=True)

CURRENT_FILEPATH = ""

# Define direction vectors
DIRS_ARROWS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}


def print_processing_header(filename, function_name):
    """
    Prints a formatted header for the current processing operation
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Function: {Fore.YELLOW}{function_name}")
    print(f"{Fore.CYAN}{'='*80}\n")


def print_grid(grid):
    """
    Prints the grid with colored output:
    - Obstacles (#) in red
    - Robot position (@) in green
    """
    for row in grid:
        for char in row:
            if char == '#':
                print(f"{Fore.RED}{char}", end='')
            elif char == '@':
                print(f"{Fore.GREEN}{char}", end='')
            else:
                print(f"{Fore.WHITE}{char}", end='')
        print()  # New line after each row
    print()  


def grid_find(grid, target):
    """
    Find the coordinates of a target character in the grid
    """
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == target:
                return i, j
    return None


def grid_rotate(grid):
    """
    Rotate the grid 90 degrees clockwise
    """
    return [list(row) for row in zip(*grid[::-1])]


def read_file(filename):
    """Read file and return maze and moves"""
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    maze = []
    moves = ""
    
    for line in lines:
        if '#' in line:  # If has walls, it's part of the maze
            maze.append(list(line))
        elif any(move in line for move in '<>^v'):  # If has moves
            moves += line
    
    return maze, moves


def find_robot(maze):
    """
    Find robot (@) position
    """
    for i, row in enumerate(maze):
        for j, char in enumerate(row):
            if char == '@':
                return i, j
    return None


def parse_data(lines):
    """
    Parse input into maze and moves
    """
    maze = []
    moves = []
    reading_maze = True
    
    for line in lines:
        if not line:
            reading_maze = False
            continue
        if reading_maze:
            maze.append(line)
        else:
            moves.append(line)
            
    return maze, ''.join(moves)


def move_box_single(maze: list[str], direction: str) -> list[str]:
    """
    Handle box movement for single width
    """
    rotations = {'^': 3, 'v': 1, '>': 2, '<': 0}
    
    # Rotate maze to position
    for _ in range(rotations[direction]):
        maze = grid_rotate(maze)
        
    # Move box logic
    r, c = grid_find(maze, '@')
    ll = 1
    while maze[r][c - ll] == 'O':
        ll += 1
    if maze[r][c - ll] == '.':
        maze[r][c - ll] = 'O'
        maze[r][c - 1] = '@'
        maze[r][c] = '.'
        
    # Rotate back
    for _ in range((4 - rotations[direction]) % 4):
        maze = grid_rotate(maze)
        
    return maze


def find_box_pair(maze: list[str], point: tuple[int, int, str], direction: str) -> set[tuple[int,int,str]]:
    """
    Find box pairs for double width
    """
    r, c = point[0], point[1]
    dr, dc = DIRS_ARROWS[direction]
    points = set([(r, c, maze[r][c])])

    if direction in '^v':
        if maze[r][c] == ']':
            points.add((r - dr, c - dc, maze[r - dr][c - dc]))
        else:
            points.add((r + dr, c + dc, maze[r + dr][c + dc]))
    else:
        if maze[r][c] == '[':
            points.add((r - dr, c - dc, maze[r - dr][c - dc]))
        else:
            points.add((r + dr, c + dc, maze[r + dr][c + dc]))
    return points


def move_box_double(maze: list[str], direction: str) -> list[str]:
    """
    Handle box movement for double width
    """
    rotations = {'^': 3, 'v': 1, '>': 2, '<': 0}
    
    # Rotate maze to position
    for _ in range(rotations[direction]):
        maze = grid_rotate(maze)

    robot = grid_find(maze, '@')
    seen = set()
    boxes = find_box_pair(maze, (robot[0], robot[1] - 1), direction)

    while boxes:
        poped = boxes.pop()
        if poped in seen:
            continue
        seen.add(poped)
        r, c, _ = poped
        if maze[r][c - 1] == '#':
            # Rotate back before returning
            for _ in range((4 - rotations[direction]) % 4):
                maze = grid_rotate(maze)
            return maze
        if maze[r][c - 1] != '.':
            boxes |= find_box_pair(maze, (r, c - 1), direction)

    for r, c, _ in seen:
        maze[r][c] = '.'
    for r, c, char in seen:
        maze[r][c-1] = char
    robot_r, robot_c = robot
    maze[robot_r][robot_c - 1] = '@'
    maze[robot_r][robot_c] = '.'

    # Rotate back
    for _ in range((4 - rotations[direction]) % 4):
        maze = grid_rotate(maze)
        
    return maze


def box_coords(lines: list[str]) -> tuple[int, float]:
    """
    Get GPS coordinates for all boxes
    """
    start_time = time.time()
    
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 1 - {current_func}")

    maze_data, moves = parse_data(lines)
    maze = [list(line) for line in maze_data]

    print_grid(maze)

    for char in moves:
        r, c = grid_find(maze, '@')
        dr, dc = DIRS_ARROWS[char]
        
        if maze[r + dr][c + dc] == '.':
            maze[r + dr][c + dc] = '@'
            maze[r][c] = '.'
        elif maze[r + dr][c + dc] == 'O':
            maze = move_box_single(maze, char)

    result = sum(row * 100 + col for row, line in enumerate(maze) 
                for col, char in enumerate(line) if char == 'O')
    
    print_grid(maze)
    
    execution_time = time.time() - start_time
    return result, execution_time


def box_coords_scaled(lines: list[str]) -> tuple[int, float]:
    """
    Get GPS coordinates for all boxes using a scaled grid
    """
    start_time = time.time()
    
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_processing_header(filename, f"Part 2 - {current_func}")

    maze_data, moves = parse_data(lines)
    char_map = {'@': '@.', '#': '##', 'O': '[]', '.': '..'}
    
    maze = []
    for line in maze_data:
        maze.append(list(''.join(char_map[char] for char in line)))

    print_grid(maze)

    for char in moves:
        r, c = grid_find(maze, '@')
        dr, dc = DIRS_ARROWS[char]

        if maze[r + dr][c + dc] == '.':
            maze[r][c] = '.'
            maze[r + dr][c + dc] = '@'
        elif maze[r + dr][c + dc] in '[]':
            maze = move_box_double(maze, char)

    result = sum(row * 100 + col for row, line in enumerate(maze) 
                for col, char in enumerate(line) if char == '[')
    
    print_grid(maze)

    execution_time = time.time() - start_time
    return result, execution_time


def process_file(filepath: str):
    """
    Process a single input file through both parts of the puzzle
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    
    try:
        with open(filepath, 'r') as file:
            content = [line.strip() for line in file.readlines()]
            part1_result, time1 = box_coords(content)
            part2_result, time2 = box_coords_scaled(content)
            return True, (part1_result, part2_result, time1, time2)
    except Exception as e:
        return False, str(e)


def process_directory(input_dir="./input/"):
    """
    Processes all files in the specified directory.
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    print(f"\n{Fore.CYAN}Processing files in directory: {Fore.YELLOW}{input_dir}")
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    results = {}
    
    for file in files:
        filepath = os.path.join(input_dir, file)
        success, result = process_file(filepath)  
        results[file] = (success, result)  
    
    return results


def main():
    try:
        input_dir = "./input/"
        results = process_directory(input_dir)
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}Final Results")
        print(f"{Fore.CYAN}{'='*80}\n")
        
        for file, (success, result) in results.items():
            if success:
                part1, part2, time1, time2 = result
                print(f"{Fore.BLUE}{file}:")
                print(f"  {Fore.YELLOW}Part 1 BOX COORDS:        {Fore.GREEN}{part1:<15} {Fore.CYAN}Time: {time1:.6f}s")
                print(f"  {Fore.YELLOW}Part 2 BOX COORDS SCALED: {Fore.GREEN}{part2:<15} {Fore.CYAN}Time: {time2:.6f}s")
            else:
                print(f"{Fore.BLUE}{file}: {Fore.RED}Error - {result}")
                
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()