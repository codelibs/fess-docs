==========================
API de Suggest
==========================

Vision General
==============

La API de Suggest es una API para gestionar la funcionalidad de sugerencias de |Fess|.
Permite obtener informacion estadistica de las palabras de sugerencia y eliminar palabras de sugerencia.

URL Base
========

::

    /api/admin/suggest

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
     - Obtener informacion estadistica de palabras de sugerencia
   * - DELETE
     - /all
     - Eliminar todas las palabras de sugerencia
   * - DELETE
     - /document
     - Eliminar palabras de sugerencia derivadas de documentos
   * - DELETE
     - /query
     - Eliminar palabras de sugerencia derivadas de consultas de busqueda

Obtener Informacion Estadistica de Palabras de Sugerencia
=========================================================

Obtiene informacion estadistica sobre el numero de palabras de sugerencia.

Solicitud
---------

::

    GET /api/admin/suggest

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 300
        }
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``setting.totalWordsNum``
     - Numero total de palabras de sugerencia
   * - ``setting.documentWordsNum``
     - Numero de palabras de sugerencia derivadas de documentos
   * - ``setting.queryWordsNum``
     - Numero de palabras de sugerencia derivadas de consultas de busqueda

Eliminar Todas las Palabras de Sugerencia
=========================================

Elimina todas las palabras de sugerencia.

Solicitud
---------

::

    DELETE /api/admin/suggest/all

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Eliminar Palabras de Sugerencia Derivadas de Documentos
=======================================================

Elimina las palabras de sugerencia generadas a partir de documentos.

Solicitud
---------

::

    DELETE /api/admin/suggest/document

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Eliminar Palabras de Sugerencia Derivadas de Consultas de Busqueda
==================================================================

Elimina las palabras de sugerencia generadas a partir de consultas de busqueda.

Solicitud
---------

::

    DELETE /api/admin/suggest/query

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Ejemplos de Uso
===============

Obtener Informacion Estadistica
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Todas las Palabras de Sugerencia
-----------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Palabras de Sugerencia Derivadas de Documentos
-------------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-badword` - API de palabras prohibidas
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/suggest-guide` - Guia de gestion de sugerencias
