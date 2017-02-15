import logging

'''Pass in a Profile object'''
class User():
    id = 0

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.bio = data['bio']
        self.avatar_url = data['avatar_url']
        self.login_id = data['login_id']

    def add(self, data):
        if type(data) is list:
            self.courses = data
        elif type(data) is str:
            self.token = data
        else:
            logging.debug("Data type not recognized")

    def __str__(self):
        to_return = ''
        to_return += "User ID: {}\nFull Name: {}\nLogin ID: {}"\
            .format(self.id, self.name, self.login_id)
        try:
            to_return += "\nToken: {}".format(self.token)
        except Exception:
            pass
        try:
            to_return += "\nBio: {}"\
                .format(self.bio)
        except Exception:
            pass
        try:
            to_return += "\nFavorite Courses: "
            for course in self.courses:
                to_return += "\n\t{}".format(course['name'])
        except Exception:
            pass
        return to_return
