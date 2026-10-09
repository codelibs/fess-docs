===================
API de TagType
===================

Descripción general
===================

La API de TagType es una API para gestionar las etiquetas de usuario de |Fess|, es decir, las
etiquetas propias de cada usuario que los usuarios que han iniciado sesión asignan a documentos
(consulte :doc:`../../admin/tagtype-guide`). Gestiona las etiquetas de todos los usuarios, tanto si
``user.tag.enabled`` es ``true`` como si no.

Para conocer el método de autenticación y las especificaciones comunes de la Respuesta
(código ``status``, campo ``version``, formato de errores, códigos de estado HTTP, etc.),
consulte :doc:`api-admin-overview`.
Para acceder a esta API, es necesario especificar un token de acceso con el permiso de Admin API
(``admin-api``) en el encabezado ``Authorization: Bearer <token de acceso>``.

Los nombres de los campos JSON de esta API están en snake_case (``sort_order``, ``virtual_host``,
``seq_no``, ``primary_term``, etc.).

URL base
========

::

    /api/admin/tagtype

Lista de endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /settings
     - Obtener la lista de etiquetas de usuario
   * - GET
     - /setting/{id}
     - Obtener una etiqueta de usuario
   * - POST
     - /setting
     - Crear una etiqueta de usuario
   * - PUT
     - /setting
     - Actualizar una etiqueta de usuario
   * - DELETE
     - /setting/{id}
     - Eliminar una etiqueta de usuario

Obtener la lista de etiquetas de usuario
========================================

Solicitud
---------

::

    GET /api/admin/tagtype/settings

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Obligatorio
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página. El valor predeterminado es el de ``paging.page.size`` (``25`` de forma predeterminada).
   * - ``page``
     - Integer
     - No
     - Número de página (empieza en 1). El valor predeterminado es ``1``.
   * - ``name``
     - String
     - No
     - Filtrar por nombre (búsqueda con comodines: coincide con los nombres que contienen el texto).
   * - ``owner``
     - String
     - No
     - Filtrar por propietario (búsqueda con comodines: coincide con los propietarios que contienen el texto).

Las etiquetas se ordenan por orden de clasificación, nombre y propietario.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "settings": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "seq_no": 12,
            "primary_term": 1,
            "name": "to-review",
            "owner": "alice",
            "permissions": "{user}alice",
            "virtual_host": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

.. note::

   La lista no lee las rutas de las etiquetas, que pueden ser largas, por lo que sus elementos no
   tienen ``paths``. PUT sustituye la etiqueta por completo: para editarla, obténgala antes con
   ``GET /setting/{id}`` para conservar sus ``paths``.

Obtener una etiqueta de usuario
===============================

Solicitud
---------

::

    GET /api/admin/tagtype/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
          "seq_no": 12,
          "primary_term": 1,
          "name": "to-review",
          "owner": "alice",
          "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
          "permissions": "{user}alice",
          "virtual_host": "",
          "sort_order": 0
        }
      }
    }

``seq_no`` y ``primary_term`` identifican la versión leída de la etiqueta. ``paths`` y
``permissions`` contienen un valor por línea.

Crear una etiqueta de usuario
=============================

Solicitud
---------

::

    POST /api/admin/tagtype/setting
    Content-Type: application/json

Cuerpo de la solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "specs",
      "owner": "bob",
      "paths": "https://www.example.com/spec.pdf",
      "permissions": "{user}bob\n{role}guest",
      "sort_order": 0
    }

Descripción de campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Campo
     - Tipo
     - Obligatorio
     - Descripción
   * - ``name``
     - String
     - Sí
     - Nombre de la etiqueta. Se normaliza con NFKC, los espacios consecutivos se reducen a uno y se
       recortan los extremos; el resultado debe tener entre 1 y ``user.tag.name.max.length``
       (predeterminado: ``50``) caracteres sin caracteres de control ni de formato.
   * - ``owner``
     - String
     - Sí
     - ID de usuario de inicio de sesión del propietario (máximo 1000 caracteres).
   * - ``paths``
     - String
     - No
     - URL de los documentos a los que se asigna la etiqueta, separadas por un salto de línea
       (``\n``). Cada una debe ser igual al campo ``url`` de un documento. Como máximo
       ``user.tag.max.paths`` (predeterminado: ``10000``).
   * - ``permissions``
     - String
     - No
     - Usuarios/grupos/roles que pueden ver la etiqueta (p. ej. ``{role}guest``), separados por un
       salto de línea (``\n``). Si está vacío, solo el propietario la ve. ``{role}guest`` (el valor
       de ``role.search.guest.permissions``) la comparte con todos los usuarios que han iniciado
       sesión.
   * - ``virtual_host``
     - String
     - No
     - Host virtual (máximo 1000 caracteres).
   * - ``sort_order``
     - Integer
     - No
     - Orden de visualización (entero no negativo). Si se omite, ``0``.

