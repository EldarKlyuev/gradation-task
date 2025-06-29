import time
import functools
from typing import Callable, Any


def measure_time(func: Callable) -> Callable:
    """
    Декоратор для измерения времени выполнения функции.
    Выводит время выполнения в консоль.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {execution_time:.4f} секунд")
        return result
    return wrapper


# Пример использования декоратора
@measure_time
def factorial(n: int) -> int:
    """Вычисляет факториал числа n"""
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@measure_time
def long_task(seconds: int) -> str:
    """Длительная задача с использованием time.sleep"""
    import time
    time.sleep(seconds)
    return f"Задача выполнена за {seconds} секунд" 