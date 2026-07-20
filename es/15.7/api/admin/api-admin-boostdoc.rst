==========================
BoostDoc API
==========================

Visión General
==============

La API de BoostDoc es para gestionar la configuración de impulso de documentos de |Fess|.
Al configurar el impulso de documentos, puede elevar la puntuación de los documentos que
coincidan con ciertas condiciones y hacer que aparezcan con mayor facilidad en las posiciones
superiores de los resultados de búsqueda.

El impulso se aplica a cada documento en el momento de la indexación (durante el rastreo).
La condición (``urlExpr``) y el valor de impulso (``boostExpr``) se evaluan ambos como expresiones Groovy.
Las reglas múltiples se evaluan en orden ascendente según ``sortOrder``, y solo se aplica el valor de
impulso de la primera regla cuya condición coincida (una vez encontrada una regla que coincida,
las reglas siguientes no se evaluan).

.. note::

   En el panel de administración, ``urlExpr`` se muestra como "Condición" y ``boostExpr`` como "Expresión de valor de impulso".
   Para más detalles sobre los elementos de configuración, consulte :doc:`../../admin/boostdoc-guide`.

URL Base
========

::

    /api/admin/boostdoc

Autenticación
=============

Para usar esta API, se requiere un token de acceso con el permiso ``Radmin-api``.
Consulte :doc:`api-admin-overview` para conocer como obtener y especificar el token de acceso.

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
     - Obtener lista de impulsos de documentos
   * - GET
     - /setting/{id}
     - Obtener impulso de documento
   * - POST
     - /setting
     - Crear impulso de documento
   * - PUT
     - /setting
     - Actualizar impulso de documento
   * - DELETE
     - /setting/{id}
     - Eliminar impulso de documento

Obtener Lista de Impulsos de Documentos
========================================

Solicitud
---------

::

    GET /api/admin/boostdoc/settings

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (predeterminado: 25)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1. Predeterminado: 1)
   * - ``urlExpr``
     - String
     - No
     - Filtrado por expresión de condición (coincidencia parcial)
   * - ``boostExpr``
     - String
     - No
     - Filtrado por expresión de valor de impulso (coincidencia parcial)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "boostdoc_id_1",
            "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
            "boostExpr": "3.0",
            "sortOrder": 1,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Además de los campos mostrados anteriormente, cada objeto de configuración en la respuesta incluye también metadatos de creación/actualización (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``).
   ``versionNo`` es obligatorio al actualizar (PUT), por lo que debe obtener su valor actual mediante la API de obtención individual o de lista antes de actualizar.

Obtener Impulso de Documento
=============================

Solicitud
---------

::

    GET /api/admin/boostdoc/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
          "boostExpr": "3.0",
          "sortOrder": 1,
          "versionNo": 1
        }
      }
    }

Crear Impulso de Documento
===========================

Solicitud
---------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``urlExpr``
     - Sí
     - Expresión de condición. Expresión Groovy que determina los documentos objetivo del impulso y devuelve ``Boolean``. Corresponde a "Condición" en el panel de administración (máximo 10000 caracteres).
   * - ``boostExpr``
     - Sí
     - Expresión de valor de impulso. Expresión Groovy que devuelve el valor de impulso (numérico). También se puede especificar un valor fijo como ``3.0``. Corresponde a "Expresión de valor de impulso" en el panel de administración (máximo 10000 caracteres).
   * - ``sortOrder``
     - Sí
     - Orden de aplicación. Las reglas se evaluan en orden ascendente y se aplica el valor de impulso de la primera regla cuya condición coincida (valor inicial del formulario: 0; entero mayor o igual a 0).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Actualizar Impulso de Documento
================================

Solicitud
---------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

Al actualizar, además de los campos utilizados al crear, ``id`` (el identificador de la regla objetivo, hasta 1000 caracteres) y ``versionNo`` (el número de versión para bloqueo optimista) son obligatorios. Especifique el número de versión actual obtenido desde la respuesta de la API de obtención individual o de lista para ``versionNo``. La actualización falla si el número de versión no coincide.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

Eliminar Impulso de Documento
==============================

Solicitud
---------

::

    DELETE /api/admin/boostdoc/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Acerca de las Expresiones de Condición y de Valor de Impulso
=============================================================

``urlExpr`` (condición) y ``boostExpr`` (expresión de valor de impulso) se evaluan ambas como expresiones Groovy.
Dentro de la expresión, se pueden referenciar los valores de campo del documento a indexar como variables con el nombre del campo.

- ``urlExpr`` debe devolver ``Boolean`` (ejemplo: ``url.startsWith("https://docs.example.com/")``). Una simple cadena de expresión regular (ejemplo: ``.*docs\.example\.com.*``) no devuelve ``Boolean`` como expresión Groovy y por lo tanto no funciona como condición. Para usar expresiones regulares, utilice ``String#matches`` de Groovy.
- ``boostExpr`` debe devolver un valor numérico. El resultado se convierte a ``float`` y el impulso se aplica solo si es mayor que 0.

.. note::

   Principales variables de campo disponibles dentro de la expresión: ``url``, ``title``, ``content``, ``content_length``, ``last_modified``, entre otros.
   ``click_count`` y ``favorite_count`` están disponibles cuando ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled`` están habilitados (ambos habilitados por defecto).
   La sintaxis de calculo de fechas de OpenSearch como ``now - 7d`` no se puede usar en Groovy.

Ejemplos de Expresión de Condición (``urlExpr``)
-------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expresión de condición
     - Descripción
   * - ``url.startsWith("https://docs.example.com/")``
     - Aplica a documentos cuya URL comienza con la URL especificada
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - Evalua la URL mediante expresión regular (``String#matches`` de Groovy)
   * - ``title.contains("Notas de la version")``
     - Aplica a documentos que contienen una palabra específica en el título

Ejemplos de Expresión de Valor de Impulso (``boostExpr``)
----------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expresión de valor de impulso
     - Descripción
   * - ``3.0``
     - Impulso con valor fijo
   * - ``click_count * 0.1 + 1``
     - Impulso según el número de clics
   * - ``Math.log(click_count + 1)``
     - Impulso en escala logaritmica basado en el número de clics

Ejemplos de Uso
===============

Impulso de Sitio de Documentación
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

Impulso de Contenido con Muchos Clics
--------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://www.example.com/\")",
           "boostExpr": "click_count * 0.1 + 1",
           "sortOrder": 10
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/boostdoc-guide` - Guía de gestión de impulso de documentos
