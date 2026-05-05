import pandas as pd
from azure.storage.blob import BlobServiceClient
import os
import io

container_name = "inputs-daily-report"

def read_csv_from_blob(blob_name: str) -> pd.DataFrame:

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    blob_data = blob_client.download_blob().readall()
    return pd.read_csv(io.BytesIO(blob_data), encoding='latin-1')

def load_input_data():
    
    df_prov = read_csv_from_blob("proveedores.csv")
    proveedor_datos = list(df_prov.itertuples(index=False, name=None))
    glns_proveedores = tuple(df_prov.iloc[:,0].astype(str).tolist())

    df_pdv = read_csv_from_blob("pdv.csv")
    pdv_datos = list(df_pdv.itertuples(index=False, name=None))
    glns_pdv = tuple(df_pdv.iloc[:,0].astype(str).tolist())

    df_prod = read_csv_from_blob("productos.csv")
    productos_datos = list(df_prod.itertuples(index=False, name=None))
    glns_productos = tuple(df_prod.iloc[:,0].astype(str).tolist())

    return (proveedor_datos,glns_proveedores, pdv_datos, glns_pdv, productos_datos, glns_productos)
