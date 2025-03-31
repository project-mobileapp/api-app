from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os
import mysql.connector

# โหลดตัวแปรจาก .env
load_dotenv()

# สร้าง FastAPI instance
app = FastAPI()

# ตั้งค่า CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือกำหนด origin ที่เฉพาะเจาะจง
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API By Kittiphong"}

# ฟังก์ชันเชื่อมต่อฐานข้อมูล
def get_db_connection():
    try:
        cnx = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USERNAME"),  # แก้ชื่อเป็น MYSQL_USERNAME
            password=os.getenv("MYSQL_PASSWORD"),  # เพิ่ม password (ถ้ามี)
            database=os.getenv("MYSQL_DATABASE"),
            auth_plugin="mysql_native_password"  # ป้องกันปัญหา login
        )
        return cnx
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# Data Model สำหรับ User
class User(BaseModel):
    username: str
    email: str
    password: str
    createtime: datetime
    updatetime: datetime

# สร้าง User
@app.post("/user")
def create_user(user: User):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    try:
        query = '''
        INSERT INTO user (username, email, password, createtime, updatetime)
        VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (user.username, user.email, user.password, 
                               user.createtime, user.updatetime))
        cnx.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "message": "User created successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Insert error: {err}")
    finally:
        cursor.close()
        cnx.close()

# ดึงข้อมูล User
@app.get("/user")
def get_user():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)  # คืนค่าเป็น dictionary
    try:
        query = "SELECT * FROM user"
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Fetch error: {err}")
    finally:
        cursor.close()
        cnx.close()

# ดึงข้อมูล Goal
@app.get("/goal")
def get_goal():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    try:
        query = "SELECT * FROM goal_score"
        cursor.execute(query)
        goals = cursor.fetchall()
        return goals
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Fetch error: {err}")
    finally:
        cursor.close()
        cnx.close()  # ตรงนี้ปิดให้ถูกต้อง
