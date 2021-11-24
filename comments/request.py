import sqlite3
import json

from models import Comment

def get_all_comments():
    with sqlite3.connect("./raremedia.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content,
            c.created_on
        FROM Comments c
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'], row['created_on'])

            comments.append(comment.__dict__)

    return json.dumps(comments)

def get_single_comment(id):
    pass