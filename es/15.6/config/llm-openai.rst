==========================
Configuracion de OpenAI
==========================

Descripcion general
===================

OpenAI es un servicio en la nube que proporciona modelos de lenguaje grandes (LLM) de alto rendimiento, comenzando con GPT-4.
|Fess| puede utilizar la API de OpenAI para implementar la funcionalidad de modo de búsqueda IA.

Al usar OpenAI, es posible generar respuestas de alta calidad con modelos de IA de ultima generacion.

Caracteristicas principales
---------------------------

- **Respuestas de alta calidad**: Generacion de respuestas de alta precision con modelos GPT de ultima generacion
- **Escalabilidad**: Facil escalado al ser un servicio en la nube
- **Mejora continua**: El rendimiento mejora con actualizaciones periodicas de modelos
- **Funcionalidad rica**: Compatible con diversas tareas como generacion de texto, resumen, traduccion

Modelos compatibles
-------------------

Principales modelos disponibles en OpenAI:

- ``gpt-5`` - Ultimo modelo de alto rendimiento
- ``gpt-5-mini`` - Version ligera de GPT-5 (buena relacion costo-rendimiento)
- ``gpt-4o`` - Modelo multimodal de alto rendimiento
- ``gpt-4o-mini`` - Version ligera de GPT-4o
- ``o3-mini`` - Modelo ligero especializado en razonamiento
- ``o4-mini`` - Modelo ligero de proxima generacion especializado en razonamiento

.. note::
   Para la informacion mas reciente sobre modelos disponibles, consulte `OpenAI Models <https://platform.openai.com/docs/models>`__.

.. note::
   Al usar modelos de la serie o1/o3/o4 o de la serie gpt-5, |Fess| utiliza automaticamente el parametro ``max_completion_tokens`` de la API de OpenAI. No se requieren cambios de configuracion.

Requisitos previos
==================

Antes de usar OpenAI, prepare lo siguiente.

1. **Cuenta de OpenAI**: Cree una cuenta en `https://platform.openai.com/ <https://platform.openai.com/>`__
2. **Clave API**: Genere una clave API en el dashboard de OpenAI
3. **Configuracion de facturacion**: Configure la informacion de facturacion ya que el uso de la API genera cargos

Obtencion de clave API
----------------------

1. Inicie sesion en `OpenAI Platform <https://platform.openai.com/>`__
2. Navegue a la seccion "API keys"
3. Haga clic en "Create new secret key"
4. Ingrese un nombre para la clave y creela
5. Guarde la clave mostrada de forma segura (solo se muestra una vez)

.. warning::
   La clave API es informacion confidencial. Tenga en cuenta lo siguiente:

   - No la commita en sistemas de control de versiones
   - No la imprima en logs
   - Administrela con variables de entorno o archivos de configuracion seguros

Instalacion del plugin
======================

En |Fess| 15.6, la funcionalidad de integracion con OpenAI se proporciona como plugin. Para usarla es necesario instalar el plugin ``fess-llm-openai``.

1. Descargue `fess-llm-openai-15.6.0.jar`
2. Coloque el archivo JAR en el directorio ``app/WEB-INF/plugin/`` del directorio de instalacion de |Fess|::

    cp fess-llm-openai-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Reinicie |Fess|

.. note::
   La version del plugin debe coincidir con la version de |Fess|.

Configuracion basica
====================

En |Fess| 15.6, los elementos de configuracion se dividen en los siguientes dos archivos segun su uso.

- ``app/WEB-INF/conf/fess_config.properties`` - Configuracion del nucleo de |Fess| y configuracion especifica del proveedor LLM
- ``system.properties`` / Pantalla de administracion (Administracion > Sistema > General) - Seleccion del proveedor LLM (``rag.llm.name``)

Configuracion minima
--------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # Clave API de OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelo a usar
    rag.llm.openai.model=gpt-5-mini

``system.properties`` (tambien configurable en Administracion > Sistema > General):

::

    # Configurar el proveedor LLM como OpenAI
    rag.llm.name=openai

Configuracion recomendada (entorno de produccion)
-------------------------------------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # Clave API de OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuracion del modelo (usar modelo de alto rendimiento)
    rag.llm.openai.model=gpt-4o

    # Endpoint de API (normalmente no necesita cambios)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Configuracion de timeout
    rag.llm.openai.timeout=120000

    # Limite de solicitudes simultaneas
    rag.llm.openai.max.concurrent.requests=5

``system.properties`` (tambien configurable en Administracion > Sistema > General):

::

    # Configuracion del proveedor LLM
    rag.llm.name=openai

