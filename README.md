# NiñasCode
# Primera vez en el proyecto

### Clonar el repositorio. 
Para obtener el código del proyecto hay que descargarlo de Github haciendo 
```
git clone link-del-proyecto
```
Luego hay que entrar en la carpeta que se clonó recién haciendo 
```
cd nombre-carpeta
```

### Crear el ambiente virtual
Tenemos que crear un ambiente virtual con python 3 para correr el proyecto.
En este caso le pondremos 'env' a nuestro ambiente. 

```
python3 -m venv env 
```

Cada vez que vamos a abrir el proyecto hay que abrir el ambiente virtual. Esto se hace estando en la misma carpeta que la carpeta env (no dentro de env).
```
source env/bin/activate
```


### Iniciar el proyecto Django: 
Para iniciar el proyecto django hay que seguir una serie de pasos: 
1. ``` pip3 intstall requirements.txt ``` para instalar todas la librerías necesarias para el proyecto. 
> En caso que salga un error relacionado con C, al instalar rcssmin probar instalar con el siguiente comando: 
''' 
    pip install rcssmin --install-option="--without-c-extensions"
    pip install rjsmin --install-option="--without-c-extensions"
    pip install django-compressor --upgrade
'''
2.  ```python manage.py makemigrations``` para crear los archivos que crean las tablas de la base de datos. 
3. ```python manage.py migrate```  para crear las tablas de la base de datos. 
4. ```python manage.py collectstatic``` para crear los archivos estáticos del proyecto. 
5. ```python manage.py runserver ``` para correr la aplicación web.
6. En otra consola ejecutar `python run_server.py` o `python run_server_win.py` según tu sistema operativo cuando vayas a utilizar la revisión de soluciones. 

El paso 5 siempre se hace para correr el servidor, para poder acceder a la aplicación hay que entrar a _localhost:8000/_ o a _127.0.0.1:8000/_. 

En la siguiente carpeta encuentras ejemplos de enunciados, casos de prueba y soluciones para hacer pruebas: https://drive.google.com/drive/u/1/folders/16XIQIm0lMl6OVuNQjjZbepWmCkUlDoWu


### Crear datos
#### Con fixtures
Al iniciar el proyecto la base de datos va a estar vacía. 
Si el proyecto trae una carpeta _fixtures_ se puede llenar la base de datos con los datos de la fixture: 
```
python manage.py loaddata nombre-archivo-fixture.json
```
* `fixture_user_cursos_clases_asistencia`: Esta fixture trae data de todos los modelos que salen en su nombre. Los nombres de las usuarias y sus contraseñas las encontrarás en el archivo `Scripts_y_datos/creardbpequeño.py` 

#### Superusuario
Con o sin fixtures crearemos un super usuario que nos dará acceso al administrador de Django: 
```
python manage.py createsuperuser
```

Luego hay que entrar a _localhost:8000/admin_ e ingresar con las credenciales creadas antes y 
tendrás acceso a la mayoría de los datos de la base de datos. 

