import os
import base64
import logging
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition
)

def send_email_with_attachment(excel_bytes: bytes, filename: str):

    try:
        date_now = datetime.now().strftime('%Y-%m-%d')
        date_report = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M')
        message = Mail(
            from_email=os.getenv("SENDGRID_FROM_EMAIL"),
            to_emails=os.getenv("SENDGRID_TO_EMAIL"),
            subject=f"Reporte diario de ventas e inventarios {date_now}",
            html_content=f"""
                <div style="
                    background-color:#4472C4;
                    color:white;
                    padding:15px;
                    text-align:center;
                    font-size:18px;
                    font-weight:bold;
                    border-radius:5px;
                ">
                    REPORTE DIARIO DE VENTAS E INVENTARIO

                </div>

                <p>Este es un correo electrónico automático.</p>

                <p>Hola,</p>

                <p>Adjunto te comparto el archivo con la información diaria de ventas e inventarios de las cadenas Éxito, Olimpica y Alkosto, correspondiente a {date_report}.</p>
                
                <p>Saludos,<br/>Azure Function App</p>
            """
        )

        encoded_file = base64.b64encode(excel_bytes).decode()

        attachment = Attachment(
            FileContent(encoded_file),
            FileName(filename),
            FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            Disposition("attachment")
        )

        message.attachment = attachment

        sendgrid_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sendgrid_client.send(message)

        logging.info("📧 Email sent successfully with attachment: %s", filename)

    except Exception:
        logging.error("❌ Error sending email with SendGrid", exc_info=True)
        raise
