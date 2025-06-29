import time
from datetime import datetime
from typing import TextIO, Optional


class FileLogger:
    """
    Контекстный менеджер для работы с файлами.
    Автоматически записывает время открытия и закрытия файла.
    """
    
    def __init__(self, filename: str, mode: str = 'a'):
        self.filename = filename
        self.mode = mode
        self.file: Optional[TextIO] = None
    
    def __enter__(self) -> TextIO:
        """Открывает файл и записывает время открытия"""
        self.file = open(self.filename, self.mode, encoding='utf-8')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file.write(f"[{current_time}] Файл открыт\n")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Закрывает файл и записывает время закрытия"""
        if self.file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.file.write(f"[{current_time}] Файл закрыт\n")
            self.file.close()


# Пример использования контекстного менеджера
def example_file_usage():
    """Пример использования контекстного менеджера FileLogger"""
    with FileLogger('example.log', 'w') as file:
        file.write("Это тестовое сообщение\n")
        file.write("Еще одно сообщение\n")