import sqlite3
import data_structures
import canvas

def main():
    db = 'canvasplusplus.cm39236m2xbo.us-west-2.rds.amazonaws.com'
    conn=sqlite3.connect(db)
    create_user_table()
    user = User(user_data)

def create_user_table():
    #cursor object
    c=conn.cursor()
    #create table for user
    c.execute ('''CREATE TABLE users (id, name, account_id, enrollment_term_id)''')
    #save (commit) the changes to database
    conn.commit()

def insert_user(user):
    #insert user into table
    c.execute("INSERT INTO user VALUES (user.id, user.data, user.bio, user.avatar_url, user.login_id)")
    #save (commit) the changes to database
    conn.commit()

def access_user(user):
    #access user information from user table by user ID
    c.execute('SELECT user.id FROM user')
main()