import logging
from enum import Enum
from typing import Dict

class Service(Enum):
    ORIGINAL = 0
    CANVAS = 1


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

'''Pass in a Course object as data.'''
class TodoList():
    def __init__(self, data):
        self.canvas_id = data["id"]
        self.name = data["name"]
        self.canvas_account = data["account_id"]
        self.canvas_term = data["enrollment_term"]
        self.service = Service.CANVAS
        self.todos = []

    def add(self, data):
        if type(data) is dict:
            self.todos.append(data)
        elif type(data) is list:
            self.todos = self.todos + data
        else:
            logging.debug("Data type not recognized")

    def __str__(self):
        to_return = ''
        to_return +=\
            "Canvas ID: {}\nCourse Name: {}\nAssociated Account: {}\nTerm: {}"\
            .format(self.canvas_id, self.name,\
                    self.canvas_account, self.canvas_term)
        return to_return

    def __sizeof__(self):
        return len(self.todos)

def main():
    user_data = {'id': 42, 'name': 'Arthur Dent', 'bio': 'Mostly harmless.', 'avatar_url': 'www.images.google.com', 'login_id': 'adent42'}
    test_user = User(user_data)
    print(str(test_user))
    print('\n')
    course_data = {'id': 51, 'name': 'Intro to CS', 'account_id': 42, 'enrollment_term': 'Fall 2015'}
    test_course = TodoList(course_data)
    print(str(test_course))

main()