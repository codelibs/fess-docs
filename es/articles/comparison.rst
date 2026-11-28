==========================================
Fess frente a otras soluciones de búsqueda
==========================================

Introducción
============

Al implantar la búsqueda de documentos internos o de un sitio web, las opciones incluyen sistemas de búsqueda como Fess, un desarrollo propio sobre un motor de búsqueda como OpenSearch o Apache Solr, servicios externos de búsqueda web y productos comerciales de búsqueda empresarial.
Este artículo primero resume lo que ofrece Fess 15.9 de forma fácil de comprobar y, después, compara en qué se diferencia su papel del de las demás opciones.

.. note::

   La información sobre Fess corresponde a la versión 15.9.
   Para otros productos y servicios, este artículo solo trata diferencias de arquitectura que difícilmente cambian. Las funciones, los precios y la disponibilidad pueden cambiar, así que consulte la documentación más reciente de cada producto.

Qué ofrece Fess
===============

Fess es un sistema de búsqueda que usa OpenSearch como motor de búsqueda.
Ofrece el rastreador, la consola de administración, la interfaz de búsqueda y las API como una sola aplicación, y guarda el índice y la configuración de rastreo en OpenSearch.
No es posible usar Elasticsearch ni Solr como motor de búsqueda.
La licencia es Apache License 2.0.

Muchas funciones se ofrecen como plugins, y solo se instalan las que se necesitan.
Los elementos cuya columna «Requisitos» está vacía en la siguiente tabla funcionan solo con Fess.

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - Elemento
     - Qué ofrece 15.9
     - Requisitos
   * - Rastreo web
     - Rastrea sitios HTTP/HTTPS. Se pueden configurar la autenticación web, los encabezados de solicitud y la asignación de rutas
     -
   * - Rastreo de archivos
     - Rastrea rutas ``file``, ``smb``, ``smb1`` y ``ftp``
     -
   * - Rastreo de almacenamiento en la nube
     - ``s3://`` (Amazon S3 y almacenamiento compatible con S3), ``gcs://`` (Google Cloud Storage)
     - ``fess-storage-s3``, ``fess-storage-gcs``
   * - Bases de datos y SaaS
     - Se importan mediante conectores de almacén de datos (lista en la siguiente sección)
     - Plugins ``fess-ds-*``
   * - Formatos de documento
     - Documentos de Office, PDF, HTML, texto, archivos comprimidos, etc. El OCR de imágenes y PDF escaneados está desactivado de forma predeterminada
     - El comando ``tesseract`` para el OCR
   * - Control de acceso
     - Muestra resultados de búsqueda distintos según el rol, el grupo y el usuario. En el rastreo de SMB y de archivos, los permisos de los archivos se importan como roles. La integración con LDAP (incluido Active Directory) es una función del núcleo
     -
   * - Inicio de sesión único
     - OpenID Connect, SAML, SPNEGO (Kerberos), Microsoft Entra ID
     - ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``
   * - Interfaz de búsqueda
     - Se muestra con un tema estático (HTML, CSS y JavaScript empaquetados en un ZIP). El tema incluido es ``bootstrap``
     -
   * - API
     - ``/api/v2`` para búsqueda, etiquetas, sugerencias, palabras populares, comprobación de estado, modo de búsqueda con IA, etc.; ``/api/admin`` para la administración
     -
   * - API heredadas
     - ``/api/v1``, ``/json`` y ``/suggest``
     - ``fess-webapp-v1-api``, ``fess-webapp-classic-api``
   * - Búsqueda semántica
     - Divide el contenido en fragmentos (chunks), los vectoriza y combina los resultados con los de la búsqueda por palabras clave mediante Rank Fusion. Desactivada de forma predeterminada
     - Un modelo de embeddings (ML Commons de OpenSearch o un plugin ``fess-llm-*``)
   * - Modo de búsqueda con IA (RAG)
     - Un LLM responde a partir de los resultados de búsqueda. Desactivado de forma predeterminada
     - Uno de ``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``
   * - Servidor MCP
     - Permite que los agentes de IA busquen en Fess a través de ``/mcp``
     - ``fess-webapp-mcp``
   * - Búsqueda de imágenes
     - Búsqueda multimodal que encuentra imágenes (GIF, JPEG, PNG) a partir de una descripción en texto
     - ``fess-webapp-multimodal`` y un servidor CLIP

