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
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Mail de prueba Soporte UTN</p> """

    message = MessageSchema(
        subject="Este es un mail generado por una API Rest",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