El ID de una etiqueta es el SHA-256 de su valor, formado a partir del nombre y el propietario, por
lo que lo decide el servidor. El propietario y el nombre identifican juntos una etiqueta: si el
propietario ya tiene una etiqueta con ese nombre, la creación falla con un error de validación
(``status: 1``, "A tag with the same name and owner already exists.").

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
        "created": true
      }
    }

Si la creación tiene éxito, ``created`` es ``true``.

Actualizar una etiqueta de usuario
==================================

Solicitud
---------

::

    PUT /api/admin/tagtype/setting
    Content-Type: application/json

Cuerpo de la solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
      "seq_no": 12,
      "primary_term": 1,
      "name": "reviewed",
      "owner": "alice",
      "paths": "https://www.example.com/a.html",
      "permissions": "{user}alice",
      "virtual_host": "",
      "sort_order": 0
    }

El cuerpo contiene todos los campos de la creación y, además, los siguientes. La etiqueta se
sustituye por completo, así que envíe también las ``paths`` que quiera conservar.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Campo
     - Tipo
     - Obligatorio
     - Descripción
   * - ``id``
     - String
     - Sí
     - El ID de la etiqueta que se actualiza.
   * - ``seq_no``
     - Integer
     - Sí
     - El ``seq_no`` de la etiqueta devuelto por ``GET /setting/{id}``.
   * - ``primary_term``
     - Integer
     - Sí
     - El ``primary_term`` de la etiqueta devuelto por ``GET /setting/{id}``.

- Si la etiqueta cambió después de leerla, es decir, ``seq_no`` y ``primary_term`` ya no
  coinciden, la actualización falla con un error de validación (``status: 1``, "The tag was
  changed by someone else. Reload it and try again."). Vuelva a obtener la etiqueta y repita la
  operación.
- Cambiar ``name`` u ``owner`` da a la etiqueta un ID nuevo; el ``id`` de la respuesta es el nuevo.
  Si el propietario ya tiene una etiqueta con el nuevo nombre, la actualización falla con "A tag
  with the same name and owner already exists.".
- Al cambiar el propietario, el permiso de usuario del propietario anterior en ``permissions`` se
  sustituye por el del nuevo propietario.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "c1fd8e024cbadfc79468e66fa52350e46cc31837aabf75b7ee6d929edaa20396",
        "created": false
      }
    }

En una actualización, ``created`` es ``false``.

Eliminar una etiqueta de usuario
================================

Solicitud
---------

::

    DELETE /api/admin/tagtype/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Si la etiqueta cambia mientras se elimina, la eliminación falla con "The tag was changed by someone
else. Reload it and try again.".

Cómo llegan los cambios a los documentos
========================================

Crear, actualizar y eliminar una etiqueta con esta API se guarda de inmediato en las etiquetas.
Mientras ``user.tag.enabled`` sea ``true``, el cambio para los documentos (rutas añadidas y
quitadas, un cambio de nombre o una eliminación) se pone en cola y lo aplica cada minuto el trabajo
"Log Aggregator" (``log_aggregator``). Mientras sea ``false`` no se pone nada en cola; ejecute el
trabajo "Tag Updater" (``tag_updater``) después de habilitar las etiquetas. Consulte
:doc:`../../admin/tagtype-guide`.

Ejemplos de uso
===============

Compartir una etiqueta con todos los usuarios que han iniciado sesión
---------------------------------------------------------------------

.. code-block:: bash

    # Leer la etiqueta, con paths, seq_no y primary_term
    curl "http://localhost:8080/api/admin/tagtype/setting/0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Devolverla con {role}guest añadido a los permisos
    curl -X PUT "http://localhost:8080/api/admin/tagtype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
           "seq_no": 12,
           "primary_term": 1,
           "name": "to-review",
           "owner": "alice",
           "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
           "permissions": "{user}alice\n{role}guest",
           "sort_order": 0
         }'

Obtener las etiquetas de un usuario
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/tagtype/settings" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"owner": "alice", "size": 50, "page": 1}'

Véase también
=============

- :doc:`api-admin-overview` - Descripción general de Admin API
- :doc:`../api-tag` - API de etiquetas de usuario
- :doc:`../../admin/tagtype-guide` - Guía de gestión de etiquetas de usuario
