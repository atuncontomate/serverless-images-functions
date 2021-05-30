import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

connection_string = os.getenv("AzureWebJobsStorage")

def main(myblob: func.InputStream):

    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = "samples-workitems"
    container_client = blob_service_client.get_container_client(container_name)

    width = "width-dir"
    created_md5 = "md5"
    blob_client = container_client.get_blob_client(f"{width}/{created_md5}")
    blob_client.upload_blob(myblob, blob_type="BlockBlob")