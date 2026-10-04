===========================
API de etiquetas de usuario
===========================

Este documento describe la API de etiquetas de usuario v2 de |Fess|, con la que los usuarios que han
iniciado sesión gestionan sus propias etiquetas y las asignan a documentos. Para el sobre de
respuesta común, el modelo de errores y CSRF, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

.. note::

   Las etiquetas de usuario están deshabilitadas de forma predeterminada. Para usarlas, configure
   ``user.tag.enabled=true`` en ``fess_config.properties``. ``features.user_tag`` de
   ``/api/v2/ui/config`` indica el estado. Mientras estén deshabilitadas, los endpoints de
   etiquetas responden ``invalid_request`` (400) a una solicitud que supera las comprobaciones de
   CSRF y Origin y usa un método admitido.

Funcionamiento de las etiquetas de usuario
==========================================

- Las etiquetas de usuario se gestionan por usuario. Quien crea una etiqueta es su propietario, y el
  propietario es el ID de usuario con el que inició sesión. Dos usuarios pueden usar el mismo nombre
  y tener aun así dos etiquetas distintas.
- Solo los usuarios que han iniciado sesión pueden usar etiquetas. Cada endpoint actúa como el
  usuario de la sesión iniciada; un token de acceso no sustituye al inicio de sesión. Quien llama sin
  haber iniciado sesión recibe ``auth_required`` (401).
- Una etiqueta nueva es privada: solo su propietario la ve. Cuando el propietario la comparte, todos
  los usuarios que han iniciado sesión pueden verla y filtrar por ella. Un usuario que no ha iniciado
  sesión no ve ninguna etiqueta, ni siquiera las compartidas.
- Solo el propietario puede cambiar o eliminar una etiqueta, o asignarla a documentos y quitarla. Una
  etiqueta compartida de otro usuario solo se puede mostrar y usar para filtrar. Los administradores
  gestionan todas las etiquetas en la pantalla de administración (consulte
  :doc:`../admin/tagtype-guide`).
- Una etiqueta se asigna a la URL de un documento, por lo que todos los documentos indexados con esa
  URL la reciben.

Cada etiqueta tiene dos identificadores.

``value``
    El valor de la etiqueta, ``base64url(nombre):base64url(propietario)`` (UTF-8, sin relleno), que se
    guarda en el campo ``tag`` del índice. Trátelo como un valor opaco para filtrar los resultados de
    búsqueda.

``id``
    El ID de la etiqueta, el SHA-256 de ``value`` en hexadecimal en minúsculas (64 caracteres). Se
    indica en rutas como ``/api/v2/tags/{tagId}``. Al renombrar una etiqueta cambian tanto ``value``
    como ``id``.

El nombre de una etiqueta se normaliza con NFKC, los espacios consecutivos se reducen a uno y se
recortan los extremos. El resultado debe tener entre 1 y ``user.tag.name.max.length``
(predeterminado: ``50``) caracteres, y se rechazan los nombres con un carácter de control o de
formato (como un carácter de ancho cero o una anulación bidireccional).

Etiquetas de usuario en la búsqueda
===================================

Mientras ``user.tag.enabled`` sea ``true``, la API de búsqueda (``/api/v2/search``) trata las
etiquetas de usuario de la siguiente manera.

- Cada resultado incluye en ``tags`` las etiquetas que quien llama puede ver. Cada elemento tiene
  ``value``, ``name``, ``owner``, ``mine`` (``true`` cuando quien llama es el propietario) y
  ``shared`` (``true`` para una etiqueta compartida). Si no hay ninguna, ``tags`` no aparece. El
  campo de índice ``tag`` nunca se devuelve.
- ``facet.field=tag`` devuelve en ``facet_field`` una faceta de las etiquetas que quien llama puede
  ver. Además de ``value`` y ``count``, cada grupo tiene ``label`` (el nombre de la etiqueta),
  ``owner``, ``mine`` y ``shared``.
