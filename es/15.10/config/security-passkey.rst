=================================================================
Configuración del inicio de sesión con llave de acceso (WebAuthn)
=================================================================

Descripción general
===================

|Fess| permite que un usuario local (un usuario creado en «Usuario» de la pantalla de administración) inicie sesión con una llave de acceso (passkey, WebAuthn) en lugar de una contraseña. La función es nueva en 15.10 y está desactivada de forma predeterminada.

- Un usuario puede iniciar sesión con la contraseña o con una llave de acceso. No es una autenticación multifactor que exija ambas.
- Solo se contemplan los usuarios locales del índice ``fess_user``. Un usuario de LDAP o SSO no puede registrar una llave de acceso, y un inicio de sesión con llave de acceso nunca consulta a LDAP.
- |Fess| almacena la clave pública, el nombre de la llave de acceso y datos similares. La clave privada permanece en el autenticador del usuario (un navegador, un sistema operativo, una llave de seguridad, etc.) y nunca llega a |Fess|.

Configuración
=============

Los ajustes de las llaves de acceso se escriben en ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` en el paquete ZIP, ``/etc/fess/fess_config.properties`` en RPM/DEB). No hay ningún elemento para ellos en «Sistema» > «General» de la pantalla de administración, y no se pueden definir en ``system.properties``. Para aplicar un cambio es necesario reiniciar |Fess|. Con Docker, puede pasarlos como ``-Dfess.config.passkey.enabled=true`` en ``FESS_JAVA_OPTS`` (consulte :doc:`../install/install-docker`).

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Clave
     - Valor predeterminado
     - Descripción
   * - ``passkey.enabled``
     - ``false``
     - Habilita el inicio de sesión con llave de acceso. Aunque sea ``true``, la función permanece desactivada a menos que ``passkey.rp.id`` y ``passkey.origins`` (más abajo) contengan valores utilizables.
   * - ``passkey.rp.id``
     - (vacío)
     - ID de la parte confiante (relying party): el dominio al que quedan vinculadas las llaves de acceso (por ejemplo, ``example.com``). Una llave de acceso funciona solo en este host y en sus subdominios.
   * - ``passkey.rp.name``
     - ``Fess``
     - El nombre de la parte confiante que muestra el navegador al crear una llave de acceso.
   * - ``passkey.origins``
     - (vacío)
     - Los orígenes (separados por comas) desde los que se acepta una ceremonia de llave de acceso (por ejemplo, ``https://fess.example.com``). Cada entrada debe ser un origen ``http`` o ``https`` con un nombre de host.

Un ejemplo que activa la función:
::

    passkey.enabled=true
    passkey.rp.id=example.com
    passkey.rp.name=Fess
    passkey.origins=https://fess.example.com

- ``passkey.rp.id`` es el dominio al que quedan vinculadas todas las llaves de acceso. Si se cambia después de que los usuarios hayan registrado llaves de acceso, todas dejan de ser utilizables y los usuarios deben registrarlas de nuevo con el nuevo ID, así que elíjalo una sola vez. El host de cada origen de ``passkey.origins`` debe ser ``passkey.rp.id`` o un subdominio de él.
- ``passkey.origins`` enumera tal cual los orígenes (esquema, host y puerto) con los que los usuarios abren |Fess| en el navegador, no las direcciones que hay detrás de un proxy inverso. Una ceremonia desde cualquier otro origen se rechaza.

Cuándo permanece desactivada la función
---------------------------------------

Incluso con ``passkey.enabled=true``, las llaves de acceso **permanecen desactivadas sin ningún error en pantalla** en los casos siguientes. Las pantallas de inicio de sesión no muestran ningún botón de llave de acceso, todas las API bajo ``/api/v2/auth/passkey`` responden ``404`` y ``features.passkey_enabled`` de ``/api/v2/ui/config`` es ``false``. El motivo consta en una advertencia de ``fess.log``; cada advertencia se escribe solo una vez tras el arranque.

- ``passkey.rp.id`` o ``passkey.origins`` está vacío: ``passkey.enabled is true but passkey.rp.id or passkey.origins is empty, so passkeys are disabled.``
- ``passkey.origins`` no contiene ninguna entrada: ``passkey.enabled is true but passkey.origins holds no origin, so passkeys are disabled.``
- ``passkey.origins`` contiene una entrada que no es un origen ``http`` o ``https`` (un valor sin nombre de host, otro esquema, etc.): ``passkey.origins holds an entry that is not an http or https origin, so passkeys are disabled: entry=...``

Cuando ``passkey.origins`` es utilizable pero el origen con el que el usuario abre |Fess| no figura en él, se rechazan todos los registros y todos los inicios de sesión. La pantalla del usuario no muestra el motivo, así que consulte ``fess.log``: ``A passkey response came from an origin that is not in passkey.origins: origin=...`` indica el origen rechazado y el ajuste (solo se escribe el primero). Añada ese origen a ``passkey.origins``.

Uso
===

Inicio de sesión
----------------

Cuando las llaves de acceso están activadas y el navegador admite WebAuthn, aparece un botón «Iniciar sesión con una llave de acceso» en el inicio de sesión de la pantalla de búsqueda y en la página de inicio de sesión de la pantalla de administración. El navegador solicita el autenticador y el usuario inicia sesión sin escribir un nombre de usuario.

Un inicio de sesión con llave de acceso usa el mismo límite de tasa por dirección IP (``theme.api.login.*``) que un inicio de sesión con contraseña. Un fallo cuenta para el límite y un éxito devuelve el recuento (consulte :doc:`rate-limiting`). La pantalla no indica el motivo del fallo; muestra el mismo mensaje que ante una contraseña incorrecta.

Registro y eliminación de llaves de acceso
------------------------------------------

Un usuario local registra y elimina sus propias llaves de acceso en «Llaves de acceso» dentro de «Cambiar contraseña» (``/profile``) en el menú de usuario de la pantalla de búsqueda.

1. Introduzca un nombre para la llave de acceso (hasta 64 caracteres) y la contraseña actual, y pulse «Registrar una llave de acceso».
2. Siga las indicaciones del navegador para crear la llave de acceso en un autenticador.

- La contraseña actual es necesaria en cada registro. Un usuario local cuyo nombre y contraseña también acepta el directorio (LDAP) no puede registrar una llave de acceso, porque la comprobación de la contraseña no puede saber qué cuenta ha verificado.
- Un usuario puede tener hasta 20 llaves de acceso.
- La sección «Llaves de acceso» no se muestra a un usuario que no tiene llaves de acceso y no puede registrar ninguna (un usuario de LDAP o SSO, o un navegador sin WebAuthn).
- Eliminar una llave de acceso **cierra las demás sesiones de inicio de sesión** del usuario, para que no sobreviva una sesión abierta con un autenticador perdido. Funciona igual que un cambio de contraseña (consulte «Relación con la contraseña» más abajo). La sesión que realizó la eliminación se mantiene.

Acciones del administrador
--------------------------

La página de detalles de un usuario en «Usuario» de la pantalla de administración enumera las llaves de acceso del usuario (etiqueta, hora de creación, hora del último uso). Un administrador no puede registrar una llave de acceso, pero un administrador con permiso de edición puede eliminar una con «Restablecer», por ejemplo cuando el usuario ha perdido el autenticador. A continuación, el usuario puede registrar una llave de acceso nueva. Un restablecimiento también cierra las sesiones de inicio de sesión de ese usuario (consulte «Relación con la contraseña» más abajo).

Después de volver a establecer ``passkey.enabled`` en ``false``, la página de detalles sigue enumerando las llaves de acceso de un usuario que las tenga, y pueden eliminarse. Desactivar la función no elimina los datos de las llaves de acceso.

Relación con la contraseña
==========================

- Una llave de acceso y una contraseña son credenciales independientes. Cambiar la contraseña de un usuario, o que un administrador establezca una nueva, no elimina las llaves de acceso registradas, y siguen pudiendo usarse para iniciar sesión.
- Cuando se cambia una contraseña, las demás sesiones de inicio de sesión del usuario terminan (consulte :doc:`../install/security`). Esto incluye una sesión abierta con una llave de acceso. Cada sesión comprueba como máximo una vez cada ``password.changed.check.interval`` segundos (valor predeterminado ``60``), por lo que las sesiones terminan dentro de ese tiempo.
- Eliminar una llave de acceso cierra las demás sesiones de la misma manera (véase más arriba).

Eliminación y cambio de nombre de usuarios
==========================================

Una llave de acceso se vincula a un usuario únicamente por su nombre de usuario. Para que otro usuario con el mismo nombre no la herede, las llaves de acceso también se eliminan en estos casos:

- Cuando se elimina un usuario.
- Cuando se crea un usuario (se elimina cualquier llave de acceso que quede con ese nombre).
- Cuando se cambia el nombre de un usuario (se eliminan las llaves de acceso del nombre anterior y del nuevo). Una llave de acceso no sigue al cambio de nombre, por lo que el usuario debe registrarla de nuevo. Un cambio de nombre a uno que ya tiene otro usuario se rechaza antes de eliminar ninguna llave de acceso.

Almacenamiento y copia de seguridad
===================================

Las llaves de acceso se almacenan en el índice ``fess_user.passkey`` (el prefijo es ``index.user.index``, ``fess_user`` de forma predeterminada). El índice se crea cuando arranca |Fess| aunque las llaves de acceso estén desactivadas, y se usa al eliminar o cambiar el nombre de un usuario y en la página de detalles del usuario. Si |Fess| no tiene permiso para crear índices, créelo antes de la actualización (consulte :ref:`upgrade-1510-passkey`).

El índice no se une al alias ``fess_user``, por lo que ``fess_user.bulk`` de «Copia de seguridad» en la pantalla de administración no contiene llaves de acceso. Tras restaurar una copia de seguridad, los usuarios deben registrar de nuevo sus llaves de acceso.

Requisitos
==========

- **HTTPS**: los navegadores permiten WebAuthn solo en un contexto seguro (HTTPS o ``localhost``). |Fess| también acepta un origen ``http`` en ``passkey.origins``, pero en producción sirva |Fess| mediante HTTPS e indique orígenes ``https://`` (consulte «Habilitación de HTTPS» en :doc:`../install/security`).
- **Navegador**: se requiere un navegador que ofrezca la API WebAuthn (``PublicKeyCredential``). En un navegador que no la tenga, no se muestra ni el botón de inicio de sesión ni la sección de registro.
- **Autenticador**: debe admitir credenciales detectables (discoverable credentials) y verificación de usuario (un PIN, biometría, etc.). |Fess| exige ambas, admite los algoritmos de firma ES256 y RS256 y no usa atestación.
- **Varios nodos**: el desafío (challenge) de una ceremonia de llave de acceso se conserva en la sesión HTTP durante 5 minutos. Si ejecuta varios nodos detrás de un balanceador de carga, comparta las sesiones entre los nodos (variable de entorno ``FESS_SESSION_STORE=opensearch``) o haga que el balanceador de carga fije cada sesión a un nodo.

API
===

Las API de llaves de acceso están bajo ``/api/v2/auth/passkey``. Todas responden ``404`` mientras las llaves de acceso están desactivadas. ``features.passkey_enabled`` de ``/api/v2/ui/config`` indica si la función está disponible (consulte :doc:`../api/api-uiconfig`).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Endpoint
     - Descripción
   * - ``POST /api/v2/auth/passkey/login/options``
     - Obtiene las opciones de inicio de sesión (el desafío).
   * - ``POST /api/v2/auth/passkey/login/verify``
     - Verifica la respuesta del autenticador e inicia sesión.
   * - ``GET /api/v2/auth/passkey``
     - Enumera las llaves de acceso del usuario con sesión iniciada e indica si el usuario puede registrar una (``can_register``).
   * - ``POST /api/v2/auth/passkey/register/options``
     - Comprueba la contraseña actual (``current_password``) y obtiene las opciones de registro.
   * - ``POST /api/v2/auth/passkey/register/verify``
     - Verifica el nombre (``label``) y la respuesta del autenticador, y registra la llave de acceso.
   * - ``DELETE /api/v2/auth/passkey/{credentialId}``
     - Elimina una llave de acceso del usuario con sesión iniciada.

Las llamadas ``register`` y la eliminación necesitan el encabezado ``X-Fess-CSRF-Token``. Las dos llamadas de inicio de sesión no necesitan token CSRF, igual que ``/api/v2/auth/login``.

Solución de problemas
=====================

No se muestra el botón de llave de acceso
-----------------------------------------

- Compruebe ``features.passkey_enabled`` de ``/api/v2/ui/config``. Si es ``false``, busque una advertencia en ``fess.log`` para ver si los ajustes son utilizables (consulte «Cuándo permanece desactivada la función» más arriba).
- Compruebe que |Fess| se reinició tras el cambio.
- Compruebe que el navegador admite WebAuthn y que la página se abre mediante HTTPS (o ``localhost``).
- Si usa un tema distinto del incluido, el tema debe admitir el botón de llave de acceso.

Falla el registro o el inicio de sesión
---------------------------------------

- Si ``fess.log`` contiene una advertencia con ``is not in passkey.origins``, añada a ``passkey.origins`` el origen abierto en el navegador.
- Después de cambiar ``passkey.rp.id``, las llaves de acceso registradas antes del cambio no se pueden usar. Elimine las llaves de acceso antiguas y regístrelas de nuevo.
