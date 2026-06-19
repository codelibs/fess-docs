==========================
Configuracion de Ollama
==========================

Descripcion general
===================

Ollama es una plataforma de codigo abierto para ejecutar modelos de lenguaje grandes (LLM) en entorno local.
La funcionalidad de integracion con Ollama de |Fess| se proporciona como plugin ``fess-llm-ollama`` y es adecuada para uso en entornos privados.

Al usar Ollama, puede utilizar la funcionalidad del modo de busqueda IA sin enviar datos al exterior.

Caracteristicas principales
----------------------------

- **Ejecucion local**: Los datos no se envian externamente, asegurando privacidad
- **Modelos diversos**: Compatible con muchos modelos como Llama, Mistral, Gemma, CodeLlama
- **Eficiencia de costos**: Sin costos de API (solo costos de hardware)
- **Personalizacion**: Tambien puede usar modelos con ajuste fino personalizado

Modelos compatibles
--------------------

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

La funcionalidad de integracion con Ollama se proporciona como plugin.
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

La configuracion relacionada con LLM se divide en multiples archivos de configuracion.

Configuracion minima
--------------------

``system.properties`` (tambien configurable en Administracion > Sistema > General):

::

    # Configurar el proveedor LLM como Ollama
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de busqueda IA
    rag.chat.enabled=true

    # URL de Ollama (para entorno local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modelo a usar
    rag.llm.ollama.model=gemma4:e4b

.. note::
   La configuracion del proveedor LLM tambien se puede configurar desde la pantalla de administracion (Administracion > Sistema > General) estableciendo ``rag.llm.name``.

Configuracion recomendada (entorno de produccion)
-------------------------------------------------

``system.properties`` (tambien configurable en Administracion > Sistema > General):

::

    # Configuracion del proveedor LLM
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar la funcionalidad de modo de busqueda IA
    rag.chat.enabled=true

    # URL de Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuracion del modelo (usar modelo grande)
    rag.llm.ollama.model=llama3.3:70b

    # Configuracion de timeout (aumentar para modelos grandes)
    rag.llm.ollama.timeout=120000

    # Control del numero de solicitudes simultaneas
    rag.llm.ollama.max.concurrent.requests=5

Elementos de configuracion
==========================

Todos los elementos de configuracion disponibles para el cliente de Ollama. Todos excepto ``rag.llm.name`` se configuran en ``fess_config.properties``.

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
     - Intervalo de verificacion de disponibilidad (segundos). Si se especifica ``0`` o un valor menor, se deshabilita la verificacion periodica de disponibilidad
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Numero maximo de solicitudes simultaneas
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Numero maximo de documentos relevantes en la evaluacion
     - ``3``
   * - ``rag.llm.ollama.concurrency.wait.timeout``
     - Timeout de espera para la obtencion del permiso de control de concurrencia (milisegundos)
     - ``30000``
   * - ``rag.llm.ollama.connect.timeout``
     - Timeout de conexion TCP (milisegundos). Se puede especificar de forma independiente a ``rag.llm.ollama.timeout``
     - ``5000``
   * - ``rag.llm.ollama.retry.max``
     - Numero maximo de reintentos HTTP (en errores ``429`` y de la familia ``5xx``)
     - ``3``
   * - ``rag.llm.ollama.retry.base.delay.ms``
     - Retardo base del backoff exponencial (milisegundos)
     - ``2000``

Configuracion detallada
-----------------------

Elementos de configuracion detallados relacionados con el historial y el tamano del contexto.

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.ollama.chat.evaluation.description.max.chars``
     - Numero maximo de caracteres de la descripcion en la evaluacion
     - ``500``
   * - ``rag.llm.ollama.history.max.chars``
     - Numero maximo de caracteres del historial de conversacion
     - ``4000``
   * - ``rag.llm.ollama.intent.history.max.messages``
     - Numero maximo de mensajes del historial en la determinacion de intencion
     - ``6``
   * - ``rag.llm.ollama.intent.history.max.chars``
     - Numero maximo de caracteres del historial en la determinacion de intencion
     - ``3000``
   * - ``rag.llm.ollama.history.assistant.max.chars``
     - Numero maximo de caracteres del historial de respuestas del asistente
     - ``500``
   * - ``rag.llm.ollama.history.assistant.summary.max.chars``
     - Numero maximo de caracteres del historial de resumenes del asistente
     - ``500``

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
- ``rag.llm.ollama.{promptType}.max.tokens`` - Numero maximo de tokens (mapeado a ``num_predict`` en la API de Ollama)
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Numero maximo de caracteres del contexto
- ``rag.llm.ollama.{promptType}.thinking.budget`` - Presupuesto de pensamiento (control de pensamiento en formato booleano; consulte "Soporte de modelo de pensamiento" para mas detalles)
- ``rag.llm.ollama.{promptType}.thinking.level`` - Nivel de pensamiento (formato de cadena ``high`` / ``medium`` / ``low``; consulte "Soporte de modelo de pensamiento" para mas detalles)
- ``rag.llm.ollama.{promptType}.top.p`` - Valor de muestreo Top-P
- ``rag.llm.ollama.{promptType}.top.k`` - Valor de muestreo Top-K
- ``rag.llm.ollama.{promptType}.num.ctx`` - Tamano de la ventana de contexto

