# Tagle, Marc Neil V.

import sqlite3


def get_connection():
    conn = sqlite3.connect("db/bday_tracker.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_people():
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT person_id, first_name, last_name, birth_date, email, phone_number, notes FROM people")
        people_data = cursor.fetchall()
        return people_data
    
    except Exception as e:
        print("Get people failed:", e)
        return False
    
    finally:
        con.close()


def insert_person(first_name, last_name, birth_date, email, phone, notes):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO people (first_name, last_name, birth_date, email, phone_number, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, birth_date, email, phone, notes))
        conn.commit()
    
        person_id = cursor.lastrowid

        cursor.execute("INSERT INTO reminders (person_id) VALUES (?)", (person_id,))

        conn.commit()
        return True
    
    except Exception as e:
        print("Insert failed:", e)
        return False
    
    finally:
        conn.close()


def edit_person(first_name, last_name, birth_date, email, phone, notes, person_id):
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("""
            UPDATE people
            SET first_name = ?, last_name = ?, birth_date = ?, email = ?, phone_number = ?, notes = ?
            WHERE person_id = ?
        """, (first_name, last_name, birth_date, email, phone, notes, person_id))
        con.commit()
        return True

    except Exception as e:
        print("Edit failed:", e)
        return False
    
    finally:
        con.close()


def delete_person(person_id):
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM people WHERE person_id = ?", (person_id,))
        con.commit()
        return True

    except Exception as e:
        print("Deletion failed:", e)
        return False
    
    finally:
        con.close()


def get_gifts():
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("""
            SELECT
                g.gift_id,
                p.first_name || ' ' || p.last_name AS full_name,
                g.gift_name,
                g.description,
                g.place,
                g.link,
                g.price,
                g.notes
            FROM gift_ideas g
            JOIN people p ON g.person_id = p.person_id
        """)
        gifts_data = cursor.fetchall()
        return gifts_data
    
    except Exception as e:
        print("Get gifts failed:", e)
        return False
    
    finally:
        con.close()


def insert_gift(person_id, gift_name, description, place, link, price, notes):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO gift_ideas (person_id, gift_name, description, place, link, price, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (person_id, gift_name, description, place, link, price, notes))
        conn.commit()
        return True
    
    except Exception as e:
        print("Insert failed:", e)
        return False
    
    finally:
        conn.close()


def edit_gift(person_id, gift_name, description, place, link, price, notes, gift_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE gift_ideas
            SET person_id = ?, gift_name = ?, description = ?, place = ?, link = ?, price = ?, notes = ?
            WHERE gift_id = ?
        """, (person_id, gift_name, description, place, link, price, notes, gift_id))
        conn.commit()
        return True

    except Exception as e:
        print("Edit gift failed:", e)
        return False
    
    finally:
        conn.close()


def delete_gift(gift_id):
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM gift_ideas WHERE gift_id = ?", (gift_id,))
        con.commit()
        return True

    except Exception as e:
        print("Deletion failed:", e)
        return False
    
    finally:
        con.close()


def get_people_with_reminders():
    try:
        con = get_connection()
        cursor = con.cursor()

        cursor.execute("""
            SELECT p.person_id, p.first_name, p.last_name, p.birth_date
            FROM people p
            JOIN reminders r ON p.person_id = r.person_id
        """)
        
        rows = cursor.fetchall()

        people = []
        for row in rows:
            person = {
                "person_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "birth_date": row[3],
            }
            people.append(person)

        return people

    except Exception as e:
        print("Get reminders failed:", e)
        return False
    
    finally:
        con.close()