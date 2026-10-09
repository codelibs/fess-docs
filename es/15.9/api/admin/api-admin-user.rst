==========================
API de User
==========================

Visión General
==============

La API de User es una API REST para gestionar cuentas de usuario de |Fess|.
Permite crear, obtener, actualizar y eliminar usuarios, además de asignar roles y grupos.

Esta es una API de administración, y el acceso requiere autenticación con un token de acceso de administrador.
Consulte :doc:`api-admin-overview` para conocer el método de autenticación y las especificaciones comunes.

Cada respuesta está envuelta en un objeto ``response`` e incluye los siguientes campos comunes:

- ``version`` : La cadena de versión del producto |Fess|.
- ``status`` : El código de estado del resultado (``0`` =éxito, ``1`` =solicitud incorrecta, ``2`` =error del sistema, ``3`` =no autorizado, ``9`` =fallo).

URL Base
========

::

    /api/admin/user

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
     - Listar usuarios
   * - GET
     - /setting/{id}
     - Obtener usuario
   * - POST
     - /setting
     - Crear usuario
   * - PUT
     - /setting
     - Actualizar usuario
   * - DELETE
     - /setting/{id}
     - Eliminar usuario

Listar Usuarios
===============

Solicitud
---------

::

    GET /api/admin/user/settings

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 10 65

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página. El valor predeterminado es el valor configurado ``paging.page.size`` (predeterminado: 25).
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1). El valor predeterminado es 1.

.. note::

   En la implementación actual, el endpoint de lista de usuarios no aplica los parámetros ``size`` y ``page``.
   Siempre devuelve la primera página, con el número de elementos definido por la configuración del servidor ``paging.page.size`` (predeterminado: 25), ordenado por nombre de usuario (``name``) en orden ascendente.
   El número total de usuarios coincidentes está disponible en ``response.total``.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "settings": [
          {
            "id": "YWRtaW4=",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["YWRtaW4=", "Z3Vlc3Q="],
            "groups": [],
            "version_no": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` : El array de usuarios en la página actual.
- ``total`` : El número total de usuarios coincidentes.

Obtener Usuario
===============

Solicitud
---------

::

    GET /api/admin/user/setting/{id}

Especifique el ID de documento del usuario objetivo en ``{id}``.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "setting": {
          "id": "YWRtaW4=",
          "name": "admin",
          "attributes": {
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "telephoneNumber": "",
            "uidNumber": "",
            "gidNumber": "",
            "homeDirectory": ""
          },
          "roles": ["YWRtaW4=", "Z3Vlc3Q="],
          "groups": [],
          "version_no": 1
        }
      }
    }

.. note::

   ``attributes`` incluye todos los atributos almacenados para el usuario, excepto ``name``, ``password``, ``roles`` y ``groups``.
   ``password`` no se incluye en la respuesta.

Crear Usuario
=============

Solicitud
---------

::

    POST /api/admin/user/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "confirm_password": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["Z3Vlc3Q="],
      "groups": ["group_id_1"]
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
     - Nombre de usuario (ID de inicio de sesión)
   * - ``password``
     - Sí
     - Contraseña
   * - ``confirm_password``
     - No
     - Contraseña de confirmación
   * - ``attributes``
     - No
     - Mapa de atributos (véase más adelante)
   * - ``roles``
     - No
     - Array de IDs de roles
   * - ``groups``
     - No
     - Array de IDs de grupos

.. note::

   En ``roles`` y ``groups`` indique el ID del rol o del grupo, no su nombre. Un ID que no existe (incluido el nombre de un rol o de un grupo) se rechaza con ``400``.
   Los ID se pueden consultar en el ``id`` que devuelven ``GET /api/admin/role/settings`` y ``GET /api/admin/group/settings``.
   El ID de un rol o grupo creado en la interfaz de administración o mediante la API es su nombre codificado en Base64 URL (por ejemplo, ``YWRtaW4=`` para el rol ``admin`` y ``Z3Vlc3Q=`` para ``guest``, que existen por defecto).

.. note::

   Se aplican las mismas verificaciones de contraseña que en la interfaz de administración. Se rechazan con ``400`` una creación sin ``password``, un ``confirm_password`` que no coincide con ``password`` (``confirm_password`` puede omitirse) y una contraseña que incumple la política de contraseñas (``password.min.length`` (por defecto ``8``), ``password.max.length``, ``password.require.*`` y ``password.invalid.admin.passwords`` de ``fess_config.properties``).

Las claves de ``attributes`` son los nombres de atributos de la entidad de usuario (los nombres de elementos derivados del esquema LDAP).
Las claves más comunes son:

- ``surname``, ``givenName``, ``displayName``, ``mail``
- ``telephoneNumber``, ``mobile``, ``homePhone``
- ``employeeNumber``, ``title``, ``description``, ``homeDirectory``
- ``uidNumber``, ``gidNumber``

``uidNumber`` y ``gidNumber`` deben ser numéricos (su tipo se valida en la actualización).
También se pueden especificar muchas otras claves de atributos LDAP.

.. note::

   En la creación, el ID de usuario (ID de documento) se genera automáticamente como el valor codificado en Base64 URL del nombre de usuario
   (por ejemplo, el nombre de usuario ``admin`` se convierte en ``YWRtaW4=``).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

- ``id`` : El ID de documento del usuario creado.
- ``created`` : ``true`` cuando se ha creado.

Actualizar Usuario
==================

Solicitud
---------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "confirm_password": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["Z3Vlc3Q=", "YWRtaW4="],
      "groups": ["group_id_1", "group_id_2"],
      "version_no": 1
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripción
   * - ``id``
     - Sí
     - El ID de documento del usuario a actualizar.
   * - ``name``
     - Sí
     - Nombre de usuario (ID de inicio de sesión)
   * - ``version_no``
     - Sí
     - Número de versión (para bloqueo optimista)
   * - ``password``
     - No
     - Nueva contraseña (se actualiza solo cuando se especifica)
   * - ``confirm_password``
     - No
     - Contraseña de confirmación
   * - ``attributes``
     - No
     - Mapa de atributos (véase "Crear Usuario")
   * - ``roles``
     - No
     - Array de IDs de roles
   * - ``groups``
     - No
     - Array de IDs de grupos

.. note::

   En la actualización, ``id``, ``name`` y ``version_no`` son obligatorios.
   ``version_no`` es el valor devuelto al obtener el usuario objetivo (GET), y corresponde a la versión del documento de OpenSearch.
   Si no coincide con la versión actual, la solicitud se trata como un conflicto y la actualización es rechazada.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` : ``false`` para una actualización.

Eliminar Usuario
================

Solicitud
---------

::

    DELETE /api/admin/user/setting/{id}

Especifique el ID de documento del usuario a eliminar en ``{id}``.

.. note::

   No es posible eliminar el usuario que tiene la sesión actualmente iniciada.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

- ``id`` : El ID de documento del usuario eliminado.

Ejemplos de Uso
===============

Crear Nuevo Usuario
-------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "confirm_password": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
           "roles": ["Z3Vlc3Q="],
           "groups": []
         }'

Cambiar Roles de Usuario
------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "user_id_123",
           "name": "john.doe",
           "roles": ["Z3Vlc3Q=", "YWRtaW4="],
           "version_no": 1
         }'

Referencia
==========

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-role` - API de gestión de roles
- :doc:`api-admin-group` - API de gestión de grupos
- :doc:`../../admin/user-guide` - Guía de gestión de usuarios
