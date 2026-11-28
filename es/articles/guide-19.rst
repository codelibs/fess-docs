===================================================
Consultar documentos internos con búsqueda IA (RAG)
===================================================

Introducción
============

En lugar de abrir los resultados de búsqueda uno por uno y compararlos, a menudo se desea hacer una pregunta como "¿Cuál es la fecha límite para presentar los gastos?" y recibir una respuesta basada en los documentos internos.
El modo de búsqueda IA de Fess (chat RAG) hace que el propio Fess busque los documentos relacionados con la pregunta, entrega su contenido a un LLM (modelo de lenguaje de gran tamaño) para que genere una respuesta y la devuelve junto con enlaces a los documentos en los que se basa.

En este artículo se explica cómo poner en marcha el modo de búsqueda IA en Fess 15.9, cómo limitar quién puede usarlo y qué documentos consulta, y cómo comprobar su funcionamiento en la página de búsqueda y a través de la API.
Al terminar los pasos de este artículo, podrá:

- Elegir uno de los cuatro proveedores de LLM e instalar el plugin y la configuración correspondientes
- Conectar un LLM a Fess en Docker con los archivos Compose de superposición que proporciona docker-fess
- Limitar qué usuarios pueden usar el chat y en qué documentos se basan las respuestas
- Comprobar que funciona en la página de búsqueda, a través de ``/api/v2/chat`` y en el registro de búsqueda

Como requisito previo, Fess debe estar en ejecución y debe haber documentos ya rastreados.
Si no es así, prepárelo siguiendo los pasos de :doc:`guide-02`.
La búsqueda semántica, que encuentra documentos de significado similar, se trata en :doc:`guide-18`, y MCP, que permite a agentes de IA buscar en Fess, en :doc:`guide-20`.

Cómo funciona el modo de búsqueda IA
====================================

El modo de búsqueda IA no utiliza un índice vectorial dedicado.
Encuentra los documentos con el mismo procesamiento que la búsqueda habitual (búsqueda por palabras clave de forma predeterminada), por lo que puede empezar sin preparar un modelo de embeddings ni la división en fragmentos.
Si la búsqueda semántica está habilitada, se incorpora automáticamente también a las búsquedas del modo de búsqueda IA.

El flujo del procesamiento depende del endpoint al que se llame.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Endpoint
     - Flujo del procesamiento
   * - ``POST /api/v2/chat/stream`` (el que usa la búsqueda IA de la página de búsqueda)
     - Detección de la intención → búsqueda → evaluación de la relevancia por el LLM → obtención del contenido de los documentos → generación de la respuesta. El progreso de cada etapa y los fragmentos de la respuesta se devuelven en orden como Server-Sent Events
   * - ``POST /api/v2/chat``
     - Detección de la intención → búsqueda → generación de la respuesta. No hay evaluación de la relevancia y el resultado se devuelve en un único JSON

En ambos casos, cuando una búsqueda no devuelve resultados, el LLM reformula los términos de búsqueda y vuelve a buscar (hasta 2 veces de forma predeterminada, ``rag.chat.query.regeneration.max.count``).
Como una sola pregunta llama al LLM varias veces, las respuestas tardan más que una búsqueda normal y, con un LLM en la nube, cada llamada tiene un coste.

Al LLM se envían la pregunta del usuario y el contenido o fragmentos de los documentos encontrados en la búsqueda.
Al elegir un proveedor, compruebe a dónde se envían estos datos.

Las conversaciones se identifican mediante ``session_id`` y se guardan en la memoria de Fess.
De forma predeterminada, una conversación se descarta tras 30 minutos de inactividad (``rag.chat.session.timeout.minutes``), y cada conversación conserva hasta 30 mensajes (``rag.chat.history.max.messages``).
Las conversaciones también se pierden al reiniciar Fess.

Elegir un proveedor de LLM
==========================

En Fess 15.9, la conexión con un LLM la proporciona un plugin ``fess-llm-*`` para cada proveedor.
El proveedor que se usa se indica con ``rag.llm.name``.

