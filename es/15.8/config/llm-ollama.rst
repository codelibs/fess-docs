=========================================
Configuración de Ollama (LLM Local / RAG)
=========================================

Descripción general
===================

Esta página explica cómo configurar el plugin ``fess-llm-ollama`` para que |Fess| pueda usar un modelo Ollama alojado localmente en su **modo de búsqueda IA (RAG: Retrieval-Augmented Generation)** — respondiendo preguntas en lenguaje natural a partir de su índice de búsqueda empresarial con fuentes citadas, sin enviar datos a una API externa. |Fess| llama a la API local de Ollama para ejecutar RAG sobre sus documentos rastreados.

Ollama es una plataforma de código abierto para ejecutar modelos de lenguaje grandes (LLM) en entorno local.
La funcionalidad de integración con Ollama de |Fess| se proporciona como plugin ``fess-llm-ollama`` y es adecuada para uso en entornos privados.

Al usar Ollama, puede utilizar la funcionalidad del modo de búsqueda IA sin enviar datos al exterior.

Características principales
----------------------------

- **Ejecución local**: Los datos no se envían externamente, asegurando privacidad
- **Modelos diversos**: Compatible con muchos modelos como Llama, Mistral, Gemma, CodeLlama
- **Eficiencia de costos**: Sin costos de API (solo costos de hardware)
- **Personalización**: También puede usar modelos con ajuste fino personalizado

Modelos compatibles
--------------------

Principales modelos disponibles en Ollama:

- ``llama3.3:70b`` - Llama 3.3 de Meta (70B parámetros)
- ``gemma4:e4b`` - Gemma 4 de Google (E4B parámetros, predeterminado)
- ``mistral:7b`` - Mistral de Mistral AI (7B parámetros)
- ``codellama:13b`` - Code Llama de Meta (13B parámetros)
- ``phi3:3.8b`` - Phi-3 de Microsoft (3.8B parámetros)

.. note::
   Para la lista más reciente de modelos disponibles, consulte `Ollama Library <https://ollama.com/library>`__.

Requisitos previos
==================

Antes de usar Ollama, verifique lo siguiente.

1. **Instalación de Ollama**: Descargue e instale desde `https://ollama.com/ <https://ollama.com/>`__
2. **Descarga de modelo**: Descargue el modelo a usar en Ollama
3. **Inicio del servidor Ollama**: Confirme que Ollama esté ejecutándose

Instalación de Ollama
---------------------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

Descargue y ejecute el instalador desde el sitio oficial.

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

Descarga de modelos
-------------------

::

    # Descargar el modelo predeterminado (Gemma 4 E4B)
    ollama pull gemma4:e4b

    # Descargar Llama 3.3
    ollama pull llama3.3:70b

    # Verificar funcionamiento del modelo
    ollama run gemma4:e4b "Hello, how are you?"

Instalación del plugin
======================

La funcionalidad de integración con Ollama se proporciona como plugin.
Para usar Ollama es necesario instalar el plugin ``fess-llm-ollama``.

1. Descargue `fess-llm-ollama-15.8.0.jar`.
2. Colóquelo en el directorio ``app/WEB-INF/plugin/`` del directorio de instalación de |Fess|.

::

    cp fess-llm-ollama-15.8.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Reinicie |Fess|.

.. note::
   La versión del plugin debe coincidir con la versión de |Fess|.

Configuración básica
====================

La configuración relacionada con LLM se divide en múltiples archivos de configuración.

Configuración mínima
--------------------

``system.properties`` (también configurable en Administración > Sistema > General):

::

    # Configurar el proveedor LLM como Ollama
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # URL de Ollama (para entorno local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modelo a usar
    rag.llm.ollama.model=gemma4:e4b

.. note::
   La configuración del proveedor LLM también se puede configurar desde la pantalla de administración (Administración > Sistema > General) estableciendo ``rag.llm.name``.

Configuración recomendada (entorno de producción)
-------------------------------------------------

``system.properties`` (también configurable en Administración > Sistema > General):

