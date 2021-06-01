# Serverless Images Functions

Se trata de una aplicación que, mediante una función serverless en Azure Functions, procesa imágenes redimensionándolas a una serie de anchos configurados.

Su arquitectura consta de los siguientes componentes:

- **API REST**, desde la cual importar nuevas imágenes y conocer el estado de los procesos.
- **Función serverless**, encargada de procesar las imágenes de entrada y actualizar los procesos asociados.
- **Base de datos**, en la que se persiste la información sobre los procesos y las imágenes creadas.
- **Sistema de almacenamiento**, donde se alojan las imágenes originales y las resultantes. Será una cuenta de almacenamiento de Azure Blob Storage.

## API REST

Su implementación está basada en **NodeJS**, está protegida mediante **HTTPS**, y se encuentra en el directorio `/api-rest` de este repositorio. 
Contiene dos recursos: un endpoint `POST` para realizar la subida de imágenes, y un endpoint `GET` para recuperar el estado de los procesos de redimensión.

### Subida de imágenes

> POST - /tasks

Mediante este endpoint `POST`, subiremos una imagen a nuestro entorno remoto en Azure, y persistiremos en base de datos la información de este nuevo proceso de redimensión.
Este fichero de subida será almacenado en una cuenta de almacenamiento de Azure Blob Storage, en una ruta en la que nuestra función serverless esté escuchando.
Si la subida ha ido bien, este servicio creará en base de datos un registro con la información de esta nueva tarea.

Podremos invocar a nuestro endpoint de la siguiente forma:

```bash
$ curl --location --request POST 'https://localhost:3443/tasks' --form 'image=@"/home/path/<image_path>"'
```

La respuesta de este endpoint será el identificador de la tarea creada.

### Consulta del estado de una tarea

> GET - /tasks/:id

Mediante este endpoint `GET`, obtendremos el estado de la tarea cuyo identificador especifiquemos en la url. El estado de una tarea se encuentra persistido en base de datos, y será la función serverless quien lo actualice cada vez que sea necesario.
Una tarea podrá tener uno de los siguientes estados:

- PENDING: La imagen está esperando a ser redimensionada.
- PROCESSING: La imagen se está redimiensionado.
- FINISHED: La imagen se ha redimensionado correctamente, y se han guardado las imágenes resultantes correctamente.
- ERROR: Ocurrió algún error al procesr las imagen.

Podremos invocar a nuestro endpoint de la siguiente forma:

```bash
$ curl --location --request GET 'https://localhost:3443/tasks/<id>'
```

La respuesta de este endpoint será el estado de la tarea.

### :gear: Cómo iniciar el servidor

Ubicados en el directorio `/api-rest`, instalaremos las dependencias configuradas en el proyecto mediante el comando `npm install`.

Después, le daremos valor a las variables de entorno:
```
export ACCOUNT_NAME=<<blob_storage_account_name>>
export ACCOUNT_KEY=<<blob_storage_account_key>>
export CONTAINER_NAME=<<blob_storage_container_name>>
export HOST_NAME=<<database_host_name>>
export USER_NAME=<<database_user_name>>
export PASSWORD=<<database_user_password>>
```

Por último, arrancamos el servidor con el comando `node server.js`.

## Función serverless

Ha sido implementada en **Python**, desarrollada para correr en el stack de Azure, y se encuentra en el directorio `/serverless` de este repositorio. La función tiene configurado un disparador que escucha en el directorio `/input` del contenedor que configuremos, y cada vez que recibe un fichero se pone a trabajar.

Las operaciones que realiza son las siguientes:

1. Al recibir una imagen, extrae el path completo de dicha imagen y recupera el proceso correspondiente de base de datos mediante ese path.
2. Actualiza el proceso al estado `PROCESSING`.
3. Recupera de las variables de configuración los anchos a los que se tiene que redimensionar la imagen.
4. Para cada ancho, genera una imagen redimensionada y la almacena en el contenedor del Blob Storage.
5. Si todo ha ido bien, actualiza el estado del proceso a `FINISHED`. De lo contrario, si se ha producido algún error, actualiza el estado a `ERROR`.

:warning: La función ha sido probada con los formatos de imagen `.png` y `.jpg`.

### :gear: Configuración necesaria

Para ejecutar en el entorno remoto de Azure esta función, se deben añadir una serie de variables de configuración. Serán las siguientes:

```
OutputWidths=<<Output width, e.g "800,1024">>
AzureWebJobsStorage=<<storage connection string>>
ContainerName=<<container name>>
DBHost=<<database host>>
DBUsername=<<database username>>
DBPassword=<<database password>>
```

## Base de datos

La información de los procesos y las imágenes creadas se persistirá en una base de datos MySQL. Será necesario crear una base de datos MySQL que contenga un esquema llamado `imagefunctions`, en el cual crearemos las siguientes tablas:

```sql
CREATE TABLE Tasks (
    Id INT NOT NULL AUTO_INCREMENT,
    Filepath VARCHAR(255) NOT NULL,
    Status VARCHAR(20)NOT NULL,
    CreatedDate TIMESTAMP,
    LastModifiedDate TIMESTAMP,
    PRIMARY KEY (Id)
);
CREATE TABLE Images (
    Id INT NOT NULL AUTO_INCREMENT,
    CreatedDate TIMESTAMP,
    MD5 VARCHAR(32),
    Width INT,
    Filepath VARCHAR(255),
    PRIMARY KEY (Id)
);
```
