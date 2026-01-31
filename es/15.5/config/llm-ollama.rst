==========================
Configuracion de Ollama
==========================

Descripcion general
===================

Ollama es una plataforma de codigo abierto para ejecutar modelos de lenguaje grandes (LLM) en entorno local.
Esta configurado como el proveedor LLM predeterminado de |Fess| y es adecuado para uso en entornos privados.

Al usar Ollama, puede utilizar la funcionalidad de chat de IA sin enviar datos al exterior.

Caracteristicas principales
---------------------------

- **Ejecucion local**: Los datos no se envian externamente, asegurando privacidad
- **Modelos diversos**: Compatible con muchos modelos como Llama, Mistral, Gemma, CodeLlama
- **Eficiencia de costos**: Sin costos de API (solo costos de hardware)
- **Personalizacion**: Tambien puede usar modelos afinados personalizados

Modelos compatibles
-------------------

Principales modelos disponibles en Ollama:

- ``llama3.3:70b`` - Llama 3.3 de Meta (70B parametros)
- ``gemma3:4b`` - Gemma 3 de Google (4B parametros, predeterminado)
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

    # Descargar el modelo predeterminado (Gemma 3 4B)
    ollama pull gemma3:4b

    # Descargar Llama 3.3
    ollama pull llama3.3:70b

    # Verificar funcionamiento del modelo
    ollama run gemma3:4b "Hello, how are you?"

Configuracion basica
====================

Agregue la siguiente configuracion en ``app/WEB-INF/conf/system.properties``.

Configuracion minima
--------------------

::

    # Habilitar la funcionalidad de modo IA
    rag.chat.enabled=true

    # Configurar el proveedor LLM como Ollama
    rag.llm.type=ollama

    # URL de Ollama (para entorno local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modelo a usar
    rag.llm.ollama.model=gemma3:4b

Configuracion recomendada (entorno de produccion)
-------------------------------------------------

::

    # Habilitar la funcionalidad de modo IA
    rag.chat.enabled=true

    # Configuracion del proveedor LLM
    rag.llm.type=ollama

    # URL de Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuracion del modelo (usar modelo grande)
    rag.llm.ollama.model=llama3.3:70b

    # Configuracion de timeout (aumentar para modelos grandes)
    rag.llm.ollama.timeout=120000

Opciones de configuracion
=========================

Todas las opciones de configuracion disponibles para el cliente de Ollama.

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
     - ``gemma3:4b``
   * - ``rag.llm.ollama.timeout``
     - Timeout de solicitud (milisegundos)
     - ``60000``

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
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma3:4b
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
   * - ``gemma3:4b``
     - Pequeno-Medio
     - 6GB+
     - Uso general equilibrado (predeterminado)
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
    ollama run gemma3:4b --verbose

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

Modelo no encontrado
--------------------

**Sintoma**: Se muestra "Configured model not found in Ollama" en el log

**Solucion**:

1. Verificar que el nombre del modelo sea exacto (puede incluir tag ``:latest``)::

    # Verificar lista de modelos
    ollama list

2. Descargar el modelo necesario::

    ollama pull gemma3:4b

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
- :doc:`rag-chat` - Detalles de la funcionalidad de modo IA
