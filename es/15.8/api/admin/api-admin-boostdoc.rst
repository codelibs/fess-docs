==========================
BoostDoc API
==========================

Vision General
==============

La API de BoostDoc es para gestionar la configuracion de impulso de documentos de |Fess|.
Al configurar el impulso de documentos, puede elevar la puntuacion de los documentos que
coincidan con ciertas condiciones y hacer que aparezcan con mayor facilidad en las posiciones
superiores de los resultados de busqueda.

El impulso se aplica a cada documento en el momento de la indexacion (durante el rastreo).
La condicion (``urlExpr``) y el valor de impulso (``boostExpr``) se evaluan ambos como expresiones Groovy.
Las reglas multiples se evaluan en orden ascendente segun ``sortOrder``, y solo se aplica el valor de
impulso de la primera regla cuya condicion coincida (una vez encontrada una regla que coincida,
las reglas siguientes no se evaluan).

.. note::

   En el panel de administracion, ``urlExpr`` se muestra como "Condicion" y ``boostExpr`` como "Expresion de valor de impulso".
   Para mas detalles sobre los elementos de configuracion, consulte :doc:`../../admin/boostdoc-guide`.

URL Base
========

::

    /api/admin/boostdoc

Autenticacion
=============

Para usar esta API, se requiere un token de acceso con el permiso ``Radmin-api``.
Consulte :doc:`api-admin-overview` para conocer como obtener y especificar el token de acceso.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
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

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``size``
     - Integer
     - No
     - Numero de elementos por pagina (predeterminado: 25)
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 1. Predeterminado: 1)
   * - ``urlExpr``
     - String
     - No
     - Filtrado por expresion de condicion (coincidencia parcial)
   * - ``boostExpr``
     - String
     - No
     - Filtrado por expresion de valor de impulso (coincidencia parcial)

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

   Ademas de los campos mostrados anteriormente, cada objeto de configuracion en la respuesta incluye tambien metadatos de creacion/actualizacion (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``).
   ``versionNo`` es obligatorio al actualizar (PUT), por lo que debe obtener su valor actual mediante la API de obtencion individual o de lista antes de actualizar.

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

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``urlExpr``
     - Si
     - Expresion de condicion. Expresion Groovy que determina los documentos objetivo del impulso y devuelve ``Boolean``. Corresponde a "Condicion" en el panel de administracion (maximo 10000 caracteres).
   * - ``boostExpr``
     - Si
     - Expresion de valor de impulso. Expresion Groovy que devuelve el valor de impulso (numerico). Tambien se puede especificar un valor fijo como ``3.0``. Corresponde a "Expresion de valor de impulso" en el panel de administracion (maximo 10000 caracteres).
   * - ``sortOrder``
     - Si
     - Orden de aplicacion. Las reglas se evaluan en orden ascendente y se aplica el valor de impulso de la primera regla cuya condicion coincida (valor inicial del formulario: 0; entero mayor o igual a 0).

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

Al actualizar, ademas de los campos utilizados al crear, ``id`` (el identificador de la regla objetivo, hasta 1000 caracteres) y ``versionNo`` (el numero de version para bloqueo optimista) son obligatorios. Especifique el numero de version actual obtenido desde la respuesta de la API de obtencion individual o de lista para ``versionNo``. La actualizacion falla si el numero de version no coincide.

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

Acerca de las Expresiones de Condicion y de Valor de Impulso
=============================================================

``urlExpr`` (condicion) y ``boostExpr`` (expresion de valor de impulso) se evaluan ambas como expresiones Groovy.
Dentro de la expresion, se pueden referenciar los valores de campo del documento a indexar como variables con el nombre del campo.

- ``urlExpr`` debe devolver ``Boolean`` (ejemplo: ``url.startsWith("https://docs.example.com/")``). Una simple cadena de expresion regular (ejemplo: ``.*docs\.example\.com.*``) no devuelve ``Boolean`` como expresion Groovy y por lo tanto no funciona como condicion. Para usar expresiones regulares, utilice ``String#matches`` de Groovy.
- ``boostExpr`` debe devolver un valor numerico. El resultado se convierte a ``float`` y el impulso se aplica solo si es mayor que 0.

.. note::

   Principales variables de campo disponibles dentro de la expresion: ``url``, ``title``, ``content``, ``content_length``, ``last_modified``, entre otros.
   ``click_count`` y ``favorite_count`` estan disponibles cuando ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled`` estan habilitados (ambos habilitados por defecto).
   La sintaxis de calculo de fechas de OpenSearch como ``now - 7d`` no se puede usar en Groovy.

Ejemplos de Expresion de Condicion (``urlExpr``)
-------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expresion de condicion
     - Descripcion
   * - ``url.startsWith("https://docs.example.com/")``
     - Aplica a documentos cuya URL comienza con la URL especificada
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - Evalua la URL mediante expresion regular (``String#matches`` de Groovy)
   * - ``title.contains("Notas de la version")``
     - Aplica a documentos que contienen una palabra especifica en el titulo

Ejemplos de Expresion de Valor de Impulso (``boostExpr``)
----------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expresion de valor de impulso
     - Descripcion
   * - ``3.0``
     - Impulso con valor fijo
   * - ``click_count * 0.1 + 1``
     - Impulso segun el numero de clics
   * - ``Math.log(click_count + 1)``
     - Impulso en escala logaritmica basado en el numero de clics

Ejemplos de Uso
===============

Impulso de Sitio de Documentacion
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

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/boostdoc-guide` - Guia de gestion de impulso de documentos
