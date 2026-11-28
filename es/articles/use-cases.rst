===============================================
Casos de uso y escenarios de aplicación de Fess
===============================================

Introducción
============

Esta página presenta las situaciones en las que se suele utilizar Fess, organizadas por sector, por escala y por objetivo técnico.
Para cada escenario se indican el problema que se quiere resolver, las funciones y los plugins de Fess que se utilizan y los artículos que explican los pasos.
Los pasos de configuración en sí están en cada artículo, así que parta del escenario más parecido a su situación para elegir qué artículos leer.

Los nombres de funciones y plugins de esta página corresponden a Fess 15.9.
En la versión 15.9, la importación desde bases de datos y servicios SaaS, el SSO y el rastreo de S3 y GCS se ofrecen mediante plugins.
Utilice para los plugins la misma versión 15.9.x que Fess y reinicie Fess después de instalarlos.
Para saber cómo instalarlos, consulte `Plugins <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__.

.. note::

   Lo que sigue son patrones de uso generales. Para conocer casos reales de implantación, póngase en contacto con el `soporte comercial <../support-services.html>`__.

Buscar funciones según el objetivo
==================================

.. list-table::
   :header-rows: 1
   :widths: 34 38 28

   * - Lo que quiere hacer
     - Funciones y plugins
     - Artículos que leer
   * - Probarlo primero en local
     - Docker Compose (docker-fess)
     - :doc:`guide-02`
   * - Buscar a la vez en el sitio de la intranet y en los servidores de archivos
     - Rastreo web, rastreo del sistema de archivos, Autenticación de archivos, etiquetas
     - :doc:`guide-04`, :doc:`file-server-search`
   * - Mostrar documentos distintos según el departamento o el cargo
     - Permisos, roles y grupos, LDAP (Active Directory)
     - :doc:`guide-05`
   * - Añadir un cuadro de búsqueda a un sitio existente
     - Formulario de búsqueda, Fess Site Search (``fess-webapp-v1-api``), temas
     - :doc:`guide-03`
   * - Buscar en Git, Confluence, Jira y Slack
     - ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack``
     - :doc:`datastore-basics`, :doc:`guide-06`
   * - Buscar en Google Drive, SharePoint Online y Box
     - ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box``
     - :doc:`datastore-basics`, :doc:`guide-07`
   * - Buscar en bases de datos, CSV y Salesforce
     - ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce``
     - :doc:`datastore-basics`, :doc:`guide-12`
   * - Buscar desde los sistemas de negocio
     - API de búsqueda (``/api/v2``), tokens de acceso
     - :doc:`guide-11`
   * - Permitir buscar con el inicio de sesión de la empresa
     - ``fess-sso-entraid``, ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``
     - :doc:`guide-15`
   * - Compartir un solo Fess entre varias organizaciones
     - Hosts virtuales, roles, etiquetas
     - :doc:`guide-13`
   * - Analizar los términos sin resultados y el uso de la búsqueda para mejorarla
     - [Información del sistema] > [Registro de búsqueda]
     - :doc:`guide-08`
   * - Encontrar documentos de significado parecido, obtener respuestas de una IA
     - Búsqueda semántica, modo de búsqueda IA, ``fess-webapp-mcp``
     - :doc:`guide-18`, :doc:`guide-19`, :doc:`guide-20`
   * - Prepararse para el aumento de documentos y usuarios
     - Separación y clúster de OpenSearch, varios servidores Fess
     - :doc:`guide-14`
   * - Funcionar de forma estable en producción
     - ``/api/v2/health``, copias de seguridad, registros
     - :doc:`guide-10`

Casos de uso por sector
=======================

Industria manufacturera: encontrar documentos técnicos dispersos
----------------------------------------------------------------

**Problema**: los documentos de diseño, las especificaciones y los registros de calidad están repartidos en los servidores de archivos de cada departamento, y encontrar el material relacionado a partir de un número de plano o de modelo lleva tiempo.

**Funciones que se utilizan**:

- Rastree los servidores de archivos con ``smb://`` para que el texto de los PDF y de los documentos de Office se pueda buscar. Los permisos de acceso de Windows (ACL) se importan de forma predeterminada como permisos de los documentos
- Cree etiquetas con nombres visibles como "Diseño" y "Calidad", clasifique los documentos según las rutas que abarcan y permita filtrar por ellas en la página de búsqueda
- Los registros en papel escaneados se pueden buscar por su texto si se activa el OCR. El OCR está desactivado de forma predeterminada y requiere ``tesseract`` en el host donde se ejecuta el rastreador (`Configuración de OCR <https://fess.codelibs.org/es/stable/config/crawler-ocr.html>`__)

