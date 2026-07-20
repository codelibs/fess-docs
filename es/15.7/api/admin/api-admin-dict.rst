==========================
API de Dict
==========================

Visión General
==============

La API de Dict es para gestionar los diccionarios de |Fess|.
En el endpoint raíz se puede obtener la lista de diccionarios disponibles.
La referencia, creación, actualización y eliminación de elementos de diccionario individuales, así como la carga y descarga de archivos de diccionario, se operan mediante los subendpoints por tipo de diccionario (synonym, kuromoji, mapping, protwords, stopwords, stemmeroverride).

URL Base
========

::

    /api/admin/dict

Lista de Endpoints
==================

Raíz del Diccionario
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /
     - Obtener lista de diccionarios

Endpoints por Tipo de Diccionario
----------------------------------

En ``{type}`` se especifica uno de ``synonym`` , ``kuromoji`` , ``mapping`` , ``protwords`` , ``stopwords`` , ``stemmeroverride`` .
Estos valores coinciden con el valor del campo ``type`` incluido en la respuesta de la lista de diccionarios.
``{dictId}`` es el ID del diccionario obtenido en la lista de diccionarios.

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /{type}/settings/{dictId}
     - Obtener lista de elementos del diccionario
   * - GET
     - /{type}/setting/{dictId}/{id}
     - Obtener elemento del diccionario
   * - POST
     - /{type}/setting/{dictId}
     - Crear elemento del diccionario
   * - PUT
     - /{type}/setting/{dictId}
     - Actualizar elemento del diccionario
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - Eliminar elemento del diccionario
   * - PUT
     - /{type}/upload/{dictId}
     - Cargar archivo de diccionario
   * - GET
     - /{type}/download/{dictId}
     - Descargar archivo de diccionario

Obtener Lista de Diccionarios
=============================

Obtiene la lista de archivos de diccionario disponibles.

Solicitud
---------

::

    GET /api/admin/dict

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "ZjA5...synonym.txt",
            "type": "synonym",
            "path": "/var/lib/fess/dict/synonym.txt",
            "timestamp": "2025-01-29T10:00:00.000+0000"
          },
          {
            "id": "ZjA5...mapping.txt",
            "type": "mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "timestamp": "2025-01-28T15:30:00.000+0000"
          }
        ],
        "total": 2
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``settings[].id``
     - ID del diccionario (usado como ``{dictId}`` en las operaciones de diccionario individuales)
   * - ``settings[].type``
     - Tipo de diccionario
   * - ``settings[].path``
     - Ruta del archivo de diccionario
   * - ``settings[].timestamp``
     - Fecha y hora de actualización del archivo de diccionario
   * - ``total``
     - Número total de archivos de diccionario

Obtener Lista de Elementos del Diccionario
==========================================

Obtiene la lista de elementos dentro del diccionario especificado.

Solicitud
---------

::

    GET /api/admin/dict/{type}/settings/{dictId}

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetros
     - Tipo
     - Requerido
     - Descripción
   * - ``dictId``
     - String
     - Sí
     - ID del diccionario (parámetro de ruta)
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (por defecto: 25)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, por defecto: 1)

Respuesta
---------

Los campos de cada elemento del arreglo ``settings`` de la respuesta varían según el tipo de diccionario (consulte "Campos de Elementos por Tipo de Diccionario" más adelante).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": 1,
            "dictId": "ZjA5...synonym.txt",
            "inputs": "busqueda,buscar",
            "outputs": "busqueda,buscar,investigar"
          }
        ],
        "total": 1
      }
    }

El ejemplo anterior corresponde al diccionario ``synonym``.

Obtener Elemento del Diccionario
================================

Obtiene un elemento específico dentro del diccionario.

Solicitud
---------

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetros
     - Tipo
     - Requerido
     - Descripción
   * - ``dictId``
     - String
     - Sí
     - ID del diccionario (parámetro de ruta)
   * - ``id``
     - Long
     - Sí
     - ID del elemento (parámetro de ruta)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "busqueda,buscar",
          "outputs": "busqueda,buscar,investigar"
        }
      }
    }

Crear Elemento del Diccionario
==============================

Crea un nuevo elemento en el diccionario.

Solicitud
---------

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Cuerpo de la Solicitud (ejemplo de synonym)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "busqueda,buscar",
      "outputs": "busqueda,buscar,investigar"
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

Actualizar Elemento del Diccionario
===================================

Actualiza un elemento existente dentro del diccionario.

Solicitud
---------

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Cuerpo de la Solicitud (ejemplo de synonym)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "busqueda,buscar",
      "outputs": "busqueda,buscar,investigar,search"
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Eliminar Elemento del Diccionario
=================================

Elimina un elemento dentro del diccionario.

Solicitud
---------

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetros
     - Tipo
     - Requerido
     - Descripción
   * - ``dictId``
     - String
     - Sí
     - ID del diccionario (parámetro de ruta)
   * - ``id``
     - Long
     - Sí
     - ID del elemento (parámetro de ruta)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Cargar Archivo de Diccionario
=============================

Carga y reemplaza el archivo de diccionario completo.

Solicitud
---------

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

El nombre del campo de archivo varía según el tipo de diccionario (consulte "Campos de Elementos por Tipo de Diccionario" más adelante).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Descargar Archivo de Diccionario
================================

Descarga el archivo de diccionario.

Solicitud
---------

::

    GET /api/admin/dict/{type}/download/{dictId}

La respuesta es el binario del archivo de diccionario ( ``application/octet-stream`` ).

Campos de Elementos por Tipo de Diccionario
===========================================

Los campos del cuerpo de la solicitud de creación y actualización de elementos del diccionario, así como los de la respuesta, varían según el tipo de diccionario.
``id`` (ID del elemento) y ``dictId`` (ID del diccionario) se incluyen en común en la respuesta.

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - Tipo
     - Campos de elemento
     - Campo de archivo de carga
   * - ``synonym``
     - ``inputs`` (requerido), ``outputs`` (requerido)
     - ``synonymFile``
   * - ``kuromoji``
     - ``token`` (requerido), ``segmentation`` (requerido), ``reading`` (requerido), ``pos`` (requerido)
     - ``kuromojiFile``
   * - ``mapping``
     - ``inputs`` (requerido), ``output``
     - ``charMappingFile``
   * - ``protwords``
     - ``input`` (requerido)
     - ``protwordsFile``
   * - ``stopwords``
     - ``input`` (requerido)
     - ``stopwordsFile``
   * - ``stemmeroverride``
     - ``input`` (requerido), ``output`` (requerido)
     - ``stemmerOverrideFile``

Ejemplos de Uso
===============

Obtener Lista de Diccionarios
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Lista de Elementos del Diccionario de Sinonimos
-------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

Agregar Elemento al Diccionario de Sinonimos
--------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "busqueda,buscar",
           "outputs": "busqueda,buscar,investigar"
         }'

Cargar Archivo del Diccionario de Sinonimos
-------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

Descargar Archivo del Diccionario de Sinonimos
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`../../admin/dict-guide` - Guía de gestión de diccionarios
