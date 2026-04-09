============================================================
Parte 19: Construcción de un asistente de IA interno -- Un sistema de preguntas y respuestas basado en búsqueda con RAG
============================================================

Introducción
============

En el artículo anterior, organizamos los conceptos de búsqueda semántica.
En este artículo, como evolución de ese enfoque, construimos un asistente de IA interno utilizando RAG (Retrieval-Augmented Generation).

RAG es un mecanismo que "encuentra documentos relevantes mediante búsqueda y luego un LLM (modelo de lenguaje grande) genera respuestas basadas en su contenido".
Dado que las respuestas se generan a partir de documentos internos, RAG puede responder preguntas específicas de la empresa que una IA de chat de propósito general no puede contestar.

Audiencia objetivo
==================

- Personas interesadas en construir un asistente de IA interno
- Personas que desean aprender cómo implementar RAG
- Personas que desean comprender las opciones de integración con LLM

Cómo funciona RAG
===================

Pipeline de RAG
----------------

El modo de búsqueda con IA de Fess opera a través del siguiente pipeline:

1. **Análisis de intención (Intent)**: Analiza la pregunta del usuario y clasifica la intención (búsqueda, resumen, FAQ, ambigua)
2. **Búsqueda (Search)**: Recupera documentos relevantes del índice de Fess (regenera automáticamente las consultas y vuelve a buscar cuando no hay resultados)
3. **Evaluación (Evaluate)**: El LLM evalúa la relevancia de los documentos recuperados
4. **Obtención del texto completo (Fetch)**: Recupera el texto completo de los documentos altamente relevantes
5. **Generación de respuesta (Answer)**: El LLM genera una respuesta en streaming con citas basadas en el contenido del documento

Este pipeline mitiga las "respuestas plausibles pero inexactas (alucinaciones)" del LLM y proporciona respuestas respaldadas por documentos internos.

El modo de búsqueda con IA de Fess no requiere búsqueda vectorial (modelos de embeddings).
Aprovecha los índices de búsqueda de texto completo existentes tal cual, con el LLM encargándose de la evaluación de resultados de búsqueda y la generación de respuestas.
Esto significa que puede introducir la búsqueda con IA basada en RAG de inmediato, sin preparación de infraestructura adicional como la selección de modelos de embeddings o la construcción de bases de datos vectoriales.

Elección de un proveedor de LLM
=================================

Fess admite tres backends de LLM.
A continuación se presenta un resumen de las características y criterios de selección de cada proveedor.

.. list-table:: Comparación de proveedores de LLM
   :header-rows: 1
   :widths: 15 25 25 35

   * - Proveedor
     - Plugin
     - Costo
     - Características
   * - OpenAI
     - fess-llm-openai
     - Pago por uso de API
     - Alta calidad de respuesta, soporte GPT-4o, fácil de comenzar
   * - Google Gemini
     - fess-llm-gemini
     - Pago por uso de API
     - Soporte de pensamiento extendido, contexto largo
   * - Ollama
     - fess-llm-ollama
     - Costos de hardware
     - Ejecución local, los datos no salen de la empresa, enfoque en privacidad

Criterios de selección
----------------------

**Cuándo elegir una API en la nube (OpenAI / Gemini)**

- Desea minimizar los costos iniciales
- No puede preparar un servidor con GPU
- La calidad de respuesta es su máxima prioridad
- El envío de datos a servicios externos es aceptable

**Cuándo elegir ejecución local (Ollama)**

- El envío de datos internos a servicios externos no está permitido
- Los requisitos de seguridad y privacidad son estrictos
- Puede preparar un servidor con GPU
- Desea reducir los costos operativos (para uso de alto volumen)

Configuración del modo de búsqueda con IA
============================================

Instalación del plugin
-----------------------

Instale el plugin correspondiente a su proveedor de LLM elegido.

1. Vaya a [Sistema] > [Plugins] en la consola de administración
2. Instale el plugin correspondiente (por ejemplo, ``fess-llm-openai``)

Activación del modo de búsqueda con IA
---------------------------------------

Active el modo de búsqueda con IA en la configuración de Fess.

Establezca ``rag.chat.enabled=true`` en la configuración de la consola de administración o en el archivo de configuración.

Configuración de conexión del LLM
-----------------------------------

Configure la información de conexión para su proveedor de LLM elegido.

**Para OpenAI**

- Clave de API
- Modelo a utilizar (gpt-4o, gpt-4o-mini, etc.)
- Número máximo de tokens

**Para Ollama**

- URL del servidor Ollama
- Nombre del modelo a utilizar
- Adición de un servicio mediante Docker Compose

.. code-block:: yaml

    services:
      ollama:
        image: ollama/ollama
        volumes:
          - ollama-data:/root/.ollama
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

