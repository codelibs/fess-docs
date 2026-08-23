===========================================
Configuración de OpenAI (Búsqueda IA / RAG)
===========================================

Descripción general
===================

Esta página explica cómo configurar el plugin ``fess-llm-openai`` para que |Fess| pueda usar OpenAI en su **modo de búsqueda IA (RAG: Retrieval-Augmented Generation)** — respondiendo preguntas en lenguaje natural a partir de su índice de búsqueda empresarial con fuentes citadas. |Fess| llama a la API de OpenAI para ejecutar RAG sobre sus documentos rastreados con modelos GPT.

OpenAI es un servicio en la nube que proporciona modelos de lenguaje grandes (LLM) de alto rendimiento, comenzando con GPT-4.
|Fess| puede utilizar la API de OpenAI para implementar la funcionalidad de modo de búsqueda IA.

Al usar OpenAI, es posible generar respuestas de alta calidad con modelos de IA de última generación.

Características principales
---------------------------

- **Respuestas de alta calidad**: Generación de respuestas de alta precisión con modelos GPT de última generación
- **Escalabilidad**: Fácil escalado al ser un servicio en la nube
- **Mejora continua**: El rendimiento mejora con actualizaciones periódicas de modelos
- **Funcionalidad rica**: Compatible con diversas tareas como generación de texto, resumen, traducción

Modelos compatibles
-------------------

Principales modelos disponibles en OpenAI:

- ``gpt-5`` - Último modelo de alto rendimiento
- ``gpt-5-mini`` - Versión ligera de GPT-5 (buena relación costo-rendimiento)
- ``gpt-4o`` - Modelo multimodal de alto rendimiento
- ``gpt-4o-mini`` - Versión ligera de GPT-4o
- ``o3-mini`` - Modelo ligero especializado en razonamiento
- ``o4-mini`` - Modelo ligero de próxima generación especializado en razonamiento

.. note::
   Para la información más reciente sobre modelos disponibles, consulte `OpenAI Models <https://platform.openai.com/docs/models>`__.

.. note::
   Al usar modelos de la serie o1/o3/o4 o de la serie gpt-5, |Fess| utiliza automáticamente el parámetro ``max_completion_tokens`` de la API de OpenAI. No se requieren cambios de configuración.

Requisitos previos
==================

Antes de usar OpenAI, prepare lo siguiente.

1. **Cuenta de OpenAI**: Cree una cuenta en `https://platform.openai.com/ <https://platform.openai.com/>`__
2. **Clave API**: Genere una clave API en el dashboard de OpenAI
3. **Configuración de facturación**: Configure la información de facturación ya que el uso de la API genera cargos

Obtención de clave API
----------------------

1. Inicie sesión en `OpenAI Platform <https://platform.openai.com/>`__
2. Navegue a la sección "API keys"
3. Haga clic en "Create new secret key"
4. Ingrese un nombre para la clave y créela
5. Guarde la clave mostrada de forma segura (solo se muestra una vez)

.. warning::
   La clave API es información confidencial. Tenga en cuenta lo siguiente:

   - No la commita en sistemas de control de versiones
   - No la imprima en logs
   - Adminístrela con variables de entorno o archivos de configuración seguros

Instalación del plugin
======================

La funcionalidad de integración con OpenAI se proporciona como plugin. Para usarla es necesario instalar el plugin ``fess-llm-openai``.

1. Descargue `fess-llm-openai-15.9.0.jar`
2. Coloque el archivo JAR en el directorio ``app/WEB-INF/plugin/`` del directorio de instalación de |Fess|::

    cp fess-llm-openai-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Reinicie |Fess|

.. note::
   La versión del plugin debe coincidir con la versión de |Fess|.

Configuración básica
====================

Los elementos de configuración se dividen en los siguientes dos archivos según su uso.

- ``app/WEB-INF/conf/fess_config.properties`` - Configuración del núcleo de |Fess| y configuración específica del proveedor LLM
- ``system.properties`` / Pantalla de administración (Administración > Sistema > General) - Selección del proveedor LLM (``rag.llm.name``)

Configuración mínima
--------------------

``system.properties`` (también configurable en Administración > Sistema > General):

