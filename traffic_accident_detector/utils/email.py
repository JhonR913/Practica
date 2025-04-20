import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_accident_email(to_email, accident_details):
    """
    Envía un correo electrónico cuando se detecta un accidente.
    """
    from_email = "your_email@example.com"
    from_password = "your_password"
    
    # Configuración del mensaje de correo
    subject = "Accidente Detectado"
    body = f"Se ha detectado un accidente. Detalles: {accident_details}"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establecer la conexión con el servidor SMTP y enviar el correo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
