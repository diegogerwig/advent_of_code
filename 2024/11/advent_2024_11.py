'''
--- Day 11: Plutonian Pebbles ---
The ancient civilization on Pluto was known for its ability to manipulate spacetime, and while The Historians explore their infinite corridors, you've noticed a strange set of physics-defying stones.

At first glance, they seem like normal stones: they're arranged in a perfectly straight line, and each stone has a number engraved on it.

The strange part is that every time you blink, the stones change.

Sometimes, the number engraved on a stone changes. Other times, a stone might split in two, causing all the other stones to shift over a bit to make room in their perfectly straight line.

As you observe them for a while, you find that the stones have a consistent behavior. Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:

If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.

How will the stones evolve if you keep blinking at them? You take a note of the number engraved on each stone in the line (your puzzle input).

If you have an arrangement of five stones engraved with the numbers 0 1 10 99 999 and you blink once, the stones transform as follows:

The first stone, 0, becomes a stone marked 1.
The second stone, 1, is multiplied by 2024 to become 2024.
The third stone, 10, is split into a stone marked 1 followed by a stone marked 0.
The fourth stone, 99, is split into two stones marked 9.
The fifth stone, 999, is replaced by a stone marked 2021976.
So, after blinking once, your five stones would become an arrangement of seven stones engraved with the numbers 1 2024 1 0 9 9 2021976.

Here is a longer example:

Initial arrangement:
125 17

After 1 blink:
253000 1 7

After 2 blinks:
253 0 2024 14168

After 3 blinks:
512072 1 20 24 28676032

After 4 blinks:
512 72 2024 2 0 2 4 2867 6032

After 5 blinks:
1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

After 6 blinks:
2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2
In this example, after blinking six times, you would have 22 stones. After blinking 25 times, you would have 55312 stones!

Consider the arrangement of stones in front of you. How many stones will you have after blinking 25 times?

--- Part Two ---
The Historians sure are taking a long time. To be fair, the infinite corridors are very large.

How many stones would you have after blinking a total of 75 times?
'''

from collections import Counter  # Used to efficiently count repeated numbers
from typing import List, Tuple  # Used for type hints
import os  # Used for file operations
from colorama import init, Fore  # Used for colored terminal output

init(autoreset=True)


