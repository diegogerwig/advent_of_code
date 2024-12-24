from graphviz import Digraph

ops = { "AND": 0, "OR": 1, "XOR": 2 }
funcs = [lambda a, b: a & b, lambda a, b: a | b, lambda a, b: a ^ b]

def solve(wires, todos):
    while todos:
        new = []
        for a, op, b, c in todos:
            if a in wires and b in wires:
                wires[c] = funcs[ops[op]](wires[a], wires[b])
            else:
                new.append((a, op, b, c))
        todos = new

def zs_as_int(wires):
    zs = [(k, v) for k, v in wires.items() if k.startswith('z')]
    zs = sorted(zs, reverse=True)
    zs = [z[1] for z in zs]
    return int("".join(map(str, zs)), 2)

input = open("./input/input_I.txt").read().strip().split("\n\n")
wires = { wire: int(val) for line in input[0].split("\n") for wire, val in [line.split(": ")] }
todos = [(a, op, b, c) for line in input[1].split("\n") for a, op, b, _, c in [line.split()]]

solve(wires, todos)
one = zs_as_int(wires)

# Solve part two visually
graph = Digraph(format="png")
graph.attr(rankdir="UD")

# Add wires and gates to the graph
for a, op, b, c in todos:
    graph.node(a, a, shape="ellipse")
    graph.node(b, b, shape="ellipse")
    graph.node(c, c, shape="ellipse")
    
    op_node = f"{a}_{b}_{op}"
    graph.node(op_node, op, shape="box")
    
    graph.edge(a, op_node)
    graph.edge(b, op_node)
    graph.edge(op_node, c)

graph.render("logic_operations_flow", cleanup=True)

# Find the swaps by looking at the graph:
swaps = [
    "z07", "gmt",
    "z18", "dmn",
    "z35", "cfk",
    "cbj", "qjj",
]
two = ",".join(sorted(swaps))

print(f"Part one: {one}")
print(f"Part two: {two}")
