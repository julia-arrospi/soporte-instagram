from fastapi_mail import ConnectionConfig
import smtplib
import email.message


# Pedir los datos reales al grupo. El archivo final de configuración debe llamarse config.pygit status
conf = ConnectionConfig(
    MAIL_USERNAME="Tu dirección de mail",
    MAIL_PASSWORD="Tu password",
    MAIL_FROM="Tu dirección de mail",
    MAIL_PORT=587,
    MAIL_SERVER="Tu servidor SMTP",
    MAIL_FROM_NAME="Tu nombre",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


# Configuración para smtplib
server = smtplib.SMTP('Tu servidor SMTP:Puerto SMTP')
login = 'Tu dirección de correo'
password = 'Tu password'
msg = email.message.Message()
subject = 'Asunto'
