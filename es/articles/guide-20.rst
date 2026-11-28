==========================================
Buscar en Fess desde agentes de IA con MCP
==========================================

Introducción
============

Cuando quiere que un agente de IA como Claude Code consulte documentos internos, si el agente puede llamar directamente a la búsqueda de Fess, puede usar los documentos indexados tal cual como fundamento de sus respuestas.
El mecanismo para ello es MCP (Model Context Protocol).
En Fess, al instalar el plugin ``fess-webapp-mcp`` se añade un punto de conexión de servidor MCP en ``/mcp``.

Este artículo explica cómo instalar este plugin en Fess 15.9, hacer obligatoria la autenticación, conectarse desde un agente de IA y comprobar que todo funciona.

Al terminar los pasos de este artículo, tendrá lo siguiente:

- Puede comprobar con ``curl`` que ``/mcp`` funciona
- Las llamadas sin token de acceso se rechazan
- El alcance de los documentos que el agente puede buscar se determina con los permisos del token
- Claude Code puede llamar a la herramienta ``search`` de Fess

.. note::

   El sentido de las llamadas es el inverso al del modo de búsqueda con IA de :doc:`guide-19`.
   En el modo de búsqueda con IA, Fess llama a un LLM (Ollama, OpenAI, etc.) para generar respuestas. Ollama es el entorno de ejecución de ese LLM, no un cliente MCP.
   Con MCP, un agente de IA externo llama a Fess como herramienta de búsqueda, y la respuesta la genera el LLM del lado del agente.

Qué ofrece ``/mcp``
===================

``/mcp`` solo acepta ``POST`` y devuelve un único JSON por solicitud (no mantiene sesiones).
Las búsquedas pasan por el mismo procesamiento que la página de búsqueda, por lo que el filtrado de resultados por rol se aplica tal cual.

El plugin 15.9.0 expone lo siguiente.
Todo es de solo lectura; nada modifica los datos de Fess.

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Nombre
     - Contenido
     - Disponibilidad
   * - ``search`` (herramienta)
     - Búsqueda de texto completo. Cada resultado incluye un ``doc_id``
     - Siempre disponible
   * - ``suggest`` (herramienta)
     - Sugerencias para un término escrito a medias
     - Siempre disponible
   * - ``get_document`` (herramienta)
     - Obtiene el texto de un documento a partir de su ``doc_id``
     - Siempre disponible
   * - ``get_index_stats`` (herramienta)
     - Nombre del índice, número de documentos y uso de memoria de la JVM
     - No disponible con la configuración inicial (véase más adelante)
   * - ``fess://document/{doc_id}`` (recurso)
     - Realiza la misma obtención que ``get_document``, como recurso
     - Siempre disponible
   * - ``fess://index/stats`` (recurso)
     - El mismo contenido que ``get_index_stats``
     - Igual que ``get_index_stats``
   * - ``basic_search`` / ``advanced_search`` (prompt)
     - Plantillas de prompt para búsquedas. ``advanced_search`` también acepta ``sort`` y ``num``
     - Siempre disponible

Si omite ``num`` en ``search``, solo se devuelven 3 resultados (el valor predeterminado de ``mcp.default.page.size``).
Tanto los extractos de ``search`` como el texto de ``get_document`` se truncan a un máximo de 10000 caracteres, y en ``get_document`` ``truncated`` pasa a ``true`` (``mcp.content.max.length``).

Instalación del plugin
======================

La versión del plugin debe coincidir con la versión menor de Fess.
Para Fess 15.9, use ``fess-webapp-mcp`` 15.9.x.
Instálelo con uno de los métodos siguientes y, después, reinicie Fess.

- Consola de administración: en [Sistema] > [Plugin], haga clic en [Instalar], seleccione ``fess-webapp-mcp`` en la pestaña [Remoto] e instálelo
- Línea de comandos: ``bin/fess-setup install plugin fess-webapp-mcp:15.9.0``
- Docker: añada ``FESS_PLUGINS`` a ``environment`` de ``fess01`` en ``compose.yaml``. La imagen de Docker no incluye este plugin

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"

En la versión Docker, si el nombre o la versión son incorrectos, ese plugin se omite y el contenedor arranca igualmente.
Después de añadirlo, compruebe en el registro de arranque que el plugin se ha descargado.

.. warning::

   Al actualizar Fess, sustituya también este plugin por la nueva versión antes de arrancarlo.
   Si el jar de una versión antigua del plugin (por ejemplo, la de 15.8) queda en ``WEB-INF/plugin``, Fess 15.9 no logra inicializarse al arrancar, y no solo ``/mcp`` sino todas las páginas y API devuelven 404.
   Desde la línea de comandos puede sustituirlo con ``bin/fess-setup upgrade plugins``.

