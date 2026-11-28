================================================
Operar Fess: supervisión, respaldo e incidencias
================================================

Introducción
============

Una vez que Fess está disponible para toda la organización, los responsables de operarlo suelen encontrarse con situaciones como estas:
se enteran de que la búsqueda ha dejado de funcionar solo cuando los usuarios empiezan a preguntar, no se dan cuenta durante días de que el rastreo nocturno está fallando, o al reconstruir un servidor descubren que la configuración no se ha recuperado.

En este artículo se explica cómo prepararse para estas situaciones con los mecanismos que incorpora Fess 15.9.

- Comprobar el estado de Fess y de OpenSearch desde una herramienta de supervisión externa con ``/api/v2/health`` y ``/api/admin/stats``
- Recibir por correo electrónico, Slack o Google Chat avisos del fin de los rastreos, de los cambios de estado de OpenSearch y de los registros de errores
- Saber qué contiene cada archivo de registro y dónde se encuentra
- Obtener copias de seguridad de la configuración con cron y restaurarlas en otro servidor
- Saber qué pantallas y qué registros de Fess revisar cuando se produce una incidencia

La gestión de la configuración como código se trata en :doc:`guide-16`, y la ampliación ante el aumento de documentos y usuarios (incluido el ajuste del heap) en :doc:`guide-14`.
Los comandos de ejemplo suponen el entorno Docker de :doc:`guide-02` (``fess01`` y ``search01``).
Las diferencias de la versión ZIP y de los paquetes RPM/DEB se indican en cada caso.

Supervisar
==========

Supervisión de disponibilidad: /api/v2/health
---------------------------------------------

Fess ofrece una API de comprobación de estado que se puede llamar sin autenticación.

::

    $ curl -fsS --max-time 10 http://localhost:8080/api/v2/health
    {"response":{"status":0,"engine":{"status":"GREEN","ping_status":0}}}

Los códigos de estado HTTP significan lo siguiente.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Estado
     - Situación
   * - 200
     - Fess responde y el clúster de OpenSearch está en ``GREEN`` o ``YELLOW``
   * - 503
     - El clúster de OpenSearch está en ``RED``, o Fess no puede conectarse a OpenSearch (``error.details.engine.status`` es ``UNAVAILABLE``)
   * - Sin respuesta / tiempo de espera agotado
     - El proceso de Fess se ha detenido, o Fess está esperando a un OpenSearch que no responde

La herramienta de supervisión debe basar su evaluación en este código de estado.
Con ``curl``, la opción ``-f`` hace que el código de salida sea distinto de 0 ante un 503.
Si OpenSearch deja de responder sin que su proceso se detenga, esta API espera la respuesta de OpenSearch hasta ``index.health.timeout`` (``10m`` por defecto).
En la herramienta de supervisión, establezca un tiempo de espera, como ``--max-time 10`` en el ejemplo anterior, y trate también el tiempo de espera agotado como un fallo.
Tenga en cuenta que ``/api/v1/health``, presentado en versiones anteriores de este artículo, no está disponible en una instalación estándar de 15.9 (``/api/v1`` solo se ofrece si se instala el plugin ``fess-webapp-v1-api``).

En Docker, ``fess01`` utiliza esta API mediante dos mecanismos.

- El ``healthcheck`` de ``compose.yaml`` la llama cada 30 segundos; el resultado aparece como ``(healthy)`` en ``docker compose ps``
- El script de arranque del contenedor también la llama cada 60 segundos y, una vez iniciado Fess, detiene el contenedor tras 5 respuestas consecutivas distintas de 200. Gracias a ``restart: unless-stopped``, el contenedor se reinicia a continuación

Por ello, si OpenSearch permanece en ``RED`` durante unos minutos, ``fess01`` se reinicia una y otra vez.
Si ``fess01`` se reinicia continuamente, revise primero ``search01``.

Supervisión de recursos: /api/admin/stats
-----------------------------------------

El uso del heap y el espacio libre en disco se obtienen con la API de administración ``GET /api/admin/stats``.
[Información del sistema] > [Información de configuración] solo muestra una lista de propiedades, no el uso de memoria.

La API de administración requiere un token de acceso.

