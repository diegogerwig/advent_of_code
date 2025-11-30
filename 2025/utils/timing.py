import time
from functools import wraps

def timer(func):
    """Decorador para medir el tiempo de ejecución"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Tiempo de {func.__name__}: {end_time - start_time:.4f} segundos")
        return result
    return wrapper