La imagen de Docker incluye los cuatro plugins de SSO, ``fess-storage-s3``, ``fess-storage-gcs`` y ``fess-script-groovy``.
Los demás plugins se instalan desde [Sistema] > [Plugin] y, a continuación, se reinicia Fess.
Elija la versión del plugin que coincida con la versión menor de Fess (15.9.x para 15.9).

Conectores de almacén de datos
------------------------------

Para 15.9 están publicados los siguientes plugins de almacén de datos.
La configuración se describe en la referencia de cada conector.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Categoría
     - Plugin (destino)
   * - Almacenamiento en la nube
     - ``fess-ds-box`` (Box), ``fess-ds-dropbox`` (Dropbox), ``fess-ds-gsuite`` (Google Drive), ``fess-ds-microsoft365`` (OneDrive, SharePoint Online, Teams, etc.)
   * - Colaboración
     - ``fess-ds-atlassian`` (Confluence, Jira), ``fess-ds-slack`` (Slack), ``fess-ds-notion`` (Notion), ``fess-ds-backlog`` (Backlog), ``fess-ds-sharepoint`` (SharePoint Server local)
   * - Desarrollo y sistemas de negocio
     - ``fess-ds-git`` (repositorios Git), ``fess-ds-salesforce`` (Salesforce)
   * - Datos
     - ``fess-ds-db`` (bases de datos accesibles mediante JDBC), ``fess-ds-csv`` (CSV), ``fess-ds-json`` (JSON), ``fess-ds-wikipedia`` (volcados de Wikipedia)

Una fuente de datos que no figure aquí puede hacerse buscable escribiendo su propio plugin de almacén de datos (:doc:`guide-17`) o registrando los documentos mediante la API de administración (:doc:`guide-11`).

Frente a un desarrollo propio sobre un motor de búsqueda (OpenSearch, Apache Solr)
==================================================================================

OpenSearch y Apache Solr son motores de búsqueda.
Se encargan de la indexación y la búsqueda, pero no incluyen un rastreador para recopilar datos, una interfaz de búsqueda para los usuarios ni un control de acceso por documento.
Estas partes se desarrollan por cuenta propia o se combinan con otro software.
Para el rastreo web, por ejemplo, existen proyectos independientes como Apache Nutch.

Fess es una aplicación que ofrece estas partes sobre OpenSearch.
Las diferencias son las siguientes.

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - Aspecto
     - Fess
     - Desarrollo propio sobre un motor de búsqueda
   * - Recopilación de datos
     - Los rastreos web, de archivos y de almacén de datos se configuran en la consola de administración
     - Crear rastreadores y procesos de importación, o combinar otro software
   * - Interfaz de búsqueda
     - Se muestra con un tema. Para cambiar el aspecto, cree un tema o construya su propia interfaz sobre la API
     - Totalmente libre, pero hay que desarrollarlo todo
   * - Control de acceso
     - Los roles y los permisos de los archivos se registran en cada documento, y la búsqueda se filtra según el usuario que ha iniciado sesión
     - Diseñar e implementar tanto la importación de los permisos de los documentos como el filtrado en el momento de la búsqueda
   * - Diseño del índice
     - Usa el índice definido por Fess. Hay analizadores preconfigurados para muchos idiomas, incluido el español
     - Se puede diseñar libremente según el uso
   * - Qué hay que operar
     - Fess y OpenSearch
     - El motor de búsqueda y todas las partes desarrolladas internamente

