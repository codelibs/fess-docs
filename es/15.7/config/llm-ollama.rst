==========================
Configuracion de Ollama
==========================

Descripcion general
===================

Ollama es una plataforma de codigo abierto para ejecutar modelos de lenguaje grandes (LLM) en entorno local.
En |Fess| 15.7, la funcionalidad de integracion con Ollama se proporciona como plugin ``fess-llm-ollama`` y es adecuada para uso en entornos privados.

Al usar Ollama, puede utilizar la funcionalidad del modo de busqueda IA sin enviar datos al exterior.

Caracteristicas principales
---------------------------

- **Ejecucion local**: Los datos no se envian externamente, asegurando privacidad
- **Modelos diversos**: Compatible con muchos modelos como Llama, Mistral, Gemma, CodeLlama
- **Eficiencia de costos**: Sin costos de API (solo costos de hardware)
- **Personalizacion**: Tambien puede usar modelos con ajuste fino personalizado

Modelos compatibles
-------------------

Principales modelos disponibles en Ollama:

- ``llama3.3:70b`` - Llama 3.3 de Meta (70B parametros)
- ``gemma4:e4b`` - Gemma 4 de Google (E4B parametros, predeterminado)
- ``mistral:7b`` - Mistral de Mistral AI (7B parametros)
- ``codellama:13b`` - Code Llama de Meta (13B parametros)
- ``phi3:3.8b`` - Phi-3 de Microsoft (3.8B parametros)

.. note::
   Para la lista mas reciente de modelos disponibles, consulte `Ollama Library <https://ollama.com/library>`__.

Requisitos previos
==================

Antes de usar Ollama, verifique lo siguiente.

1. **Instalacion de Ollama**: Descargue e instale desde `https://ollama.com/ <https://ollama.com/>`__
2. **Descarga de modelo**: Descargue el modelo a usar en Ollama
3. **Inicio del servidor Ollama**: Confirme que Ollama este ejecutandose

Instalacion de Ollama
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

Instalacion del plugin
======================

En |Fess| 15.7, la funcionalidad de integracion con Ollama ha sido separada como plugin.
Para usar Ollama es necesario instalar el plugin ``fess-llm-ollama``.

1. Descargue `fess-llm-ollama-15.7.0.jar`.
2. Coloquelo en el directorio ``app/WEB-INF/plugin/`` del directorio de instalacion de |Fess|.

::

    cp fess-llm-ollama-15.7.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Reinicie |Fess|.

.. note::
   La version del plugin debe coincidir con la version de |Fess|.

Configuracion basica
====================

En |Fess| 15.7, la configuracion relacionada con LLM se divide en multiples archivos de configuracion.

Configuracion minima
--------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # URL de Ollama (para entorno local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modelo a usar
    rag.llm.ollama.model=gemma4:e4b

``system.properties`` (tambien configurable en Administracion > Sistema > General):

::

    # Configurar el proveedor LLM como Ollama
    rag.llm.name=ollama

.. note::
   La configuracion del proveedor LLM tambien se puede configurar desde la pantalla de administracion (Administracion > Sistema > General) estableciendo ``rag.llm.name``.

Configuracion recomendada (entorno de produccion)
-------------------------------------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

    # URL de Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuracion del modelo (usar modelo grande)
    rag.llm.ollama.model=llama3.3:70b

    # Configuracion de timeout (aumentar para modelos grandes)
    rag.llm.ollama.timeout=120000

    # Control del numero de solicitudes simultaneas
    rag.llm.ollama.max.concurrent.requests=5

``system.properties`` (tambien configurable en Administracion > Sistema > General):

::

    # Configuracion del proveedor LLM
    rag.llm.name=ollama

Elementos de configuracion
==========================

Todos los elementos de configuracion disponibles para el cliente de Ollama. Todos se configuran en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
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
     - Intervalo de verificacion de disponibilidad (segundos)
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Numero maximo de solicitudes simultaneas
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Numero maximo de documentos relevantes en la evaluacion
     - ``3``

Control de concurrencia
-----------------------

Usando ``rag.llm.ollama.max.concurrent.requests``, puede controlar el numero de solicitudes simultaneas a Ollama.
El valor predeterminado es 5. Ajustelo segun los recursos del servidor Ollama.
Si el numero de solicitudes simultaneas es demasiado alto, puede sobrecargar el servidor Ollama y reducir la velocidad de respuesta.

Configuracion por tipo de prompt
=================================

En |Fess|, se pueden personalizar los parametros del LLM por tipo de prompt.
La configuracion se escribe en ``fess_config.properties``.

Se pueden configurar los siguientes parametros por tipo de prompt:

- ``rag.llm.ollama.{promptType}.temperature`` - Temperature en la generacion
- ``rag.llm.ollama.{promptType}.max.tokens`` - Numero maximo de tokens
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Numero maximo de caracteres del contexto

Tipos de prompt disponibles:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tipo de prompt
     - Descripcion
   * - ``intent``
     - Prompt para determinar la intencion del usuario
   * - ``evaluation``
     - Prompt de evaluacion de resultados de busqueda
   * - ``unclear``
     - Prompt de respuesta para consultas no claras
   * - ``noresults``
     - Prompt para cuando no hay resultados de busqueda
   * - ``docnotfound``
     - Prompt para cuando no se encuentra el documento
   * - ``answer``
     - Prompt de generacion de respuesta
   * - ``summary``
     - Prompt de generacion de resumen
   * - ``faq``
     - Prompt de generacion de FAQ
   * - ``direct``
     - Prompt de respuesta directa

