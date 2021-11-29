from datetime import datetime

class Subscription():
    
    def __init__(self, id, follower_id, author_id, created_on = None, ended_on = None):
        self.id = id
        self.follower_id = follower_id
        self.author_id = author_id
        self.created_on = created_on or datetime.now()
        self.ended_on = ended_on or datetime.now()