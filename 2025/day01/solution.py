from pathlib import Path
from utils.timing import timer
from utils.testing import run_tests

@timer
def part1(input_data: str):
    """Solución para la parte 1 del día 1"""
    lines = input_data.strip().split('\n')
    # Implementar solución
    result = 0
    print(f"Parte 1: {result}")
    return result

@timer
def part2(input_data: str):
    """Solución para la parte 2 del día 1"""
    lines = input_data.strip().split('\n')
    # Implementar solución
    result = 0
    print(f"Parte 2: {result}")
    return result

def solve():
    """Función principal que resuelve el día completo"""
    day_dir = Path(__file__).parent
    input_file = day_dir / "input.txt"
    example_file = day_dir / "example.txt"
    
    # Ejecutar tests primero con el ejemplo
    if example_file.exists():
        print("=== Ejecutando tests con ejemplo ===")
        run_tests(part1, part2, str(example_file))
    
    # Resolver con input real
    if input_file.exists():
        with open(input_file, 'r') as f:
            input_data = f.read().strip()
        
        print("\\n=== Solución con input real ===")
        result1 = part1(input_data)
        print(f"✅ Parte 1: {result1}")
        
        result2 = part2(input_data)
        print(f"✅ Parte 2: {result2}")

if __name__ == "__main__":
    solve()
