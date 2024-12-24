import os
from aocd.models import Puzzle

def download_and_store_data(year, day, base_dir):
    # Fetch the puzzle for the specified day
    puzzle = Puzzle(year=year, day=day)
    
    # Define file paths
    input_dir = os.path.join(base_dir, "inputs")
    os.makedirs(input_dir, exist_ok=True)
    input_file = os.path.join(input_dir, "input.txt")
    example_file = os.path.join(input_dir, "example.txt")

    # Check and store input data
    if not os.path.exists(input_file):
        with open(input_file, 'w') as f:
            f.write(puzzle.input_data)

    # Check and store example data
    if puzzle.examples and not os.path.exists(example_file):
        with open(example_file, 'w') as f:
            f.write(puzzle.examples[0].input_data)

    # print("Data stored locally.")

def get_input_data(base_dir):
    """
    Read and return the content of both example.txt and input.txt files.
    
    Args:
        base_dir (str): Base directory containing the 'inputs' folder
        
    Returns:
        tuple: (example_data, input_data) containing the contents of both files
    """
    input_dir = os.path.join(base_dir, "inputs")
    input_file = os.path.join(input_dir, "input.txt")
    example_file = os.path.join(input_dir, "example.txt")
    
    example_data = ""
    input_data = ""
    
    if os.path.exists(example_file):
        with open(example_file, 'r') as f:
            example_data = f.read()
            
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            input_data = f.read()
            
    return example_data, input_data