::

    # Configuración del proveedor LLM
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # URL de Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuración del modelo (usar modelo grande)
    rag.llm.ollama.model=llama3.3:70b

    # Configuración de timeout (aumentar para modelos grandes)
    rag.llm.ollama.timeout=120000

    # Control del número de solicitudes simultáneas
    rag.llm.ollama.max.concurrent.requests=5

Elementos de configuración
==========================

Todos los elementos de configuración disponibles para el cliente de Ollama. Todos excepto ``rag.llm.name`` se configuran en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.ollama.api.url``
     - URL base del servidor Ollama
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - Nombre del modelo a usar (modelo descargado en Ollama)
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - Timeout de solicitud (milisegundos)
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - Intervalo de verificación de disponibilidad (segundos). Si se especifica ``0`` o un valor menor, se deshabilita la verificación periódica de disponibilidad
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Número máximo de solicitudes simultáneas
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Número máximo de documentos relevantes en la evaluación
     - ``3``
   * - ``rag.llm.ollama.concurrency.wait.timeout``
     - Timeout de espera para la obtención del permiso de control de concurrencia (milisegundos)
     - ``30000``
   * - ``rag.llm.ollama.connect.timeout``
     - Timeout de conexión TCP (milisegundos). Se puede especificar de forma independiente a ``rag.llm.ollama.timeout``
     - ``5000``
   * - ``rag.llm.ollama.retry.max``
     - Número máximo de reintentos HTTP (en errores ``429`` y de la familia ``5xx``)
     - ``3``
   * - ``rag.llm.ollama.retry.base.delay.ms``
     - Retardo base del backoff exponencial (milisegundos)
     - ``2000``

Configuración detallada
-----------------------

Elementos de configuración detallados relacionados con el historial y el tamaño del contexto.

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.ollama.chat.evaluation.description.max.chars``
     - Número máximo de caracteres de la descripción en la evaluación
     - ``500``
   * - ``rag.llm.ollama.history.max.chars``
     - Número máximo de caracteres del historial de conversación
     - ``4000``
   * - ``rag.llm.ollama.intent.history.max.messages``
     - Número máximo de mensajes del historial en la determinación de intención
     - ``6``
   * - ``rag.llm.ollama.intent.history.max.chars``
     - Número máximo de caracteres del historial en la determinación de intención
     - ``3000``
   * - ``rag.llm.ollama.history.assistant.max.chars``
     - Número máximo de caracteres del historial de respuestas del asistente
     - ``500``
   * - ``rag.llm.ollama.history.assistant.summary.max.chars``
     - Número máximo de caracteres del historial de resúmenes del asistente
     - ``500``

Control de concurrencia
-----------------------

Usando ``rag.llm.ollama.max.concurrent.requests``, puede controlar el número de solicitudes simultáneas a Ollama.
El valor predeterminado es 5. Ajústelo según los recursos del servidor Ollama.
Si el número de solicitudes simultáneas es demasiado alto, puede sobrecargar el servidor Ollama y reducir la velocidad de respuesta.

Configuración por tipo de prompt
=================================

En |Fess|, se pueden personalizar los parámetros del LLM por tipo de prompt.
La configuración se escribe en ``fess_config.properties``.

Se pueden configurar los siguientes parámetros por tipo de prompt:

- ``rag.llm.ollama.{promptType}.temperature`` - Temperature en la generación
- ``rag.llm.ollama.{promptType}.max.tokens`` - Número máximo de tokens (mapeado a ``num_predict`` en la API de Ollama)
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Número máximo de caracteres del contexto
- ``rag.llm.ollama.{promptType}.thinking.budget`` - Presupuesto de pensamiento (control de pensamiento en formato booleano; consulte "Soporte de modelo de pensamiento" para más detalles)
- ``rag.llm.ollama.{promptType}.thinking.level`` - Nivel de pensamiento (formato de cadena ``high`` / ``medium`` / ``low``; consulte "Soporte de modelo de pensamiento" para más detalles)
- ``rag.llm.ollama.{promptType}.top.p`` - Valor de muestreo Top-P
- ``rag.llm.ollama.{promptType}.top.k`` - Valor de muestreo Top-K
- ``rag.llm.ollama.{promptType}.num.ctx`` - Tamaño de la ventana de contexto