Tras el reinicio, si aparece el siguiente WARN en el archivo de registro ``fess.log``, el punto de conexión está habilitado.

::

    [MCP] mcp.auth.mode=none - every /mcp caller is treated as anonymous. Set mcp.auth.mode=fess_token, ...

Este mensaje indica que el punto de conexión funciona sin autenticación, como se describe en la sección siguiente.

Comprobación inicial sin autenticación
======================================

.. warning::

   Justo después de la instalación, ``/mcp`` funciona sin autenticación (``mcp.auth.mode=none``).
   Cualquiera que llegue a ``/mcp`` puede buscar con los mismos privilegios que un usuario que no ha iniciado sesión (invitado), e incluso obtener el texto de los documentos con ``get_document``.
   Quedan expuestos todos los documentos de las configuraciones de rastreo cuyos permisos se han dejado en el valor predeterminado ``{role}guest``.
   Limite las pruebas en este estado a su entorno local y haga obligatoria la autenticación como se explica en la sección siguiente.
   Si "Requiere inicio de sesión" está activado en [Sistema] > [General], ``/mcp`` en este estado rechaza todas las llamadas con HTTP 403. En ese caso, pase a la sección siguiente.

Suponiendo que Fess se ejecuta en ``http://localhost:8080``, llame a ``server/discover``.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: server/discover' \
        -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

La llamada ha tenido éxito si en la respuesta ``result.supportedVersions`` contiene ``2026-07-28`` y ``result.capabilities`` contiene, entre otros, ``tools``.

A continuación, llame a la herramienta ``search``.
Indique en ``q`` una palabra que aparezca en los documentos rastreados.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: tools/call' \
        -H 'Mcp-Name: search' \
        -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search","arguments":{"q":"Fess","num":5},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

Los resultados de búsqueda están en ``result.structuredContent.hits`` y el número de coincidencias en ``total``.
Los valores de las cabeceras deben coincidir con el cuerpo de la solicitud.
``MCP-Protocol-Version`` debe ser igual a la versión de ``params._meta``, ``Mcp-Method`` a ``method`` y ``Mcp-Name`` al nombre de la herramienta.
Si no coinciden, el resultado es HTTP 400 (código de error ``-32020``).

Hacer obligatoria la autenticación
==================================

Cambie al modo ``fess_token``, que autentica con los tokens de acceso de Fess.
También existe el modo ``oauth``, que autentica con JWT emitidos por un servidor de autorización externo.
Para su configuración, consulte la sección "OAuth 2.1 reference" del README.

Crear un token de acceso
------------------------

1. En la consola de administración, abra [Sistema] > [Token de acceso] y haga clic en [Crear nuevo]
2. En "Nombre", introduzca un nombre que indique su uso, como ``mcp-agent``
3. En "Permisos", introduzca los roles de los documentos que el agente puede ver, uno por línea. Si bastan los documentos para invitados, introduzca ``{role}guest`` (cómo elegirlos se explica en "Permisos del token y resultados de búsqueda")
4. Si es necesario, indique "Caduca" y haga clic en [Crear]
5. En la lista, haga clic en el nombre del token creado; su valor se muestra en "Token" en la página de detalles

Configurar mcp.auth.mode
------------------------

Todos los ajustes ``mcp.*`` se leen de las propiedades del sistema de Fess (``system.properties``).
Si los escribe en ``fess_config.properties`` o como ``-Dfess.config.*``, se ignoran sin que aparezca ningún error ni mensaje en el registro.

En la versión ZIP, añada la siguiente línea a ``app/WEB-INF/conf/system.properties``; en las versiones RPM/DEB, a ``/etc/fess/system.properties``.

::

    mcp.auth.mode=fess_token

El valor se vuelve a leer durante la ejecución, por lo que se aplica en pocos segundos y no hace falta reiniciar.

El contenedor ``fess01`` de la versión Docker no tiene volumen, así que los ajustes escritos en archivos dentro del contenedor se pierden al volver a crearlo.
Especifique el ajuste en ``FESS_JAVA_OPTS`` de ``compose.yaml`` con el prefijo ``-Dfess.system.`` (no ``fess.config.``).

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"
      - "FESS_JAVA_OPTS=-Dfess.system.mcp.auth.mode=fess_token"

``FESS_PLUGINS`` y ``FESS_JAVA_OPTS`` se aplican cuando se vuelve a crear el contenedor.
Después de editar ``compose.yaml``, ejecute el siguiente comando.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Si la misma clave existe en ``system.properties``, prevalece ese valor.

Comprobar que la autenticación funciona
---------------------------------------