Si quiere diseñar el mecanismo de búsqueda desde cero o buscar en estructuras de datos propias, es más adecuado usar directamente un motor de búsqueda.
En cambio, si el objetivo es recopilar documentos y hacerlos buscables dentro de la organización, empezar con Fess y cubrir lo que falte con la API o con plugins reduce el alcance del desarrollo.

Fess también puede conectarse a un clúster de OpenSearch existente.
En servicios donde no se pueden instalar los plugins de CodeLibs, como Amazon OpenSearch Service, establezca ``search_engine.type`` en ``aws`` o ``vanilla``.
En ese caso, algunas funciones, como la gestión de diccionarios y la detección de documentos duplicados, no están disponibles (consulte `Tipo de motor de búsqueda <https://fess.codelibs.org/es/stable/config/search-engine-type.html>`__).

Frente a la búsqueda en el sitio mediante un servicio externo de búsqueda web
=============================================================================

Otra forma de ofrecer búsqueda en un sitio es usar el índice de un proveedor de servicios de búsqueda.
Con este método, solo se pueden buscar las páginas públicas que haya obtenido el rastreador del proveedor.
No se pueden incluir páginas que requieren inicio de sesión ni servidores de archivos internos, y cuándo se rastrea y en qué orden se muestran los resultados también depende del proveedor.

Con Fess, usted decide qué se rastrea y cuándo, y el índice permanece en su propio entorno.
Para ajustar los resultados de búsqueda puede usar, entre otras funciones, Coincidencia de clave (mostrar documentos concretos en las primeras posiciones para términos concretos), Impulso de documento y Consulta relacionada.
Hay dos formas de integrar Fess en un sitio existente.

- Colocar un formulario de búsqueda que lleve a la interfaz de búsqueda de Fess (tema)
- Insertar el JavaScript de Fess Site Search (FSS) para mostrar los resultados de búsqueda dentro de la página

FSS llama a ``/api/v1``, por lo que en 15.9 se necesita el plugin ``fess-webapp-v1-api``.
Consulte :doc:`guide-03` para ver el procedimiento.

Frente a los productos comerciales de búsqueda empresarial
==========================================================

Al comparar con productos comerciales, el alcance varía mucho de un producto a otro, por lo que no se puede decir en términos generales cuál es mejor.
Recomendamos comprobar los productos candidatos y Fess en las mismas condiciones según los siguientes aspectos.

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Aspecto
     - En el caso de Fess
   * - Fuentes de datos admitidas
     - Consulte la tabla de la sección anterior y la lista de conectores de almacén de datos. Si falta algo, puede escribir su propio plugin
   * - Control de acceso
     - Por rol, grupo y usuario, con compatibilidad con LDAP y cuatro métodos de SSO
   * - IA generativa
     - Modo de búsqueda con IA (RAG), búsqueda semántica y servidor MCP. El LLM se elige entre Ollama (alojado por usted), OpenAI, Gemini y Amazon Bedrock
   * - Ubicación de los datos
     - El índice se guarda en un OpenSearch que usted mismo opera. Si usa servicios externos para el LLM o los embeddings, las preguntas y el contenido de los documentos se envían a esos servicios
   * - Modelo de operación
     - Software que se aloja y opera uno mismo. Se puede instalar con Docker, en Linux (ZIP, RPM, DEB) y en Windows. También funciona en Kubernetes, pero no hay un chart de Helm oficial
   * - Costes y soporte
     - No hay costes de licencia. Los costes son los servidores y el esfuerzo de operación. Para el soporte comercial, consulte `Soporte comercial <https://fess.codelibs.org/es/support-services.html>`__
   * - Libertad de modificación
     - El código fuente es público, y Fess se puede ampliar con temas, plugins y la API

Los productos comerciales son adecuados cuando el producto ya ofrece los conectores y las funciones de gestión necesarios y se quiere delegar la operación en el proveedor.
Fess es adecuado cuando se quiere construir una plataforma de búsqueda combinando las funciones necesarias y manteniendo los datos en el propio entorno.

