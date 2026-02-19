==========================
Configuracion de Google Gemini
==========================

Descripcion general
===================

Google Gemini es un modelo de lenguaje grande (LLM) de ultima generacion proporcionado por Google.
|Fess| puede implementar la funcionalidad de modo IA con el modelo Gemini utilizando Google AI API (Generative Language API).

Al usar Gemini, es posible generar respuestas de alta calidad aprovechando la ultima tecnologia de IA de Google.

Caracteristicas principales
---------------------------

- **Soporte multimodal**: Capaz de procesar no solo texto sino tambien imagenes
- **Contexto largo**: Ventana de contexto larga que puede procesar grandes cantidades de documentos a la vez
- **Eficiencia de costos**: El modelo Flash es rapido y de bajo costo
- **Integracion con Google**: Facil integracion con servicios de Google Cloud

Modelos compatibles
-------------------

Principales modelos disponibles en Gemini:

- ``gemini-2.5-flash`` - Modelo rapido y eficiente (recomendado)
- ``gemini-2.5-pro`` - Modelo con mayor capacidad de razonamiento
- ``gemini-1.5-flash`` - Modelo Flash version estable
- ``gemini-1.5-pro`` - Modelo Pro version estable

.. note::
   Para la informacion mas reciente sobre modelos disponibles, consulte `Google AI for Developers <https://ai.google.dev/models/gemini>`__.

Requisitos previos
==================

Antes de usar Gemini, prepare lo siguiente.

1. **Cuenta de Google**: Se requiere una cuenta de Google
2. **Acceso a Google AI Studio**: Acceda a `https://aistudio.google.com/ <https://aistudio.google.com/>`__
3. **Clave API**: Genere una clave API en Google AI Studio

Obtencion de clave API
----------------------

1. Acceda a `Google AI Studio <https://aistudio.google.com/>`__
2. Haga clic en "Get API key"
3. Seleccione "Create API key"
4. Seleccione o cree un nuevo proyecto
5. Guarde la clave API generada de forma segura

.. warning::
   La clave API es informacion confidencial. Tenga en cuenta lo siguiente:

   - No la commita en sistemas de control de versiones
   - No la imprima en logs
   - Administrela con variables de entorno o archivos de configuracion seguros

Configuracion basica
====================

Agregue la siguiente configuracion en ``app/WEB-INF/conf/fess_config.properties``.

Configuracion minima
--------------------

::

    # Habilitar la funcionalidad de modo IA
    rag.chat.enabled=true

    # Configurar el proveedor LLM como Gemini
    rag.llm.type=gemini

    # Clave API de Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelo a usar
    rag.llm.gemini.model=gemini-2.5-flash

Configuracion recomendada (entorno de produccion)
-------------------------------------------------

::

    # Habilitar la funcionalidad de modo IA
    rag.chat.enabled=true

    # Configuracion del proveedor LLM
    rag.llm.type=gemini

    # Clave API de Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuracion del modelo (usar modelo rapido)
    rag.llm.gemini.model=gemini-2.5-flash

    # Endpoint de API (normalmente no necesita cambios)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Configuracion de timeout
    rag.llm.gemini.timeout=60000

Opciones de configuracion
=========================

Todas las opciones de configuracion disponibles para el cliente de Gemini.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.gemini.api.key``
     - Clave API de Google AI
     - (requerido)
   * - ``rag.llm.gemini.model``
     - Nombre del modelo a usar
     - ``gemini-2.5-flash``
   * - ``rag.llm.gemini.api.url``
     - URL base de la API
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Timeout de solicitud (milisegundos)
     - ``60000``

Configuracion con variables de entorno
======================================

Por razones de seguridad, se recomienda configurar la clave API con variables de entorno.

Entorno Docker
--------------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=gemini
          - RAG_LLM_GEMINI_API_KEY=${GEMINI_API_KEY}
          - RAG_LLM_GEMINI_MODEL=gemini-2.5-flash

Entorno systemd
---------------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_GEMINI_API_KEY=AIzaSy..."

Uso a traves de Vertex AI
=========================

Si esta usando Google Cloud Platform, tambien puede usar Gemini a traves de Vertex AI.
Al usar Vertex AI, el endpoint de la API y el metodo de autenticacion son diferentes.

.. note::
   El |Fess| actual utiliza Google AI API (generativelanguage.googleapis.com).
   Si se requiere el uso a traves de Vertex AI, puede ser necesaria una implementacion personalizada.

