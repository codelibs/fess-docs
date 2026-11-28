==================================================
Buscar en Git, Confluence, Jira y Slack del equipo
==================================================

Introducción
============

La información de un equipo de desarrollo está repartida entre herramientas: el código y los README en Git, los documentos de diseño en Confluence, las incidencias en Jira y las conversaciones en Slack.
Buscar en las cuatro herramientas una tras otra cada vez que se quiere saber "¿dónde se decidió esa especificación?" resulta tedioso.
Con los plugins de almacén de datos de Fess, puede buscar la información de las cuatro herramientas desde una sola página de búsqueda.

Sin embargo, si la configuración es incorrecta, se producen situaciones como estas:

- Todos los archivos de Git se registran con la URL vacía, por lo que no se puede abrir el archivo original desde los resultados de búsqueda
- Todos los mensajes de Slack se muestran sin título
- Los mensajes de los canales privados aparecen también en los resultados de búsqueda de los usuarios que no han iniciado sesión
- Los archivos de Git desaparecen del índice al cabo de unos días

Para cada herramienta, este artículo muestra una configuración mínima que funciona tal cual, y explica cómo cada ajuste evita los problemas anteriores.
Los pasos comunes a todos los almacenes de datos, como la instalación de plugins, la forma de escribir el nombre del manejador, los parámetros y el script, o la creación de trabajos, se recogen en :doc:`datastore-basics`.
Léalo antes de continuar.
Los valores de configuración de este artículo corresponden a Fess 15.9 y a la versión 15.9.0 de cada plugin.

Lo que vamos a construir
========================

.. list-table::
   :header-rows: 1
   :widths: 14 20 26 40

   * - Herramienta
     - Plugin
     - Nombre del manejador
     - Qué preparar en la herramienta
   * - Git
     - ``fess-ds-git``
     - ``GitDataStore``
     - Un token de acceso con permiso de lectura (debe poder clonarse por HTTPS)
   * - Confluence / Jira
     - ``fess-ds-atlassian``
     - ``ConfluenceDataStore`` / ``JiraDataStore``
     - Un token de API de la cuenta de rastreo
   * - Slack
     - ``fess-ds-slack``
     - ``SlackDataStore``
     - El Bot User OAuth Token (``xoxb-``) de una aplicación de Slack

Si ejecuta Fess con Docker, puede instalar todos los plugins de una vez al arrancar enumerando sus nombres y versiones, separados por espacios, en la variable de entorno ``FESS_PLUGINS``.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-git:15.9.0 fess-ds-atlassian:15.9.0 fess-ds-slack:15.9.0

Si los instala desde la consola de administración o con ``fess-setup``, reinicie Fess después de la instalación.

Primero decida: quién puede ver los resultados
==============================================

Al crear una nueva configuración de almacén de datos, el campo "Permisos" ya contiene ``{role}guest``.
Si lo deja así, la información importada podrá ser encontrada también por usuarios que no han iniciado sesión.

Los plugins de Git, Confluence y Jira no trasladan a Fess los permisos de acceso de la herramienta de origen.
Se importa todo lo que puede leer la cuenta de rastreo, y queda visible para quien tenga un rol o grupo escrito en el campo "Permisos".
Por eso, el alcance se decide combinando estos dos puntos:

- Sustituir ``{role}guest`` del campo "Permisos" por las personas que deben ver el contenido (p. ej., ``{group}developers``)
- Limitar lo que se importa a lo que esas personas pueden ver, mediante los permisos de la cuenta de rastreo y los parámetros ``jira.jql`` e ``include_pattern`` que se explican más adelante

Solo el plugin de Slack puede importar los miembros de los canales privados como permisos (se explica más adelante).
Para saber cómo funcionan los grupos y los roles, consulte :doc:`guide-05`.

Repositorios Git
================

Preparación
-----------