Vuelva a ejecutar sin cambios la llamada ``server/discover`` de la sección anterior.
Como no se adjunta ningún token, se devuelve HTTP 401 junto con la cabecera ``WWW-Authenticate: Bearer realm="fess-mcp"`` (con ``curl -i`` se muestran las cabeceras).
En el modo ``fess_token``, ``server/discover`` también requiere autenticación.

A continuación, ejecute el ``curl`` de ``search`` de la sección anterior añadiendo ``-H 'Authorization: Bearer <token>'``.
Sustituya ``<token>`` por el valor que aparece en la página de detalles.
Si se devuelven resultados de búsqueda, la configuración ha terminado.
Con un token inexistente o caducado, el resultado es HTTP 401.

Permisos del token y resultados de búsqueda
===========================================

En el modo ``fess_token``, los permisos del token se convierten directamente en los roles de la búsqueda.
No solo ``search``, sino también ``get_document`` se filtra con los mismos roles, de modo que no se pueden obtener documentos sin permiso aunque se conozca su ``doc_id``.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Permisos del token
     - Documentos que se pueden buscar
   * - Vacío
     - Los mismos que un invitado (documentos con ``{role}guest``)
   * - ``{role}guest``
     - Los mismos que un invitado
   * - ``{role}sales``
     - Solo los documentos con ``{role}sales``. No incluye los documentos para invitados
   * - ``{role}sales`` y ``{role}guest``
     - Los documentos de ambos

El rol de invitado solo se añade automáticamente a los tokens con permisos vacíos.
Si quiere que el agente busque tanto en los documentos del departamento como en los destinados a todos, indique también ``{role}guest``.
Para el funcionamiento de roles y permisos, consulte :doc:`guide-05`.

Para comprobarlo, ejecute ``search`` con la misma palabra usando dos tokens con permisos distintos y compare ``total``.

.. warning::

   No asigne ``{role}admin-api`` a un token para agentes.
   Un token con ``{role}admin-api`` puede llamar a toda la Admin API de Fess.
   Además, un ``search`` con un token que solo tiene ``{role}admin-api`` devuelve 0 resultados, porque ningún documento tiene ese rol.

Habilitar ``get_index_stats``
-----------------------------

``get_index_stats`` y ``fess://index/stats`` solo se muestran a los llamantes que tienen alguno de los permisos enumerados en ``mcp.tools.index_stats.permissions``.
El valor predeterminado es ``Radmin-api`` (la notación interna de ``{role}admin-api``) y, en el modo ``none``, ningún llamante tiene permisos, por lo que no se muestran a nadie.
Un llamante sin permiso recibe el mismo error que con una herramienta inexistente.

Para buscar no se necesita esta herramienta.
Si la usa, en lugar de conceder ``{role}admin-api``, defina un rol dedicado y añádalo a los permisos del token.
En ``system.properties`` se escribe con la notación interna (``R`` en lugar de ``{role}``).

::

    mcp.tools.index_stats.permissions=Rmcp-stats

En este ejemplo, añada ``{role}mcp-stats`` a los permisos del token.

Otros ajustes
=============

Todos se escriben en ``system.properties`` (en la versión Docker, ``-Dfess.system.<clave>``).
En los valores booleanos solo ``true`` se considera verdadero; ``1`` o ``yes`` se consideran falsos.

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Clave
     - Valor predeterminado
     - Contenido
   * - ``mcp.allowed.origins``
     - (vacío)
     - Para llamadas desde el navegador, los valores de ``Origin`` permitidos, con el formato ``https://app.example.com`` y separados por comas. Si está vacío, todas las solicitudes con cabecera ``Origin`` se rechazan con HTTP 403. ``curl`` y los agentes de línea de comandos no envían ``Origin``, así que no se ven afectados
   * - ``mcp.rate.limit.per.minute``
     - ``60``
     - Límite por minuto de ``tools/call`` y llamadas similares para cada llamante (el token o, si no lo hay, la dirección IP). Al superarlo se devuelven HTTP 429 y ``Retry-After``. ``0`` lo desactiva
   * - ``mcp.content.max.length``
     - ``10000``
     - Número máximo de caracteres del texto que devuelven ``search`` y ``get_document``
   * - ``mcp.default.page.size``
     - ``3``
     - Número de resultados cuando se omite ``num`` en ``search``
   * - ``mcp.enabled``
     - ``true``
     - Con ``false``, ``/mcp`` devuelve siempre HTTP 503
   * - ``mcp.legacy.protocol.enabled``
     - ``true``
     - Acepta también clientes antiguos (``2025-11-25`` / ``2025-06-18``) que se conectan con ``initialize``

A diferencia de ``mcp.*``, los dos ajustes siguientes pertenecen al ``fess_config.properties`` de Fess (en la versión Docker, ``-Dfess.config.<clave>``).

