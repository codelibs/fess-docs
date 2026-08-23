===================================================
Configuración de Google Gemini (Búsqueda IA / RAG)
===================================================

Descripción general
===================

Esta página explica cómo configurar el plugin ``fess-llm-gemini`` para que |Fess| pueda usar Google Gemini en su **modo de búsqueda IA (RAG: Retrieval-Augmented Generation)** — respondiendo preguntas en lenguaje natural a partir de su índice de búsqueda empresarial con fuentes citadas. |Fess| llama a la API de Google AI (Generative Language API) para ejecutar RAG sobre sus documentos rastreados con modelos Gemini.

Google Gemini es un modelo de lenguaje grande (LLM) de última generación proporcionado por Google.
|Fess| puede implementar la funcionalidad de modo de búsqueda IA con el modelo Gemini utilizando Google AI API (Generative Language API).

Al usar Gemini, es posible generar respuestas de alta calidad aprovechando la última tecnología de IA de Google.

Características principales
---------------------------

- **Soporte multimodal**: Capaz de procesar no solo texto sino también imágenes
- **Contexto largo**: Ventana de contexto larga que puede procesar grandes cantidades de documentos a la vez
- **Eficiencia de costos**: El modelo Flash es rápido y de bajo costo
- **Integración con Google**: Fácil integración con servicios de Google Cloud

Modelos compatibles
-------------------

Principales modelos disponibles en Gemini:

- ``gemini-3.1-flash-lite-preview`` - Modelo rápido ligero y de bajo costo (predeterminado)
- ``gemini-3-flash-preview`` - Modelo Flash estándar
- ``gemini-3.1-pro`` / ``gemini-3-pro`` - Modelos de alto razonamiento
- ``gemini-2.5-flash`` - Modelo rápido versión estable
- ``gemini-2.5-pro`` - Modelo de alto razonamiento versión estable

.. note::
   Para la información más reciente sobre modelos disponibles, consulte `Google AI for Developers <https://ai.google.dev/models/gemini>`__.

Requisitos previos
==================

Antes de usar Gemini, prepare lo siguiente.

1. **Cuenta de Google**: Se requiere una cuenta de Google
2. **Acceso a Google AI Studio**: Acceda a `https://aistudio.google.com/ <https://aistudio.google.com/>`__
3. **Clave API**: Genere una clave API en Google AI Studio

Obtención de clave API
----------------------

1. Acceda a `Google AI Studio <https://aistudio.google.com/>`__
2. Haga clic en "Get API key"
3. Seleccione "Create API key"
4. Seleccione o cree un nuevo proyecto
5. Guarde la clave API generada de forma segura

.. warning::
   La clave API es información confidencial. Tenga en cuenta lo siguiente:

   - No la commita en sistemas de control de versiones
   - No la imprima en logs
   - Adminístrela con variables de entorno o archivos de configuración seguros

Instalación del plugin
======================

La funcionalidad de integración con Gemini se proporciona como plugin ``fess-llm-gemini``.
Para usar Gemini es necesario instalar el plugin.

1. Descargue `fess-llm-gemini-15.9.0.jar`
2. Colóquelo en el directorio ``app/WEB-INF/plugin/`` de |Fess|
3. Reinicie |Fess|

::

    # Ejemplo de colocacion del plugin
    cp fess-llm-gemini-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   La versión del plugin debe coincidir con la versión de |Fess|.

Configuración básica
====================

La habilitación de la funcionalidad de modo de búsqueda IA y la configuración específica de Gemini se realizan en ``fess_config.properties``, y la selección del proveedor LLM (``rag.llm.name``) se realiza en la pantalla de administración o en ``system.properties``.

Configuración de fess_config.properties
----------------------------------------

Agregue la configuración de habilitación de la funcionalidad de modo de búsqueda IA en ``app/WEB-INF/conf/fess_config.properties``.

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

Configuración del proveedor LLM
--------------------------------