- ``fields.tag=<valor>`` acota los resultados a los documentos con una etiqueta. Indique tal cual el
  ``value`` de ``tags`` de un resultado o de un grupo de la faceta.

Una condición sobre etiquetas (``fields.tag``, ``tag:``, ``ex_q``, ``facet.query``) solo coincide
con el valor exacto de una etiqueta que quien llama puede ver. El valor de una etiqueta que no puede
ver y las condiciones con comodines, de prefijo, difusas y de rango no coinciden con nada. Quien llama
sin haber iniciado sesión no recibe etiquetas ni faceta de etiquetas, y una condición sobre
etiquetas no coincide con nada.

Un usuario ve como máximo ``user.tag.visible.max.size`` (predeterminado: ``1000``) etiquetas, primero
las suyas. Las que superan ese número no aparecen en ``tags`` de los resultados ni en la faceta, pero
se pueden seguir usando para filtrar.

Cuándo se reflejan los cambios en los documentos
================================================

Crear, cambiar y eliminar etiquetas, y asignarlas a documentos o quitarlas, se refleja de inmediato
en los endpoints de etiquetas. En cambio, el campo ``tag`` de los documentos indexados se actualiza
mediante una cola en memoria que el trabajo "Log Aggregator" (``log_aggregator``) aplica en bloque
cada minuto. Por ello, los resultados, la faceta y los filtros reflejan un cambio al cabo de hasta un
minuto aproximadamente. Tras renombrar una etiqueta, los documentos conservan el valor anterior hasta
que se procesa la cola, y mientras tanto la etiqueta no se muestra en ellos.

Para la cola y los trabajos, consulte :doc:`../admin/tagtype-guide`.

Listar las etiquetas
====================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/tags``
==================  ====================================================

Devuelve las etiquetas de quien llama, por orden de clasificación y nombre. No incluye las etiquetas
compartidas de otros usuarios.

Respuesta
---------

