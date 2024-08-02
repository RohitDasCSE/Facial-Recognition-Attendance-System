import os
import mysql.connector as mc


mycon = mc.connect(host='localhost', user='newuser', passwd='newpassword', database='school_attendance')
if mycon.is_connected():
    print('Connection Successful......')
cursor = mycon.cursor()


studentsInDirectory = set()
newList = os.listdir('Students')
for i in newList:
    studentsInDirectory.add(i.split('.')[0])


cursor.execute("SELECT Name FROM attendance")
data = cursor.fetchall()
studentsInDatabase = set(student[0] for student in data)


added = studentsInDirectory - studentsInDatabase
removed = studentsInDatabase - studentsInDirectory


for student in added:
    cursor.execute(f"INSERT INTO attendance (Name) VALUES ('{student}')")
for student in removed:
    cursor.execute(f"DELETE FROM attendance WHERE Name='{student}'")
mycon.commit()


print('Student list refreshed in database successfully...')