- Si las llamadas pasan por un proxy inverso en otro host, añada la dirección IP del proxy a ``rate.limit.trusted.proxies`` (valor predeterminado ``127.0.0.1,::1``). Si no lo hace, todos los llamantes que pasan por el proxy comparten el mismo límite
- Para llamadas desde el navegador con otro origen, además de ``mcp.allowed.origins``, añada ``MCP-Protocol-Version``, ``Mcp-Method`` y ``Mcp-Name`` a ``api.cors.allow.headers``. Para más detalles, consulte la sección "Browser clients" del README

Conexión desde agentes de IA
============================

Claude Code
-----------

Claude Code puede conectarse directamente con ``2026-07-28``.
Registre Fess como servidor MCP HTTP con ``claude mcp add`` y pase el token con ``--header``.

::

    $ claude mcp add --transport http fess http://localhost:8080/mcp \
        --header "Authorization: Bearer <token>"

Al ejecutar ``claude mcp list`` se muestra el ``fess`` registrado y también se puede comprobar el estado de la conexión.
Si le pide a Claude Code algo como "Busca en Fess el procedimiento para liquidar los gastos de viaje", el agente llama a la herramienta ``search`` con argumentos como los siguientes y, después, llama a ``get_document`` con el ``doc_id`` de los resultados para leer el texto.

.. code-block:: json

    {
      "name": "search",
      "arguments": {
        "q": "gastos de viaje",
        "num": 5,
        "fields": { "label": ["manual"] }
      }
    }

En ``label`` de ``fields``, indique el valor de una etiqueta de Fess (omítalo si no filtra por etiqueta).
Otros argumentos de ``search`` son, entre otros, ``start`` (paginación), ``sort`` (por ejemplo, ``last_modified.desc``) y ``lang``.

Otros clientes
--------------

Los clientes que se conectan con el protocolo antiguo (``initialize``), como OpenCode, Codex CLI o Gemini CLI, también funcionan siempre que ``mcp.legacy.protocol.enabled`` mantenga su valor predeterminado ``true``.
Los clientes que solo admiten ``2025-03-26`` o versiones anteriores no pueden conectarse.
Los clientes de escritorio que solo pueden iniciar servidores MCP por stdio pasan por ``mcp-remote``, que hace de intermediario entre stdio y HTTP.
La compatibilidad de cada cliente se resume en la sección "Client compatibility" del README.

Cuidado con el envío de resultados de búsqueda al exterior
----------------------------------------------------------

Si el LLM que usa el agente es un servicio en la nube, los extractos de ``search`` y el texto de ``get_document`` se envían a ese servicio.
Para acotar lo que se envía, seleccione con los permisos del token solo los documentos que se pueden enviar y, si es necesario, reduzca ``mcp.content.max.length``.

Solución de problemas
=====================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Síntoma
     - Causa y solución
   * - HTTP 400, código de error ``-32020``
     - Falta ``MCP-Protocol-Version``, ``Mcp-Method`` o ``Mcp-Name``, o no coincide con el cuerpo de la solicitud
   * - HTTP 401
     - En el modo ``fess_token``, el token falta, no existe o ha caducado
   * - Todas las solicitudes devuelven HTTP 403
     - La cabecera ``Origin`` no está en ``mcp.allowed.origins``. O bien, en el modo ``none``, está activado "Requiere inicio de sesión"
   * - La primera llamada falla con ``-32601`` y menciona ``initialize``
     - Es un cliente antiguo y ``mcp.legacy.protocol.enabled`` no es ``true``
   * - ``search`` devuelve 0 resultados
     - Los permisos del token no incluyen los roles de los documentos. Si ``partial`` es ``true`` en el resultado, la búsqueda no se completó (tiempo de espera agotado o fallo de OpenSearch), así que no significa necesariamente que no haya coincidencias
   * - ``Tool execution failed (error_code:...)``
     - La causa se registra como WARN en ``fess.log``. Busque en el registro el valor de ``error_code``

Artículos relacionados
======================

- Separar por rol los documentos que se muestran a través de MCP: :doc:`guide-05`
- Que el propio Fess responda con un LLM: :doc:`guide-19`
- Encontrar documentos de significado similar aunque no coincidan las palabras clave: :doc:`guide-18`
- Usar la API de búsqueda desde sistemas de negocio o separar los tokens de acceso según el uso: :doc:`guide-11`
- Configurar de forma conjunta el SSO y la protección de acceso: :doc:`guide-15`

Referencias
===========

- `fess-webapp-mcp README (15.9.0) <https://github.com/codelibs/fess-webapp-mcp/blob/fess-webapp-mcp-15.9.0/README.md>`__
- `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `Token de Acceso <https://fess.codelibs.org/es/stable/admin/accesstoken-guide.html>`__
- `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__
- `Model Context Protocol <https://modelcontextprotocol.io/>`__
