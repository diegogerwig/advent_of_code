from pathlib import Path

import typer

app = typer.Typer()


def read_input_file(input_file_path: str) -> list[str]:
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


def parse_gate(gate_str: str) -> tuple[str, str, str, str]:
    parts = gate_str.split(" ")

    return (parts[0], parts[1], parts[2], parts[4])


def parse(data: list[str]) -> tuple[dict[str, int], list[tuple[str, str, str, str]]]:
    idx = data.index("")
    wires = {line.split(": ")[0]: int(line.split(": ")[1]) for line in data[:idx]}
    gates = [parse_gate(line) for line in data[idx + 1 :]]

    return wires, gates


def simulate(
    wires: dict[str, int], gates: list[tuple[str, str, str, str]]
) -> dict[str, int]:
    all_wires = {g[0] for g in gates} | {g[2] for g in gates} | {g[3] for g in gates}
    while all_wires != set(wires.keys()):
        for g in gates:
            if g[0] in wires and g[2] in wires:
                match g[1]:
                    case "XOR":
                        wires[g[3]] = wires[g[0]] ^ wires[g[2]]
                    case "OR":
                        wires[g[3]] = wires[g[0]] | wires[g[2]]
                    case "AND":
                        wires[g[3]] = wires[g[0]] & wires[g[2]]
    return wires


def solve_1(data: list[str]) -> int:
    wires, gates = parse(data)
    wires = simulate(wires, gates)
    z_wires = [w for w in wires if w[0] == "z"]
    z_wires = list(sorted(z_wires, key=lambda x: int(x[1:]), reverse=True))
    values = [str(wires[w]) for w in z_wires]
    return int("".join(values), base=2)


def solve_2(data: list[str]) -> str:
    wires, gates = parse(data)
    erronous_gates = set()
    for in1, op, in2, out in gates:
        if op != "XOR" and out[0] == "z" and out != "z45":
            erronous_gates.add(out)
        if (
            op == "XOR"
            and in1[0] not in ["x", "y"]
            and in2[0] not in ["x", "y"]
            and out[0] not in ["z"]
        ):
            erronous_gates.add(out)

        if op == "AND" and "x00" not in [in1, in2]:
            for subin1, subop, subin2, subout in gates:
                if (out == subin1 or out == subin2) and subop != "OR":
                    erronous_gates.add(out)

        if op == "XOR":
            for subin1, subop, subin2, subout in gates:
                if (out == subin1 or out == subin2) and subop == "OR":
                    erronous_gates.add(out)
    return ",".join(sorted(erronous_gates))


@app.command()
def part_1(input_file: str = "input.txt"):
    data = read_input_file(input_file)
    print(f"The number is {solve_1(data)}")


@app.command()
def part_2(input_file: str = "input.txt"):
    data = read_input_file(input_file)
    print(f"The names of the wires are {solve_2(data)}")


if __name__ == "__main__":
    app()
