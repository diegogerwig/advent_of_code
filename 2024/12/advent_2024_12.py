'''
--- Day 12: Garden Groups ---
Why not search for the Chief Historian near the gardener and his massive farm? There's plenty of food, so The Historians grab something to eat while they search.

You're about to settle near a complex arrangement of garden plots when some Elves ask if you can lend a hand. They'd like to set up fences around each region of garden plots, but they can't figure out how much fence they need to order or how much it will cost. They hand you a map (your puzzle input) of the garden plots.

Each garden plot grows only a single type of plant and is indicated by a single letter on your map. When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), they form a region. For example:

AAAA
BBCD
BBCC
EEEC
This 4x4 arrangement includes garden plots growing five different types of plants (labeled A, B, C, D, and E), each grouped into their own region.

In order to accurately calculate the cost of the fence around a single region, you need to know that region's area and perimeter.

The area of a region is simply the number of garden plots the region contains. The above map's type A, B, and C plants are each in a region of area 4. The type E plants are in a region of area 3; the type D plants are in a region of area 1.

Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of garden plots in the region that do not touch another garden plot in the same region. The type A and C plants are each in a region with perimeter 10. The type B and E plants are each in a region with perimeter 8. The lone D plot forms its own region with perimeter 4.

Visually indicating the sides of plots in each region that contribute to the perimeter using - and |, the above map's regions' perimeters are measured as follows:

+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+
Plants of the same type can appear in multiple separate regions, and regions can even appear within other regions. For example:

OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
The above map contains five regions, one containing all of the O garden plots, and the other four each containing a single X plot.

The four X regions each have area 1 and perimeter 4. The region containing 21 type O plants is more complicated; in addition to its outer edge contributing a perimeter of 20, its boundary with each X region contributes an additional 4 to its perimeter, for a total perimeter of 36.

Due to "modern" business practices, the price of fence required for a region is found by multiplying that region's area by its perimeter. The total price of fencing all regions on a map is found by adding together the price of fence for every region on the map.

In the first example, region A has price 4 * 10 = 40, region B has price 4 * 8 = 32, region C has price 4 * 10 = 40, region D has price 1 * 4 = 4, and region E has price 3 * 8 = 24. So, the total price for the first example is 140.

In the second example, the region with all of the O plants has price 21 * 36 = 756, and each of the four smaller X regions has price 1 * 4 = 4, for a total price of 772 (756 + 4 + 4 + 4 + 4).

Here's a larger example:

RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
It contains:

A region of R plants with price 12 * 18 = 216.
A region of I plants with price 4 * 8 = 32.
A region of C plants with price 14 * 28 = 392.
A region of F plants with price 10 * 18 = 180.
A region of V plants with price 13 * 20 = 260.
A region of J plants with price 11 * 20 = 220.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 18 = 234.
A region of I plants with price 14 * 22 = 308.
A region of M plants with price 5 * 12 = 60.
A region of S plants with price 3 * 8 = 24.
So, it has a total price of 1930.

What is the total price of fencing all regions on your map?

--- Part Two ---
Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!

Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. Each straight section of fence counts as a side, regardless of how long it is.

Consider this example again:

AAAA
BBCD
BBCC
EEEC
The region containing type A plants has 4 sides, as does each of the regions containing plants of type B, D, and E. However, the more complex region containing the plants of type C has 8 sides!

Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.

The second example above (full of type X and O plants) would have a total price of 436.

Here's a map that includes an E-shaped region full of type E plants:

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
The E-shaped region has an area of 17 and 12 sides for a price of 204. Including the two regions full of type X plants, this map has a total price of 236.

This map has a total price of 368:

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
It includes two regions full of type B plants (each with 4 sides) and a single region full of type A plants (with 4 sides on the outside and 8 more sides on the inside, a total of 12 sides). Be especially careful when counting the fence around regions like the one full of type A plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two B regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)

The larger example from before now has the following updated prices:

A region of R plants with price 12 * 10 = 120.
A region of I plants with price 4 * 4 = 16.
A region of C plants with price 14 * 22 = 308.
A region of F plants with price 10 * 12 = 120.
A region of V plants with price 13 * 10 = 130.
A region of J plants with price 11 * 12 = 132.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 8 = 104.
A region of I plants with price 14 * 16 = 224.
A region of M plants with price 5 * 6 = 30.
A region of S plants with price 3 * 6 = 18.
Adding these together produces its new total price of 1206.

What is the new total price of fencing all regions on your map?
'''

