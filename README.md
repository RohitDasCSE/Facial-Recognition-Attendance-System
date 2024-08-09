#### Demo:
[![Attendance System](Demo/thumbnail.jpg)](https://youtu.be/J1bY1v0oXkM "Attendance System")

#### New features not shown in Demo:
* A 'Refresh' feature has been added which when used, automatically refreshes the student list in the database based on the 
current student images in the 'Students' folder. This eliminates the need to add or remove students in the database table manually.

#### Description:  
This is an attendance management system which uses facial recognition to efficiently track attendance and store records in
a MySQL database along with proper date and time. It also has a feature to export the database into a .csv format and email
it to an admin.  
This project was created by me for CBSE Grade 12 Computer Science project on Python and MySQL connectivity.
The entire code in the first commit was written by me in August 2023.

#### Features:
* Use facial recognition to identify students
* Store accurate timestamp of attendance for each student
* Securely store all records in a MySQL database
* The program can automatically detect if it's a new day. Hence there is no need to manually create a field 
 in the database's table for each day
* Export database to a .csv format which can be opened using MS Excel
* Send the .csv file to an admin via email
* A 'Refresh' feature automatically refreshes the student list in the database based on the current student images in the 
 'Students' folder


#### Dependencies:
* setuptools
* opencv-python
* face_recognition
* numpy
* mysql-connector-python
* dlib
* cmake
* pygame
* Pillow


#### Instructions:
* Create a folder called 'Students' in the same location, and in it add pictures of students in jpg format clearly showing 
their face and saved in student_name.jpg format.
* Create a database in MySQL called 'school_attendance' **OR** change the name of the database in source code.
 In it, create a table called 'attendance' with just the Name attribute
* Use as MySQL root user by changing the source code as mentioned in the comments, **OR** create a new user (in this case 'newuser') using the following commands:
  * CREATE USER 'newuser'@'localhost';
  * GRANT ALL PRIVILEGES ON school_attendance.* To 'newuser'@'localhost' IDENTIFIED BY 'newpassword';
* For the first time, the students have to be added to the database table manually.
* If any change has been made to the contents of the 'Students' folder at a later data, such as addition or removal of 
a student, the 'Refresh' feature must be used to automatically reflect those changes in the MySQL database
* Setup ExportAndEmail.py using your own credentials. In case you are using Gmail, the smtp_login_password would be your
gmail password. If you are facing errors with that, enable 2 Step Verification, generate an App Password and use that.


#### Further Work:
* Adding a Liveness Detector that can differentiate between fake and legitimate faces thereby preventing proxy attendance using a picture or video of a student
* Ability to schedule the emailing of the attendance records to the admin at a regular time interval
* Adding data analytics to offer more insight over a period of time