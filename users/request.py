import sqlite3
import json
from models import User


def login_user(user_data):
    with sqlite3.connect("./raremedia.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT * FROM Users u
            WHERE
            u.username = ?
            AND
            u.password = ?;
        """, (user_data['username'], user_data['password']))

        result = db_cursor.fetchone()

        if not result:
            return None
        else:
            return User(**result)


def create_user(post_data):
    new_user = User(**post_data)

    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Users
            ( first_name, last_name, email, bio, username, password, profile_image_url, created_on, active, is_staff )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );
        """, ( new_user.first_name, new_user.last_name, new_user.email, new_user.bio, new_user.username, new_user.password, new_user.profile_image_url, new_user.created_on, new_user.active, new_user.is_staff ))

        id = db_cursor.lastrowid
        new_user.id = id

    return new_user


def get_all_users():
    with sqlite3.connect('./raremedia.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            u.is_staff
        FROM Users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            user = User(**row)
            users.append(user.__dict__)

    return json.dumps(users)


def get_single_user(id):
    with sqlite3.connect('./raremedia.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            u.is_staff
        FROM Users u
        WHERE u.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        user = User(**data)

        return json.dumps(user.__dict__)


def get_user_by_email(email):

    with sqlite3.connect('./raremedia.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            u.is_staff
        FROM Users u
        WHERE u.email = ?
        """, ( email, ))

        users = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            user = User(row['id'], row['first_name'], row['last_name'], row['email'],
            row['bio'], row['username'], row['password'], row['profile_image_url'],
            row['created_on'], row['active'], row['is_staff'])
            users.append(user.__dict__)

    return json.dumps(users)


def update_user(id, new_user):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Users
            SET
                first_name = ?,
                last_name = ?,
                email = ?,
                bio = ?,
                username = ?,
                password = ?,
                profile_image_url = ?,
                is_staff = ?
        WHERE id = ?
        """, (new_user['first_name'],new_user['last_name'],new_user['email'],
            new_user['bio'], new_user['username'], new_user['password'],
            new_user['profile_image_url'], new_user['is_staff'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def delete_user(id):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Users
        WHERE id = ?
        """, (id, ))