'''
--- Day 22: Monkey Market ---
As you're all teleported deep into the jungle, a monkey steals The Historians' device! You'll need get it back while The Historians are looking for the Chief.

The monkey that stole the device seems willing to trade it, but only in exchange for an absurd number of bananas. Your only option is to buy bananas on the Monkey Exchange Market.

You aren't sure how the Monkey Exchange Market works, but one of The Historians senses trouble and comes over to help. Apparently, they've been studying these monkeys for a while and have deciphered their secrets.

Today, the Market is full of monkeys buying good hiding spots. Fortunately, because of the time you recently spent in this jungle, you know lots of good hiding spots you can sell! If you sell enough hiding spots, you should be able to get enough bananas to buy the device back.

On the Market, the buyers seem to use random prices, but their prices are actually only pseudorandom! If you know the secret of how they pick their prices, you can wait for the perfect time to sell.

The part about secrets is literal, the Historian explains. Each buyer produces a pseudorandom sequence of secret numbers where each secret is derived from the previous.

In particular, each buyer's secret number evolves into the next secret number in the sequence via the following process:

Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
Each step of the above process involves mixing and pruning:

To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
To prune the secret number, calculate the value of the secret number modulo 16777216. Then, the secret number becomes the result of that operation. (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
After this process completes, the buyer is left with the next secret number in the sequence. The buyer can repeat this process as many times as necessary to produce more secret numbers.

So, if a buyer had a secret number of 123, that buyer's next ten secret numbers would be:

15887950
16495136
527345
704524
1553684
12683156
11100544
12249484
7753432
5908254
Each buyer uses their own secret number when choosing their price, so it's important to be able to predict the sequence of secret numbers for each buyer. Fortunately, the Historian's research has uncovered the initial secret number of each buyer (your puzzle input). For example:

1
10
100
2024
This list describes the initial secret number of four different secret-hiding-spot-buyers on the Monkey Exchange Market. If you can simulate secret numbers from each buyer, you'll be able to predict all of their future prices.

In a single day, buyers each have time to generate 2000 new secret numbers. In this example, for each buyer, their initial secret number and the 2000th new secret number they would generate are:

1: 8685429
10: 4700978
100: 15273692
2024: 8667524
Adding up the 2000th new secret number for each buyer produces 37327623.

For each buyer, simulate the creation of 2000 new secret numbers. What is the sum of the 2000th secret number generated by each buyer?

--- Part Two ---
Of course, the secret numbers aren't the prices each buyer is offering! That would be ridiculous. Instead, the prices the buyer offers are just the ones digit of each of their secret numbers.

So, if a buyer starts with a secret number of 123, that buyer's first ten prices would be:

3 (from 123)
0 (from 15887950)
6 (from 16495136)
5 (etc.)
4
4
6
4
4
2
This price is the number of bananas that buyer is offering in exchange for your information about a new hiding spot. However, you still don't speak monkey, so you can't negotiate with the buyers directly. The Historian speaks a little, but not enough to negotiate; instead, he can ask another monkey to negotiate on your behalf.

Unfortunately, the monkey only knows how to decide when to sell by looking at the changes in price. Specifically, the monkey will only look for a specific sequence of four consecutive changes in price, then immediately sell when it sees that sequence.

So, if a buyer starts with a secret number of 123, that buyer's first ten secret numbers, prices, and the associated changes would be:

     123: 3 
15887950: 0 (-3)
16495136: 6 (6)
  527345: 5 (-1)
  704524: 4 (-1)
 1553684: 4 (0)
12683156: 6 (2)
11100544: 4 (-2)
12249484: 4 (0)
 7753432: 2 (-2)
Note that the first price has no associated change because there was no previous price to compare it with.

In this short example, within just these first few prices, the highest price will be 6, so it would be nice to give the monkey instructions that would make it sell at that time. The first 6 occurs after only two changes, so there's no way to instruct the monkey to sell then, but the second 6 occurs after the changes -1,-1,0,2. So, if you gave the monkey that sequence of changes, it would wait until the first time it sees that sequence and then immediately sell your hiding spot information at the current price, winning you 6 bananas.

Each buyer only wants to buy one hiding spot, so after the hiding spot is sold, the monkey will move on to the next buyer. If the monkey never hears that sequence of price changes from a buyer, the monkey will never sell, and will instead just move on to the next buyer.

Worse, you can only give the monkey a single sequence of four price changes to look for. You can't change the sequence between buyers.

You're going to need as many bananas as possible, so you'll need to determine which sequence of four price changes will cause the monkey to get you the most bananas overall. Each buyer is going to generate 2000 secret numbers after their initial secret number, so, for each buyer, you'll have 2000 price changes in which your sequence can occur.

Suppose the initial secret number of each buyer is:

1
2
3
2024
There are many sequences of four price changes you could tell the monkey, but for these four buyers, the sequence that will get you the most bananas is -2,1,-1,3. Using that sequence, the monkey will make the following sales:

For the buyer with an initial secret number of 1, changes -2,1,-1,3 first occur when the price is 7.
For the buyer with initial secret 2, changes -2,1,-1,3 first occur when the price is 7.
For the buyer with initial secret 3, the change sequence -2,1,-1,3 does not occur in the first 2000 changes.
For the buyer starting with 2024, changes -2,1,-1,3 first occur when the price is 9.
So, by asking the monkey to sell the first time each buyer's prices go down 2, then up 1, then down 1, then up 3, you would get 23 (7 + 7 + 9) bananas!

Figure out the best sequence to tell the monkey so that by looking for that same sequence of changes in every buyer's future prices, you get the most bananas in total. What is the most bananas you can get?
'''


