=====================================================
API de consultas relacionadas y contenido relacionado
=====================================================

Esta página describe los dos endpoints para obtener información relacionada con una consulta.

- ``GET /related-queries`` — Obtiene candidatos de consultas relacionadas para una consulta dada.
- ``GET /related-content`` — Obtiene contenido HTML relacionado para una consulta dada.

Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

Obtención de consultas relacionadas
====================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/related-queries``
==================  ====================================================

Al enviar a |Fess| una solicitud como ``http://<Server Name>/api/v2/related-queries?q=fess``, puede recibir en formato JSON una lista de términos de consultas relacionadas para la consulta especificada.

Incluso si ``q`` está vacío o no se especifica, no se genera un error; se devuelve un array ``queries`` vacío. La respuesta siempre es un sobre de éxito.

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Parámetros de solicitud

   * - q
     - Término de búsqueda para obtener consultas relacionadas. (Ejemplo) ``q=fess``

Respuesta
---------

En caso de éxito, se devuelve una respuesta con el formato de sobre común como la siguiente:

::

    {
      "response": {
        "status": 0,
        "queries": [
          "fess search",
          "fess install"
        ]
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Información de respuesta

   * - queries
     - Array de términos de consultas relacionadas (array de cadenas de texto). Devuelve un array vacío cuando ``q`` está vacío o no se especifica.

Respuesta de error
~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Obtención de contenido relacionado
===================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/related-content``
==================  ====================================================

Al enviar a |Fess| una solicitud como ``http://<Server Name>/api/v2/related-content?q=fess``, puede recibir en formato JSON el contenido HTML relacionado para la consulta especificada.

Cuando coinciden varios elementos de contenido, se concatenan con saltos de línea.
Incluso si ``q`` está vacío o no se especifica, no se genera un error; se devuelve un ``content`` con cadena vacía. La respuesta siempre es un sobre de éxito.

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Parámetros de solicitud

   * - q
     - Término de búsqueda para obtener contenido relacionado. (Ejemplo) ``q=fess``

Respuesta
---------

En caso de éxito, se devuelve una respuesta con el formato de sobre común como la siguiente:

::

    {
      "response": {
        "status": 0,
        "content": "<div>...contenido HTML relacionado...</div>",
        "content_type": "html"
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Información de respuesta

   * - content
     - Contenido HTML relacionado (cadena de texto). Cuando coinciden varios elementos, se concatenan con saltos de línea. Devuelve una cadena vacía cuando ``q`` está vacío o no se especifica.
   * - content_type
     - Tipo de contenido. El valor es siempre ``html``.

Respuesta de error
~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.
