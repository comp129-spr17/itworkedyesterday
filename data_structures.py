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
        self.canvas_name = data["name"]
        self.canvas_state = data["workflow_state"]
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
            "Canvas ID: {}\nCourse Name: {}\nWork State: {}\nAssociated Account: {}\nTerm: {}"\
            .format(self.canvas_id, self.canvas_name, self.canvas_state,\
            self.canvas_account, self.canvas_term)
        return to_return

    def __sizeof__(self):
        return len(self.todos)

class Assignment_Task():
    def __init__(self, data):
        self.assignment = data['name']
        #self.description = data['description']
        #self.due_at = data['due_at']
        #self.course_id = data['course_id']

    def __str__(self):
        to_return = ''
        to_return += "Course ID: {}\nAssignment: {}\nDescription: {}\nDue Date: {}\n".format(self.course_id, self.assignment,self.description, self.due_at)
        return to_return