Cada parametro se resuelve en el siguiente orden: ``rag.llm.ollama.{promptType}.<param>`` (configuracion especifica por tipo de prompt) → ``rag.llm.ollama.default.<param>`` (valor de reserva comun para todos los tipos de prompt) → valor predeterminado codificado por tipo de prompt. Los valores especificados explicitamente en la solicitud siempre tienen prioridad.

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
   * - ``queryregeneration``
     - Prompt de regeneracion de consulta

Cada tipo de prompt tiene valores predeterminados codificados que se aplican cuando se omite la configuracion.

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
Al especificarlos con el formato ``rag.llm.ollama.default.<param>``, se usan como valor de reserva comun para todos los tipos de prompt.
El mecanismo de reserva mediante ``default`` se aplica no solo a ``top.p`` / ``top.k`` / ``num.ctx``, sino tambien a ``temperature`` / ``max.tokens`` / ``thinking.budget`` / ``thinking.level``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.llm.ollama.default.top.p``
     - Valor de muestreo Top-P (0.0 a 1.0). Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.top.p``
     - (sin definir)
   * - ``rag.llm.ollama.default.top.k``
     - Valor de muestreo Top-K. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.top.k``
     - (sin definir)
   * - ``rag.llm.ollama.default.num.ctx``
     - Tamano de la ventana de contexto. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.num.ctx``
     - (sin definir)
   * - ``rag.llm.ollama.default.temperature``
     - Valor de reserva de temperature en la generacion. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.temperature``
     - (sin definir)
   * - ``rag.llm.ollama.default.max.tokens``
     - Valor de reserva del numero maximo de tokens. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.max.tokens``
     - (sin definir)
   * - ``rag.llm.ollama.default.thinking.budget``
     - Valor de reserva del presupuesto de pensamiento. Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.thinking.budget``
     - (sin definir)
   * - ``rag.llm.ollama.default.thinking.level``
     - Valor de reserva del nivel de pensamiento (``high`` / ``medium`` / ``low``). Se puede sobrescribir por tipo de prompt con ``rag.llm.ollama.{promptType}.thinking.level``
     - (sin definir)
   * - ``rag.llm.ollama.options.*``
     - Opciones globales pasadas directamente a la API de Ollama. El sufijo se usa como nombre de opcion (ejemplo: ``rag.llm.ollama.options.repeat_penalty=1.1``). Los valores se convierten automaticamente a Integer, Double, Boolean o String
     - (sin definir)

Ejemplo de configuracion::

    # Muestreo Top-P predeterminado (comun para todos los tipos de prompt)
    rag.llm.ollama.default.top.p=0.9

    # Muestreo Top-K predeterminado
    rag.llm.ollama.default.top.k=40

    # Tamano de ventana de contexto predeterminado
    rag.llm.ollama.default.num.ctx=4096

    # Cambiar Top-P solo en la generacion de respuestas
    rag.llm.ollama.answer.top.p=0.95

    # Opciones globales (pasadas directamente a la API de Ollama)
    rag.llm.ollama.options.repeat_penalty=1.1

Soporte de modelo de pensamiento
==================================

Cuando se usa un modelo de pensamiento (thinking model) como gemma4 o qwen3, |Fess| soporta la configuracion del presupuesto de pensamiento (thinking budget).

El presupuesto de pensamiento se configura por tipo de prompt en ``fess_config.properties``:

::

    # Configuracion del presupuesto de pensamiento en la generacion de respuestas
    rag.llm.ollama.answer.thinking.budget=1024

    # Configuracion del presupuesto de pensamiento en la generacion de resumenes
    rag.llm.ollama.summary.thinking.budget=1024

Al configurar el presupuesto de pensamiento, puede controlar el numero de tokens asignados al paso de "pensar" antes de que el modelo genere una respuesta.

.. note::
   En Ollama, el presupuesto de pensamiento se convierte a un flag booleano (si el valor es mayor que 0, se usa ``think: true``; si es 0, se usa ``think: false``). El control detallado por numero de tokens no esta disponible debido a las restricciones de la API de Ollama.

Nivel de pensamiento (thinking level)
--------------------------------------

