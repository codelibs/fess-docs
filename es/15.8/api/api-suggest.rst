==================
API de sugerencias
==================

Obtención de lista de palabras sugeridas
=========================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/suggest-words``
==================  ====================================================

Al enviar a |Fess| una solicitud como ``http://<Server Name>/api/v2/suggest-words?q=fes``, puede recibir en formato JSON una lista de palabras sugeridas para el prefijo introducido.

Las palabras sugeridas provienen de tres fuentes:

- **Documentos** — Generadas a partir de documentos rastreados. Para obtenerlas, habilite "Sugerir por documentos" en la consola de administración en Sistema > General.
- **Términos de búsqueda (registro de búsqueda)** — Generadas a partir de los registros de búsqueda de los usuarios. Para obtenerlas, habilite "Sugerir por término de búsqueda" en la consola de administración en Sistema > General.
- **Diccionario de usuario** — Palabras sugeridas registradas por los administradores. Siempre se devuelven independientemente de la configuración anterior.

Incluso cuando "Sugerir por documentos" y "Sugerir por término de búsqueda" están deshabilitados, la API no devuelve un error; simplemente se omiten las palabras sugeridas correspondientes de los resultados.
Las palabras sugeridas también se filtran automáticamente según los roles del usuario solicitante.

Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

Parámetros de solicitud
-----------------------

Los parámetros de solicitud disponibles son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Parámetros de solicitud

   * - q
     - Término de búsqueda (prefijo) para realizar sugerencias. Si se omite, se devuelven palabras sugeridas sin filtrado por prefijo. (Ejemplo) ``q=fes``
   * - num
     - Número de palabras sugeridas (entero mayor o igual a 0). Predeterminado ``10``. Si se especifica un valor no numérico, se utiliza el valor predeterminado. (Ejemplo) ``num=20``
   * - fn
     - Nombre de campo para filtrar el objetivo de sugerencia. Se puede especificar varias veces (array). (Ejemplo) ``fn=content&fn=title``
   * - lang
     - Idioma de búsqueda. Se puede especificar varias veces (array). (Ejemplo) ``lang=en``
   * - label
     - Nombre de etiqueta (tag) para filtrar. Se puede especificar varias veces (array). Los valores especificados se comparan contra los ``types`` de cada palabra sugerida. (Ejemplo) ``label=java``

.. note::

   En v2, el parámetro para especificar nombres de campo es ``fn`` (no ``fields`` como en v1).
   En lugar de enumerar valores como una cadena separada por comas, ``fn`` se repite para pasar múltiples valores.

Respuesta
---------

En caso de éxito, se devuelve una respuesta con el formato de sobre común como la siguiente:

::

    {
      "response": {
        "status": 0,
        "q": "fes",
        "page_size": 10,
        "record_count": 355,
        "query_time": 18,
        "suggest_words": [
          {
            "text": "fess",
            "types": [
              "label1"
            ]
          }
        ]
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Información de respuesta

   * - q
     - Término de búsqueda solicitado (cadena de texto). Devuelve una cadena vacía cuando se omite ``q``.
   * - page_size
     - Número de palabras sugeridas solicitado (el valor de ``num``, entero).
   * - record_count
     - Número total de palabras sugeridas coincidentes (entero de 64 bits).
   * - query_time
     - Tiempo de procesamiento de la consulta en milisegundos (entero de 64 bits).
   * - suggest_words
     - Array de palabras sugeridas. Cada elemento tiene ``text`` y ``types``.
   * - text
     - Palabra sugerida (cadena de texto).
   * - types
     - Array de etiquetas (tags) asociadas a la palabra sugerida (array de cadenas de texto). Cada etiqueta se deriva del campo ``label`` o ``virtual_host`` de un documento, o de las condiciones de filtro extraídas del registro de búsqueda. Devuelve un array vacío cuando no hay etiquetas.

.. note::

   ``types`` contiene valores de etiquetas (tags), no el tipo de la palabra sugerida (como ``document`` o ``query``). Este array corresponde al campo ``labels`` de los elementos de sugerencia en v1.
   El parámetro de solicitud ``label`` filtra por estos valores de ``types``.

Ejemplos de uso
===============

Ejemplo de solicitud usando el comando curl:

::

    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

Respuesta de error
==================

Si la API de sugerencias falla, se devuelve el sobre de error común. Consulte :doc:`api-overview` para detalles del modelo de errores.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido. La cabecera ``Allow`` indica ``GET``.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.
