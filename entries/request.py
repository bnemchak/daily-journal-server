from models import Journal_entries, Mood
import sqlite3
import json

def get_all_entries():
    with sqlite3.connect("./daily-journal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
            m.id id,
            m.label mood
        FROM Journal_entries e
        JOIN Mood m
            ON m.id = e.mood_id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Journal_entries(row['id'], row['concept'], row['entry'],
                            row['mood_id'], row['date'])

            mood = Mood(row['mood_id'], row['date'])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./daily-journal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
        FROM Journal_entries e
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry = Journal_entries(data['id'], data['concept'], data['entry'], data['mood_id'],
                                    data['date'])

        return json.dumps(entry.__dict__)

def search_for_entry(entry):
    with sqlite3.connect('./daily-journal.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(f"""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Journal_entries e
        WHERE e.entry LIKE '%{entry}%'
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Journal_entries(row['id'], row['concept'], row['entry'], row['mood_id'],
                                    row['date'])
            entries.append(entry.__dict__)

        return json.dumps(entries)

def delete_entry(id):
    with sqlite3.connect('./daily-journal.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Journal_entries
        WHERE id = ?
        """, (id, ))

def create_journal_entry(new_object):
    with sqlite3.connect('./daily-journal.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Journal_entries
            ( concept, entry, mood_id, date )
        VALUES
            (?, ?, ?, ?)
        """, (new_object['concept'], new_object['entry'], new_object['mood_id]'], new_object['date'], ))

        id = db_cursor.lastrowid

        new_object['id'] = id

    return json.dumps(new_object)
