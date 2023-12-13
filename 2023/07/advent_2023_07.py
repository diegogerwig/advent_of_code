#!/usr/bin/python3

import os
import time
import pathlib
import sys

import collections

from colorama import init, Fore
init(autoreset=True)

# Function to parse the input data
def parse_data(puzzle_input):
    data = []
    # Split the input into lines and process each line
    for line in puzzle_input.split("\n"):
        cards, bid = line.split()
        # Append a tuple containing the cards and bid to the 'data' list
        data.append((cards, int(bid)))
    return data

# Function to solve part 1 of the puzzle
def part1(data):
    # Sort the cards based on their rank and calculate the score
    cards = sorted(((rank_cards(cards), bid) for cards, bid in data), reverse=True)
    return sum(rank * bid for rank, (_, bid) in enumerate(cards, start=1))

# Function to solve part 2 of the puzzle
def part2(data):
    # Sort the cards based on their rank (using joker) and calculate the score
    cards = sorted(
        ((rank_cards(cards, use_joker=True), bid) for cards, bid in data), reverse=True
    )
    return sum(rank * bid for rank, (_, bid) in enumerate(cards, start=1))

# Function to rank the cards based on their type and order
def rank_cards(cards, use_joker=False):
    # Define the order of card ranks
    order = "AKQT98765432J" if use_joker else "AKQJT98765432"
    # Return a tuple containing the classification and the index of each card in the order
    return (classify(cards, use_joker=use_joker),) + tuple(
        order.index(card) for card in cards
    )

# Function to classify the type of cards (e.g., pair, two pairs, etc.)
def classify(cards, use_joker):
    # If a joker is used, replace it with the most common card and reclassify
    if use_joker:
        card_counts = collections.Counter(cards)
        if "J" in card_counts:
            common, _ = max(card_counts.items(), key=lambda x: (x[0] != "J", x[1]))
            return classify(cards.replace("J", common), use_joker=False)

    # Sort and count the occurrences of each card in the hand
    counts = sorted(collections.Counter(cards).values())

    # Classify the hand based on the count of each card type
    if tuple(counts) == (5,):  # Five of a kind
        return 1
    elif tuple(counts) == (1, 4):  # Four of a kind
        return 2
    elif tuple(counts) == (2, 3):  # Full house
        return 3
    elif tuple(counts) == (1, 1, 3):  # Three of a kind
        return 4
    elif tuple(counts) == (1, 2, 2):  # Two pairs
        return 5
    elif tuple(counts) == (1, 1, 1, 2):  # One pair
        return 6
    elif tuple(counts) == (1, 1, 1, 1, 1):  # High card
        return 7
    else:
        # Raise an error if the hand couldn't be classified
        raise ValueError(f"couldn't classify {cards}")

def solve(input_file):
    data = parse_data(input_file)
    yield part1(data)
    yield part2(data)

if __name__ == "__main__":
    dir_input = "./input"

    file_input = os.listdir(dir_input)

    for file_name in file_input:
        start_time = time.time()

        file_path = os.path.join(dir_input, file_name)

        print(f"{Fore.YELLOW}{file_path}:")
        
        try:
            input_file = pathlib.Path(file_path).read_text().rstrip()
            if not input_file:
                print("⚠️  Input file is empty.")
            else:
                solutions = solve(input_file)
                print("\n".join(str(solution) for solution in solutions))
        except Exception as e:
            print(f"🔴  Error reading or processing the file: {e}")

        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_rounded = "{:.4f}".format(execution_time)
        print(f"Execution time: {execution_time_rounded} s")

        print("*" * 50)