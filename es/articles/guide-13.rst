=======================================
Un solo Fess para varias organizaciones
=======================================

Introducción
============

Si quiere ofrecer un servicio de búsqueda a cada empresa de un grupo o a cada departamento y construye un Fess por organización, los servidores y las configuraciones de rastreo que debe administrar se multiplican por el número de organizaciones.
Con la función de hosts virtuales de Fess, puede publicar un único Fess con varios nombres de host y cambiar, según el nombre de host, los destinos de búsqueda, las etiquetas y la página de búsqueda.

Sin embargo, un host virtual solo cambia lo que se muestra según el nombre de host por el que llegó la solicitud; no es un control de acceso.
Para garantizar que los documentos de una organización no sean visibles para otra, hay que combinarlo con permisos basados en roles y con el inicio de sesión.

En este artículo, tomamos como ejemplo dos inquilinos, la Empresa A y la Empresa B, y configuramos paso a paso lo siguiente en Fess 15.9.

- Asociar los nombres de host con los inquilinos en "Host virtual" de [General]
- Indicar el host virtual y los permisos en las configuraciones de rastreo y en las etiquetas para separar los documentos de cada inquilino
- Dar a cada inquilino su propia página de búsqueda con un tema que se llame igual que la clave del host virtual
- Iniciar sesión con un usuario de un inquilino y comprobar que no se ven los documentos de los demás inquilinos
- Añadir y eliminar inquilinos en el orden correcto

Los fundamentos de roles, grupos y usuarios se tratan en :doc:`guide-05`.

Lo primero: un host virtual no es un control de acceso
======================================================

En cada solicitud, Fess evalúa de arriba abajo las líneas escritas en "Host virtual" de [General] y usa el nombre de host virtual (en adelante, la clave) de la primera línea cuyo encabezado indicado (normalmente ``Host``) coincida.
Una vez determinada la clave, las siguientes funciones se filtran por esa clave.

- Resultados de búsqueda: solo se devuelven los documentos cuya configuración de rastreo tiene esa clave en "Hosts virtuales" (lo mismo ocurre con la API de búsqueda)
- Etiquetas: solo se muestran las etiquetas cuyo campo "Host virtual" es esa clave
- Coincidencia de clave, Contenido relacionado y Consulta relacionada: solo se usan los ajustes cuyo campo "Host virtual" es esa clave
- Página de búsqueda: si existe un tema cuyo nombre es la clave en minúsculas, la página se muestra con ese tema

En cambio, en una solicitud que no coincide con ninguna línea, no se aplica ninguno de estos filtros.
Si alguien accede directamente al servidor por su dirección IP, o si un proxy inverso reescribe el encabezado ``Host``, desaparece el filtrado por host virtual y los documentos de todos los inquilinos que permitan los permisos pasan a ser buscables.
Un nombre de host mal escrito o un número de puerto olvidado en [General] tampoco produce un error: simplemente se trata como "sin coincidencia".

Por eso, para que los documentos no sean visibles entre inquilinos, combine las dos medidas siguientes.

- Limitar los permisos de los documentos de cada inquilino al rol de ese inquilino (por ejemplo, ``{role}tenanta_user``)
- Exigir el inicio de sesión en la página de búsqueda y asignar a los usuarios el rol de su inquilino

La configuración de este artículo
=================================

.. list-table::
   :header-rows: 1
   :widths: 16 26 14 18 26

   * - Inquilino
     - Nombre de host público
     - Clave
     - Rol
     - Destino del rastreo
   * - Empresa A
     - ``search-a.example.com``
     - ``tenanta``
     - ``tenanta_user``
     - ``https://portal-a.example.com/``
   * - Empresa B
     - ``search-b.example.com``
     - ``tenantb``
     - ``tenantb_user``
     - ``https://portal-b.example.com/``

