'''
* It Worked Yesterday...
* 2/7/17
* canvas.py
* Handles connection the Canvas Learning Managment Software.
'''
from urllib import parse as parse
from urllib import request as request
import json
import pprint
import codecs

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


def get_user_token():
    try:
        token_file = open('usertoken.txt', 'r')
        token = token_file.read()
    except:
        token = input("Please enter your token value: ")
        token_file = open('usertoken.txt', 'w')
        token_file.write(token)
    return token


def get_user_account():
    mode = "users/self/profile"
    return get_data(mode)


def get_courses():
    mode = "courses"
    return get_data(mode)


def main():
    global user_token  # The token used to authenticate the user.
    user_token = get_user_token()
    profile_data = get_user_account()
    id_number = profile_data['id']  # Can be used in place of 'self' in mode.
    course_data = get_courses()
    pp.pprint(course_data)
    for course in course_data:
        print(course['name'])


main()
