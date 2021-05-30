import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from PIL import Image

connection_string = os.getenv("AzureWebJobsStorage")

def main(myblob: func.InputStream):

    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = "samples-workitems"
    container_client = blob_service_client.get_container_client(container_name)

    output_width = 300
    created_md5 = "md5"

    output_blob = scaling_by_width(myblob, output_width)

    blob_client = container_client.get_blob_client(f"{output_width}/{created_md5}")
    blob_client.upload_blob(output_blob, blob_type="BlockBlob")

def scaling_by_width(input_blob: func.InputStream, output_width):

    input_stream = BytesIO(input_blob.read())
    input_img = Image.open(input_stream)
    
    wpercent = (output_width / float(input_img.size[0]))
    hsize = int((float(input_img.size[1]) * float(wpercent)))
    
    resized_image = input_img.resize((output_width, hsize), Image.ANTIALIAS)
    input_stream.close()

    output_byte_arr = BytesIO()
    resized_image.save(output_byte_arr, format='PNG')
    
    return output_byte_arr.getvalue()
