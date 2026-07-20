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
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
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
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   La respuesta incluye los campos de auditoría ``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime`` y ``versionNo``, que son asignados automáticamente
   en el momento del registro o la actualización.
   ``versionNo`` es obligatorio al actualizar (consulte la sección "Actualizar configuración de rastreo web" a continuación).

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
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
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
   * - ``includedUrls``
     - No
     - Patrón de expresión regular para URLs a rastrear
   * - ``excludedUrls``
     - No
     - Patrón de expresión regular para URLs a excluir del rastreo
   * - ``includedDocUrls``
     - No
     - Patrón de expresión regular para URLs a indexar
   * - ``excludedDocUrls``
     - No
     - Patrón de expresión regular para URLs a excluir del índice
   * - ``configParameter``
     - No
     - Parámetros de configuración adicionales (formato ``key=value``, un elemento por línea)
   * - ``depth``
     - No
     - Profundidad de rastreo (0 o más)
   * - ``maxAccessCount``
     - No
     - Número máximo de accesos (0 o más)
   * - ``userAgent``
     - Sí
     - Cadena User-Agent (máximo 200 caracteres)
   * - ``numOfThread``
     - Sí
     - Número de hilos paralelos (1 o más)
   * - ``intervalTime``
     - Sí
     - Intervalo de acceso (milisegundos, 0 o más)
   * - ``boost``
     - Sí
     - Valor de impulso en resultados de búsqueda
   * - ``available``
     - Sí
     - Habilitado/Deshabilitado (cadena ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Sí
     - Orden de visualización (0 o más)
   * - ``permissions``
     - No
     - Roles con permiso de acceso (separados por saltos de línea si son varios)
   * - ``virtualHosts``
     - No
     - Hosts virtuales (separados por saltos de línea si son varios)

.. note::

   Los campos de auditoría como ``createdBy``, ``createdTime``, ``updatedBy`` y ``updatedTime``
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
el registro a actualizar y ``versionNo`` como número de versión.
En ``versionNo`` se debe especificar el valor actual incluido en la respuesta de la API de consulta (GET).

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
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
   * - ``versionNo``
     - Sí
     - Número de versión actual del registro a actualizar. Se especifica el valor de ``versionNo`` incluido en la respuesta de la API de consulta (GET)

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

En ``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` se utilizan expresiones regulares.

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
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
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
           "includedUrls": ".*docs\\.example\\.com.*",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-fileconfig` - API de configuración de rastreo de archivos
- :doc:`api-admin-dataconfig` - API de configuración de almacén de datos
- :doc:`../../admin/webconfig-guide` - Guía de configuración de rastreo web
