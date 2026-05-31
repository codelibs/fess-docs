================================
API de autenticación y sesión
================================

Descripción general
===================

La API v2 utiliza autenticación basada en sesión.
El inicio de sesión se realiza mediante ``POST /auth/login``; si tiene éxito, se establece una sesión y se emite un token CSRF.

Las solicitudes que modifican el estado (``POST``) requieren la cabecera ``X-Fess-CSRF-Token``.
Para la obtención del token CSRF, el mecanismo de rotación, el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

Esta página describe los siguientes cuatro endpoints:

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Lista de endpoints
   :header-rows: 1
   :widths: 25 15 60

   * - Endpoint
     - Método
     - Descripción
   * - ``/auth/me``
     - GET
     - Obtiene el usuario autenticado actualmente.
   * - ``/auth/login``
     - POST
     - Inicia sesión con nombre de usuario y contraseña.
   * - ``/auth/logout``
     - POST
     - Cierra la sesión (idempotente).
   * - ``/auth/password``
     - POST
     - Cambia la contraseña del usuario actual.

.. _api-auth-userpayload:

Información de usuario común (UserPayload)
==========================================

La información de usuario incluida en las respuestas de ``GET /auth/me`` y ``POST /auth/login`` se devuelve con la estructura común ``UserPayload``.
Todos los campos de tipo array son no nulos; cuando no hay valores, se devuelve un array vacío.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: UserPayload
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Descripción
   * - ``user_id``
     - string
     - ID de usuario. (Obligatorio)
   * - ``username``
     - string
     - Nombre de usuario mostrado en el menú de cuenta de la SPA. Actualmente tiene el mismo valor que ``user_id``, pero en el futuro el backend podría proporcionarlo de forma independiente. (Obligatorio)
   * - ``name``
     - string
     - Nombre para mostrar en el menú de cuenta de la SPA. Actualmente tiene el mismo valor que ``user_id``. (Obligatorio)
   * - ``roles``
     - string[]
     - Array de roles del usuario. (Obligatorio)
   * - ``groups``
     - string[]
     - Array de grupos del usuario. (Obligatorio)
   * - ``permissions``
     - string[]
     - Array de permisos del usuario. (Obligatorio)
   * - ``editable``
     - boolean
     - Si la información del usuario es editable. (Obligatorio)
   * - ``admin``
     - boolean
     - ``true`` cuando el usuario tiene alguno de los ``authentication.admin.roles`` configurados. Controla la visualización del elemento "Administration" en la SPA. (Obligatorio)

Obtención del estado de autenticación
======================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/auth/me``
==================  ====================================================

Obtiene el usuario autenticado actualmente.
Las llamadas anónimas no generan un error; se devuelve ``authenticated: false``.
Cuando está autenticado, ``user`` contiene un :ref:`UserPayload <api-auth-userpayload>`.

Respuesta
---------

En caso de éxito (HTTP 200), se devuelve una respuesta con el formato de sobre común como la siguiente (ejemplo autenticado):

