import cv2
import numpy as np
import face_recognition as fr
import os
import mysql.connector as mc
from datetime import datetime

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer


# a new user 'newuser' has been created to ensure security. Alternatively, the connection can be made using the root
# user by modifying the below line to: user='root', and entering corresponding password in the argument. The database
# name can be changed if needed, too.

mycon = mc.connect(host='localhost', user='newuser', passwd='newpassword', database='school_attendance')
if mycon.is_connected():
    print('Connection Successful......')
cursor = mycon.cursor()


mixer.init()
mixer.music.load("marked.mp3")


get1 = datetime.now()
head = get1.strftime('`%d-%m-%Y`')


# load student names and images
studentsImages = []
studentsNames = []
newList = os.listdir('Students')
for i in newList:
    studentsImages.append(cv2.imread('Students/'+i))
    studentsNames.append(i.split('.')[0])


# automatically create a new date column if it's a new day
cursor.execute('select column_name from information_schema.columns where table_name = \'attendance\' and '
               'ordinal_position = (Select max(ordinal_position) from information_schema.columns where table_name = '
               '\'Attendance\')')
lastColumn = f'`{cursor.fetchone()[0]}`'
if lastColumn!=head:
    cursor.execute(f"ALTER TABLE attendance ADD({head} VARCHAR(20) DEFAULT 'Absent')")
    mycon.commit()


# create a set of students who are absent till now
# set instead of list for faster search times (avg O(1)) in markAttendance func
cursor.execute(f"SELECT name FROM attendance WHERE {head}='Absent'")
absentStudents = cursor.fetchall()
tillNowAbsent = set(absent[0] for absent in absentStudents)


# create encodings of student images
def Encode(imageList):
    encodedList = []
    for im in imageList:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        encodedList.append(fr.face_encodings(im)[0])
    return encodedList


studentsEncode = Encode(studentsImages)
print('Encoding Successful......')


# marking attendance by executing an update command
def markAttendance(matchName, get):
    # ensuring the update command is only executed for those who are marked absent, and not unnecessarily for those
    # who are already marked present
    if matchName in tillNowAbsent:
        timeArrival = get.strftime('%H:%M:%S')
        cursor.execute(f"UPDATE attendance SET {head} = '{timeArrival}' WHERE name = '{matchName}'")
        mycon.commit()
        print(f"{matchName} has been marked as PRESENT.")
        mixer.music.play()
        tillNowAbsent.remove(matchName)


cap = cv2.VideoCapture(0)


try:
    while True:
        x, wcamImg = cap.read()
        wcamImgSmall = cv2.resize(wcamImg, (0,0), None, 0.25, 0.25)
        wcamImgSmall = cv2.cvtColor(wcamImgSmall, cv2.COLOR_BGR2RGB)

        wcamFacesLoc = fr.face_locations(wcamImgSmall)
        wcamFacesEncode = fr.face_encodings(wcamImgSmall, wcamFacesLoc)

        for enc, loc in zip(wcamFacesEncode, wcamFacesLoc):
            matchResults = fr.compare_faces(studentsEncode, enc)
            faceDis = fr.face_distance(studentsEncode, enc)
            matchIndex = np.argmin(faceDis)
            if matchResults[matchIndex]:
                get2 = datetime.now()
                matchName = studentsNames[matchIndex].title()
                y1, x2, y2, x1 = loc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(wcamImg, (x1,y1), (x2,y2), (0,252,124), 2)
                cv2.rectangle(wcamImg, (x1, y2-35), (x2,y2), (0,252,124), cv2.FILLED)
                cv2.putText(wcamImg, matchName,(x1+6, y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255), 2)
                markAttendance(matchName, get2)
        cv2.imshow('WebCam', wcamImg)
        key = cv2.waitKey(1)
        if key == ord('X'):
            break
except KeyboardInterrupt:
    print('The program has been force stopped.')
finally:
    mycon.close()
    cap.release()
    cv2.destroyAllWindows()