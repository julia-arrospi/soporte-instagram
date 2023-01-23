# Para ver la documentación autogenerada de Swagger:
http://127.0.0.1:8000/docs

Si no permite usar un endpoint, loguear con un usuario arriba de todo, donde dice Authorize.

## Para correr el entorno virtual
*win*
`.\env\bin\activate`

o 
*linux*
`.\env\bin\activate.bat`

## Requerimientos, estan dentro del entorno virtual env

`pip freeze > requirements.txt` hace un dump de los requerimientos en un archivo.

`pip install -r requirements.txt` instala todas las dependencias.

# Para correr la app:

`uvicorn main:app --reload`
