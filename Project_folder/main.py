#!/usr/bin/env python
# coding: utf-8

# In[8]:


# main.py
import json
import re
import sqlite3
import pandas as pd
from pandas import json_normalize
import numpy as np
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from courses_data import courses

# ---------------- Original Class  ----------------
class Eligible:
    def __init__(self,json_data):
        self.json_data=json_data
        self.name_pattern =r'^[A-Za-z ]+$'
        self.age_pattern = r'^1[7-9]$'
        self.gender_cat = ["Male", "Female", "Other"]

        # database setup
        self.connection=sqlite3.connect("students.db", check_same_thread=False)
        self.cursor=self.connection.cursor()
        self.create_table()
        
    def name_check(self):
        name = self.json_data.get("name")
        if re.fullmatch(self.name_pattern, name, re.IGNORECASE):
            return self.age_check()
        else:
            return False
                    
    def age_check(self):
        age = str(self.json_data.get("age"))
        if re.fullmatch(self.age_pattern,age):
            return self.gender_check()
        else:
            return False
            
    def gender_check(self):
        gender = self.json_data.get("gender")
        if gender in self.gender_cat:
            return self.marks_check()
        else:
            return False
            
    def marks_check(self):
        marks=self.json_data.get("marks_12th")
        for subject,score in marks.items():
            if not (0 <= score <= 100):
                return False
        return self.desired_course_check()
                          
    def desired_course_check(self):
        desired_course=self.json_data.get("desired_course")
        for stream,subcourses in courses.items():
            if desired_course in subcourses.keys():
                return True 
        return False
    
    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            gender TEXT,
            marks_12th TEXT,
            qualification_exam TEXT,
            desired_course TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''')
        self.connection.commit()

    def data_clean(self):
        self.df = pd.json_normalize(self.json_data)
        self.numeric_cols= [x for x in self.df.columns if "age" in x or "qualification_exam.score" in x or "marks_12th" in x ]
        self.df[self.numeric_cols]=self.df[self.numeric_cols].apply(pd.to_numeric)

        self.string_cols=[x for x in self.df.columns if "gender" in x or "desired_course" in x or "name" in x]
        for x in self.string_cols:
            self.df[x]=self.df[x].str.title()

        self.cols=["name", "gender", "desired_course","qualification_exam.exam_name"]
        self.df[self.cols]=self.df[self.cols].replace("", "Unknown").fillna("Unknown")

        self.df.fillna(0, inplace = True)

    def engineer_course_eligible(self):
        PCM_total=(self.df["marks_12th.Physics"]+self.df["marks_12th.Chemistry"]+self.df["marks_12th.Maths"])
        PCM_percentage=(PCM_total/300)*100
        eligible_courses=[]
        if PCM_percentage.iloc[0]>=65:
            eligible_courses.append("Civil Engineering")
            if PCM_percentage.iloc[0]>=70:
                eligible_courses.extend(["Mechanical Engineering","Electrical Engineering","Electronics and Communication Engineering"])
                if PCM_percentage.iloc[0]>=75:
                    eligible_courses.append("Computer Science Engineering")
        return eligible_courses
                    
    def Medicine_course_eligible(self):
        PCB_total=(self.df["marks_12th.Physics"]+self.df["marks_12th.Chemistry"]+self.df["marks_12th.Biology"])
        PCB_percentage=(PCB_total/300)*100
        eligible_courses=[]
        if PCB_percentage.iloc[0]>=70:
            eligible_courses.append("BPT (Physiotherapy)")
            if PCB_percentage.iloc[0]>=75:
                eligible_courses.extend(["BAMS (Ayurveda)","BHMS (Homeopathy)"])
                if PCB_percentage.iloc[0]>=80:
                    eligible_courses.append("BDS (Dentistry)")
                    if PCB_percentage.iloc[0]>=85:
                        eligible_courses.append("MBBS")
        return eligible_courses

    def commerce_course_eligible(self):
        commerce_courses = courses["Commerce"]
        eligible_courses=[]
        for course_name,details in commerce_courses.items():
            required_subjects=details["subjects"]
            required_columns = [f"marks_12th.{subj}" for subj in required_subjects]
            
            if all(col in self.df.columns for col in required_columns):
                eligible_courses.append(course_name)
        if not eligible_courses:
            eligible_courses.extend(self.Humanities_course_eligible())
        return eligible_courses
                
    def Humanities_course_eligible(self):
        humanities_courses = courses["Humanities"]
        eligible_courses=[]
        for course_name,details in humanities_courses.items():
            required_subjects=details["subjects"]
            required_columns = [f"marks_12th.{subj}" for subj in required_subjects]
            
            if all(col in self.df.columns for col in required_columns):
                eligible_courses.append(course_name)
        return eligible_courses

    def sql_data(self):
        self.cursor.execute('''
            INSERT OR REPLACE INTO Students 
            (name, age, gender, marks_12th, qualification_exam, desired_course, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            self.json_data["name"],
            self.json_data["age"],
            self.json_data["gender"],
            json.dumps(self.json_data["marks_12th"]),
            self.json_data["qualification_exam"]["exam_name"],
            self.json_data["desired_course"]
        ))
        self.connection.commit()
        
    def everything(self):
        if not self.name_check():
            return {"status": "error", "message": "Validation failed"}

        self.data_clean()
        self.sql_data()

        # Determine eligible courses
        eligible_courses = []
        if (self.df["qualification_exam.exam_name"].str.upper() == "JEE").any():
            eligible_courses = self.engineer_course_eligible()
        elif (self.df["qualification_exam.exam_name"].str.upper() == "NEET").any():
            eligible_courses = self.Medicine_course_eligible()
        else:
            eligible_courses = self.commerce_course_eligible()

        return {
        "status": "success",
        "message": "Eligibility checked and stored",
        "eligible_courses": eligible_courses
        }



# ---------------- FastAPI ----------------
app = FastAPI()

@app.post("/check-eligibility")
async def check_eligibility(student: dict):
    obj = Eligible(student)
    result = obj.everything()
    return JSONResponse(content=result)


# In[11]:





# In[ ]:





# In[ ]:





# In[ ]:




