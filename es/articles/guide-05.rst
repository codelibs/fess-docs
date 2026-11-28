===========================================
Controlar los resultados con roles y grupos
===========================================

Introducción
============

Una vez que todos los documentos internos se pueden buscar desde un único Fess, la siguiente pregunta es "quién puede ver qué".
No conviene que los documentos de evaluación de Recursos Humanos aparezcan en los resultados de búsqueda de todos los empleados y, al contrario, tampoco que las normas para toda la empresa solo las vean unas pocas personas.

En Fess, los valores que se escriben en el campo "Permisos" de una configuración de rastreo se registran en cada documento y, en cada búsqueda, se comparan con los derechos del usuario que ha iniciado sesión.
En este artículo configuramos en Fess 15.9 una visibilidad por departamento y llegamos hasta comprobar qué documentos ve cada usuario.

Al seguir los pasos de este artículo, podrá:

- Configurar tres tipos de visibilidad (departamento, dirección, todos los empleados) con grupos y permisos
- Usar directamente los grupos de Active Directory como permisos
- Ajustar la visibilidad de las etiquetas a la de los documentos
- Comprobar qué documentos ve cada usuario y qué derechos están registrados en un documento

La configuración de SSO se trata en :doc:`guide-15`, y el uso de varias organizaciones mediante hosts virtuales en :doc:`guide-13`.

Cómo funcionan los permisos
===========================

Cómo escribir los permisos
--------------------------

En el campo "Permisos" de una configuración de rastreo, escriba valores con los siguientes formatos, uno por línea.
Si cualquiera de ellos coincide con los derechos del usuario, el documento se muestra en los resultados de búsqueda.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Formato
     - Usuarios que coinciden
   * - ``{user}nombre_usuario``
     - Ese mismo usuario
   * - ``{group}nombre_grupo``
     - Los usuarios que pertenecen a ese grupo
   * - ``{role}nombre_rol``
     - Los usuarios que tienen ese rol
   * - ``(deny){group}nombre_grupo``
     - A los usuarios que coinciden no se les muestra el documento, aunque otro valor lo permita (también se puede usar con ``{user}`` y ``{role}``)

Derechos de un usuario
----------------------

En cada búsqueda, Fess determina los derechos del usuario de la siguiente manera.

- Usuario que ha iniciado sesión: ``{user}`` con su propio nombre de usuario, ``{group}`` por cada grupo al que pertenece y ``{role}`` por cada rol que tiene
- Visitante que no ha iniciado sesión: ``{role}guest``

Lo importante aquí es que los usuarios que han iniciado sesión no reciben ``{role}guest``.
El campo "Permisos" de una configuración de rastreo nueva contiene ``{role}guest`` desde el principio.
Si lo deja así, los documentos serán visibles para los visitantes que no han iniciado sesión, pero no para los usuarios que sí lo han hecho.
Para los documentos que deban ver todos los empleados, escriba en los permisos un grupo (o rol) al que pertenezcan todos los empleados.

Tenga en cuenta también que el usuario inicial ``admin`` tiene los roles ``admin`` y ``guest``.
Si busca en un navegador que sigue con la sesión iniciada en la consola de administración, la búsqueda se realiza como ``admin``, por lo que solo se muestran los documentos con ``{role}guest`` y no los de los departamentos.

¿Roles o grupos?
----------------

Los roles y los grupos se comparan exactamente de la misma manera.
La diferencia está en el origen de los valores.
En la gestión de usuarios de Fess, puede asignar a cada usuario tanto roles como grupos.
Con la integración LDAP (Active Directory), los grupos a los que pertenece el usuario (``memberOf``) se convierten en ``{group}nombre_grupo`` (solo las entradas cuyo DN contiene ``ou=Role`` se convierten en ``{role}``).

En este artículo, todas las unidades organizativas, como los departamentos o el conjunto de los empleados, se representan como grupos, para que los mismos valores de permiso sirvan tanto para los usuarios de Fess como para Active Directory.

Lo que vamos a construir
========================

Tomamos como ejemplo una empresa cuyo portal de intranet ``https://intra.example.com/`` tiene páginas para cada departamento y páginas para toda la empresa.

.. list-table:: Grupos y usuarios
   :header-rows: 1
   :widths: 20 40 40

   * - Usuario
     - Departamento
     - Grupos
   * - ``sato``
     - Ventas
     - ``Sales``, ``AllStaff``
   * - ``suzuki``
     - Desarrollo
     - ``Engineering``, ``AllStaff``
   * - ``tanaka``
     - Recursos Humanos
     - ``HR``, ``AllStaff``
   * - ``yamada``
     - Dirección
     - ``Executives``, ``AllStaff``

