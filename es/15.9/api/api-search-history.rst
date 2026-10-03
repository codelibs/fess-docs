============================
API de historial de búsqueda
============================

Este documento describe la API de historial de búsqueda v2 de |Fess|.
Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

.. note::

   El historial de búsqueda está disponible mientras ``search.history.enabled`` (predeterminado:
   ``true``) y el registro de búsqueda estén habilitados. ``features.search_history`` de
   ``/api/v2/ui/config`` indica el estado.

Obtener las búsquedas recientes
===============================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/search-history``
==================  ====================================================

Devuelve las búsquedas recientes que el usuario que ha iniciado sesión hizo con ``/api/v2/search`` en
el host virtual actual, de la más reciente a la más antigua. Un cliente puede volver a ejecutar una
de ellas con las condiciones devueltas.

- Solo se incluyen las búsquedas de la primera página. Las búsquedas con las mismas condiciones se
  combinan en la más reciente, y se omiten las búsquedas sin consulta.
- Se devuelven como máximo ``search.history.size`` (predeterminado: ``10``) búsquedas.
- Los registros de búsqueda los escribe un trabajo que se ejecuta cada minuto, por lo que una búsqueda
  puede tardar hasta un minuto aproximadamente en aparecer.
- El historial pertenece al usuario de la sesión. Las llamadas anónimas reciben ``auth_required``
  (401); un token de acceso no sustituye al inicio de sesión.
- Cuando el historial de búsqueda está deshabilitado, el endpoint responde con ``invalid_request`` (400).

No hay parámetros de solicitud.

Respuesta
---------

Si tiene éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "record_count": 1,
        "data": [
          {
            "q": "fess",
            "fields": { "label": ["docs"] },
            "sort": "last_modified.desc",
            "requested_at": "2026-10-01T09:00:00Z",
            "hit_count": 42
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``record_count``
     - Número de búsquedas en ``data`` (int).
   * - ``data``
     - Búsquedas recientes, de la más reciente a la más antigua. Las claves de las condiciones son los
       nombres de los parámetros de ``/api/v2/search``; una clave se omite cuando la búsqueda no la usó.
   * - ``data[].q``
     - La consulta (str).
   * - ``data[].fields``
     - Condiciones de campo indicadas con ``fields.<name>``, por nombre de campo, con sus valores.
   * - ``data[].ex_q``
     - Consultas adicionales (array de str).
   * - ``data[].sort``
     - Orden (str).
   * - ``data[].lang``
     - Idiomas solicitados con ``lang`` (array de str).
   * - ``data[].requested_at``
     - Momento de la búsqueda (UTC, ISO-8601).
   * - ``data[].hit_count``
     - Número de resultados de la búsqueda (int64).

Tabla: Campos de respuesta

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando el historial de búsqueda está deshabilitado.
   * - 401 Unauthorized
     - Cuando quien llama no ha iniciado sesión.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error

En el tema incluido
===================

En el tema incluido ``bootstrap``, un usuario que ha iniciado sesión ve sus búsquedas recientes en la
lista de sugerencias al hacer clic en el cuadro de búsqueda vacío o pulsar la flecha hacia abajo en
él. Al elegir una entrada se vuelve a ejecutar la misma búsqueda, incluidas condiciones como las
etiquetas. Los registros de búsqueda anteriores a |Fess| 15.9 no guardan las condiciones y no se
muestran.
