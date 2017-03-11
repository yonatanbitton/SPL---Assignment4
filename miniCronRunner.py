import hotelWorker
import os.path
import sqlite3
import time

def check(): #checking for a situation where all the NumTimes is 0
    conn = sqlite3.connect('cronhoteldb.db')
    cursor = conn.cursor()
    cursor.execute('SELECT NumTimes FROM TaskTimes')
    temp = cursor.fetchall()
    numtimes = []
    for i in range(len(temp)):
        numtimes.append(temp[i][0])
    count = 0
    for i in range(len(numtimes)):
        if numtimes[i] == 0:
            count += 1
    if count == len(numtimes):
        return True
    return False

def task_id(cursor): #making a list of task id's
    cursor.execute('SELECT TaskId FROM TaskTimes;')
    temp = cursor.fetchall()
    id = []
    for i in range(len(temp)):
        id.append(temp[i][0])
    return id

count = 0 # future test for first iteration
d = {} # future dictionary {taskid : last time executed}

while os.path.isfile('cronhoteldb.db') and check() == False: # looping while the database exists and there is a task left to do
    conn = sqlite3.connect('cronhoteldb.db')
    cursor = conn.cursor()
    taskid = task_id(cursor)
    if count == 0: #if first iteration, do all the jobs
        for id in taskid:
            cursor.execute('SELECT TaskName FROM Tasks WHERE TaskId = %d;' % id)
            taskname = cursor.fetchall()[0][0]
            cursor.execute('SELECT Parameter FROM Tasks WHERE TaskId = %d;' % id)
            parameter = cursor.fetchall()[0][0]
            t = hotelWorker.dohoteltask(taskname, parameter)
            d[id] = t   #{taskid:last time executed}
            cursor.execute('SELECT NumTimes FROM TaskTimes WHERE TaskId = %d;' % id)
            temp = cursor.fetchall()[0][0]
            if temp > 0: # if the last execution of the current task is not the last, decrease the NumTimes value!
                cursor.execute('UPDATE TaskTimes SET NumTimes = NumTimes-1 WHERE TaskId = %d;' % id)
                conn.commit() # commiting
        count += 1 # next iteration is not the first!
        conn.close() #closing connection
    else:
        for id in taskid:
            cursor.execute('SELECT NumTimes FROM TaskTimes WHERE TaskId == {0};'.format(id))
            numtime = cursor.fetchall()[0][0]
            if numtime == 0: # if the currnet task has finished, go to next iteration
                continue
            cursor.execute('SELECT DoEvery FROM TaskTimes WHERE TaskId == {0};'.format(id)) #getitng the DoEvery of the current task
            doevery = cursor.fetchall()[0][0]
            nexttime = d[id] + doevery #next time the task should be done
            now = time.time()
            if int(nexttime) == int(now): #is it now? if so execute the task
                cursor.execute('SELECT TaskName FROM Tasks WHERE TaskId = %d;' % id) #getting task name of the current task id
                taskname = cursor.fetchall()[0][0]
                cursor.execute('SELECT Parameter FROM Tasks WHERE TaskId = %d;' % id) # getting the parameter of the current task id
                parameter = cursor.fetchall()[0][0]
                t = hotelWorker.dohoteltask(taskname, parameter) # send it all to dohoteltask!
                d[id] = t #updating the last time executed value for the current task id
                cursor.execute('SELECT NumTimes FROM TaskTimes WHERE TaskId = %d;' % id)
                temp = cursor.fetchall()[0][0]
                if temp > 0: # same as above
                    cursor.execute('UPDATE TaskTimes SET NumTimes = NumTimes-1 WHERE TaskId = %d;' % id)
                    conn.commit()

            else:
                continue
        conn.close()