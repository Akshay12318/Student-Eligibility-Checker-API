# Student Eligibility API

This project is a **FastAPI**-based application that evaluates student eligibility for different courses based on their 12th-grade marks, age, gender, and qualification exams.

---

## Features
- Validates student details (name, age, gender, marks, desired course)
- Calculates eligibility for:
    - Engineering (JEE)
    - Medical (NEET)
    - Commerce and Humanities
- Stores data in **SQLite database**
- Provides **REST API endpoint** to check eligibility
- Automatically normalizes and cleans input data for accurate evaluation

---

## Project Structure
student_eligibility_api/
│
├── main.py # FastAPI backend
├── courses_data.py # Contains course data and subjects
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── students.db # SQLite database (created automatically)

## API Endpoint
**POST** `/check-eligibility`  
- Accepts student JSON data  
- Returns eligibility result with courses

## Libraries
Python 3.x (jupyter notebook)
FastAPI
SQLite3
Pandas
NumPy
Uvicorn


## Project workflow diagram
POST /check-eligibility
         │
         ▼
   Eligible Class
         │
         ▼
  everything() method
         │
   ┌─────────────Validation Chain─────────────┐
   │ name_check → age_check → gender_check → marks_check → desired_course_check │
   └──────────────────────────────────────────┘
         │
         ▼
   Data Cleaning & Normalization
         │
         ▼
   Store in SQLite Database
         │
         ▼
   Eligibility Calculation
         │
         ▼
   JSON Response (eligible courses)


## How to Run

1. Open **Anaconda Prompt** and navigate to the folder:
cd "C:\Users\Akshay sadaphule\MASTER CODE\student_eligibility_api"

2. -start the FASTAPI server
uvicorn main:app --reload

3.-Open in browser :-
http://127.0.0.1:8000/docs

____________________________________________________________________________________________________________________________



