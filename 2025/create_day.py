import sys
import shutil
from pathlib import Path
from utils.download_input import ensure_input
from config import AOCConfig

def create_day(day: int, year: int = None):
    """Create structure for a new day with enhanced testing"""
    if year is None:
        year = AOCConfig.get_year()
        
    day_dir = Path(f"{day:02d}")
    day_dir.mkdir(exist_ok=True)
    
    # Show active session
    AOCConfig.show_status()
    
    # Copy template files
    template_dir = Path("template")
    
    # Copy and customize solution.py
    solution_template = template_dir / "solution.py"
    if solution_template.exists():
        with open(solution_template, 'r') as f:
            solution_content = f.read()
        
        # Replace placeholders
        solution_content = solution_content.replace('DayXX', f'Day{day:02d}')
        solution_content = solution_content.replace('dayXX', f'day{day:02d}')
        
        with open(day_dir / "solution.py", 'w') as f:
            f.write(solution_content)
    
    # Copy and customize test_solution.py
    test_template = template_dir / "test_solution.py"
    if test_template.exists():
        with open(test_template, 'r') as f:
            test_content = f.read()
        
        test_content = test_content.replace('TestDayXX', f'TestDay{day:02d}')
        test_content = test_content.replace('DayXX', f'Day{day:02d}')
        
        with open(day_dir / "test_solution.py", 'w') as f:
            f.write(test_content)
    
    # Copy test_inputs.py
    test_inputs_template = template_dir / "test_inputs.py"
    if test_inputs_template.exists():
        shutil.copy(test_inputs_template, day_dir / "test_inputs.py")
    
    # Create empty example file
    (day_dir / "example.txt").touch()
    
    # Create __init__.py to make it a package
    (day_dir / "__init__.py").touch()
    
    # Download input
    success = ensure_input(day, year)
    
    print(f"\n{'-'*60}")
    print(f"✅ Day {day:02d} structure created in {day_dir}/")
    print(f"📁 Files created:")
    print(f"   - solution.py (main solution file)")
    print(f"   - test_solution.py (unit tests)")
    print(f"   - test_inputs.py (test expected results)")
    print(f"   - example.txt (for example input)")
    print(f"   - input.txt ({'✅ downloaded' if success else '❌ download failed'})")
    print(f"   - __init__.py (package marker)")
    print(f"\n🎯 Next steps:")
    print(f"   1. Add example input to example.txt")
    print(f"   2. Update expected results in test_inputs.py")
    print(f"   3. Implement solution in solution.py")
    print(f"   4. Run: py {day_dir}/solution.py")
    print(f"   5. Test: py -m unittest {day_dir}/test_solution.py")
    print(f"{'-'*60}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py create_day.py <day>")
        sys.exit(1)
    
    try:
        day_num = int(sys.argv[1])
        create_day(day_num)
    except ValueError:
        print("Day must be a number")
        sys.exit(1)