================================================================
Descripción general de la búsqueda IA (RAG) y la integración LLM
================================================================

Descripción general
===================

|Fess| soporta la funcionalidad de modo de búsqueda IA (RAG: Retrieval-Augmented Generation) que aprovecha los modelos de lenguaje de gran escala (LLM).
Esta funcionalidad permite a los usuarios obtener información mediante un diálogo interactivo con un asistente de IA basado en los resultados de búsqueda, respondiendo preguntas en lenguaje natural directamente desde su índice de búsqueda empresarial con fuentes citadas.

La funcionalidad de integración con LLM se proporciona como plugins ``fess-llm-*``. Instale el plugin correspondiente al proveedor LLM que desea utilizar.

El modo de búsqueda IA obtiene los documentos a través del pipeline estándar de búsqueda de |Fess| (rank fusion), no de un índice vectorial independiente; por defecto se utiliza búsqueda por palabras clave (BM25). Como reutiliza este pipeline, si instala y configura el plugin de Búsqueda Semántica, su buscador semántico (vectorial) participa en el rank fusion de todas las búsquedas, incluido el paso de recuperación del modo de búsqueda IA; no se requiere ninguna configuración específica para el modo de búsqueda IA. Consulte :doc:`rank-fusion`.

Proveedores compatibles
=======================

|Fess| soporta los siguientes proveedores de LLM.

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Proveedor
     - Valor de configuración
     - Plugin
     - Descripción
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - Servidor LLM de código abierto que se ejecuta en entorno local. Puede ejecutar modelos como Llama, Mistral, Gemma. Configuración predeterminada.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - API en la nube de OpenAI. Disponible para modelos como GPT-4.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - API en la nube de Google. Disponible para modelos Gemini.

Comparación de proveedores
--------------------------

.. list-table::
   :header-rows: 1

   * - Proveedor (``rag.llm.name``)
     - Modelo predeterminado
     - Endpoint
     - Autenticación
     - Ubicación de los datos
   * - Ollama (``ollama``)
     - ``gemma4:e4b``
     - ``http://localhost:11434``
     - Ninguna (local)
     - Local / autoalojado — la pregunta y los documentos permanecen en su host
   * - OpenAI (``openai``)
     - ``gpt-5-mini``
     - ``https://api.openai.com/v1``
     - ``Authorization: Bearer`` (``rag.llm.openai.api.key``)
     - Nube — la pregunta y los documentos recuperados se envían a OpenAI
   * - Google Gemini (``gemini``)
     - ``gemini-3.1-flash-lite-preview``
     - ``https://generativelanguage.googleapis.com/v1beta``
     - ``x-goog-api-key`` (``rag.llm.gemini.api.key``)
     - Nube — la pregunta y los documentos recuperados se envían a Google

.. note::

   Si ``rag.llm.name`` no está configurado, de forma predeterminada solo el cliente Ollama está activo; instale y seleccione el proveedor que desee con ``rag.llm.name``.

Instalación del plugin
======================

La funcionalidad LLM se proporciona como plugin. Es necesario colocar el archivo JAR del plugin ``fess-llm-{provider}`` correspondiente al proveedor que desea utilizar en el directorio de plugins.

Por ejemplo, para usar el proveedor OpenAI, descargue ``fess-llm-openai-15.7.0.jar`` y colóquelo en el siguiente directorio.

::

    app/WEB-INF/plugin/

Después de colocarlo, reinicie |Fess| para que el plugin sea cargado.

Arquitectura
============

La funcionalidad de modo de búsqueda IA opera con el siguiente flujo.

1. **Entrada del usuario**: El usuario ingresa una pregunta en la interfaz de chat
2. **Análisis de intención (intent)**: El LLM analiza la pregunta del usuario y extrae palabras clave de búsqueda
3. **Ejecución de búsqueda (search)**: Busca documentos relacionados usando el motor de búsqueda de |Fess|
4. **Evaluación de resultados (evaluate)**: El LLM evalúa la relevancia de los resultados de búsqueda y selecciona los documentos más apropiados
5. **Regeneración de consulta (si es necesario)**: Si no se obtienen resultados de búsqueda o no se encuentran documentos relevantes en la evaluación, el LLM regenera la consulta y realiza una nueva búsqueda
6. **Obtención de contenido (fetch)**: Se obtiene el cuerpo de texto de los documentos seleccionados
7. **Generación de respuesta (answer)**: El LLM genera una respuesta basada en los documentos obtenidos (con renderizado Markdown)
8. **Cita de fuentes**: La respuesta incluye enlaces a los documentos de referencia

.. note::

   El procesamiento interno se compone de cinco fases: ``intent``, ``search``, ``evaluate``, ``fetch`` y ``answer``. El progreso de cada fase se notifica al cliente mediante streaming (SSE).

Configuración básica
====================

La configuración de la funcionalidad LLM se realiza en los siguientes dos lugares.

Configuración general de la pantalla de administración / system.properties
---------------------------------------------------------------------------

Se configura en la configuración general de la pantalla de administración o en ``system.properties``. Se usa para la selección del proveedor LLM.

::

    # Especificar el proveedor LLM (ollama, openai, gemini)
    rag.llm.name=ollama

fess_config.properties
-----------------------

Se configura en ``app/WEB-INF/conf/fess_config.properties``. Además de habilitar el modo de búsqueda IA y configurar sesiones e historial, también se describen en este archivo la configuración específica del proveedor (URL de conexión, clave API, parámetros de generación, etc.).

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # Ejemplo de configuración específica del proveedor (en el caso de OpenAI)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