1. Abra [Sistema] > [Token de acceso] y haga clic en [Crear nuevo]
2. Introduzca el propósito en "Nombre" (por ejemplo, ``monitoring``) y ``{role}admin-api`` en "Permisos", y haga clic en [Crear]
3. Abra el token creado desde la lista y anote el valor de "Token"

.. warning::

   Un token ``{role}admin-api`` permite usar todas las API de administración, incluidas las que modifican o eliminan configuración.
   No existe ningún ajuste para limitarlo a solo lectura.
   Guárdelo, por ejemplo en un archivo del servidor de supervisión, con el mismo cuidado que la contraseña del administrador.

Pase el token en la cabecera ``Authorization``.
El siguiente ejemplo extrae el uso del heap (%) y el porcentaje de uso de cada sistema de archivos.

::

    $ curl -fsS -H "Authorization: Bearer <token>" http://localhost:8080/api/admin/stats \
        | jq '{heap: .response.stats.jvm.memory.heap.percent, fs: [.response.stats.fs[] | {path, percent}]}'

La respuesta incluye además el número y el tiempo acumulado de las recolecciones de basura (``jvm.gc``), el uso de CPU y la carga media del sistema operativo (``os``), y el estado del clúster de OpenSearch y el número de shards (``engine``).
Para ver la lista completa de campos, consulte `API de Stats <https://fess.codelibs.org/es/stable/api/admin/api-admin-stats.html>`__.

Tenga en cuenta los dos puntos siguientes al leer los valores.

- ``jvm`` son los valores de la JVM de Fess (la aplicación web). Los rastreos se ejecutan en un proceso JVM independiente, por lo que la falta de memoria del rastreador no aparece aquí. Compruébela en ``fess-crawler.log`` (véase más adelante)
- ``fs`` son los sistemas de archivos del host en el que se ejecuta Fess (en Docker, el contenedor). Para conocer el espacio libre del área de datos de OpenSearch, consulte directamente a OpenSearch

::

    $ curl -s "http://localhost:9200/_cat/allocation?v"

Para cambiar el tamaño del heap, consulte :doc:`guide-14`.

Recibir notificaciones
----------------------

Los destinos de las notificaciones de Fess se configuran con tres campos de la sección "Notificación" de [Sistema] > [General].

- "Correo de notificación": direcciones de correo de los destinatarios (separadas por comas si hay varias)
- "Slack Webhook URLs": la URL de Incoming Webhook de Slack
- "Google Chat Webhook URLs": la URL de Webhook de Google Chat

En cuanto se configura cualquiera de ellos, se envían los tres tipos de notificación siguientes a los mismos destinos.

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Notificación
     - Cuándo se envía
     - Configuración adicional necesaria
   * - Fin del rastreo (asunto ``[FESS] Crawler completed``)
     - Se envía cada vez que termina un trabajo de rastreo, haya tenido éxito o no. Incluye el estado (OK/FAIL) y el número de documentos indexados
     - Ninguna
   * - Cambio de estado de OpenSearch (asunto ``[FESS] Status Change``)
     - El trabajo del programador "Search Engine Monitor" consulta OpenSearch cada minuto y envía un aviso cuando el clúster pasa a ``RED`` y cuando sale de ``RED``
     - Ninguna
   * - Notificación de registros (asunto ``[FESS] ERROR Log Alert``)
     - El trabajo "Log Notification" reúne cada 5 minutos los registros ERROR (o de un nivel igual o superior al indicado) escritos por Fess, el rastreador y otros procesos, y los envía juntos
     - Activar "Log Notification" en [General] y elegir un "Log Notification Level"

Si Fess no puede conectarse a OpenSearch, el propio trabajo "Search Engine Monitor" falla y no se envía la notificación de cambio de estado.
Detecte las pérdidas de conexión supervisando ``/api/v2/health`` desde el exterior, como se describe en la sección anterior.

El nivel predeterminado de la notificación de registros es ``ERROR``.
Los trabajos programados que fallan se registran con ``WARN`` (``Failed to execute job: ...``), así que, si también quiere enterarse de los fallos de los trabajos, establezca "Log Notification Level" en ``WARN``.
En ese caso, también se notificarán todos los demás ``WARN``.