#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from itertools import product

init(autoreset=True)

CURRENT_FILEPATH = ""

TEST_STATUS = {
    "PASSED": "PASSED",
    "FAILED": "FAILED", 
    "IN_PROGRESS": "IN PROGRESS",
    "UNKNOWN": "UNKNOWN"
}

STATUS_COLORS = {
    TEST_STATUS["PASSED"]: Fore.GREEN,
    TEST_STATUS["FAILED"]: Fore.RED,
    TEST_STATUS["IN_PROGRESS"]: Fore.YELLOW,
    TEST_STATUS["UNKNOWN"]: Fore.BLUE
}

TEST_SOLUTIONS = {
    ".test_I.txt": {
        "part1": 37327623,
        "part2": 'N/A',
    },
    ".test_II.txt": {
        "part1": 'N/A',
        "part2": 23,
    },
    "input_I.txt": {
        "part1": 20332089158,
        "part2": 'N/A',
    }
}


def print_header(filename, part):
    """
    Simple header printing function
    """
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Processing file: {Fore.YELLOW}{filename}")
    print(f"{Fore.CYAN}Part {part}")
    print(f"{Fore.CYAN}{'='*80}\n")


def parse_input(content):
    """
    Parse the input content removing empty lines and whitespace
    """
    lines = content.splitlines()  # split by newlines
    result = []
    
    for line in lines:
        clean_line = line.strip()  # remove whitespace at start and end
        if clean_line:  # if line is not empty
            result.append(clean_line)
            
    return result




def generate_next_secret(secret):
    """
    Generate the next secret number based on the rules:
    1. Multiply by 64, mix (XOR), and prune
    2. Divide by 32, mix (XOR), and prune
    3. Multiply by 2048, mix (XOR), and prune
    """
    # Step 1: Multiply by 64, mix, and prune
    result = secret
    mult_64 = result * 64
    result ^= mult_64  # mix (XOR)
    result %= 16777216  # prune
    
    # Step 2: Divide by 32, mix, and prune
    div_32 = result // 32
    result ^= div_32
    result %= 16777216
    
    # Step 3: Multiply by 2048, mix, and prune
    mult_2048 = result * 2048
    result ^= mult_2048
    result %= 16777216
    
    return result


def get_nth_secret(initial, n):
    """
    Get the nth secret number in the sequence starting from initial
    """
    current = initial
    for _ in range(n):
        current = generate_next_secret(current)
    return current


def part1(content):
    """
    Solution for Part 1
    - Parse initial secret numbers from input
    - For each number, generate 2000 new secret numbers using the given rules
    - Sum the 2000th number from each sequence
    """
    start_time = time.time()
    
    # Parse input
    data = parse_input(content)

    # Convert strings to numbers more explicitly
    initial_numbers = []
    for item in data:
        number = int(item)
        initial_numbers.append(number)
    
    # Get 2000th number for each sequence and sum them
    total = 0
    for num in initial_numbers:
        secret_2000 = get_nth_secret(num, 2000)
        total = total + secret_2000
    
    result = {
        "value": total,
        "execution_time": time.time() - start_time
    }
    
    return result




def generate_price_sequence(initial, count):
    """Generate a sequence of prices (ones digits) from an initial secret"""
    prices = []
    current = initial
    
    # Use a more efficient list building approach
    for _ in range(count + 1):  # +1 for initial number
        prices.append(current % 10)
        current = generate_next_secret(current)
    
    return prices

def get_price_changes(prices):
    """Calculate the changes between consecutive prices"""
    # More efficient list comprehension for changes
    return [b - a for a, b in zip(prices[:-1], prices[1:])]

def find_first_match(changes, target_sequence):
    """Find the first occurrence of target_sequence in changes using a sliding window"""
    target_len = len(target_sequence)
    for i in range(len(changes) - target_len + 1):
        # Use direct comparison for better performance
        match = True
        for j in range(target_len):
            if changes[i + j] != target_sequence[j]:
                match = False
                break
        if match:
            return i + target_len
    return -1

def evaluate_sequence_batch(args):
    """Evaluate a batch of sequences against all price sequences"""
    sequences_batch, price_sequences = args
    results = []
    
    for sequence in sequences_batch:
        total_bananas = 0
        for prices in price_sequences:
            changes = get_price_changes(prices)
            match_index = find_first_match(changes, sequence)
            if match_index != -1:
                total_bananas += prices[match_index]
        results.append((sequence, total_bananas))
    
    return results

