from flask import Flask,render_template,request
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date
import sqlite3
from flask import session
import pandas as pd
import json

name="saismitha"

app = Flask(__name__)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method=="POST":
        return render_template('index.html')
    else:
        return "Everything is okay!"

@app.route('/name', methods=['GET', 'POST'])
def name():

    if request.method == "POST":

        name1 = request.form.get("name1")
        image = request.files.get("image")

        if not name1:
            return {
                "success": False,
                "message": "Student name is required."
            }

        if not image:
            return {
                "success": False,
                "message": "No image received."
            }

        # Training images folder inside the project
        path = os.path.join(
            app.root_path,
            "Training images"
        )

        # Create folder if it doesn't exist
        os.makedirs(path, exist_ok=True)

        # Create filename
        filename = name1.strip() + ".png"

        filepath = os.path.join(
            path,
            filename
        )

        # Save the image captured by the browser
        image.save(filepath)

        print("Image saved:", filepath)

        return {
            "success": True,
            "message": "Student registered successfully!"
        }

    return render_template("index.html")
@app.route('/attendance', methods=['GET'])
def attendance():
    return render_template('attendance.html')

@app.route('/recognize_face', methods=['POST'])
def recognize_face():

    image = request.files.get("image")

    if not image:
        return {
            "success": False,
            "message": "No image received."
        }

    # Save the browser-captured image temporarily
    temp_path = os.path.join(
        app.root_path,
        "temp_attendance.png"
    )

    image.save(temp_path)

    # Load the captured image
    img = cv2.imread(temp_path)

    if img is None:
        return {
            "success": False,
            "message": "Could not read captured image."
        }

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Find faces in captured image
    captured_encodings = face_recognition.face_encodings(img_rgb)

    if len(captured_encodings) == 0:
        return {
            "success": False,
            "message": "No face detected. Please try again."
        }

    captured_encoding = captured_encodings[0]

    # Load registered students
    training_path = os.path.join(
        app.root_path,
        "Training images"
    )

    images = []
    classNames = []

    for filename in os.listdir(training_path):

        filepath = os.path.join(
            training_path,
            filename
        )

        training_img = cv2.imread(filepath)

        if training_img is None:
            continue

        training_rgb = cv2.cvtColor(
            training_img,
            cv2.COLOR_BGR2RGB
        )

        encodings = face_recognition.face_encodings(
            training_rgb
        )

        if len(encodings) == 0:
            continue

        images.append(encodings[0])
        classNames.append(
            os.path.splitext(filename)[0]
        )

    if len(images) == 0:
        return {
            "success": False,
            "message": "No valid registered faces found."
        }

    # Compare captured face with registered faces
    matches = face_recognition.compare_faces(
        images,
        captured_encoding,
        tolerance=0.50
    )

    face_distances = face_recognition.face_distance(
        images,
        captured_encoding
    )

    match_index = np.argmin(face_distances)

    if matches[match_index]:

        student_name = classNames[match_index].upper()

        # Record attendance
        mark_name = student_name

        now = datetime.now()
        time_string = now.strftime('%H:%M')
        today = date.today()

        conn = sqlite3.connect('information.db')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS Attendance
            (
                NAME TEXT NOT NULL,
                Time TEXT NOT NULL,
                Date TEXT NOT NULL
            )
        ''')

        conn.execute(
            '''
            INSERT INTO Attendance
            (NAME, Time, Date)
            VALUES (?, ?, ?)
            ''',
            (mark_name, time_string, today)
        )

        conn.commit()
        conn.close()

        # Delete temporary image
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {
            "success": True,
            "message": f"Attendance marked for {student_name}!"
        }

    # Delete temporary image
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return {
        "success": False,
        "message": "Face not recognized."
    }


@app.route('/login',methods = ['POST'])
def login():
    #print( request.headers )
    json_data = json.loads(request.data.decode())
    username = json_data['username']
    password = json_data['password']
    #print(username,password)
    df= pd.read_csv('cred.csv')
    if len(df.loc[df['username'] == username]['password'].values) > 0:
        if df.loc[df['username'] == username]['password'].values[0] == password:
            session['username'] = username
            return 'success'
        else:
            return 'failed'
    else:
        return 'failed'
        


@app.route('/checklogin')
def checklogin():
    #print('here')
    if 'username' in session:
        return session['username']
    return 'False'


@app.route('/how',methods=["GET","POST"])
def how():
    return render_template('form.html')
@app.route('/data',methods=["GET","POST"])
def data():
    '''user=request.form['username']
    pass1=request.form['pass']
    if user=="tech" and pass1=="tech@321" :
    '''
    if request.method=="POST":
        today=date.today()
        print(today)
        conn = sqlite3.connect('information.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print ("Opened database successfully");
        cursor = cur.execute("SELECT DISTINCT NAME,Time, Date from Attendance where Date=?",(today,))
        rows=cur.fetchall()
        print(rows)
        for line in cursor:

            data1=list(line)
        print ("Operation done successfully");
        conn.close()

        return render_template('form2.html',rows=rows)
    else:
        return render_template('form1.html')


            
@app.route('/whole',methods=["GET","POST"])
def whole():
    today=date.today()
    print(today)
    conn = sqlite3.connect('information.db')
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor() 
    print ("Opened database successfully");
    cursor = cur.execute("SELECT DISTINCT NAME,Time, Date from Attendance")
    rows=cur.fetchall()    
    return render_template('form3.html',rows=rows)

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def home():
    return render_template('main.html')
# Sending Email about the attendance report to the faculties/ parents / etc.
# Not working currently
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def sendMail():
    mssg=MIMEMultipart()


    server=smtplib.SMTP("smtp.gmail.com",'587')
    server.starttls()
    print("Connected with the server")
    user=input("Enter username:")
    pwd=input("Enter password:")
    server.login(user,pwd)
    print("Login Successful!")
    send=user
    rcv=input("Enter Receiver's Email id:")
    mssg["Subject"] = "Employee Report csv"
    mssg["From"] = user
    mssg["To"] = rcv

    body='''
        <html>
        <body>
         <h1>Employee Quarterly Report</h1>
         <h2>Contains the details of all the employees</h2>
         <p>Do not share confidential information with anyone.</p>
        </body>
        </html>
         '''

    body_part=MIMEText(body,'html')
    mssg.attach(body_part)

    with open("emp.csv",'rb') as f:
        mssg.attach(MIMEApplication(f.read(),Name="emp.csv"))

    server.sendmail(mssg["From"],mssg["To"],mssg.as_string())
   # server.quit()




if __name__ == '__main__':
    app.run(debug=True)



