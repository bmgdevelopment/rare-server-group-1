import sqlite3
import json
from models import Posts

# POSTS = [
#     {
#         "id": 1,
#         "user_id": 1,
#         "category_id": 1,
#         "title": "Food Products",
#         "publication_date": "21 November 2021",
#         "image_url": "placeholder",
#         "content": '',
#         "approved": ''
#     },
#     {
#        "id": 2,
#         "user_id": 1,
#         "category_id": 2,
#         "title": "Food Products",
#         "publication_date": "21 November 2021",
#         "image_url": "image goes here",
#         "content": '',
#         "approved": '' 
#     },
#     {
#         "id": 3,
#         "user_id": 1,
#         "category_id": 2,
#         "title": "Fancy Example",
#         "publication_date": "20 November 2021",
#         "image_url": "placeholder",
#         "content": '',
#         "approved": ''
#     }
# ]


def get_all_posts():
    with sqlite3.connect("./raremedia.db") as conn:
        
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM posts p
        """)
        
        posts = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            
            post = Posts(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
            
            posts.append(post.__dict__)
    
    return json.dumps(posts)
    
def get_single_post(id):
    with sqlite3.connect("./raremedia.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM posts p
        WHERE p.id = ?
        """, ( id, ))
        
        data = db_cursor.fetchone()
        
        post = Posts(data['id'], data['user_id'], data['category_id'], data['title'],
                            data['publication_date'], data['image_url'],
                            data['content'], data['approved'])
        return json.dumps(post.__dict__)

def create_post(new_post):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'] ))

        id = db_cursor.lastrowid

        new_post['id'] = id

    return json.dumps(new_post)



def delete_post(id):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))
        

        
        
        
def update_post(id, new_post):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?
                content = ?
                approved = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'], id, ))

        
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        
        return False
    else:
        return True
    
    
def get_post_by_title(title):
    with sqlite3.connect("./raremedia.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        select
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            p.approved
        from Posts p
        WHERE p.title = ?
        """, ( title, ))
        
        posts = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post = Posts(row['id'], row['user_id'], row['category_id'], row['title'],
                            row['publication_date'], row['image_url'],
                            row['content'], row['approved'])
            posts.append(post.__dict__)
            
    return json.dumps(posts)