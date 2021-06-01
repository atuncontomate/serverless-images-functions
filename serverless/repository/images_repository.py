import os
import datetime

container_name = os.getenv("ContainerName")

def create_image(db_connection, md5_digest, width, filepath):
    cursor = db_connection.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO imagefunctions.images (CreatedDate, MD5, Width, Filepath) VALUES ('%s','%s','%s','%s')" 
        % (timestamp, md5_digest, width, container_name + "/" + filepath))
    db_connection.commit()