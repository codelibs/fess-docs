==========================
Descripcion general de integracion LLM
==========================

Descripcion general
===================

|Fess| 15.5 soporta la funcionalidad de modo IA (RAG: Retrieval-Augmented Generation) que aprovecha modelos de lenguaje grandes (LLM).
Esta funcionalidad permite a los usuarios obtener informacion a traves de un dialogo interactivo con un asistente de IA basado en los resultados de busqueda.

Proveedores compatibles
=======================

|Fess| soporta los siguientes proveedores de LLM.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Proveedor
     - Valor de configuracion
     - Descripcion
   * - Ollama
     - ``ollama``
     - Servidor LLM de codigo abierto que se ejecuta en entorno local. Puede ejecutar modelos como Llama, Mistral, Gemma. Configuracion predeterminada.
   * - OpenAI
     - ``openai``
     - API en la nube de OpenAI. Disponible para modelos como GPT-4.
   * - Google Gemini
     - ``gemini``
     - API en la nube de Google. Disponible para modelos Gemini.

Arquitectura
============

La funcionalidad de modo IA opera con el siguiente flujo.

1. **Entrada del usuario**: El usuario ingresa una pregunta en la interfaz de chat
2. **Analisis de intencion**: El LLM analiza la pregunta del usuario y extrae palabras clave de busqueda
3. **Ejecucion de busqueda**: Busca documentos relacionados usando el motor de busqueda de |Fess|
4. **Evaluacion de resultados**: El LLM evalua la relevancia de los resultados de busqueda y selecciona los documentos mas apropiados
5. **Generacion de respuesta**: El LLM genera una respuesta basada en los documentos seleccionados
6. **Cita de fuentes**: La respuesta incluye enlaces a los documentos de referencia

Configuracion basica
====================

Para habilitar la funcionalidad LLM, agregue la siguiente configuracion en ``app/WEB-INF/conf/fess_config.properties``.

Habilitar modo IA
-----------------

::

    # Habilitar la funcionalidad de modo IA
    rag.chat.enabled=true

Seleccion de proveedor LLM
--------------------------

::

    # Especificar el proveedor LLM (ollama, openai, gemini)
    rag.llm.type=ollama

Para la configuracion detallada de cada proveedor, consulte los siguientes documentos.

- :doc:`llm-ollama` - Configuracion de Ollama
- :doc:`llm-openai` - Configuracion de OpenAI
- :doc:`llm-gemini` - Configuracion de Google Gemini

Configuracion comun
===================

Configuraciones comunes utilizadas por todos los proveedores LLM.

Parametros de generacion
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.max.tokens``
     - Numero maximo de tokens a generar
     - ``4096``
   * - ``rag.chat.temperature``
     - Aleatoriedad de la generacion (0.0-1.0). Valores mas bajos producen respuestas mas deterministas
     - ``0.7``

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
   * - ``rag.chat.context.max.chars``
     - Numero maximo de caracteres del contexto
     - ``4000``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,...``

Prompt del sistema
------------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

Este prompt define el comportamiento basico del LLM. Puede personalizarlo segun sea necesario.

Verificacion de disponibilidad
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.availability.check.interval``
     - Intervalo para verificar la disponibilidad del LLM (segundos). 0 para deshabilitar
     - ``60``

Esta configuracion permite que |Fess| verifique periodicamente el estado de conexion del proveedor LLM.

Gestion de sesiones
===================

Configuracion relacionada con las sesiones de chat.

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
     - ``20``

Limite de tasa
==============

Configuracion de limite de tasa para prevenir sobrecarga de la API.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.rate.limit.enabled``
     - Habilitar limite de tasa
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - Numero maximo de solicitudes por minuto
     - ``10``

Configuracion de evaluacion
===========================

Configuracion relacionada con la evaluacion de resultados de busqueda.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Numero maximo de documentos relevantes a seleccionar en la fase de evaluacion
     - ``3``

Siguientes pasos
================

- :doc:`llm-ollama` - Configuracion detallada de Ollama
- :doc:`llm-openai` - Configuracion detallada de OpenAI
- :doc:`llm-gemini` - Configuracion detallada de Google Gemini
- :doc:`rag-chat` - Configuracion detallada de la funcionalidad de modo IA
- :doc:`rank-fusion` - Configuracion de Rank Fusion (Fusion de resultados de busqueda hibrida)
