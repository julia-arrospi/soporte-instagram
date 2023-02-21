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

## Archivos necesarios para correr la app

Se necesitan dos archivos para que la app funcione, que por seguridad no deben ser versionados así que están incluidos en la carpeta de la entrega del proyecto.

1. en `/mail` debe colocarse el archivo `config.py`

2. en el directorio raíz debe colocarse el archivo `ig_api.db`

## Para visualizar la BBDD

Recomendamos utilizar DBeaver para visualizar las tablas y sus datos.
[https://dbeaver.io/download/](https://dbeaver.io/download/)

Simplemente agregar una nueva conexión de SQLite, apuntando al archivo `ig_api.db`. A medida que se agreguen registros, refrescar la BBDD.
