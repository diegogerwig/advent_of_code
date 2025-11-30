#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.timing import timer
from utils.testing import run_tests

init(autoreset=True)

class DayXX:
    def __init__(self, content):
        self.content = content
        self.data = self.parse_input(content)
        
    def parse_input(self, content):
        """Parse the input content"""
        lines = content.splitlines()
        result = []
        
        for line in lines:
            clean_line = line.strip()
            if clean_line:
                result.append(clean_line)
                
        return result

    @timer
    def part1(self):
        """Solution for Part 1"""
        # TODO: Implement part 1 solution
        result = 0
        
        # Example implementation
        for line in self.data:
            # Process each line
            pass
            
        return result

    @timer
    def part2(self):
        """Solution for Part 2"""
        # TODO: Implement part 2 solution
        result = 0
        
        # Example implementation  
        for line in self.data:
            # Process each line
            pass
            
        return result

def solve():
    """Main solving function"""
    day_dir = Path(__file__).parent
    input_file = day_dir / "input.txt"
    example_file = day_dir / "example.txt"
    
    # Test with example first
    if example_file.exists():
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Testing with example input")
        print(f"{Fore.CYAN}{'='*60}")
        
        with open(example_file, 'r') as f:
            example_content = f.read()
        
        day = DayXX(example_content)
        
        try:
            result1 = day.part1()
            print(f"{Fore.GREEN}Part 1 (example): {result1}")
        except Exception as e:
            print(f"{Fore.RED}Part 1 failed: {e}")
        
        try:
            result2 = day.part2() 
            print(f"{Fore.GREEN}Part 2 (example): {result2}")
        except Exception as e:
            print(f"{Fore.RED}Part 2 failed: {e}")
    
    # Solve with real input
    if input_file.exists():
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Solving with real input")
        print(f"{Fore.CYAN}{'='*60}")
        
        with open(input_file, 'r') as f:
            input_content = f.read()
        
        day = DayXX(input_content)
        
        result1 = day.part1()
        print(f"{Fore.GREEN}✅ Part 1: {result1}")
        
        result2 = day.part2()
        print(f"{Fore.GREEN}✅ Part 2: {result2}")

if __name__ == "__main__":
    solve()