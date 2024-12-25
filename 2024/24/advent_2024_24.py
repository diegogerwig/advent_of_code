'''
--- Day 24: Crossed Wires ---
You and The Historians arrive at the edge of a large grove somewhere in the jungle. After the last incident, the Elves installed a small device that monitors the fruit. While The Historians search the grove, one of them asks if you can take a look at the monitoring device; apparently, it's been malfunctioning recently.

The device seems to be trying to produce a number through some boolean logic gates. Each gate has two inputs and one output. The gates all operate on values that are either true (1) or false (0).

AND gates output 1 if both inputs are 1; if either input is 0, these gates output 0.
OR gates output 1 if one or both inputs is 1; if both inputs are 0, these gates output 0.
XOR gates output 1 if the inputs are different; if the inputs are the same, these gates output 0.
Gates wait until both inputs are received before producing output; wires can carry 0, 1 or no value at all. There are no loops; once a gate has determined its output, the output will not change until the whole system is reset. Each wire is connected to at most one gate output, but can be connected to many gate inputs.

Rather than risk getting shocked while tinkering with the live system, you write down all of the gate connections and initial wire values (your puzzle input) so you can consider them in relative safety. For example:

x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
Because gates wait for input, some wires need to start with a value (as inputs to the entire system). The first section specifies these values. For example, x00: 1 means that the wire named x00 starts with the value 1 (as if a gate is already outputting that value onto that wire).

The second section lists all of the gates and the wires connected to them. For example, x00 AND y00 -> z00 describes an instance of an AND gate which has wires x00 and y00 connected to its inputs and which will write its output to wire z00.

In this example, simulating these gates eventually causes 0 to appear on wire z00, 0 to appear on wire z01, and 1 to appear on wire z02.

Ultimately, the system is trying to produce a number by combining the bits on all wires starting with z. z00 is the least significant bit, then z01, then z02, and so on.

In this example, the three output bits form the binary number 100 which is equal to the decimal number 4.

Here's a larger example:

x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
After waiting for values on all wires starting with z, the wires in this system have the following values:

bfw: 1
bqk: 1
djm: 1
ffh: 0
fgs: 1
frj: 1
fst: 1
gnj: 1
hwm: 1
kjc: 0
kpj: 1
kwq: 0
mjb: 1
nrd: 1
ntg: 0
pbm: 1
psh: 1
qhw: 1
rvg: 0
tgd: 0
tnw: 1
vdt: 1
wpb: 0
z00: 0
z01: 0
z02: 0
z03: 1
z04: 0
z05: 1
z06: 1
z07: 1
z08: 1
z09: 1
z10: 1
z11: 0
z12: 0
Combining the bits from all wires starting with z produces the binary number 0011111101000. Converting this number to decimal produces 2024.

Simulate the system of gates and wires. What decimal number does it output on the wires starting with z?

--- Part Two ---
After inspecting the monitoring device more closely, you determine that the system you're simulating is trying to add two binary numbers.

Specifically, it is treating the bits on wires starting with x as one binary number, treating the bits on wires starting with y as a second binary number, and then attempting to add those two numbers together. The output of this operation is produced as a binary number on the wires starting with z. (In all three cases, wire 00 is the least significant bit, then 01, then 02, and so on.)

The initial values for the wires in your puzzle input represent just one instance of a pair of numbers that sum to the wrong value. Ultimately, any two binary numbers provided as input should be handled correctly. That is, for any combination of bits on wires starting with x and wires starting with y, the sum of the two numbers those bits represent should be produced as a binary number on the wires starting with z.

For example, if you have an addition system with four x wires, four y wires, and five z wires, you should be able to supply any four-bit number on the x wires, any four-bit number on the y numbers, and eventually find the sum of those two numbers as a five-bit number on the z wires. One of the many ways you could provide numbers to such a system would be to pass 11 on the x wires (1011 in binary) and 13 on the y wires (1101 in binary):

x00: 1
x01: 1
x02: 0
x03: 1
y00: 1
y01: 0
y02: 1
y03: 1
If the system were working correctly, then after all gates are finished processing, you should find 24 (11+13) on the z wires as the five-bit binary number 11000:

z00: 0
z01: 0
z02: 0
z03: 1
z04: 1
Unfortunately, your actual system needs to add numbers with many more bits and therefore has many more wires.

Based on forensic analysis of scuff marks and scratches on the device, you can tell that there are exactly four pairs of gates whose output wires have been swapped. (A gate can only be in at most one such pair; no gate's output was swapped multiple times.)

For example, the system below is supposed to find the bitwise AND of the six-bit number on x00 through x05 and the six-bit number on y00 through y05 and then write the result as a six-bit number on z00 through z05:

x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
However, in this example, two pairs of gates have had their output wires swapped, causing the system to produce wrong answers. The first pair of gates with swapped outputs is x00 AND y00 -> z05 and x05 AND y05 -> z00; the second pair of gates is x01 AND y01 -> z02 and x02 AND y02 -> z01. Correcting these two swaps results in this system that works as intended for any set of initial values on wires that start with x or y:

x00 AND y00 -> z00
x01 AND y01 -> z01
x02 AND y02 -> z02
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z05
In this example, two pairs of gates have outputs that are involved in a swap. By sorting their output wires' names and joining them with commas, the list of wires involved in swaps is z00,z01,z02,z05.

Of course, your actual system is much more complex than this, and the gates that need their outputs swapped could be anywhere, not just attached to a wire starting with z. If you were to determine that you need to swap output wires aaa with eee, ooo with z99, bbb with ccc, and aoc with z24, your answer would be aaa,aoc,bbb,ccc,eee,ooo,z24,z99.

Your system of gates and wires has four pairs of gates which need their output wires swapped - eight wires in total. Determine which four pairs of gates need their outputs swapped so that your system correctly performs addition; what do you get if you sort the names of the eight wires involved in a swap and then join those names with commas?
'''


