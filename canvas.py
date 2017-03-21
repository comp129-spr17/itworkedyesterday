'''
* It Worked Yesterday...
* 2/7/17
* canvas.py
* Handles connection the Canvas Learning Management Software.
'''
from urllib import parse as parse
from urllib import request as request
from urllib import error as url_error
import logging
from enum import Enum
from typing import Dict
from bs4 import BeautifulSoup
import logging
import json
import pprint
import codecs
import unittest

'''Global variables'''
reader = codecs.getreader('utf-8')  # This exists to help the json and urllib libraries work together.
pp = pprint.PrettyPrinter(indent=4)  # Print out larger, data objects in a readable manner.
service_url = "https://pacific.instructure.com/api/v1/"  # The site that we're pulling our data from.


class RetrieveFromCanvasTest(unittest.TestCase):

    # Test to see if able to retrieve token from file
    def test_a_obtain_token(self):
        self.token = None
        try:
            token_file = open('usertoken.txt', 'r')
            self.token = token_file.read()
            token_file.close()
        except:
            pass
        self.assertIsNotNone(self.token)

    # Test to see if able to retrieve at least one class from canvas
    def test_b_has_courses(self):
        global user_token
        user_token = None
        self.courses = []
        try:
            token_file = open('usertoken.txt', 'r')
            user_token = token_file.read()
            token_file.close()
        except:
            pass
        try:
            self.courses = get_favorite_courses()
        except:
            pass
        self.assertIsNotNone(user_token)
        self.assertGreater(len(self.courses), 0)

    # Test to see if able to pull at least one assignment from canvas
    def test_c_has_assignments(self):
        global user_token
        user_token = None
        self.courses = []
        try:
            token_file = open('usertoken.txt', 'r')
            user_token = token_file.read()
            token_file.close()
        except:
            pass
        try:
            self.courses = get_favorite_courses()
        except:
            pass
        self.assignments = []
        try:
            for course in self.courses:
                self.course_assignments = get_assignments(str(course['id']))
                for assignment in self.course_assignments:
                    self.assignments.append(assignment)
        except:
            pass
        self.assertIsNotNone(user_token)
        self.assertIsNotNone(self.courses)
        self.assertGreater(len(self.assignments), 0)


class Service(Enum):
    ORIGINAL = 0
    CANVAS = 1


'''Pass in a Profile object'''
class User:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.bio = data['bio']
        self.avatar_url = data['avatar_url']
        self.login_id = data['login_id']
        self.token = None
        self.ToDoLists = []
        self.courses = None  # Maybe unneeded?

    def __str__(self):
        to_return = ''
        to_return += "User ID: {}\nFull Name: {}\nLogin ID: {}"\
            .format(self.id, self.name, self.login_id)
        try:
            to_return += "\nToken: {}".format(self.token)
        except KeyError:
            pass
        try:
            to_return += "\nBio: {}"\
                .format(self.bio)
        except KeyError:
            pass
        try:
            to_return += "\nFavorite Courses: "
            for course in self.courses:
                to_return += "\n\t{}".format(course['name'])
        except TypeError or KeyError:
            pass
        return to_return

    def add(self, data):
        # If the data is a list, the data is a list of course objects
        if type(data) is list:
            for course in data:
                to_do_list = TodoList(course, self.id)
                self.ToDoLists.append(to_do_list)
            ''' Add in at your own risk, prints all assignments and all corresponding data
            for course in self.ToDoLists:
                print(course)
            '''
        # If the data is a string, the data is the user token
        elif type(data) is str:
            self.token = data
        else:
            logging.debug("Data type not recognized")


'''Pass in a Course object as data.'''
class TodoList:
    def __init__(self, data, user_id):
        self.canvas_id = data["id"]
        self.name = data["name"]
        self.canvas_account = data["account_id"]
        self.canvas_term = data["enrollment_term_id"]
        self.service = Service.CANVAS
        assignments = get_assignments(str(data['id'])) # data id is the course id
        self.assignment_tasks = []
        self.user_id = user_id
        for assignment in assignments:
            todo = Assignment_Task(assignment, user_id)
            self.assignment_tasks.append(todo)

    def __str__(self):
        to_return = ''
        to_return +=\
            "Canvas ID: {}\nCourse Name: {}\nAssociated Account: {}\nTerm: {}\nAssignments: {}"\
            .format(self.canvas_id, self.name, self.canvas_account, self.canvas_term, self.__sizeof__())
        return to_return

    def __sizeof__(self):
        return len(self.assignment_tasks)

    def add(self, data):
        if type(data) is dict:
            self.todos.append(data)
        elif type(data) is list:
            self.assignment_tasks = self.assignment_tasks + data
        else:
            logging.debug("Data type not recognized")