Guia de seleccion de modelos
============================

Guia para la seleccion de modelos segun el proposito de uso.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modelo
     - Velocidad
     - Calidad
     - Uso
   * - ``gemini-2.5-flash``
     - Rapido
     - Alta
     - Uso general, enfasis en equilibrio (recomendado)
   * - ``gemini-2.5-pro``
     - Medio
     - Maxima
     - Razonamiento complejo, cuando se requiere alta calidad
   * - ``gemini-1.5-flash``
     - Rapido
     - Buena
     - Enfasis en costos, enfasis en estabilidad
   * - ``gemini-1.5-pro``
     - Medio
     - Alta
     - Cuando se requiere contexto largo

Ventana de contexto
-------------------

Los modelos Gemini soportan ventanas de contexto muy largas:

- **Gemini 1.5/2.5 Flash**: Hasta 1 millon de tokens
- **Gemini 1.5/2.5 Pro**: Hasta 2 millones de tokens

Aprovechando esta caracteristica, puede incluir mas resultados de busqueda en el contexto.

::

    # Incluir mas documentos en el contexto
    rag.chat.context.max.documents=10
    rag.chat.context.max.chars=20000

Estimacion de costos
--------------------

La API de Google AI cobra segun el uso (con cuota gratuita disponible).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modelo
     - Entrada (1M caracteres)
     - Salida (1M caracteres)
   * - Gemini 1.5 Flash
     - $0.075
     - $0.30
   * - Gemini 1.5 Pro
     - $1.25
     - $5.00
   * - Gemini 2.5 Flash
     - Los precios pueden variar
     - Los precios pueden variar

.. note::
   Para los precios mas recientes e informacion sobre la cuota gratuita, consulte `Google AI Pricing <https://ai.google.dev/pricing>`__.

Limite de tasa
==============

La API de Google AI tiene limites de tasa. Configure apropiadamente junto con la funcionalidad de limite de tasa de |Fess|.

::

    # Configuracion de limite de tasa de Fess
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

Limites de la cuota gratuita
----------------------------

La API de Google AI tiene una cuota gratuita, pero con las siguientes limitaciones:

- Solicitudes/minuto: 15 RPM
- Tokens/minuto: 1 millon TPM
- Solicitudes/dia: 1,500 RPD

Solucion de problemas
=====================

Error de autenticacion
----------------------

**Sintoma**: Errores relacionados con la clave API

**Verificaciones**:

1. Verificar que la clave API este configurada correctamente
2. Confirmar que la clave API sea valida en Google AI Studio
3. Confirmar que la clave API tenga los permisos necesarios
4. Verificar que la API este habilitada en el proyecto

Error de limite de tasa
-----------------------

**Sintoma**: Error "429 Resource has been exhausted"

**Solucion**:

1. Configurar limites de tasa mas estrictos en |Fess|::

    rag.chat.rate.limit.requests.per.minute=5

2. Esperar unos minutos y reintentar
3. Solicitar aumento de cuota si es necesario

Restriccion de region
---------------------

**Sintoma**: Error de que el servicio no esta disponible

**Verificaciones**:

La API de Google AI solo esta disponible en ciertas regiones.
Consulte la documentacion de Google para las regiones soportadas.

Timeout
-------

**Sintoma**: Las solicitudes tienen timeout

**Solucion**:

1. Extender el tiempo de timeout::

    rag.llm.gemini.timeout=120000

2. Considerar usar el modelo Flash (mas rapido)

Configuracion de depuracion
---------------------------

Para investigar problemas, puede ajustar el nivel de log de |Fess| para obtener logs detallados relacionados con Gemini.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

Notas de seguridad
==================

Al usar la API de Google AI, tenga en cuenta los siguientes aspectos de seguridad.

1. **Privacidad de datos**: El contenido de los resultados de busqueda se envia a los servidores de Google
2. **Gestion de claves API**: La filtracion de claves puede llevar a uso no autorizado
3. **Cumplimiento**: Si incluye datos confidenciales, verifique las politicas de su organizacion
4. **Terminos de uso**: Cumpla con los terminos de uso y la Politica de Uso Aceptable de Google

Informacion de referencia
=========================

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - Descripcion general de integracion LLM
- :doc:`rag-chat` - Detalles de la funcionalidad de modo IA
