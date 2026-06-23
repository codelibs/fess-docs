==========================
API de User
==========================

Vision General
==============

La API de User es una API REST para gestionar cuentas de usuario de |Fess|.
Permite crear, obtener, actualizar y eliminar usuarios, ademas de asignar roles y grupos.

Esta es una API de administracion, y el acceso requiere autenticacion con un token de acceso de administrador.
Consulte :doc:`api-admin-overview` para conocer el metodo de autenticacion y las especificaciones comunes.

Cada respuesta esta envuelta en un objeto ``response`` e incluye los siguientes campos comunes:

- ``version`` : La cadena de version del producto |Fess|.
- ``status`` : El codigo de estado del resultado (``0`` =exito, ``1`` =solicitud incorrecta, ``2`` =error del sistema, ``3`` =no autorizado, ``9`` =fallo).

URL Base
========

::

    /api/admin/user

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

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 10 65

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``size``
     - Integer
     - No
     - Numero de elementos por pagina. El valor predeterminado es el valor configurado ``paging.page.size`` (predeterminado: 25).
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 1). El valor predeterminado es 1.

.. note::

   En la implementacion actual, el endpoint de lista de usuarios no aplica los parametros ``size`` y ``page``.
   Siempre devuelve la primera pagina, con el numero de elementos definido por la configuracion del servidor ``paging.page.size`` (predeterminado: 25), ordenado por nombre de usuario (``name``) en orden ascendente.
   El numero total de usuarios coincidentes esta disponible en ``response.total``.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
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
            "roles": ["admin"],
            "groups": [],
            "versionNo": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` : El array de usuarios en la pagina actual.
- ``total`` : El numero total de usuarios coincidentes.

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
        "version": "15.7.0",
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
          "roles": ["admin"],
          "groups": [],
          "versionNo": 1
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
      "confirmPassword": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["user"],
      "groups": ["group_id_1"]
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre de usuario (ID de inicio de sesion)
   * - ``password``
     - No
     - Contrasena
   * - ``confirmPassword``
     - No
     - Contrasena de confirmacion
   * - ``attributes``
     - No
     - Mapa de atributos (vease mas adelante)
   * - ``roles``
     - No
     - Array de IDs de roles
   * - ``groups``
     - No
     - Array de IDs de grupos

.. note::

   La API REST no realiza la verificacion de contrasena obligatoria, la verificacion de coincidencia entre ``password`` y ``confirmPassword``, ni la validacion de politica de contrasenas (estas se aplican unicamente en la interfaz de administracion).
   En la practica, se recomienda especificar una ``password`` valida cuyo valor coincida con ``confirmPassword``.

Las claves de ``attributes`` son los nombres de atributos de la entidad de usuario (los nombres de elementos derivados del esquema LDAP).
Las claves mas comunes son:

- ``surname``, ``givenName``, ``displayName``, ``mail``
- ``telephoneNumber``, ``mobile``, ``homePhone``
- ``employeeNumber``, ``title``, ``description``, ``homeDirectory``
- ``uidNumber``, ``gidNumber``

``uidNumber`` y ``gidNumber`` deben ser numericos (su tipo se valida en la actualizacion).
Tambien se pueden especificar muchas otras claves de atributos LDAP.

.. note::

   En la creacion, el ID de usuario (ID de documento) se genera automaticamente como el valor codificado en Base64 URL del nombre de usuario
   (por ejemplo, el nombre de usuario ``admin`` se convierte en ``YWRtaW4=``).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
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
      "confirmPassword": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripcion
   * - ``id``
     - Si
     - El ID de documento del usuario a actualizar.
   * - ``name``
     - Si
     - Nombre de usuario (ID de inicio de sesion)
   * - ``versionNo``
     - Si
     - Numero de version (para bloqueo optimista)
   * - ``password``
     - No
     - Nueva contrasena (se actualiza solo cuando se especifica)
   * - ``confirmPassword``
     - No
     - Contrasena de confirmacion
   * - ``attributes``
     - No
     - Mapa de atributos (vease "Crear Usuario")
   * - ``roles``
     - No
     - Array de IDs de roles
   * - ``groups``
     - No
     - Array de IDs de grupos

.. note::

   En la actualizacion, ``id``, ``name`` y ``versionNo`` son obligatorios.
   ``versionNo`` es el valor devuelto al obtener el usuario objetivo (GET), y corresponde a la version del documento de OpenSearch.
   Si no coincide con la version actual, la solicitud se trata como un conflicto y la actualizacion es rechazada.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` : ``false`` para una actualizacion.

Eliminar Usuario
================

Solicitud
---------

::

    DELETE /api/admin/user/setting/{id}

Especifique el ID de documento del usuario a eliminar en ``{id}``.

.. note::

   No es posible eliminar el usuario que tiene la sesion actualmente iniciada.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
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
           "confirmPassword": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
           "roles": ["user"],
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
           "roles": ["user", "editor", "admin"],
           "versionNo": 1
         }'

Referencia
==========

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-role` - API de gestion de roles
- :doc:`api-admin-group` - API de gestion de grupos
- :doc:`../../admin/user-guide` - Guia de gestion de usuarios