class StonePattern:
    """
    Keeps track of the stones and how they change.
    Uses a special technique to track zeros separately for better performance.
    """
    def __init__(self, stones: List[int]):
        # Count how many zeros we have
        self.zero_count = 0
        # Use Counter to track how many times each non-zero number appears
        self.non_zero_stones = Counter(stones)
    
    def process_blink(self) -> 'StonePattern':
        """
        Apply one blink transformation to all stones.
        Returns a new pattern with the transformed stones.
        """
        # Create a new pattern to store the results
        new_pattern = StonePattern([])
        new_non_zeros = Counter()
        
        # Rule 1: Transform existing zeros to ones
        if self.zero_count > 0:
            new_non_zeros[1] += self.zero_count
        
        # Process each non-zero stone
        for stone, count in self.non_zero_stones.items():
            if stone == 0:
                # Rule 1: Zero becomes one
                new_non_zeros[1] += count
                continue
            
            # Count how many digits the number has
            digit_count = len(str(stone))
            
            if digit_count % 2 == 0:
                # Rule 2: Split even-digit numbers into two parts
                # For example: 1234 -> 12 and 34
                divisor = 10 ** (digit_count // 2)  # This splits the number in half
                left = stone // divisor   # Get left half (12 in our example)
                right = stone % divisor   # Get right half (34 in our example)
                
                # Track the new stones, keeping zeros separate
                if left == 0:
                    new_pattern.zero_count += count
                else:
                    new_non_zeros[left] += count
                    
                if right == 0:
                    new_pattern.zero_count += count
                else:
                    new_non_zeros[right] += count
            else:
                # Rule 3: Multiply by 2024 if no other rule applies
                new_non_zeros[stone * 2024] += count
        
        # Store the new non-zero stones in our pattern
        new_pattern.non_zero_stones = new_non_zeros
        return new_pattern
    
    def total_stones(self) -> int:
        """Count how many stones we have in total"""
        return self.zero_count + sum(self.non_zero_stones.values())
    
    def preview(self, limit: int = 20) -> List[int]:
        """
        Get a preview of the first few stones.
        Shows zeros first, then other numbers in order.
        """
        result = []
        # Add zeros first
        result.extend([0] * min(self.zero_count, limit))
        # Add non-zero numbers if we still have room
        if len(result) < limit:
            non_zeros = sorted(
                [stone for stone, count in self.non_zero_stones.items() 
                 for _ in range(count)])
            result.extend(non_zeros[:limit - len(result)])
        return result[:limit]


def simulate_blinks(initial_stones: List[int], num_blinks: int) -> int:
    """
    Main simulation function that shows what happens after each blink
    """
    # Create initial pattern from our starting stones
    pattern = StonePattern(initial_stones)
    
    # Show initial state
    total = pattern.total_stones()
    zeros = pattern.zero_count
    non_zeros = total - zeros
    preview = pattern.preview()
    print(f"{Fore.CYAN}Initial:  {Fore.GREEN}[{total:16d} stones] {Fore.YELLOW}[{zeros}/{non_zeros} z/nz] {Fore.WHITE}→ {preview}")
    
    # Process each blink
    for i in range(num_blinks):
        # Transform the stones according to the rules
        pattern = pattern.process_blink()
        total = pattern.total_stones()
        zeros = pattern.zero_count
        non_zeros = total - zeros
        
        # Show what happened after this blink
        print(f"{Fore.YELLOW}Blink {i+1:2d}: {Fore.GREEN}[{total:16d} stones] {Fore.YELLOW}[{zeros}/{non_zeros} z/nz] {Fore.WHITE}→ {pattern.preview()}")
        
        # Optimization: If we only have zeros, we can predict the future!
        # Because zeros become ones, then get multiplied by 2024 and split,
        # each stone will become 2 stones in the next blink
        if non_zeros == 0 and i < num_blinks - 1:
            remaining_blinks = num_blinks - i - 1
            final_count = total * (2 ** remaining_blinks)
            print(f"{Fore.GREEN}Fast-forward {remaining_blinks} blinks → Final count: {final_count} stones")
            return final_count
            
    return pattern.total_stones()


def process_input(content: str, blinks: int) -> int:
    """
    Convert input string to numbers and simulate the blinks
    """
    initial_stones = list(map(int, content.strip().split()))
    return simulate_blinks(initial_stones, blinks)


def process_file(filepath: str) -> Tuple[int, int]:
    """
    Process one input file:
    - Part 1: Simulate 25 blinks
    - Part 2: Simulate 75 blinks
    """
    print(f"\n{Fore.CYAN}{'═' * 60}")
    print(f"{Fore.CYAN}Processing: {os.path.basename(filepath)}")
    print(f"{Fore.CYAN}{'═' * 60}")
    
    with open(filepath, 'r') as file:
        content = file.read()
        
        print(f"\n{Fore.CYAN}Part 1 (25 blinks):")
        part1_result = process_input(content, 25)
        
        print(f"\n{Fore.CYAN}Part 2 (75 blinks):")
        part2_result = process_input(content, 75)
        
        return part1_result, part2_result

if __name__ == "__main__":
    # Directory where input files are stored
    input_dir = "./input/"
    results = {}
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath):
            try:
                part1, part2 = process_file(filepath)
                results[filename] = (True, part1, part2)
            except Exception as e:
                results[filename] = (False, str(e))
    
    # Show final results for all files
    print(f"\n{Fore.CYAN}{'═' * 60}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'═' * 60}")
    
    for filename, result in results.items():
        if result[0]:  # If processing was successful
            part1, part2 = result[1], result[2]
            print(f"\n{Fore.BLUE}File: {filename}")
            print(f"{Fore.YELLOW}├─ Part 1 (25 blinks): {Fore.GREEN}{part1}")
            print(f"{Fore.YELLOW}└─ Part 2 (75 blinks): {Fore.GREEN}{part2}")
        else:  # If there was an error
            print(f"\n{Fore.RED}Error in {filename}: {result[1]}")
    
    print(f"\n{Fore.CYAN}{'═' * 60}")