# 📊 Oracle ↔ PostgresPro Data Comparator

Модульный скрипт для потокового сравнения больших таблиц (5M+ строк) между Oracle и PostgreSQL/PostgresPro.

## 🚀 Возможности

- **Сравнение больших объёмов данных** — оптимизирован для таблиц с 5+ миллионами строк
- **Разные схемы** — поддержка раздельных имён схем в Oracle и PostgreSQL
- **Keyset Pagination** — быстрая постраничная выборка без деградации производительности (без OFFSET)
- **Авто-поиск первичного ключа** — автоматическое определение PK для навигации по данным
- **Визуализация результатов** — интерактивные дашборды с использованием seaborn/matplotlib
- **Безопасность** — bind-variables, таймауты соединений, graceful error handling
- **Параллельная выборка** — одновременная загрузка данных из Oracle и PostgreSQL через ThreadPoolExecutor
- **Экспорт отчётов** — CSV, HTML и JSON форматы результатов сравнения

## 📋 Требования

- Python 3.8+
- Jupyter Notebook / JupyterLab

### Библиотеки

```bash
pip install pandas numpy oracledb psycopg seaborn matplotlib tqdm
```

### Установка драйверов

- **Oracle**: `oracledb` работает в "thin" режиме без дополнительных зависимостей
- **PostgreSQL**: `psycopg` v3 требует Python 3.8+

## ⚙️ Конфигурация

Перед запуском настройте параметры подключения через переменные окружения или напрямую в коде:

```python
# Oracle DB
ORA_CFG = {
    "user": os.getenv("ORA_USER", "your_user"),
    "password": os.getenv("ORA_PASS", "your_password"),
    "dsn": os.getenv("ORA_DSN", "host:port/service")
}

# PostgreSQL
PG_CFG = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
    "dbname": os.getenv("PG_DB", "your_db"),
    "user": os.getenv("PG_USER", "your_user"),
    "password": os.getenv("PG_PASS", "your_password")
}

# Параметры сравнения
SCHEMA_ORA = os.getenv("SCHEMA_ORA", "YOUR_SCHEMA")
SCHEMA_PG = os.getenv("SCHEMA_PG", "public")
TABLE_NAME = os.getenv("TABLE_NAME", "YOUR_TABLE")
```

## 🏃 Запуск

1. Откройте `racle_pg_comparator.ipynb` в Jupyter
2. Настройте конфигурацию в ячейке `if __name__ == "__main__":`
3. Выполните все ячейки последовательно
4. Результаты сравнения, дашборд и отчёты будут сгенерированы автоматически

### Структура ноутбука

| Ячейка | Тип | Описание |
|--------|-----|----------|
| 0 | Markdown | Заголовок и описание архитектуры |
| 1 | Code | Импорт библиотек (`pandas`, `numpy`, `oracledb`, `psycopg`, `seaborn`, `matplotlib`, `tqdm`) |
| 2 | Code | Настройка логирования (файл + консоль), классы исключений |
| 3 | Code | Контекстные менеджеры `_ora_conn()` и `_pg_conn()` для безопасных соединений |
| 4 | Code | Функция `_resolve_pk()` для авто-поиска PRIMARY KEY |
| 5 | Code | Keyset Pagination: `_keyset_query()` и `_fetch_batch_keyset()` для эффективной выборки |
| 6 | Code | Инкрементальное сравнение: `_row_hash()`, `_compare_batch()`, `_stream_compare()` |
| 7 | Code | Визуализация: `_plot_dashboard()` и `_print_summary()` |
| 8 | Code | Экспорт отчётов: `_export_report()` (CSV, HTML, JSON) |
| 9 | Code | Пример запуска с конфигурацией |
| 10 | Markdown | Документация и советы |

## 📊 Архитектура

```
Подключение → Метаданные → Keyset Pagination → Инкрементальное сравнение → Dashboard
```

| Аспект | Реализация |
|--------|------------|
| **Разные схемы** | `schema_ora` и `schema_pg` передаются раздельно |
| **5 млн строк** | Пакетная обработка по 1000-2000 строк + Keyset Pagination, `tqdm` для прогресса |
| **Параллелизм** | `ThreadPoolExecutor(max_workers=2)` для одновременной выборки из Oracle и PostgreSQL |
| **Безопасность** | Bind-variables, `call_timeout=60s`, try/finally для закрытия соединений |

## 💡 Рекомендации

### Оптимизация производительности

| Параметр | Рекомендация |
|----------|-------------|
| `batch_size` | 1000–5000 (баланс памяти/скорости) |
| `max_workers` | Не более 4–8 (избегайте перегрузки БД) |
| Индексы | Убедитесь, что PK проиндексирован в обеих БД |

### Безопасность

- Никогда не храните пароли в коде. Используйте переменные окружения.
- Для продакшена: HashiCorp Vault, AWS Secrets Manager или Azure Key Vault.

### Отладка

```python
_logger.setLevel(_log.DEBUG)
with _ora_conn(ORA_CFG) as c:
    print(c.version)
```

## 📊 Визуализация результатов

После выполнения сравнения строится дашборд с использованием seaborn/matplotlib:

### Дашборд (2x2 сетка)

1. **Distribution of Rows** — круговая диаграмма распределения строк (Match, Mismatch, Only Oracle, Only Postgres)
2. **Absolute Counts** — горизонтальная столбчатая диаграмма абсолютных значений
3. **Performance Metrics** — таблица метрик (Total Processed, Mismatches, Rows/sec, Time)
4. **Sample Mismatches** — первые 10 несовпадений с первичными ключами

## 📄 Экспорт результатов

Функция `_export_report()` сохраняет результаты в трёх форматах:

| Формат | Описание |
|--------|----------|
| **CSV** | Таблица несовпадений с расширенными первичными ключами |
| **HTML** | Интерактивный отчёт с метриками и примерами несовпадений |
| **JSON** | Полная статистика сравнения для программной обработки |

Отчёты сохраняются в директорию `./reports/` с временной меткой в имени файла.

## 🔍 Проверка типов данных

Скрипт автоматически обрабатывает и сравнивает следующие типы данных:

| Тип данных | Обработка | Особенности |
|------------|-----------|-------------|
| **Числовые** (INT, NUMBER, FLOAT) | Сравнение с точностью до 6 знаков после запятой | NaN значения считаются равными |
| **Строки** (VARCHAR, TEXT, CHAR) | Побайтовое сравнение | Чувствительно к регистру |
| **Даты и время** (DATE, TIMESTAMP) | Преобразование в строку перед хешированием | Требуют нормализации часовых поясов |
| **NULL значения** | Считаются равными друг другу | `NULL == NULL` возвращает `True` |

## 📈 Примеры использования результатов

Функция `_stream_compare()` возвращает словарь с метриками:

```python
results = _stream_compare(...)

# Доступные метрики
print(results["total_processed"])     # Всего обработано строк
print(results["total_matches"])       # Совпавшие строки
print(results["total_mismatches"])    # Несовпадающие строки
print(results["only_in_oracle"])      # Только в Oracle
print(results["only_in_postgres"])    # Только в PostgreSQL
print(results["timing"]["rows_per_second"])  # Скорость обработки
```

## 📄 Лицензия

MIT
