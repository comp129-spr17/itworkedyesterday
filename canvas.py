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

def getUserToken():
    try:
        token_file = open('usertoken.txt', 'r')
        token = token_file.read()
    except:
        token = input("Please enter your token value: ")
        token_file = open('usertoken.txt', 'w')
        token_file.write(token)
    return token

def getUserAccount():
    mode = "users/self/profile"
    url = service_url + mode + '?' + parse.urlencode({'access_token': user_token})
    response = request.urlopen(url)
    obj = json.load(reader(response))
    return obj

reader = codecs.getreader('utf-8')
pp = pprint.PrettyPrinter(indent=4)
service_url = "https://pacific.instructure.com/api/v1/"
mode = ""
url = ""
user_token = getUserToken()
working_data = getUserAccount()
pp.pprint(working_data)