``fess-ds-git`` clona por HTTPS.
No admite URI SSH (con la forma ``git@...``).
Para los repositorios privados, cree un token de acceso de lectura.
En un token clásico de GitHub es el ámbito ``repo``; en GitLab, el ámbito ``read_repository``.

Parámetros y script
-------------------

En [Rastreador] > [Almacén de datos] > [Crear nuevo], seleccione ``GitDataStore`` como "Nombre del manejador".

.. code-block:: properties

    script_type=javascript
    uri=https://github.com/example/dev-platform.git
    username=fess-crawler
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    base_url=https://github.com/example/dev-platform/blob/main/
    include_pattern=.*\.(md|rst|txt|java|py|ts|yml|yaml)$
    time_to_live=5256000

.. code-block:: properties

    url=url
    title=path
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp
    label="code"

El significado de cada línea es el siguiente:

- ``base_url``: la ``url`` del script es ``base_url`` concatenada tal cual con la ruta dentro del repositorio. Si la omite, ``url`` queda como cadena vacía; todos los archivos reciben entonces el mismo ID de documento y se sobrescriben entre sí. Termínela en ``/`` y haga coincidir el nombre de rama con la rama que se rastrea (por defecto, la rama predeterminada del remoto; para cambiarla, use ``commit_id``).
- ``username`` / ``password``: solo se usan para la autenticación cuando se indican ambos. No incruste el token en ``uri``; escríbalo en ``password`` (``password`` se cifra al guardarse, ``uri`` no).
- ``include_pattern``: una expresión regular que debe coincidir con la ruta completa dentro del repositorio (p. ej., ``docs/setup.md``). No es una URL.
- ``title=path``: con ``name``, que solo contiene el nombre del archivo, los archivos homónimos como ``README.md`` no se distinguen en los resultados de búsqueda; por eso se usa la ruta.

Rastreo diferencial y caducidad
-------------------------------

Cuando un rastreo termina correctamente, ``fess-ds-git`` escribe su ID de commit en ``prev_commit_id`` del campo "Parámetro".
A partir del segundo rastreo, solo registra los archivos incluidos en el diff con el commit anterior, y elimina los documentos de los archivos borrados o renombrados (para reflejar las eliminaciones se necesita ``base_url``).

Este rastreo diferencial no se lleva bien con la caducidad de los documentos de Fess; por eso el ejemplo anterior especifica ``time_to_live``.
Los documentos de un almacén de datos reciben una fecha de caducidad al registrarse.
Por defecto, la determina "Eliminar documentos anteriores" en [Sistema] > [General] (3 días por defecto), y el trabajo "Doc Purger", que se ejecuta cada minuto, elimina los documentos caducados.
En el rastreo diferencial, los archivos sin cambios no se vuelven a registrar, de modo que su caducidad no se prolonga y desaparecen unos días después del primer rastreo.
``time_to_live`` es un parámetro que indica en minutos la caducidad de los documentos de esta configuración; ``5256000`` equivale a unos 10 años.

Por la misma razón, los cambios en el script, ``base_url``, ``include_pattern`` o el campo "Permisos" no se aplican a los archivos sin cambios.
Para volver a registrar todos los archivos, siga estos pasos:

1. En [Información del sistema] > [Búsqueda], busque ``label:code`` y elimine los documentos antiguos con [Eliminar todo con esta consulta]
2. Borre el valor de ``prev_commit_id=`` en el campo "Parámetro" y guarde
3. Ejecute el trabajo

Si cambió el campo "Permisos" o ``base_url``, los ID de documento cambian, así que si omite el paso 1 quedarán documentos antiguos.
Cuando elimine esta configuración de almacén de datos, borre también antes sus documentos con el paso 1.

Confluence
==========