Para recibir correos, configure el servidor SMTP en dos archivos y reinicie Fess.

::

    mail.smtp.server.main.host.and.port=smtp.example.com:587

- ``fess_env_web.properties``: se usa para la notificación de registros, los cambios de estado y el botón [Enviar correo de prueba]
- ``fess_env_crawler.properties``: se usa para la notificación de fin del rastreo (porque el rastreo se ejecuta en un proceso independiente)

Estos archivos están en ``app/WEB-INF/classes/`` en la versión ZIP y en ``/etc/fess/`` en los paquetes RPM/DEB.
Tras configurarlos, compruebe con [Enviar correo de prueba] en [General] que el correo llega.

Si quiere recibir notificaciones rápidamente en Docker, lo más sencillo es un webhook de Slack o de Google Chat, ya que no hay que editar archivos.
Sin embargo, la configuración de [General] se guarda en ``system.properties`` dentro del contenedor ``fess01``, por lo que se pierde al volver a crear el contenedor con ``docker compose down`` (consulte la sección sobre la detención y el reinicio en :doc:`guide-02`).
Incluya también ``system.properties`` en la copia de seguridad que se describe más adelante.

Revisar los tiempos de respuesta de búsqueda y los resultados del rastreo
-------------------------------------------------------------------------

Además de la supervisión externa, revise periódicamente las tres pantallas de administración siguientes.

- [Información del sistema] > [Registro de trabajo]: el estado (OK/Fallo) y el resultado de trabajos como "Default Crawler". Los trabajos que se ejecutan cada minuto o cada pocos minutos, como "Search Engine Monitor" y "Log Notification", no se registran aquí
- [Información del sistema] > [Información de rastreo]: "Estado del rastreador", "Tamaño del índice (Web/Archivo)" y "Tamaño del índice (Almacén de datos)" de cada sesión. Compruebe que no hayan disminuido mucho respecto a la vez anterior
- La pestaña [Rendimiento] de [Información del sistema] > [Registro de búsqueda]: la mediana, el p95 y el p99 de los tiempos de respuesta, y los términos de búsqueda con respuestas lentas. Para interpretar los registros de búsqueda, consulte :doc:`guide-08`

Leer los registros
==================

Tipos de archivos de registro
-----------------------------

Fess escribe los registros en un archivo distinto para cada tipo de procesamiento.
Elija el archivo que debe abrir según lo que quiera investigar.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Archivo
     - Contenido
   * - ``fess.log``
     - Registro de Fess (página de búsqueda, administración, API, programador). Fallos de arranque, errores de conexión a OpenSearch, fallos al importar copias de seguridad, etc.
   * - ``fess-crawler.log``
     - Registro del proceso del rastreador. Errores de obtención por URL, fallos de autenticación, falta de memoria del rastreador, etc.
   * - ``audit.log``
     - Registro de auditoría de inicios y cierres de sesión y de operaciones de administración
   * - ``fess-suggest.log`` / ``fess-thumbnail.log``
     - Registros de la generación de sugerencias y de miniaturas
   * - ``fess-llm.log``
     - Registro del modo de búsqueda con IA (RAG) y de la integración con LLM
   * - ``searchlog.log``
     - Un registro por cada búsqueda (cuando "Registro de búsqueda" está activado en [General])
   * - ``server_*.log``
     - Registros de Tomcat

Su ubicación depende del método de instalación.

- Versión ZIP: ``logs/`` en el directorio donde se descomprimió Fess
- Paquetes RPM/DEB: ``/var/log/fess/``
- Docker: ``/var/log/fess/`` dentro del contenedor. ``fess.log``, ``fess-crawler.log``, ``audit.log`` y otros también se envían a la salida estándar, por lo que se pueden leer con ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01``. Se pierden al volver a crear el contenedor

Sea cual sea el método de instalación, puede descargar un archivo haciendo clic en su nombre en [Información del sistema] > [Archivo de registro].
Así, también el personal que no puede iniciar sesión en el servidor puede revisar los registros.

