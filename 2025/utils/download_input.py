import requests
import os
from pathlib import Path
from config import get_session, get_year

def download_input(day: int, year: int = None):
    """Descarga el input del día específico desde AOC"""
    if year is None:
        year = get_year()
        
    session_cookie = get_session()  # Ahora solo recibe la cookie
    
    print(f"📥 Descargando input para día {day:02d} ({year})")
    
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {'Cookie': f'session={session_cookie}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        raise ValueError(f"El día {day} del año {year} no está disponible aún")
    elif response.status_code == 400:
        raise ValueError("Cookie de sesión inválida o expirada")
    
    response.raise_for_status()
    
    return response.text.strip()

def ensure_input(day: int, year: int = None):
    """Asegura que el archivo de input existe, si no lo descarga"""
    if year is None:
        year = get_year()
        
    day_dir = Path(f"{day:02d}")
    day_dir.mkdir(exist_ok=True)
    
    input_file = day_dir / "input.txt"
    
    if not input_file.exists() or input_file.stat().st_size == 0:
        try:
            input_data = download_input(day, year)
            input_file.write_text(input_data)
            print(f"✅ Input del día {day:02d} descargado")
            return True
        except Exception as e:
            print(f"❌ Error descargando input: {e}")
            # Crear archivo vacío si falla la descarga
            input_file.touch()
            return False
    return True