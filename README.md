# Face Recognition-Based Attendance System

## Project Description
The Face Recognition-Based Attendance System is a Python-based application that automates the attendance tracking process using facial recognition technology. It captures and recognizes individuals' faces through a webcam and automatically records their attendance in an SQLite database.

The system uses OpenCV for face detection and recognition, Flask for the web application, and SQLite for storing attendance records. It reduces manual effort, minimizes attendance errors, and provides an efficient way to manage student attendance.

## Features
- **Face Detection:** Detects faces using a webcam.
- **Face Recognition:** Identifies registered individuals using facial recognition.
- **Automated Attendance:** Marks attendance automatically after successful face recognition.
- **Database Management:** Stores attendance records using SQLite.
- **Web Interface:** Provides an interface to manage and monitor attendance.
- **Attendance Tracking:** Maintains attendance records for future reference.

## Technologies Used
- Python
- OpenCV
- Flask
- HTML
- CSS
- SQLite

## How It Works
1. Register individuals and capture their facial images.
2. Train the face recognition model using the collected images.
3. Start the webcam to detect and recognize faces.
4. When a registered face is recognized, the system records attendance.
5. Attendance details are stored in the SQLite database.

## Project Objective
To develop an automated attendance management system that uses facial recognition to make attendance tracking faster, easier, and more reliable compared to traditional manual methods.

## Future Enhancements
- Email notifications for attendance updates.
- Admin dashboard for attendance management.
- Attendance reports with date-wise filtering.
- Improved recognition accuracy under different lighting conditions.