La experiencia del chat con IA
================================

Interfaz de chat
-----------------

Cuando el modo de búsqueda con IA está activado, se agrega el modo de búsqueda con IA a la pantalla de búsqueda de Fess.
Los usuarios pueden alternar entre la búsqueda por palabras clave y el chat con IA.

Ejemplo de pregunta y respuesta
--------------------------------

**Pregunta**: "¿Cómo solicito vacaciones pagadas?"

**Respuesta de la IA**:

    Para solicitar vacaciones pagadas, siga estos pasos:

    1. Acceda a la página de "Gestión de asistencia" en el portal interno
    2. Seleccione "Vacaciones pagadas" en el menú "Solicitud de ausencia"
    3. Ingrese las fechas, seleccione a su superior y envíe la solicitud

    Por favor, envíe su solicitud al menos 3 días hábiles antes de la fecha de vacaciones.

    Referencia: [Reglamento de trabajo, Artículo 15](https://portal/rules/chapter15.html)

La respuesta incluye enlaces a las fuentes, lo que permite a los usuarios verificar los documentos originales.

Uso de la Chat API (SSE)
==========================

Para utilizar el modo de búsqueda con IA desde un programa, utilice la Chat API.
La Chat API devuelve respuestas en streaming mediante Server-Sent Events (SSE).

Para respuestas en streaming (SSE):

::

    GET /api/v1/chat/stream?message=Cómo solicitar vacaciones pagadas

Para respuestas JSON sin streaming:

::

    POST /api/v1/chat
    Content-Type: application/x-www-form-urlencoded

    message=Cómo solicitar vacaciones pagadas

Con SSE, las respuestas se envían al cliente en tiempo real a medida que se generan.
Los usuarios pueden comenzar a leer la respuesta que se muestra progresivamente sin esperar a que se genere la respuesta completa.

Historial de conversación
--------------------------

La Chat API admite historial de conversación basado en sesiones.
Es posible realizar preguntas de seguimiento basadas en el contexto de preguntas anteriores.

Ejemplo:

- P1: "¿Cómo solicito vacaciones pagadas?"
- R1: (Respuesta como la anterior)
- P2: "¿Qué debo hacer si se me pasó el plazo de solicitud?"
- R2: (Respuesta basada en el contexto de P1)

Ajuste de RAG
==============

Mejora de la calidad de respuesta
----------------------------------

La calidad de respuesta de RAG se ve influenciada por los siguientes factores:

**Calidad de búsqueda**

Dado que RAG genera respuestas basadas en resultados de búsqueda, la calidad de búsqueda afecta directamente la calidad de respuesta.
Mejorar la calidad de búsqueda mediante el ciclo de ajuste descrito en la Parte 8 también conduce a una mejora en la calidad de RAG.

**Calidad de los documentos**

Si los documentos buscados están desactualizados, son inexactos o ambiguos, la calidad de respuesta de RAG también disminuirá.
Las actualizaciones periódicas y la gestión de calidad de los documentos son importantes.

**Configuración de prompts**

El ajuste de los prompts (texto de instrucciones) enviados al LLM le permite ajustar el estilo y la precisión de las respuestas.

Consideraciones de seguridad
==============================

Contramedidas contra inyección de prompts
------------------------------------------

La función RAG de Fess tiene defensas integradas contra la inyección de prompts.
Protege contra ataques que intentan manipular el comportamiento del LLM mediante entradas maliciosas.

Prevención de fugas de información
------------------------------------

Dado que RAG genera respuestas basadas en resultados de búsqueda, combinarlo con la búsqueda basada en roles (Parte 5) asegura que solo se generen respuestas apropiadas para los permisos del usuario.
El contenido de documentos a los que el usuario no tiene acceso autorizado no se incluye en las respuestas de RAG.

Resumen
=======

En este artículo, explicamos cómo construir un asistente de IA interno utilizando el modo de búsqueda con IA de Fess.

- Funcionamiento del pipeline de RAG (análisis de intención -> búsqueda -> evaluación -> generación de respuesta)
- Criterios de selección para tres proveedores de LLM (OpenAI, Gemini, Ollama)
- Configuración y experiencia del modo de búsqueda con IA
- Uso de la Chat API (SSE) desde programas
- Ajuste de la calidad de respuesta y consideraciones de seguridad

Con un asistente de IA basado en documentos internos, el uso del conocimiento pasa de "buscar" a "preguntar".

En el próximo artículo, cubriremos cómo integrar Fess como servidor MCP en agentes de IA.

Referencias
===========

- `Fess AI Search Mode Settings <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Fess Chat API <https://fess.codelibs.org/ja/15.5/api/api-chat.html>`__
