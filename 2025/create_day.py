import sys
from pathlib import Path
from utils.download_input import ensure_input
from config import AOCConfig

def create_day(day: int, year: int = None):
    """Crea la estructura para un nuevo día"""
    if year is None:
        year = AOCConfig.get_year()
        
    day_dir = Path(f"{day:02d}")  # Cambiado de "day{day:02d}" a "{day:02d}"
    day_dir.mkdir(exist_ok=True)
    
    # Mostrar sesión activa
    AOCConfig.show_status()
    
    # Crear solution.py
    solution_content = f'''from pathlib import Path
from utils.timing import timer
from utils.testing import run_tests

@timer
def part1(input_data: str):
    """Solución para la parte 1 del día {day}"""
    lines = input_data.strip().split('\\n')
    # Implementar solución
    result = 0
    return result

@timer
def part2(input_data: str):
    """Solución para la parte 2 del día {day}"""
    lines = input_data.strip().split('\\n')
    # Implementar solución
    result = 0
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
        
        print("\\\\n=== Solución con input real ===")
        result1 = part1(input_data)
        print(f"✅ Parte 1: {{result1}}")
        
        result2 = part2(input_data)
        print(f"✅ Parte 2: {{result2}}")

if __name__ == "__main__":
    solve()
'''
    
    with open(day_dir / "solution.py", "w") as f:
        f.write(solution_content)
    
    # Crear test_solution.py
    test_content = f'''import unittest
from solution import part1, part2

class TestDay{day:02d}(unittest.TestCase):
    
    def setUp(self):
        self.example_data = """"""
    
    def test_part1_example(self):
        # TODO: Configurar test cuando tengas el ejemplo
        # self.assertEqual(part1(self.example_data), expected_value)
        pass
    
    def test_part2_example(self):
        # TODO: Configurar test cuando tengas el ejemplo
        # self.assertEqual(part2(self.example_data), expected_value)
        pass

if __name__ == '__main__':
    unittest.main()
'''
    
    with open(day_dir / "test_solution.py", "w") as f:
        f.write(test_content)
    
    # Crear archivos vacíos
    (day_dir / "__init__.py").touch()
    (day_dir / "example.txt").touch()
    
    # Descargar input automáticamente
    success = ensure_input(day, year)
    
    print(f"✅ Estructura del día {day:02d} creada en {day_dir}/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python create_day.py <día>")
        sys.exit(1)
    
    try:
        day_num = int(sys.argv[1])
        create_day(day_num)
    except ValueError:
        print("El día debe ser un número")
        sys.exit(1)