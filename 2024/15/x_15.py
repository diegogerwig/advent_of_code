import argparse
import sys
import os
from functools import wraps

# Define direction vectors that were likely in the lib module
DIRS_ARROWS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

def grid_find(grid, target):
    """Find the coordinates of a target character in the grid"""
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == target:
                return i, j
    return None

def grid_rotate(grid):
    """Rotate the grid 90 degrees clockwise"""
    return [list(row) for row in zip(*grid[::-1])]

def read_file(file: str) -> list[str]:
    """Read and parse input file"""
    if not os.path.exists(file):
        print(f"File {file} not found")
        exit(1)
    with open(file) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

def content() -> tuple[list[str], list[str]]:
    """Read both input and test files"""
    input_file = './input/input_I.txt'
    test_file = './input/.test_I.txt'
    return read_file(input_file), read_file(test_file)

def parse_data(lines: list[str]) -> tuple[list[list[str]], str]:
    """Parse input data into maze and moves"""
    maze = []
    moves = []
    is_maze = True
    
    for line in lines:
        if not line:
            is_maze = False
            continue
        if is_maze:
            maze.append(line)
        else:
            moves.append(line)
    
    return maze, ''.join(moves)

def grid_rotation_wrapper(func):
    """Decorator to handle grid rotations for different directions"""
    @wraps(func)
    def wrapper(maze: list[str], dirr: str, *args, **kwargs):
        rotations = {
            '^': 3,
            'v': 1,
            '>': 2,
            '<': 0
        }
        
        # Rotate to standard orientation
        for _ in range(rotations[dirr]):
            maze = grid_rotate(maze)
            
        result = func(maze, dirr, *args, **kwargs)
        
        # Rotate back
        for _ in range((4 - rotations[dirr]) % 4):
            result = grid_rotate(result)
            
        return result
    return wrapper

def silver(lines: list[str]) -> int:
    """Solve part 1"""
    @grid_rotation_wrapper
    def move_box(maze: list[str], _: str) -> list[str]:
        r, c = grid_find(maze, '@')
        ll = 1
        while maze[r][c - ll] == 'O':
            ll += 1
        if maze[r][c - ll] == '.':
            maze[r][c - ll] = 'O'
            maze[r][c - 1] = '@'
            maze[r][c] = '.'
        return maze

    maze_data, moves = parse_data(lines)
    maze = [list(line) for line in maze_data]

    for char in moves:
        r, c = grid_find(maze, '@')
        dr, dc = DIRS_ARROWS[char]
        
        if maze[r + dr][c + dc] == '.':
            maze[r + dr][c + dc] = '@'
            maze[r][c] = '.'
        elif maze[r + dr][c + dc] == 'O':
            maze = move_box(maze, char)

    return sum(row * 100 + col for row, line in enumerate(maze) 
              for col, char in enumerate(line) if char == 'O')

def gold(lines: list[str]) -> int:
    """Solve part 2"""
    @grid_rotation_wrapper
    def move_box(maze: list[str], dirr: str) -> list[str]:
        def pair(maze: list[str], point: tuple[int, int, str]) -> set[tuple[int,int,str]]:
            r, c = point[0], point[1]
            dr, dc = DIRS_ARROWS[dirr]
            points = set([(r, c, maze[r][c])])

            if dirr in '^v':
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

        robot = grid_find(maze, '@')
        seen = set()
        boxes = pair(maze, (robot[0], robot[1] - 1))

        while boxes:
            poped = boxes.pop()
            if poped in seen:
                continue
            seen.add(poped)
            r, c, _ = poped
            if maze[r][c - 1] == '#':
                return maze
            if maze[r][c - 1] != '.':
                boxes |= pair(maze, (r, c - 1))

        for r, c, _ in seen:
            maze[r][c] = '.'
        for r, c, char in seen:
            maze[r][c-1] = char
        robot_r, robot_c = robot
        maze[robot_r][robot_c - 1] = '@'
        maze[robot_r][robot_c] = '.'
        return maze

    maze_data, moves = parse_data(lines)
    char_map = {
        '@': '@.',
        '#': '##',
        'O': '[]',
        '.': '..'
    }
    
    maze = []
    for line in maze_data:
        maze.append(list(''.join(char_map[char] for char in line)))

    for char in moves:
        r, c = grid_find(maze, '@')
        dr, dc = DIRS_ARROWS[char]

        if maze[r + dr][c + dc] == '.':
            maze[r][c] = '.'
            maze[r + dr][c + dc] = '@'
        elif maze[r + dr][c + dc] in '[]':
            maze = move_box(maze, char)

    return sum(row * 100 + col for row, line in enumerate(maze) 
              for col, char in enumerate(line) if char == '[')

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", 
                       help="run the test samples only",
                       action="store_true")
    return parser.parse_args()

def main():
    """Main function"""
    lines, test = content()
    options = parse_args()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    if not options.debug:
        print(f"Silver:      {silver(lines)}")
        print(f"Gold:        {gold(lines)}")

if __name__ == "__main__":
    main()