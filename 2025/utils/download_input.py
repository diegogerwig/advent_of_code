import requests
import os
from pathlib import Path

def download_input(day: int, year: int = 2025):
    """Descarga el input del día específico desde AOC"""
    # Necesitas configurar tu session cookie de AOC
    session_cookie = os.getenv('AOC_SESSION')
    if not session_cookie:
        raise ValueError("Configura la variable de entorno AOC_SESSION")
    
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {'Cookie': f'session={session_cookie}'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.text

def ensure_input(day: int, year: int = 2025):
    """Asegura que el archivo de input existe, si no lo descarga"""
    day_dir = Path(f"day{day:02d}")
    input_file = day_dir / "input.txt"
    
    if not input_file.exists():
        input_data = download_input(day, year)
        input_file.write_text(input_data)
        print(f"Input del día {day} descargado")