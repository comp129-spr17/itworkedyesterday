import sqlite3
import MySQLdb
import data_structures
import canvas

def main():
    username = 'admin'
    pw = 'mypassword'
    host = 'canvasplusplus.cm39236m2xbo.us-west-2.rds.amazonaws.com'
    db_name = 'canvas++'
    db = connect_to_db(username, pw, host, db_name)
    cur = create_cursor(db)


def connect_to_db(username, pw, host, db_name):

    db = MySQLdb.connect(host = host, user = username, passwd= pw, db = db_name )
    return db

def create_cursor(db):
    cur = db.cursor()
    return cur


def create_user_table(cur, db):
    sql = """CREATE TABLE USER(id VARCHAR(20) NOT NULL, name VARCHAR(30), bio VARCHAR(20), avatar_url VARCHAR(30), login_id VARCHAR(30)"""
    cur.execute(sql)
    db.close()

    #create table for user
    #c.execute ('''CREATE TABLE users (id, name, account_id, enrollment_term_id)''')
    #save (commit) the changes to database
    #conn.commit()




def insert_user(cur, user, db):
    sql = """INSERT INTO USER (id, name, bio, avatar_url, login_id) VALUES(user.id, user.name, user.bio, user.avatar_url, user.login_id)"""
    try:
        #Execute the SQL command
        cur.execute(sql)
        #commit your changes in the database
        db.commit()
    except:
        #Rollback in case there is an error
        db.rollback()

    #disconnect from server
    db.close()
    #insert user into table
    #c.execute("INSERT INTO user VALUES (user.id, user.data, user.bio, user.avatar_url, user.login_id)")
    #save (commit) the changes to database
    #conn.commit()

def access_user(cur,db):
    sql = "SELECT * FROM USER"
    try:
        #Execute the SQL command
        cur.execute(sql)
        #fetch all the rows in a list of lists
        results = cur.fetchall()
        for row in results:
            id = row[0]
            name = row[1]
            bio = row[2]
            avatar_url = row[3]
            login_id = row[4]
            #print fetched result
            print ("id= ", id, " name= ",name, " bio= ", bio, "avatar_url= ", avatar_url, "login_id= ", login_id)
    except:
        print("Error: unable to fetch data")
    #disconnect from server
    db.close()


    #access user information from user table by user ID
    #c.execute('SELECT user.id FROM user')

def create_course_table(cur, db):
    sql = """CREATE TABLE COURSES (canvas_id VARCHAR(20) NOT NULL, course_name VARCHAR(20) NOT NULL, associated_account VARCHAR(20), term VARCHAR(20) """
    cur.execute(sql)
    db.close()
    #create course table
    #c.execute('''CREATE TABLE courses (canvas_id, course_name, associated_account, term)''')
    #save (commit) the changes to databse
    #conn.commit()

def insert_course(cur, user, db):
    sql = """INSERT INTO COURSES (canvas_id, course_name, associated_account, term) VALUES (user.canvas_id, user.name, user.canvas_account, user.canvas_term)"""
    try:
        #Execute the SQL command
        cur.execute(sql)
        #commit your changes in the database
        db.commit()
    except:
        #Rollback in case there is an error
        db.rollback()

    #disconnect from server
    db.close()

    #insert course into table
    #need to pass in correct way to access this info about courses
    #c.execute("INSERT INTO courses (user.canvas_id, user.name, user.canvas_account, user.canvas_term")
    #save(commit) the changes to database
    #conn.commit()

def access_user_courses(c, user):
    c.execute('SELECT user.canvas_id FROM course')

main()