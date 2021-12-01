import sqlite3
import json

from models import Category

def get_single_category(id):
    with sqlite3.connect("./raremedia.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        WHERE c.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        category = Category(data['id'], data['label'])

        return json.dumps(category.__dict__)


def get_all_categories():
    with sqlite3.connect("./raremedia.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['label'])

            categories.append(category.__dict__)

    return json.dumps(categories)


def create_category(new_cat):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            (label)
        VALUES
            (?);
        """, (new_cat['label'], ))

        id = db_cursor.lastrowid

        new_cat['id'] = id

    return json.dumps(new_cat)


# DELETE CATEGORY
# ----------------
def delete_category(id):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (id, ))


# UPDATE CATEGORY
# ----------------
def update_category(id, new_cat):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
            SET
                label = ?
        WHERE id = ?
        """, (new_cat['label'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True