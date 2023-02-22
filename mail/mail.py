import string
from smtplib import SMTPException, SMTPDataError

import mail.config
import email.message
from email.utils import formataddr
from email.header import Header


def send_mail(user_post_email: string, user_post: string, user_comment: string, text_comment: string):
    email_content = """
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Soporte UTN Instagram</title>
    </head>
    <body>
    <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>
    <table id="top-message" cellpadding="20" cellspacing="0" width="600" align="center">
    <tr><td align="center"></td></tr></table>
    <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff"><tr><td>
    <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9"><tr>
    <td width="570" align="center" bgcolor="#d80a3e"><h1>Soporte UTN Instagram</h1></td>
    </tr><tr></tr></table></td></tr><tr><td>
    <table id="content-4" cellpadding="0" cellspacing="0" align="center"><tr>
    <td width="600" valign="top">
    <h3>{}, tienes un nuevo comentario</h3>
    <p><b>{}</b> ha escrito: "{}"</p></td></tr>
    </table>
    </body>
    </html>

    """.format(user_post, user_comment, text_comment)

    login = mail.config.login
    password = mail.config.password
    msg = email.message.Message()
    msg['Subject'] = mail.config.subject
    msg['From'] = formataddr((str(Header('Soporte UTN Instagram', 'utf-8')), login))
    msg['To'] = user_post_email
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    try:
        s = mail.config.server
        s .starttls()
        s.login(login, password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
    except SMTPException:
        print('\n********\nLímite diario de envío de emails excedido. '
              'Se creó el comentario pero no se envió notificación por email.\n********\n{')