.. list-table::
   :header-rows: 1
   :widths: 14 12 18 22 34

   * - Proveedor
     - ``rag.llm.name``
     - Plugin
     - Modelo predeterminado
     - Configuración necesaria para conectarse y destino de las preguntas y los documentos
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ``gemma4:e4b``
     - ``rag.llm.ollama.api.url`` (predeterminado ``http://localhost:11434``). Los datos se envían al servidor Ollama que usted mismo opera
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - ``gpt-5-mini``
     - ``rag.llm.openai.api.key``. Los datos se envían a OpenAI
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - ``gemini-3.1-flash-lite-preview``
     - ``rag.llm.gemini.api.key``. Los datos se envían a Google
   * - Amazon Bedrock
     - ``bedrock``
     - ``fess-llm-bedrock``
     - ``us.amazon.nova-2-lite-v1:0``
     - ``rag.llm.bedrock.region`` (predeterminado ``us-east-1``), y ``rag.llm.bedrock.api.key`` o credenciales de AWS. Los datos se envían a Amazon Bedrock en la región indicada

El modelo se puede cambiar con ``rag.llm.<proveedor>.model``.

Con OpenAI y Gemini basta con una clave de API para empezar, pero las preguntas y los documentos se envían al servicio correspondiente.
Ollama no saca las preguntas ni los documentos de sus propios servidores, pero necesita un servidor que ejecute el modelo.
El archivo Compose de docker-fess para Ollama presupone una GPU de NVIDIA.
Bedrock requiere credenciales de AWS y la configuración de una región.
Para la configuración, consulte `Configuración de Amazon Bedrock <https://fess.codelibs.org/es/stable/config/llm-bedrock.html>`__.

Tres elementos que configurar
=============================

El modo de búsqueda IA solo funciona cuando se cumplen los tres elementos siguientes.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Configuración
     - Dónde se establece
     - Cómo se pasa en Docker
   * - ``rag.chat.enabled=true`` (predeterminado ``false``)
     - ``fess_config.properties``. La consola de administración no tiene ningún campo para ello
     - ``-Dfess.config.rag.chat.enabled=true`` en ``FESS_JAVA_OPTS``
   * - Un plugin ``fess-llm-*``
     - [Sistema] > [Plugin], o ``bin/fess-setup``
     - ``FESS_PLUGINS=fess-llm-openai:15.9.0``, etc.
   * - ``rag.llm.name`` y la configuración de conexión de cada proveedor
     - ``rag.llm.name`` en [Sistema] > [General]; la configuración de conexión (``rag.llm.<proveedor>.*``) en ``fess_config.properties``
     - ``-Dfess.system.rag.llm.name=openai``, ``-Dfess.config.rag.llm.openai.api.key=...``, etc.

El valor predeterminado de ``rag.llm.name`` es ``ollama``.
Si instala solo el plugin de OpenAI y no cambia ``rag.llm.name``, Fess sigue buscando un cliente de Ollama que no existe y el modo de búsqueda IA no se puede usar.
En ese caso, aparece en el registro la advertencia ``[LLM] LlmClient not found. componentName=ollamaLlmClient``.

``-Dfess.system.rag.llm.name`` es un valor inicial que solo se usa cuando ``system.properties`` no contiene ningún valor.
En cuanto un valor guardado en [General] se escribe en ``system.properties``, ese valor tiene prioridad.

Ejecutar en Docker (OpenAI y Gemini)
====================================

docker-fess incluye archivos Compose de superposición para conectar un LLM.
En el directorio donde colocó los archivos Compose en :doc:`guide-02`, descargue el archivo de la v15.9.0.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-openai.yaml

Guarde la clave de API en una variable de entorno del shell e inicie indicando los tres archivos.

::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` añade las siguientes variables de entorno a ``fess01``.
La clave de API y el nombre del modelo se toman de ``OPENAI_API_KEY`` y ``OPENAI_MODEL`` del shell (``gpt-5-mini`` si no está definida), por lo que no es necesario escribir la clave en el archivo.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Los plugins de ``FESS_PLUGINS`` se instalan al iniciar el contenedor, antes que el propio Fess, así que no hace falta reiniciar por separado.
Si ``fess01`` ya está en ejecución, este comando vuelve a crear ``fess01`` y la configuración que había cambiado en [General] se pierde junto con el contenedor.
Indique también los mismos tres archivos en los comandos posteriores, como ``ps``, ``logs`` y ``down``.

Para Gemini, descargue ``compose-gemini.yaml``, defina ``GEMINI_API_KEY`` e indíquelo de la misma forma como tercer archivo.
Este archivo establece el modelo a partir de ``GEMINI_MODEL`` (``gemini-2.5-flash`` si no está definida), por lo que se usa ``gemini-2.5-flash`` en lugar del modelo predeterminado del plugin.

.. note::

   Si indica dos o más archivos de superposición que definen ``FESS_JAVA_OPTS`` (por ejemplo, al combinarlos con la configuración para OCR), solo se usa el valor del último archivo.
   En ese caso, prepare su propio archivo Compose que reúna todas las opciones ``-D`` necesarias en un único ``FESS_JAVA_OPTS``.
   ``FESS_JAVA_OPTS`` se divide por los espacios, por lo que no se pueden escribir opciones cuyo valor contenga espacios.

Una clave de API pasada como en ``-Dfess.config.rag.llm.openai.api.key`` se muestra enmascarada en [Información del sistema] > [Información de configuración].
Si necesita salir al exterior a través de un proxy interno, añada ``-Dfess.config.http.proxy.host=...`` y ``-Dfess.config.http.proxy.port=...``.
Los plugins de LLM usan la configuración de proxy común de Fess.

Ejecutar en Docker (Ollama)
===========================

``compose-ollama.yaml`` añade un contenedor de Ollama, ``ollama01``, y conecta ``fess01`` a él.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Destino
     - Qué se configura
   * - ``fess01``
     - ``FESS_PLUGINS=fess-llm-ollama:15.9.0``, ``-Dfess.config.rag.chat.enabled=true``, ``-Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434``
   * - ``ollama01``
     - Imagen ``ollama/ollama:latest``, red ``search_net``, puerto 11434, volumen ``ollama-data`` y asignación de una GPU de NVIDIA

``rag.llm.name`` y el modelo no se configuran, por lo que se usan los valores predeterminados ``ollama`` y ``gemma4:e4b``.
La URL apunta a ``ollama01`` porque el valor predeterminado ``http://localhost:11434`` haría referencia al propio contenedor ``fess01``.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-ollama.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gemma4:e4b

Para usar este archivo se necesita un entorno con NVIDIA Container Toolkit instalado.
Para probarlo en un entorno sin GPU, elimine la sección ``deploy:`` de ``ollama01`` en el archivo descargado.
El modelo se ejecutará en la CPU, por lo que las respuestas tardarán.

Fess solo considera que Ollama está disponible cuando el modelo configurado figura en la lista de modelos de Ollama (``/api/tags``), y hace esta comprobación cada 60 segundos de forma predeterminada.
Por eso, el modo de búsqueda IA pasa a estar disponible aproximadamente un minuto después de descargar el modelo.
Los comentarios al principio del archivo mencionan otro nombre de archivo y los pasos para descargar ``gpt-oss:20b``, pero siga los pasos anteriores.
Para usar otro modelo, descárguelo con ``ollama pull`` y añada ``-Dfess.config.rag.llm.ollama.model=<nombre-del-modelo>`` a ``FESS_JAVA_OPTS``.

Configurar sin Docker (ZIP, RPM y DEB)
======================================

1. Instale el plugin. Selecciónelo en [Sistema] > [Plugin] > [Instalar] o instálelo con un comando

   ::

       $ bin/fess-setup install plugin fess-llm-openai:15.9.0

2. Añada la configuración a ``fess_config.properties``. Es ``app/WEB-INF/classes/fess_config.properties`` en el paquete ZIP y ``/etc/fess/fess_config.properties`` en los paquetes RPM/DEB

   ::

       rag.chat.enabled=true
       rag.llm.openai.api.key=sk-...
       rag.llm.openai.model=gpt-5-mini

3. Reinicie Fess. Tanto el plugin como los cambios en ``fess_config.properties`` se cargan al reiniciar
4. Abra [Sistema] > [General], seleccione ``openai`` en "Proveedor de LLM" de la sección "Búsqueda IA" y haga clic en [Actualizar]

La sección "Búsqueda IA" solo se muestra cuando ``rag.chat.enabled=true`` está definido y hay al menos un plugin de LLM cargado.
Las opciones de "Proveedor de LLM" se limitan a los proveedores de los plugins instalados.
Si no encuentra la sección, revise los pasos 1 a 3.

Comprobar el funcionamiento
===========================

Comprobar en la página de búsqueda
----------------------------------

1. Abra ``http://localhost:8080/``. En la barra de navegación superior aparece [Búsqueda IA] con un icono de robot
2. Haga clic en [Búsqueda IA] para abrir la página de chat (``/chat``)
3. Escriba una pregunta que los documentos rastreados probablemente puedan responder. Si rastreó la Guía de búsqueda en :doc:`guide-02`, puede probar con algo como "¿Qué caracteres puedo usar en la búsqueda con comodines?"

Mientras se genera la respuesta, se muestran en orden las etapas Analizar, Buscar, Evaluar, Obtener y Responder.
Debajo de la respuesta, los documentos en los que se basa aparecen numerados en "Fuentes", y esos números corresponden a referencias como ``[1]`` en el texto de la respuesta.
Para cambiar de tema, haga clic en [Nueva conversación]; el historial de la conversación se borra.

Si [Búsqueda IA] no aparece, revise la sección "Problemas frecuentes" más adelante.

Comprobar a través de la API
----------------------------

Para comprobarlo sin usar la página, llame a ``/api/v2/ui/config``.
Si ``response.features.rag_chat_enabled`` es ``true``, ese usuario puede usar el modo de búsqueda IA.

Las solicitudes que cambian el estado, como ``/api/v2/chat``, deben enviar un token CSRF vinculado a la sesión en el encabezado ``X-Fess-CSRF-Token``.
La respuesta de ``/api/v2/ui/config`` contiene el token, así que obténgalo guardando las cookies y haga la llamada con las mismas cookies (el ejemplo usa ``jq``).

::

    $ curl -s -c cookies.txt http://localhost:8080/api/v2/ui/config > ui-config.json
    $ jq '.response.features.rag_chat_enabled' ui-config.json
    true
    $ TOKEN=$(jq -r '.response.csrf_token' ui-config.json)
    $ curl -s -b cookies.txt -X POST http://localhost:8080/api/v2/chat \
        -H 'Content-Type: application/json' \
        -H "X-Fess-CSRF-Token: $TOKEN" \
        -d '{"message":"¿Qué caracteres puedo usar en la búsqueda con comodines?"}' | jq '.response'

En la respuesta, ``content`` es la respuesta, ``sources`` son los documentos en los que se basa (``rank``, ``title``, ``url``, etc.) y ``session_id`` es el ID de la conversación.
Para hacer una pregunta de seguimiento, devuelva el ``session_id``, por ejemplo ``{"message":"...","session_id":"<session_id anterior>"}``.

Este ejemplo llama a la API como un usuario anónimo que no ha iniciado sesión, por lo que solo se buscan los documentos que tienen ``{role}guest``.
Para saber cómo llamarla como usuario que ha iniciado sesión, qué eventos devuelve la versión en streaming ``/api/v2/chat/stream`` y cuáles son los códigos de error, consulte `Chat API <https://fess.codelibs.org/es/stable/api/api-chat.html>`__ y `Descripción general de la API <https://fess.codelibs.org/es/stable/api/api-overview.html>`__.
``/api/v1/chat`` es una API de formato antiguo que solo está disponible si se instala el plugin ``fess-webapp-v1-api``.
Para integraciones nuevas, use ``/api/v2/chat``.

Comprobar en la consola de administración y en los registros
------------------------------------------------------------

La pestaña [Chat con IA] de [Información del sistema] > [Registro de búsqueda] muestra el número de solicitudes, el número de usuarios, el total de tokens, el tiempo medio de respuesta y la tasa de errores, además de los recuentos por usuario, por intención y por modelo.
Este registro está habilitado mediante ``rag.chat.log.enabled`` (predeterminado ``true``), y el texto de las preguntas y respuestas no se guarda.
El número de tokens solo se registra cuando el plugin de LLM lo informa.

En Docker, puede comprobar en el registro del contenedor si el plugin se instaló.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml logs fess01 | grep -E 'Installing|\[LLM\]'

Si aparece ``Installing fess-llm-openai-15.9.0.jar``, el plugin está instalado.
Si a continuación aparece repetidamente ``[LLM] LlmClient not found``, ``rag.llm.name`` no coincide con el plugin instalado.

Limitar los usuarios y los documentos consultados
=================================================

Las búsquedas del modo de búsqueda IA se filtran por rol igual que la búsqueda habitual.
Los documentos que un usuario no puede ver en los resultados de búsqueda no se usan ni como base de las respuestas ni como fuentes.
Qué documentos ve cada usuario lo determinan los "Permisos" de la configuración de rastreo.
Para el enfoque de diseño, consulte :doc:`guide-05`.

Además, en la sección "Búsqueda IA" de [Sistema] > [General] puede limitar quién puede usar el propio chat.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Descripción
   * - "Permisos del chat" (``rag.chat.permissions``)
     - Indica los usuarios que pueden usar el chat como una lista separada por comas, por ejemplo ``{role}rag_user,{group}sales,{user}taro``. Si está vacío, todos pueden usarlo. Para que también puedan usarlo los usuarios que no han iniciado sesión, incluya ``{role}guest``
   * - "Etiquetas del chat" (``rag.chat.labels``)
     - Limita los documentos en los que se basan las respuestas a los que tienen alguno de los valores de etiqueta indicados. Indíquelos como una lista separada por comas, por ejemplo ``faq,policy``; si está vacío, se usan todos los documentos que el usuario puede ver

Los usuarios no incluidos en "Permisos del chat" no ven [Búsqueda IA], y la API devuelve 401 si no han iniciado sesión o 403 si la han iniciado.
Los usuarios que han iniciado sesión no tienen ``{role}guest``, así que si indica solo ``{role}guest``, esos usuarios dejan de poder usar el chat.
Si guarda un valor sin ninguna entrada válida (por ejemplo, solo ``{role}``), nadie podrá usar el chat.

"Etiquetas del chat" sirve cuando quiere que las respuestas provengan solo de documentos fiables como base, por ejemplo los reglamentos internos y las preguntas frecuentes, a los que ha asignado previamente una etiqueta.
Para crear y asignar etiquetas, consulte :doc:`guide-04`.

Problemas frecuentes
====================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Síntoma
     - Qué comprobar
   * - [Búsqueda IA] no aparece
     - Compruebe en este orden. (1) ¿Se pasa ``rag.chat.enabled=true``? (2) ¿Está instalado el plugin (``Installing`` en el registro)? (3) ¿Coincide ``rag.llm.name`` con el plugin instalado (advertencia ``LlmClient not found``)? (4) ¿La clave de API no está vacía y, en Ollama, se ha descargado el modelo? (5) ¿Ha quedado usted fuera de "Permisos del chat"?
   * - No existe la sección "Búsqueda IA" en [General]
     - O bien ``rag.chat.enabled`` sigue en ``false``, o bien no hay ningún plugin de LLM cargado. Compruebe que reinició Fess después de definir la configuración e instalar el plugin
   * - "Proveedor de LLM" volvió a su valor anterior tras ``down`` y ``up -d``
     - Los valores de [General] se guardan en ``system.properties`` dentro del contenedor ``fess01``, por lo que se pierden al volver a crear el contenedor. Indíquelo con ``-Dfess.system.rag.llm.name`` en ``FESS_JAVA_OPTS``
   * - La API devuelve ``403``
     - Compruebe que envía el token CSRF en ``X-Fess-CSRF-Token`` y que envía las cookies obtenidas al conseguir el token. Un usuario que ha iniciado sesión y no está incluido en "Permisos del chat" también recibe 403
   * - La API devuelve ``429``
     - Cada usuario tiene un límite de 30 solicitudes por minuto (``api.chat.rate.limit.per.user.per.minute``)
   * - No se puede conectar con un LLM en la nube
     - Compruebe que el contenedor puede acceder al exterior y, si se necesita un proxy, defina ``http.proxy.host`` y ``http.proxy.port``

Para mejorar la calidad de las respuestas, compruebe primero la calidad de la búsqueda.
El modo de búsqueda IA se basa en los documentos mejor clasificados de una búsqueda normal (5 de forma predeterminada, ``rag.chat.context.max.documents``), así que si al buscar con las palabras de la pregunta aparecen arriba documentos que no tienen relación, la respuesta también se verá arrastrada por ellos.
La mejora de la búsqueda se trata en :doc:`guide-08`.
Para la temperatura y el número máximo de tokens por tipo de prompt, y para sustituir los prompts, consulte `Descripción general de la búsqueda IA (RAG) y la integración LLM <https://fess.codelibs.org/es/stable/config/llm-overview.html>`__.

Artículos recomendados
======================

- Añadir a los resultados documentos de significado similar aunque las palabras clave no coincidan: :doc:`guide-18`
- Permitir que agentes de IA como Claude busquen en Fess: :doc:`guide-20`
- Separar los documentos que se pueden buscar según el departamento o el rol: :doc:`guide-05`
- Mejorar la calidad de la búsqueda a partir del registro de búsqueda: :doc:`guide-08`
- Hacer que los usuarios inicien sesión con SSO y mostrar documentos distintos a cada uno: :doc:`guide-15`

Referencias
===========

- `Configuración de la funcionalidad de modo de búsqueda IA <https://fess.codelibs.org/es/stable/config/rag-chat.html>`__
- `Descripción general de la búsqueda IA (RAG) y la integración LLM <https://fess.codelibs.org/es/stable/config/llm-overview.html>`__
- `Configuración de Ollama <https://fess.codelibs.org/es/stable/config/llm-ollama.html>`__
- `Configuración de OpenAI <https://fess.codelibs.org/es/stable/config/llm-openai.html>`__
- `Configuración de Google Gemini <https://fess.codelibs.org/es/stable/config/llm-gemini.html>`__
- `Configuración de Amazon Bedrock <https://fess.codelibs.org/es/stable/config/llm-bedrock.html>`__
- `Chat API <https://fess.codelibs.org/es/stable/api/api-chat.html>`__
- `Modo de búsqueda IA (para usuarios) <https://fess.codelibs.org/es/stable/user/chat-search.html>`__
- `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `Directorio compose de docker-fess (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