Para la configuración detallada de cada proveedor, consulte los siguientes documentos.

- :doc:`llm-ollama` - Configuración de Ollama
- :doc:`llm-openai` - Configuración de OpenAI
- :doc:`llm-gemini` - Configuración de Google Gemini

Configuración común
===================

Elementos de configuración utilizados en común por todos los proveedores LLM. Estos se configuran en ``fess_config.properties``.

Configuración de contexto
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.chat.context.max.documents``
     - Número máximo de documentos a incluir en el contexto
     - ``5``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,doc_id,content_title,content_description``

.. note::

   El número máximo de caracteres del contexto (``context.max.chars``) ha sido modificado a una configuración por proveedor y por tipo de prompt. Configúrelo en ``fess_config.properties`` como ``rag.llm.{provider}.{promptType}.context.max.chars``.

Prompt del sistema
------------------

Los prompts del sistema se gestionan en el archivo DI XML de cada plugin, no en archivos de propiedades.

Los prompts del sistema están definidos en el archivo ``fess_llm++.xml`` incluido dentro del archivo JAR de cada plugin ``fess-llm-*``. Dado que este archivo es un recurso de classpath incluido en el JAR del plugin, para personalizar los prompts es necesario editar el archivo DI XML dentro del JAR.

Verificación de disponibilidad
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.{provider}.availability.check.interval``
     - Intervalo para verificar la disponibilidad del LLM (segundos). 0 para deshabilitar
     - ``60``

Esta configuración se realiza en ``fess_config.properties``. |Fess| verifica periódicamente el estado de conexión del proveedor LLM.

Gestión de sesiones
===================

Configuración relacionada con las sesiones de chat. Estas se configuran en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.chat.session.timeout.minutes``
     - Tiempo de espera de la sesión (minutos)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Número máximo de sesiones
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Número máximo de mensajes a mantener en el historial de conversación
     - ``30``

Control de concurrencia
=======================

Configuración que controla el número de solicitudes simultáneas al LLM. Se configura en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - Número máximo de solicitudes simultáneas al proveedor
     - ``5``
   * - ``rag.llm.{provider}.concurrency.wait.timeout``
     - Tiempo máximo de espera (en milisegundos) cuando se alcanza el límite de concurrencia. Si no se obtiene disponibilidad dentro de este tiempo, se produce un error de límite de tasa
     - ``30000``

Por ejemplo, para configurar el número de solicitudes simultáneas del proveedor OpenAI, se hace de la siguiente manera.

::

    rag.llm.openai.max.concurrent.requests=10

Configuración de evaluación
============================

Configuración relacionada con la evaluación de los resultados de búsqueda. Se configura en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - Número máximo de documentos relevantes a seleccionar en la fase de evaluación
     - ``3``

Configuración por tipo de prompt
=================================

Los parámetros de generación se pueden configurar por tipo de prompt. Esto permite ajustes detallados según el uso. La configuración se realiza en ``fess_config.properties``.

Lista de tipos de prompt
------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Tipo de prompt
     - Valor de configuración
     - Descripción
   * - Análisis de intención
     - ``intent``
     - Analiza la pregunta del usuario y extrae palabras clave de búsqueda
   * - Evaluación
     - ``evaluation``
     - Evalúa la relevancia de los resultados de búsqueda
   * - Pregunta ambigua
     - ``unclear``
     - Genera una respuesta cuando la pregunta no está clara
   * - Sin resultados de búsqueda
     - ``noresults``
     - Genera una respuesta cuando no se encuentran resultados de búsqueda
   * - Documento no encontrado
     - ``docnotfound``
     - Genera una respuesta cuando no existe el documento correspondiente
   * - Generación de respuesta
     - ``answer``
     - Genera una respuesta basada en los resultados de búsqueda
   * - Resumen
     - ``summary``
     - Genera un resumen del documento
   * - FAQ
     - ``faq``
     - Genera una respuesta en formato FAQ
   * - Respuesta directa
     - ``direct``
     - Genera una respuesta directa sin pasar por la búsqueda
   * - Regeneración de consulta
     - ``queryregeneration``
     - Regenera la consulta cuando no se obtienen resultados de búsqueda

Patrón de configuración
-----------------------

La configuración por tipo de prompt se especifica con el siguiente patrón.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

Ejemplo de configuración (en el caso del proveedor OpenAI):

::

    # Configurar la temperatura de generación de respuestas a un valor bajo
    rag.llm.openai.answer.temperature=0.5
    # Número máximo de tokens para generación de respuestas
    rag.llm.openai.answer.max.tokens=4096
    # El análisis de intención es suficiente con respuestas cortas, por lo que se configura bajo
    rag.llm.openai.intent.max.tokens=256
    # Número máximo de caracteres de contexto para resumen
    rag.llm.openai.summary.context.max.chars=8000

.. note::

   ``temperature``, ``max.tokens`` y ``context.max.chars`` son parámetros comunes a todos los proveedores. Además, cada proveedor soporta parámetros específicos como ``thinking.budget``, ``top.p`` y ``reasoning.effort``. Consulte la documentación de cada proveedor para más detalles.

Siguientes pasos
================

- :doc:`llm-ollama` - Configuración detallada de Ollama
- :doc:`llm-openai` - Configuración detallada de OpenAI
- :doc:`llm-gemini` - Configuración detallada de Google Gemini
- :doc:`rag-chat` - Configuración detallada de la funcionalidad de modo de búsqueda IA
- :doc:`rank-fusion` - Configuración de Rank Fusion (fusión de resultados de búsqueda híbrida)