En una clave solo se pueden usar caracteres alfanuméricos y guiones bajos (``a-zA-Z0-9_``).
Los demás caracteres se eliminan al guardar, así que si escribe ``tenant-a``, la clave pasa a ser ``tenanta``, y un ``tenant-a`` escrito en una configuración de rastreo no coincidirá.
``admin``, ``common``, ``error``, ``login`` y ``profile`` están reservados y no se pueden usar.

Los campos "Hosts virtuales" de las configuraciones de rastreo y "Host virtual" de las etiquetas son de texto libre, y la comparación con la clave distingue entre mayúsculas y minúsculas.
Los nombres de tema tampoco admiten mayúsculas, así que usar desde el principio claves alfanuméricas en minúsculas evita errores.

Paso 1: asociar los nombres de host con las claves
==================================================

En la consola de administración, abra [Sistema] > [General], escriba en "Host virtual" una entrada ``nombre-encabezado:valor=clave`` por línea y actualice.

::

    Host:search-a.example.com=tenanta
    Host:search-b.example.com=tenantb

El valor del encabezado se compara por coincidencia exacta, sin distinguir entre mayúsculas y minúsculas.
Cuando un navegador accede a un puerto distinto de los estándar (80 y 443), añade el número de puerto al encabezado ``Host``; por eso, si los usuarios acceden directamente al puerto 8080 de Fess, incluya también el puerto como se muestra a continuación.
También puede escribir ambas formas una tras otra.

::

    Host:search-a.example.com:8080=tenanta
    Host:search-b.example.com:8080=tenantb

El ajuste se aplica en cuanto se guarda; no es necesario reiniciar.
También puede escribirlo con el mismo formato en ``virtual.host.headers`` de ``fess_config.properties``, pero si [General] tiene un valor, este tiene prioridad.

Si coloca Fess detrás de un proxy inverso, haga llegar hasta Fess el encabezado ``Host`` que envía el navegador.
De forma predeterminada, Nginx establece ``Host`` en el destino de ``proxy_pass``, por lo que se necesita ``proxy_set_header Host $host;``.

::

    server {
        server_name search-a.example.com search-b.example.com;
        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
        }
    }

En una configuración que reescribe ``Host``, también puede indicar ``X-Forwarded-Host`` como nombre del encabezado (por ejemplo, ``X-Forwarded-Host:search-a.example.com=tenanta``).