#!/usr/bin/python3

import os
from colorama import init, Fore
import inspect

init(autoreset=True)

CURRENT_FILEPATH = ""


def print_header(filename, part):
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing Part {part} - File: {filename}")
    print(f"{Fore.YELLOW}{'Type':<5}{'Area':<6}{'Metric':<7}{'Price':<8} │ {'Details'}")
    print(f"{Fore.CYAN}{'-'*35}│{'-'*14}")


def print_region_info(plant_type, area, metric, price):
    print(f"{Fore.GREEN}{plant_type:<5}{area:<6}{metric:<7}{price:<8} │ {area} × {metric} = {price}")


def print_grid_info(grid, only_dimensions=False):
    if not only_dimensions:
        print("\nGrid:")
        for row in grid:
            print(''.join(row))
    print(f"Size: {len(grid)}x{len(grid[0])}\n")
    

def get_neighbours(grid, row, col):
    """
    Get valid neighboring cells in the grid (up, down, left, right)
    """
    neighbours = []
    rows = len(grid)
    cols = len(grid[0])
    
    # Check all four directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dir_row, dir_col in directions:
        new_row = row + dir_row
        new_col = col + dir_col
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbours.append((new_row, new_col))
    
    return neighbours


def count_region_properties(grid, row, col, visited):
    """
    Count area and perimeter of a region starting at given position
    """
    plant_type = grid[row][col]
    
    area = 0
    perimeter = 0
    stack = [(row, col)]
    
    while stack:
        current_row, current_col = stack.pop()
        if (current_row, current_col) in visited:
            continue
        if grid[current_row][current_col] != plant_type:
            continue
            
        visited.add((current_row, current_col))
        area += 1
        
        neighbours = get_neighbours(grid, current_row, current_col)
        edge_count = 4
        
        for next_row, next_col in neighbours:
            if grid[next_row][next_col] == plant_type:
                edge_count -= 1
                if (next_row, next_col) not in visited:
                    stack.append((next_row, next_col))
                    
        perimeter += edge_count
    
    return area, perimeter


def get_region(grid, row, col, visited):
    """
    Get all cells in a region and count its area
    """
    rows = len(grid)
    cols = len(grid[0])
    plant_type = grid[row][col]
    
    region = set()
    area = 0
    stack = [(row, col)]
    
    while stack:
        current_row, current_col = stack.pop()
        if (current_row, current_col) in visited:
            continue
        if grid[current_row][current_col] != plant_type:
            continue
            
        visited.add((current_row, current_col))
        region.add((current_row, current_col))
        area += 1
        
        for nr, nc in [(current_row-1,current_col), (current_row+1,current_col), 
                       (current_row,current_col-1), (current_row,current_col+1)]:
            if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in visited:
                stack.append((nr, nc))
    
    return region, area


def find_segments_in_row(region, row):
    """
    Finds continuous segments in a row directly from region coordinates
    Returns list of tuples (start, end) for each continuous segment
    """
    # Get all columns in this row
    cols = sorted([col for r, col in region if r == row])
    if not cols:
        return []
    
    segments = []
    start = cols[0]
    prev = start
    
    for col in cols[1:]:
        if col > prev + 1:  # Gap found
            segments.append((start, prev))
            start = col
        prev = col
    segments.append((start, prev))
    
    return segments


