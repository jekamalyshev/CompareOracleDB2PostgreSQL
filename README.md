# 📊 Oracle ↔ PostgresPro Data Comparator

Модульный скрипт для потокового сравнения больших таблиц (5M+ строк) между Oracle и PostgreSQL/PostgresPro.

## 🚀 Возможности

- **Сравнение больших объёмов данных** — оптимизирован для таблиц с 5+ миллионами строк
- **Разные схемы** — поддержка раздельных имён схем в Oracle и PostgreSQL
- **Keyset Pagination** — быстрая постраничная выборка без деградации производительности
- **Авто-поиск первичного ключа** — автоматическое определение PK для навигации по данным
- **Визуализация результатов** — интерактивные дашборды с использованием seaborn/matplotlib
- **Безопасность** — bind-variables, таймауты соединений, graceful error handling
- **Опциональные фильтры** — гибкая фильтрация данных через параметризованные WHERE-условия

## 📋 Требования

- Python 3.8+
- Jupyter Notebook / JupyterLab

### Библиотеки

```bash
pip install pandas numpy oracledb psycopg seaborn matplotlib tqdm
```

## ⚙️ Конфигурация

Перед запуском настройте параметры подключения:

```python
# Oracle DB
ORA_CONFIG = {
    "user": "your_user",
    "password": "your_password",
    "dsn": "host:port/service_name"
}

# PostgreSQL
PG_CONFIG = {
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": 5432,
    "dbname": "your_database"
}

# Параметры сравнения
TABLE_NAME = "your_table"
SCHEMA_ORA = "oracle_schema"
SCHEMA_PG = "postgres_schema"
KEY_COLUMN = "id"  # Первичный ключ
CHUNK_SIZE = 100_000  # Строк за одну итерацию
```

## 🏃 Запуск

1. Откройте `racle_pg_comparator.ipynb` в Jupyter
2. Настройте конфигурацию в начале ноутбука
3. Последовательно выполните ячейки 1–8
4. Запустите ячейку 9 для начала сравнения

## 📊 Архитектура

```
Подключение → Метаданные → Keyset Pagination → Инкрементальное сравнение → Dashboard
```

| Аспект | Реализация |
|--------|------------|
| **Разные схемы** | `schema_ora` и `schema_pg` передаются раздельно |
| **5 млн строк** | `chunk=100_000` + `Keyset Pagination`, `tqdm` для прогресса |
| **Фильтры** | Опциональная параметризация `WHERE`-условий |
| **Безопасность** | Bind-variables, `call_timeout=60s`, try/finally |

## 💡 Рекомендации

- Для таблиц >10M строк увеличьте `chunk` до 200 000
- Убедитесь, что `key_col` имеет **B-Tree индекс** в обеих БД
- Используйте фильтры для сравнения подмножеств данных (например, `WHERE year=2024`)

## 🛠 Расширение

Архитектура открыта для расширений:
- Добавьте `export_to_parquet(report)` для сохранения отчётов
- Замените стратегию сравнения на хэш-валидацию
- Интегрируйте с CI/CD для автоматической валидации миграций

## 📄 Лицензия

MIT