La selección del proveedor LLM (``rag.llm.name``) se configura en la pantalla de administración (Administración > Sistema > General) o en ``system.properties``. La configuración específica de Gemini se realiza en ``fess_config.properties``.

Configuración mínima
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``system.properties`` (también configurable en Administración > Sistema > General):

::

    # Configurar el proveedor LLM como Gemini
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # Clave API de Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelo a usar
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

Configuración recomendada (entorno de producción)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``system.properties`` (también configurable en Administración > Sistema > General):

::

    # Configurar el proveedor LLM como Gemini
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # Clave API de Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuracion del modelo (usar modelo rapido)
    rag.llm.gemini.model=gemini-3-flash-preview

    # Endpoint de API (normalmente no necesita cambios)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Configuracion de timeout
    rag.llm.gemini.timeout=60000

Elementos de configuración
==========================

Todos los elementos de configuración disponibles para el cliente de Gemini. Todos se configuran en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.gemini.api.key``
     - Clave API de Google AI (debe configurarse para usar la API de Gemini)
     - ``""``
   * - ``rag.llm.gemini.model``
     - Nombre del modelo a usar
     - ``gemini-3.1-flash-lite-preview``
   * - ``rag.llm.gemini.api.url``
     - URL base de la API
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Timeout de solicitud (milisegundos)
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - Intervalo de verificación de disponibilidad (segundos)
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - Número máximo de solicitudes simultáneas
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - Número máximo de documentos relevantes en la evaluación
     - ``3``
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - Número máximo de caracteres para la descripción del documento en la evaluación
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - Tiempo de espera de solicitudes simultáneas (milisegundos)
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - Número máximo de caracteres del historial de chat
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - Número máximo de mensajes del historial para la determinación de intención
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - Número máximo de caracteres del historial para la determinación de intención
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - Número máximo de caracteres del historial del asistente
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - Número máximo de caracteres del resumen del historial del asistente
     - ``1000``
   * - ``rag.llm.gemini.retry.max``
     - Número máximo de reintentos HTTP (en errores ``429`` y de la familia ``5xx``)
     - ``10``
   * - ``rag.llm.gemini.retry.base.delay.ms``
     - Retardo base del backoff exponencial (milisegundos)
     - ``2000``

Método de autenticación
=======================

La clave API se envía mediante el encabezado HTTP ``x-goog-api-key`` (método recomendado por Google).
Ya no se añade a la URL como parámetro de consulta ``?key=...`` como anteriormente, por lo que la clave API no queda registrada en los logs de acceso.

Comportamiento de reintentos
============================

Las solicitudes a la API de Gemini se reintentan automáticamente para los siguientes códigos de estado HTTP:

- ``429`` Resource Exhausted (cuota superada / límite de tasa)
- ``500`` Internal Server Error
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Durante los reintentos se aplica un backoff exponencial (valor base ``rag.llm.gemini.retry.base.delay.ms`` milisegundos, hasta ``rag.llm.gemini.retry.max`` intentos, con jitter de +/-20%).
En las solicitudes de streaming, solo la conexión inicial es objeto de reintentos; los errores que ocurren después de comenzar a recibir el cuerpo de la respuesta se propagan inmediatamente.

Configuración por tipo de prompt
=================================

En |Fess|, se pueden configurar los parámetros del LLM en detalle por tipo de prompt.
La configuración por tipo de prompt se escribe en ``fess_config.properties``.

Formato de configuración
------------------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
    rag.llm.gemini.{promptType}.context.max.chars

Tipos de prompt disponibles
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tipo de prompt
     - Descripción
   * - ``intent``
     - Prompt para determinar la intención del usuario
   * - ``evaluation``
     - Prompt para evaluar la relevancia de los documentos
   * - ``unclear``
     - Prompt para cuando la pregunta no está clara
   * - ``noresults``
     - Prompt para cuando no hay resultados de búsqueda
   * - ``docnotfound``
     - Prompt para cuando no se encuentra el documento
   * - ``answer``
     - Prompt de generación de respuesta
   * - ``summary``
     - Prompt de generación de resumen
   * - ``faq``
     - Prompt de generación de FAQ
   * - ``direct``
     - Prompt de respuesta directa
   * - ``queryregeneration``
     - Prompt de regeneración de consulta