def calc_segment_overlaps(segments1, segments2):
    """
    Calculates overlapping sides between segments in adjacent rows
    Returns total number of overlapping edges
    """
    overlaps = 0
    for seg1 in segments1:
        for seg2 in segments2:
            if seg1[0] == seg2[0] and seg1[1] == seg2[1]:
                overlaps += 4  # Complete overlap
            elif seg1[0] == seg2[0]:
                overlaps += 2  # Start point overlap
            elif seg1[1] == seg2[1]:
                overlaps += 2  # End point overlap
    return overlaps


def count_straight_sides(region, grid_rows, grid_cols):
    """
    Counts straight sides directly from region coordinates
    Returns total number of straight sides
    """
    if not region:
        return 0
    
    # Get all rows that contain region cells
    rows = sorted(set(r for r, _ in region))
    if not rows:
        return 0
    
    # Process first row
    prev_segments = find_segments_in_row(region, rows[0])
    total_sides = 4 * len(prev_segments)
    
    # Process remaining rows
    for row in rows[1:]:
        curr_segments = find_segments_in_row(region, row)
        overlaps = calc_segment_overlaps(prev_segments, curr_segments)
        total_sides += (4 * len(curr_segments)) - overlaps
        prev_segments = curr_segments
    
    return total_sides


def price_by_perimeter(content):
    """
    Price = area * perimeter for each region
    """
    # Get function name and file for header
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_header(filename, f"Part 1 - {current_func}")
    
    # Parse input into grid
    lines = content.strip().split('\n')
    while lines and not all(c.isalpha() for c in lines[0]):
        lines.pop(0)
    
    grid = []
    for line in lines:
        if all(c.isalpha() for c in line):
            grid.append(list(line))
    
    if not grid:
        print(f"{Fore.RED}Error: Empty grid")
        return 0
        
    print_grid_info(grid)
        
    visited = set()
    total_price = 0
    rows = len(grid)
    cols = len(grid[0])
    
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                area, perimeter = count_region_properties(grid, row, col, visited)
                price = area * perimeter
                total_price += price
                print_region_info(grid[row][col], area, perimeter, price)
    
    print(f"\n{Fore.GREEN}Total Price: {total_price}")
    return total_price


def price_by_sides(content):
    """
    Price = area * number of straight sides for each region
    """
    # Get function name and file for header
    filename = os.path.basename(CURRENT_FILEPATH)
    current_func = inspect.currentframe().f_code.co_name.replace('_', ' ').title()
    print_header(filename, f"Part 2 - {current_func}")
    
    # Parse input into grid
    lines = content.strip().split('\n')
    while lines and not all(c.isalpha() for c in lines[0]):
        lines.pop(0)
        
    grid = []
    for line in lines:
        if all(c.isalpha() for c in line):
            grid.append(list(line))
            
    if not grid:
        print(f"{Fore.RED}Error: Empty grid")
        return 0
        
    print_grid_info(grid)
    
    visited = set()
    total_price = 0
    rows = len(grid)
    cols = len(grid[0])
    
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                region, area = get_region(grid, row, col, visited)
                sides = count_straight_sides(region, rows, cols)
                price = area * sides
                total_price += price
                print_region_info(grid[row][col], area, sides, price)
                
    print(f"\n{Fore.GREEN}Total Price: {total_price}")
    return total_price


def process_file(filepath):
    """
    Process a single input file through both parts of the puzzle
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    
    with open(filepath, 'r') as file:
        content = file.read()
        part1_result = price_by_perimeter(content)
        part2_result = price_by_sides(content)
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
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Garden Groups Analysis Tool")
    print(f"{Fore.CYAN}{'='*80}")
    
    results = process_directory("./input/")
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}")
    
    for file, result in results.items():
        if result[0]:
            print(f"\n{Fore.BLUE}{file}:")
            print(f"{Fore.YELLOW}Part 1 Price by PERIMETER: {Fore.GREEN}{result[1]}")
            print(f"{Fore.YELLOW}Part 2 Price by SIDES:     {Fore.GREEN}{result[2]}")
        else:
            print(f"\n{Fore.RED}Error processing {file}: {result[1]}")