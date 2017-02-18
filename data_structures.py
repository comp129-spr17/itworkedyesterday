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


class Assignment_Task ():

    def __init__(self, data):
        self.assignment_name = data['name']
        self.description = data['description']
        self.due_date = data['due_at']
        self.all_dates = data['all_dates']
        self.course_id = data['course_id']


    def __str__(self):
        to_return = "Course ID: {}\nAssignment: {}\nDescription: {}\nDue Date: {}\n".format(self.course_id, self.assignment_name, self.description, self.due_date)
        return to_return