Si tiene éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "tags": [
          {
            "id": "cb15c50dbcf7a9c8b3010895b5969bd81663741e550ae832146066dc7e0d3bf2",
            "value": "cmV2aXNhcg:bHVjaWE",
            "name": "revisar",
            "shared": false,
            "sort_order": 0,
            "path_count": 3
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``tags``
     - Las etiquetas de quien llama. Cada una tiene ``id``, ``value``, ``name``, ``shared``
       (``true`` para una etiqueta compartida), ``sort_order`` y ``path_count`` (el número de URL
       con la etiqueta).

Tabla: Campos de respuesta

Crear una etiqueta
==================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/tags``
==================  ====================================================

Crea una etiqueta de quien llama. Como solicitud que cambia el estado, requiere la cabecera
``X-Fess-CSRF-Token`` (consulte :doc:`api-overview`).

- Un usuario puede tener como máximo ``user.tag.max.tags`` (predeterminado: ``1000``) etiquetas. Si
  se supera, el endpoint responde ``invalid_request`` (400).
- Si quien llama ya tiene una etiqueta con ese nombre, el endpoint responde ``conflict`` (409). Que
  otro usuario tenga una etiqueta con el mismo nombre no importa.

Envíe ``Content-Type: application/json``; el cuerpo puede ocupar como máximo 1 KiB (1024 bytes).

::

    {
      "name": "revisar",
      "shared": false
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Cuerpo de la solicitud

   * - ``name``
     - Nombre de la etiqueta (str, obligatorio).
   * - ``shared``
     - ``true`` permite que todos los usuarios que han iniciado sesión vean la etiqueta (bool,
       predeterminado: ``false``).

Tabla: Cuerpo de la solicitud

Respuesta
---------

Si tiene éxito (200), ``tag`` directamente bajo ``response`` contiene la etiqueta nueva, con la forma
de un elemento de ``GET /api/v2/tags`` y ``path_count`` igual a ``0``.

Cambiar una etiqueta
====================

Solicitud
---------

==================  ====================================================
Método HTTP         PUT
Endpoint            ``/api/v2/tags/{tagId}``
==================  ====================================================

Renombra una etiqueta de quien llama o cambia si está compartida. Se requiere la cabecera
``X-Fess-CSRF-Token``.

- El cuerpo contiene ``name``, ``shared`` o ambos.
- Un ``name`` nuevo renombra la etiqueta, lo que le da un ``id`` y un ``value`` nuevos. Los
  documentos con el valor anterior reciben el nuevo cuando se procesa la cola. Renombrar a un nombre
  que quien llama ya usa responde ``conflict`` (409) y deja la etiqueta sin cambios.
- ``shared`` solo cambia quién ve la etiqueta; no se actualiza ningún documento. Al poner ``shared``
  en ``false`` se conservan los roles y grupos que un administrador añadió a los permisos.
- Una etiqueta compartida de otro usuario responde ``forbidden`` (403), y una etiqueta que quien
  llama no puede ver, ``not_found`` (404).
- Una escritura que pierde repetidamente frente a otra actualización también responde ``conflict``
  (409).

::

    {
      "name": "revisada",
      "shared": true
    }

Si tiene éxito (200), ``response`` contiene ``tag`` (la etiqueta modificada) y ``renamed`` (``true``
si la etiqueta se renombró; en ese caso ``tag.id`` y ``tag.value`` son nuevos).

Eliminar una etiqueta
=====================

Solicitud
---------

==================  ====================================================
Método HTTP         DELETE
Endpoint            ``/api/v2/tags/{tagId}``
==================  ====================================================

Elimina una etiqueta de quien llama. Los documentos pierden su valor cuando se procesa la cola. Se
requiere la cabecera ``X-Fess-CSRF-Token``. Una etiqueta compartida de otro usuario responde
``forbidden`` (403), y una etiqueta que quien llama no puede ver, ``not_found`` (404).

Si tiene éxito (200), ``response`` contiene ``id`` (el ID de la etiqueta eliminada) y ``deleted``
(siempre ``true``).

Obtener las etiquetas de un documento
=====================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Devuelve las etiquetas de la URL del documento que quien llama puede ver y las etiquetas propias de
quien llama que aún no están asignadas. El documento se busca con los roles de quien llama, por lo que
un documento que no puede buscar responde ``not_found`` (404).

Respuesta
---------

Si tiene éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "tags": [
          {
            "id": "cb15c50dbcf7a9c8b3010895b5969bd81663741e550ae832146066dc7e0d3bf2",
            "value": "cmV2aXNhcg:bHVjaWE",
            "name": "revisar",
            "owner": "lucia",
            "mine": true,
            "shared": false
          },
          {
            "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
            "value": "c3BlY3M:Ym9i",
            "name": "specs",
            "owner": "bob",
            "mine": false,
            "shared": true
          }
        ],
        "addable": []
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``doc_id``
     - ID del documento (str).
   * - ``tags``
     - Las etiquetas de la URL del documento que quien llama puede ver. Cada una tiene ``id``,
       ``value``, ``name``, ``owner``, ``mine`` (``true`` cuando quien llama es el propietario) y
       ``shared`` (``true`` para una etiqueta compartida).
   * - ``addable``
     - Las etiquetas de quien llama que no están asignadas a la URL del documento, con la misma forma
       que ``tags``.
   * - ``added``
     - Solo POST. ``false`` cuando la etiqueta ya estaba asignada al documento (bool).
   * - ``tag``
     - Solo POST. La etiqueta asignada al documento, con la misma forma que ``tags``.
   * - ``removed``
     - Solo DELETE. ``false`` cuando la etiqueta no estaba asignada al documento (bool).

Tabla: Campos de respuesta

Asignar una etiqueta a un documento
===================================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Añade la URL del documento a una etiqueta de quien llama. Se requiere la cabecera
``X-Fess-CSRF-Token``.

El cuerpo (``Content-Type: application/json``, como máximo 1 KiB) indica ``id``, una etiqueta
existente, o ``name``, un nombre de etiqueta. Si se indican ambos, prevalece ``id``.

::

    {
      "name": "revisar"
    }

- Con ``name``, si quien llama no tiene ninguna etiqueta con ese nombre, se crea una etiqueta privada
  y se asigna. La etiqueta nueva cuenta para ``user.tag.max.tags``.
- Una etiqueta puede estar asignada como máximo a ``user.tag.max.paths`` (predeterminado:
  ``10000``) URL. Si se supera, el endpoint responde ``invalid_request`` (400).
- El ``id`` de una etiqueta de otro usuario responde ``forbidden`` (403) si quien llama puede verla y
  ``not_found`` (404) en caso contrario.
- Si tiene éxito, la respuesta contiene los campos de "Obtener las etiquetas de un documento" más
  ``added`` y ``tag``. Los endpoints de etiquetas muestran la etiqueta de inmediato; los resultados de
  búsqueda de los documentos con esa URL la reflejan cuando se procesa la cola (aproximadamente un
  minuto después).

Quitar una etiqueta de un documento
===================================

Solicitud
---------

==================  ====================================================
Método HTTP         DELETE
Endpoint            ``/api/v2/documents/{docId}/tags/{tagId}``
==================  ====================================================

Quita la URL del documento de la etiqueta de quien llama indicada por ``tagId``. Se requiere la
cabecera ``X-Fess-CSRF-Token``. Una etiqueta de otro usuario responde ``forbidden`` (403) si quien
llama puede verla y ``not_found`` (404) en caso contrario. Si tiene éxito, la respuesta contiene los
campos de "Obtener las etiquetas de un documento" más ``removed``.

Respuesta de error
==================

Para obtener detalles sobre el modelo de errores, consulte :doc:`api-overview`. Los endpoints de
etiquetas devuelven los siguientes estados HTTP.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida, también cuando las etiquetas de usuario están
       deshabilitadas, el nombre no es válido, falta un campo obligatorio o se superaría
       ``user.tag.max.tags`` o ``user.tag.max.paths``.
   * - 401 Unauthorized
     - Sin iniciar sesión (un token de acceso no lo sustituye).
   * - 403 Forbidden
     - Un token CSRF ausente o caducado, o un cambio en la etiqueta de otro usuario. La comprobación
       de CSRF se hace antes que la del inicio de sesión, por lo que una solicitud que cambia el
       estado sin sesión recibe 403, no 401.
   * - 404 Not Found
     - Cuando la etiqueta no existe o quien llama no puede verla, o el documento no se encuentra o
       quien llama no puede buscarlo.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 409 Conflict
     - Cuando ya existe una etiqueta con ese nombre, o una escritura perdió frente a otra
       actualización.
   * - 413 Payload Too Large
     - Cuando el cuerpo de la solicitud supera el límite de tamaño (1 KiB).
   * - 415 Unsupported Media Type
     - Cuando el ``Content-Type`` no es compatible.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error

Configuración
=============

Los siguientes ajustes de ``fess_config.properties`` regulan las etiquetas de usuario.

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``user.tag.enabled``
     - Si los usuarios que han iniciado sesión pueden usar etiquetas.
     - ``false``
   * - ``user.tag.name.max.length``
     - Longitud máxima del nombre de una etiqueta, en puntos de código.
     - ``50``
   * - ``user.tag.max.tags``
     - Número máximo de etiquetas que puede tener un usuario.
     - ``1000``
   * - ``user.tag.max.paths``
     - Número máximo de URL a las que se puede asignar una etiqueta.
     - ``10000``
   * - ``user.tag.queue.max.size``
     - Número máximo de cambios que se mantienen en memoria hasta que llegan a los documentos. Un
       cambio que lo supere se descarta con un registro WARN.
     - ``10000``
   * - ``user.tag.process.batch.size``
     - Número de URL actualizadas por solicitud en bloque al aplicar los cambios a los documentos.
     - ``100``
   * - ``user.tag.visible.max.size``
     - Número máximo de etiquetas visibles para un usuario en una búsqueda.
     - ``1000``