Cada registro se comprime en ``.log.gz`` y se rota al cambiar la fecha o al superar los 100 MB.
Los archivos comprimidos se eliminan automáticamente a los 90 días en el caso de ``fess.log`` y ``searchlog.log``, y a los 360 días en el de ``audit.log``.
En cambio, los archivos comprimidos de los registros del rastreador y de los procesos hijos, como ``fess-crawler.log``, ``fess-suggest.log`` y ``fess-thumbnail.log``, no se eliminan automáticamente.
Supervise el espacio que ocupa el directorio de registros y elimine periódicamente los archivos antiguos.

Investigar con más detalle
--------------------------

De forma predeterminada, ``fess.log`` registra WARN o superior, y ``fess-crawler.log`` registra INFO o superior.
Para que ``fess.log`` sea más detallado, suba "Nivel de registro" en [Sistema] > [General] a ``INFO`` o ``DEBUG``.
Este cambio se revierte al reiniciar Fess.
El nivel de registro del rastreador lo determina el script del trabajo.
El script de "Default Crawler" contiene ``logLevel("info")``; si lo cambia a ``logLevel("debug")`` en [Sistema] > [Programador], se escribirán registros detallados a partir del siguiente rastreo.
Cuando termine la investigación, restablezca el valor original.
Para cambiar el nivel de forma permanente, consulte `Configuración de Registro <https://fess.codelibs.org/es/stable/config/admin-logging.html>`__.

Si va a pedir ayuda en un foro u otro lugar, resulta útil [Descargar registros] en "Diagnóstico" de [Información del sistema] > [Mantenimiento].
Descarga un archivo zip con los registros, ``system.properties``, ``fess_config.properties``, el contenido de los índices de configuración y el estado de OpenSearch.
Los valores como las claves de API y ``app.cipher.key`` se sustituyen por ``XXXXXXXX``, pero el cuerpo de los registros y el contenido de los índices de configuración no se enmascaran.
Revise el contenido antes de entregarlo a terceros.

Hacer copias de seguridad
=========================

Qué está dónde
--------------

Los datos de Fess se reparten en tres lugares.
[Información del sistema] > [Copia de seguridad] solo cubre el primero de ellos.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Datos
     - Ubicación
     - Método de copia de seguridad
   * - Configuraciones de rastreo, programador, etiquetas, usuarios, configuración de [General]
     - Índices de configuración de OpenSearch y ``system.properties``
     - [Información del sistema] > [Copia de seguridad], o la API de administración
   * - Documentos rastreados, diccionarios (sinónimos, palabras vacías, etc.)
     - Índices ``fess.*`` e índice ``configsync`` de OpenSearch
     - Snapshots de OpenSearch (para los diccionarios por sí solos, también sirve copiar los archivos)
   * - ``fess_config.properties`` (incluido ``app.cipher.key``), configuración de arranque, plugins instalados
     - Archivos en el servidor de Fess
     - Copia de los archivos, o gestión de la configuración

Los documentos rastreados se pueden reconstruir volviendo a rastrear, siempre que se haya restaurado la configuración.
Haga snapshots solo si volver a rastrear llevaría demasiado tiempo.

Archivos que se obtienen en [Copia de seguridad]
------------------------------------------------

[Información del sistema] > [Copia de seguridad] muestra los archivos siguientes.
Haga clic en un nombre para descargar ese archivo.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Archivo
     - Contenido
   * - ``fess_basic_config.bulk``
     - Configuración como las configuraciones de rastreo, el programador, las etiquetas, las coincidencias de palabras clave y la autenticación web/de archivos
   * - ``fess_config.bulk``
     - Todo lo anterior más la información de rastreo, las URL de fallo, los registros de trabajos, las etiquetas de usuario, etc.
   * - ``fess_user.bulk``
     - Usuarios, roles y grupos
   * - ``system.properties``
     - La configuración de [Sistema] > [General]
   * - ``fess.json`` / ``doc.json``
     - Configuración y mapping del índice de documentos
   * - ``*.ndjson``
     - Registros de búsqueda, registros de clics, favoritos, registros del chat de IA y usuarios de búsqueda. Se pueden descargar, pero no subir para restaurarlos

Los archivos que se usan para restaurar la configuración son ``fess_basic_config.bulk``, ``fess_user.bulk`` y ``system.properties``.
Si usa etiquetas de usuario, obtenga también ``fess_config.bulk``.