class Assignment_Task:
    def __init__(self, data, user_id):
        # print(data)
        self.assignment = data['name']
        self.description = data['description']
        self.due_at = data['due_at']
        self.course_id = data['course_id']
        self.user_id = user_id

    def __str__(self):
        to_return = ''
        to_return += "Course ID: {}\nAssignment: {}\nDescription: {}\nDue Date: {}\n"\
                .format(self.course_id, self.assignment,self.description, self.due_at)
        return to_return


'''Gets the url that contains the desired data. URL changes based on the user token and the mode.
@param mode: Represents the type of data that we're trying to recieve.'''
def get_url(mode):
    return service_url + mode + '?' + parse.urlencode({'access_token': user_token})


def get_data_from_url(url):
    # print(url)
    response = request.urlopen(url)
    obj = json.load(reader(response))
    return obj


def get_data(mode):
    return get_data_from_url(get_url(mode))


''' Gathering and returning user data objects'''
def get_user_token():
    try:
        token_file = open('usertoken.txt', 'r')
        token = token_file.read()
        token_file.close()
    except:
        token = input("Please enter your token value: ")
        token_file = open('usertoken.txt', 'w')
        token_file.write(token)
    return token


''' @return: User's profile if found, returns None if unable to retrieve
    @rtype: Profile'''
def get_user():
    mode = "users/self/profile"
    try:
        return get_data(mode)
    except (url_error.HTTPError, url_error.URLError, url_error.ContentTooShortError):
        logging.error('Unable to retrieve user data.')
        return None


''' @return: list of favorite courses or active courses if user has no favorite courses. Returns None if unable to retrieve
    @rtype: list of Favorite['context_type'] where context_type = "Course" '''
def get_favorite_courses():
    mode = "users/self/favorites/courses"
    try:
        return get_data(mode)
    except (url_error.HTTPError, url_error.URLError, url_error.ContentTooShortError):
        logging.error('Unable to retrieve favorite courses.')
        return None


''' Returns "Active" courses, which can be misleading if professor does not deactivate course after term end.
    @return: list of "Active" courses.
    @rtype: list of courses. '''
def get_courses():
    mode = "courses"
    return get_data(mode)


def get_assignments(course_id):
    mode = "users/self/courses/" + course_id + "/assignments"
    try:
        return get_data(mode)
    except (url_error.HTTPError, url_error.URLError, url_error.ContentTooShortError):
        logging.error('Unable to retrieve assignment list from each of your favorite courses.')
        return None


''' Returns an estimate of time needed to complete assignments for each course based on user input
    @return: dictionary of time estimates.
    @rtype: dictionary of courses and corresponding time values. '''
def time_estimate():
    input_time = {}
    course_items = get_favorite_courses()
    print("Enter the average amount of time needed [in minutes] to complete an assignment for the following class:")
    for course in course_items:
        time = input(course['name'] + ': ')
        input_time[course['name']] = time
    return input_time

def main():
    global user_token  # The token used to authenticate the user.
    unittest.main(exit=False)
    user_token = get_user_token()
    user_data = get_user()
    user = User(user_data)
    user.add(get_favorite_courses())
    user.add(user_token)
    '''
    pp.pprint(course_data)
    time_needed = time_estimate()
    print('\"Active\" Courses:')
    for course in course_data:
        print('\t', course['name'])
    print('Favorite Courses:')
    # Print Favorite Courses
    for favorite_course in favorite_course_data:
        print('\t', favorite_course['name'])
        print('\t\t','Assignments From Course:')
        assignments_data = get_assignments(str(favorite_course['id']))
        # Print assignments in course
        for assignments in assignments_data:
            print('\t\t\t', assignments['name'])

            html = str(assignments['description'])
            soup = BeautifulSoup(html, "html.parser")
            print(soup.get_text())
            #print('\t\t\t\t', assignments['description'])
            print('\t\t\t\t', 'Available: ', assignments['unlock_at'], 'to', assignments['lock_at'])
            print('\t\t\t\t', 'Due: ', assignments['due_at'])
            print('\t\t\t\t', 'Points Possible: ', assignments['points_possible'])
            print('\t\t\t\t', 'Grading Type: ', assignments['grading_type'])
            print('\t\t\t\t', 'Time Needed to Complete: ', time_needed[favorite_course['name']], " minutes")
    '''
    print("\nUser Object string output:")
    print(user)

main()