Los archivos en formatos de los que Fess no puede extraer el texto solo se encuentran por su nombre o su ruta.
Compruebe los formatos admitidos en `Archivos compatibles <../supported-files.html>`__.

**Artículos que leer**: construya la configuración con :doc:`guide-04`, compruebe los requisitos previos de las ACL en :doc:`file-server-search` y configure la visibilidad por departamento con :doc:`guide-05`.

Finanzas y seguros: encontrar normativas y contratos con permisos
-----------------------------------------------------------------

**Problema**: hay una gran cantidad de normativas internas, manuales y contratos, y buscarlos en cada consulta o auditoría supone un esfuerzo. Al mismo tiempo, se quiere separar de forma estricta por departamento quién puede consultarlos.

**Funciones que se utilizan**:

- Con los permisos por documento se limita a quién se muestra cada documento en los resultados de búsqueda. Los permisos de una nueva configuración de rastreo incluyen ``{role}guest`` desde el principio; elimínelo en los documentos que no sean públicos
- Para que los usuarios que no han iniciado sesión no puedan buscar, active "Requiere inicio de sesión" en [General]
- Para iniciar sesión con la plataforma de identidad de la empresa, utilice SSO: ``fess-sso-saml`` para SAML y ``fess-sso-entraid`` para Entra ID (la imagen de Docker incluye los cuatro plugins de SSO)
- Para buscar desde los sistemas de negocio, guarde un token de acceso en el lado del servidor y llame a la API de búsqueda

**Artículos que leer**: diseñe los permisos con :doc:`guide-05` y configure SSO y HTTPS con :doc:`guide-15`. La integración con los sistemas de negocio se trata en :doc:`guide-11`.

Educación: buscar de forma transversal en los sitios y unidades compartidas del campus
--------------------------------------------------------------------------------------

**Problema**: los sitios web de cada facultad, los materiales de las clases y los documentos internos de la institución están en lugares distintos, y ni los estudiantes ni el personal llegan a la información que buscan.

**Funciones que se utilizan**:

- Importe los sitios web del campus mediante rastreo web. Los repositorios institucionales (como DSpace) no tienen un conector específico, así que rastree sus páginas públicas
- Importe las unidades compartidas de Google Drive con ``fess-ds-gsuite`` y SharePoint Online con ``fess-ds-microsoft365``
- Para mostrar ámbitos distintos a estudiantes y a personal, sepárelos con roles y permisos. Si quiere dividir el propio sitio, utilice hosts virtuales

**Artículos que leer**: :doc:`guide-04`, :doc:`guide-07`, :doc:`guide-05`. Para dividir el sitio, consulte :doc:`guide-13`.

TI y software: encontrar la información de desarrollo en un solo lugar
----------------------------------------------------------------------

**Problema**: el código está en Git, el diseño en Confluence, las incidencias en Jira y las conversaciones en Slack o Teams, por lo que cuesta reconstruir lo que se decidió en el pasado.

**Funciones que se utilizan**:

- Importe los archivos de los repositorios con ``fess-ds-git``, Confluence y Jira con ``fess-ds-atlassian`` y los mensajes de Slack con ``fess-ds-slack``
- Los canales y chats de Teams se pueden importar con el ``TeamsDataStore`` de ``fess-ds-microsoft365`` (`Conector de Microsoft 365 <https://fess.codelibs.org/es/stable/config/datastore/ds-microsoft365.html>`__)
- Como configuración especializada en la búsqueda de código fuente, está publicado `docker-codesearch <https://github.com/codelibs/docker-codesearch>`__
- Para integrar la búsqueda en herramientas internas, utilice la API de búsqueda; para que busquen agentes de IA, utilice ``fess-webapp-mcp``

**Artículos que leer**: :doc:`datastore-basics` y después :doc:`guide-06`. La integración con agentes de IA se trata en :doc:`guide-20`.

Casos de uso por escala
=======================

El número de servidores y la memoria necesarios no dependen solo del número de usuarios o de documentos.
La carga cambia con la longitud del texto, la proporción de archivos adjuntos y si los usuarios inician sesión o no, así que empiece con poco, mida y amplíe lo que falte.
Los pasos para decidirlo se resumen en la sección sobre las orientaciones de escala de :doc:`guide-14`.
Para los requisitos de servidor recomendados para producción (4 o más núcleos de CPU, 8 GB o más de memoria, etc.), consulte `Requisitos del sistema <https://fess.codelibs.org/es/stable/install/prerequisites.html>`__.