Elementos de configuracion
==========================

Todos los elementos de configuracion disponibles para el cliente de OpenAI. Excepto ``rag.llm.name``, todos se configuran en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - Propiedad
     - Descripcion
     - Predeterminado
     - Lugar de configuracion
   * - ``rag.llm.name``
     - Nombre del proveedor LLM (especificar ``openai``)
     - ``ollama``
     - system.properties
   * - ``rag.llm.openai.api.key``
     - Clave API de OpenAI
     - (requerido)
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - Nombre del modelo a usar
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - URL base de la API
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - Timeout de solicitud (milisegundos)
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - Intervalo de verificacion de disponibilidad (segundos)
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - Numero maximo de solicitudes simultaneas
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - Numero maximo de documentos relevantes en la evaluacion
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - Timeout de espera de solicitudes simultaneas (ms)
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - Multiplicador de max tokens para modelos de inferencia
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.retry.max``
     - Numero maximo de reintentos HTTP (en errores ``429`` y de la familia ``5xx``)
     - ``10``
     - fess_config.properties
   * - ``rag.llm.openai.retry.base.delay.ms``
     - Retardo base del backoff exponencial (milisegundos)
     - ``2000``
     - fess_config.properties
   * - ``rag.llm.openai.stream.include.usage``
     - Envia ``stream_options.include_usage=true`` durante el streaming para recibir la informacion de tokens utilizados en el chunk final
     - ``true``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - Maximo de caracteres para historial de conversacion
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - Maximo de mensajes de historial para deteccion de intencion
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - Maximo de caracteres de historial para deteccion de intencion
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - Maximo de caracteres para mensajes del asistente
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - Maximo de caracteres para resumen del asistente
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - Maximo de caracteres para descripcion de documentos en evaluacion
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - Habilitacion de la funcionalidad de modo de búsqueda IA
     - ``false``
     - fess_config.properties

Configuracion por tipo de prompt
=================================

En |Fess|, se pueden configurar parametros individuales para cada tipo de prompt. La configuracion se realiza en ``fess_config.properties``.

Patron de configuracion
------------------------

La configuracion por tipo de prompt se especifica con el siguiente patron:

- ``rag.llm.openai.{promptType}.temperature`` - Aleatoriedad de generacion (0.0 a 2.0). Se ignora para modelos de inferencia (serie o1/o3/o4/gpt-5)
- ``rag.llm.openai.{promptType}.max.tokens`` - Numero maximo de tokens
- ``rag.llm.openai.{promptType}.context.max.chars`` - Numero maximo de caracteres del contexto (predeterminado: ``16000`` para answer/summary, ``10000`` para otros)

Tipos de prompt
---------------

Tipos de prompt disponibles:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tipo de prompt
     - Descripcion
   * - ``intent``
     - Prompt para determinar la intencion del usuario
   * - ``evaluation``
     - Prompt para evaluar la relevancia de los resultados de busqueda
   * - ``unclear``
     - Prompt de respuesta para consultas no claras
   * - ``noresults``
     - Prompt de respuesta cuando no hay resultados de busqueda
   * - ``docnotfound``
     - Prompt de respuesta cuando no se encuentra el documento
   * - ``answer``
     - Prompt para generar respuestas
   * - ``summary``
     - Prompt para generar resumenes
   * - ``faq``
     - Prompt para generar FAQ
   * - ``direct``
     - Prompt para respuesta directa
   * - ``queryregeneration``
     - Prompt de regeneracion de consultas

Valores predeterminados
-----------------------

Valores predeterminados para cada tipo de prompt. La configuracion de temperature se ignora para modelos de inferencia (serie o1/o3/o4/gpt-5).

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Tipo de prompt
     - Temperature
     - Max Tokens
     - Notas
   * - ``intent``
     - 0.1
     - 256
     - Deteccion de intencion determinista
   * - ``evaluation``
     - 0.1
     - 256
     - Evaluacion de relevancia determinista
   * - ``unclear``
     - 0.7
     - 512
     -
   * - ``noresults``
     - 0.7
     - 512
     -
   * - ``docnotfound``
     - 0.7
     - 256
     -
   * - ``direct``
     - 0.7
     - 1024
     -
   * - ``faq``
     - 0.7
     - 1024
     -
   * - ``answer``
     - 0.5
     - 2048
     - Generacion de respuesta principal
   * - ``summary``
     - 0.3
     - 2048
     - Generacion de resumen
   * - ``queryregeneration``
     - 0.3
     - 256
     - Regeneracion de consultas

