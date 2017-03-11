import time
import sqlite3

def dohoteltask(taskname, parameter):
    conn = sqlite3.connect('cronhoteldb.db')
    cursor = conn.cursor()
    if taskname == 'wakeup':
        cursor.execute('SELECT FirstName FROM Residents WHERE RoomNumber = {0};'.format(parameter)) #getting first name of resident according to the room parameter
        firstname = cursor.fetchall()[0][0] #getting the root value
        firstname = str(firstname)
        cursor.execute('SELECT LastName FROM Residents WHERE RoomNumber = {0};'.format(parameter)) #getting last name of resident according to the room parameter
        lastname = cursor.fetchall()[0][0]
        lastname = str(lastname)
        t = time.time() #capturing the time!
        print firstname + " " + lastname.rstrip() + ' in room {0} received a wakeup call at {1}'.format(parameter, t)
        return t
    if taskname == 'breakfast':
        cursor.execute('SELECT FirstName FROM Residents WHERE RoomNumber = {0};'.format(parameter))
        firstname = cursor.fetchall()[0][0]
        firstname = str(firstname)
        cursor.execute('SELECT LastName FROM Residents WHERE RoomNumber = {0};'.format(parameter))
        lastname = cursor.fetchall()[0][0]
        lastname = str(lastname)
        t = time.time()
        print (firstname + ' ' + lastname.rstrip() + ' in room {0} has been served breakfast at {1}'.format(parameter,t))
        return t
    if taskname == 'clean':
        cursor.execute('SELECT RoomNumber FROM Residents;') #getting the RoomNumber out of the Resident table
        result = cursor.fetchall()
        l = []
        for i in range(len(result)): #making a list out of it
            l.append(result[i][0])
        cursor.execute('SELECT * FROM Rooms;')#getting the room numbers
        result = cursor.fetchall()
        l2 = []
        for i in range(len(result)): #checking for rooms without a resident
            if result[i][0] not in l:
                l2.append(str(result[i][0]))
        st = ', '.join(l2) #making a string out of it
        t = time.time()
        print 'Rooms ' + st + ' were cleaned at {0}'.format(t)
        return t

    conn.close()