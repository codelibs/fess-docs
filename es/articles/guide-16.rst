===============================================
Gestionar Fess como código y recrear su entorno
===============================================

Introducción
============

En la configuración acumulada a través de la consola de administración no se puede rastrear después quién cambió qué ni cuándo.
Y cuando lleva a producción una configuración validada en un entorno de pruebas, termina repitiendo a mano las mismas operaciones en pantalla.

En este artículo escribimos la configuración de Fess 15.9 como archivos de un repositorio Git, la aplicamos con un script a un entorno Docker recién iniciado y comprobamos que se ha aplicado.
Para ello usamos los archivos Compose de docker-fess, la API de administración de Fess (Admin API) y fessctl, su cliente de línea de comandos.

El alcance de las copias de seguridad y el procedimiento de restauración no se tratan aquí.
Consulte :doc:`guide-10`.

Decidir cómo gestionar cada configuración según dónde se guarda
===============================================================

La configuración de Fess no está concentrada en un solo lugar.
La forma de convertirla en código depende de dónde se guarda.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Configuración
     - Dónde se guarda
     - Cómo convertirla en código
   * - Versión de Fess, plugins
     - Imagen Docker, contenedor
     - Tag de imagen en el archivo Compose y ``FESS_PLUGINS``
   * - Elementos de ``fess_config.properties`` (como ``app.cipher.key``)
     - Archivo dentro del contenedor
     - ``-Dfess.config.<clave>`` en ``FESS_JAVA_OPTS``
   * - Elementos de [Sistema] > [General]
     - ``system.properties`` dentro del contenedor
     - ``-Dfess.system.<clave>`` en ``FESS_JAVA_OPTS``
   * - Configuraciones de rastreo, etiquetas, programador, usuarios, etc.
     - Índices de configuración de OpenSearch
     - Admin API (fessctl)
   * - Diccionarios (sinónimos, etc.)
     - ``FESS_DICTIONARY_PATH`` del contenedor de OpenSearch
     - Carga de diccionarios mediante la Admin API (fessctl)
   * - Tokens de acceso, valor de la clave de cifrado
     - Los tokens en OpenSearch, la clave de cifrado en las opciones de arranque
     - Fuera de Git, en ``.env`` o en los secretos de la CI

El contenedor ``fess01`` de docker-fess no tiene volumen, por lo que ``system.properties`` desaparece junto con el contenedor al ejecutar ``docker compose down``.
La configuración guardada en OpenSearch, como las configuraciones de rastreo, se conserva en su volumen.

Estructura del repositorio
==========================

En este artículo gestionamos con Git los siguientes archivos.

::

    fess-infra/
    ├── compose.yaml               archivo de docker-fess v15.9.0
    ├── compose-opensearch3.yaml   archivo de docker-fess v15.9.0
    ├── compose-site.yaml          diferencias para su propio entorno
    ├── dict/
    │   └── synonym.txt            diccionario de sinónimos
    ├── apply.sh                   script que aplica la configuración
    ├── .gitignore
    └── .env                       fuera de Git (clave de cifrado y token)

Fijar la configuración de Docker a una versión
==============================================

Obtener los archivos Compose
----------------------------

Obtenga los archivos de la etiqueta ``v15.9.0`` de docker-fess.
``compose.yaml`` apunta a la imagen ``ghcr.io/codelibs/fess:15.9.0`` y ``compose-opensearch3.yaml`` a ``ghcr.io/codelibs/fess-opensearch:3.9.0``, de modo que las versiones quedan fijadas.

::

    $ mkdir fess-infra && cd fess-infra
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

No edite estos dos archivos; escriba las diferencias de su entorno en un archivo aparte.
Así, al actualizar docker-fess solo tendrá que volver a obtener los archivos.

Escribir las diferencias de su entorno
--------------------------------------

Cree ``compose-site.yaml``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-ds-git:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.app.cipher.key=${FESS_CIPHER_KEY:?FESS_CIPHER_KEY is not set} -Dfess.system.purge.searchlog.day=180"

- En ``FESS_PLUGINS`` se indican, separados por espacios, los plugins que se descargan al arrancar, con el formato ``nombre:versión``. Use la misma versión 15.9.x que Fess. El plugin ``fess-ds-git`` del ejemplo sirve para rastrear repositorios Git con un almacén de datos. El origen de la descarga está fijado en ``maven.codelibs.org``, por lo que aquí solo puede indicar plugins publicados, y el contenedor debe poder salir a Internet
- ``-Dfess.config.<clave>`` tiene prioridad sobre el elemento del mismo nombre de ``fess_config.properties``
- ``-Dfess.system.<clave>`` pasa a ser el valor predeterminado de un elemento de [General]. ``purge.searchlog.day`` en el ejemplo es el número de días de "Eliminar registros de búsqueda anteriores" en [General]

