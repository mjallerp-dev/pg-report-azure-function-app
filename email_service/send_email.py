import smtplib
import os
import logging
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def send_email_with_attachment(excel_bytes: bytes, filename: str):

    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("APP_PASSWORD")
    receiver = [email.strip() for email in os.getenv("EMAIL_RECEIVER").split(",")]

    try:
        date_now = datetime.now().strftime('%Y-%m-%d')
        date_report = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M')

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ", ".join(receiver)
        msg['Subject'] = f"Reporte diario de ventas e inventarios {date_now}"

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

        msg.attach(MIMEText(html_content, 'html'))

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(excel_bytes)
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={filename}'
        )
        msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)


        logging.info("📧 Email sent successfully with attachment: %s", filename)

    except Exception:
        logging.error("❌ Error sending email with SendGrid", exc_info=True)
        raise
