from azure.storage.blob import BlobServiceClient
import os

def upload_excel_to_blob(excel_bytes: bytes, filename: str):

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client("ddvi-report-storage")
    blob_client = container_client.get_blob_client(filename)

    blob_client.upload_blob(excel_bytes, overwrite=True)