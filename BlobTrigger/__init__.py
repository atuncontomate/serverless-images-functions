import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from PIL import Image
import hashlib

from repository import connection_utils
from repository import tasks_repository
from repository import images_repository
from utils.task_status_enum import TaskStatus

connection_string = os.getenv("AzureWebJobsStorage")
output_widths = os.getenv("OutputWidths")
container_name = os.getenv("ContainerName")

def main(myblob: func.InputStream):

    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    db_connection = connection_utils.connect_database()
    task_id = tasks_repository.get_task_id_by_filepath(db_connection, myblob.name)
    tasks_repository.update_task_status(db_connection, TaskStatus.PROCESSING, task_id)

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)
        
        input_filename, extension = get_filename_and_extension(myblob.name)
        input_blob_bytes = BytesIO(myblob.read())

        for output_width in output_widths.split(","):

            output_blob = scaling_by_width(input_blob_bytes, int(output_width), extension)
            created_md5 = hashlib.md5(output_blob).hexdigest()
            output_filepath = f"{input_filename}/{output_width}/{created_md5}.{extension}"

            blob_client = container_client.get_blob_client(output_filepath)
            blob_client.upload_blob(output_blob, blob_type="BlockBlob")

            images_repository.create_image(db_connection, created_md5, output_width, output_filepath)
        
        input_blob_bytes.close()
        
    except:
        tasks_repository.update_task_status(db_connection, TaskStatus.ERROR, task_id)
    else:
        tasks_repository.update_task_status(db_connection, TaskStatus.FINISHED, task_id)


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
