import sqlite3
import json
from models import Subscription

def get_single_subscription(id):
    with sqlite3.connect("./raremedia.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on
        FROM Subscriptions s
        WHERE s.id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        subscription = Subscription(data['id'], data['follower_id'], data['author_id'],
                                    data['created_on'], data['ended_on'])
        
        return json.dumps(subscription.__dict__)
    
    
def get_all_subscriptions():
    with sqlite3.connect("./raremedia.db") as conn:
        
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on
        FROM Subscriptions s
        """)
        
        
        subscriptions = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'],
                                        row['created_on'], row['ended_on'])
            
            
            subscription_dict = subscription.__dict__
            subscription_dict['created_on'] = str(subscription.created_on)
            subscription_dict['ended_on'] = str(subscription.ended_on)
            subscriptions.append(subscription_dict)
            
    return json.dumps(subscriptions)

def get_subscription_by_author_id(author_id):
    with sqlite3.connect("./raremedia.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on
        FROM Subscriptions s
        WHERE s.author_id = ?
        """, ( author_id, ))

        subscriptions = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'],
                                        row['created_on'], row['ended_on'])           
            subscriptions.append(subscription.__dict__)

    return json.dumps(subscriptions)


def create_subscription(new_subscription):
    with sqlite3.connect("./raremedia.db") as conn:
        db_cursor = conn.cursor()
        subscription = Subscription(id = None, follower_id = new_subscription['follower_id'], author_id = new_subscription['author_id'])
        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( follower_id, author_id, created_on, ended_on )
        VALUES
            ( ?, ?, ?, ?);
        """, (subscription.follower_id, subscription.author_id, subscription.created_on, subscription.ended_on))
        
        id = db_cursor.lastrowid
        
        
        new_subscription['created_on'] = str(subscription.created_on)
        new_subscription['ended_on'] = str(subscription.ended_on)
        new_subscription['id'] = id
    
        
    return json.dumps(new_subscription)