#!/usr/bin/python3

import sys
import os
from colorama import init, Fore
import time

import typer
app = typer.Typer()

from graphviz import Digraph

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
        "part1": 4,
        "part2": 'N/A',
    },
    ".test_II.txt": {
        "part1": 2024,
        "part2": 'N/A',
    },
    ".test_III.txt": {
        "part1": 'N/A',
        "part2": 'aaa,aoc,bbb,ccc,eee,ooo,z24,z99',
    },
    "input_I.txt": {
        "part1": 55920211035878,
        "part2": 'btb,cmv,mwp,rdg,rmj,z17,z23,z30',
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


def create_circuit_graph(gates, filename="logic_circuit_part1", highlight_nodes=None):
    graph = Digraph(format="png")
    graph.attr(rankdir="TB", bgcolor='lightgray')
    
    if highlight_nodes is None:
        highlight_nodes = set()
    
    is_part2 = len(gates[0]) == 4
    
    # Colors for different types
    gate_colors = {
        'AND': '#FF9999',  # Light red
        'OR': '#99FF99',   # Light green
        'XOR': '#9999FF'   # Light blue
    }
    
    for gate in gates:
        if is_part2:
            in1, op, in2, out = gate
            inputs = [in1, in2]
        else:
            inputs, op, out = gate
            
        gate_id = f"{inputs[0]}_{inputs[1]}_{op}_{out}"
        
        # Input nodes
        for inp in inputs:
            node_color = "red" if inp in highlight_nodes else "#FFB366" if inp.startswith('x') else "#66B2FF"
            graph.node(inp, inp, shape="ellipse", color="black", style="filled", fillcolor=node_color)
        
        # Gate node
        graph.node(gate_id, op, shape="box", style="filled", fillcolor=gate_colors.get(op, 'white'))
        
        # Output node
        node_color = "red" if out in highlight_nodes else "#FF99FF" if out.startswith('z') else "white"
        graph.node(out, out, shape="ellipse", color="black", style="filled", fillcolor=node_color)
        
        # Edges
        for inp in inputs:
            graph.edge(inp, gate_id)
        graph.edge(gate_id, out)
    
    # Add legend
    with graph.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', bgcolor='white')
        legend.node('x_legend', 'X inputs', shape="ellipse", style="filled", fillcolor="#FFB366")
        legend.node('y_legend', 'Y inputs', shape="ellipse", style="filled", fillcolor="#66B2FF")
        legend.node('z_legend', 'Z outputs', shape="ellipse", style="filled", fillcolor="#FF99FF")
        legend.node('and_legend', 'AND', shape="box", style="filled", fillcolor=gate_colors['AND'])
        legend.node('or_legend', 'OR', shape="box", style="filled", fillcolor=gate_colors['OR'])
        legend.node('xor_legend', 'XOR', shape="box", style="filled", fillcolor=gate_colors['XOR'])
    
    graph.render(filename, cleanup=True)


def part1(content):
    """
    Simulate the system of gates and wires to determine the decimal number output
    """
    start_time = time.time()
    
    # Initialize variables
    wires = {}  # Store wire values
    gates = []  # Store gate operations
    
    # Parse input
    data = parse_input(content)
    
    # Process each line
    for line in data:
        if ':' in line:  # Initial wire value
            wire, value = line.split(':')
            wires[wire.strip()] = bool(int(value.strip()))
        else:  # Gate definition
            inputs_str, output = line.split(' -> ')
            inputs = inputs_str.split()
            
            # Determine gate type
            if 'AND' in inputs:
                gate_type = 'AND'
                inputs.remove('AND')
            elif 'OR' in inputs:
                gate_type = 'OR'
                inputs.remove('OR')
            elif 'XOR' in inputs:
                gate_type = 'XOR'
                inputs.remove('XOR')
            else:
                raise ValueError(f"Unknown gate type in: {line}")
                
            gates.append((inputs, gate_type, output.strip()))
    
    # Create visualization
    create_circuit_graph(gates)

    # Simulate gates until no more changes
    while True:
        changes = 0
        for inputs, gate_type, output in gates:
            if output not in wires:  # Only evaluate if output not yet determined
                # Get input values
                input_vals = []
                for inp in inputs:
                    if inp not in wires:
                        input_vals = None
                        break
                    input_vals.append(wires[inp])
                
                if input_vals is None:
                    continue
                
                # Evaluate gate
                if gate_type == 'AND':
                    result = input_vals[0] and input_vals[1]
                elif gate_type == 'OR':
                    result = input_vals[0] or input_vals[1]
                elif gate_type == 'XOR':
                    result = input_vals[0] != input_vals[1]
                
                wires[output] = result
                changes += 1
        
        if changes == 0:  # If no changes made, we're done
            break
    
    # Get all z wires and sort them numerically by their index
    z_wires = []
    for wire in wires:
        if wire.startswith('z'):
            number = int(wire[1:])  # Extract number after 'z'
            z_wires.append((number, wire))
    z_wires.sort()  # Sort by number
    
    # Convert to binary string (1s and 0s), from least to most significant bit
    # Initialize empty binary string
    binary = ''

    # Loop through each wire (using normal variable names)
    for wire_info in z_wires:
        wire_name = wire_info[1]  # Get the wire name from the tuple
        wire_value = wires[wire_name]  # Get the wire's boolean value
        
        # Convert boolean to '1' or '0' using regular if statement
        if wire_value == True:
            bit = '1'
        else:
            bit = '0'
            
        # Add the bit to the start of the string (because least significant bit comes first)
        binary = bit + binary
    
    # Convert binary to decimal
    # Check if we have any binary digits
    if binary == '':
        result = 0
    else:
        # Convert binary string to decimal number
        # The 2 in int(binary, 2) means "convert from base 2"
        result = int(binary, 2)
    
    return {
        "value": result,
        "execution_time": time.time() - start_time
    }


def part2(content):
    """
    Simulate the system of gates and wires to determine the names of the wires that are erroneously set
    """
    start_time = time.time()
    data = parse_input(content)
    
    # Parse initial wires and gates
    wires = {}
    gates = []
    
    for line in data:
        if ':' in line:
            wire, value = line.split(':')
            wires[wire.strip()] = int(value.strip())
        elif '->' in line:
            parts = line.split(' ')
            op_index = -1
            for i, part in enumerate(parts):
                if part in ['AND', 'OR', 'XOR']:
                    op_index = i
                    break
            if op_index != -1:
                gates.append((parts[op_index-1], parts[op_index], parts[op_index+1], parts[op_index+3]))

    erroneous_gates = set()
    for in1, op, in2, out in gates:
        if op != "XOR" and out[0] == "z" and out != "z45":
            erroneous_gates.add(out)
        
        if (op == "XOR" and 
            in1[0] not in ["x", "y"] and 
            in2[0] not in ["x", "y"] and 
            out[0] not in ["z"]):
            erroneous_gates.add(out)

        if op == "AND" and "x00" not in [in1, in2]:
            for other_in1, other_op, other_in2, other_out in gates:
                if (out == other_in1 or out == other_in2) and other_op != "OR":
                    erroneous_gates.add(out)

        if op == "XOR":
            for other_in1, other_op, other_in2, other_out in gates:
                if (out == other_in1 or out == other_in2) and other_op == "OR":
                    erroneous_gates.add(out)

    # Create visualization with highlighted erroneous gates
    create_circuit_graph(gates, "logic_circuit_part2", erroneous_gates)

    result = ','.join(sorted(erroneous_gates))
    return {
        "value": result,
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

@app.command()
def main():
    try:
        input_dir = "./input/"
        results = process_directory(input_dir)
        print_results(results)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()   
    # main()