Empezar con un servidor
-----------------------

Para una implantación a nivel de departamento o una prueba, ejecute Fess y OpenSearch en un solo servidor.
Con Docker Compose, se inicia con dos archivos: ``compose.yaml`` y ``compose-opensearch3.yaml``.
Los pasos están en :doc:`guide-02`.

Incluso con un solo servidor, decida desde el principio los dos puntos siguientes.

- Cómo hacer las copias de seguridad. La configuración se puede descargar desde [Información del sistema] > [Copia de seguridad], pero no incluye los diccionarios (:doc:`guide-10`)
- Con Docker, la configuración modificada en [Sistema] > [General] se guarda en ``system.properties`` dentro del contenedor y vuelve a su estado original al recrear el contenedor (consulte la sección sobre detener y reanudar en :doc:`guide-02`)

Cuando se suman más departamentos
---------------------------------

Cuando la búsqueda o el rastreo se vuelvan lentos, averigüe primero si la causa está en el propio Fess, en el rastreador o en OpenSearch.
En la mayoría de los casos, se amplía en el orden siguiente.

1. Con un solo servidor, ajustar el heap de Fess, del rastreador y de OpenSearch, así como el paralelismo del rastreo
2. Separar OpenSearch en otro servidor
3. Convertir OpenSearch en un clúster de tres nodos
4. Ejecutar varios servidores Fess y repartir las peticiones con un balanceador de carga

Con varios servidores Fess, mantenga iguales en todos ellos la configuración de [General], ``app.cipher.key`` en ``fess_config.properties`` y los plugins instalados.
En Fess 15.9, las sesiones de inicio de sesión se guardan en la memoria de cada servidor, por lo que, al repartir pantallas que se usan con sesión iniciada, active las sesiones persistentes (sticky sessions) en el balanceador de carga.
Guardar las sesiones en OpenSearch para compartirlas entre servidores es posible a partir de la versión 15.10.

**Artículos que leer**: :doc:`guide-14`, :doc:`guide-10`.

Uso en toda la empresa
----------------------

A escala de toda la empresa, considere lo siguiente además de la configuración anterior.

- Asigne el rastreo a un único servidor Fess (``scheduler.target.name`` y el "Objetivo" del trabajo). Así la carga del rastreo no recae en los servidores que atienden las búsquedas
- Utilice ``/api/v2/health`` para el balanceador de carga y la monitorización. Devuelve 503 cuando el clúster de OpenSearch está en ``RED`` o no se puede conectar con él
- Para separar la página de búsqueda o los destinos de búsqueda por organización, utilice hosts virtuales o instancias de Fess separadas (:doc:`guide-13`)
- Revise periódicamente en el registro de búsqueda los términos sin resultados y los términos cuyos resultados no reciben clics (:doc:`guide-08`)

