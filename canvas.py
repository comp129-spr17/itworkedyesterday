from urllib import request as urlrequest
from urllib import parse as urlparse
import json

print("hello world")

class Token():
    name = ""
    string = ""
    def __init__(self, n, s):
        name = n
        string = s

service_url = "https://pacific.instructure.com/login/auth?"
token_list = [Token("Jack", "4571~shh2TtP3Ik0FQ7lk2s351bLelRoKDdbVcudLlg5I3wQ4iXXwEKTJBwXoSInoDDL6")]
canvas_url = service_url + urlparse.urlencode(client_id=token_list[0])