::

    # Configurar el proveedor LLM como OpenAI
    rag.llm.name=openai

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # Clave API de OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelo a usar
    rag.llm.openai.model=gpt-5-mini

Configuración recomendada (entorno de producción)
-------------------------------------------------

``system.properties`` (también configurable en Administración > Sistema > General):

::

    # Configuracion del proveedor LLM
    rag.llm.name=openai

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

Elementos de configuración
==========================

Todos los elementos de configuración disponibles para el cliente de OpenAI. Excepto ``rag.llm.name``, todos se configuran en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - Propiedad
     - Descripción
     - Predeterminado
     - Lugar de configuración
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
     - Intervalo de verificación de disponibilidad (segundos)
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - Número máximo de solicitudes simultáneas
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - Número máximo de documentos relevantes en la evaluación
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - Timeout de espera de solicitudes simultáneas (ms)
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - Multiplicador de max tokens para modelos de inferencia
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.retry.max``
     - Número máximo de reintentos HTTP (en errores ``429`` y de la familia ``5xx``)
     - ``10``
     - fess_config.properties
   * - ``rag.llm.openai.retry.base.delay.ms``
     - Retardo base del backoff exponencial (milisegundos)
     - ``2000``
     - fess_config.properties
   * - ``rag.llm.openai.stream.include.usage``
     - Envía ``stream_options.include_usage=true`` durante el streaming para recibir la información de tokens utilizados en el chunk final
     - ``true``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - Máximo de caracteres para historial de conversación
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - Máximo de mensajes de historial para detección de intención
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - Máximo de caracteres de historial para detección de intención
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - Máximo de caracteres para mensajes del asistente
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - Máximo de caracteres para resumen del asistente
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - Máximo de caracteres para descripción de documentos en evaluación
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - Habilitación de la funcionalidad de modo de búsqueda IA
     - ``false``
     - fess_config.properties

Configuración por tipo de prompt
=================================

En |Fess|, se pueden configurar parámetros individuales para cada tipo de prompt. La configuración se realiza en ``fess_config.properties``.

Patrón de configuración
------------------------

La configuración por tipo de prompt se especifica con el siguiente patrón:

- ``rag.llm.openai.{promptType}.temperature`` - Aleatoriedad de generación (0.0 a 2.0). Se ignora para modelos de inferencia (serie o1/o3/o4/gpt-5)
- ``rag.llm.openai.{promptType}.max.tokens`` - Número máximo de tokens
- ``rag.llm.openai.{promptType}.context.max.chars`` - Número máximo de caracteres del contexto (predeterminado: ``16000`` para answer/summary, ``10000`` para otros)

Tipos de prompt
---------------

Tipos de prompt disponibles:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tipo de prompt
     - Descripción
   * - ``intent``
     - Prompt para determinar la intención del usuario
   * - ``evaluation``
     - Prompt para evaluar la relevancia de los resultados de búsqueda
   * - ``unclear``
     - Prompt de respuesta para consultas no claras
   * - ``noresults``
     - Prompt de respuesta cuando no hay resultados de búsqueda
   * - ``docnotfound``
     - Prompt de respuesta cuando no se encuentra el documento
   * - ``answer``
     - Prompt para generar respuestas
   * - ``summary``
     - Prompt para generar resúmenes
   * - ``faq``
     - Prompt para generar FAQ
   * - ``direct``
     - Prompt para respuesta directa
   * - ``queryregeneration``
     - Prompt de regeneración de consultas

Valores predeterminados
-----------------------

Valores predeterminados para cada tipo de prompt. La configuración de temperature se ignora para modelos de inferencia (serie o1/o3/o4/gpt-5).

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
     - Detección de intención determinista
   * - ``evaluation``
     - 0.1
     - 256
     - Evaluación de relevancia determinista
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
     - Generación de respuesta principal
   * - ``summary``
     - 0.3
     - 2048
     - Generación de resumen
   * - ``queryregeneration``
     - 0.3
     - 256
     - Regeneración de consultas

Ejemplo de configuración
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

Las solicitudes a la API de OpenAI se reintentan automáticamente para los siguientes códigos de estado HTTP:

- ``429`` Too Many Requests (límite de tasa)
- ``500`` Internal Server Error
- ``502`` Bad Gateway (OpenAI puede devolverlo cuando el upstream está sobrecargado)
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Durante los reintentos se aplica un backoff exponencial (valor base ``rag.llm.openai.retry.base.delay.ms`` milisegundos, hasta ``rag.llm.openai.retry.max`` intentos, con jitter de +/-20%).
Si el servidor devuelve un encabezado ``Retry-After`` (segundos enteros, limitado a ``600`` segundos como máximo), ese valor tiene prioridad sobre el backoff exponencial. Esto sigue la guía oficial de OpenAI.

Tenga en cuenta que las ``IOException`` (timeouts de conexión, reset de socket, fallos de DNS) no se reintentan, ya que la solicitud podría haber llegado al servidor y un reintento podría provocar un cobro doble.
En las solicitudes de streaming, solo la conexión inicial es objeto de reintentos; los errores que ocurren después de comenzar a recibir el cuerpo de la respuesta se propagan inmediatamente.

.. note::
   Con la configuración predeterminada (máximo 10 intentos, base 2 segundos), en el peor caso la suma de los 9 backoffs es ``2 + 4 + 8 + ... + 512 = aproximadamente 1022 segundos (aproximadamente 17 minutos)``. Si ``Retry-After`` (máximo 600 segundos) se devuelve en cada intento, el peor caso puede llegar a ``9 x 600 segundos = 90 minutos``. Si desea controlar la latencia de forma más estricta, reduzca ``rag.llm.openai.retry.max``.

Streaming e información de uso
==============================

Por defecto, se incluye ``stream_options.include_usage=true`` en las solicitudes y, en el chunk SSE final de la respuesta de streaming, se recibe el objeto ``usage`` (que incluye ``completion_tokens_details.reasoning_tokens`` para los modelos de inferencia y ``prompt_tokens_details.cached_tokens`` cuando se utiliza la caché de prompts).

Si utiliza un backend que no admite el campo ``stream_options.include_usage`` (como vLLM o gateways compatibles con Azure OpenAI), desactívelo de la siguiente forma::

    rag.llm.openai.stream.include.usage=false

Salida de logs y detección de anomalías
=======================================

El cliente de OpenAI emite los siguientes logs estructurados, que permiten supervisar el uso de tokens y las anomalías de respuesta sin necesidad de habilitar el nivel ``DEBUG``.

- ``[LLM:OPENAI] Stream completed.`` (INFO) - Al finalizar la respuesta de streaming, emite el número de chunks, el tiempo hasta el primer chunk y la información de uso de tokens
- ``[LLM:OPENAI] Chat response received.`` (INFO) - Al finalizar la respuesta no-streaming, emite información equivalente
- ``[LLM:OPENAI] Chat finished abnormally`` / ``Stream finished abnormally`` (WARN) - Cuando ``finish_reason`` es distinto de ``stop`` (``length``: truncado por max_tokens, ``content_filter``: moderación, ``tool_calls`` / ``function_call``: invocación de herramientas no esperada por configuración errónea, etc.)
- ``[LLM:OPENAI] Stream refusal.`` (WARN) - Cuando se devuelve ``delta.refusal`` con salida estructurada

Estos logs WARN pueden utilizarse para ajustar ``max_tokens``, auditar filtros de contenido y detectar configuraciones incorrectas de ``extra_params``.

Enmascaramiento de credenciales en URLs registradas
---------------------------------------------------

Las URLs emitidas en los logs se enmascaran automáticamente sustituyendo por ``***`` los parámetros de consulta que contienen credenciales (``api_key``, ``apikey``, ``api-key``, ``key``, ``token``, ``access_token``, ``access-token``; sin distinguir mayúsculas y minúsculas).

