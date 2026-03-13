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
     - (requerido)
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

- ``rag.llm.openai.{promptType}.temperature`` - Aleatoriedad de generacion (0.0 a 2.0)
- ``rag.llm.openai.{promptType}.max.tokens`` - Numero maximo de tokens
- ``rag.llm.openai.{promptType}.context.max.chars`` - Numero maximo de caracteres del contexto

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

Soporte de modelos de inferencia
=================================

Cuando se usan modelos de inferencia de las series o1/o3/o4 o de la serie gpt-5, |Fess| utiliza automaticamente el parametro ``max_completion_tokens`` de la API de OpenAI en lugar de ``max_tokens``. No se requieren cambios adicionales de configuracion.

Parametros adicionales para modelos de inferencia
--------------------------------------------------

Al usar modelos de inferencia, se pueden configurar los siguientes parametros adicionales en ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.openai.reasoning.effort``
     - Configuracion de reasoning effort para modelos serie o (``low``, ``medium``, ``high``)
     - (no configurado)
   * - ``rag.llm.openai.top.p``
     - Umbral de probabilidad para la seleccion de tokens (0.0 a 1.0)
     - (no configurado)
   * - ``rag.llm.openai.frequency.penalty``
     - Penalizacion de frecuencia (-2.0 a 2.0)
     - (no configurado)
   * - ``rag.llm.openai.presence.penalty``
     - Penalizacion de presencia (-2.0 a 2.0)
     - (no configurado)

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

Configuracion con variables de entorno
======================================

Por razones de seguridad, se recomienda configurar la clave API con variables de entorno.

Entorno Docker
--------------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.6.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-5-mini

Entorno systemd
---------------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_OPENAI_API_KEY=sk-xxx..."

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