Ejemplo de configuracion
------------------------

::

    # Configuracion de temperatura del prompt answer
    rag.llm.openai.answer.temperature=0.7

    # Numero maximo de tokens del prompt answer
    rag.llm.openai.answer.max.tokens=2048

    # Configuracion de temperatura del prompt summary (se configura bajo para resumen)
    rag.llm.openai.summary.temperature=0.3

    # Configuracion de temperatura del prompt intent (se configura bajo para determinacion de intencion)
    rag.llm.openai.intent.temperature=0.1

Comportamiento de reintentos
============================

Las solicitudes a la API de OpenAI se reintentan automaticamente para los siguientes codigos de estado HTTP:

- ``429`` Too Many Requests (limite de tasa)
- ``500`` Internal Server Error
- ``502`` Bad Gateway (OpenAI puede devolverlo cuando el upstream esta sobrecargado)
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Durante los reintentos se aplica un backoff exponencial (valor base ``rag.llm.openai.retry.base.delay.ms`` milisegundos, hasta ``rag.llm.openai.retry.max`` intentos, con jitter de +/-20%).
Si el servidor devuelve un encabezado ``Retry-After`` (segundos enteros, limitado a ``600`` segundos como maximo), ese valor tiene prioridad sobre el backoff exponencial. Esto sigue la guia oficial de OpenAI.

Tenga en cuenta que las ``IOException`` (timeouts de conexion, reset de socket, fallos de DNS) no se reintentan, ya que la solicitud podria haber llegado al servidor y un reintento podria provocar un cobro doble.
En las solicitudes de streaming, solo la conexion inicial es objeto de reintentos; los errores que ocurren despues de comenzar a recibir el cuerpo de la respuesta se propagan inmediatamente.

.. note::
   Con la configuracion predeterminada (maximo 10 intentos, base 2 segundos), en el peor caso la suma de los 9 backoffs es ``2 + 4 + 8 + ... + 512 = aproximadamente 1022 segundos (aproximadamente 17 minutos)``. Si ``Retry-After`` (maximo 600 segundos) se devuelve en cada intento, el peor caso puede llegar a ``9 x 600 segundos = 90 minutos``. Si desea controlar la latencia de forma mas estricta, reduzca ``rag.llm.openai.retry.max``.

Streaming e informacion de uso
==============================

Por defecto, se incluye ``stream_options.include_usage=true`` en las solicitudes y, en el chunk SSE final de la respuesta de streaming, se recibe el objeto ``usage`` (que incluye ``completion_tokens_details.reasoning_tokens`` para los modelos de inferencia y ``prompt_tokens_details.cached_tokens`` cuando se utiliza la cache de prompts).

Si utiliza un backend que no admite el campo ``stream_options.include_usage`` (como vLLM o gateways compatibles con Azure OpenAI), desactivelo de la siguiente forma::

    rag.llm.openai.stream.include.usage=false

Salida de logs y deteccion de anomalias
=======================================

Desde |Fess| 15.6.1, el cliente de OpenAI emite los siguientes logs estructurados, que permiten supervisar el uso de tokens y las anomalias de respuesta sin necesidad de habilitar el nivel ``DEBUG``.

- ``[LLM:OPENAI] Stream completed.`` (INFO) - Al finalizar la respuesta de streaming, emite el numero de chunks, el tiempo hasta el primer chunk y la informacion de uso de tokens
- ``[LLM:OPENAI] Chat response received.`` (INFO) - Al finalizar la respuesta no-streaming, emite informacion equivalente
- ``[LLM:OPENAI] Chat finished abnormally`` / ``Stream finished abnormally`` (WARN) - Cuando ``finish_reason`` es distinto de ``stop`` (``length``: truncado por max_tokens, ``content_filter``: moderacion, ``tool_calls`` / ``function_call``: invocacion de herramientas no esperada por configuracion erronea, etc.)
- ``[LLM:OPENAI] Stream refusal.`` (WARN) - Cuando se devuelve ``delta.refusal`` con salida estructurada

Estos logs WARN pueden utilizarse para ajustar ``max_tokens``, auditar filtros de contenido y detectar configuraciones incorrectas de ``extra_params``.

Enmascaramiento de credenciales en URLs registradas
---------------------------------------------------

Las URLs emitidas en los logs se enmascaran automaticamente sustituyendo por ``***`` los parametros de consulta que contienen credenciales (``api_key``, ``apikey``, ``api-key``, ``key``, ``token``, ``access_token``, ``access-token``; sin distinguir mayusculas y minusculas).