.. list-table:: Permisos de las configuraciones de rastreo
   :header-rows: 1
   :widths: 25 40 35

   * - Configuración de rastreo
     - URL
     - Permisos
   * - Ventas
     - ``https://intra.example.com/sales/``
     - ``{group}Sales`` y ``{group}Executives``
   * - Desarrollo
     - ``https://intra.example.com/dev/``
     - ``{group}Engineering`` y ``{group}Executives``
   * - Recursos Humanos
     - ``https://intra.example.com/hr/``
     - ``{group}HR`` y ``{group}Executives``
   * - Toda la empresa
     - ``https://intra.example.com/common/``
     - ``{group}AllStaff``

Con esta configuración, cada usuario ve los siguientes documentos.

.. list-table:: Documentos visibles para cada usuario
   :header-rows: 1
   :widths: 30 70

   * - Usuario
     - Documentos en los resultados de búsqueda
   * - ``sato``
     - Ventas, Toda la empresa
   * - ``suzuki``
     - Desarrollo, Toda la empresa
   * - ``tanaka``
     - Recursos Humanos, Toda la empresa
   * - ``yamada``
     - Ventas, Desarrollo, Recursos Humanos, Toda la empresa
   * - Visitantes que no han iniciado sesión
     - Ninguno
   * - ``admin`` (página de búsqueda)
     - Ninguno

Si también quiere que los visitantes que no han iniciado sesión vean los documentos de toda la empresa, añada además ``{role}guest`` a la configuración de toda la empresa.
En ese caso, ``admin`` también verá los documentos de toda la empresa.

Los nombres de grupo se comparan distinguiendo entre mayúsculas y minúsculas.
``{group}sales`` y ``{group}Sales`` se tratan como grupos distintos, así que escriba el nombre del grupo y el valor del permiso exactamente igual.

Configuración con usuarios de Fess
==================================

Crear los grupos y los usuarios
-------------------------------

1. En la consola de administración, en [Usuario] > [Grupo], haga clic en [Crear nuevo], introduzca ``Sales`` en "Nombre" y haga clic en [Crear]. Cree ``Engineering``, ``HR``, ``Executives`` y ``AllStaff`` de la misma manera
2. En [Usuario] > [Usuario], haga clic en [Crear nuevo] e introduzca "Nombre de usuario", "Contraseña" y "Contraseña (confirmar)". La contraseña debe tener al menos 8 caracteres
3. En "Grupos", seleccione los grupos según la tabla anterior y haga clic en [Crear]

Los usuarios, grupos y roles se guardan en OpenSearch, por lo que se conservan aunque vuelva a crear los contenedores en Docker.

Crear las configuraciones de rastreo
------------------------------------

Para cada departamento, cree una configuración de rastreo en [Rastreador] > [Web].
La siguiente tabla muestra el ejemplo de Ventas.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Valor
   * - Nombre
     - ``Portal de Ventas``
   * - URLs
     - ``https://intra.example.com/sales/``
   * - URLs a incluir en el rastreo
     - ``https://intra.example.com/sales/.*``
   * - Permisos
     - Borre el valor inicial ``{role}guest`` e introduzca las dos líneas siguientes

::

    {group}Sales
    {group}Executives

Cree Desarrollo, Recursos Humanos y Toda la empresa de la misma manera, cambiando la URL y los permisos según la tabla.
Después, haga clic en [Iniciar ahora] para "Default Crawler" en [Sistema] > [Programador] para ejecutar el rastreo.
Para saber cómo comprobar que el rastreo ha terminado, consulte :doc:`guide-02`.

.. note::

   En las configuraciones de rastreo de sistemas de archivos (SMB o archivos locales), los derechos leídos de la ACL del archivo se registran en el documento **además** de los valores de "Permisos".
   Este comportamiento está activado de forma predeterminada.
   Por ello, los documentos de un servidor de archivos pueden mostrarse a un ámbito más amplio que el indicado en "Permisos".
   Para combinarlo con las ACL, consulte :doc:`file-server-search`.
   Los permisos de las configuraciones de rastreo de almacenes de datos se tratan en :doc:`datastore-basics`.

Usar los grupos de Active Directory
===================================

Si sus usuarios se gestionan en Active Directory, configure la integración LDAP en lugar de crear usuarios y grupos en Fess.
Los grupos del atributo ``memberOf`` del usuario que ha iniciado sesión se convierten en derechos ``{group}``.

Configurar la conexión LDAP
---------------------------