En Atlassian Cloud, cree un token de API con la cuenta de rastreo y úselo como contraseña de la autenticación Basic.
Se importan las páginas y las entradas de blog de los espacios que esta cuenta puede ver.
Seleccione ``ConfluenceDataStore`` como "Nombre del manejador".

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    include_pattern=https://example\.atlassian\.net/wiki/spaces/(DEV|OPS)/.*

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body + content.comments
    last_modified=content.last_modified
    label="docs"

- ``home`` funciona con o sin ``/wiki``. En Cloud, se añade ``/wiki`` para Confluence.
- Si se omite ``deployment``, se considera ``cloud`` cuando el nombre de host termina en ``.atlassian.net``, y ``datacenter`` en los demás casos.
- Al añadir ``content.comments``, los comentarios de la página también se pueden buscar como parte del cuerpo. Los comentarios se concatenan separados por líneas en blanco.
- ``include_pattern`` se compara con la URL completa del documento. En Cloud, las URL de las páginas tienen la forma ``https://<sitio>/wiki/spaces/<clave-de-espacio>/pages/<id-de-página>``, por lo que puede filtrar por clave de espacio. Las URL de Data Center (``/pages/viewpage.action?pageId=...``) no contienen la clave de espacio, así que este método no sirve allí.

En Data Center, indique ``deployment=datacenter``; para usar un token de acceso personal, especifique ``auth_type=pat`` y ``pat.token``.

Jira
====

La autenticación es la misma que en Confluence.
Seleccione ``JiraDataStore`` como "Nombre del manejador" y limite con JQL las incidencias que se importan.

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    jira.jql=project in (DEV, OPS)

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description + issue.comments
    last_modified=issue.last_modified
    label="tickets"

El parámetro de JQL se llama ``jira.jql``.
El nombre antiguo ``issue.jql`` todavía funciona, pero el registro muestra la advertencia ``Parameter "issue.jql" is deprecated``.
Está previsto eliminar el nombre antiguo en la versión 16.0.
Si se omite ``jira.jql``, se usa ``created is not empty``, es decir, todas las incidencias que la cuenta puede ver.

Al añadir ``issue.comments``, los comentarios de la incidencia también se incorporan al cuerpo, separados por líneas en blanco, y se pueden buscar.
Los comentarios se obtienen por la API para cada incidencia, lo que aumenta el número de llamadas (consulte los límites de velocidad más adelante).

Slack
=====

Preparar la aplicación de Slack
-------------------------------

Cree una aplicación en https://api.slack.com/apps y añada los siguientes ámbitos en Bot Token Scopes, dentro de [OAuth & Permissions]; después, instálela en el espacio de trabajo.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Ámbito
     - Cuándo se necesita
   * - ``channels:read``, ``channels:history``, ``users:read``, ``team:read``
     - Siempre
   * - ``groups:read``, ``groups:history``
     - Para importar canales privados (``include_private=true``)
   * - ``users:read.email``
     - Para usar los miembros de los canales privados como permisos (``permission_sync=true``)
   * - ``files:read``
     - Para importar también archivos (``file_crawl=true``)

Sin ``team:read``, el plugin llama a ``chat.getPermalink`` por cada mensaje, lo que aumenta mucho el número de llamadas a la API.
Después de la instalación, añada la aplicación a cada canal que quiera importar.
Los canales en los que la aplicación no participa se omiten con una advertencia.

Cree dos configuraciones de almacén de datos separadas: una para los canales públicos y otra para los privados.
El motivo se explica en la sección "Canales privados".

Canales públicos
----------------

Seleccione ``SlackDataStore`` como "Nombre del manejador" e indique en el campo "Permisos" las personas que deben ver los canales públicos.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=*all
    include_private=false

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    label="slack"

``message.title`` es siempre una cadena vacía en los mensajes, así que si escribe ``title=message.title``, ningún resultado tendrá título.
Como en el ejemplo anterior, construya el título a partir del autor y del nombre del canal.
Las respuestas de los hilos también se registran como documentos individuales.
Los mensajes del sistema como ``channel_join`` se excluyen por defecto (``ignore_system_events=true``).

