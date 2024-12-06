#!/usr/bin/python3

'''
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
'''

import os
from colorama import init, Fore

init(autoreset=True)


def parse_map(content):
    """
    Parses the input map and returns the grid, guard position and initial direction.
    Initial_direction: Integer representing initial direction (0:N, 1:E, 2:S, 3:W)
    """
    # Parse the input map
    grid = []
    for line in content.splitlines():
        if line and not line.isspace():
            grid.append(list(line))
    
    # Find guard's initial position and direction
    guard_pos = None
    direction = None

    # Direction mapping
    dir_idx = {"^": 0, ">": 1, "v": 2, "<": 3}
    
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in "^>v<":
                guard_pos = (r, c)
                direction = dir_idx[cell]
                break
        if guard_pos:
            break
            
    if not guard_pos:
        raise ValueError("Guard not found in the map")
        
    return grid, guard_pos, direction


def guard_positions(content):
    """
    Simulates guard patrol and counts distinct positions visited before leaving the mapped area.
    """
    # Parse map and get initial state
    grid, guard_pos, direction = parse_map(content)
    rows = len(grid)
    cols = len(grid[0])

    # Directions: (North, East, South, West) as coordinate changes
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  

    # Initialize tracking variables
    visited = set([guard_pos])
    r, c = guard_pos
    max_steps = rows * cols * 2
    steps = 0
    states = set()

    while steps < max_steps:
        # Current state is position + direction
        current_state = (r, c, direction)
        if current_state in states:
            print(f"Loop detected at position ({r}, {c}) facing direction {direction}")
            return len(visited)
            
        states.add(current_state)
        
        dr, dc = directions[direction]
        next_r, next_c = r + dr, c + dc

        # First check if we're about to leave the map
        if next_r < 0 or next_r >= rows or next_c < 0 or next_c >= cols:
            return len(visited)  # Guard is about to leave the map

        # Check if next position is blocked
        if grid[next_r][next_c] == '#':
            # Turn right
            direction = (direction + 1) % 4
        else:
            # Move forward
            r, c = next_r, next_c
            visited.add((r, c))

        steps += 1
        
    print(f"Reached maximum steps ({max_steps})")
    return len(visited)


def simulate_guard_movement(grid, start_pos, start_direction, max_steps=None):
    """
    Simulates guard movement and returns whether it loops and visited positions.
    """
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W
    
    if max_steps is None:
        max_steps = rows * cols * 2

    r, c = start_pos
    direction = start_direction
    states = set([(r, c, direction)])
    steps = 0
    
    while steps < max_steps:
        dr, dc = directions[direction]
        next_r, next_c = r + dr, c + dc
        
        # Check if guard would leave the map
        if next_r < 0 or next_r >= rows or next_c < 0 or next_c >= cols:
            return False
            
        # Check if next position is blocked
        if grid[next_r][next_c] == '#' or grid[next_r][next_c] == 'O':
            direction = (direction + 1) % 4
        else:
            r, c = next_r, next_c
            if (r, c, direction) in states:
                return True
            states.add((r, c, direction))
            
        steps += 1
    
    return True  # If we reach max_steps, assume it's a loop


def obstacle_positions(content):
    """
    Find number of positions where placing an obstacle creates a patrol loop.
    """
    # Get initial map state
    grid, guard_pos, start_direction = parse_map(content)
    rows, cols = len(grid), len(grid[0])
    
    # Store the initial grid state
    original_grid = []
    for row in grid:
        original_grid.append(row[:])

    possible_positions = 0
    total_positions = rows * cols
    positions_checked = 0
    loops_found = []

    print(f"\nSearching for obstacle positions in a {rows}x{cols} grid")
    print("=" * 62)
    
    # Try placing an obstacle at each position
    for r in range(rows):
        for c in range(cols):
            positions_checked += 1
            progress = (positions_checked / total_positions) * 100
            
            # Update progress bar
            bar_length = 50
            filled_length = int(bar_length * positions_checked // total_positions)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            print(f'\rProgress: [{bar}] {progress:.1f}% ({positions_checked}/{total_positions}) - Loops found: {possible_positions}', end='')
            
            # Skip if position:
            # - is guard's starting position
            # - already has an obstacle
            # - already has the guard
            if ((r, c) == guard_pos or 
                original_grid[r][c] == '#' or 
                original_grid[r][c] in '^>v<'):
                continue
                
            # Reset grid to original state
            grid = []
            for row in original_grid:
                grid.append(row[:])
            
            # Place new obstacle
            grid[r][c] = 'O'
            
            # Simulate guard movement with new obstacle
            creates_loop = simulate_guard_movement(grid, guard_pos, start_direction)
            
            # If it creates a loop, count this position and store it
            if creates_loop:
                possible_positions += 1
                loops_found.append((r, c))
    
    print("\n" + "=" * 62)
    print(f"Search complete!")
    print(f"Total loops found: {possible_positions}")
    print("Loop positions:", ', '.join([f"({r}, {c})" for r, c in loops_found]))
    
    return possible_positions


def process_file(filepath):
    """
    Processes a single file and returns the results.
    - Calculate the gaurd patrol movements
    - Calculate the number of obstacle positions that create a loop
    """
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = guard_positions(content)
        part2_result = obstacle_positions(content)
        return part1_result, part2_result


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
            part1_result, part2_result = process_file(filepath)
            results[file] = (True, part1_result, part2_result)
        except Exception as e:
            results[file] = (False, str(e))
    
    return results


if __name__ == "__main__":
    input_dir = "./input/"
    results = process_directory(input_dir)
    
    for file, result in results.items():
        if result[0]:  # Successfully processed
            part1, part2 = result[1], result[2]
            print(f"{Fore.BLUE}{file}:")
            print(f"  {Fore.YELLOW}Part 1 (Guard positions): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Obstacle positions): {Fore.GREEN}{part2}")
        else:  # Error during processing
            print(f"{Fore.CYAN}{file}: {Fore.RED}Error - {result[1]}")
