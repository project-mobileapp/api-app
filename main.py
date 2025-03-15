from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

app = FastAPI()

def get_db_connection():
    cnx = mysql.connector.connect(
        host= os.getenv("MYSQL_HOST"),
        user= os.getenv("MYSQL_username"),
        database= os.getenv("MYSQL_DATABASE")
    )
    return cnx

class User(BaseModel):
    full_name: str
    email: str
    password: str
    created_at: datetime
    update_at: datetime

@app.post("/user")
def create_user(user: User):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = '''
    INSERT INTO user (full_name, email, password, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (user.full_name, user.email, user.password, user.created_at, user.update_at))

    cnx.commit()
    user_id = cursor.lastrowid
    cursor.close()
    cnx.close()
    return {"id": user_id}

@app.get("/user")
def get_user():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT * FROM user"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    user = []
    for row in rows:
        user.append({
            "id": row[0],
            "fullname": row[1],
            "email": row[2],
            "created_at": row[4],
            "updated_at": row[5]
        })
        return user

@app.get('/')
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def read_hello():
    return {"message" : "Hello page"}

@app.get('/items/{id}')
def read_item(id:int):
    return {"items":id}