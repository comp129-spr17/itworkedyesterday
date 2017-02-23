'''
* It Worked Yesterday...
* 2/7/17
* canvas.py
* Handles connection the Canvas Learning Managment Software.
'''
from urllib import parse as parse
from urllib import request as request
from urllib import error as url_error
from bs4 import BeautifulSoup
import logging
import json
import pprint
import codecs
import data_structures

'''Global variables'''
reader = codecs.getreader('utf-8')  # This exists to help the json and urllib libraries work together.
pp = pprint.PrettyPrinter(indent=4)  # Print out larger, data objects in a readable manner.
service_url = "https://pacific.instructure.com/api/v1/"  # The site that we're pulling our data from.

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

''' @return: list of favorite courses, Returns None if unable to retrieve
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
    user_token = get_user_token()
    user_data = get_user()
    user = data_structures.User(user_data)
    user2 = data_structures.Assignment_Task(user_data)
    id_number = user_data['id']  # Can be used in place of 'self' in mode.
    course_data = get_courses()
    favorite_course_data = get_favorite_courses()
    user.add(favorite_course_data)
    user.add(user_token)
    pp.pprint(course_data)
    time_needed = time_estimate()
    print('\"Active\" Courses:')
    for course in course_data:
        print('\t', course['name'])
    print('Favorite Courses:')
    print(type(favorite_course_data))
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
    print("User Object string output:")
    print(user)
    print(user2)

main()
