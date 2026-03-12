==========================
API de Dict
==========================

Vision General
==============

La API de Dict es para gestionar archivos de diccionario de |Fess|.
Puede gestionar diccionarios de sinonimos, diccionarios de mapeo, diccionarios de palabras protegidas, etc.

URL Base
========

::

    /api/admin/dict

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /
     - Obtener lista de diccionarios
   * - GET
     - /{id}
     - Obtener contenido del diccionario
   * - PUT
     - /{id}
     - Actualizar contenido del diccionario
   * - POST
     - /upload
     - Cargar archivo de diccionario

Obtener Lista de Diccionarios
=============================

Solicitud
---------

::

    GET /api/admin/dict

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dicts": [
          {
            "id": "synonym",
            "name": "Diccionario de sinonimos",
            "path": "/var/lib/fess/dict/synonym.txt",
            "type": "synonym",
            "updatedAt": "2025-01-29T10:00:00Z"
          },
          {
            "id": "mapping",
            "name": "Diccionario de mapeo",
            "path": "/var/lib/fess/dict/mapping.txt",
            "type": "mapping",
            "updatedAt": "2025-01-28T15:30:00Z"
          },
          {
            "id": "protwords",
            "name": "Diccionario de palabras protegidas",
            "path": "/var/lib/fess/dict/protwords.txt",
            "type": "protwords",
            "updatedAt": "2025-01-27T12:00:00Z"
          }
        ],
        "total": 3
      }
    }

Obtener Contenido del Diccionario
=================================

Solicitud
---------

::

    GET /api/admin/dict/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dict": {
          "id": "synonym",
          "name": "Diccionario de sinonimos",
          "path": "/var/lib/fess/dict/synonym.txt",
          "type": "synonym",
          "content": "busqueda,buscar,search\nFess,fess\nbusqueda de texto completo,full-text search",
          "updatedAt": "2025-01-29T10:00:00Z"
        }
      }
    }

Actualizar Contenido del Diccionario
====================================

Solicitud
---------

::

    PUT /api/admin/dict/{id}
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "content": "busqueda,buscar,search,query\nFess,fess\nbusqueda de texto completo,full-text search"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``content``
     - Si
     - Contenido del diccionario (separado por saltos de linea)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary updated successfully"
      }
    }

Cargar Archivo de Diccionario
=============================

Solicitud
---------

::

    POST /api/admin/dict/upload
    Content-Type: multipart/form-data

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="type"

    synonym
    --boundary
    Content-Disposition: form-data; name="file"; filename="synonym.txt"
    Content-Type: text/plain

    busqueda,buscar,search
    Fess,fess
    --boundary--

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``type``
     - Si
     - Tipo de diccionario (synonym/mapping/protwords/stopwords)
   * - ``file``
     - Si
     - Archivo de diccionario

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary uploaded successfully"
      }
    }

Tipos de Diccionario
====================

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tipo
     - Descripcion
   * - ``synonym``
     - Diccionario de sinonimos (expande sinonimos durante la busqueda)
   * - ``mapping``
     - Diccionario de mapeo (normalizacion de caracteres)
   * - ``protwords``
     - Diccionario de palabras protegidas (palabras excluidas del stemming)
   * - ``stopwords``
     - Diccionario de palabras vacias (palabras excluidas del indice)
   * - ``kuromoji``
     - Diccionario Kuromoji (analisis morfologico japones)

Ejemplos de Formato de Diccionario
==================================

Diccionario de Sinonimos
------------------------

::

    # Especificar sinonimos separados por comas
    busqueda,buscar,search,query
    Fess,fess
    busqueda de texto completo,full-text search

Diccionario de Mapeo
--------------------

::

    # antes de conversion => despues de conversion
    0 => 0
    1 => 1
    2 => 2

Diccionario de Palabras Protegidas
----------------------------------

::

    # Palabras a proteger del procesamiento de stemming
    running
    searching
    indexing

Ejemplos de Uso
===============

Obtener Lista de Diccionarios
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Contenido del Diccionario de Sinonimos
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN"

Actualizar Diccionario de Sinonimos
-----------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "content": "busqueda,buscar,search\nFess,fess\ndocumento,document"
         }'

Cargar Archivo de Diccionario
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "type=synonym" \
         -F "file=@synonym.txt"

Notas Importantes
=================

- Despues de actualizar un diccionario, puede ser necesario reconstruir el indice
- Archivos de diccionario grandes pueden afectar el rendimiento de busqueda
- Use codificacion UTF-8 para los archivos de diccionario

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`../../admin/dict-guide` - Guia de gestion de diccionarios
