import mysql.connector
from mysql.connector import errorcode
import data_structures
import canvas

def main():
    connect_to_db()
    TABLES = {}

def connect_to_db():
    username = 'admin'
    pw = 'mypassword'
    host = 'canvasplusplus.cm39236m2xbo.us-west-2.rds.amazonaws.com'
    db_name = 'canvas++'
    try:
        connection = mysql.connector.connect(user=username, password=pw, host=host, databse=db_name)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERROR: Username or Password is not correct")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("ERROR: Database does not exist")
        else:
            print(err)
    else:
        connection.close()


def create_user_table(TABLES):
    """
    #cursor object
    c=conn.cursor()
    #create table for user
    c.execute ('''CREATE TABLE users (id, name, account_id, enrollment_term_id)''')
    #save (commit) the changes to database
    conn.commit()
    """
    TABLES['user'] = (
        "CREATE TABLE 'user' ("
        "'user_id' int(9) NOT NULL,"
        #how long do we need to make names?
        "'user_name varchar(30) NOT NULL,"
        #how many numbers are in account id?
        "'account_id' int(10) NOT NULL,"
        #how many numbers are in enrollment term id?
        "'enrollment_term_id int(10) NOT NULL,"
        "PRIMARY KEY ('user_id')"
        ") ENGINE = InnoDB"
    )

def insert_user(user):
    #insert user into table
    c.execute("INSERT INTO user VALUES (user.id, user.data, user.bio, user.avatar_url, user.login_id)")
    #save (commit) the changes to database
    conn.commit()

def access_user(user):
    #access user information from user table by user ID
    c.execute('SELECT user.id FROM user')
main()