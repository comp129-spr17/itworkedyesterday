import sqlite3
import data_structures
import canvas
''' Global variables '''
conn = None
db_location = 'canvasplusplus.cm39236m2xbo.us-west-2.rds.amazonaws.com'
db_user = 'admin'
db_password = 'mypassword'
db = None
''' '''


def main():
    global db_location
    conn = sqlite3.connect(db_location)
    create_user_table()
    user = canvas.User(user_data) #TODO: Pass in user data a different way


def create_user_table():
    # cursor object
    c = conn.cursor()
    # create table for user
    c.execute ('''CREATE TABLE users (id, name, account_id, enrollment_term_id)''')
    # save (commit) the changes to database
    conn.commit()


def insert_user(user):
    # insert user into table TODO: Pass in cursor object before calling c.execute?
    c.execute("INSERT INTO user VALUES (user.id, user.data, user.bio, user.avatar_url, user.login_id)")
    # save (commit) the changes to database
    conn.commit()


def access_user(user):
    # access user information from user table by user ID TODO: Pass in cursor object before calling c.execute?
    c.execute('SELECT user.id FROM user')


main()
