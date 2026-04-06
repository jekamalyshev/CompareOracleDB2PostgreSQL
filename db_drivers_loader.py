"""
Модуль для гибкого импорта oracledb и psycopg.
Логика: пытается импортировать из текущего окружения. Если не получается,
автоматически находит пакеты в системном (глобальном) Python и добавляет их в path.
"""

import sys
import subprocess
import os

def get_system_python_paths():
    """
    Получает пути к сайт-пакетам системного Python (не текущего venv/conda).
    """
    # Используем 'python' (системный) или явно указываем путь, если известно
    # Команда возвращает список путей, разделенных ос-специфичным разделителем
    cmd = [sys.executable.replace('python.exe', 'python').replace('python3.exe', 'python'), "-c", 
           "import sys; print(sys.path[-1] if len(sys.path) > 1 else '')"]
    
    # Более надежный способ: запустить чистый системный python, если он доступен в PATH как 'python'
    # Но так как мы внутри процесса, попробуем найти 'python' отдельно от sys.executable
    system_python = 'python'
    
    try:
        # Запрашиваем у системного python его site-packages
        result = subprocess.run(
            [system_python, "-c", "import site; print(site.getsitepackages()[0])"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            system_site_packages = result.stdout.strip()
            return [system_site_packages]
    except Exception:
        pass

    # Фоллбэк: если не удалось получить через subprocess, пробуем угадать пути
    # Обычно системные пакеты лежат рядом с исполняемым файлом или в стандартных путях OS
    return []

def ensure_import(module_name, import_name=None):
    """
    Пытается импортировать модуль. Если не выходит, ищет его в системном Python.
    """
    if import_name is None:
        import_name = module_name

    try:
        # 1. Попытка импорта из текущего окружения
        module = __import__(module_name, fromlist=[import_name])
        return getattr(module, import_name) if hasattr(module, import_name) else module
    except ImportError:
        pass

    # 2. Если не нашли, пытаемся добавить пути системного Python
    system_paths = get_system_python_paths()
    
    # Добавляем пути в начало sys.path, чтобы они имели приоритет при следующем импорте
    for path in system_paths:
        if path and path not in sys.path:
            sys.path.insert(1, path) # Вставляем после '' (текущей директории)

    # Очищаем кэш импортов, если вдруг что-то частично загрузилось
    if module_name in sys.modules:
        del sys.modules[module_name]
        
    # Повторная попытка импорта
    try:
        module = __import__(module_name, fromlist=[import_name])
        return getattr(module, import_name) if hasattr(module, import_name) else module
    except ImportError as e:
        raise ImportError(
            f"Не удалось импортировать {module_name} ни из текущего окружения, "
            f"ни из системного Python. Ошибка: {e}"
        )

# --- ИСПОЛЬЗОВАНИЕ ---

# Импорт oracledb как _oracledb
_oracledb = ensure_import('oracledb')

# Импорт psycopg (в версии 3 основной модуль называется psycopg) как _psycopg
# Примечание: в psycopg3 классы часто доступны напрямую из модуля psycopg
_psycopg = ensure_import('psycopg')

print(f"Успешно загружен oracledb из: {_oracledb.__file__}")
print(f"Успешно загружен psycopg из: {_psycopg.__file__}")

# Пример использования (раскомментировать для проверки)
# conn = _oracledb.connect(...)
# conn = _psycopg.connect(...)
