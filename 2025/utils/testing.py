from colorama import Fore, Style
import time

def run_tests(part1_func, part2_func, example_file="example.txt"):
    """Run tests with example file"""
    try:
        with open(example_file, 'r') as f:
            example_data = f.read().strip()
        
        print(f"{Fore.CYAN}🧪 Running tests with example...")
        
        # Test part 1
        start_time = time.time()
        try:
            result1 = part1_func(example_data)
            elapsed1 = time.time() - start_time
            print(f"{Fore.GREEN}✅ Part 1 (example): {result1} ({elapsed1:.4f}s)")
        except Exception as e:
            print(f"{Fore.RED}❌ Part 1 failed: {e}")
        
        # Test part 2
        start_time = time.time()
        try:
            result2 = part2_func(example_data)
            elapsed2 = time.time() - start_time
            print(f"{Fore.GREEN}✅ Part 2 (example): {result2} ({elapsed2:.4f}s)")
        except Exception as e:
            print(f"{Fore.RED}❌ Part 2 failed: {e}")
            
    except FileNotFoundError:
        print(f"{Fore.YELLOW}📝 Example file {example_file} not found")
    except Exception as e:
        print(f"{Fore.RED}❌ Error in tests: {e}")

def validate_solution(actual, expected, part_name):
    """Validate solution against expected result"""
    if expected is None:
        return f"{Fore.YELLOW}⚠️  {part_name}: {actual} (no expected value)"
    
    if actual == expected:
        return f"{Fore.GREEN}✅ {part_name}: {actual} (matches expected)"
    else:
        return f"{Fore.RED}❌ {part_name}: {actual} (expected {expected})"