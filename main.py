from os import name
from fastapi import FastAPI
from sqlalchemy.sql.functions import user
from db import models
from db.database import engine
from routers import user, post, comment, email
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware

description = """
  Esta aplicación te permitirá subir tus fotos, encontrar a tus amigos y ver lo que están haciendo!. 🚀

  ## Users

  * Crear tu usuario, ver tu perfil y sus estadísticas.
  * Seguir a otros usuarios

  ## Posts

  Podrás:

  * Crear post.
  * Ver todos los posts.
  * Agregar una imagen a un post.
  * Eliminar un post

  **IMPORTANTE**
  > Al subir una imagen, el parámetro `image_url_type` acepta dos valores: absolute o relative. Las imagenes relativas no están implementadas automaticamente ya que requieren de un front-end, y limitamos el desarrollo al backend. Por lo tanto, en la ruta deberá ponerse una imagen sacada de internet con la ruta absoluta. (Ver ejemplos ya subidos)
  >
  > **Por ejemplo:**
  > `image_url`: "https://img.freepik.com/foto-gratis/bodegon-primer-plano-flor-interior_23-2148965612.jpg?w=2000"
  > `image_url_type`: "absolute"

  ## Comentarios

  Podrás:

  * Crear un comentario para un post.
  * Ver todos los comentarios de un post.

  ## Emails
  
  Envío masivo de emails. Envía un email con datos de prueba para implementar mensajes masivos a todos los usuarios.

  """

app = FastAPI(
  title="Soporte UTN Instagram",
  description=description,
  version="0.0.1",
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(email.router)
app.include_router(authentication.router)

@app.get("/")
def root():
  return "Bienvenido a Instagram"


origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:3002'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)


models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')