.. code-block:: json

    {
      "response": {
        "status": 0,
        "authenticated": true,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        }
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Información de respuesta
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Descripción
   * - ``authenticated``
     - boolean
     - Si está autenticado. (Obligatorio)
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`. Solo existe cuando ``authenticated`` es ``true``.

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error
   :header-rows: 1
   :widths: 25 75

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Inicio de sesión
================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/auth/login``
==================  ====================================================

Inicia sesión con nombre de usuario y contraseña.
Cuando el inicio de sesión es exitoso, se rota el ID de sesión del servlet, se emite un nuevo token CSRF y se borran los cubos de límite de velocidad para la IP del cliente y el usuario objetivo.
Cuando se supera el límite de velocidad, se añade la cabecera ``Retry-After`` (en segundos).

Incluso con una sesión ya autenticada, no se realiza un cortocircuito; las credenciales proporcionadas se verifican siempre.

``return_to`` debe ser una ruta relativa que coincida con ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$``.
Además, las rutas relativas al protocolo (que comienzan con ``//``) y las que contienen caracteres de control ASCII son rechazadas y eliminadas silenciosamente de la respuesta devuelta.

.. note::

   Este endpoint está **excluido de CSRF** (porque el token no existe antes del inicio de sesión).

.. note::

   A diferencia de otros endpoints que modifican el estado, este endpoint agrupa los cuerpos de solicitud excesivos y los ``Content-Type`` no admitidos como ``400 invalid_request`` (otros endpoints devuelven ``413`` / ``415``).

Cuerpo de la solicitud (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El Content-Type es ``application/json``.

.. tabularcolumns:: |p{3cm}|p{2cm}|p{2cm}|p{7cm}|
.. list-table:: LoginRequest
   :header-rows: 1
   :widths: 20 12 12 56

   * - Campo
     - Tipo
     - Obligatorio
     - Descripción
   * - ``username``
     - string
     - Sí
     - Nombre de usuario. ``minLength`` es 1.
   * - ``password``
     - string
     - Sí
     - Contraseña. ``minLength`` es 1.
   * - ``return_to``
     - string
     - No
     - Destino de redirección después del inicio de sesión. Debe ser una ruta relativa que coincida con el patrón indicado.

Ejemplo de solicitud:

.. code-block:: json

    {
      "username": "taro",
      "password": "secret",
      "return_to": "/search"
    }

Respuesta
---------

En caso de éxito (HTTP 200, LoginResponse), se devuelve una respuesta con el formato de sobre común como la siguiente:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        },
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f",
        "return_to": "/search"
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Información de respuesta
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Descripción
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`.
   * - ``csrf_token``
     - string
     - Nuevo token CSRF asociado a la nueva sesión. (Obligatorio)
   * - ``return_to``
     - string
     - Solo se devuelve si el valor de la solicitud pasó la lista de permitidos.

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error
   :header-rows: 1
   :widths: 25 75

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida (incluye cuerpo de solicitud excesivo y ``Content-Type`` no admitido).
   * - 401 Unauthorized
     - Cuando las credenciales son inválidas.
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 429 Too Many Requests
     - Cuando se supera el límite de velocidad. La cabecera ``Retry-After`` indica los segundos que se deben esperar.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Cierre de sesión
================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/auth/logout``
==================  ====================================================

Cierra la sesión. Esta operación es idempotente; si no hay sesión activa, funciona como no-op sin devolver un error. Siempre devuelve ``ok: true``.

Se requiere la cabecera ``X-Fess-CSRF-Token``.

Respuesta
---------

En caso de éxito (HTTP 200, OkResponse), se devuelve una respuesta con el formato de sobre común como la siguiente:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Información de respuesta
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Descripción
   * - ``ok``
     - boolean
     - Siempre ``true``. (Obligatorio)

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error
   :header-rows: 1
   :widths: 25 75

   * - Código de estado
     - Descripción
   * - 403 Forbidden
     - Cuando el token CSRF está ausente o ha expirado.
   * - 405 Method Not Allowed
     - Cuando se especifica un método distinto a POST. Se añade la cabecera ``Allow: POST``.

Cambio de contraseña
====================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/auth/password``
==================  ====================================================

Cambia la contraseña del usuario actual.
Verifica ``current_password``, aplica la política de contraseñas configurada a ``new_password``, invalida la sesión actual e indica a la SPA que redirija a la página de inicio de sesión con ``re_login_required: true``.

Dado que la sesión se destruye en el servidor, no se devuelve ``csrf_token``. La SPA debe obtener un nuevo token tras la reautenticación.

Se requiere la cabecera ``X-Fess-CSRF-Token``.

Cuerpo de la solicitud (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El Content-Type es ``application/json``.

.. tabularcolumns:: |p{3.5cm}|p{2cm}|p{2cm}|p{6.5cm}|
.. list-table:: PasswordChangeRequest
   :header-rows: 1
   :widths: 22 12 12 54

   * - Campo
     - Tipo
     - Obligatorio
     - Descripción
   * - ``current_password``
     - string
     - Sí
     - Contraseña actual. ``minLength`` es 1.
   * - ``new_password``
     - string
     - Sí
     - Nueva contraseña. Debe cumplir con la política de contraseñas configurada. ``minLength`` es 1.
   * - ``confirm_password``
     - string
     - Sí
     - Contraseña de confirmación. Debe coincidir con ``new_password``. ``minLength`` es 1.

Respuesta
---------

En caso de éxito (HTTP 200), se devuelve una respuesta con el formato de sobre común como la siguiente:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true,
        "re_login_required": true
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Información de respuesta
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Descripción
   * - ``ok``
     - boolean
     - Siempre ``true``. (Obligatorio)
   * - ``re_login_required``
     - boolean
     - Siempre ``true``. La sesión actual ha sido invalidada en el servidor. La SPA debe redirigir a la página de inicio de sesión para obtener una nueva sesión y un nuevo token CSRF. (Obligatorio)

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error
   :header-rows: 1
   :widths: 25 75

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida.
   * - 401 Unauthorized
     - Cuando se requiere autenticación o ``current_password`` es inválida.
   * - 403 Forbidden
     - Cuando el token CSRF está ausente o ha expirado.
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 413 Payload Too Large
     - Cuando el cuerpo de la solicitud supera el límite de tamaño.
   * - 415 Unsupported Media Type
     - Cuando el ``Content-Type`` no es admitido.
   * - 429 Too Many Requests
     - Cuando se supera el límite de velocidad.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.
