"""
Точка входа в игру DreamCatcher.
Создаёт экземпляр приложения и запускает его.
"""
from src.app import DreamCatcherApp

if __name__ == "__main__":
    app = DreamCatcherApp()
    app.run()