import sqlite3
import os.path
import sys

def build(): #building the data base

    conn = sqlite3.connect('cronhoteldb.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS TaskTimes(TaskId INT PRIMARY KEY NOT NULL, DoEvery INT NOT NULL, NumTimes INT NOT NULL);')
    cursor.execute('CREATE TABLE IF NOT EXISTS Tasks(TaskId INT NOT NULL REFERENCES TaskTimes(TaskId), TaskName TEXT NOT NULL, Parameter INT NOT NULL);')
    cursor.execute('CREATE TABLE IF NOT EXISTS Rooms(RoomNumber INT PRIMARY KEY NOT NULL);')
    cursor.execute('CREATE TABLE IF NOT EXISTS Residents(RoomNumber INT NOT NULL REFERENCES Rooms(RoomNumber), FirstName TEXT NOT NULL, LastName TEXT NOT NULL);')

    l = []
    for i in open(sys.argv[1], 'r'): #creating a list of lists containing each line from the configuration file
        l.append(i.split(','))
    for i in range(len(l)):
        if l[i][0] == 'room': # inserting into the room/room&resident columns, depending on the if result
            if len(l[i]) == 2:
                cursor.execute('INSERT INTO Rooms VALUES ({0});'.format(l[i][1]))
            else:
                cursor.execute('INSERT INTO Rooms VALUES ({0});'.format(l[i][1]))
                cursor.execute('INSERT INTO Residents VALUES ({0}, "{1}", "{2}");'.format(l[i][1], l[i][2], l[i][3]))
        elif l[i][0] == 'clean': # checking 'clean' espiecially for making the parameter 0
            id = cursor.execute('SELECT COUNT(*) FROM TaskTimes;') #creating a unique id according to the number of rows
            id = id.fetchall()
            id = id[0][0]
            cursor.execute('INSERT INTO TaskTimes VALUES ({0},{1},{2});'.format(id, l[i][1], l[i][2]))
            cursor.execute('INSERT INTO Tasks VALUES ({0},"{1}",{2});'.format(id, l[i][0], 0))
        else:
            id = cursor.execute('SELECT COUNT(*) FROM TaskTimes;') #creating a unique id according to the number of rows
            id = id.fetchall()
            id = id[0][0]
            cursor.execute('INSERT INTO TaskTimes (TaskId, DoEvery, NumTimes) VALUES ({0},{1},{2});'.format(id, l[i][1], l[i][3]))
            cursor.execute('INSERT INTO Tasks VALUES ({0},"{1}",{2});'.format(id, l[i][0], l[i][2]))
    
    conn.commit() #commiting the changes
    conn.close() # closing the connection

if os.path.isfile('cronhoteldb.db') == False: #checking whether the database does not exist
    build()