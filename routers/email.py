from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from starlette.responses import JSONResponse
from mail.config import conf

router = APIRouter(
  prefix='/email',
  tags=['email']
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


@router.post('')
async def massive_email_send(email: EmailSchema) -> JSONResponse:
    html = """
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
    <h3><b>¡Les deseamos a nuestros usuarios un feliz 2023!</b></h3>
    <p></p></td></tr>
    </table>
    </body>
    </html>

    """

    message = MessageSchema(
        subject="Notificación a los usuarios de Soporte UTN Instagram",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
