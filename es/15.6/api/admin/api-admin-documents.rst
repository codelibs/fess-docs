==========================
API de Documents
==========================

Vision General
==============

La API de Documents es para gestionar documentos en el indice de |Fess|.
Puede realizar operaciones como eliminacion masiva, actualizacion y busqueda de documentos.

URL Base
========

::

    /api/admin/documents

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - DELETE
     - /
     - Eliminar documentos (especificando consulta)
   * - DELETE
     - /{id}
     - Eliminar documento (especificando ID)

Eliminar Documentos por Consulta
================================

Elimina masivamente los documentos que coinciden con una consulta de busqueda.

Solicitud
---------

::

    DELETE /api/admin/documents

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``q``
     - String
     - Si
     - Consulta de busqueda para eliminacion

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deleted": 150
      }
    }

Ejemplo de Uso
~~~~~~~~~~~~~~

.. code-block:: bash

    # Eliminar documentos de un sitio especifico
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Eliminar documentos antiguos
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO 2023-01-01]" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Eliminar documentos por etiqueta
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=label:old_label" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Documento por ID
=========================

Elimina un documento especificando su ID.

Solicitud
---------

::

    DELETE /api/admin/documents/{id}

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``id``
     - String
     - Si
     - ID del documento (parametro de ruta)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Ejemplo de Uso
~~~~~~~~~~~~~~

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/documents/doc_id_12345" \
         -H "Authorization: Bearer YOUR_TOKEN"

Sintaxis de Consulta
====================

Las consultas de eliminacion pueden usar la sintaxis de busqueda estandar de |Fess|.

Consultas Basicas
-----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Ejemplo de Consulta
     - Descripcion
   * - ``url:example.com``
     - Documentos con "example.com" en la URL
   * - ``url:https://example.com/*``
     - URLs con un prefijo especifico
   * - ``host:example.com``
     - Documentos de un host especifico
   * - ``title:keyword``
     - Documentos con palabra clave en el titulo
   * - ``content:keyword``
     - Documentos con palabra clave en el contenido
   * - ``label:mylabel``
     - Documentos con una etiqueta especifica

Consultas de Rango de Fechas
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Ejemplo de Consulta
     - Descripcion
   * - ``lastModified:[2023-01-01 TO 2023-12-31]``
     - Documentos actualizados dentro del periodo especificado
   * - ``lastModified:[* TO 2023-01-01]``
     - Documentos actualizados antes de la fecha especificada
   * - ``created:[2024-01-01 TO *]``
     - Documentos creados despues de la fecha especificada

Consultas Compuestas
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Ejemplo de Consulta
     - Descripcion
   * - ``url:example.com AND label:blog``
     - Condicion AND
   * - ``url:example.com OR url:sample.com``
     - Condicion OR
   * - ``NOT url:example.com``
     - Condicion NOT
   * - ``(url:example.com OR url:sample.com) AND label:news``
     - Agrupacion

Notas Importantes
=================

Precaucion al Eliminar
----------------------

.. warning::
   Las operaciones de eliminacion no se pueden deshacer. Asegurese de probar en un entorno de prueba antes de ejecutar en produccion.

- La eliminacion de grandes cantidades de documentos puede llevar tiempo
- El rendimiento del indice puede verse afectado durante la eliminacion
- Puede haber un ligero retraso antes de que los resultados de busqueda reflejen la eliminacion

Practicas Recomendadas
----------------------

1. **Confirmar antes de eliminar**: Use la API de busqueda con la misma consulta para verificar los documentos a eliminar
2. **Eliminacion gradual**: Ejecute eliminaciones masivas en multiples lotes
3. **Copia de seguridad**: Haga copia de seguridad de datos importantes con anticipacion

Ejemplos de Uso
===============

Preparacion para Re-rastreo de Sitio Completo
---------------------------------------------

.. code-block:: bash

    # Eliminar documentos antiguos de un sitio especifico
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=host:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Iniciar trabajo de rastreo
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Limpieza de Documentos Antiguos
-------------------------------

.. code-block:: bash

    # Eliminar documentos no actualizados en mas de 1 ano
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO now-1y]" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-crawlinginfo` - API de informacion de rastreo
- :doc:`../../admin/searchlist-guide` - Guia de gestion de lista de busqueda
