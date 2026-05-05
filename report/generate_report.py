import pandas as pd
from io import BytesIO
from datetime import datetime
import logging

def generate_excel_report(db_connection, final_query_string):

    try:

        df = pd.read_sql(final_query_string, db_connection)
        filename = f"reporte_ventas_inv_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        output = BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Report')
            worksheet = writer.sheets['Report']
   
            (max_row, max_col) = df.shape
            column_settings = [{'header': column} for column in df.columns]

            worksheet.add_table(0, 0, max_row, max_col - 1, {
                'columns': column_settings,
                'style': 'Table Style Medium 9',
                'name': 'TablaVentas'           
            })

            for i, col in enumerate(df.columns):
                width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, width)

        output.seek(0)
        logging.info("Excel report generated: %s", filename)
        return filename, output.getvalue()

    except Exception:
        logging.error(f"[ERROR] Ha ocurrido un error durante el proceso", exc_info=True)
    finally:
        db_connection.close()