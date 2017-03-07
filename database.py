import sqlite3
import data_structures
import canvas

def main():
    connect_to_db()
    TABLES = {}

def connect_to_db():
    """
    username = 'admin'
    pw = 'mypassword'
    host = 'canvasplusplus.cm39236m2xbo.us-west-2.rds.amazonaws.com'
    db_name = 'canvas++'
    """

def create_connection(conn):
    #cursor object
    c=conn.cursor()
    return c


def create_user_table(c,conn):
    #create table for user
    c.execute ('''CREATE TABLE users (id, name, account_id, enrollment_term_id)''')
    #save (commit) the changes to database
    conn.commit()


def insert_user(c, user, conn):
    #insert user into table
    c.execute("INSERT INTO user VALUES (user.id, user.data, user.bio, user.avatar_url, user.login_id)")
    #save (commit) the changes to database
    conn.commit()

def access_user(c,user):
    #access user information from user table by user ID
    c.execute('SELECT user.id FROM user')

def create_course_table(c, conn):
    #create course table
    c.execute('''CREATE TABLE courses (canvas_id, course_name, associated_account, term)''')
    #save (commit) the changes to databse
    conn.commit()

def insert_course(c, user, conn):
    #insert course into table
    #need to pass in correct way to access this info about courses
    c.execute("INSERT INTO courses (user.canvas_id, user.name, user.canvas_account, user.canvas_term")
    #save(commit) the changes to database
    conn.commit()

def access_user_courses(c, user):
    c.execute('SELECT user.canvas_id FROM course')

main()