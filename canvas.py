'''
* It Worked Yesterday...
* 2/7/17
* canvas.py
* Handles connection the Canvas Learning Managment Software.
'''
from urllib import parse as parse
from urllib import request as request
import json

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
    mode = "accounts"
    url = service_url + mode + '?' + parse.urlencode({'access_token': user_token})
    print(url)
    return request.urlopen(url).read()

service_url = "https://pacific.instructure.com/api/v1/"
mode = ""
url = ""
user_token = getUserToken()
working_data = getUserAccount()
print(working_data)
