===================================================
Configuración de Amazon Bedrock (Búsqueda IA / RAG)
===================================================

Descripción general
===================

Esta página explica cómo configurar el plugin ``fess-llm-bedrock`` para que |Fess| pueda usar Amazon Bedrock en su **modo de búsqueda IA (RAG: Retrieval-Augmented Generation)** y como proveedor de embeddings para los chunks de contenido.

Amazon Bedrock es el servicio de AWS que ofrece, mediante una única API, modelos fundacionales de Amazon y de otros proveedores de modelos.
El plugin llama a la API Bedrock Runtime en la región de AWS que usted elija:

- **Modo de búsqueda IA**: la API Converse (``ConverseStream`` para respuestas en streaming)
- **Embedding de chunks de contenido**: la API InvokeModel con Amazon Titan Text Embeddings V2 o Cohere Embed

Modelos compatibles
-------------------

El modo de búsqueda IA funciona con cualquier modelo que admita la API Converse en su región.
El modelo predeterminado es Amazon Nova 2 Lite a través del perfil de inferencia entre regiones de EE. UU., ``us.amazon.nova-2-lite-v1:0``.
``rag.llm.bedrock.model`` acepta un ID de modelo, un ID de perfil de inferencia (por ejemplo, con el prefijo ``us.``, ``eu.`` o ``global.``) o un ARN.

El embedding de chunks de contenido admite los siguientes modelos.

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - Modelo
     - ``content_chunker.embedding.dimension``
     - Textos por solicitud
   * - ``amazon.titan-embed-text-v2:0``
     - ``256``, ``512`` o ``1024``
     - 1
   * - ``cohere.embed-english-v3`` / ``cohere.embed-multilingual-v3``
     - ``1024``
     - hasta 96, cada uno de como máximo 2048 caracteres
   * - ``cohere.embed-v4:0`` (también a través de un perfil de inferencia)
     - ``256``, ``512``, ``1024`` o ``1536``
     - hasta 96

El modelo de embedding se reconoce por el nombre del modelo base contenido en el ID configurado: un ID de modelo base, un ID de perfil de inferencia entre regiones (``us.``, ``eu.``, ``global.`` ...) o un ARN que contenga alguno de ellos.
Los perfiles de inferencia de aplicación tienen IDs opacos y no se reconocen.

.. note::
   Para consultar los modelos disponibles en cada región, vea `Supported foundation models in Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html>`__.

Requisitos previos
==================

1. **Cuenta de AWS** con Amazon Bedrock disponible en la región que utilice
2. **Acceso a los modelos**: los modelos que configure deben poder usarse desde su cuenta en esa región
3. **Credenciales**: una clave API de Bedrock o credenciales de AWS con permiso para llamar a los modelos (consulte :ref:`bedrock-authentication`)

Instalación del plugin
======================

La integración con Bedrock se proporciona como plugin ``fess-llm-bedrock``.
Instálelo desde "Sistema" > "Plugins" en la pantalla de administración, o coloque el archivo JAR manualmente y reinicie |Fess|.

::

    cp fess-llm-bedrock-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   La versión del plugin debe coincidir con la versión de |Fess|.

Configuración básica
====================

El proveedor LLM (``rag.llm.name``) se selecciona en la pantalla de administración (Administración > Sistema > General) o en ``system.properties``.
La habilitación del modo de búsqueda IA y las configuraciones ``rag.llm.bedrock.*`` se escriben en ``fess_config.properties``.

``system.properties`` (también configurable en Administración > Sistema > General):

::

    rag.llm.name=bedrock

``app/WEB-INF/classes/fess_config.properties`` (``/etc/fess/fess_config.properties`` en instalaciones por paquete), con credenciales de AWS:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.model=us.amazon.nova-2-lite-v1:0

Con una clave API de Bedrock en lugar de credenciales de AWS:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.api.key=your-bedrock-api-key

Elementos de configuración
==========================