Cómo elegir
===========

Responda a las siguientes preguntas en orden para decidir si Fess es un candidato.

1. ¿Los datos que quiere buscar están cubiertos por los destinos de rastreo o los conectores de almacén de datos de Fess?

   - Si no lo están, estime el desarrollo necesario para escribir su propio plugin (:doc:`guide-17`) o para registrar los documentos mediante la API (:doc:`guide-11`).

2. ¿Necesita mostrar documentos distintos a cada usuario?

   - Para usar los permisos del servidor de archivos, consulte :doc:`file-server-search`; para el diseño de roles, :doc:`guide-05`; para el SSO, :doc:`guide-15`.

3. ¿Le basta el tema de Fess para la interfaz de búsqueda?

   - Para integrar la búsqueda en su propia aplicación, use ``/api/v2`` (:doc:`guide-11`).

4. ¿Puede operar Fess y OpenSearch por su cuenta?

   - Si no puede, o si quiere delegar la operación en un proveedor, considere el soporte comercial de Fess o un producto comercial.

5. ¿Necesita respuestas con IA generativa o búsqueda semántica?

   - Decida qué LLM usar y compruebe la configuración necesaria en :doc:`guide-19` y :doc:`guide-18`.

Si las respuestas a 1 y 4 son «sí», lo más fiable es probar Fess y comprobar los resultados de búsqueda con sus documentos reales.

Probar para comprobar
=====================

Una tabla comparativa por sí sola no indica qué tan bien se pueden buscar sus propios documentos.
Inicie Fess con Docker siguiendo el procedimiento de :doc:`guide-02`, rastree una parte de lo que quiere buscar y compruebe lo siguiente.

- Si los documentos de destino se han indexado (compruebe en [Información del sistema] > [Registro de trabajo] y [URL de fallo] que no haya URL que terminaran en error)
- Si al buscar términos de uso frecuente aparecen arriba los documentos esperados
- Si, al cambiar de usuario con sesión iniciada, siguen ocultos los documentos que no deberían verse (si necesita control de acceso)

Artículos recomendados a continuación
=====================================

- Conocer la arquitectura de Fess y cómo recorrer los artículos: :doc:`guide-01`
- Ponerlo en marcha primero en local: :doc:`guide-02`
- Integrar la búsqueda en un sitio existente: :doc:`guide-03`
- Buscar datos de bases de datos o de SaaS: :doc:`datastore-basics`
- Reflejar los permisos del servidor de archivos en los resultados de búsqueda: :doc:`file-server-search`
- Hacer que una IA generativa responda a partir de documentos internos: :doc:`guide-19`
- Prepararse para el crecimiento: :doc:`guide-14`
- Conocer ejemplos de uso: :doc:`use-cases`

Referencias
===========

- `Descripción general de los conectores de almacén de datos <https://fess.codelibs.org/es/stable/config/datastore/ds-overview.html>`__
- `Rastreo de sistema de archivos (búsqueda en servidores de archivos) <https://fess.codelibs.org/es/stable/admin/fileconfig-guide.html>`__
- `Archivos objetivo de búsqueda <https://fess.codelibs.org/es/supported-files.html>`__
- `Configuración de OCR <https://fess.codelibs.org/es/stable/config/crawler-ocr.html>`__
- `Tema <https://fess.codelibs.org/es/stable/admin/theme-guide.html>`__
- `Descripción general de la API <https://fess.codelibs.org/es/stable/api/api-overview.html>`__
- `Búsqueda semántica <https://fess.codelibs.org/es/stable/config/search-semantic.html>`__
- `Descripción general de la búsqueda IA (RAG) y la integración LLM <https://fess.codelibs.org/es/stable/config/llm-overview.html>`__
- `Tipo de motor de búsqueda <https://fess.codelibs.org/es/stable/config/search-engine-type.html>`__
- `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
