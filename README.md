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

<img width="300" height="110" alt="image" src="https://github.com/user-attachments/assets/1cb8a22f-0ef4-44e9-8fe4-1fc7a87d263e" />


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

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/83ac1f23-4869-405c-bd06-2b49e0a0c216" />


## How to Run

1. Open **Anaconda Prompt** and navigate to the folder:
cd "C:\Users\Akshay sadaphule\MASTER CODE\student_eligibility_api"

2. -start the FASTAPI server
uvicorn main:app --reload

3.-Open in browser :-
http://127.0.0.1:8000/docs

____________________________________________________________________________________________________________________________



