import smtplib
from email.message import EmailMessage

def mandar_correo_codigo(sender, receiver, password, codigo):
    email_subject = 'Código de Cambio de Contraseña'
    sender_email_address = sender
    receiver_email_address = receiver
    email_smtp = "smtp.gmail.com"
    email_password = password

    # Create an email message object
    message = EmailMessage()

    # Configure email headers
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address

    # Set email body text
    message.set_content(f"Su código para cambiar su contraseña es {codigo}")

    # Set smtp server and port
    server = smtplib.SMTP(email_smtp, '587')

    # Identify this client to the SMTP server
    server.ehlo()

    # Secure the SMTP connection
    server.starttls()

    # Login to email account
    server.login(sender_email_address, email_password)

    # Send email
    server.send_message(message)

    # Close connection to server
    server.quit()