Compose combina ``environment`` por nombre de variable, de modo que ``SEARCH_ENGINE_HTTP_URL`` y las demás variables de ``compose.yaml`` se mantienen tal cual.
Sin embargo, si define la misma variable en varios archivos, el valor del archivo posterior la reemplaza.
Las superposiciones como ``compose-openai.yaml`` también definen ``FESS_PLUGINS`` y ``FESS_JAVA_OPTS``, así que, si las combina, reúna los valores en un solo archivo.

.. note::

   ``-Dfess.system.<clave>`` solo se usa cuando ``system.properties`` no contiene esa clave.
   En cuanto guarde [General] una sola vez en la consola de administración o ejecute ``fessctl general update``, todos los elementos de la pantalla se escriben en ``system.properties`` y, a partir de entonces, esos valores tienen prioridad.
   En ese estado, cambiar el valor en ``compose-site.yaml`` no tiene efecto hasta que ejecute ``down`` y vuelva a crear el contenedor.

Decidir la clave de cifrado
---------------------------

``app.cipher.key`` es la clave que cifra las contraseñas de la autenticación web y de la autenticación de archivos, así como los valores secretos guardados en los parámetros de las configuraciones de rastreo y de almacén de datos.
No use el valor predeterminado ``___change__me___``; decida la clave antes del primer arranque.

La cadena de la clave se usa tal cual como clave AES, por lo que debe tener 16, 24 o 32 bytes.
La salida de ``openssl rand -hex 16`` (32 caracteres hexadecimales) ocupa 32 bytes.

::

    $ printf 'FESS_CIPHER_KEY=%s\n' "$(openssl rand -hex 16)" > .env
    $ printf '.env\nbackup/\n' > .gitignore

Si cambia la clave después de haber guardado credenciales, los valores guardados ya no se pueden descifrar y los rastreos que usan esa configuración fallan.
También necesitará la misma clave para restaurar una copia de seguridad en otro entorno (:doc:`guide-10`).
Guarde también una copia fuera de ``.env``, por ejemplo en un gestor de contraseñas.