Ejemplo de configuracion::

    # Configurar la temperature en la generacion de respuestas
    rag.llm.ollama.answer.temperature=0.7

    # Configurar el numero maximo de tokens en la generacion de resumenes
    rag.llm.ollama.summary.max.tokens=2048

    # Configurar el numero maximo de caracteres de contexto en la determinacion de intencion
    rag.llm.ollama.intent.context.max.chars=4000

Opciones de modelo Ollama
==========================

Los parametros del modelo Ollama se pueden configurar en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.ollama.top.p``
     - Valor de muestreo Top-P (0.0 a 1.0)
     - (no configurado)
   * - ``rag.llm.ollama.top.k``
     - Valor de muestreo Top-K
     - (no configurado)
   * - ``rag.llm.ollama.num.ctx``
     - Tamano de la ventana de contexto
     - (no configurado)
   * - ``rag.llm.ollama.default.*``
     - Configuracion de reserva predeterminada
     - (no configurado)
   * - ``rag.llm.ollama.options.*``
     - Opciones globales
     - (no configurado)

Ejemplo de configuracion::

    # Muestreo Top-P
    rag.llm.ollama.top.p=0.9

    # Muestreo Top-K
    rag.llm.ollama.top.k=40

    # Tamano de la ventana de contexto
    rag.llm.ollama.num.ctx=4096

Soporte de modelo de pensamiento
==================================

Cuando se usa un modelo de pensamiento (thinking model) como gemma4 o qwen3.5, |Fess| soporta la configuracion del presupuesto de pensamiento (thinking budget).

Configure lo siguiente en ``fess_config.properties``:

::

    # Configuracion del presupuesto de pensamiento
    rag.llm.ollama.thinking.budget=1024

Al configurar el presupuesto de pensamiento, puede controlar el numero de tokens asignados al paso de "pensar" antes de que el modelo genere una respuesta.

Configuracion de red
====================

Configuracion con Docker
------------------------

Ejemplo de configuracion cuando tanto |Fess| como Ollama se ejecutan en Docker.

``docker-compose.yml``:

::

    version: '3'
    services:
      fess:
        image: codelibs/fess:15.7.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma4:e4b
        depends_on:
          - ollama
        # ... otras configuraciones

      ollama:
        image: ollama/ollama
        volumes:
          - ollama_data:/root/.ollama
        ports:
          - "11434:11434"

    volumes:
      ollama_data:

.. note::
   En entornos Docker Compose, use ``ollama`` como nombre de host (no ``localhost``).

Servidor Ollama remoto
----------------------

Cuando se ejecuta Ollama en un servidor diferente a Fess:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama no tiene funcionalidad de autenticacion por defecto, por lo que si lo hace accesible externamente,
   considere medidas de seguridad a nivel de red (firewall, VPN, etc.).

Guia de seleccion de modelos
============================

Guia para la seleccion de modelos segun el proposito de uso.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modelo
     - Tamano
     - VRAM requerida
     - Uso
   * - ``phi3:3.8b``
     - Pequeno
     - 4GB+
     - Entornos ligeros, respuestas simples
   * - ``gemma4:e4b``
     - Pequeno-Medio
     - 8GB+
     - Uso general equilibrado, soporte de thinking (predeterminado)
   * - ``mistral:7b``
     - Medio
     - 8GB+
     - Cuando se requieren respuestas de alta calidad
   * - ``llama3.3:70b``
     - Grande
     - 48GB+
     - Respuestas de maxima calidad, razonamiento complejo

Soporte de GPU
--------------

Ollama soporta aceleracion por GPU. El uso de GPUs NVIDIA mejora significativamente
la velocidad de inferencia.

::

    # Verificar soporte de GPU
    ollama run gemma4:e4b --verbose

Solucion de problemas
=====================

Error de conexion
-----------------

**Sintoma**: Errores en la funcionalidad de chat, LLM mostrado como no disponible

**Verificaciones**:

1. Verificar que Ollama este ejecutandose::

    curl http://localhost:11434/api/tags

2. Verificar que el modelo este descargado::

    ollama list

3. Verificar la configuracion del firewall

4. Verificar que el plugin ``fess-llm-ollama`` este colocado en ``app/WEB-INF/plugin/``

Modelo no encontrado
--------------------

**Sintoma**: Se muestra "Configured model not found in Ollama" en el log

**Solucion**:

1. Verificar que el nombre del modelo sea exacto (puede incluir tag ``:latest``)::

    # Verificar lista de modelos
    ollama list

2. Descargar el modelo necesario::

    ollama pull gemma4:e4b

Timeout
-------

**Sintoma**: Las solicitudes tienen timeout

**Solucion**:

1. Extender el tiempo de timeout::

    rag.llm.ollama.timeout=120000

2. Usar un modelo mas pequeno o considerar un entorno con GPU

Configuracion de depuracion
---------------------------

Para investigar problemas, puede ajustar el nivel de log de |Fess| para obtener logs detallados relacionados con Ollama.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

Informacion de referencia
=========================

- `Sitio oficial de Ollama <https://ollama.com/>`__
- `Biblioteca de modelos Ollama <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - Descripcion general de integracion LLM
- :doc:`rag-chat` - Detalles de la funcionalidad de modo de búsqueda IA
