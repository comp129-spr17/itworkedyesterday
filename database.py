import sqlite3
import data_structures

def main():
    db = example.db
    conn=sqlite3.connect(db)
    user = User(user_data)

def database(user):
    #cursor object
    c=conn.cursor()
    #create table for user
    c.execute ('''CREATE TABLE users (id, name, account_id, enrollment_term_id)''')
    #insert user into table
    c.execute("INSERT INTO user VALUES (user.id, user.data, user.bio, user.avatar_url, user.login_id)")
    #save (commit) the changes to database
    conn.commit()

main()