==========================
Descripcion general de integracion LLM
==========================

Descripcion general
===================

|Fess| 15.7 soporta la funcionalidad de modo de búsqueda IA (RAG: Retrieval-Augmented Generation) que aprovecha modelos de lenguaje grandes (LLM).
Esta funcionalidad permite a los usuarios obtener informacion a traves de un dialogo interactivo con un asistente de IA basado en los resultados de busqueda.

En |Fess| 15.7, la funcionalidad de integracion con LLM se proporciona como plugins ``fess-llm-*``. Instale el plugin correspondiente al proveedor LLM que desea utilizar.

Proveedores compatibles
=======================

|Fess| soporta los siguientes proveedores de LLM.

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Proveedor
     - Valor de configuracion
     - Plugin
     - Descripcion
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - Servidor LLM de codigo abierto que se ejecuta en entorno local. Puede ejecutar modelos como Llama, Mistral, Gemma. Configuracion predeterminada.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - API en la nube de OpenAI. Disponible para modelos como GPT-4.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - API en la nube de Google. Disponible para modelos Gemini.

Instalacion de plugin
=====================

En |Fess| 15.7, la funcionalidad LLM esta separada como plugin. Es necesario colocar el archivo JAR del plugin ``fess-llm-{provider}`` correspondiente al proveedor que desea utilizar en el directorio de plugins.

Por ejemplo, para usar el proveedor OpenAI, descargue ``fess-llm-openai-15.7.0.jar`` y coloquelo en el siguiente directorio.

::

    app/WEB-INF/plugin/

Despues de colocarlo, reinicie |Fess| para que el plugin sea cargado.

Arquitectura
============

La funcionalidad de modo de búsqueda IA opera con el siguiente flujo.

1. **Entrada del usuario**: El usuario ingresa una pregunta en la interfaz de chat
2. **Analisis de intencion**: El LLM analiza la pregunta del usuario y extrae palabras clave de busqueda
3. **Ejecucion de busqueda**: Busca documentos relacionados usando el motor de busqueda de |Fess|
4. **Regeneracion de consulta**: Cuando no se encuentran resultados, el LLM regenera la consulta y reintenta
5. **Evaluacion de resultados**: El LLM evalua la relevancia de los resultados de busqueda y selecciona los documentos mas apropiados
6. **Generacion de respuesta**: El LLM genera una respuesta basada en los documentos seleccionados (con renderizado Markdown)
7. **Cita de fuentes**: La respuesta incluye enlaces a los documentos de referencia

Configuracion basica
====================

La configuracion de la funcionalidad LLM se realiza en los siguientes dos lugares.

Configuracion general de la pantalla de administracion / system.properties
---------------------------------------------------------------------------

Se configura en la configuracion general de la pantalla de administracion o en ``system.properties``. Se usa para la seleccion del proveedor LLM.

::

    # Especificar el proveedor LLM (ollama, openai, gemini)
    rag.llm.name=ollama

fess_config.properties
-----------------------

Se configura en ``app/WEB-INF/conf/fess_config.properties``. Son configuraciones que se cargan al inicio, y se usa para habilitar el modo de búsqueda IA, configurar sesiones e historial, y la configuracion especifica del proveedor (URL de conexion, clave API, parametros de generacion, etc.).

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # Ejemplo de configuracion especifica del proveedor (en el caso de OpenAI)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

Para la configuracion detallada de cada proveedor, consulte los siguientes documentos.

- :doc:`llm-ollama` - Configuracion de Ollama
- :doc:`llm-openai` - Configuracion de OpenAI
- :doc:`llm-gemini` - Configuracion de Google Gemini

Configuracion comun
===================

Configuraciones utilizadas en comun por todos los proveedores LLM. Estas se configuran en ``fess_config.properties``.

Configuracion de contexto
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.context.max.documents``
     - Numero maximo de documentos a incluir en el contexto
     - ``5``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,...``

.. note::

   El numero maximo de caracteres del contexto ( ``context.max.chars`` ) se ha cambiado a una configuracion por proveedor y por tipo de prompt. Configurelo en ``fess_config.properties`` como ``rag.llm.{provider}.{promptType}.context.max.chars``.

