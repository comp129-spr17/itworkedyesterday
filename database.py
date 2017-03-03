import mysql.connector
from mysql.connector import errorcode
import data_structures
import canvas

def main():
    connect_to_db()

def connect_to_db():
    username = 'admin'
    pw = 'mypassword'
    host = 'canvasplusplus.cm39236m2xbo.us-west-2.rds.amazonaws.com'
    db = 'canvas++'
    try:
        connection = mysql.connector.connect(user=username, password=pw, host=host, databse=db)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERROR: Username or Password is not correct")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("ERROR: Database does not exist")
        else:
            print(err)
    else:
        connection.close()


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