Salvo las credenciales que se describen más adelante, los archivos ``*.bulk`` contienen los valores de configuración sin cifrar.
Guárdelos como archivos confidenciales.

Copia de seguridad diaria con cron
----------------------------------

La API de administración ``GET /api/admin/backup/file/<nombre-de-archivo>/`` devuelve los mismos archivos que la pantalla.
Cree un token con el mismo procedimiento que en "Supervisión de recursos" y guárdelo en un archivo que solo pueda leer el usuario que ejecuta el script.

::

    $ sudo mkdir -p /etc/fess-backup
    $ sudo sh -c 'umask 077; echo "<token>" > /etc/fess-backup/token'

El siguiente script guarda los archivos en un directorio por fecha y elimina los directorios con más de 30 días de antigüedad (el periodo de conservación es un ejemplo).

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    FESS_URL=http://localhost:8080
    FESS_TOKEN=$(cat /etc/fess-backup/token)
    BASE_DIR=/var/backups/fess
    BACKUP_DIR="${BASE_DIR}/$(date +%Y%m%d)"

    umask 077
    mkdir -p "${BACKUP_DIR}"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      curl -fsS -H "Authorization: Bearer ${FESS_TOKEN}" \
        -o "${BACKUP_DIR}/${id}" "${FESS_URL}/api/admin/backup/file/${id}/"
      test -s "${BACKUP_DIR}/${id}"
    done

    # Entorno Docker: copiar también los archivos de diccionario
    docker cp search01:/usr/share/opensearch/config/dictionary/. "${BACKUP_DIR}/dictionary"

    find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

Puntos clave:

- No se puede omitir la ``/`` final de la URL. Como los nombres de archivo contienen un punto, sin la ``/`` la solicitud se trata como una petición de un archivo estático y devuelve 404
- Sin ``-f``, ``curl`` guarda también en el archivo las respuestas 404 y otros errores, y parece que el script ha tenido éxito. Con ``-f`` y ``set -e``, el script se detiene si algo falla
- En la versión ZIP y en los paquetes RPM/DEB, en lugar de la línea ``docker cp``, copie el directorio de diccionarios del lado de OpenSearch (la ubicación a la que apunta ``FESS_DICTIONARY_PATH`` de Fess)

Guarde el script como ``/usr/local/bin/fess-backup.sh``, dele permiso de ejecución y regístrelo en el crontab de root (en este ejemplo, se ejecuta a diario a las 2:30).

::

    30 2 * * * /usr/local/bin/fess-backup.sh