.. warning::

   Los ajustes de [General] se guardan en ``system.properties`` dentro del contenedor.
   ``fess01`` de docker-fess no tiene volumen, así que si vuelve a crear el contenedor con ``docker compose down``, también se pierde el valor de "Host virtual" (con ``stop`` y ``start`` se conserva).
   El tema que subirá en un paso posterior también se guarda dentro del contenedor, por lo que se pierde de la misma manera.
   Para saber cómo conservar los ajustes, consulte `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__.

Paso 2: crear los roles y los usuarios de los inquilinos
========================================================

1. En [Usuario] > [Rol], cree los roles llamados ``tenanta_user`` y ``tenantb_user``.
2. En [Usuario] > [Usuario], cree los usuarios de cada inquilino y seleccione en "Roles" el rol de su inquilino.
3. En [Sistema] > [General], active "Requiere inicio de sesión".

Los usuarios que han iniciado sesión no reciben ``{role}guest`` y buscan solo con los permisos de su usuario, sus grupos y sus roles.
Si quiere usar directamente los grupos de LDAP o SSO, puede indicar ``{group}<nombre del grupo>`` en lugar de un rol.
Para el funcionamiento de los permisos y la integración con LDAP, consulte :doc:`guide-05`; para el SSO, consulte :doc:`guide-15`.

Paso 3: crear una etiqueta para cada inquilino
==============================================

Una etiqueta se asigna, durante el rastreo, a los documentos cuya URL coincide con "Rutas incluidas".
Créela antes de rastrear.

En [Rastreador] > [Etiqueta], pulse [Crear nuevo] e introduzca lo siguiente para la Empresa A (cree la de la Empresa B de la misma manera).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Valor
   * - Nombre
     - ``Portal Empresa A``
   * - Valor
     - ``tenanta_docs`` (solo caracteres alfanuméricos y guiones bajos)
   * - Rutas incluidas
     - ``https://portal-a\.example\.com/.*``
   * - Permisos
     - ``{role}tenanta_user``
   * - Host virtual
     - ``tenanta``

Los permisos de una etiqueta nueva contienen ``{role}guest``.
Una etiqueta solo se muestra cuando el usuario tiene un rol incluido en sus permisos, así que si deja ``{role}guest``, la etiqueta no se muestra a los usuarios del inquilino que han iniciado sesión.

Una etiqueta cuyo "Host virtual" está vacío no se muestra cuando se accede a través de un host virtual.
Una etiqueta solo admite un host virtual, así que si quiere que varios inquilinos vean la misma etiqueta, cree tantas etiquetas con el mismo nombre y valor como inquilinos haya y escriba en el "Host virtual" de cada una la clave correspondiente.
Lo mismo ocurre con Coincidencia de clave, Contenido relacionado y Consulta relacionada: los ajustes cuyo "Host virtual" está vacío no se usan en los hosts de los inquilinos.

Paso 4: indicar el host virtual y los permisos en la configuración de rastreo
=============================================================================

En [Rastreador] > [Web], cree la configuración de rastreo de la Empresa A.
Las configuraciones de rastreo de sistemas de archivos y de almacenes de datos tienen los mismos dos campos.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Valor
   * - Nombre
     - ``Portal Empresa A``
   * - URLs
     - ``https://portal-a.example.com/``
   * - URLs a incluir en el rastreo
     - ``https://portal-a.example.com/.*``
   * - Permisos
     - ``{role}tenanta_user`` (elimine el ``{role}guest`` que aparece de forma predeterminada)
   * - Hosts virtuales
     - ``tenanta``

Si deja ``{role}guest``, esos documentos quedan visibles al acceder por la dirección IP o antes de iniciar sesión.

Para documentos que deben ver varios inquilinos, como un compendio de normas de todo el grupo, escriba en una sola configuración de rastreo una línea por inquilino, para ambos inquilinos, en "Hosts virtuales" y en "Permisos".

::

    Hosts virtuales:
    tenanta
    tenantb

    Permisos:
    {role}tenanta_user
    {role}tenantb_user

Los hosts virtuales y los permisos se escriben en los documentos durante el rastreo.
Si los cambia en una configuración que ya se ha rastreado, los documentos existentes no reflejan el cambio hasta que se vuelvan a rastrear.

Después de guardar la configuración, cree un trabajo exclusivo para el inquilino con [Crear nuevo trabajo] en la pantalla de detalles, o ejecute ``Default Crawler`` con [Iniciar ahora] en [Sistema] > [Programador].

Paso 5: preparar una página de búsqueda propia para cada inquilino
==================================================================

En Fess 15.9, la página de búsqueda se muestra mediante un tema.
Si instala un tema cuyo ``name`` en ``theme.yml`` es igual a la clave en minúsculas, ese tema se usa para las solicitudes con esa clave.
No es necesario establecerlo como tema predeterminado; las solicitudes que no coinciden con ninguna clave usan el tema predeterminado.

Créelo copiando el tema ``bootstrap`` incluido.
Con Docker, extráigalo del contenedor de la siguiente manera.

::

    $ docker cp fess01:/usr/share/fess/app/themes/bootstrap ./tenanta

1. En ``tenanta/theme.yml``, cambie ``name`` a ``tenanta`` y ``displayName`` a algo como ``Búsqueda Empresa A``.
2. Sustituya ``assets/styles.css`` (colores) y ``assets/logo-head.png`` y ``assets/logo.png`` (logotipos). No es necesario modificar ``index.html``.
3. Empaquételo de modo que ``theme.yml`` quede en la raíz del ZIP.

   ::

       $ cd tenanta && zip -r ../tenanta.zip .

4. Suba ``tenanta.zip`` con [Subir] en [Sistema] > [Tema].

La página de inicio de sesión (``/login/``) es común a todos los inquilinos y no se puede cambiar con un tema.
Para más detalles sobre cómo copiar el tema incluido, consulte la `Guía de Desarrollo de Temas <https://fess.codelibs.org/es/stable/dev/theme-development.html>`__.

