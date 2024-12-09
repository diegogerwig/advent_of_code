#!/usr/bin/python3

'''
--- Day 9: Disk Fragmenter ---
Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

He shows you the disk map (your puzzle input) he's already generated. For example:

2333133121414131402
The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

0..111....22222
The first example above, 2333133121414131402, represents these individual blocks:

00...111...2...333.44.5555.6666.777.888899
The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......
The first example requires a few more steps:

00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............
The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)

--- Part Two ---
Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..
The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?
'''

import os
from colorama import init, Fore, Style
from tqdm import tqdm
import inspect

init(autoreset=True)

CURRENT_FILEPATH = ""


def show_header(filename, function_name):
    """
    Prints a formatted header showing current file and operation
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Function: {Fore.YELLOW}{function_name}")
    print(f"{Fore.CYAN}{'='*80}\n")


def single_block_movement(content):
    """
    Part 1: Moves blocks one by one from end to start
    """
    # Get function name and file for header
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    show_header(filename, f"Part 1 - {current_func}")
    
    # Create empty disk and start with file ID 0
    disk = []
    file_id = 0
    
    # Remove spaces from input
    content = content.strip()
    
    # Read the input two numbers at a time
    position = 0
    while position < len(content):
        # First number is file size
        file_size = int(content[position])
        
        # Add file blocks with current ID
        for _ in range(file_size):
            disk.append(str(file_id))
            
        # Move to next number and increase file ID
        position += 1
        file_id += 1
        
        # If there's a space size, add empty spaces
        if position < len(content):
            space_size = int(content[position])
            for _ in range(space_size):
                disk.append('.')
            position += 1
    
    # Move blocks from end to start
    total_files = file_id
    for current_file in tqdm(range(total_files - 1, -1, -1), 
                           desc="Moving blocks", 
                           bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'):
        # Find all blocks of this file
        blocks_positions = []
        for position, block in enumerate(disk):
            if block == str(current_file):
                blocks_positions.append(position)
        
        # For each block of this file
        for block_position in sorted(blocks_positions):
            # Look for a free space to move it
            for free_position in range(len(disk)):
                # If we found a free space before this block
                if disk[free_position] == '.' and free_position < block_position:
                    # Move the block here
                    disk[free_position] = str(current_file)
                    disk[block_position] = '.'
                    break
    
    # Calculate final score
    final_score = 0
    for position, block in enumerate(disk):
        if block != '.':
            final_score += position * int(block)
    
    return final_score


def whole_file_movement(content):
    """
    Part 2: Moves entire files at once from end to start
    """
    # Get function name and file for header
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    show_header(filename, f"Part 2 - {current_func}")
    
    # Create empty disk and start with file ID 0
    disk = []
    file_id = 0
    
    # Remove spaces from input
    content = content.strip()
    
    # Read the input two numbers at a time
    position = 0
    while position < len(content):
        # First number is file size
        file_size = int(content[position])
        
        # Add file blocks with current ID
        for _ in range(file_size):
            disk.append(str(file_id))
            
        # Move to next number and increase file ID
        position += 1
        file_id += 1
        
        # If there's a space size, add empty spaces
        if position < len(content):
            space_size = int(content[position])
            for _ in range(space_size):
                disk.append('.')
            position += 1
    
    # Move files from end to start
    total_files = file_id
    for current_file in tqdm(range(total_files - 1, -1, -1), 
                           desc="Moving files", 
                           bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'):
        # Find the boundaries of current file
        blocks_positions = []
        for position, block in enumerate(disk):
            if block == str(current_file):
                blocks_positions.append(position)
        
        if blocks_positions:  # If file was found
            file_start = blocks_positions[0]
            file_end = blocks_positions[-1]
            file_size = file_end - file_start + 1
            
            # Look for the best position to move the file
            best_position = -1
            empty_spaces = 0
            
            # Check all positions before the file
            for position in range(file_start):
                if disk[position] == '.':
                    # Start counting a new empty space
                    if empty_spaces == 0:
                        space_start = position
                    empty_spaces += 1
                    # If we found enough space, remember this position
                    if empty_spaces >= file_size:
                        best_position = space_start
                        break
                else:
                    empty_spaces = 0
            
            # If we found a good spot, move the entire file there
            if best_position != -1:
                # Copy file to new position
                for i in range(file_size):
                    disk[best_position + i] = str(current_file)
                # Clear old position
                for i in range(file_start, file_end + 1):
                    disk[i] = '.'
    
    # Calculate final score
    final_score = 0
    for position, block in enumerate(disk):
        if block != '.':
            final_score += position * int(block)
    
    return final_score


def process_file(filepath):
    """
    Process a single input file through both parts of the puzzle
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = single_block_movement(content)
        part2_result = whole_file_movement(content)
        return part1_result, part2_result


def process_directory(input_dir="./input/"):
    """
    Process all input files in the specified directory
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
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    for file, result in results.items():
        if result[0]:
            part1, part2 = result[1], result[2]
            print(f"{Fore.BLUE}File: {file}")
            print(f"  {Fore.YELLOW}Part 1 (Single Block): {Fore.GREEN}{part1}")
            print(f"  {Fore.YELLOW}Part 2 (Whole File): {Fore.GREEN}{part2}\n")
        else:
            print(f"{Fore.RED}Error processing {file}: {result[1]}\n")