Después de registrarlo, ejecútelo una vez manualmente.
Abra ``fess_basic_config.bulk`` y compruebe que las líneas que empiezan por ``{"index":{"_index":`` se alternan con líneas JSON con el contenido de la configuración.
El mismo proceso también se puede escribir con ``fessctl`` (consulte :doc:`guide-16`).

Anotar app.cipher.key
---------------------

Fess 15.9 cifra con ``app.cipher.key`` de ``fess_config.properties`` las contraseñas de la autenticación web y de archivos, así como las contraseñas y secretos guardados en los parámetros de las configuraciones de rastreo y de almacén de datos.
También permanecen cifrados en los archivos ``*.bulk``.
Para restaurar en otro servidor, es necesario configurar en él el mismo ``app.cipher.key``.
Con una clave distinta no se pueden descifrar: se registra ``CipherFailureException`` en ``fess-crawler.log`` y fallan los rastreos que usan esas credenciales.

``fess_config.properties`` está en ``app/WEB-INF/classes/`` en la versión ZIP y en ``/etc/fess/`` en los paquetes RPM/DEB.
Si ha cambiado el valor, trate este archivo como confidencial, igual que los archivos ``*.bulk``, y guárdelo en otro lugar.
Para cambiar el valor en Docker, indique ``-Dfess.config.app.cipher.key=<valor>`` en ``FESS_JAVA_OPTS`` de ``compose.yaml``.
Así se usará la misma clave aunque se vuelva a crear el contenedor.

.. warning::

   Si cambia ``app.cipher.key`` después de haber guardado credenciales, los valores guardados hasta entonces ya no se podrán descifrar.
   Si lo cambia, hágalo antes de registrar las credenciales de autenticación web, de archivos o de almacenes de datos.
   En un entorno que ya está en producción, no cambie el valor y anótelo.

Snapshots del índice de documentos
----------------------------------

Para restaurar los documentos sin volver a rastrear, use los snapshots de OpenSearch.
Además de ``fess*``, incluya siempre el índice ``configsync``, que contiene los diccionarios.
Sin ``configsync``, al restaurar en un OpenSearch nuevo faltan los archivos de diccionario y el índice de documentos no se puede abrir.

Para usar snapshots, la ruta del repositorio (``path.repo``) debe estar configurada en OpenSearch.
No está definida en ``compose-opensearch3.yaml`` de docker-fess, así que añádala si va a usar snapshots.
Los pasos para registrar el repositorio, crear snapshots y restaurarlos se describen en `Gestión de Índices <https://fess.codelibs.org/es/stable/config/admin-index-backup.html>`__.
Restaure con Fess detenido y restaure primero ``configsync``.

Restaurar
=========

Antes de restaurar
------------------

La restauración desde [Copia de seguridad] no sustituye por completo el contenido de OpenSearch.

- La restauración solo se hace subiendo archivos. La API de administración solo sirve para descargar; no existe una API de restauración
- Cada configuración de un archivo ``*.bulk`` solo se escribe si no existe la misma configuración en el servidor o si es más reciente que la del servidor. Las configuraciones modificadas después de la copia de seguridad no vuelven a su contenido anterior
- Las configuraciones creadas después de la copia de seguridad no se eliminan y se conservan

Por eso, no sirve para "devolver al estado de ayer una configuración modificada por error".
Úsela para migrar a un servidor nuevo o para restaurar un entorno reconstruido.

Restaurar la configuración en otro servidor
-------------------------------------------

1. Instale la misma versión de Fess en el destino y establezca ``app.cipher.key`` en ``fess_config.properties`` con el mismo valor que en el origen
2. Instale los plugins que se usaban en el origen (almacenes de datos, SSO, etc.) y reinicie Fess
3. Inicie sesión en la administración y abra [Información del sistema] > [Copia de seguridad]
4. Seleccione ``fess_basic_config.bulk`` en "Archivo masivo" y haga clic en [Subir]. Se muestra "Proceso masivo iniciado."
5. Suba del mismo modo ``fess_user.bulk`` y ``system.properties``. Si usa etiquetas de usuario, suba también ``fess_config.bulk`` (también se importan la información de rastreo y los registros de trabajos del origen)

La importación se realiza en segundo plano.
Espere un momento y compruebe lo siguiente.

- La configuración del origen aparece en [Rastreador] > [Web], [Sistema de archivos] y [Almacén de datos], y en [Sistema] > [Programador]
- Los usuarios del origen aparecen en [Usuario] > [Usuario]
- Los destinos de notificación y otros ajustes de [Sistema] > [General] tienen los valores del origen

Por último, restaure los diccionarios y reconstruya los documentos.

- Diccionarios: en [Sistema] > [Diccionario], abra la pantalla de cada tipo y suba el archivo de diccionario respaldado. A continuación, ejecute "Recargar índice de documentos" en [Información del sistema] > [Mantenimiento]. Durante la recarga, la búsqueda deja de estar disponible por poco tiempo
- Documentos: en [Sistema] > [Programador], haga clic en [Iniciar ahora] para "Default Crawler" y vuelva a rastrear. Para restaurar desde un snapshot, siga el procedimiento descrito anteriormente

Cuando termine el rastreo, compruebe el número de documentos indexados en [Información del sistema] > [Información de rastreo].
Si una configuración de rastreo con autenticación muestra 0 documentos, compruebe si aparece ``CipherFailureException`` en ``fess-crawler.log``.
Si aparece, ``app.cipher.key`` no coincide con el del origen.

Responder a incidencias
=======================

A continuación se resumen los síntomas habituales y dónde comprobarlos en Fess.

La página de búsqueda no se abre o /api/v2/health devuelve 503
--------------------------------------------------------------

1. Compruebe el estado de OpenSearch. Si ``status`` en ``curl -s "http://localhost:9200/_cluster/health?pretty"`` es ``red``, el problema está en OpenSearch. En Docker, revise ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs search01``
2. Si OpenSearch funciona correctamente pero Fess no responde, busque errores de arranque en ``fess.log``
3. Si el clúster pasa a ``red`` justo después de restaurar desde un snapshot, es posible que no se haya restaurado ``configsync`` (véase más arriba)

El rastreo falla o ha disminuido el número de documentos indexados
------------------------------------------------------------------

1. En [Información del sistema] > [Registro de trabajo], abra la fila del trabajo correspondiente y revise "Resultado"
2. En [Información del sistema] > [Información de rastreo], compare "Estado del rastreador" y los tamaños de índice de la sesión más reciente con los de la anterior
3. En [Información del sistema] > [URL de fallo], revise "Tipo", "Registro" y "Número de errores" de las URL que no se pudieron obtener. Los códigos HTTP 404, 403, 410 y 401 también se registran aquí
4. Los detalles están en ``fess-crawler.log``. Si busca el "Nombre del hilo" que aparece en el detalle de la URL de fallo, podrá seguir los registros de alrededor de ese momento

Si ``fess-crawler.log`` contiene ``OutOfMemoryError``, el heap del proceso del rastreador es insuficiente.
El heap del rastreador se define con ``jvm.crawler.options`` en ``fess_config.properties`` (``-Xmx512m`` por defecto) y es independiente del heap de Fess.
Para ajustarlo, consulte :doc:`guide-14`.

No llegan las notificaciones
----------------------------

En el caso del correo, compruebe primero si llega usando [Enviar correo de prueba] en [General].
Si solo no llega el correo de fin del rastreo, revise el servidor SMTP de ``fess_env_crawler.properties``.
En Docker, compruebe también que la configuración de [General] no se haya perdido por volver a crear el contenedor con ``down`` y ``up``.
Si solo no llega la notificación de registros, compruebe que "Log Notification" esté activado, que el trabajo "Log Notification" esté habilitado y que "Log Notification Level" sea el adecuado (``WARN`` para los fallos de trabajos).
Encontrará otros puntos de comprobación en "Resolución de Problemas" de `Notificación de Registros <https://fess.codelibs.org/es/stable/config/admin-log-notification.html>`__.

La búsqueda es lenta
--------------------

1. En la pestaña [Rendimiento] de [Información del sistema] > [Registro de búsqueda], compruebe si la lentitud afecta a términos de búsqueda concretos o a todas las búsquedas
2. Compare ``jvm.memory.heap.percent`` y el tiempo acumulado de ``jvm.gc`` en ``/api/admin/stats`` con los valores de antes de la ralentización

Artículos relacionados
======================

- Gestionar la configuración con scripts o con ``fessctl``: :doc:`guide-16`
- Ajustar el heap o distribuir OpenSearch y Fess en varios servidores: :doc:`guide-14`
- Reforzar la protección de acceso con SSO, registros de auditoría, etc.: :doc:`guide-15`
- Mejorar la calidad de la búsqueda a partir de los registros de búsqueda: :doc:`guide-08`

Referencias
===========

- `Health API <https://fess.codelibs.org/es/stable/api/api-health.html>`__
- `API de Stats <https://fess.codelibs.org/es/stable/api/admin/api-admin-stats.html>`__
- `Notificación de Registros <https://fess.codelibs.org/es/stable/config/admin-log-notification.html>`__
- `Configuración de Registro <https://fess.codelibs.org/es/stable/config/admin-logging.html>`__
- `Archivo de Registro <https://fess.codelibs.org/es/stable/admin/log-guide.html>`__
- `Copia de Seguridad <https://fess.codelibs.org/es/stable/admin/backup-guide.html>`__
- `API de Backup <https://fess.codelibs.org/es/stable/api/admin/api-admin-backup.html>`__
- `Gestión de Índices <https://fess.codelibs.org/es/stable/config/admin-index-backup.html>`__
- `URL de fallo <https://fess.codelibs.org/es/stable/admin/failureurl-guide.html>`__
- `Mantenimiento <https://fess.codelibs.org/es/stable/admin/maintenance-guide.html>`__