Valores predeterminados por tipo de prompt
-------------------------------------------

Valores predeterminados para cada tipo de prompt. Estos valores se utilizan cuando no se configuran explícitamente.

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - Tipo de prompt
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``512``
     - ``0``
   * - ``evaluation``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - ``0``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``0``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

Ejemplo de configuración
------------------------

::

    # Configuracion de temperatura de generacion de respuestas
    rag.llm.gemini.answer.temperature=0.7

    # Numero maximo de tokens de generacion de resumenes
    rag.llm.gemini.summary.max.tokens=2048

    # Numero maximo de caracteres de contexto de generacion de respuestas
    rag.llm.gemini.answer.context.max.chars=16000

    # Numero maximo de caracteres de contexto de generacion de resumenes
    rag.llm.gemini.summary.context.max.chars=16000

    # Numero maximo de caracteres de contexto de generacion de FAQ
    rag.llm.gemini.faq.context.max.chars=10000

.. note::
   El valor predeterminado de ``context.max.chars`` varía según el tipo de prompt.
   ``answer`` y ``summary`` son 16000, ``faq`` es 10000, y otros tipos de prompt son 10000.

Soporte de modelo de pensamiento
==================================

Gemini soporta modelos de pensamiento (Thinking Model).
Al usar un modelo de pensamiento, el modelo ejecuta un proceso de razonamiento interno antes de generar una respuesta, lo que permite generar respuestas con mayor precisión.

El presupuesto de pensamiento se configura por tipo de prompt en ``fess_config.properties``. |Fess| convierte automáticamente el valor entero (número de tokens) de ``rag.llm.gemini.{promptType}.thinking.budget`` al campo de API apropiado en función de la generación del modelo resuelta en el momento de la solicitud.

::

    # Configuracion del presupuesto de pensamiento para generacion de respuestas
    rag.llm.gemini.answer.thinking.budget=1024

    # Configuracion del presupuesto de pensamiento para generacion de resumenes
    rag.llm.gemini.summary.thinking.budget=1024

Mapeo según la generación del modelo
------------------------------------

- **Gemini 2.x** (por ejemplo, ``gemini-2.5-flash``): el valor entero configurado se envía tal cual como ``thinkingConfig.thinkingBudget``. Si se especifica ``0``, el pensamiento se desactiva por completo.
- **Gemini 3.x** (por ejemplo, ``gemini-3.1-flash-lite-preview``): el valor entero se agrupa en los valores enumerados de ``thinkingConfig.thinkingLevel`` (``MINIMAL`` / ``LOW`` / ``MEDIUM`` / ``HIGH``) antes de enviarse.

El mapeo de buckets para Gemini 3.x es el siguiente:

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Valor de presupuesto
     - thinkingLevel
     - Notas
   * - ``<=0``
     - ``MINIMAL`` o ``LOW``
     - ``MINIMAL`` para los modelos Flash / Flash-Lite; ``LOW`` para los modelos Pro que no admiten ``MINIMAL`` (``gemini-3-pro`` / ``gemini-3.1-pro``)
   * - ``<=4096``
     - ``MEDIUM``
     -
   * - ``>4096``
     - ``HIGH``
     -

.. note::
   Gemini 3.x siempre consume una cantidad fija de tokens de pensamiento en cualquier bucket (incluso con ``thinkingLevel=MINIMAL`` puede consumir varios cientos de tokens).
   Por este motivo, |Fess| añade automáticamente un margen adicional (1024 tokens) al ``maxOutputTokens`` predeterminado cuando se utiliza un modelo Gemini 3.x, evitando el truncado de la respuesta por ``finishReason=MAX_TOKENS``.
   En Gemini 2.x, ``thinkingBudget=0`` desactiva el pensamiento en sí, por lo que no se añade margen adicional.

