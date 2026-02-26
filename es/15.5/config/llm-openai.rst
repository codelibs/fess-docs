==========================
Configuracion de OpenAI
==========================

Descripcion general
===================

OpenAI es un servicio en la nube que proporciona modelos de lenguaje grandes (LLM) de alto rendimiento, comenzando con GPT-4.
|Fess| puede utilizar la API de OpenAI para implementar la funcionalidad de modo IA.

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

- ``gpt-4o`` - Modelo multimodal de alto rendimiento
- ``gpt-4o-mini`` - Version ligera de GPT-4o (buena relacion costo-rendimiento)
- ``o3-mini`` - Modelo ligero especializado en razonamiento
- ``o4-mini`` - Modelo ligero de proxima generacion especializado en razonamiento
- ``gpt-4-turbo`` - Version de alta velocidad de GPT-4
- ``gpt-3.5-turbo`` - Modelo con buen equilibrio costo-rendimiento

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

Configuracion basica
====================

Agregue la siguiente configuracion en ``app/WEB-INF/conf/fess_config.properties``.

Configuracion minima
--------------------

::

    # Habilitar la funcionalidad de modo IA
    rag.chat.enabled=true

    # Configurar el proveedor LLM como OpenAI
    rag.llm.type=openai

    # Clave API de OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelo a usar
    rag.llm.openai.model=gpt-4o-mini

Configuracion recomendada (entorno de produccion)
-------------------------------------------------

::

    # Habilitar la funcionalidad de modo IA
    rag.chat.enabled=true

    # Configuracion del proveedor LLM
    rag.llm.type=openai

    # Clave API de OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuracion del modelo (usar modelo de alto rendimiento)
    rag.llm.openai.model=gpt-4o

    # Endpoint de API (normalmente no necesita cambios)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Configuracion de timeout
    rag.llm.openai.timeout=60000

Opciones de configuracion
=========================

Todas las opciones de configuracion disponibles para el cliente de OpenAI.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.openai.api.key``
     - Clave API de OpenAI
     - (requerido)
   * - ``rag.llm.openai.model``
     - Nombre del modelo a usar
     - ``gpt-5-mini``
   * - ``rag.llm.openai.api.url``
     - URL base de la API
     - ``https://api.openai.com/v1``
   * - ``rag.llm.openai.timeout``
     - Timeout de solicitud (milisegundos)
     - ``60000``

Configuracion con variables de entorno
======================================

Por razones de seguridad, se recomienda configurar la clave API con variables de entorno.

Entorno Docker
--------------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-4o-mini

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
   * - ``gpt-3.5-turbo``
     - Bajo
     - Buena
     - Preguntas y respuestas generales, prioridad en costos
   * - ``gpt-4o-mini``
     - Medio
     - Alta
     - Uso equilibrado (recomendado)
   * - ``gpt-4o``
     - Alto
     - Maxima
     - Razonamiento complejo, cuando se requiere alta calidad
   * - ``o3-mini`` / ``o4-mini``
     - Medio
     - Maxima
     - Tareas de razonamiento como matematicas y programacion
   * - ``gpt-4-turbo``
     - Alto
     - Maxima
     - Cuando se requiere respuesta rapida

Estimacion de costos
--------------------

La API de OpenAI cobra segun el uso. Los siguientes son precios de referencia a partir de 2024.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modelo
     - Entrada (1K tokens)
     - Salida (1K tokens)
   * - gpt-3.5-turbo
     - $0.0005
     - $0.0015
   * - gpt-4o-mini
     - $0.00015
     - $0.0006
   * - gpt-4o
     - $0.005
     - $0.015

.. note::
   Para los precios mas recientes, consulte `OpenAI Pricing <https://openai.com/pricing>`__.

Limite de tasa
==============

La API de OpenAI tiene limites de tasa. Configure apropiadamente junto con la funcionalidad de limite de tasa de |Fess|.

::

    # Configuracion de limite de tasa de Fess
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

Limites por nivel de OpenAI
---------------------------

Los limites varian segun el nivel de la cuenta de OpenAI:

- **Free**: 3 RPM (solicitudes/minuto)
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: Limites aun mayores

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

1. Configurar limites de tasa mas estrictos en |Fess|::

    rag.chat.rate.limit.requests.per.minute=5

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

    rag.llm.openai.timeout=120000

2. Considerar usar un modelo mas rapido (como gpt-3.5-turbo)

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
- :doc:`rag-chat` - Detalles de la funcionalidad de modo IA
