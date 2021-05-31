import os
from utils.task_status_enum import TaskStatus
import mysql.connector

db_host = os.getenv("DBHost")
db_username = os.getenv("DBUsername")
db_password = os.getenv("DBPassword")

def connect_database():
    return mysql.connector.connect(
        user=db_username, 
        password=db_password, 
        host=db_host, 
        port=3306
    )

def get_task_id_by_filepath(db_connection, filepath):
    cursor = db_connection.cursor()
    cursor.execute("SELECT id from imagefunctions.tasks WHERE filepath = '%s'" % (filepath))
    return cursor.fetchone()[0]

def update_task_status(db_connection, status: TaskStatus, task_id):
    cursor = db_connection.cursor()
    cursor.execute("UPDATE imagefunctions.tasks SET Status='%s' WHERE Id = '%s'" % (status.value, task_id))
    db_connection.commit()