.. note::
   Al configurar un presupuesto de pensamiento mayor, el tiempo de respuesta puede aumentar.
   Configure un valor apropiado según el uso.

Configuración vía opciones JVM
==============================

Por razones de seguridad, se recomienda configurar las claves de API a través del
entorno de ejecución (opciones JVM) en lugar de archivos versionados.

Entorno Docker
--------------

El repositorio oficial `docker-fess <https://github.com/codelibs/docker-fess>`__
incluye un overlay Gemini (``compose-gemini.yaml``). Pasos mínimos:

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Contenido de ``compose-gemini.yaml`` (referencia para una configuración equivalente):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-3.1-flash-lite-preview} -Dfess.system.rag.llm.name=gemini"

Notas:

- ``FESS_PLUGINS=fess-llm-gemini:15.9.0`` hace que el ``run.sh`` del contenedor descargue e instale automáticamente el plugin en ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` habilita el modo IA
- ``-Dfess.config.rag.llm.gemini.api.key=...`` define la clave API, ``-Dfess.config.rag.llm.gemini.model=...`` selecciona el modelo
- ``-Dfess.system.rag.llm.name=gemini`` solo actúa como valor inicial por defecto antes de que se persista un valor en OpenSearch. Después del inicio el ajuste también puede modificarse desde Administración > Sistema > General (sección RAG)

Si el acceso a Internet pasa por un proxy, especifique la configuración ``http.proxy.*`` de |Fess| a través de ``FESS_JAVA_OPTS`` (consulte la sección "Uso a través de proxy HTTP" más adelante).

Entorno systemd
---------------

Agregue a ``FESS_JAVA_OPTS`` en ``/etc/sysconfig/fess`` (o ``/etc/default/fess``):

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

Uso a través de proxy HTTP
==========================

El cliente de Gemini comparte la configuración de proxy HTTP común de |Fess|. Especifique las siguientes propiedades en ``fess_config.properties``.

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
   Las propiedades de sistema Java tradicionales (como ``-Dhttps.proxyHost``) no son consultadas por el cliente de Gemini.

Uso a través de Vertex AI
=========================

Si está usando Google Cloud Platform, también puede usar Gemini a través de Vertex AI.
Al usar Vertex AI, el endpoint de la API y el método de autenticación son diferentes.

.. note::
   El |Fess| actual utiliza Google AI API (generativelanguage.googleapis.com).
   Si se requiere el uso a través de Vertex AI, puede ser necesaria una implementación personalizada.

Guía de selección de modelos
============================

Guía para la selección de modelos según el propósito de uso.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modelo
     - Velocidad
     - Calidad
     - Uso
   * - ``gemini-3.1-flash-lite-preview``
     - Rápido
     - Alta
     - Ligero y de bajo costo (predeterminado, admite ``thinkingLevel=MINIMAL``)
   * - ``gemini-3-flash-preview``
     - Rápido
     - Máxima
     - Uso general (admite ``thinkingLevel=MINIMAL``)
   * - ``gemini-3.1-pro`` / ``gemini-3-pro``
     - Medio
     - Máxima
     - Razonamiento complejo (no admite ``MINIMAL``; mínimo ``LOW``)
   * - ``gemini-2.5-flash``
     - Rápido
     - Alta
     - Versión estable, énfasis en costos
   * - ``gemini-2.5-pro``
     - Medio
     - Alta
     - Versión estable, contexto largo

Ventana de contexto
-------------------

Los modelos Gemini soportan ventanas de contexto muy largas:

- **Gemini 3 Flash / 2.5 Flash**: Hasta 1 millón de tokens
- **Gemini 3.1 Pro / 2.5 Pro**: Hasta 1 millón de tokens (3.1 Pro) / 2 millones de tokens (2.5 Pro)

Aprovechando esta característica, puede incluir más resultados de búsqueda en el contexto.

::

    # Incluir mas documentos en el contexto (configurar en fess_config.properties)
    rag.llm.gemini.answer.context.max.chars=20000

Estimación de costos
--------------------

La API de Google AI cobra según el uso (con cuota gratuita disponible).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modelo
     - Entrada (1M caracteres)
     - Salida (1M caracteres)
   * - Gemini 3 Flash Preview
     - $0.50
     - $3.00
   * - Gemini 3.1 Pro Preview
     - $2.00
     - $12.00
   * - Gemini 2.5 Flash
     - $0.075
     - $0.30
   * - Gemini 2.5 Pro
     - $1.25
     - $5.00

.. note::
   Para los precios más recientes e información sobre la cuota gratuita, consulte `Google AI Pricing <https://ai.google.dev/pricing>`__.

