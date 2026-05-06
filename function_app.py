import logging
import azure.functions as func

from data.input_data import load_input_data
from data.temp_tables import create_temp_tables
from data.queries import execute_queries
from report.generate_report import generate_excel_report
from report.upload_report import upload_excel_to_blob
from database.connection import db_connection
from email_service.send_email import send_email_with_attachment

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 0 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def pg_report_timer(myTimer: func.TimerRequest) -> None:

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    conn = db_connection()

    try:

        # input_data
        proveedor_datos, glns_proveedores, pdv_datos, glns_pdv, productos_datos, glns_productos = load_input_data()

        # temp_tables
        create_temp_tables(conn, proveedor_datos, pdv_datos, productos_datos)

        # queries
        final_query = execute_queries(conn, glns_proveedores, glns_pdv, glns_productos)

        # generate_report
        filename, excel_bytes = generate_excel_report(conn, final_query)

        # upload_report
        upload_excel_to_blob(excel_bytes, filename)
        send_email_with_attachment(excel_bytes, filename)
    
    except Exception:
        logging.error("An error occurred during the report generation process", exc_info=True)
    finally:
        conn.close()