Comprobar la separación
=======================

Antes de cambiar el DNS, puede añadir ``127.0.0.1 search-a.example.com search-b.example.com`` al archivo ``/etc/hosts`` de su equipo y probar cada host desde un navegador, por ejemplo ``http://search-a.example.com:8080/`` ([General] necesita entonces las líneas con el puerto).
Compruebe los cuatro casos siguientes buscando una palabra que aparezca en los destinos del rastreo.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Acceso
     - Resultado esperado
   * - Usuario de la Empresa A desde ``search-a.example.com``
     - Solo aparecen documentos de la Empresa A. La única etiqueta es "Portal Empresa A". La página se muestra con el tema de la Empresa A
   * - Usuario de la Empresa A desde ``search-b.example.com``
     - 0 resultados (no tiene permiso sobre los documentos de la Empresa B, y los de la Empresa A quedan excluidos por el host virtual)
   * - Usuario de la Empresa A desde la dirección IP (``http://<servidor>:8080/``)
     - Solo aparecen documentos de la Empresa A (no hay filtrado por host virtual, pero los permisos los protegen)
   * - Acceso sin iniciar sesión
     - No se puede buscar hasta iniciar sesión

Si creó documentos comunes para ambos inquilinos, también aparecen en las filas 1 a 3.
Si en la fila 3 aparecen documentos de la Empresa B, queda un ``{role}guest`` en alguna configuración de rastreo.
Si la fila 1 da 0 resultados, compare las líneas de [General] (con o sin número de puerto) con la ortografía de "Hosts virtuales" en la configuración de rastreo.

La misma comprobación se puede hacer con la API de búsqueda.
En [Sistema] > [Token de acceso], cree un token con el permiso ``{role}tenanta_user`` y llame a la API cambiando el encabezado ``Host``.

::

    $ curl -s -H "Authorization: Bearer <token de la Empresa A>" \
        -H "Host: search-a.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"
    $ curl -s -H "Authorization: Bearer <token de la Empresa A>" \
        -H "Host: search-b.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"

El resultado es el esperado si ``response.record_count`` es 1 o más en la primera llamada y 0 en la segunda.
Un token de acceso no está vinculado a un host virtual: el host virtual se determina por el nombre de host al que se envía la solicitud.
Lo que un token puede ver lo determinan sus permisos, así que asigne siempre a los tokens que entregue a los sistemas de un inquilino solo el rol de ese inquilino.
Para el uso de la API, consulte :doc:`guide-11`.

Una vez en producción, puede consultar el número de búsquedas por host virtual en la pestaña [Audiencia] de [Información del sistema] > [Registro de búsqueda].

Añadir y eliminar inquilinos
============================

Para añadir un inquilino, siga este orden, ya que los pasos posteriores usan valores de los anteriores.

1. Añadir una línea en "Host virtual" de [General]
2. Crear el rol, los usuarios y, si es necesario, los tokens de acceso
3. Crear las etiquetas (con host virtual y permisos)
4. Crear las configuraciones de rastreo (con host virtual y permisos) y rastrear
5. Subir el tema
6. Comprobar los cuatro casos de "Comprobar la separación"
7. Publicarlo mediante el DNS y el proxy inverso

Para eliminar un inquilino, a la inversa, empiece por cerrar los puntos de entrada.

1. Quitar el nombre de host del DNS y del proxy inverso
2. Eliminar las configuraciones de rastreo y los trabajos creados para ellas ([Sistema] > [Programador])
3. Eliminar los documentos del índice (ver más abajo)
4. Eliminar los tokens de acceso, los usuarios y el rol
5. Eliminar las etiquetas, las coincidencias de clave y demás ajustes de esa clave, y el tema
6. Eliminar la línea de "Host virtual" en [General]

Eliminar una configuración de rastreo no elimina del índice los documentos ya rastreados.
Elimine los documentos en [Información del sistema] > [Búsqueda].
Esta pantalla no aplica el filtrado por roles ni por host virtual, así que abarca los documentos de todos los inquilinos.
Busque en el cuadro de búsqueda con la etiqueta del inquilino, por ejemplo ``label:tenantb_docs``, compruebe que el número y los resultados corresponden solo a documentos de la Empresa B y, después, pulse [Eliminar todo con esta consulta].
En el caso de documentos web, también puede indicar el principio de la URL, por ejemplo ``site:portal-b.example.com``.

No use una consulta como ``virtual_host:tenantb``.
De forma predeterminada, ``virtual_host`` no está entre los campos disponibles para la búsqueda, así que toda la cadena se trata como una búsqueda de ese texto en el cuerpo de los documentos y no permite seleccionar los documentos deseados.

La opción de separar instancias
===============================

En una configuración en la que se comparte un solo Fess, no se pueden separar los siguientes elementos.

- La consola de administración y los administradores: cualquier administrador puede operar sobre los ajustes, usuarios y documentos de todos los inquilinos
- Los ajustes de todo el sistema, como los de [General] y los diccionarios
- La página de inicio de sesión

Si quiere delegar la administración en cada inquilino, o si un contrato exige índices separados, ejecute un Fess por inquilino y use nombres de índice distintos.
``compose/multi-instance`` de docker-fess conecta dos Fess (puertos 8080 y 8081) a un mismo OpenSearch.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess
    $ git checkout v15.9.0
    $ cd compose/multi-instance
    $ docker compose -f compose.yaml -f compose-fess01.yaml -f compose-fess02.yaml up -d

En el ``FESS_JAVA_OPTS`` de cada Fess, los nombres de índice de documentos, sugerencias, rastreo, configuración, usuarios, registros y diccionarios (8 elementos, como ``-Dfess.config.index.document.search.index=fess01.search``) son distintos en cada instancia.
Como la configuración y los usuarios también se separan por índice, la consola de administración, los usuarios y los registros de búsqueda también son por inquilino.
Para añadir un inquilino, copie ``compose-fess02.yaml`` y cambie el nombre del servicio, el puerto y todos los nombres de índice.

.. warning::

   En esta configuración, OpenSearch expone el puerto 9200 con el plugin de seguridad desactivado.
   Cualquiera que llegue al puerto 9200 puede leer los índices de todos los inquilinos, así que cierre el puerto en producción.

Siguientes lecturas
===================

- Profundizar en el diseño de permisos con roles, grupos y LDAP: :doc:`guide-05`
- Llamar a la API de búsqueda desde los sistemas de un inquilino: :doc:`guide-11`
- Iniciar sesión con SSO y proteger el acceso: :doc:`guide-15`
- Ampliar Fess y OpenSearch a medida que crecen los inquilinos: :doc:`guide-14`
- Integrar la página de búsqueda en un sitio existente: :doc:`guide-03`

Referencias
===========

- `Host Virtual <https://fess.codelibs.org/es/stable/config/security-virtual-host.html>`__
- `Configuración de multitenencia <https://fess.codelibs.org/es/stable/config/multitenancy.html>`__
- `Configuración de Búsqueda Basada en Roles <https://fess.codelibs.org/es/stable/config/security-role.html>`__
- `Etiquetas <https://fess.codelibs.org/es/stable/admin/labeltype-guide.html>`__
- `Tema <https://fess.codelibs.org/es/stable/admin/theme-guide.html>`__
- `Búsqueda <https://fess.codelibs.org/es/stable/admin/searchlist-guide.html>`__
- `docker-fess multi-instance (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose/multi-instance>`__