def part2(content):
    """
    Solution for Part 2 with optimization and progress bars
    """
    start_time = time.time()
    print(f"{Fore.CYAN}Starting Part 2 solution...")
    
    # Parse input
    data = parse_input(content)
    initial_numbers = [int(x) for x in data]
    
    # Generate price sequences for all buyers with progress bar
    print(f"{Fore.YELLOW}Generating price sequences...")
    sequences = []
    for num in tqdm(initial_numbers, desc="Generating sequences"):
        sequences.append(generate_price_sequence(num, 2000))
    
    # Generate all possible change sequences
    possible_changes = [-3, -2, -1, 0, 1, 2, 3]
    all_sequences = list(product(possible_changes, repeat=4))
    
    # Split sequences into batches for parallel processing
    num_cores = cpu_count()
    batch_size = len(all_sequences) // num_cores
    sequence_batches = [
        all_sequences[i:i + batch_size] 
        for i in range(0, len(all_sequences), batch_size)
    ]
    
    # Prepare arguments for parallel processing
    pool_args = [(batch, sequences) for batch in sequence_batches]
    
    # Process sequences in parallel with progress bar
    print(f"{Fore.YELLOW}Evaluating sequences using {num_cores} cores...")
    max_bananas = 0
    best_sequence = None
    
    with Pool(num_cores) as pool:
        results = []
        with tqdm(total=len(sequence_batches), desc="Processing batches") as pbar:
            for batch_results in pool.imap_unordered(evaluate_sequence_batch, pool_args):
                for sequence, bananas in batch_results:
                    if bananas > max_bananas:
                        max_bananas = bananas
                        best_sequence = sequence
                        print(f"\n{Fore.GREEN}New best sequence found: {sequence} → {bananas} bananas")
                pbar.update(1)
    
    print(f"\n{Fore.GREEN}Best sequence found: {best_sequence}")
    print(f"{Fore.GREEN}Maximum bananas: {max_bananas}")
    print(f"{Fore.CYAN}Execution time: {time.time() - start_time:.2f} seconds")
    
    return {
        "value": max_bananas,
        "execution_time": time.time() - start_time
    }




def determine_test_status(result, expected):
    """
    Determine the test status based on the result and expected value.
    """
    if expected == 'N/A':
        return TEST_STATUS["IN_PROGRESS"]
    
    # Convert both values to strings for comparison to handle mixed types
    result_str = str(result["value"])
    expected_str = str(expected)
    
    if result_str == expected_str:
        return TEST_STATUS["PASSED"]
    return TEST_STATUS["FAILED"]


def get_status_color(status):
    """
    Get the appropriate color for each status
    """
    return STATUS_COLORS.get(status, Fore.WHITE)


def process_file(filepath):
    """
    Process a single file and validate results against test solutions
    """
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            
            print_header(filename, 1)
            part1_result = part1(content)
            
            print_header(filename, 2)
            part2_result = part2(content)
            
            # Get test solutions if available
            test_solution = TEST_SOLUTIONS.get(filename, {})
            
            # Add status to results
            part1_result["status"] = determine_test_status(
                part1_result, 
                test_solution.get("part1", 0)
            )
            part2_result["status"] = determine_test_status(
                part2_result,
                test_solution.get("part2", 0)
            )
            
            return True, {
                "part1": part1_result,
                "part2": part2_result
            }
            
    except Exception as e:
        return False, str(e)


def process_directory(input_dir="./input/"):
    """Process all files in the specified directory"""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    print(f"\n{Fore.CYAN}Processing files in directory: {Fore.YELLOW}{input_dir}")
    files = []
    for f in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, f)):
            files.append(f)
    results = {}
    
    for file in files:
        filepath = os.path.join(input_dir, file)
        success, result = process_file(filepath)
        results[file] = (success, result)
    
    return results


def print_results(results):
    """Print results with enhanced status display"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Final Results")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    for file, (success, result) in results.items():
        print(f"\n{Fore.BLUE}{file}:")
        
        if success:
            for part_name, part_result in result.items():
                status_color = get_status_color(part_result["status"])
                status_text = f"[{part_result['status']}]"
                
                # Add expected value for FAILED status
                if part_result["status"] == TEST_STATUS["FAILED"]:
                    status_text += f" (Expected: {TEST_SOLUTIONS[file][part_name]})"
                
                print(f"  {Fore.YELLOW}{part_name}: "
                      f"{Fore.GREEN}{part_result['value']:<15} "
                      f"{status_color}{status_text}  "
                      f"{Fore.CYAN}Time: {part_result['execution_time']:.6f}s")
        else:
            print(f"  {Fore.RED}Error - {result}")


def main():
    try:
        input_dir = "./input/"
        results = process_directory(input_dir)
        print_results(results)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()