Todos los elementos de configuración del cliente del modo de búsqueda IA. Se configuran en ``fess_config.properties`` (o como opciones JVM ``-Dfess.config.<key>``).

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.llm.bedrock.api.key``
     - Clave API de Bedrock. Si está vacía, las solicitudes se firman con credenciales de AWS (SigV4)
     - ``""``
   * - ``rag.llm.bedrock.region``
     - Región de AWS del endpoint de Bedrock Runtime y de la firma SigV4
     - ``us-east-1``
   * - ``rag.llm.bedrock.endpoint``
     - URL del endpoint, por ejemplo un endpoint de interfaz de VPC. Si está vacía, ``https://bedrock-runtime.<region>.amazonaws.com``
     - ``""``
   * - ``rag.llm.bedrock.model``
     - ID de modelo, ID de perfil de inferencia o ARN
     - ``us.amazon.nova-2-lite-v1:0``
   * - ``rag.llm.bedrock.timeout``
     - Timeout de solicitud (milisegundos)
     - ``120000``
   * - ``rag.llm.bedrock.availability.check.interval``
     - Intervalo de verificación de disponibilidad (segundos)
     - ``60``
   * - ``rag.llm.bedrock.temperature.enabled``
     - ``false`` impide que se envíe ``temperature``, para modelos o modos que lo rechazan
     - ``true``
   * - ``rag.llm.bedrock.additional.model.request.fields``
     - Objeto JSON enviado como ``additionalModelRequestFields`` para parámetros específicos del modelo
     - ``""``
   * - ``rag.llm.bedrock.max.concurrent.requests``
     - Número máximo de solicitudes simultáneas
     - ``5``
   * - ``rag.llm.bedrock.concurrency.wait.timeout``
     - Tiempo de espera de solicitudes simultáneas (milisegundos)
     - ``30000``
   * - ``rag.llm.bedrock.answer.context.max.chars``
     - Número máximo de caracteres del contexto recuperado para la generación de respuestas
     - ``16000``
   * - ``rag.llm.bedrock.summary.context.max.chars``
     - Número máximo de caracteres del documento para la generación de resúmenes
     - ``16000``
   * - ``rag.llm.bedrock.faq.context.max.chars``
     - Número máximo de caracteres del contexto recuperado para la generación de FAQ
     - ``10000``
   * - ``rag.llm.bedrock.chat.evaluation.max.relevant.docs``
     - Número máximo de documentos relevantes en la evaluación
     - ``3``
   * - ``rag.llm.bedrock.chat.evaluation.description.max.chars``
     - Número máximo de caracteres para la descripción del documento en la evaluación
     - ``500``
   * - ``rag.llm.bedrock.history.max.chars``
     - Número máximo de caracteres del historial de chat
     - ``8000``
   * - ``rag.llm.bedrock.intent.history.max.messages``
     - Número máximo de mensajes del historial para la determinación de intención
     - ``8``
   * - ``rag.llm.bedrock.intent.history.max.chars``
     - Número máximo de caracteres del historial para la determinación de intención
     - ``4000``
   * - ``rag.llm.bedrock.history.assistant.max.chars``
     - Número máximo de caracteres del historial del asistente
     - ``800``
   * - ``rag.llm.bedrock.history.assistant.summary.max.chars``
     - Número máximo de caracteres del resumen del historial del asistente
     - ``800``
   * - ``rag.llm.bedrock.retry.max``
     - Número máximo de intentos HTTP (en errores ``429``, ``500``, ``502``, ``503`` y ``504``)
     - ``10``
   * - ``rag.llm.bedrock.retry.base.delay.ms``
     - Retardo base del backoff exponencial (milisegundos)
     - ``2000``

.. _bedrock-authentication:

Autenticación
=============

Clave API
---------

