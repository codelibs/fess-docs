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
   * - ``permission_state``
     - string
     - Indica si se han resuelto los permisos de grupo y de rol del usuario (``RESOLVED``, ``PENDING`` o ``FAILED``). ``PENDING`` (todavía se están resolviendo) y ``FAILED`` (han fallado o solo se han resuelto en parte) significan que el usuario tiene menos permisos de los que debería, por lo que una búsqueda puede omitir documentos que el usuario debería poder ver. (Obligatorio)

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
          "admin": true,
          "permission_state": "RESOLVED"
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
   * - 400 Bad Request
     - Cuando se ha indicado un parámetro de la solicitud que no se puede decodificar (por ejemplo, ``?q=%ff``). El ``error.code`` es ``invalid_request``.
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
Cuando el inicio de sesión es exitoso, se rota el ID de sesión del servlet, se emite un nuevo token CSRF. Además, se borra el registro de los intentos fallidos anteriores para la misma combinación de IP del cliente y nombre de usuario (el cubo por usuario). El cubo por IP no se borra, porque también cuenta los intentos realizados contra otros usuarios desde la misma IP; solo se devuelve la plaza que consumió este intento.

El límite de velocidad se aplica en dos ejes: por IP del cliente y por usuario. Cuando se supera el límite por IP, se devuelve ``429 Too Many Requests`` junto con una cabecera ``Retry-After`` (en segundos). Cuando se supera el límite por usuario, se devuelve el mismo ``401 Unauthorized`` que para credenciales inválidas (sin cabecera ``Retry-After``), de modo que el estado del contador no pueda inferirse desde el exterior.

Incluso con una sesión ya autenticada, no se realiza un cortocircuito; las credenciales proporcionadas se verifican siempre.

``return_to`` debe ser una ruta relativa que coincida con ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$``.
Además, las rutas relativas al protocolo (que comienzan con ``//``) y las que contienen caracteres de control ASCII son rechazadas y eliminadas silenciosamente de la respuesta devuelta.

.. note::

   Este endpoint está **excluido de CSRF** (porque el token no existe antes del inicio de sesión).

.. note::

   A diferencia de otros endpoints que modifican el estado, este endpoint agrupa los cuerpos de solicitud excesivos y los ``Content-Type`` no admitidos como ``400 invalid_request`` (otros endpoints devuelven ``413`` / ``415``).

.. note::

   Los límites de velocidad para el inicio de sesión y el cambio de contraseña pueden configurarse con las siguientes propiedades (valor predeterminado entre paréntesis):

   - ``theme.api.login.rate.limit.per.ip.per.minute`` (``10``): Número máximo de intentos por minuto por dirección IP. Se aplica tanto a ``/auth/login`` como al formulario de inicio de sesión ``POST /login/login``, que comparten el mismo cubo.
   - ``theme.api.login.rate.limit.per.user.per.minute`` (``5``): Número máximo de intentos por minuto por usuario. Se aplica a ``/auth/login`` y ``POST /login/login`` (que comparten un cubo por cada combinación de IP del cliente y nombre de usuario) y a ``/auth/password``.
   - ``theme.api.login.lockout.seconds`` (``900``): Duración del bloqueo (en segundos) una vez superado el límite. Se devuelve como valor de la cabecera ``Retry-After``.

   El formulario de inicio de sesión (``POST /login/login``) comparte los cubos y el bloqueo con ``/auth/login``, por lo que los fallos en el formulario cuentan para el límite de ``/auth/login`` y viceversa. Cuando se supera el límite en el formulario, se trata como un error de inicio de sesión normal en lugar de ``429``.

   Detrás de un proxy inverso que no figura en ``rate.limit.trusted.proxies`` (valor predeterminado ``127.0.0.1,::1``), todos los clientes se tratan como una única dirección IP (la del proxy). Los inicios de sesión fallidos repetidos pueden entonces bloquear a todos los usuarios durante el tiempo de bloqueo. Añada la dirección del proxy a ``rate.limit.trusted.proxies`` para que la IP real del cliente se tome de ``X-Forwarded-For``.

Cuerpo de la solicitud (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El Content-Type es ``application/json`` (charset ``UTF-8``). El tamaño máximo del cuerpo de la solicitud es de ``4 KiB``.

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
          "admin": true,
          "permission_state": "RESOLVED"
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
   * - 403 Forbidden
     - Cuando la solicitud se ha bloqueado por ser de origen cruzado: su encabezado ``Origin`` (o ``Referer``) indica un origen no permitido. Es la comprobación básica que supera toda solicitud que modifica el estado y es independiente del token CSRF, que el inicio de sesión no necesita.
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 429 Too Many Requests
     - Cuando se supera el límite de velocidad. La cabecera ``Retry-After`` indica los segundos que se deben esperar.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.
   * - 503 Service Unavailable
     - Cuando el motor de búsqueda no ha podido atender la solicitud: no está accesible o la ha rechazado por falta de capacidad. ``error.code`` es ``service_unavailable`` y un encabezado ``Retry-After`` indica los segundos que hay que esperar (``5``). La solicitud en sí es correcta, así que vuelva a intentarlo tras una breve espera.

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
   * - 400 Bad Request
     - Cuando se ha indicado un parámetro de la solicitud que no se puede decodificar (por ejemplo, ``?q=%ff``). El ``error.code`` es ``invalid_request``.
   * - 403 Forbidden
     - Cuando el token CSRF está ausente o ha expirado.
   * - 405 Method Not Allowed
     - Cuando se especifica un método distinto a POST. Se añade la cabecera ``Allow: POST``.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

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

Este endpoint tiene un límite de velocidad por usuario; cuando se supera, se devuelve ``429 Too Many Requests`` junto con una cabecera ``Retry-After`` (la configuración es compartida con el inicio de sesión).

Cuerpo de la solicitud (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El Content-Type es ``application/json`` (charset ``UTF-8``). El tamaño máximo del cuerpo de la solicitud es de ``4 KiB``.

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
     - Nueva contraseña. Debe cumplir con la política de contraseñas configurada (mínimo 8 caracteres de forma predeterminada). ``minLength`` es 1.
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
   * - 503 Service Unavailable
     - Cuando el motor de búsqueda no ha podido atender la solicitud: no está accesible o la ha rechazado por falta de capacidad. ``error.code`` es ``service_unavailable`` y un encabezado ``Retry-After`` indica los segundos que hay que esperar (``5``). La solicitud en sí es correcta, así que vuelva a intentarlo tras una breve espera.
