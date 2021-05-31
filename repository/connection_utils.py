import os
import mysql.connector

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