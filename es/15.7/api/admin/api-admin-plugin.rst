==========================
API de Plugin
==========================

Vision General
==============

La API de Plugin es para gestionar los plugins (artefactos) de |Fess|.
Permite obtener la lista de plugins instalados y de plugins instalables, asi como instalar y eliminar plugins.

URL Base
========

::

    /api/admin/plugin

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /installed
     - Obtener lista de plugins instalados
   * - GET
     - /available
     - Obtener lista de plugins instalables
   * - POST
     - /
     - Instalar plugin
   * - DELETE
     - /
     - Eliminar plugin

Campos de Informacion del Plugin
=================================

Los endpoints de listado (``/installed`` y ``/available``) devuelven un arreglo ``plugins``
cuyos elementos son objetos con los siguientes campos.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Campo
     - Descripcion
   * - ``type``
     - ID de tipo del artefacto. Puede ser uno de: ``fess-ds`` (almacen de datos), ``fess-theme`` (tema),
       ``fess-ingest`` (Ingest), ``fess-script`` (script), ``fess-webapp`` (aplicacion web),
       ``fess-thumbnail`` (miniatura), ``fess-crawler`` (crawler), ``fess-llm`` (LLM),
       ``jar`` (JAR de proposito general no incluido en los anteriores).
   * - ``id``
     - Identificador con formato ``{name}:{version}``.
   * - ``name``
     - Nombre del plugin.
   * - ``version``
     - Version del plugin.
   * - ``url``
     - URL de descarga del artefacto. Solo se incluye en la respuesta de ``/available``. En ``/installed``
       el valor no existe, por lo que el campo se omite por completo.

.. note::

   En las respuestas de la API de |Fess|, los campos con valor ``null`` no se incluyen en la salida. Por ello,
   los elementos de plugins instalados no contienen el campo ``url``.

Obtener Lista de Plugins Instalados
====================================

Devuelve la lista de plugins instalados. Recorre los artefactos del directorio de plugins
por tipo y los devuelve ordenados por nombre.

Solicitud
---------

::

    GET /api/admin/plugin/installed

Respuesta
---------

En ``plugins`` se almacena un arreglo de objetos que representan la informacion de los plugins.
Consulte `Campos de Informacion del Plugin`_ para conocer los campos de cada objeto.
En los plugins instalados, ``url`` no se incluye en la salida.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Obtener Lista de Plugins Instalables
=====================================

Devuelve la lista de plugins instalables. Obtiene artefactos de todos los tipos desde los repositorios
configurados en ``plugin.repositories`` de ``fess_config.properties``.
Los resultados se almacenan en cache durante un tiempo determinado (5 minutos por defecto).

Solicitud
---------

::

    GET /api/admin/plugin/available

Respuesta
---------

En ``plugins`` se almacena un arreglo de objetos que representan la informacion de los plugins instalables.
Consulte `Campos de Informacion del Plugin`_ para conocer los campos de cada objeto.
Los plugins instalables incluyen el campo ``url`` con la URL de descarga.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0",
            "url": "https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-slack/15.7.0/fess-ds-slack-15.7.0.jar"
          }
        ]
      }
    }

Instalar Plugin
===============

Instala el plugin con el nombre y la version especificados.

Solicitud
---------

::

    POST /api/admin/plugin
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre del plugin (maximo 100 caracteres)
   * - ``version``
     - Si
     - Version del plugin (maximo 100 caracteres)

.. note::

   ``name`` y ``version`` deben coincidir con alguno de los plugins instalables obtenidos mediante ``/available``.
   Si no existe un artefacto que coincida, se devolvera un error.

Respuesta
---------

Cuando la solicitud es aceptada, se devuelve una respuesta con ``status`` igual a ``0`` (OK).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Si no existe un artefacto que corresponda a ``name`` o ``version``, ``status`` sera
``1`` (BAD_REQUEST) y ``message`` se establecera con ``invalid name or version``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "invalid name or version"
      }
    }

.. note::

   El proceso de instalacion se ejecuta de forma asincrona en segundo plano. La respuesta con ``status: 0``
   indica que la solicitud fue aceptada, pero no garantiza que la instalacion haya finalizado.
   Una vez completada la instalacion, si ya existian plugins con el mismo nombre pero distinta version,
   estos se eliminan automaticamente. Si la descarga o la instalacion fallan, el error se registra
   en el log del servidor, pero no se refleja en la respuesta de la API.

Eliminar Plugin
===============

Elimina el plugin con el nombre y la version especificados.

Solicitud
---------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre del plugin (maximo 100 caracteres)
   * - ``version``
     - No
     - Version del plugin (maximo 100 caracteres). Se recomienda especificarlo para identificar de forma unica el artefacto a eliminar.

Respuesta
---------

Cuando la solicitud es aceptada, se devuelve una respuesta con ``status`` igual a ``0`` (OK).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

.. note::

   El proceso de eliminacion se ejecuta de forma asincrona en segundo plano. La respuesta con ``status: 0``
   indica que la solicitud fue aceptada, pero no determina si el plugin existe ni si la eliminacion fue exitosa.
   Si la eliminacion falla (por ejemplo, si el archivo no existe), el error se registra en el log del servidor,
   pero no se refleja en la respuesta de la API.

Ejemplos de Uso
===============

Obtener Lista de Plugins Instalados
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

Instalar un Plugin
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Eliminar un Plugin
------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
