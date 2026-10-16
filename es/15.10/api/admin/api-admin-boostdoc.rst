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
La condición (``url_expr``) y el valor de impulso (``boost_expr``) se evalúan con el motor de scripting
especificado en el campo ``script_type``. En ``script_type`` puede indicarse ``javascript`` o ``groovy``
(este último requiere el plugin ``fess-script-groovy``). La pantalla de creación del panel de administración
rellena ``script_type`` con ``javascript``, pero si esta API omite ``script_type`` en el cuerpo de la solicitud,
no se rellena automáticamente y las expresiones se evalúan como Groovy.
Las reglas múltiples se evalúan en orden ascendente según ``sort_order``, y solo se aplica el valor de
impulso de la primera regla cuya condición coincida (una vez encontrada una regla que coincida,
las reglas siguientes no se evalúan).

.. note::

   En el panel de administración, ``url_expr`` se muestra como "Condición", ``boost_expr`` como "Expresión de valor
   de impulso" y ``script_type`` como "Tipo de Script". ``script_type`` solo aparece en los cuerpos de solicitud y
   respuestas de creación/actualización/obtención (lista y detalle), no en los parámetros de filtro de la lista
   (``url_expr``, ``boost_expr``).
   Para más detalles sobre los elementos de configuración, consulte :doc:`../../admin/boostdoc-guide`.

URL Base
========

::

    /api/admin/boostdoc

Autenticación
=============

Para usar esta API, se requiere un token de acceso con el permiso ``Radmin-api``.
Consulte :doc:`api-admin-overview` para conocer cómo obtener y especificar el token de acceso.

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
   * - ``url_expr``
     - String
     - No
     - Filtrado por expresión de condición (coincidencia parcial)
   * - ``boost_expr``
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
            "url_expr": "url.startsWith(\"https://docs.example.com/\")",
            "boost_expr": "3.0",
            "script_type": "javascript",
            "sort_order": 1,
            "version_no": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Además de los campos mostrados anteriormente, cada objeto de configuración en la respuesta incluye también metadatos de creación/actualización (``created_by``, ``created_time``, ``updated_by``, ``updated_time``).
   ``version_no`` es obligatorio al actualizar (PUT), por lo que debe obtener su valor actual mediante la API de obtención individual o de lista antes de actualizar.

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
          "url_expr": "url.startsWith(\"https://docs.example.com/\")",
          "boost_expr": "3.0",
          "script_type": "javascript",
          "sort_order": 1,
          "version_no": 1
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
      "url_expr": "url.startsWith(\"https://important.example.com/\")",
      "boost_expr": "5.0",
      "script_type": "javascript",
      "sort_order": 0
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``url_expr``
     - Sí
     - Expresión de condición. Expresión de script que determina los documentos objetivo del impulso y devuelve ``Boolean``. Corresponde a "Condición" en el panel de administración (máximo 10000 caracteres).
   * - ``boost_expr``
     - Sí
     - Expresión de valor de impulso. Expresión de script que devuelve el valor de impulso (numérico). También se puede especificar un valor fijo como ``3.0``. Corresponde a "Expresión de valor de impulso" en el panel de administración (máximo 10000 caracteres).
   * - ``script_type``
     - No
     - Motor de scripting utilizado para evaluar ``url_expr`` y ``boost_expr``. Puede ser ``javascript`` o ``groovy`` (requiere el plugin ``fess-script-groovy``). Corresponde a "Tipo de Script" en el panel de administración (máximo 100 caracteres). Si se omite, las expresiones se evalúan como Groovy.
   * - ``sort_order``
     - Sí
     - Orden de aplicación. Las reglas se evalúan en orden ascendente y se aplica el valor de impulso de la primera regla cuya condición coincida (valor inicial del formulario: 0; entero mayor o igual a 0).

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
      "url_expr": "url.startsWith(\"https://important.example.com/\")",
      "boost_expr": "10.0",
      "script_type": "javascript",
      "sort_order": 0,
      "version_no": 1
    }

Al actualizar, además de los campos utilizados al crear, ``id`` (el identificador de la regla objetivo, hasta 1000 caracteres) y ``version_no`` (el número de versión para bloqueo optimista) son obligatorios. Especifique el número de versión actual obtenido desde la respuesta de la API de obtención individual o de lista para ``version_no``. La actualización falla si el número de versión no coincide.

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

``url_expr`` (condición) y ``boost_expr`` (expresión de valor de impulso) se evalúan con el motor de scripting
especificado en ``script_type`` (valor predeterminado: Groovy; solo la pantalla de creación del panel de
administración rellena ``javascript``).
Dentro de la expresión, se pueden referenciar los valores de campo del documento a indexar como variables con el nombre del campo.

- ``url_expr`` debe devolver ``Boolean`` (ejemplo: ``url.startsWith("https://docs.example.com/")``). Una simple cadena de expresión regular (ejemplo: ``.*docs\.example\.com.*``) no devuelve ``Boolean`` como expresión de script y por lo tanto no funciona como condición. Para usar expresiones regulares, utilice ``String#matches`` (disponible con la misma notación tanto en Groovy como en JavaScript).
- ``boost_expr`` debe devolver un valor numérico. El resultado se convierte a ``float`` y el impulso se aplica solo si es mayor que 0.

.. note::

   Principales variables de campo disponibles dentro de la expresión: ``url``, ``title``, ``content``, ``content_length``, ``last_modified``, entre otros.
   ``click_count`` y ``favorite_count`` están disponibles cuando ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled`` están habilitados (ambos habilitados por defecto).
   La sintaxis de cálculo de fechas de OpenSearch como ``now - 7d`` no se puede usar ni en Groovy ni en JavaScript.

Ejemplos de Expresión de Condición (``url_expr``)
-------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expresión de condición
     - Descripción
   * - ``url.startsWith("https://docs.example.com/")``
     - Aplica a documentos cuya URL comienza con la URL especificada
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - Evalúa la URL mediante expresión regular (``String#matches``)
   * - ``title.contains("Notas de la version")``
     - Aplica a documentos que contienen una palabra específica en el título

Ejemplos de Expresión de Valor de Impulso (``boost_expr``)
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
     - Impulso en escala logarítmica basado en el número de clics

Ejemplos de Uso
===============

Impulso de Sitio de Documentación
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url_expr": "url.startsWith(\"https://docs.example.com/\")",
           "boost_expr": "5.0",
           "sort_order": 0
         }'

Impulso de Contenido con Muchos Clics
--------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url_expr": "url.startsWith(\"https://www.example.com/\")",
           "boost_expr": "click_count * 0.1 + 1",
           "sort_order": 10
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/boostdoc-guide` - Guía de gestión de impulso de documentos