Cada parámetro se resuelve en el siguiente orden: ``rag.llm.ollama.{promptType}.<param>`` (configuración específica por tipo de prompt) → ``rag.llm.ollama.default.<param>`` (valor de reserva común para todos los tipos de prompt) → valor predeterminado codificado por tipo de prompt. Los valores especificados explícitamente en la solicitud siempre tienen prioridad.

Tipos de prompt disponibles:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tipo de prompt
     - Descripción
   * - ``intent``
     - Prompt para determinar la intención del usuario
   * - ``evaluation``
     - Prompt de evaluación de resultados de búsqueda
   * - ``unclear``
     - Prompt de respuesta para consultas no claras
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

Cada tipo de prompt tiene valores predeterminados codificados que se aplican cuando se omite la configuración.

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Tipo de prompt
     - temperature
     - max.tokens
     - thinking.budget
     - context.max.chars
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
     - ``6000``
   * - ``evaluation``
     - ``0.1``
     - ``512``
     - ``0``
     - ``6000``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - (sin definir)
     - ``10000``
   * - ``summary``
     - ``0.3``
     - ``8192``
     - (sin definir)
     - ``10000``
   * - ``faq``
     - ``0.7``
     - ``4096``
     - (sin definir)
     - ``6000``
   * - ``direct``
     - ``0.7``
     - ``4096``
     - (sin definir)
     - ``6000``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``
     - ``6000``

Ejemplo de configuración::

    # Configurar la temperature en la generación de respuestas
    rag.llm.ollama.answer.temperature=0.7

    # Configurar el número máximo de tokens en la generación de resúmenes
    rag.llm.ollama.summary.max.tokens=2048

    # Configurar el número máximo de caracteres de contexto en la determinación de intención
    rag.llm.ollama.intent.context.max.chars=4000

Opciones de modelo Ollama
==========================

Los parámetros del modelo Ollama se pueden configurar en ``fess_config.properties``.
Al especificarlos con el formato ``rag.llm.ollama.default.<param>``, se usan como valor de reserva común para todos los tipos de prompt.
El mecanismo de reserva mediante ``default`` se aplica no solo a ``top.p`` / ``top.k`` / ``num.ctx``, sino también a ``temperature`` / ``max.tokens`` / ``thinking.budget`` / ``thinking.level``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.ollama.default.top.p``
     - Valor de muestreo Top-P (0.0 a 1.0). Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.top.p``
     - (sin definir)
   * - ``rag.llm.ollama.default.top.k``
     - Valor de muestreo Top-K. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.top.k``
     - (sin definir)
   * - ``rag.llm.ollama.default.num.ctx``
     - Tamaño de la ventana de contexto. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.num.ctx``
     - (sin definir)
   * - ``rag.llm.ollama.default.temperature``
     - Valor de reserva de temperature en la generación. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.temperature``
     - (sin definir)
   * - ``rag.llm.ollama.default.max.tokens``
     - Valor de reserva del número máximo de tokens. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.max.tokens``
     - (sin definir)
   * - ``rag.llm.ollama.default.thinking.budget``
     - Valor de reserva del presupuesto de pensamiento. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.thinking.budget``
     - (sin definir)
   * - ``rag.llm.ollama.default.thinking.level``
     - Valor de reserva del nivel de pensamiento (``high`` / ``medium`` / ``low``). Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.thinking.level``
     - (sin definir)
   * - ``rag.llm.ollama.options.*``
     - Opciones globales pasadas directamente a la API de Ollama. El sufijo se usa como nombre de opción (ejemplo: ``rag.llm.ollama.options.repeat_penalty=1.1``). Los valores se convierten automáticamente a Integer, Double, Boolean o String
     - (sin definir)

Ejemplo de configuración::

    # Muestreo Top-P predeterminado (común para todos los tipos de prompt)
    rag.llm.ollama.default.top.p=0.9

    # Muestreo Top-K predeterminado
    rag.llm.ollama.default.top.k=40

    # Tamaño de ventana de contexto predeterminado
    rag.llm.ollama.default.num.ctx=4096

    # Cambiar Top-P solo en la generación de respuestas
    rag.llm.ollama.answer.top.p=0.95

    # Opciones globales (pasadas directamente a la API de Ollama)
    rag.llm.ollama.options.repeat_penalty=1.1

