import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from template.test_inputs import TEST_SOLUTIONS

class TestDayXX(unittest.TestCase):
    def setUp(self):
        self.day_dir = Path(__file__).parent
        self.example_file = self.day_dir / "example.txt"
        
    def test_part1_example(self):
        """Test part 1 with example input"""
        if self.example_file.exists():
            with open(self.example_file, 'r') as f:
                content = f.read()
            
            # Import the actual solution class
            from solution import DayXX
            day = DayXX(content)
            result = day.part1()
            
            # Get expected result from test inputs
            expected = TEST_SOLUTIONS.get("example", {}).get("part1")
            if expected is not None:
                self.assertEqual(result, expected, 
                               f"Part 1 example failed. Expected {expected}, got {result}")
    
    def test_part2_example(self):
        """Test part 2 with example input"""
        if self.example_file.exists():
            with open(self.example_file, 'r') as f:
                content = f.read()
            
            from solution import DayXX
            day = DayXX(content)
            result = day.part2()
            
            expected = TEST_SOLUTIONS.get("example", {}).get("part2")
            if expected is not None:
                self.assertEqual(result, expected,
                               f"Part 2 example failed. Expected {expected}, got {result}")

if __name__ == '__main__':
    unittest.main()