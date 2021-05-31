import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from PIL import Image
import hashlib
import mysql.connector

connection_string = os.getenv("AzureWebJobsStorage")
output_widths = os.getenv("OutputWidths")
db_host = os.getenv("DBHost")
db_username = os.getenv("DBUsername")
db_password = os.getenv("DBPassword")

def main(myblob: func.InputStream):

    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = "samples-workitems"
    container_client = blob_service_client.get_container_client(container_name)

    input_filename, extension = get_filename_and_extension(myblob.name)
    input_blob_bytes = BytesIO(myblob.read())

    for output_width in output_widths.split(","):
        output_blob = scaling_by_width(input_blob_bytes, int(output_width), extension)
        created_md5 = hashlib.md5(output_blob).hexdigest()

        blob_client = container_client.get_blob_client(f"{input_filename}/{output_width}/{created_md5}.{extension}")
        blob_client.upload_blob(output_blob, blob_type="BlockBlob")
        
    input_blob_bytes.close()

    db_connection = connect_database()
    insert_filepath(db_connection)  #TODO: This is just a POC.

def get_filename_and_extension(filepath):

    basename = os.path.splitext(os.path.basename(filepath))
    return basename[0], basename[1].lstrip(".")

def scaling_by_width(input_blob_bytes: BytesIO, output_width: int, extension):

    input_img = Image.open(input_blob_bytes)
    
    wpercent = (output_width / float(input_img.size[0]))
    hsize = int((float(input_img.size[1]) * float(wpercent)))
    
    resized_image = input_img.resize((output_width, hsize), Image.ANTIALIAS)

    output_byte_arr = BytesIO()
    resized_image.save(output_byte_arr, format=extension)
    
    return output_byte_arr.getvalue()

def connect_database():
    return mysql.connector.connect(
        user=db_username, 
        password=db_password, 
        host=db_host, 
        port=3306
    )
    
def insert_filepath(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""INSERT INTO imagefunctions.tasks(filepath) VALUES ('test')""")
    db_connection.commit()