Rellene la sección "LDAP" de [Sistema] > [General] y haga clic en [Actualizar].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Ejemplo
   * - URL de LDAP
     - ``ldap://ad.example.com:389``
   * - DN base
     - ``dc=example,dc=com``
   * - DN de enlace
     - ``cn=fess,cn=Users,dc=example,dc=com`` (cuenta de servicio para las consultas)
   * - Contraseña
     - Contraseña de la cuenta de servicio
   * - DN de usuario
     - ``%s@example.com`` (``%s`` se sustituye por el nombre de inicio de sesión)
   * - Filtro de cuenta
     - ``sAMAccountName=%s``
   * - Atributo memberOf
     - ``memberOf``

Para conocer el detalle de cada campo y cómo escribir un "Filtro de grupo" que resuelva los grupos anidados, consulte la `Guía de integración LDAP <https://fess.codelibs.org/es/stable/config/ldap-integration.html>`__.

.. warning::

   Los ajustes de [General] se guardan en ``system.properties``.
   En la configuración de docker-fess, este archivo está dentro del contenedor ``fess01``, por lo que se pierde al volver a crear el contenedor con ``down`` → ``up`` (consulte la sección sobre la detención y la reanudación en :doc:`guide-02`).

Correspondencia entre nombres de grupo y permisos
-------------------------------------------------

El valor del ``CN`` más interno del DN del grupo se convierte en el nombre del grupo.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Valor de memberOf
     - Derecho del usuario
   * - ``CN=Sales,OU=Groups,DC=example,DC=com``
     - ``{group}Sales``
   * - ``CN=AllStaff,OU=Groups,DC=example,DC=com``
     - ``{group}AllStaff``

Si llama a los grupos de Active Directory ``Sales``, ``Engineering``, ``HR``, ``Executives`` y ``AllStaff``, las configuraciones de rastreo del capítulo anterior funcionan sin cambios.
Si los nombres son distintos, ajuste los valores de los permisos a los nombres de los grupos de Active Directory.

Para todos los empleados, prepare un grupo al que todos pertenezcan directamente.
El grupo principal de Active Directory (normalmente ``Domain Users``) no se incluye en el atributo ``memberOf``, por lo que escribir ``{group}Domain Users`` no produce ninguna coincidencia.

Para comprobar qué derechos ha recibido un usuario, ponga el nivel de registro de ``org.codelibs.fess.ldap`` en DEBUG.
Cuando se obtienen los derechos desde LDAP, se escribe en ``fess.log`` una línea que empieza por ``Roles:``.
Para saber cómo configurarlo, consulte la sección "Configuración de depuración" de la Guía de integración LDAP.
Los valores de esta línea se muestran en el formato interno que se describe más adelante (por ejemplo, ``2Sales``).

Para que los usuarios inicien sesión con SSO (Entra ID, OpenID Connect, SAML, SPNEGO), se necesita el plugin ``fess-sso-*`` de cada método.
La forma de recibir los grupos y los roles también varía según el método; consulte :doc:`guide-15`.

Ajustar la visibilidad de las etiquetas
=======================================

Las etiquetas también tienen "Permisos", que determinan si la etiqueta aparece entre las opciones de etiqueta de la página de búsqueda.
No afectan a si se muestran o no los documentos, pero como las etiquetas nuevas también contienen ``{role}guest`` desde el principio, tal cual no aparecen en las opciones de los usuarios que han iniciado sesión.

Este es un ejemplo de etiqueta para los documentos de Recursos Humanos.
En [Rastreador] > [Etiqueta], haga clic en [Crear nuevo] e introduzca lo siguiente.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Valor
   * - Nombre
     - ``Recursos Humanos``
   * - Valor
     - ``hr`` (solo caracteres alfanuméricos y guiones bajos)
   * - Rutas incluidas
     - ``https://intra.example.com/hr/.*``
   * - Permisos
     - ``{group}HR`` y ``{group}Executives`` (el mismo ámbito que los documentos)

Los permisos de una etiqueta se reflejan en las opciones en cuanto se guarda.
En cambio, las "Rutas incluidas", que asignan la etiqueta a los documentos, se aplican durante el rastreo, así que ejecute un rastreo después de crear la etiqueta.

Volver a rastrear tras cambiar los derechos
===========================================

Los permisos se registran en los documentos durante el rastreo.
Cambiar los "Permisos" de una configuración de rastreo no cambia los derechos de los documentos que ya están en el índice.
Después del cambio, ejecute un trabajo que incluya esa configuración de rastreo (por ejemplo, "Default Crawler").