El endpoint oficial de OpenAI (``https://api.openai.com``) se autentica mediante el encabezado ``Authorization: Bearer``, por lo que la URL no contiene credenciales. No obstante, este enmascaramiento evita que la clave API se filtre en los logs incluso cuando ``rag.llm.openai.api.url`` apunta a un proxy personalizado que acepta credenciales como parametro de consulta (algunas implementaciones de Azure, gateways vLLM, etc.).

Soporte de modelos de inferencia
=================================

Cuando se usan modelos de inferencia de las series o1/o3/o4 o de la serie gpt-5, |Fess| utiliza automaticamente el parametro ``max_completion_tokens`` de la API de OpenAI en lugar de ``max_tokens``. No se requieren cambios adicionales de configuracion.

.. note::
   Los modelos de inferencia (serie o1/o3/o4/gpt-5) ignoran la configuracion de ``temperature`` y usan un valor fijo (1). Ademas, al usar modelos de inferencia, el ``max_tokens`` predeterminado se multiplica por ``reasoning.token.multiplier`` (predeterminado: 4).

Parametros adicionales para modelos de inferencia
--------------------------------------------------

Al usar modelos de inferencia, se pueden configurar los siguientes parametros adicionales en ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - Configuracion de reasoning effort para modelos serie o (``low``, ``medium``, ``high``)
     - ``low`` (intent/evaluation/docnotfound/unclear/noresults/queryregeneration), no configurado (otros)
   * - ``rag.llm.openai.{promptType}.top.p``
     - Umbral de probabilidad para la seleccion de tokens (0.0 a 1.0)
     - (no configurado)
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - Penalizacion de frecuencia (-2.0 a 2.0)
     - (no configurado)
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - Penalizacion de presencia (-2.0 a 2.0)
     - (no configurado)

``{promptType}`` puede ser ``intent``, ``evaluation``, ``answer``, ``summary``, etc.

Ejemplo de configuracion
------------------------

::

    # Configurar reasoning effort en high para o3-mini
    rag.llm.openai.model=o3-mini
    rag.llm.openai.reasoning.effort=high

    # Configurar top_p y penalizaciones para gpt-5
    rag.llm.openai.model=gpt-5
    rag.llm.openai.top.p=0.9
    rag.llm.openai.frequency.penalty=0.5

Configuracion via opciones JVM
==============================

Por razones de seguridad, se recomienda configurar las claves de API a traves del
entorno de ejecucion (opciones JVM) en lugar de archivos versionados.

Entorno Docker
--------------

El repositorio oficial `docker-fess <https://github.com/codelibs/docker-fess>`__
incluye un overlay OpenAI (``compose-openai.yaml``). Pasos minimos:

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

Contenido de ``compose-openai.yaml`` (referencia para una configuracion equivalente):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Notas:

- ``FESS_PLUGINS=fess-llm-openai:15.6.0`` hace que el ``run.sh`` del contenedor descargue e instale automaticamente el plugin en ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` habilita el modo IA
- ``-Dfess.config.rag.llm.openai.api.key=...`` define la clave API, ``-Dfess.config.rag.llm.openai.model=...`` selecciona el modelo
- ``-Dfess.system.rag.llm.name=openai`` solo actua como valor inicial por defecto antes de que se persista un valor en OpenSearch. Despues del inicio el ajuste tambien puede modificarse desde Administracion > Sistema > General (seccion RAG)

Si el acceso a Internet pasa por un proxy, especifique la configuracion ``http.proxy.*`` de |Fess| a traves de ``FESS_JAVA_OPTS`` (consulte la seccion "Uso a traves de proxy HTTP" mas adelante).

Entorno systemd
---------------

Agregue a ``FESS_JAVA_OPTS`` en ``/etc/sysconfig/fess`` (o ``/etc/default/fess``):

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

Uso a traves de proxy HTTP
==========================

Desde |Fess| 15.6.1, el cliente de OpenAI comparte la configuracion de proxy HTTP comun de |Fess|. Especifique las siguientes propiedades en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``http.proxy.host``
     - Nombre del host del proxy (si esta vacio, no se usa proxy)
     - ``""``
   * - ``http.proxy.port``
     - Numero de puerto del proxy
     - ``8080``
   * - ``http.proxy.username``
     - Nombre de usuario para autenticacion del proxy (opcional; al especificarlo se habilita la autenticacion Basic)
     - ``""``
   * - ``http.proxy.password``
     - Contrasena para autenticacion del proxy
     - ``""``

En entornos Docker, especifique en ``FESS_JAVA_OPTS`` de la siguiente forma::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   Esta configuracion tambien afecta el acceso HTTP de todo |Fess|, incluido el crawler.
   Las propiedades de sistema Java tradicionales (como ``-Dhttps.proxyHost``) no son consultadas por el cliente de OpenAI.

Uso de Azure OpenAI
===================

Para usar modelos de OpenAI a traves de Microsoft Azure, cambie el endpoint de la API.

::

    # Endpoint de Azure OpenAI
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Clave API de Azure
    rag.llm.openai.api.key=your-azure-api-key

    # Nombre del despliegue (especificar como nombre de modelo)
    rag.llm.openai.model=your-deployment-name

.. note::
   Al usar Azure OpenAI, el formato de solicitud de la API puede diferir ligeramente.
   Consulte la documentacion de Azure OpenAI para mas detalles.

Guia de seleccion de modelos
============================

Guia para la seleccion de modelos segun el proposito de uso.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modelo
     - Costo
     - Calidad
     - Uso
   * - ``gpt-5-mini``
     - Medio
     - Alta
     - Uso equilibrado (recomendado)
   * - ``gpt-4o-mini``
     - Bajo-Medio
     - Alta
     - Uso con prioridad en costos
   * - ``gpt-5``
     - Alto
     - Maxima
     - Razonamiento complejo, cuando se requiere alta calidad
   * - ``gpt-4o``
     - Medio-Alto
     - Maxima
     - Cuando se requiere soporte multimodal
   * - ``o3-mini`` / ``o4-mini``
     - Medio
     - Maxima
     - Tareas de razonamiento como matematicas y programacion

Estimacion de costos
--------------------

La API de OpenAI cobra segun el uso.

.. note::
   Para los precios mas recientes, consulte `OpenAI Pricing <https://openai.com/pricing>`__.

Control de solicitudes simultaneas
====================================

En |Fess|, el numero de solicitudes simultaneas a la API de OpenAI se puede controlar con ``rag.llm.openai.max.concurrent.requests`` en ``fess_config.properties``. El valor predeterminado es ``5``.

::

    # Configurar el numero maximo de solicitudes simultaneas
    rag.llm.openai.max.concurrent.requests=5

Esta configuracion permite prevenir solicitudes excesivas a la API de OpenAI y evitar errores de limite de tasa.

Limites por nivel de OpenAI
---------------------------

Los limites del lado de la API varian segun el nivel de la cuenta de OpenAI:

- **Free**: 3 RPM (solicitudes/minuto)
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: Limites aun mayores

Ajuste ``rag.llm.openai.max.concurrent.requests`` apropiadamente segun el nivel de la cuenta de OpenAI.

Solucion de problemas
=====================

Error de autenticacion
----------------------

**Sintoma**: Error "401 Unauthorized"

**Verificaciones**:

1. Verificar que la clave API este configurada correctamente
2. Confirmar que la clave API sea valida (verificar en el dashboard de OpenAI)
3. Confirmar que la clave API tenga los permisos necesarios

Error de limite de tasa
-----------------------

**Sintoma**: Error "429 Too Many Requests"

**Solucion**:

1. Reducir el valor de ``rag.llm.openai.max.concurrent.requests``::

    rag.llm.openai.max.concurrent.requests=3

2. Actualizar el nivel de la cuenta de OpenAI

Cuota excedida
--------------

**Sintoma**: Error "You exceeded your current quota"

**Solucion**:

1. Verificar el uso en el dashboard de OpenAI
2. Revisar la configuracion de facturacion y aumentar el limite si es necesario

Timeout
-------

**Sintoma**: Las solicitudes tienen timeout

**Solucion**:

1. Extender el tiempo de timeout::

    rag.llm.openai.timeout=180000

2. Considerar usar un modelo mas rapido (como gpt-5-mini)

Configuracion de depuracion
---------------------------

Para investigar problemas, puede ajustar el nivel de log de |Fess| para obtener logs detallados relacionados con OpenAI.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

Notas de seguridad
==================

Al usar la API de OpenAI, tenga en cuenta los siguientes aspectos de seguridad.

1. **Privacidad de datos**: El contenido de los resultados de busqueda se envia a los servidores de OpenAI
2. **Gestion de claves API**: La filtracion de claves puede llevar a uso no autorizado
3. **Cumplimiento**: Si incluye datos confidenciales, verifique las politicas de su organizacion
4. **Politica de uso**: Cumpla con los terminos de servicio de OpenAI

Informacion de referencia
=========================

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - Descripcion general de integracion LLM
- :doc:`rag-chat` - Detalles de la funcionalidad de modo de búsqueda IA
