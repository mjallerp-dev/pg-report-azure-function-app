
import os
import base64
import logging
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
    """
    Envía un correo electrónico con un archivo Excel adjunto usando SendGrid.
    """

    try:
        # 1. Crear el mensaje base
        message = Mail(
            from_email=os.getenv("SENDGRID_FROM_EMAIL"),
            to_emails=os.getenv("SENDGRID_TO_EMAIL"),
            subject="Daily Sales and Inventory Report",
            html_content="""
                <p>Hello,</p>
                <p>The daily sales and inventory report is attached to this email.</p>
                <p>Regards,<br/>Azure Function App</p>
            """
        )

        # 2. Codificar el archivo Excel en Base64
        encoded_file = base64.b64encode(excel_bytes).decode()

        # 3. Crear el adjunto
        attachment = Attachment(
            FileContent(encoded_file),
            FileName(filename),
            FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            Disposition("attachment")
        )

        # 4. Asociar el adjunto al mensaje
        message.attachment = attachment

        # 5. Enviar el correo usando la API de SendGrid
        sendgrid_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sendgrid_client.send(message)

        logging.info("📧 Email sent successfully with attachment: %s", filename)

    except Exception:
        logging.error("❌ Error sending email with SendGrid", exc_info=True)
        raise