Control de solicitudes simultáneas
====================================

En |Fess|, se puede controlar el número de solicitudes simultáneas a Gemini.
Configure la siguiente propiedad en ``fess_config.properties``.

::

    # Numero maximo de solicitudes simultaneas (predeterminado: 5)
    rag.llm.gemini.max.concurrent.requests=5

Esta configuración permite prevenir solicitudes excesivas a la API de Google AI y evitar errores de límite de tasa.

Límites de la cuota gratuita (referencia)
-----------------------------------------

La API de Google AI tiene una cuota gratuita, pero con las siguientes limitaciones:

- Solicitudes/minuto: 15 RPM
- Tokens/minuto: 1 millón TPM
- Solicitudes/día: 1,500 RPD

Se recomienda configurar ``rag.llm.gemini.max.concurrent.requests`` a un valor bajo cuando se usa la cuota gratuita.

Solución de problemas
=====================

Error de autenticación
----------------------

**Síntoma**: Errores relacionados con la clave API

**Verificaciones**:

1. Verificar que la clave API esté configurada correctamente
2. Confirmar que la clave API sea válida en Google AI Studio
3. Confirmar que la clave API tenga los permisos necesarios
4. Verificar que la API esté habilitada en el proyecto

Error de límite de tasa
-----------------------

**Síntoma**: Error "429 Resource has been exhausted"

**Solución**:

1. Reducir el número de solicitudes simultáneas en ``fess_config.properties``::

    rag.llm.gemini.max.concurrent.requests=3

2. Esperar unos minutos y reintentar
3. Solicitar aumento de cuota si es necesario

Restricción de región
---------------------

**Síntoma**: Error de que el servicio no está disponible

**Verificaciones**:

La API de Google AI solo está disponible en ciertas regiones.
Consulte la documentación de Google para las regiones soportadas.

Timeout
-------

**Síntoma**: Las solicitudes tienen timeout

**Solución**:

1. Extender el tiempo de timeout::

    rag.llm.gemini.timeout=120000

2. Considerar usar el modelo Flash (más rápido)

Configuración de depuración
---------------------------

Para investigar problemas, puede ajustar el nivel de log de |Fess| para obtener logs detallados relacionados con Gemini.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

Notas de seguridad
==================

Al usar la API de Google AI, tenga en cuenta los siguientes aspectos de seguridad.

1. **Privacidad de datos**: El contenido de los resultados de búsqueda se envía a los servidores de Google
2. **Gestión de claves API**: La filtración de claves puede llevar a uso no autorizado
3. **Cumplimiento**: Si incluye datos confidenciales, verifique las políticas de su organización
4. **Términos de uso**: Cumpla con los términos de uso y la Política de Uso Aceptable de Google

Información de referencia
=========================

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - Descripción general de integración LLM
- :doc:`rag-chat` - Detalles de la funcionalidad de modo de búsqueda IA
- :doc:`rank-fusion` - Búsqueda híbrida: combina búsqueda por palabras clave y búsqueda semántica (vectorial)
- :doc:`../user/chat-search` - Uso del modo de búsqueda IA (guía para el usuario final)
