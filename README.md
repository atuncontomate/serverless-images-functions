# Serverless Images Functions

Se trata de una aplicación que, mediante una función serverless en Azure Functions, procesa imágenes redimensionándolas a una serie de anchos configurados.

Su arquitectura consta de los siguientes componentes:

- **API REST**, desde la cual importar nuevas imágenes y conocer el estado de los procesos.
- **Función serverless**, encargada de procesar las imágenes de entrada y actualizar los procesos asociados.
- **Base de datos**, en la que se persiste la información sobre los procesos y las imágenes creadas.
- **Sistema de almacenamiento**, donde se alojan las imágenes originales y las resultantes.

## API REST

Su implementación está basada en **NodeJS**, está protegida mediante **HTTPS**, y se encuentra en el directorio `api-rest` de este repositorio. 
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