Soporte de modelo de pensamiento
==================================

Cuando se usa un modelo de pensamiento (thinking model) como gemma4 o qwen3, |Fess| soporta la configuración del presupuesto de pensamiento (thinking budget).

El presupuesto de pensamiento se configura por tipo de prompt en ``fess_config.properties``:

::

    # Configuración del presupuesto de pensamiento en la generación de respuestas
    rag.llm.ollama.answer.thinking.budget=1024

    # Configuración del presupuesto de pensamiento en la generación de resúmenes
    rag.llm.ollama.summary.thinking.budget=1024

Al configurar el presupuesto de pensamiento, puede controlar el número de tokens asignados al paso de "pensar" antes de que el modelo genere una respuesta.

.. note::
   En Ollama, el presupuesto de pensamiento se convierte a un flag booleano (si el valor es mayor que 0, se usa ``think: true``; si es 0, se usa ``think: false``). El control detallado por número de tokens no está disponible debido a las restricciones de la API de Ollama.

Nivel de pensamiento (thinking level)
--------------------------------------

Algunos modelos como gpt-oss ignoran el flag ``think`` en formato booleano y requieren la especificación del nivel de pensamiento mediante el formato de cadena ``high`` / ``medium`` / ``low``.
Para este tipo de modelos, use ``rag.llm.ollama.{promptType}.thinking.level``.

::

    # Configuración del nivel de pensamiento en la generación de respuestas
    rag.llm.ollama.answer.thinking.level=high

    # Configuración del nivel de pensamiento en la generación de resúmenes
    rag.llm.ollama.summary.thinking.level=medium

Los valores que se pueden establecer en ``thinking.level`` son ``high`` / ``medium`` / ``low`` (sin distinción de mayúsculas y minúsculas). Si se especifica un valor no válido, se ignora y se emite un log de advertencia.

.. note::
   Si tanto ``thinking.level`` (formato de cadena) como ``thinking.budget`` (formato booleano) están configurados, ``thinking.level`` tiene prioridad. Use ``thinking.level`` para modelos de la familia GPT-OSS y ``thinking.budget`` para otros modelos de pensamiento.

Configuración de red
====================

Configuración con Docker
------------------------

El repositorio oficial `docker-fess <https://github.com/codelibs/docker-fess>`__ de |Fess| incluye un overlay para Ollama ``compose-ollama.yaml``. Los pasos mínimos son los siguientes.

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

``compose-ollama.yaml`` está configurado para usar GPU NVIDIA (se requiere NVIDIA Container Toolkit). Su contenido es el siguiente.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.8.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434"
        depends_on:
          - ollama01

      ollama01:
        image: ollama/ollama:latest
        container_name: ollama01
        ports:
          - "11434:11434"
        volumes:
          - ollama-data:/root/.ollama
        networks:
          - search_net
        restart: unless-stopped
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

    volumes:
      ollama-data:
        driver: local

Puntos clave:

- ``FESS_PLUGINS=fess-llm-ollama:15.8.0`` hace que el script de inicio obtenga automáticamente el JAR del plugin y lo coloque en ``app/WEB-INF/plugin/`` (ajuste la versión a la de su |Fess|)
- ``-Dfess.config.rag.chat.enabled=true`` habilita el modo de búsqueda IA
- ``-Dfess.config.rag.llm.ollama.api.url=...`` especifica la URL del servidor Ollama (dentro de la red de Docker Compose se resuelve por el nombre del servicio, como ``ollama01``)
- El valor predeterminado del proveedor LLM (``rag.llm.name``) es ``ollama``, por lo que si solo se usa Ollama no es necesaria una especificación explícita. Si se cambia desde otro proveedor, agregue ``-Dfess.system.rag.llm.name=ollama`` a ``FESS_JAVA_OPTS`` o configúrelo después del inicio en la pantalla de administración "Sistema > General", sección RAG
- El bloque ``deploy.resources.reservations.devices`` es la configuración para usar GPU. Si no se usa GPU (ejecutando solo con CPU), elimine este bloque

