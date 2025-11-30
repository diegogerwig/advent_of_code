#!/usr/bin/env python3
"""
Gestor de sesiones para Advent of Code
"""

import os
from config import AOCConfig

def main():
    """Menú principal del gestor de sesiones"""
    print("🔐 Gestor de Sesiones - Advent of Code")
    print()
    
    while True:
        AOCConfig.show_status()
        print()
        print("Opciones:")
        print("  1. Cambiar a sesión HOME")
        print("  2. Cambiar a sesión WORK") 
        print("  3. Verificar sesiones")
        print("  4. Mostrar info del sistema")
        print("  5. Salir")
        
        choice = input("\nSelecciona una opción (1-5): ").strip()
        
        if choice == '1':
            AOCConfig.switch_session('home')
        elif choice == '2':
            AOCConfig.switch_session('work')
        elif choice == '3':
            verify_sessions()
        elif choice == '4':
            show_system_info()
        elif choice == '5':
            print("¡Hasta luego! 🎄")
            break
        else:
            print("❌ Opción no válida")
        
        print()

def verify_sessions():
    """Verifica que las sesiones sean válidas"""
    import requests
    from config import AOCConfig
    
    print("🔍 Verificando sesiones...")
    
    for session_name in ['home', 'work']:
        cookie = os.getenv(f'AOC_SESSION_{session_name.upper()}')
        if not cookie:
            print(f"❌ {session_name}: No configurada")
            continue
            
        try:
            response = requests.get(
                f"https://adventofcode.com/{AOCConfig.get_year()}/auth/login",
                cookies={'session': cookie},
                allow_redirects=False,
                timeout=10
            )
            
            if response.status_code == 302 and f'/{AOCConfig.get_year()}' in response.headers.get('Location', ''):
                print(f"✅ {session_name}: Válida")
            else:
                print(f"❌ {session_name}: Inválida o expirada")
                
        except Exception as e:
            print(f"❌ {session_name}: Error - {e}")

def show_system_info():
    """Muestra información del sistema para debugging"""
    import socket
    import platform
    
    print("🖥️  Información del sistema:")
    print(f"   Hostname: {socket.gethostname()}")
    print(f"   SO: {platform.system()} {platform.release()}")
    print(f"   Usuario: {os.getenv('USER', 'No detectado')}")
    print(f"   Entorno detectado: {AOCConfig.detect_environment()}")

if __name__ == "__main__":
    main()