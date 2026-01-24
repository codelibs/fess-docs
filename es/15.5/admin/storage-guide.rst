==============
Almacenamiento
==============

Descripción general
===================

La página de almacenamiento le permite administrar archivos en Amazon S3, Google Cloud Storage o almacenamiento compatible con S3 (como MinIO).

Método de gestión
==================

Configuración del servidor de almacenamiento de objetos
--------------------------------------------------------

Abra la configuración de almacenamiento desde [Sistema > General] y configure los siguientes elementos según su tipo de almacenamiento.

Configuración común
~~~~~~~~~~~~~~~~~~~

- Tipo: Tipo de almacenamiento (Automático/S3/GCS)
- Bucket: Nombre del bucket a administrar

Configuración de S3
~~~~~~~~~~~~~~~~~~~

- Punto de acceso: Punto de acceso de S3 (utiliza el predeterminado de AWS si está vacío)
- Clave de acceso: Clave de acceso de AWS
- Clave secreta: Clave secreta de AWS
- Región: Región de AWS

Configuración de GCS
~~~~~~~~~~~~~~~~~~~~

- Punto de acceso: Punto de acceso de GCS (utiliza el predeterminado de Google Cloud si está vacío)
- ID de proyecto: ID del proyecto de Google Cloud
- Ruta de credenciales: Ruta del archivo JSON de credenciales de la cuenta de servicio

Configuración de MinIO (compatible con S3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Punto de acceso: URL del punto de acceso del servidor MinIO
- Clave de acceso: Clave de acceso de MinIO
- Clave secreta: Clave secreta de MinIO


Método de visualización
-----------------------

Para abrir la página de lista de objetos que se muestra a continuación, haga clic en [Sistema > Almacenamiento] en el menú izquierdo.

|image0|


Nombre
::::::

Nombre del archivo del objeto


Tamaño
::::::

Tamaño del objeto


Fecha de última actualización
::::::::::::::::::::::::::::::

Fecha de última actualización del objeto

Descarga
--------

Puede descargar el objeto haciendo clic en el botón de descarga.


Eliminar
--------

Puede eliminar el objeto haciendo clic en el botón de eliminar.


Carga
-----

Puede abrir la ventana de carga de archivos haciendo clic en el botón de carga de archivos en la esquina superior derecha.


Crear carpeta
-------------

Puede abrir la ventana de creación de carpeta haciendo clic en el botón de crear carpeta a la derecha de la visualización de ruta. Tenga en cuenta que no se pueden crear carpetas vacías.


.. |image0| image:: ../../../resources/images/en/15.5/admin/storage-1.png