Canales privados
----------------

Con ``permission_sync=true``, el plugin crea, a partir de las direcciones de correo electrónico de los miembros de un canal privado, un rol de usuario por miembro y los guarda en ``message.roles``.
No obstante, a este valor también se añaden los valores de ``default_permissions`` y del campo "Permisos".
Los canales públicos no tienen roles propios, así que si ambos están vacíos, los documentos de los canales públicos no los ve nadie.
A la inversa, si escribe en cualquiera de los dos el público de los canales públicos, ese público verá también los documentos de los canales privados.
Como una sola configuración no puede tratar bien ambos casos, los canales privados van en una configuración aparte.

En la segunda configuración de almacén de datos, borre ``{role}guest`` del campo "Permisos" para dejarlo vacío, y enumere en ``channels`` los nombres de los canales privados que quiera importar.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=dev-security,dev-incident
    include_private=true
    permission_sync=true

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    role=message.roles
    label="slack"

- Si no escribe ``role=message.roles``, los roles calculados no se usan. En ese caso, al iniciar el rastreo aparece la advertencia ``no script value references message.roles``.
- Si mezcla canales públicos en ``channels``, sus documentos tendrán los roles vacíos y no los verá nadie.
- Con esta configuración, al iniciar el rastreo aparece la advertencia ``default_permissions is not set and this crawl's DataConfig permission field is empty``. Mientras no incluya canales públicos, no supone ningún problema.
- Los canales cuyos miembros no se pudieron obtener, o para los que no se pudo resolver ni una sola dirección de correo electrónico (por ejemplo, por haber olvidado ``users:read.email``), no se importan en ese rastreo. Se registran en [Información del sistema] > [URL de fallo] con el ID y el nombre del canal.

Al buscar, el nombre del usuario que ha iniciado sesión en Fess se compara con estas direcciones de correo electrónico.
Por lo tanto, el nombre de usuario de Fess debe coincidir con la dirección de correo electrónico de Slack.
Slack trata las direcciones de correo electrónico en minúsculas, así que los nombres de usuario de Fess también deben estar en minúsculas.
Los usuarios que no coinciden simplemente no ven los documentos de los canales privados; nunca ven los documentos de otras personas.
Para saber qué valor se convierte en el nombre de usuario al iniciar sesión con SSO, consulte :doc:`guide-15`.

Si ya había importado canales privados sin ``permission_sync``, esos documentos permanecen sin permisos hasta que caduquen.
Elimine esos documentos en [Información del sistema] > [Búsqueda] antes de rastrear con esta configuración.

Etiquetas, valor de impulso y programación
==========================================

Las etiquetas se asignan con la línea ``label="..."`` de cada uno de los scripts anteriores.
Para mostrarlas como filtros en la página de búsqueda, cree en [Rastreador] > [Etiqueta] etiquetas con los mismos valores (``code``, ``docs``, ``tickets``, ``slack``).
Tenga en cuenta que, si existe una etiqueta cuyas "Rutas incluidas" coinciden con la URL del documento, la etiqueta del script se pierde (:doc:`datastore-basics`).

Las reglas de [Rastreador] > [Impulso de documento] no se aplican a los documentos de los almacenes de datos.
Si quiere que los documentos de diseño de Confluence aparezcan por encima de los mensajes de Slack, aumente el "Valor de impulso" (valor inicial ``1.0``) de la configuración de almacén de datos de Confluence.
El valor se multiplica por la puntuación de búsqueda, así que cámbielo poco a poco y compare los resultados.

Para rastrear cada herramienta con una frecuencia distinta, use [Crear nuevo trabajo] en la página de detalles de cada configuración de almacén de datos (:doc:`datastore-basics`).

Límites de velocidad de las API
===============================

