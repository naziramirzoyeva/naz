import psycopg2
import csv
from config import load_config

def insert_from_csv(file_path):
    
    config = load_config()
    names = []
    phones = []
    
    try:

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    names.append(row[0])
                    phones.append(row[1])
        
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))
            print(f"✅ Данные из {file_path} обработаны через процедуру.")
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")

def add_or_update_contact(name, phone):
    """Задача 2: Использование процедуры Upsert"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
            print(f"✅ Операция для {name} выполнена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def search_contacts(pattern):
    """Задача 3: Поиск через SQL-функцию"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
                rows = cur.fetchall()
                for row in rows:
                    print(f"Имя: {row[0]} | Тел: {row[1]}")
    except Exception as e:
        print(f"❌ Ошибка поиска: {e}")

def get_paginated(limit, offset):
    """Задача 4: Пагинация через SQL-функцию"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s::integer, %s::integer);", (limit, offset))
                rows = cur.fetchall()
                print(f"\n--- Страница (limit {limit}, offset {offset}) ---")
                for row in rows:
                    print(f"Имя: {row[0]} | Тел: {row[1]}")
    except Exception as e:
        print(f"❌ Ошибка пагинации: {e}")

def delete_contact(identifier):
    """Задача 5: Удаление через процедуру"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s);", (identifier,))
            print(f"✅ Запрос на удаление '{identifier}' выполнен.")
    except Exception as e:
        print(f"❌ Ошибка удаления: {e}")

if __name__ == '__main__':

    print("1. Массовая загрузка...")
    insert_from_csv('contacts.csv')
    
    print("\n2. Добавление/Обновление...")
    add_or_update_contact('Natasha', '+77752233522')
    
    print("\n3. Поиск (по части 'Alice')...")
    search_contacts('Alice')
    
    print("\n4. Пагинация (первые 5 записей)...")
    get_paginated(5, 0)
    
    print("\n5. Удаление...")
    delete_contact('Natasha')