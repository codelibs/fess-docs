================
Procedimiento de Instalación
================

Método de Instalación
================

Fess proporciona distribuciones como archivo ZIP, paquetes RPM/DEB e imágenes Docker.
Al utilizar Docker, puede configurar fácilmente Fess en Windows, Mac, etc.

Al construir un entorno de operación, asegúrese de consultar :doc:`15.3/install/index`.

.. warning::

   **Notas importantes para el entorno de producción**

   No se recomienda ejecutar con OpenSearch integrado en entornos de producción o pruebas de carga.
   Asegúrese de construir un servidor OpenSearch externo.

Instalación de Docker Desktop
============================

Aquí se explicará el método de uso en Windows.
Si Docker Desktop no está instalado, instálelo siguiendo el siguiente procedimiento.

Dado que el archivo a descargar y el procedimiento difieren según el sistema operativo, debe implementarlo de acuerdo con su entorno.
Para más detalles, consulte la documentación de `Docker <https://docs.docker.com/get-docker/>`_.

Descarga
------------

Descargue el instalador del sistema operativo correspondiente en `Docker Desktop <https://www.docker.com/products/docker-desktop/>`__.

Ejecución del Instalador
--------------------

Haga doble clic en el instalador descargado para iniciar la instalación.

Asegúrese de que "Install required Windows components for WSL 2" o
"Install required Enable Hyper-V Windows Features" esté seleccionado,
y haga clic en el botón OK.

|image0|

Una vez completada la instalación, haga clic en el botón "close" para cerrar la pantalla.

|image1|

Inicio de Docker Desktop
---------------------

Haga clic en "Docker Desktop" en el menú de Windows para iniciarlo.

|image2|

Después de iniciar Docker Desktop, se mostrarán los términos de uso, marque "I accept the terms" y haga clic en el botón "Accept".

Aparecerá una guía para iniciar el tutorial, pero haga clic en "Skip tutorial" para omitirlo.
Al hacer clic en "Skip tutorial", se mostrará el Dashboard.

|image3|

Configuración
====

Para que OpenSearch se pueda ejecutar como contenedor Docker, ajuste el valor de "vm.max_map_count" en el sistema operativo.
Dado que el método de configuración difiere según el entorno utilizado, consulte "`Set vm.max_map_count to at least 262144 <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144>`_" para cada método de configuración.

Configuración de Fess
==================

Creación de archivos de inicio
------------------

Cree una carpeta apropiada y descargue `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml>`_ y `compose-opensearch3.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml>`_.

También puede obtenerlos con el comando curl de la siguiente manera.

::

    curl -o compose.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -o compose-opensearch3.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

Inicio de Fess
----------

Inicie Fess con el comando docker compose.

Abra el símbolo del sistema, navegue a la carpeta donde se encuentra el archivo compose.yaml y ejecute el siguiente comando.

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   El inicio puede tardar varios minutos.
   Puede verificar los registros con el siguiente comando::

       docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

   Puede finalizar la visualización de registros con ``Ctrl+C``.


Verificación de Funcionamiento
========

Puede verificar el inicio accediendo a \http://localhost:8080/.

La interfaz de administración está en \http://localhost:8080/admin/.
El nombre de usuario/contraseña de la cuenta de administrador predeterminada es admin/admin.

.. warning::

   **Nota importante sobre seguridad**

   Asegúrese de cambiar la contraseña predeterminada.
   Especialmente en entornos de producción, se recomienda encarecidamente cambiar la contraseña inmediatamente después del primer inicio de sesión.

La cuenta de administrador es gestionada por el servidor de aplicaciones.
La interfaz de administración de Fess determina como administrador a los usuarios autenticados con el rol fess en el servidor de aplicaciones.

Otros
======

Detención de Fess
----------

Para detener Fess, ejecute el siguiente comando en la carpeta donde inició Fess.

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Para detener y eliminar contenedores::

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Para eliminar también los volúmenes con el comando ``down``, agregue la opción ``-v``.
   En este caso, todos los datos se eliminarán, así que tenga cuidado::

       docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Cambio de contraseña de administrador
----------------------

Puede cambiarlo en la pantalla de edición de usuario de la interfaz de administración.

.. |image0| image:: ../resources/images/ja/install/dockerdesktop-1.png
.. |image1| image:: ../resources/images/ja/install/dockerdesktop-2.png
.. |image2| image:: ../resources/images/ja/install/dockerdesktop-3.png
.. |image3| image:: ../resources/images/ja/install/dockerdesktop-4.png