Los plugins de Slack y Atlassian reintentan automáticamente la solicitud ante respuestas ``429`` y ``5xx`` y, si hay una cabecera ``Retry-After``, esperan los segundos que indica (como máximo 60 segundos en Slack).

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Plugin
     - Parámetros ajustables
   * - Slack
     - ``read_interval`` (espera por mensaje, en milisegundos, por defecto ``0``), ``max_retry_count`` (por defecto ``3``), ``retry_interval`` (espera hasta el primer reintento, en milisegundos, por defecto ``3000``; se duplica en cada reintento, con un máximo de 60 segundos)
   * - Atlassian
     - ``read_interval`` (intervalo mínimo entre llamadas a la API, en milisegundos, por defecto ``0``; compartido entre hilos). El número de reintentos y su intervalo son fijos

Cuando Slack agota los reintentos, el rastreo se interrumpe.
El estado del registro de trabajos sigue siendo "OK", así que compruébelo con los pasos de la sección siguiente.

Comprobar el funcionamiento
===========================

Cómo consultar los resultados de los trabajos y los registros se explica en :doc:`datastore-basics`.
Un rastreo de almacén de datos puede fallar aunque el trabajo se muestre como "OK", así que juzgue por el número de documentos y los registros.
Con la configuración de este artículo, compruebe además lo siguiente:

1. En [Información del sistema] > [Búsqueda], busque ``label:code``, ``label:docs``, ``label:tickets`` y ``label:slack`` uno por uno, y confirme que el número no es 0
2. Abra la URL de un documento de Git y confirme que se muestra el archivo del repositorio. Si ``fess-crawler.log`` contiene la advertencia ``base_url is blank``, revise ``base_url``
3. Abra la página de detalles de la configuración de Git y confirme que ``prev_commit_id`` se ha escrito en los parámetros
4. Sin haber iniciado sesión, busque una palabra que solo aparezca en un canal privado y confirme que no se encuentra ningún resultado
5. Inicie sesión como miembro de ese canal y confirme que la misma palabra sí se encuentra

Si en el paso 5 no se encuentra, compruebe si el nombre de usuario de Fess coincide con la dirección de correo electrónico de Slack y si ``fess-crawler.log`` contiene la advertencia ``private channel(s) skipped``.
Si falla una configuración completa, por ejemplo por un error de autenticación, se registra por configuración en [Información del sistema] > [URL de fallo].

Resumen
=======

- En Git, especifique siempre ``base_url`` y añada ``time_to_live`` para que los documentos no caduquen con el rastreo diferencial.
- En Confluence y Jira, importe también los comentarios con ``content.comments`` / ``issue.comments``, y escriba el JQL en ``jira.jql``.
- En Slack, construya el título a partir de ``message.user`` y ``message.channel``.
- Git, Confluence y Jira no trasladan los permisos originales, así que decida el alcance con el campo "Permisos" y el ámbito de importación.
- Coloque los canales privados de Slack en una configuración aparte e impórtelos con ``permission_sync=true``, ``role=message.roles`` y el campo "Permisos" vacío.
- Ajuste la prioridad de cada fuente de información con el "Valor de impulso" de su configuración de almacén de datos.

Referencias
===========

- `Conector Git <https://fess.codelibs.org/es/stable/config/datastore/ds-git.html>`__
- `Conector de Atlassian <https://fess.codelibs.org/es/stable/config/datastore/ds-atlassian.html>`__
- `Conector de Slack <https://fess.codelibs.org/es/stable/config/datastore/ds-slack.html>`__
- `Rastreo de Almacén de Datos <https://fess.codelibs.org/es/stable/admin/dataconfig-guide.html>`__
- `General <https://fess.codelibs.org/es/stable/admin/general-guide.html>`__
- `README de fess-ds-slack 15.9.0 (ámbitos y sincronización de permisos) <https://github.com/codelibs/fess-ds-slack/blob/fess-ds-slack-15.9.0/README.md>`__