El valor de ``FESS_JAVA_OPTS`` es visible con ``docker inspect``.
Si quiere evitarlo, monte ``fess_config.properties`` en ``/opt/fess`` (consulte "Cómo Aplicar Archivos de Configuración" en `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__).

Arrancar
--------

Indique los tres archivos en cada comando de Compose.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-site.yaml up -d

La comprobación de estado de ``fess01`` llama a ``/api/v2/health``; cuando ``docker compose ... ps`` muestra ``fess01`` como ``(healthy)``, todo está listo.

Crear un token de acceso para la Admin API
==========================================

Las llamadas a la Admin API requieren un token de acceso, y la API que crea tokens tampoco se puede llamar sin uno.
Por eso, en cada entorno nuevo, el primer token se crea una sola vez en la consola de administración.

1. Inicie sesión en ``http://localhost:8080/admin/`` con ``admin`` / ``admin`` y establezca la nueva contraseña que se le pide (8 caracteres como mínimo)
2. Abra [Sistema] > [Token de acceso] y haga clic en [Crear nuevo]
3. Introduzca ``fess-infra`` en "Nombre" y ``{role}admin-api`` en "Permisos", y haga clic en [Crear]
4. Abra en la lista el token creado y copie el valor de "Token"

Añada el valor copiado a ``.env``.

::

    $ echo 'FESS_ACCESS_TOKEN=<valor copiado>' >> .env

Un token con ``{role}admin-api`` puede realizar todas las operaciones de la Admin API.
Eso incluye cambiar la configuración, crear usuarios e incluso descargar copias de seguridad, y no es posible crear un token limitado a un uso concreto.
Trátelo como la contraseña del administrador y no lo incluya nunca en Git ni en JavaScript que se ejecute en el navegador.

Preparar fessctl
================

fessctl es una herramienta de línea de comandos que llama a la Admin API.
Instale, fijando la versión, la 0.4.0, cuyos valores predeterminados están pensados para Fess 15.9.
Requiere Python 3.13 o posterior.

::

    $ pipx install fessctl==0.4.0

También puede usar ``uv tool install fessctl==0.4.0``.
Los scripts siguientes usan además ``jq`` y ``curl`` para extraer valores de las respuestas.

fessctl lee el destino de ``FESS_ENDPOINT`` (valor predeterminado ``http://localhost:8080``), el token de ``FESS_ACCESS_TOKEN`` y la versión del Fess al que se conecta de ``FESS_VERSION``.
Indique ``15.9.0`` en ``FESS_VERSION``.
El motivo es que la forma de llamar a la API cambia según la versión.

Compruebe la conexión.

::

    $ set -a; . ./.env; set +a
    $ export FESS_VERSION=15.9.0
    $ fessctl ping
    $ fessctl webconfig list

``ping`` termina con el código de salida 0 si el estado del clúster es GREEN o YELLOW.
La comprobación de estado funciona incluso sin token, así que compruebe la validez del token con ``webconfig list``.
Si se produce un error de autenticación, revise el valor del token y sus permisos.
Con ``-o json``, todos los comandos muestran la respuesta de la Admin API tal cual, de modo que puede extraer valores con ``jq``.

Incluir en Git el contenido inicial del diccionario
---------------------------------------------------

La carga de un diccionario reemplaza el archivo completo.
Para no perder el contenido predeterminado, descargue primero el diccionario de sinónimos actual, inclúyalo en el repositorio y edítelo ahí.

::

    $ mkdir -p dict
    $ SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    $ fessctl dict synonym download "$SYNONYM_ID" --file dict/synonym.txt

El archivo descargado ya contiene la línea de sinónimos predeterminada ``fess,フエス``.
Añada una línea de sinónimos al final del archivo.
Las palabras separadas por comas se vuelven intercambiables: al buscar cualquiera de ellas también se encuentran los documentos que contienen las demás (para el formato, consulte `Diccionario de Sinónimos <https://fess.codelibs.org/es/stable/admin/synonym-guide.html>`__).

::

    ajustes,configuración

Al registrar palabras en japonés, escriba el hiragana como katakana, el katakana pequeño como katakana de tamaño normal ("フェス" pasa a ser "フエス") y los caracteres alfanuméricos de ancho completo como caracteres de ancho medio.

El script que aplica la configuración
=====================================

En ``apply.sh`` se escribe, en forma de comandos de fessctl, la configuración que se quiere tener en el entorno.
Está pensado para ejecutarse sobre un entorno nuevo, pero omite la creación si ya existe una configuración con el mismo nombre, por lo que ejecutarlo de nuevo no genera duplicados.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_ENDPOINT="${FESS_ENDPOINT:-http://localhost:8080}"
    export FESS_VERSION=15.9.0

    until curl -fsS "$FESS_ENDPOINT/api/v2/health" > /dev/null; do sleep 10; done
    fessctl ping

    # Etiqueta: se asigna durante el rastreo a los documentos que coinciden con la ruta de destino
    if ! fessctl labeltype list -o json | jq -e '.response.settings[] | select(.value == "fess_docs")' > /dev/null; then
      fessctl labeltype create --name "Documentación de Fess" --value fess_docs --version-no 1 \
        --included-path 'https://fess\.codelibs\.org/es/stable/.*' \
        --permission '{role}guest'
    fi

    # Configuración de rastreo web
    if ! fessctl webconfig list -o json | jq -e '.response.settings[] | select(.name == "Guía de búsqueda de Fess")' > /dev/null; then
      fessctl webconfig create --name "Guía de búsqueda de Fess" \
        --url https://fess.codelibs.org/es/stable/user/index.html \
        --included-url 'https://fess\.codelibs\.org/es/stable/user/.*' \
        --depth 2 --max-access-count 50 \
        --permission '{role}guest'
    fi

    # Diccionario de sinónimos: reemplazar el archivo completo y reabrir el índice de documentos para que se cargue
    SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    fessctl dict synonym upload "$SYNONYM_ID" dict/synonym.txt --yes
    curl -fsS -X POST "localhost:9200/_configsync/flush" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_close" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_open" > /dev/null

    # Iniciar el rastreo y esperar a que termine el trabajo
    SCHEDULER_ID=$(fessctl scheduler list -o json | jq -er '.response.settings[] | select(.name == "Default Crawler") | .id')
    JOBLOG_ID=$(fessctl scheduler start "$SCHEDULER_ID" -o json | jq -er '.response.job_log_id')
    until fessctl joblog get "$JOBLOG_ID" -o json \
        | jq -e '.response.log.job_status == "ok" or .response.log.job_status == "fail"' > /dev/null; do
      sleep 30
    done
    fessctl joblog get "$JOBLOG_ID" -o json | jq -e '.response.log.job_status == "ok"'

Los puntos clave del script son los siguientes.

- Con su salida de texto predeterminada, fessctl termina con un código distinto de 0 cuando la API devuelve un error, así que ``set -e`` detiene el script en ese punto. Con ``-o json``, muchos comandos muestran la respuesta de error y terminan con 0, por lo que el valor extraído se comprueba con ``jq -e``. Si el valor no existe, jq falla y el script se detiene ahí
- ``--version-no`` de ``labeltype create`` es obligatorio en fessctl 0.4.0. En una creación nueva indique ``1``
- Los elementos omitidos en ``webconfig create`` toman los valores predeterminados de fessctl. ``--depth`` es ``1`` y ``--max-access-count`` es ``1000000``, así que escriba los valores que pretende sin omitirlos. El valor predeterminado de ``--permission`` es ``{role}guest``
- El valor de una etiqueta solo admite caracteres alfanuméricos y ``_``. Las etiquetas se asignan durante el rastreo, así que créelas antes que la configuración de rastreo
- Sin ``--yes``, la carga del diccionario se detiene para pedir confirmación
- El diccionario de sinónimos actúa en el momento de la búsqueda, pero OpenSearch solo construye los analizadores al abrir un índice. Por eso primero se escribe el diccionario en un archivo con ``_configsync/flush`` y después se cierra y se abre ``fess.update``. Mientras tanto no se puede buscar, así que en un entorno en producción ejecútelo en un horario de poco tráfico. Es la misma operación que "Recargar índice de documentos" en [Información del sistema] > [Mantenimiento] de la consola de administración
- El ``job_log_id`` de la respuesta de ``scheduler start`` es directamente el ID que aparece en [Registro de trabajo]. El script espera hasta que el estado del trabajo sea ``ok`` o ``fail``, y termina como fallo si no es ``ok``. "Default Crawler" ejecuta todas las configuraciones de rastreo habilitadas

Si cambia el valor de una configuración que ya existe, este script solo omite la creación y no sobrescribe el valor.
Actualícela indicando su ID, como en ``fessctl webconfig update <ID> --max-access-count 100``, o vuelva a ejecutar el script sobre un entorno recreado junto con sus volúmenes.

Si ejecuta el script desde una CI, no coloque ``.env`` y pase ``FESS_ACCESS_TOKEN`` y ``FESS_ENDPOINT`` como variables de entorno desde los secretos de la CI.
En ese caso, cambie en las tres líneas de ``localhost:9200`` el destino por una dirección que llegue a OpenSearch.

Comprobar que la configuración se ha aplicado
=============================================

Cuando ``apply.sh`` termine con el código de salida 0, compruebe lo siguiente en este orden.

1. El plugin está instalado

   ::

       $ fessctl plugin installed

   Si ``fess-ds-git`` 15.9.0 aparece en la lista, está instalado.
   Aunque falle la descarga de un plugin de ``FESS_PLUGINS``, Fess arranca igualmente y solo aparece ``Failed to download`` en ``docker compose ... logs fess01``, así que compruébelo aquí.

2. El valor de [General] se ha aplicado

   ::

       $ fessctl general get -o json | jq '.response.setting.purge_search_log_day'

   Si devuelve ``180``, ``-Dfess.system.purge.searchlog.day`` está en vigor.
   En la Admin API los nombres están en snake_case, como ``purge_search_log_day``, y son distintos de las claves que siguen a ``-Dfess.system.``.

3. El diccionario se ha reemplazado

   ::

       $ fessctl dict synonym download "$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')" | grep 'ajustes'

   Si se muestra la línea añadida, la carga se ha realizado.
   También puede comprobarlo con ``fessctl dict synonym list``, pero de forma predeterminada muestra 100 entradas por página, por lo que una línea añadida al final puede no aparecer en la primera página.

4. Se puede buscar con la etiqueta

   ::

       $ curl -fsS --get --data-urlencode 'q=búsqueda' --data-urlencode 'fields.label=fess_docs' \
           http://localhost:8080/api/v2/search | jq '.response.record_count'

   Si devuelve 1 o más, toda la cadena, desde el rastreo y el etiquetado hasta la búsqueda, funciona.
   Si devuelve 0, revise [Información del sistema] > [URL de fallo] y el resultado en [Registro de trabajo] en la consola de administración.

Llamar directamente a la Admin API
==================================

Lo que llama fessctl es la Admin API bajo ``/api/admin/``.
Todos los recursos que contienen configuración, como las configuraciones de rastreo, tienen la siguiente forma (``<resource>`` es ``webconfig``, ``fileconfig``, ``dataconfig``, ``labeltype``, ``keymatch``, etc.).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Solicitud
     - Operación
   * - ``GET /api/admin/<resource>/settings``
     - Lista
   * - ``GET /api/admin/<resource>/setting/<ID>``
     - Obtener un elemento
   * - ``POST /api/admin/<resource>/setting``
     - Creación
   * - ``PUT /api/admin/<resource>/setting``
     - Actualización
   * - ``DELETE /api/admin/<resource>/setting/<ID>``
     - Eliminación

fessctl tiene subcomandos con los mismos nombres (``create``, ``list``, ``get``, ``update``, ``delete``), y puede consultar los elementos con, por ejemplo, ``fessctl fileconfig create --help``.
La carga de un diccionario se envía como multipart a ``POST /api/admin/dict/<tipo>/upload/<ID del diccionario>``.
El nombre del campo del archivo varía según el tipo; para los sinónimos es ``synonymFile``.
Los nombres de campo JSON están en snake_case, como ``max_access_count``.
Para cada campo, consulte las páginas de cada recurso a las que se llega desde `Visión General de Admin API <https://fess.codelibs.org/es/stable/api/admin/api-admin-overview.html>`__.

El siguiente comando devuelve el número de configuraciones de rastreo web.

::

    $ curl -fsS -H "Authorization: Bearer $FESS_ACCESS_TOKEN" \
        http://localhost:8080/api/admin/webconfig/settings | jq '.response.total'

Sin ``-f``, curl trata incluso una respuesta 404 o 401 como un éxito y el script no se da cuenta del fallo.

Descargar una copia de la configuración
=======================================

Para cubrir la configuración que no está escrita en Git (como la que se cambia directamente en la consola de administración), descargue también copias de seguridad con regularidad.
Los archivos afectados y el procedimiento de restauración se explican en :doc:`guide-10`.
Aquí solo mostramos un ejemplo de script que funciona con la misma preparación que ``apply.sh``.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_VERSION=15.9.0
    dest="backup/$(date +%Y%m%d)"
    umask 077
    mkdir -p "$dest"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      fessctl backup download "$id" --dest "$dest/$id" --force
    done

``fessctl backup download`` llama a ``/api/admin/backup/file/<ID>/`` con la ``/`` final que se necesita cuando el ID contiene un punto.
Si lo llama con curl, no olvide la ``/`` final ni ``-f``.
Sin la ``/`` final se obtiene un 404.

Con la Admin API solo se puede descargar; la restauración únicamente puede hacerse desde [Información del sistema] > [Copia de seguridad] en la consola de administración.
Las copias de seguridad no sirven, por tanto, como procedimiento para recrear otro entorno, así que mantenga la versión de referencia de la configuración en ``apply.sh``.

Lo que no debe ir a Git
=======================

- ``.env`` (la clave de cifrado y el token de acceso)
- Los archivos de copia de seguridad. Los ``*.bulk`` también contienen valores sin cifrar y deben tratarse como archivos confidenciales. ``system.properties`` también contiene valores introducidos en [General], como claves secretas de almacenamiento o secretos de cliente de SSO

Por eso se añadieron ``.env`` y ``backup/`` a ``.gitignore``.
Guarde las copias de seguridad en un lugar con acceso restringido, como un almacenamiento cifrado.

Artículos recomendados a continuación
=====================================

- Preparar el alcance de las copias de seguridad, la restauración y la supervisión: :doc:`guide-10`
- Repasar los fundamentos del arranque y la detención con Docker: :doc:`guide-02`
- Llamar a la API de búsqueda desde sistemas empresariales: :doc:`guide-11`
- Proteger la consola de administración, incluido el manejo de tokens de acceso y SSO: :doc:`guide-15`
- Crear sus propios plugins: :doc:`guide-17`

Referencias
===========

- `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__
- `Visión General de Admin API <https://fess.codelibs.org/es/stable/api/admin/api-admin-overview.html>`__
- `API de Dict <https://fess.codelibs.org/es/stable/api/admin/api-admin-dict.html>`__
- `API de Backup <https://fess.codelibs.org/es/stable/api/admin/api-admin-backup.html>`__
- `Diccionario (momento en que se aplican los cambios) <https://fess.codelibs.org/es/stable/admin/dict-guide.html>`__
- `Token de Acceso <https://fess.codelibs.org/es/stable/admin/accesstoken-guide.html>`__
- `fessctl (GitHub) <https://github.com/codelibs/fessctl>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
