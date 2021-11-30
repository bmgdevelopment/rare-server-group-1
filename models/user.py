
class User():
    def __init__(self, id, first_name, last_name,
                email='', bio='', username='', password='', profile_image_url='',
                created_on=None, active=True, is_staff=True):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.bio = bio
        self.username = username
        self.password = password
        self.profile_image_url = profile_image_url
        self.created_on = created_on
        self.active = active
        self.is_staff = is_staff