Prompt del sistema
------------------

En |Fess| 15.7, los prompts del sistema se gestionan en el archivo DI XML de cada plugin, no en archivos de propiedades.

Los prompts del sistema estan definidos en el archivo ``fess_llm++.xml`` incluido en cada plugin ``fess-llm-*``. Para personalizar los prompts, edite el archivo DI XML en el directorio del plugin.

Verificacion de disponibilidad
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.{provider}.availability.check.interval``
     - Intervalo para verificar la disponibilidad del LLM (segundos). 0 para deshabilitar
     - ``60``

Esta configuracion se realiza en ``fess_config.properties``. |Fess| verifica periodicamente el estado de conexion del proveedor LLM.

Gestion de sesiones
===================

Configuracion relacionada con las sesiones de chat. Estas se configuran en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.session.timeout.minutes``
     - Tiempo de timeout de sesion (minutos)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Numero maximo de sesiones
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Numero maximo de mensajes a mantener en el historial de conversacion
     - ``30``

Control de concurrencia
=======================

Configuracion que controla el numero de solicitudes simultaneas al LLM. Se configura en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - Numero maximo de solicitudes simultaneas al proveedor
     - ``5``

Por ejemplo, para configurar el numero de solicitudes simultaneas del proveedor OpenAI, se hace de la siguiente manera.

::

    rag.llm.openai.max.concurrent.requests=10

Configuracion de evaluacion
============================

Configuracion relacionada con la evaluacion de resultados de busqueda. Se configura en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - Numero maximo de documentos relevantes a seleccionar en la fase de evaluacion
     - ``3``

Configuracion por tipo de prompt
=================================

En |Fess| 15.7, los parametros de generacion se pueden configurar por tipo de prompt. Esto permite ajustes detallados segun el uso. La configuracion se realiza en ``fess_config.properties``.

Lista de tipos de prompt
------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Tipo de prompt
     - Valor de configuracion
     - Descripcion
   * - Analisis de intencion
     - ``intent``
     - Analiza la pregunta del usuario y extrae palabras clave de busqueda
   * - Evaluacion
     - ``evaluation``
     - Evalua la relevancia de los resultados de busqueda
   * - Pregunta ambigua
     - ``unclear``
     - Genera una respuesta cuando la pregunta no esta clara
   * - Sin resultados de busqueda
     - ``noresults``
     - Genera una respuesta cuando no se encuentran resultados de busqueda
   * - Documento no encontrado
     - ``docnotfound``
     - Genera una respuesta cuando no existe el documento correspondiente
   * - Generacion de respuesta
     - ``answer``
     - Genera una respuesta basada en los resultados de busqueda
   * - Resumen
     - ``summary``
     - Genera un resumen del documento
   * - FAQ
     - ``faq``
     - Genera una respuesta en formato FAQ
   * - Respuesta directa
     - ``direct``
     - Genera una respuesta directa sin pasar por la busqueda
   * - Regeneracion de consulta
     - ``queryregeneration``
     - Regenera la consulta cuando no se encuentran resultados de busqueda

Patron de configuracion
-----------------------

La configuracion por tipo de prompt se especifica con el siguiente patron.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

Ejemplo de configuracion (en el caso del proveedor OpenAI):

::

    # Configurar la temperatura de generacion de respuestas a un valor bajo
    rag.llm.openai.answer.temperature=0.5
    # Numero maximo de tokens para generacion de respuestas
    rag.llm.openai.answer.max.tokens=4096
    # El analisis de intencion es suficiente con respuestas cortas, por lo que se configura bajo
    rag.llm.openai.intent.max.tokens=256
    # Numero maximo de caracteres de contexto para resumen
    rag.llm.openai.summary.context.max.chars=8000

Siguientes pasos
================

- :doc:`llm-ollama` - Configuracion detallada de Ollama
- :doc:`llm-openai` - Configuracion detallada de OpenAI
- :doc:`llm-gemini` - Configuracion detallada de Google Gemini
- :doc:`rag-chat` - Configuracion detallada de la funcionalidad de modo de búsqueda IA
- :doc:`rank-fusion` - Configuracion de Rank Fusion (Fusion de resultados de busqueda hibrida)
