==========================
Suggest API
==========================

Visión General
==============

La API de Suggest es una API para gestionar las palabras de sugerencia utilizadas por la funcionalidad de sugerencias de |Fess|.
Permite obtener información estadística sobre el número de palabras de sugerencia y eliminar palabras de sugerencia.

Las palabras de sugerencia incluyen las generadas a partir de documentos rastreados (derivadas de documentos) y
las generadas a partir de las consultas de búsqueda de los usuarios (derivadas de consultas de búsqueda). Esta API permite
eliminarlas por tipo o eliminarlas todas a la vez.

Autenticación
=============

El acceso a esta API requiere autenticación mediante un token de acceso. Especifique el token de acceso
en la cabecera de la solicitud.

::

    Authorization: Bearer <token de acceso>

El token de acceso debe tener el permiso de Admin API (por defecto ``Radmin-api``).
Para obtener información sobre cómo obtener un token de acceso y los detalles de los permisos, consulte :doc:`api-admin-overview`.

URL Base
========

::

    /api/admin/suggest

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /
     - Obtener información estadística de palabras de sugerencia
   * - DELETE
     - /all
     - Eliminar todas las palabras de sugerencia
   * - DELETE
     - /document
     - Eliminar palabras de sugerencia derivadas de documentos
   * - DELETE
     - /query
     - Eliminar palabras de sugerencia derivadas de consultas de búsqueda

Obtener Información Estadística de Palabras de Sugerencia
=========================================================

Obtiene información estadística sobre el número de palabras de sugerencia.

Solicitud
---------

::

    GET /api/admin/suggest

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 450
        }
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``setting.totalWordsNum``
     - Número total de palabras de sugerencia (número de palabras de sugerencia registradas en el índice de sugerencias)
   * - ``setting.documentWordsNum``
     - Número de palabras de sugerencia derivadas de documentos (número de palabras de sugerencia con frecuencia de documento igual o superior a 1)
   * - ``setting.queryWordsNum``
     - Número de palabras de sugerencia derivadas de consultas de búsqueda (número de palabras de sugerencia con frecuencia de consulta igual o superior a 1)

.. note::

   ``documentWordsNum`` y ``queryWordsNum`` no son excluyentes entre si. Si una palabra de sugerencia tiene origen
   tanto en documentos como en consultas de búsqueda, se incluye en el recuento de ambos. Por este motivo,
   la suma de ``documentWordsNum`` y ``queryWordsNum`` puede no coincidir con ``totalWordsNum``.

Eliminar Todas las Palabras de Sugerencia
=========================================

Elimina todas las palabras de sugerencia. Se eliminan todas las palabras de sugerencia del índice de sugerencias,
independientemente de si son derivadas de documentos o de consultas de búsqueda.

Solicitud
---------

::

    DELETE /api/admin/suggest/all

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Eliminar Palabras de Sugerencia Derivadas de Documentos
=======================================================

Elimina las palabras de sugerencia generadas a partir de documentos (palabras de sugerencia derivadas de documentos).

Solicitud
---------

::

    DELETE /api/admin/suggest/document

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Eliminar Palabras de Sugerencia Derivadas de Consultas de Búsqueda
==================================================================

Elimina las palabras de sugerencia generadas a partir de consultas de búsqueda (palabras de sugerencia derivadas de consultas de búsqueda).

Solicitud
---------

::

    DELETE /api/admin/suggest/query

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Respuesta de Error
==================

Si el proceso de eliminación falla, se devuelve el estado HTTP ``400`` y el campo ``status`` del cuerpo de la
respuesta se establece en ``1`` (BAD_REQUEST), con el campo ``message`` conteniendo el mensaje de error.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to delete a document."
      }
    }

Si el token de acceso no se especifica, no es válido o los permisos son insuficientes, el campo ``status`` del
cuerpo de la respuesta se establece en ``3`` (UNAUTHORIZED). Para consultar la lista de valores de ``status``
y códigos de estado HTTP, consulte :doc:`api-admin-overview`.

Ejemplos de Uso
===============

Obtener Información Estadística
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

Eliminar Palabras de Sugerencia Derivadas de Consultas de Búsqueda
------------------------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/query" \
         -H "Authorization: Bearer YOUR_TOKEN"

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-badword` - API de palabras prohibidas
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/suggest-guide` - Guía de gestión de sugerencias
