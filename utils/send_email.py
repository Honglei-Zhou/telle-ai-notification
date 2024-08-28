import smtplib
import ssl
from server.config import mail_settings
import logging
from email.message import EmailMessage

logger = logging.getLogger()


def send_email(recipients, subject, body=None, bcc=None):

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        # msg['From'] = Address("No-Reply Telle", "noreply@telle.ai")
        msg['From'] = 'noreply@telle.ai'
        msg['To'] = ', '.join(recipients)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)

        if body:
            msg.set_content(body)

        server = smtplib.SMTP(mail_settings['MAIL_SERVER'], mail_settings['MAIL_PORT'])

        server.starttls(context=context)  # Secure the connection

        server.login(mail_settings['MAIL_USERNAME'], mail_settings['MAIL_PASSWORD'])

        print(msg)

        server.send_message(msg)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        logger.error(e)
    finally:
        if server:
            server.quit()