Algunos modelos como gpt-oss ignoran el flag ``think`` en formato booleano y requieren la especificacion del nivel de pensamiento mediante el formato de cadena ``high`` / ``medium`` / ``low``.
Para este tipo de modelos, use ``rag.llm.ollama.{promptType}.thinking.level``.

::

    # Configuracion del nivel de pensamiento en la generacion de respuestas
    rag.llm.ollama.answer.thinking.level=high

    # Configuracion del nivel de pensamiento en la generacion de resumenes
    rag.llm.ollama.summary.thinking.level=medium

Los valores que se pueden establecer en ``thinking.level`` son ``high`` / ``medium`` / ``low`` (sin distincion de mayusculas y minusculas). Si se especifica un valor no valido, se ignora y se emite un log de advertencia.

.. note::
   Si tanto ``thinking.level`` (formato de cadena) como ``thinking.budget`` (formato booleano) estan configurados, ``thinking.level`` tiene prioridad. Use ``thinking.level`` para modelos de la familia GPT-OSS y ``thinking.budget`` para otros modelos de pensamiento.

Configuracion de red
====================

Configuracion con Docker
------------------------

El repositorio oficial `docker-fess <https://github.com/codelibs/docker-fess>`__ de |Fess| incluye un overlay para Ollama ``compose-ollama.yaml``. Los pasos minimos son los siguientes.

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

``compose-ollama.yaml`` esta configurado para usar GPU NVIDIA (se requiere NVIDIA Container Toolkit). Su contenido es el siguiente.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.7.0"
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

- ``FESS_PLUGINS=fess-llm-ollama:15.7.0`` hace que el script de inicio obtenga automaticamente el JAR del plugin y lo coloque en ``app/WEB-INF/plugin/`` (ajuste la version a la de su |Fess|)
- ``-Dfess.config.rag.chat.enabled=true`` habilita el modo de busqueda IA
- ``-Dfess.config.rag.llm.ollama.api.url=...`` especifica la URL del servidor Ollama (dentro de la red de Docker Compose se resuelve por el nombre del servicio, como ``ollama01``)
- El valor predeterminado del proveedor LLM (``rag.llm.name``) es ``ollama``, por lo que si solo se usa Ollama no es necesaria una especificacion explicita. Si se cambia desde otro proveedor, agregue ``-Dfess.system.rag.llm.name=ollama`` a ``FESS_JAVA_OPTS`` o configurelo despues del inicio en la pantalla de administracion "Sistema > General", seccion RAG
- El bloque ``deploy.resources.reservations.devices`` es la configuracion para usar GPU. Si no se usa GPU (ejecutando solo con CPU), elimine este bloque

.. note::
   Las variables de entorno en formato snake_case en mayusculas como ``RAG_CHAT_ENABLED`` o ``RAG_LLM_NAME`` no son reconocidas directamente por |Fess|. Los valores de configuracion deben pasarse siempre dentro de ``FESS_JAVA_OPTS`` como ``-Dfess.config.<key>`` (familia ``fess_config.properties``) o ``-Dfess.system.<key>`` (familia ``system.properties``).

Servidor Ollama remoto
----------------------

Cuando se ejecuta Ollama en un servidor diferente a Fess:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama no tiene funcionalidad de autenticacion por defecto, por lo que si lo hace accesible externamente,
   considere medidas de seguridad a nivel de red (firewall, VPN, etc.).

Uso a traves de proxy HTTP
==========================

El cliente de Ollama comparte la configuracion de proxy HTTP comun de |Fess|. Si necesita pasar por un proxy para conectarse al servidor Ollama (por ejemplo al usar un servidor Ollama remoto), especifique las siguientes propiedades en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``http.proxy.host``
     - Nombre del host del proxy (si la cadena esta vacia, no se usa proxy)
     - ``""``
   * - ``http.proxy.port``
     - Numero de puerto del proxy
     - ``8080``
   * - ``http.proxy.username``
     - Nombre de usuario para autenticacion del proxy (opcional; al especificarlo se habilita la autenticacion Basic)
     - ``""``
   * - ``http.proxy.password``
     - Contrasena para autenticacion del proxy
     - ``""``

.. note::
   Como Ollama normalmente se ejecuta en local o dentro de la red interna, la configuracion de proxy solo es necesaria en casos limitados (por ejemplo, cuando se usa un servidor Ollama remoto al que solo se puede llegar a traves del proxy corporativo).
   Esta configuracion tambien afecta el acceso HTTP de todo |Fess|, incluido el crawler.

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

**Sintoma**: Se muestra en el log "Configured model not found"

**Solucion**:

1. Verificar que el nombre del modelo sea exacto (puede incluir el tag ``:latest``)::

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
- :doc:`rag-chat` - Detalles de la funcionalidad de modo de busqueda IA
