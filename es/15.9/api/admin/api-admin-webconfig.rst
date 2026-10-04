==========================
API de WebConfig
==========================

Visión General
==============

La API de WebConfig es para gestionar la configuración de rastreo web de |Fess|.
Puede operar configuraciones como URLs de rastreo, profundidad de rastreo y patrones de exclusión.

URL Base
========

::

    /api/admin/webconfig

.. note::

   Todos los endpoints requieren privilegios de administrador y un token de acceso válido.
   Consulte :doc:`api-admin-overview` para obtener información sobre la autenticación.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /settings
     - Obtener lista de configuraciones de rastreo web
   * - GET
     - /setting/{id}
     - Obtener configuración de rastreo web
   * - POST
     - /setting
     - Crear configuración de rastreo web
   * - PUT
     - /setting
     - Actualizar configuración de rastreo web
   * - DELETE
     - /setting/{id}
     - Eliminar configuración de rastreo web

Obtener Lista de Configuraciones de Rastreo Web
===============================================

Solicitud
---------

::

    GET /api/admin/webconfig/settings

.. note::

   El endpoint de lista también acepta ``PUT`` además de ``GET``.

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1)
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (predeterminado: 25, según la configuración ``paging.page.size``)
   * - ``name``
     - String
     - No
     - Filtrar por nombre de configuración
   * - ``urls``
     - String
     - No
     - Filtrar por URL de rastreo
   * - ``description``
     - String
     - No
     - Filtrar por descripción

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "Sitio de ejemplo",
            "urls": "https://example.com/",
            "included_urls": ".*example\\.com.*",
            "excluded_urls": ".*\\.(pdf|zip)$",
            "included_doc_urls": "",
            "excluded_doc_urls": "",
            "config_parameter": "",
            "depth": 3,
            "max_access_count": 1000,
            "user_agent": "Mozilla/5.0",
            "num_of_thread": 1,
            "interval_time": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtual_hosts": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

``total`` indica el número total de configuraciones que coinciden con los criterios de búsqueda.

Obtener Configuración de Rastreo Web
=====================================

Solicitud
---------

::

    GET /api/admin/webconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "Sitio de ejemplo",
          "urls": "https://example.com/",
          "included_urls": ".*example\\.com.*",
          "excluded_urls": ".*\\.(pdf|zip)$",
          "included_doc_urls": "",
          "excluded_doc_urls": "",
          "config_parameter": "",
          "depth": 3,
          "max_access_count": 1000,
          "user_agent": "Mozilla/5.0",
          "num_of_thread": 1,
          "interval_time": 1000,
          "boost": 1.0,
          "available": "true",
          "sort_order": 0,
          "permissions": "{role}admin",
          "virtual_hosts": "",
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   La respuesta incluye los campos de auditoría ``created_by``, ``created_time``,
   ``updated_by``, ``updated_time`` y ``version_no``, que son asignados automáticamente
   en el momento del registro o la actualización.
   ``version_no`` es obligatorio al actualizar (consulte la sección "Actualizar configuración de rastreo web" a continuación).

Crear Configuración de Rastreo Web
===================================