.. note::
   Las variables de entorno en formato snake_case en mayúsculas como ``RAG_CHAT_ENABLED`` o ``RAG_LLM_NAME`` no son reconocidas directamente por |Fess|. Los valores de configuración deben pasarse siempre dentro de ``FESS_JAVA_OPTS`` como ``-Dfess.config.<key>`` (familia ``fess_config.properties``) o ``-Dfess.system.<key>`` (familia ``system.properties``).

Servidor Ollama remoto
----------------------

Cuando se ejecuta Ollama en un servidor diferente a Fess:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama no tiene funcionalidad de autenticación por defecto, por lo que si lo hace accesible externamente,
   considere medidas de seguridad a nivel de red (firewall, VPN, etc.).

Uso a través de proxy HTTP
==========================

El cliente de Ollama comparte la configuración de proxy HTTP común de |Fess|. Si necesita pasar por un proxy para conectarse al servidor Ollama (por ejemplo al usar un servidor Ollama remoto), especifique las siguientes propiedades en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``http.proxy.host``
     - Nombre del host del proxy (si la cadena está vacía, no se usa proxy)
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

.. note::
   Como Ollama normalmente se ejecuta en local o dentro de la red interna, la configuración de proxy solo es necesaria en casos limitados (por ejemplo, cuando se usa un servidor Ollama remoto al que solo se puede llegar a través del proxy corporativo).
   Esta configuración también afecta el acceso HTTP de todo |Fess|, incluido el crawler.

Guía de selección de modelos
============================

Guía para la selección de modelos según el propósito de uso.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modelo
     - Tamaño
     - VRAM requerida
     - Uso
   * - ``phi3:3.8b``
     - Pequeño
     - 4GB+
     - Entornos ligeros, respuestas simples
   * - ``gemma4:e4b``
     - Pequeño-Medio
     - 8GB+
     - Uso general equilibrado, soporte de thinking (predeterminado)
   * - ``mistral:7b``
     - Medio
     - 8GB+
     - Cuando se requieren respuestas de alta calidad
   * - ``llama3.3:70b``
     - Grande
     - 48GB+
     - Respuestas de máxima calidad, razonamiento complejo

Soporte de GPU
--------------

Ollama soporta aceleración por GPU. El uso de GPUs NVIDIA mejora significativamente
la velocidad de inferencia.

::

    # Verificar soporte de GPU
    ollama run gemma4:e4b --verbose

Solución de problemas
=====================

Error de conexión
-----------------

**Síntoma**: Errores en la funcionalidad de chat, LLM mostrado como no disponible

**Verificaciones**:

1. Verificar que Ollama esté ejecutándose::

    curl http://localhost:11434/api/tags

2. Verificar que el modelo esté descargado::

    ollama list

3. Verificar la configuración del firewall

4. Verificar que el plugin ``fess-llm-ollama`` esté colocado en ``app/WEB-INF/plugin/``

Modelo no encontrado
--------------------

**Síntoma**: Se muestra en el log "Configured model not found"

**Solución**:

1. Verificar que el nombre del modelo sea exacto (puede incluir el tag ``:latest``)::

    # Verificar lista de modelos
    ollama list

2. Descargar el modelo necesario::

    ollama pull gemma4:e4b

Timeout
-------

**Síntoma**: Las solicitudes tienen timeout

**Solución**:

1. Extender el tiempo de timeout::

    rag.llm.ollama.timeout=120000

2. Usar un modelo más pequeño o considerar un entorno con GPU

Configuración de depuración
---------------------------

Para investigar problemas, puede ajustar el nivel de log de |Fess| para obtener logs detallados relacionados con Ollama.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

Información de referencia
=========================

- `Sitio oficial de Ollama <https://ollama.com/>`__
- `Biblioteca de modelos Ollama <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - Descripción general de integración LLM
- :doc:`rag-chat` - Detalles de la funcionalidad de modo de búsqueda IA
- :doc:`rank-fusion` - Búsqueda híbrida: combina búsqueda por palabras clave y búsqueda semántica (vectorial)
- :doc:`../user/chat-search` - Uso del modo de búsqueda IA (guía para el usuario final)
