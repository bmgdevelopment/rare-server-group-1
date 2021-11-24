import sqlite3
import json

from models import Tag

def get_single_tag(id):
    with sqlite3.connect("./raremedia.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE t.id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        tag = Tag(data['id'], data['label'])
        
        return json.dumps(tag.__dict__)
    

def get_all_tags():
    with sqlite3.connect("./raremedia.db") as conn:
        
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        """)
        
        tags = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            tag = Tag(row['id'], row['label'])
            
            tags.append(tag.__dict__)
            
    return json.dumps(tags)


def create_tag(new_tag):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            ( label )
        VALUES
            ( ? );
        """, (new_tag['label'], ))
               
        id = db_cursor.lastrowid

        new_tag['id'] = id


    return json.dumps(new_tag)

# UPDATE TAG 
# ----------------
def update_tag(id, new_tag):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?
        """, (new_tag['label'], id, ))
     
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
