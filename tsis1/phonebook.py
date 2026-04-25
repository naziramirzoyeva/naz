import psycopg2
import json
from config import load_config


# соединение с базой
def get_conn():
    return psycopg2.connect(**load_config())


# поиск 
def search_contacts():
    query = input("Search: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s);", (query,))
            rows = cur.fetchall()
            for r in rows:
                print(r)


# filter by group
def filter_by_group():
    group = input("Group: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, c.email, g.name
                FROM contacts c
                JOIN groups g ON c.group_id = g.id
                WHERE g.name = %s;
            """, (group,))
            for row in cur.fetchall():
                print(row)


# sort
def sort_contacts():
    field = input("Sort by (name/birthday/email): ")

    if field not in ["name", "birthday", "email"]:
        print("Invalid field")
        return

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM contacts ORDER BY {field};")
            for row in cur.fetchall():
                print(row)


# add phone
def add_phone():
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s,%s,%s);", (name, phone, ptype))
    print("Phone added")


# move to group
def move_to_group():
    name = input("Name: ")
    group = input("New group: ")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s,%s);", (name, group))
    print("Moved to group")


# pagination
def pagination_loop():
    limit = 3
    offset = 0 

    #бесконечный цикл чтобы выходило меню
    while True:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s,%s);",
                    (limit, offset)
                )
                rows = cur.fetchall()
                print("\n--- PAGE ---")
                for r in rows:
                    print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break


# export json
def export_json():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                LEFT JOIN phones p ON p.contact_id = c.id;
            """)
             #берем все данные с базы  
            data = cur.fetchall() #сохранили

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=str) #запись данных в json файл

    print("Exported to contacts.json")


# import json
def import_json():
    try:
        with open("contacts.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("No contacts.json file")
        return

    with get_conn() as conn:
        with conn.cursor() as cur:
            for row in data:
                name, email, birthday, group, phone, ptype = row

                choice = input(f"{name} exists? skip/overwrite: ")

                if choice == "skip":
                    continue

                # group
                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING;
                """, (group,))

                # get group id
                cur.execute("SELECT id FROM groups WHERE name=%s;", (group,))
                gid = cur.fetchone()[0]

                # insert contact
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s,%s,%s,%s)
                    ON CONFLICT (name) DO UPDATE
                    SET email=EXCLUDED.email,
                        birthday=EXCLUDED.birthday,
                        group_id=EXCLUDED.group_id;
                """, (name, email, birthday, gid))

                # get contact id
                cur.execute("SELECT id FROM contacts WHERE name=%s;", (name,))
                cid = cur.fetchone()[0]

                # phone
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s,%s,%s);
                """, (cid, phone, ptype))

    print("Import done")


# menu
def menu():
    while True:
        print("""
1. Search
2. Filter by group
3. Sort contacts
4. Add phone
5. Move to group
6. Pagination
7. Export JSON
8. Import JSON
0. Exit
""")

        choice = input("> ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            filter_by_group()
        elif choice == "3":
            sort_contacts()
        elif choice == "4":
            add_phone()
        elif choice == "5":
            move_to_group()
        elif choice == "6":
            pagination_loop()
        elif choice == "7":
            export_json()
        elif choice == "8":
            import_json()
        elif choice == "0":
            break


# run
if __name__ == "__main__":
    menu()