Solicitud
---------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe)$",
      "user_agent": "Mozilla/5.0",
      "num_of_thread": 3,
      "interval_time": 500,
      "boost": 1.0,
      "available": "true",
      "sort_order": 0,
      "permissions": "{role}admin\n{role}user"
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripción
   * - ``name``
     - Sí
     - Nombre de la configuración (máximo 200 caracteres)
   * - ``description``
     - No
     - Descripción de la configuración (máximo 1000 caracteres)
   * - ``urls``
     - Sí
     - URL de inicio de rastreo (separadas por salto de línea si son múltiples). Se especifica con ``http:`` o ``https:``
   * - ``included_urls``
     - No
     - Patrón de expresión regular para URLs a rastrear
   * - ``excluded_urls``
     - No
     - Patrón de expresión regular para URLs a excluir del rastreo
   * - ``included_doc_urls``
     - No
     - Patrón de expresión regular para URLs a indexar
   * - ``excluded_doc_urls``
     - No
     - Patrón de expresión regular para URLs a excluir del índice
   * - ``config_parameter``
     - No
     - Parámetros de configuración adicionales (formato ``key=value``, un elemento por línea)
   * - ``depth``
     - No
     - Profundidad de rastreo (0 o más)
   * - ``max_access_count``
     - No
     - Número máximo de accesos (0 o más)
   * - ``user_agent``
     - Sí
     - Cadena User-Agent (máximo 200 caracteres)
   * - ``num_of_thread``
     - Sí
     - Número de hilos paralelos (1 o más)
   * - ``interval_time``
     - Sí
     - Intervalo de acceso (milisegundos, 0 o más)
   * - ``boost``
     - Sí
     - Valor de impulso en resultados de búsqueda
   * - ``available``
     - Sí
     - Habilitado/Deshabilitado (cadena ``"true"`` / ``"false"``)
   * - ``sort_order``
     - Sí
     - Orden de visualización (0 o más)
   * - ``permissions``
     - No
     - Roles con permiso de acceso (separados por saltos de línea si son varios)
   * - ``virtual_hosts``
     - No
     - Hosts virtuales (separados por saltos de línea si son varios)

.. note::

   Los campos de auditoría como ``created_by``, ``created_time``, ``updated_by`` y ``updated_time``
   son asignados automáticamente por el servidor, por lo que no es necesario incluirlos en el cuerpo de la solicitud.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_webconfig_id",
        "created": true
      }
    }

Actualizar Configuración de Rastreo Web
=========================================

Solicitud
---------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

Al actualizar, además de los campos de creación, son obligatorios ``id`` para identificar
el registro a actualizar y ``version_no`` como número de versión.
En ``version_no`` se debe especificar el valor actual incluido en la respuesta de la API de consulta (GET).

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe|dmg)$",
      "user_agent": "Mozilla/5.0",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 5,
      "interval_time": 300,
      "boost": 1.2,
      "available": "true",
      "sort_order": 0,
      "version_no": 1
    }

Campos Adicionales para la Actualización
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripción
   * - ``id``
     - Sí
     - ID de la configuración a actualizar (máximo 1000 caracteres)
   * - ``version_no``
     - Sí
     - Número de versión actual del registro a actualizar. Se especifica el valor de ``version_no`` incluido en la respuesta de la API de consulta (GET)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_webconfig_id",
        "created": false
      }
    }

Eliminar Configuración de Rastreo Web
=======================================

Solicitud
---------

::

    DELETE /api/admin/webconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Ejemplos de Patrones de URL
============================

En ``included_urls`` / ``excluded_urls`` / ``included_doc_urls`` / ``excluded_doc_urls`` se utilizan expresiones regulares.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Patrón
     - Descripción
   * - ``.*example\\.com.*``
     - Todas las URLs que contienen example.com
   * - ``https://example\\.com/docs/.*``
     - Solo bajo /docs/
   * - ``.*\\.(pdf|doc|docx)$``
     - Archivos PDF, DOC, DOCX
   * - ``.*\\?.*``
     - URLs con parámetros de consulta
   * - ``.*/(login|logout|admin)/.*``
     - URLs que contienen rutas específicas

Ejemplos de Uso
===============

Configuración de Rastreo de Sitio Corporativo
---------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "included_urls": ".*www\\.example\\.com.*",
           "excluded_urls": ".*/(login|admin|api)/.*",
           "user_agent": "Mozilla/5.0",
           "depth": 5,
           "max_access_count": 10000,
           "num_of_thread": 3,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
           "permissions": "{role}guest"
         }'

Configuración de Rastreo de Sitio de Documentación
----------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "included_urls": ".*docs\\.example\\.com.*",
           "included_doc_urls": ".*\\.(html|htm)$",
           "user_agent": "Mozilla/5.0",
           "max_access_count": 50000,
           "num_of_thread": 5,
           "interval_time": 200,
           "boost": 1.5,
           "available": "true",
           "sort_order": 0
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-fileconfig` - API de configuración de rastreo de archivos
- :doc:`api-admin-dataconfig` - API de configuración de almacén de datos
- :doc:`../../admin/webconfig-guide` - Guía de configuración de rastreo web
