import os
import platform
import socket
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

class AOCConfig:
    """Gestión de configuración para Advent of Code"""
    
    @staticmethod
    def get_year():
        """Obtiene el año desde .env o usa el por defecto"""
        year = os.getenv('AOC_YEAR')
        if year and year.isdigit():
            return int(year)
        else:
            print("⚠️  AOC_YEAR no configurado en .env, usando 2024 por defecto")
            return 2024
    
    @staticmethod
    def detect_environment():
        """Detecta automáticamente si estamos en home o work"""
        hostname = socket.gethostname().lower()
        username = os.getenv('USER', '').lower()
        
        # Patrones comunes para identificar trabajo vs casa
        work_indicators = [
            'work', 'office', 'corp', 'company', 'laptop', 
            'macbook-pro', 'thinkpad', 'dell', 'hp', 'empresa',
            'trabajo', 'job'
        ]
        
        home_indicators = [
            'home', 'personal', 'desktop', 'pc', 'mac', 'macbook',
            'casa', 'portatil', 'personal', 'house'
        ]
        
        # Verificar hostname
        for indicator in work_indicators:
            if indicator in hostname:
                return 'work'
        
        for indicator in home_indicators:
            if indicator in hostname:
                return 'home'
        
        # Verificar username (patrones comunes)
        if any(indicator in username for indicator in work_indicators):
            return 'work'
        if any(indicator in username for indicator in home_indicators):
            return 'home'
        
        # Por defecto, usar 'home'
        return 'home'
    
    @staticmethod
    def get_active_session():
        """Obtiene la cookie de sesión activa"""
        # Primero intentar la sesión configurada en .env
        active = os.getenv('AOC_ACTIVE_SESSION', '').lower()
        
        # Si no está configurada, detectar automáticamente
        if not active:
            active = AOCConfig.detect_environment()
            print(f"🔍 Entorno detectado automáticamente: {active}")
        
        if active == 'home':
            session = os.getenv('AOC_SESSION_HOME')
        elif active == 'work':
            session = os.getenv('AOC_SESSION_WORK')
        else:
            raise ValueError(f"Sesión activa no válida: {active}. Usa 'home' o 'work'")
        
        if not session:
            raise ValueError(f"Sesión {active} no configurada en .env")
        
        return session, active
    
    @staticmethod
    def get_session_cookie():
        """Obtiene solo la cookie de sesión (sin información del entorno)"""
        session, _ = AOCConfig.get_active_session()
        return session
    
    @staticmethod
    def get_available_sessions():
        """Lista las sesiones disponibles"""
        sessions = {}
        if os.getenv('AOC_SESSION_HOME'):
            sessions['home'] = '✅ Configurada'
        else:
            sessions['home'] = '❌ No configurada'
            
        if os.getenv('AOC_SESSION_WORK'):
            sessions['work'] = '✅ Configurada'
        else:
            sessions['work'] = '❌ No configurada'
            
        return sessions
    
    @staticmethod
    def switch_session(session_name):
        """Cambia la sesión activa (no persiste en .env)"""
        session_name = session_name.lower()
        if session_name not in ['home', 'work']:
            raise ValueError("Sesión debe ser 'home' o 'work'")
        
        os.environ['AOC_ACTIVE_SESSION'] = session_name
        print(f"✅ Sesión activa cambiada a: {session_name}")
    
    @staticmethod
    def show_status():
        """Muestra el estado actual de la configuración"""
        _, active = AOCConfig.get_active_session()
        sessions = AOCConfig.get_available_sessions()
        hostname = socket.gethostname()
        year = AOCConfig.get_year()
        
        print("🔐 Configuración de AOC:")
        print(f"   Año: {year} (desde .env)")
        print(f"   Equipo: {hostname}")
        print(f"   Sesión activa: {active} (auto-detectada)")
        for name, status in sessions.items():
            marker = "➤" if name == active else " "
            print(f"   {marker} {name}: {status}")

# Funciones de conveniencia - CORREGIDAS
def get_session():
    return AOCConfig.get_session_cookie()  # Solo retorna la cookie

def get_year():
    return AOCConfig.get_year()