Fess también puede ejecutarse en Kubernetes, pero no se ofrece un chart de Helm oficial.
Convierta los archivos de Docker Compose o escriba usted mismo los manifiestos (consulte las preguntas frecuentes de `Instalación con Docker (detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__).

Para implantaciones en entornos de gran escala, considere también el `soporte comercial <../support-services.html>`__.

Casos de uso técnicos
=====================

Búsqueda transversal en wikis internos y bases de conocimiento
--------------------------------------------------------------

La forma de importar el contenido depende del tipo de wiki.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Destino
     - Forma de importación
     - Referencia
   * - Confluence
     - ``fess-ds-atlassian`` (``ConfluenceDataStore``)
     - :doc:`guide-06`
   * - Notion
     - ``fess-ds-notion``
     - `Conector de Notion <https://fess.codelibs.org/es/stable/config/datastore/ds-notion.html>`__
   * - Backlog
     - ``fess-ds-backlog``
     - `Conector de Backlog <https://fess.codelibs.org/es/stable/config/datastore/ds-backlog.html>`__
   * - Wikis que se pueden consultar en la web, como MediaWiki
     - Rastreo web (si se requiere inicio de sesión, configure también la Autenticación web)
     - :doc:`guide-04`

Los documentos importados mediante un almacén de datos también incluyen ``{role}guest`` en sus permisos desde el principio.
Si importa espacios que solo puede leer un grupo limitado de personas, lea primero la sección de :doc:`guide-06` sobre a quién mostrar los resultados de búsqueda.

Búsqueda unificada en servidores de archivos
--------------------------------------------

Los protocolos que admite el rastreo de archivos de Fess 15.9 son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Formato de la ruta
     - Destino
   * - ``smb://``
     - Carpetas compartidas de Windows o NAS compartidos por SMB
   * - ``smb1://``
     - Servidores antiguos que solo admiten SMB1
   * - ``file:``
     - Directorios visibles desde el servidor de Fess. Los recursos compartidos NFS se montan primero en el sistema operativo y luego se indican en este formato
   * - ``ftp://``
     - Servidores FTP
   * - ``s3://`` / ``gcs://``
     - Almacenamiento compatible con Amazon S3 / Google Cloud Storage. Requiere ``fess-storage-s3`` / ``fess-storage-gcs`` (incluidos en la imagen de Docker)

Los protocolos activados de forma predeterminada son ``file``, ``smb``, ``smb1`` y ``ftp`` (``crawler.file.protocols``).
Para que las ACL de SMB se reflejen en los resultados de búsqueda, debe eliminar ``{role}guest`` de los permisos de la configuración de rastreo.
El motivo y la forma de comprobarlo están en :doc:`file-server-search`, y la configuración concreta en :doc:`guide-04`.

Búsqueda dentro de un sitio web
-------------------------------

Hay tres formas de añadir búsqueda a un sitio público, y se pueden combinar.

- Colocar un formulario de búsqueda que lleve a la página de búsqueda de Fess. No hace falta ninguna configuración adicional en Fess
- Mostrar los resultados de búsqueda dentro de una página existente con Fess Site Search (FSS). FSS llama a ``/api/v1``, por lo que en 15.9 requiere el plugin ``fess-webapp-v1-api``. Fess no sirve el JavaScript de FSS, así que genérelo con FSS JS Generator y colóquelo en su propio sitio
- Adaptar la página de búsqueda de Fess al aspecto del sitio existente mediante un tema

Los pasos están en :doc:`guide-03`.
Para crear su propia página de búsqueda, utilice ``/api/v2/search`` (:doc:`guide-11`).

Búsqueda en bases de datos
--------------------------

La información almacenada en bases de datos, como los maestros de productos o las preguntas frecuentes, se importa con ``fess-ds-db``.
Admite bases de datos compatibles con JDBC (MySQL, PostgreSQL, Oracle, SQL Server, etc.), y el controlador JDBC adecuado para el destino se proporciona por separado.
Un script asigna las columnas obtenidas con una sentencia SELECT a campos como ``title`` y ``content``.

Si construye la URL de la pantalla de negocio original y la guarda en ``url``, los usuarios pueden abrir los datos originales directamente desde el enlace del resultado de búsqueda.
Los pasos están en :doc:`guide-12`.

Combinar con IA generativa
--------------------------

- Encontrar documentos de significado parecido aunque las palabras clave no coincidan: búsqueda semántica (:doc:`guide-18`)
- Hacer que una IA responda basándose en los documentos internos: modo de búsqueda IA. Funciona también sin búsqueda vectorial (:doc:`guide-19`)
- Permitir que agentes de IA como Claude Code busquen en Fess: ``fess-webapp-mcp`` (:doc:`guide-20`)

Con cualquiera de los métodos, los documentos buscados se filtran con los mismos permisos que una búsqueda normal (en el modo de búsqueda IA, los del usuario que ha iniciado sesión; en MCP, los del token de acceso, o los permisos de invitado si MCP se usa sin autenticación).
Estos permisos también determinan qué documentos llegan a la IA, así que complete primero el diseño de permisos de :doc:`guide-05`.

Cómo llevar a cabo la implantación
==================================

1. Iniciar Fess con :doc:`guide-02`, rastrear una parte de los destinos y probar la búsqueda
2. En la tabla anterior, elegir los artículos que se ajustan a su problema y realizar la configuración
3. Decidir los permisos (:doc:`guide-05`) y la operación (:doc:`guide-10`) antes de abrirlo a los usuarios

Referencias
===========

- `Inicio rápido <../quick-start.html>`__
- `Documentación <../documentation.html>`__
- `Plugins <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `Guía de conectores de almacén de datos <https://fess.codelibs.org/es/stable/config/datastore/index.html>`__
- `Foro de discusión <https://discuss.codelibs.org/c/FessEN/>`__
- `GitHub <https://github.com/codelibs/fess>`__
