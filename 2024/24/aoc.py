import sys
import re
from math import *
from collections import *
import itertools as it
from functools import *
import bisect
import heapq
import copy
from pprint import pprint
from input_manager import download_and_store_data
from puzzle_runner import test_with_example, submit_solutions

sys.setrecursionlimit(100000)

# Common Utils
DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Left, Right, Up, Down
DIR8 = [
    (-1, 0),  # West
    (1, 0),   # East
    (0, -1),  # North
    (0, 1),   # South
    (-1, -1), # NorthWest
    (-1, 1),  # NorthEast
    (1, -1),  # SouthWest
    (1, 1)    # SouthEast
]


# Input Parsing
def input_split(string, delimiter="\n") -> list:
    """Return input array split by delimiter"""
    return string.split(delimiter)

def input_as_lines(string) -> list:
    """Return input as lines split by \\n"""
    return input_split(string)

def input_as_ints(string) -> list:
    """Convert each line to int and return list of ints"""
    lines = input_as_lines(string)
    line_as_int = lambda l: int(l.rstrip('\n'))
    return list(map(line_as_int, lines))

def input_as_grid(string) -> list:
    """Return input as 2D grid"""
    return list(list(line) for line in input_as_lines(string))

def get_diagonals_from_lines(lines):
    """Returns diagonals from top-left to bottom-right and bottom-left to top-right directions."""
    diagonals = []
    num_rows, num_cols = len(lines), len(lines[0])
    for d in range(num_rows + num_cols - 1):
        diagonals.append(''.join(lines[i][d - i] for i in range(num_rows) if 0 <= d - i < num_cols))
        diagonals.append(''.join(lines[i][i - d + num_cols - 1] for i in range(num_rows) if 0 <= i - d + num_cols - 1 < num_cols))
    return diagonals

def get_columns_from_lines(lines):
    """Return all columns from list of strings as list of strings."""
    return [''.join(line[i] for line in lines) for i in range(len(lines[0]))]

def lmap(func, *iterables) -> list:
    """Applies a function to all items in the provided iterables and returns a list."""
    return list(map(func, *iterables))

def ints(s: str) -> list:
    """Extracts a list of integers from a string."""
    return lmap(int, re.findall(r"-?\d+", s)) 

def positive_ints(s: str) -> list:
    """Extracts a list of positive integers from a string."""
    return lmap(int, re.findall(r"\d+", s))

def floats(s: str) -> list:
    """Extracts a list of floats, including negative, from a string."""
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))

def positive_floats(s: str) -> list:
    """Extracts a list of positive floats from a string."""
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))

def words(s: str) -> list:
    """Extracts a list of words (alphabetic strings) from a string."""
    return re.findall(r"[a-zA-Z]+", s)

def flatten(l):
    """Flattens a list of lists into a single list."""
    return [i for x in l for i in x]

def quantify(iterable, pred=bool) -> int:
    """Count number of items in iterable for which pred is true"""
    return sum(map(pred, iterable))

def first(iterable, default=None) -> object:
    """Return first item from iterable or default"""
    return next(iter(iterable), default)

def product(iterable) -> float:
    """Return product of items in iterable"""
    return prod(iterable)

def combinations(iterable, r):
    """Return combinations as string of r items from iterable"""
    combinations = []
    for c in it.product(iterable, repeat=r):
        combinations.append(''.join(c))
    return combinations


# Math Utils
# Helper function for Chinese Remainder Theorem
def chinese_remainder(n, a):
    """
    Takes in a list of remainders (a) and a list of moduli (n)
    Solve the equation
        x = a_0 (mod n_0)
        x = a_1 (mod n_1)
        ...
        x = a_{n-1} (mod n_{n-1})
    for x.
    """
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

# Helper function to find modular inverse
def mul_inv(a, b):
    """
    Takes two integers a and b.
    Returns the integer such that (a * x) % b == 1
    """
    
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def solve_equations(coefficients, constants):
    """
    Solves a system of linear equations using Cramer's Rule.
    coefficients: List of coefficients for each equation
    constants: List of constants for each equation
    
    Example:
    >>> coefficients = [[1, 2], [3, 4]]
    >>> constants = [5, 6]
    For the system:
    1x + 2y = 5
    3x + 4y = 6
    """
    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for c in range(len(matrix)):
            sub_matrix = [row[:c] + row[c+1:] for row in (matrix[1:])]
            det += ((-1)**c) * matrix[0][c] * determinant(sub_matrix)
        return det

    def replace_column(matrix, column, new_column):
        return [row[:column] + [new_col] + row[column+1:] for row, new_col in zip(matrix, new_column)]

    n = len(coefficients)
    det_main = determinant(coefficients)

    if det_main == 0:
        raise ValueError("The system has no unique solution")

    solutions = []
    for i in range(n):
        modified_matrix = replace_column(coefficients, i, constants)
        det_modified = determinant(modified_matrix)
        solutions.append(det_modified / det_main)

    return solutions


def lcm_list(nums):
    return reduce(lcm, nums, 1)

def gcd_list(nums):
    return reduce(gcd, nums, nums[0])

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def inside_grid(x, y, grid):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


#TODO
# Binary Search, Bisect, Union Find, Segment Tree, Sliding Window, Range 



# Useful Code
'''
# Two pointer (left and right end) iteration
for i in range(len(nums)//2):
    print(i) # 0,1,2
    print(~i) # -1 (i.e. 4), -2 (i.e. 3), -3(i.e. 2)
'''

# Graphs
'''
queue = deque()
queue.append((0, 0))
visited = set()
visited.add((0, 0))
while queue:
    x, y = queue.popleft()
    for dx, dy in DIR4:
        nx, ny = x + dx, y + dy
        if (nx, ny) in visited:
            continue
        visited.add((nx, ny))
        queue.append((nx, ny))
'''

'''General DFS
def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited
'''


'''
# Example code for Dijkstra's algorithm with priority queue
import heapq

def dijkstra(graph, start):
    """Finds the shortest paths from the start vertex to all other vertices in a graph."""
    queue = [(0, start)]
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    while queue:
        current_distance, current_vertex = heapq.heappop(queue)
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances

# Example usage with a simple graph
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}
print(dijkstra(graph, 'A'))
'''


'''
# General Karger Alorithm to find minimum cut in a graph
def karger_stein(g):
    while len(g) > 2:
        u, v = random.sample(g.nodes(), 2)
        g.remove_node(u)
        g.remove_node(v)
        g.add_edge(u, v)
    return g
'''

'''
import networkx as nx
G = nx.Graph()
# G.add_edge(3, 1)
nx.shortest_path(G, -1, 5)
'''

# Assembler interpreter
'''
prog = s.splitlines()
pc = 0
regs = []
while 0 <= pc < len(prog):
    op = prog[pc]
    if op == 1:
        ...
    elif op == 2:
        ...
    else:
        assert False
    pc += 1
'''














# Print Utils
def print_grid(grid, spacing=1):
    for row in grid:
        if spacing == 0:
            print(''.join(row))
            continue
        print(' '.join(f'{cell:>{spacing}}' for cell in row))
    print()

def print_matrix(matrix):
    for row in matrix:
        print(row)
    print()

def print_dict(d):
    for k, v in d.items():
        print(f"{k}: {v}")
    print()

def print_list(l):
    for item in l:
        print(item)
    print()