En las configuraciones de rastreo web y de sistemas de archivos, los documentos cuyos derechos han cambiado se vuelven a obtener en el siguiente rastreo, y el documento antiguo con la misma URL se sustituye.
Hasta que termina el nuevo rastreo, los documentos siguen apareciendo en los resultados de búsqueda con los derechos antiguos.
Cuando restrinja la visibilidad, ejecute el rastreo de inmediato.

Para volver a rastrear de inmediato solo una configuración de rastreo concreta, haga clic en [Crear nuevo trabajo] en la página de detalles de esa configuración y ejecute el trabajo creado con [Iniciar ahora].

Comprobar el funcionamiento
===========================

Buscar como cada usuario
------------------------

1. Abra ``http://localhost:8080/`` en una ventana privada del navegador. En una ventana con la sesión iniciada en la consola de administración, la búsqueda se realiza como ``admin``
2. Busque sin iniciar sesión y compruebe que no se muestran los documentos de los departamentos ni los de toda la empresa
3. Inicie sesión como ``sato`` desde el enlace de inicio de sesión de la parte superior de la página de búsqueda y compruebe que solo se muestran los documentos de Ventas y los de toda la empresa
4. Haga clic en el nombre de usuario de la parte superior de la página, elija "Cerrar sesión" y compruebe lo mismo con ``suzuki``, ``tanaka`` y ``yamada``

Al comprobarlo, buscar una palabra que aparezca en todos los documentos (por ejemplo, el nombre de la empresa) facilita comparar el alcance de los documentos mostrados.

Ver los derechos registrados en un documento
--------------------------------------------

Si los documentos no se muestran como esperaba, revise los derechos registrados en el documento.

1. En la consola de administración, abra [Información del sistema] > [Búsqueda] y busque palabras de la URL o del título del documento. Esta pantalla no filtra por derechos y muestra todos los documentos
2. Haga clic en [Actualizar] en el documento en cuestión para abrir la pantalla de edición, donde se muestran los derechos registrados en el campo ``role``. Solo consúltelos; no guarde

Los valores del campo ``role`` se muestran en el siguiente formato interno.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Permiso
     - Valor en el campo role
     - Ejemplo
   * - ``{user}nombre_usuario``
     - ``1`` + nombre
     - ``1sato``
   * - ``{group}nombre_grupo``
     - ``2`` + nombre
     - ``2Sales``
   * - ``{role}nombre_rol``
     - ``R`` + nombre
     - ``Rguest``
   * - Con ``(deny)``
     - Prefijo ``D``
     - ``D2Sales``

Si el campo ``role`` de un documento de Ventas contiene ``2Sales`` y ``2Executives``, los permisos se han registrado según la configuración.
Si sigue apareciendo ``Rguest``, o bien no ha vuelto a rastrear después de cambiar los permisos, o bien olvidó borrar el valor inicial ``{role}guest``.

No mostrar nada a quien no ha iniciado sesión
=============================================

Si coloca Fess en una red a la que pueden acceder personas ajenas a la empresa, o si directamente no permite buscar sin iniciar sesión, active "Requiere inicio de sesión" en [Sistema] > [General].
Una vez activado, los visitantes que no han iniciado sesión ya no pueden buscar.

Este ajuste es independiente del control mediante permisos.
Aunque queden documentos con ``{role}guest``, ya no se mostrarán a los visitantes que no han iniciado sesión.
Este ajuste también se guarda en ``system.properties``, por lo que en Docker hay que tener la misma precaución que con los ajustes de LDAP.

Artículos recomendados
======================

- Controlar la visibilidad con las ACL de un servidor de archivos: :doc:`file-server-search`
- Permitir el inicio de sesión por SSO con las cuentas de la empresa: :doc:`guide-15`
- Usar un solo Fess para varias organizaciones: :doc:`guide-13`
- Asignar derechos también a documentos de Slack o del almacenamiento en la nube: :doc:`datastore-basics`
- Buscar en Git, Confluence, Jira y Slack de un equipo de desarrollo: :doc:`guide-06`

Referencias
===========

- `Configuración de Búsqueda Basada en Roles <https://fess.codelibs.org/es/stable/config/security-role.html>`__
- `Búsqueda por roles (para usuarios) <https://fess.codelibs.org/es/stable/user/role-search.html>`__
- `Guía de integración LDAP <https://fess.codelibs.org/es/stable/config/ldap-integration.html>`__
- `Usuario <https://fess.codelibs.org/es/stable/admin/user-guide.html>`__
- `Grupo <https://fess.codelibs.org/es/stable/admin/group-guide.html>`__
- `Etiquetas <https://fess.codelibs.org/es/stable/admin/labeltype-guide.html>`__
- `Búsqueda (consola de administración) <https://fess.codelibs.org/es/stable/admin/searchlist-guide.html>`__