El endpoint oficial de OpenAI (``https://api.openai.com``) se autentica mediante el encabezado ``Authorization: Bearer``, por lo que la URL no contiene credenciales. No obstante, este enmascaramiento evita que la clave API se filtre en los logs incluso cuando ``rag.llm.openai.api.url`` apunta a un proxy personalizado que acepta credenciales como parámetro de consulta (algunas implementaciones de Azure, gateways vLLM, etc.).

Soporte de modelos de inferencia
=================================

Cuando se usan modelos de inferencia de las series o1/o3/o4 o de la serie gpt-5, |Fess| utiliza automáticamente el parámetro ``max_completion_tokens`` de la API de OpenAI en lugar de ``max_tokens``. No se requieren cambios adicionales de configuración.

.. note::
   Los modelos de inferencia (serie o1/o3/o4/gpt-5) ignoran la configuración de ``temperature`` y usan un valor fijo (1). Además, al usar modelos de inferencia, el ``max_tokens`` predeterminado se multiplica por ``reasoning.token.multiplier`` (predeterminado: 4).

Parámetros adicionales para modelos de inferencia
--------------------------------------------------

Al usar modelos de inferencia, se pueden configurar los siguientes parámetros adicionales en ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - Configuración de reasoning effort para modelos serie o (``low``, ``medium``, ``high``)
     - ``low`` (intent/evaluation/docnotfound/unclear/noresults/queryregeneration), no configurado (otros)
   * - ``rag.llm.openai.{promptType}.top.p``
     - Umbral de probabilidad para la selección de tokens (0.0 a 1.0)
     - (no configurado)
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - Penalización de frecuencia (-2.0 a 2.0)
     - (no configurado)
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - Penalización de presencia (-2.0 a 2.0)
     - (no configurado)

``{promptType}`` puede ser ``intent``, ``evaluation``, ``answer``, ``summary``, etc.

Ejemplo de configuración
------------------------

::

    # Configurar reasoning effort en high para la generación de respuestas con o3-mini
    rag.llm.openai.model=o3-mini
    rag.llm.openai.answer.reasoning.effort=high

    # Configurar top_p y penalizaciones para la generación de respuestas con gpt-5
    rag.llm.openai.model=gpt-5
    rag.llm.openai.answer.top.p=0.9
    rag.llm.openai.answer.frequency.penalty=0.5

Configuración vía opciones JVM
==============================

Por razones de seguridad, se recomienda configurar las claves de API a través del
entorno de ejecución (opciones JVM) en lugar de archivos versionados.

Entorno Docker
--------------

El repositorio oficial `docker-fess <https://github.com/codelibs/docker-fess>`__
incluye un overlay OpenAI (``compose-openai.yaml``). Pasos mínimos:

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

Contenido de ``compose-openai.yaml`` (referencia para una configuración equivalente):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Notas:

- ``FESS_PLUGINS=fess-llm-openai:15.9.0`` hace que el ``run.sh`` del contenedor descargue e instale automáticamente el plugin en ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` habilita el modo IA
- ``-Dfess.config.rag.llm.openai.api.key=...`` define la clave API, ``-Dfess.config.rag.llm.openai.model=...`` selecciona el modelo
- ``-Dfess.system.rag.llm.name=openai`` solo actúa como valor inicial por defecto antes de que se persista un valor en OpenSearch. Después del inicio el ajuste también puede modificarse desde Administración > Sistema > General (sección RAG)

Si el acceso a Internet pasa por un proxy, especifique la configuración ``http.proxy.*`` de |Fess| a través de ``FESS_JAVA_OPTS`` (consulte la sección "Uso a través de proxy HTTP" más adelante).

Entorno systemd
---------------

Agregue a ``FESS_JAVA_OPTS`` en ``/etc/sysconfig/fess`` (o ``/etc/default/fess``):

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

Uso a través de proxy HTTP
==========================

El cliente de OpenAI comparte la configuración de proxy HTTP común de |Fess|. Especifique las siguientes propiedades en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``http.proxy.host``
     - Nombre del host del proxy (si está vacío, no se usa proxy)
     - ``""``
   * - ``http.proxy.port``
     - Número de puerto del proxy
     - ``8080``
   * - ``http.proxy.username``
     - Nombre de usuario para autenticación del proxy (opcional; al especificarlo se habilita la autenticación Basic)
     - ``""``
   * - ``http.proxy.password``
     - Contraseña para autenticación del proxy
     - ``""``

En entornos Docker, especifique en ``FESS_JAVA_OPTS`` de la siguiente forma::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   Esta configuración también afecta el acceso HTTP de todo |Fess|, incluido el crawler.
   Las propiedades de sistema Java tradicionales (como ``-Dhttps.proxyHost``) no son consultadas por el cliente de OpenAI.

Uso de Azure OpenAI
===================

Para usar modelos de OpenAI a través de Microsoft Azure, cambie el endpoint de la API.

::

    # Endpoint de Azure OpenAI
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Clave API de Azure
    rag.llm.openai.api.key=your-azure-api-key

    # Nombre del despliegue (especificar como nombre de modelo)
    rag.llm.openai.model=your-deployment-name

.. note::
   Al usar Azure OpenAI, el formato de solicitud de la API puede diferir ligeramente.
   Consulte la documentación de Azure OpenAI para más detalles.

Guía de selección de modelos
============================

Guía para la selección de modelos según el propósito de uso.

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
     - Máxima
     - Razonamiento complejo, cuando se requiere alta calidad
   * - ``gpt-4o``
     - Medio-Alto
     - Máxima
     - Cuando se requiere soporte multimodal
   * - ``o3-mini`` / ``o4-mini``
     - Medio
     - Máxima
     - Tareas de razonamiento como matemáticas y programación

Estimación de costos
--------------------

La API de OpenAI cobra según el uso.

.. note::
   Para los precios más recientes, consulte `OpenAI Pricing <https://openai.com/pricing>`__.

Control de solicitudes simultáneas
====================================

En |Fess|, el número de solicitudes simultáneas a la API de OpenAI se puede controlar con ``rag.llm.openai.max.concurrent.requests`` en ``fess_config.properties``. El valor predeterminado es ``5``.

::

    # Configurar el numero maximo de solicitudes simultaneas
    rag.llm.openai.max.concurrent.requests=5

Esta configuración permite prevenir solicitudes excesivas a la API de OpenAI y evitar errores de límite de tasa.

Límites por nivel de OpenAI
---------------------------

Los límites del lado de la API varían según el nivel de la cuenta de OpenAI:

- **Free**: 3 RPM (solicitudes/minuto)
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: Límites aún mayores

Ajuste ``rag.llm.openai.max.concurrent.requests`` apropiadamente según el nivel de la cuenta de OpenAI.

Solución de problemas
=====================

Error de autenticación
----------------------

**Síntoma**: Error "401 Unauthorized"

**Verificaciones**:

1. Verificar que la clave API esté configurada correctamente
2. Confirmar que la clave API sea válida (verificar en el dashboard de OpenAI)
3. Confirmar que la clave API tenga los permisos necesarios

Error de límite de tasa
-----------------------

**Síntoma**: Error "429 Too Many Requests"

**Solución**:

1. Reducir el valor de ``rag.llm.openai.max.concurrent.requests``::

    rag.llm.openai.max.concurrent.requests=3

2. Actualizar el nivel de la cuenta de OpenAI

Cuota excedida
--------------

**Síntoma**: Error "You exceeded your current quota"

**Solución**:

1. Verificar el uso en el dashboard de OpenAI
2. Revisar la configuración de facturación y aumentar el límite si es necesario

Timeout
-------

**Síntoma**: Las solicitudes tienen timeout

**Solución**:

1. Extender el tiempo de timeout::

    rag.llm.openai.timeout=180000

2. Considerar usar un modelo más rápido (como gpt-5-mini)

Configuración de depuración
---------------------------

Para investigar problemas, puede ajustar el nivel de log de |Fess| para obtener logs detallados relacionados con OpenAI.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

Notas de seguridad
==================

Al usar la API de OpenAI, tenga en cuenta los siguientes aspectos de seguridad.

1. **Privacidad de datos**: El contenido de los resultados de búsqueda se envía a los servidores de OpenAI
2. **Gestión de claves API**: La filtración de claves puede llevar a uso no autorizado
3. **Cumplimiento**: Si incluye datos confidenciales, verifique las políticas de su organización
4. **Política de uso**: Cumpla con los términos de servicio de OpenAI

Información de referencia
=========================

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - Descripción general de integración LLM
- :doc:`rag-chat` - Detalles de la funcionalidad de modo de búsqueda IA
- :doc:`rank-fusion` - Búsqueda híbrida: combina búsqueda por palabras clave y búsqueda semántica (vectorial)
- :doc:`../user/chat-search` - Uso del modo de búsqueda IA (guía para el usuario final)
