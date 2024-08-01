from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
import mysql.connector as msc
from pathlib import Path
from string import Template
from datetime import datetime
import config


mycon = msc.connect(host='localhost', user='newuser', passwd='newpassword', database='school_attendance')
cursor = mycon.cursor()


cursor.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'Attendance'
""")

data = cursor.fetchall()
columnsList = [f"'{i[0]}'" for i in data]
columnsStr = ', '.join(columnsList)


get = datetime.now()
dateExport = get.strftime('%A, %d %b %Y')
timeExport = get.strftime('%H:%M:%S')


export_query = fr"""
    SELECT {columnsStr}
    UNION
    SELECT * FROM attendance
    ORDER BY CASE WHEN Name = 'Name' THEN 0 ELSE 1 END, Name
    INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.2/Uploads/attendance_export.csv'
    FIELDS ENCLOSED BY '"'
    TERMINATED BY ','
    ESCAPED BY '"'
    LINES TERMINATED BY '\r\n';
"""

cursor.execute(export_query)
print('Database Exported Successfully......')


template = Template(Path("email.html").read_text())
body = template.substitute({'dateExport':dateExport, 'timeExport':timeExport,
                            'creator_email': config.creator_email, 'Creator': 'Rohit Das'})


email = MIMEMultipart()
email['from'] = 'SAMS'
email['to'] = config.email_to
email['subject'] = 'Attendance Records'
email.attach(MIMEText(body, "html"))


attachment = open("C:/ProgramData/MySQL/MySQL Server 8.2/Uploads/attendance_export.csv", "rb")
part = MIMEBase("application", "octet-stream")
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename=attendance_export.csv")
email.attach(part)
attachment.close()


with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config.smtp_login_user, config.smtp_login_password)
    smtp.send_message(email)
print('Email Sent to Admin Successfully......')

os.remove('C:/ProgramData/MySQL/MySQL Server 8.2/Uploads/attendance_export.csv')