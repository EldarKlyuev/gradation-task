#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации декоратора и контекстного менеджера
"""

from utils.decorators import factorial, long_task
from utils.context_managers import FileLogger, example_file_usage
import time


def test_decorator():
    """Тестирование декоратора для измерения времени"""
    print("=== Тестирование декоратора measure_time ===")
    
    # Тест вычисления факториала
    print("\n1. Вычисление факториала 10:")
    result = factorial(10)
    print(f"Результат: {result}")
    
    # Тест длительной задачи
    print("\n2. Длительная задача (2 секунды):")
    result = long_task(2)
    print(f"Результат: {result}")


def test_context_manager():
    """Тестирование контекстного менеджера"""
    print("\n=== Тестирование контекстного менеджера FileLogger ===")
    
    # Тест записи в файл
    print("\n1. Запись в файл с автоматическим логированием времени:")
    with FileLogger('test_output.log', 'w') as file:
        file.write("Первая строка тестового файла\n")
        file.write("Вторая строка тестового файла\n")
        file.write("Третья строка тестового файла\n")
    
    print("Файл закрыт автоматически. Проверьте содержимое test_output.log")
    
    # Тест функции example_file_usage
    print("\n2. Использование функции example_file_usage:")
    example_file_usage()
    print("Проверьте содержимое example.log")


def test_async_functions():
    """Тестирование асинхронных функций"""
    print("\n=== Тестирование асинхронных функций ===")
    
    import asyncio
    from fastapi_app.main import fetch_external_api
    
    async def test_external_api():
        """Тест асинхронного запроса к внешнему API"""
        try:
            print("Выполнение асинхронного запроса к JSONPlaceholder API...")
            result = await fetch_external_api("https://jsonplaceholder.typicode.com/posts/1")
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    # Запуск асинхронной функции
    asyncio.run(test_external_api())


def main():
    """Главная функция для запуска всех тестов"""
    print("Запуск тестов для Gradation Project")
    print("=" * 50)
    
    # Тест декоратора
    test_decorator()
    
    # Тест контекстного менеджера
    test_context_manager()
    
    # Тест асинхронных функций
    test_async_functions()
    
    print("\n" + "=" * 50)
    print("Все тесты завершены!")
    print("\nСозданные файлы:")
    print("- test_output.log - файл с логами времени")
    print("- example.log - файл с примером использования")


if __name__ == "__main__":
    main() 