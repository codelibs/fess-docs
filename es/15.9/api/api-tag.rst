===========================
API de etiquetas de usuario
===========================

Este documento describe la API de etiquetas de usuario v2 de |Fess|, que permite a los usuarios
etiquetar documentos. Para el sobre de respuesta común, el modelo de errores y CSRF, consulte
:doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

.. note::

   Las etiquetas de usuario están deshabilitadas de forma predeterminada. Para usarlas, configure
   ``user.tag.enabled=true`` en ``fess_config.properties``. ``features.user_tag`` de
   ``/api/v2/ui/config`` indica el estado.

Una etiqueta de usuario es una etiqueta del tipo "Etiqueta de usuario" (consulte
:doc:`../admin/labeltype-guide`): el nombre de la etiqueta es el nombre, el valor es el SHA-256 del
nombre en hexadecimal, las rutas incluidas son las URL etiquetadas y los permisos deciden quién puede
verla. Solo es visible cuando su etiqueta es visible para quien llama.

La API de búsqueda (``/api/v2/search``) devuelve en ``tags`` las etiquetas de usuario de cada
resultado que quien llama puede ver. ``fields.tag=<valor>`` acota los resultados a los documentos con
una etiqueta, y ``facet.field=tag`` devuelve una faceta de etiquetas. El campo de índice ``tag`` no se
devuelve.

Obtener las etiquetas
=====================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Devuelve las etiquetas de usuario del documento que quien llama puede ver. Si quien llama no puede
buscar el documento, el endpoint responde con ``not_found`` (404).

Respuesta
---------

Si tiene éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "addable": true,
        "tags": [
          { "value": "9f86d081884c7d65...", "name": "revisar", "mine": true }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``doc_id``
     - ID del documento (str).
   * - ``addable``
     - ``true`` cuando quien llama ha iniciado sesión y puede añadir etiquetas (bool).
   * - ``added``
     - Solo POST. ``false`` cuando quien llama ya había etiquetado el documento (bool).
   * - ``removed``
     - Solo DELETE (bool).
   * - ``tags``
     - Las etiquetas de usuario que quien llama puede ver. Cada una tiene ``value`` (el valor de la
       etiqueta, usado con ``fields.tag``), ``name`` (el nombre) y ``mine`` (``true`` cuando quien
       llama está en los permisos de la etiqueta).

Tabla: Campos de respuesta

Añadir una etiqueta
===================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Etiqueta la URL del documento para el usuario que ha iniciado sesión; un token de acceso no sustituye
al inicio de sesión. Como solicitud que cambia el estado, requiere la cabecera ``X-Fess-CSRF-Token``.

- Si ya existe una etiqueta con ese nombre, la URL se añade a sus rutas incluidas y el usuario a sus
  permisos. Si no, se crea una etiqueta que solo ese usuario puede ver. Por eso las etiquetas con el
  mismo nombre se combinan en una, y los usuarios que añadieron una etiqueta con el mismo nombre ven
  dónde están las etiquetas de los demás.
- Volver a etiquetar el mismo documento responde ``added: false``.
- Un documento puede tener como máximo ``user.tag.max.document.tags`` (predeterminado: ``100``)
  etiquetas de usuario.

Envíe ``Content-Type: application/json`` con el nombre en ``name``.

::

    {
      "name": "revisar"
    }

El nombre se normaliza con NFKC, los espacios consecutivos se reducen a uno y se recorta. Debe tener
entre 1 y ``user.tag.name.max.length`` (predeterminado: ``50``) caracteres, y se rechazan los nombres
con un carácter de control o de formato (como un carácter de ancho cero o una anulación
bidireccional).

Quitar una etiqueta
===================

Solicitud
---------

==================  ====================================================
Método HTTP         DELETE
Endpoint            ``/api/v2/documents/{docId}/tags?value=<valor>``
==================  ====================================================

Quita al usuario que ha iniciado sesión de los permisos de la etiqueta indicada en ``value``. Cuando no
queda ningún permiso de usuario, grupo o rol, la etiqueta se elimina y se quita de los documentos. Si
el usuario no está en los permisos de la etiqueta, el endpoint responde con ``forbidden`` (403). Se
requiere la cabecera ``X-Fess-CSRF-Token``.

Respuesta de error
==================

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida (también cuando las etiquetas de usuario están deshabilitadas,
       el nombre no es válido o se supera un límite).
   * - 401 Unauthorized
     - POST o DELETE sin iniciar sesión.
   * - 403 Forbidden
     - Un token CSRF ausente o caducado, o un DELETE de una etiqueta que el usuario no añadió.
   * - 404 Not Found
     - Cuando el documento no se encuentra o quien llama no puede buscarlo.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 413 Payload Too Large
     - Cuando el cuerpo de la solicitud supera el límite de tamaño.
   * - 415 Unsupported Media Type
     - Cuando el ``Content-Type`` no es compatible.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
