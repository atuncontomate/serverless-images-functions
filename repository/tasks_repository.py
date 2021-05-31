import os
from utils.task_status_enum import TaskStatus
import mysql.connector
import datetime

db_host = os.getenv("DBHost")
db_username = os.getenv("DBUsername")
db_password = os.getenv("DBPassword")
container_name = os.getenv("ContainerName")

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
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE imagefunctions.tasks SET Status='%s', LastModifiedDate='%s' WHERE Id = '%s'" % (status.value, timestamp, task_id))
    db_connection.commit()

def create_image(db_connection, md5_digest, width, filepath):
    cursor = db_connection.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO imagefunctions.images (CreatedDate, MD5, Width, Filepath) VALUES ('%s','%s','%s','%s')" 
        % (timestamp, md5_digest, width, container_name + "/" + filepath))
    db_connection.commit()