Cuando se define ``rag.llm.bedrock.api.key``, se envía como ``Authorization: Bearer <key>``.
Las claves API de Bedrock de corta duración caducan y solo son válidas en la región en la que se crearon; las de larga duración están asociadas a un usuario de IAM.
El valor se enmascara en Administración > Sistema > Información del sistema cuando se define en ``fess_config.properties`` (o, en el caso de ``content_chunker.embedding.bedrock.api.key``, en ``system.properties``).
Las variables de entorno y las propiedades del sistema JVM, incluidas las opciones ``-Dfess.config.*`` y ``-Dfess.system.*``, se muestran allí sin enmascarar, por lo que no pase la clave de esa manera.

Credenciales de AWS (SigV4)
---------------------------

Si no se define ninguna clave API, cada solicitud se firma con AWS Signature Version 4.
Las credenciales se toman de la primera de estas fuentes que las proporcione:

1. las propiedades del sistema JVM ``aws.accessKeyId`` / ``aws.secretAccessKey`` / ``aws.sessionToken``
2. las variables de entorno ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` / ``AWS_SESSION_TOKEN``
3. identidad web (``AWS_WEB_IDENTITY_TOKEN_FILE`` y ``AWS_ROLE_ARN``, como se usa en Amazon EKS)
4. los archivos compartidos ``~/.aws/credentials`` y ``~/.aws/config`` (``AWS_PROFILE`` selecciona el perfil)
5. el endpoint de credenciales de contenedor (Amazon ECS)
6. el servicio de metadatos de instancia de EC2 (perfil de instancia)

Las propiedades del sistema JVM (fuente 1) solo llegan al proceso web de |Fess|.
El embedding de chunks de contenido (documentos) se ejecuta en una JVM hija independiente, por lo que en ese caso use variables de entorno, un perfil de credenciales compartido o un rol de IAM, o repita las opciones ``-Daws.*`` en ``jvm.chunk.options``.

La región siempre proviene de ``rag.llm.bedrock.region``; ``AWS_REGION`` no se lee.
No se admiten los perfiles que usan IAM Identity Center (SSO).

.. warning::
   Prefiera un rol de IAM (perfil de instancia de EC2, rol de tarea de ECS, identidad web de EKS) o el archivo de credenciales compartido del usuario que ejecuta |Fess|.
   Las variables de entorno y las propiedades del sistema JVM se muestran sin enmascarar en Administración > Sistema > Información del sistema, por lo que no guarde en ellas claves de larga duración.

La entidad de IAM necesita ``bedrock:InvokeModel`` (Converse e InvokeModel) y ``bedrock:InvokeModelWithResponseStream`` (ConverseStream) sobre los modelos que utilice.
Cuando el modelo es un perfil de inferencia, permita tanto el perfil de inferencia como los modelos fundacionales a los que enruta.

Comportamiento de reintentos
============================

Las solicitudes se reintentan ante ``429``, ``500``, ``502``, ``503`` y ``504``, y cuando no se pudo establecer la conexión con Bedrock.
Los reintentos esperan con backoff exponencial (base ``rag.llm.bedrock.retry.base.delay.ms``, jitter de +/-20%, hasta ``rag.llm.bedrock.retry.max`` intentos); un encabezado ``Retry-After`` tiene prioridad.
En las solicitudes de streaming, solo se reintenta la solicitud inicial; un error posterior al inicio del streaming de la respuesta, incluido un evento de excepción dentro del stream, finaliza la solicitud.

Configuración por tipo de prompt
================================

``temperature`` y ``max.tokens`` se pueden configurar por tipo de prompt, igual que en los demás proveedores:

::

    rag.llm.bedrock.{promptType}.temperature
    rag.llm.bedrock.{promptType}.max.tokens
    rag.llm.bedrock.{promptType}.context.max.chars
    rag.llm.bedrock.{promptType}.additional.model.request.fields

``{promptType}`` es uno de ``intent``, ``evaluation``, ``unclear``, ``noresults``, ``docnotfound``, ``direct``, ``faq``, ``answer``, ``summary`` y ``queryregeneration``.
Un ``additional.model.request.fields`` por tipo de prompt reemplaza el valor global para ese tipo de prompt.

Valores predeterminados utilizados cuando no se configura nada:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Tipo de prompt
     - temperature
     - max.tokens
   * - ``intent``, ``evaluation``
     - ``0.1``
     - ``256``
   * - ``unclear``, ``noresults``
     - ``0.7``
     - ``512``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
   * - ``direct``, ``faq``
     - ``0.7``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``

.. note::
   ``rag.llm.bedrock.{promptType}.thinking.budget`` no es compatible: los ajustes de razonamiento difieren según el modelo en Bedrock.
   Un valor configurado no se envía y se registra un WARN. Use ``additional.model.request.fields`` en su lugar.

Parámetros específicos del modelo
=================================

``additional.model.request.fields`` pasa un objeto JSON al modelo tal cual.
Un valor que no sea un objeto JSON no se envía, y se registra un WARN que indica la propiedad.

Por ejemplo, para usar el pensamiento extendido de un modelo Anthropic Claude solo en la generación de respuestas:

::

    rag.llm.bedrock.model=<a Claude model ID or inference profile ID>
    rag.llm.bedrock.temperature.enabled=false
    rag.llm.bedrock.answer.additional.model.request.fields={"thinking":{"type":"enabled","budget_tokens":2048}}
    rag.llm.bedrock.answer.max.tokens=6144

Claude rechaza ``temperature`` mientras el pensamiento está habilitado, y ``max.tokens`` debe ser mayor que ``budget_tokens``.
El texto de razonamiento nunca se muestra a los usuarios; solo se muestra el texto de la respuesta.

Embedding de chunks de contenido
================================

Para usar Bedrock en el embedding de chunks de contenido, configure lo siguiente en ``app/WEB-INF/conf/system.properties`` (``/etc/fess/system.properties`` en los paquetes RPM/DEB, ``/opt/fess/system.properties`` en Docker), o como opciones ``-Dfess.system.<key>``.
A diferencia de ``rag.llm.bedrock.*``, estas claves no se leen desde ``fess_config.properties``.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=bedrock
    content_chunker.embedding.dimension=1024
    content_chunker.embedding.bedrock.region=us-east-1
    content_chunker.embedding.bedrock.model=amazon.titan-embed-text-v2:0

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``content_chunker.embedding.bedrock.api.key``
     - Clave API de Bedrock. Si está vacía, se usan credenciales de AWS
     - ``""``
   * - ``content_chunker.embedding.bedrock.region``
     - Región de AWS
     - ``us-east-1``
   * - ``content_chunker.embedding.bedrock.endpoint``
     - URL del endpoint. Si está vacía, se deriva de la región
     - ``""``
   * - ``content_chunker.embedding.bedrock.model``
     - Modelo de embedding (consulte `Modelos compatibles`_)
     - ``amazon.titan-embed-text-v2:0``
   * - ``content_chunker.embedding.bedrock.normalize``
     - Solo Titan: si los vectores se normalizan
     - ``true``
   * - ``content_chunker.embedding.bedrock.truncate``
     - Solo Cohere: ``truncate`` (``NONE``/``START``/``END`` para v3, ``NONE``/``LEFT``/``RIGHT`` para v4). No se envía si está vacío
     - ``""``
   * - ``content_chunker.embedding.bedrock.timeout``
     - Timeout de solicitud (milisegundos)
     - ``120000``
   * - ``content_chunker.embedding.bedrock.connect.timeout``
     - Timeout de conexión (milisegundos)
     - ``5000``
   * - ``content_chunker.embedding.bedrock.availability.check.interval``
     - Intervalo de verificación de disponibilidad (segundos)
     - ``60``
   * - ``content_chunker.embedding.bedrock.retry.max``
     - Número máximo de intentos HTTP (en errores ``429``, ``500``, ``502``, ``503`` y ``504``)
     - ``10``
   * - ``content_chunker.embedding.bedrock.retry.base.delay.ms``
     - Retardo base del backoff exponencial (milisegundos)
     - ``2000``
   * - ``content_chunker.embedding.bedrock.retry.max.delay.ms``
     - Límite superior de una espera de backoff, incluido ``Retry-After`` (milisegundos)
     - ``60000``

``content_chunker.embedding.dimension`` debe ser un tamaño que el modelo produzca (consulte `Modelos compatibles`_); de lo contrario, el proveedor de embedding se reporta como no disponible con un log ERROR.
Los documentos se incrustan con ``input_type=search_document`` de Cohere y las consultas con ``search_query``.
Cohere Embed v3 acepta como máximo 2048 caracteres por texto. Bedrock rechaza un texto más largo con ``400 ValidationException`` independientemente de lo que indique ``truncate``, y el plugin no acorta ni divide los textos.
``truncate`` (``END`` cuando no se define) se aplica únicamente a un texto de hasta 2048 caracteres que supere los 512 tokens.

Uso de proxy HTTP
=================

Las solicitudes a Bedrock usan la configuración de proxy HTTP común de |Fess| (``http.proxy.host``, ``http.proxy.port``, ``http.proxy.username`` y ``http.proxy.password`` en ``fess_config.properties``).
Las consultas de credenciales que llaman a endpoints de AWS (STS para la identidad web, el endpoint de credenciales de contenedor y el servicio de metadatos de instancia) no usan esta configuración.
Para llegar a Bedrock a través de un endpoint de interfaz de VPC, defina ``rag.llm.bedrock.endpoint`` (y ``content_chunker.embedding.bedrock.endpoint``) con su URL; la configuración de región sigue determinando la región de firma.

Solución de problemas
=====================

El modo de búsqueda IA no está disponible
-----------------------------------------

El cliente se reporta como disponible cuando el modelo y la región están definidos, el endpoint es una URL válida, y además hay una clave API definida o se pueden resolver credenciales de AWS.
Una región o un endpoint no válidos se registran con nivel ERROR. Para ver por qué no se pudieron resolver las credenciales, active DEBUG para ``org.codelibs.fess.llm.bedrock``.
Una consulta de credenciales fallida se recuerda durante 60 segundos, por lo que las credenciales que estén disponibles más tarde se detectan en menos de un minuto.

Acceso denegado
---------------

Un ``403`` con ``type=AccessDeniedException`` en el log WARN significa que la clave API o la entidad de IAM no tiene permiso para invocar el modelo.
Compruebe los permisos de IAM indicados arriba y que el modelo se pueda usar desde su cuenta en la región configurada.

Errores de validación
---------------------

Un ``400`` con ``type=ValidationException`` suele significar que el ID de modelo no está disponible en la región (para algunos modelos solo se puede usar un ID de perfil de inferencia) o que ``additional.model.request.fields`` contiene parámetros que el modelo no acepta.

Configuración de depuración
---------------------------

Active DEBUG para ``org.codelibs.fess.llm.bedrock`` para registrar los cuerpos de solicitud y respuesta del modo de búsqueda IA, así como el motivo por el que no se pudieron resolver las credenciales de AWS.
DEBUG para ``org.codelibs.fess.embedding.bedrock`` registra cómo se normalizó el texto de la consulta y el mismo motivo de las credenciales; no registra las solicitudes de embedding.
Estos loggers nunca escriben claves API, credenciales de AWS ni firmas.

.. warning::
   Otros dos loggers escriben credenciales en DEBUG: el wire logging de Apache HttpClient escribe el encabezado ``Authorization``, y el firmante del SDK de AWS (``software.amazon.awssdk.http.auth.aws.internal.signer``) escribe la solicitud canónica, incluido el ``x-amz-security-token`` de las credenciales temporales.
   Iniciar |Fess| con el nivel de log raíz en DEBUG habilita ambos; mantenga ``org.apache.hc`` y ``software.amazon.awssdk`` en INFO o superior.

Referencias
===========

- :doc:`llm-overview` - Descripción general de la integración LLM
- :doc:`rag-chat` - Detalles del modo de búsqueda IA
- :doc:`search-semantic` - Búsqueda semántica y embedding de chunks de contenido
- `Amazon Bedrock User Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>`__
