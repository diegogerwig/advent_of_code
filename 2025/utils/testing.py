def run_tests(part1_func, part2_func, example_file="example.txt"):
    """Ejecuta tests con el archivo de ejemplo"""
    try:
        with open(example_file, 'r') as f:
            example_data = f.read().strip()
        
        print("=== Ejecutando tests con ejemplo ===")
        
        # Test parte 1
        try:
            result1 = part1_func(example_data)
            print(f"Parte 1 (ejemplo): {result1}")
        except Exception as e:
            print(f"Parte 1 falló: {e}")
        
        # Test parte 2
        try:
            result2 = part2_func(example_data)
            print(f"Parte 2 (ejemplo): {result2}")
        except Exception as e:
            print(f"Parte 2 falló: {e}")
            
    except FileNotFoundError:
        print(f"Archivo de ejemplo {example_file} no encontrado")