=========================================
Qué permite hacer Fess y cómo implantarlo
=========================================

Introducción
============

Los documentos internos están repartidos entre sitios web, servidores de archivos, almacenamiento en la nube, servicios SaaS como el chat o la gestión de tickets, y bases de datos.
Aunque cada herramienta tenga su propia búsqueda, no es posible buscar en todos esos lugares a la vez.
Fess es un servidor de búsqueda que reúne los documentos de esos lugares en un único índice para que se puedan buscar desde una sola página de búsqueda o API.

Este artículo está dirigido al personal de TI y a los desarrolladores que están considerando implantar Fess, y explica lo siguiente:

- De qué se compone Fess y cómo funciona
- Qué funciones están disponibles de serie y cuáles requieren plugins adicionales
- Qué artículos leer a continuación según su objetivo

Los pasos de configuración de cada función se tratan en los artículos correspondientes.

Versión cubierta por esta guía práctica
=======================================

Todos los artículos de esta guía práctica se basan en Fess 15.9.
Los nombres de los campos de la interfaz, las claves de configuración y los valores predeterminados se han comprobado en la versión 15.9.
Cuando un artículo presenta una función que solo está disponible a partir de la versión 15.10, lo indica de forma explícita.

Los enlaces a la documentación de referencia empiezan por ``https://fess.codelibs.org/es/stable/`` y apuntan a la documentación de la versión estable actual.
Si utiliza otra versión, sustituya ``stable`` en la URL por el número de versión (por ejemplo, ``15.9``) y compruebe los nombres de los campos y los valores predeterminados en esa página.

¿Qué es Fess?
=============

Fess es un servidor de búsqueda de texto completo de código abierto escrito en Java.
Se distribuye bajo la licencia Apache License 2.0 y puede utilizarse de forma gratuita, incluso en entornos comerciales.

Fess utiliza OpenSearch para almacenar y buscar los documentos.
Al iniciarse, Fess 15.9 comprueba el servidor al que se conecta y cancela el arranque si no es OpenSearch 3 o posterior.
No puede conectarse a OpenSearch 2 o anterior, ni a Elasticsearch.
En la versión 15.9 se eliminó el motor de búsqueda que antes venía integrado en Fess, por lo que siempre hay que proporcionar OpenSearch por separado (en la configuración de Docker, se inicia un contenedor de OpenSearch junto con Fess).

Una sola instancia de Fess incluye todo lo siguiente:

- Rastreadores que recopilan documentos (web, servidores de archivos y diversos servicios mediante plugins)
- Una consola de administración para configurar el rastreo, los usuarios, los permisos, los diccionarios, las programaciones y mucho más
- Una página de búsqueda para los usuarios
- API (``/api/v2/``) para invocar la búsqueda y las sugerencias desde sistemas externos

La página de búsqueda se muestra mediante un tema estático que agrupa HTML, CSS y JavaScript.
Fess incluye el tema ``bootstrap``, y puede añadir otros temas como archivos ZIP en [Sistema] > [Tema].

Estructura de Fess
==================

Los componentes que intervienen en el funcionamiento de Fess son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Componente
     - Función
   * - Fess (aplicación web)
     - Proporciona la página de búsqueda, la consola de administración y las API. Aquí también se ejecuta el programador, que lanza trabajos como el rastreo a las horas configuradas
   * - Rastreador (proceso independiente)
     - Los trabajos de rastreo se lanzan como procesos Java independientes de Fess. Obtienen páginas web y archivos, extraen su texto y lo registran en OpenSearch. Los trabajos que crean las sugerencias, generan las miniaturas y crean los vectores para la búsqueda semántica también se ejecutan del mismo modo, en procesos independientes
   * - OpenSearch
     - Mantiene el índice de los documentos que se van a buscar y ejecuta las búsquedas. Gran parte de la información registrada en la consola de administración, como la configuración de rastreo, los usuarios, los registros de trabajos y los registros de búsqueda, también se guarda aquí

Como el rastreador es un proceso Java independiente, su memoria se configura por separado de la de Fess (se trata en :doc:`guide-14`).

El proceso hasta que los documentos se pueden buscar es el siguiente:

1. Registre una configuración de rastreo en la consola de administración (las URL o rutas de destino, los permisos que determinan quién puede ver los resultados, etc.)
2. El programador lanza el trabajo de rastreo. También puede lanzarlo manualmente desde la consola de administración con [Iniciar ahora]
3. El rastreador obtiene los documentos, extrae su texto y los registra en OpenSearch junto con sus permisos
4. Cuando un usuario busca, Fess filtra los resultados según los roles y grupos del usuario antes de devolverlos

Puede probar toda la secuencia, desde el arranque con Docker hasta el rastreo y la búsqueda, en :doc:`guide-02`.

Funciones básicas y plugins
===========================

En Fess 15.9, muchas funciones se ofrecen como plugins separados de Fess.
Que los plugins necesarios ya estén instalados o no depende del método de instalación.

- Fess instalado desde ZIP, RPM o DEB no incluye ningún plugin
- La imagen Docker estándar (por ejemplo, ``ghcr.io/codelibs/fess:15.9.0``) incluye preinstalados los siete plugins siguientes: ``fess-script-groovy``, ``fess-storage-s3``, ``fess-storage-gcs``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``, ``fess-sso-oidc``
- La imagen Docker slim (por ejemplo, ``15.9.0-slim``) no incluye ningún plugin

La tabla siguiente resume las funciones principales y los plugins que requieren.

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Función
     - Disponible solo con Fess
     - Requiere un plugin
   * - Rastreo
     - Web (http y https), sistemas de archivos, servidores de archivos (SMB), FTP
     - Amazon S3 (``fess-storage-s3``), Google Cloud Storage (``fess-storage-gcs``), rastreo web que ejecuta JavaScript en un navegador para obtener las páginas (``fess-crawler-playwright``)
   * - SaaS, bases de datos, etc.
     - La pantalla de configuración de almacenes de datos y el mecanismo que los ejecuta
     - Un plugin de almacén de datos (``fess-ds-*``) para cada origen que se quiera importar. Slack, Confluence y Jira, Google Drive, Microsoft 365, Box, bases de datos, CSV, Git, etc.
   * - Inicio de sesión y permisos
     - Usuarios, roles y grupos registrados en Fess, e integración con LDAP / Active Directory
     - SSO (``fess-sso-oidc`` para OpenID Connect, ``fess-sso-saml`` para SAML, ``fess-sso-entraid`` para Entra ID, ``fess-sso-spnego`` para SPNEGO)
   * - Scripts
     - JavaScript
     - Groovy (``fess-script-groovy``), OGNL (``fess-script-ognl``)
   * - Página de búsqueda
     - El tema incluido ``bootstrap``
     - En lugar de un plugin, se añade un archivo ZIP de tema
   * - API
     - ``/api/v2/`` (búsqueda, etiquetas, sugerencias, palabras populares, comprobación de estado, etc.) y la API de administración
     - ``/api/v1/`` (``fess-webapp-v1-api``), ``/json`` y ``/suggest`` (``fess-webapp-classic-api``). Fess Site Search utiliza ``/api/v1/``, por lo que requiere ``fess-webapp-v1-api``
   * - IA
     - Los mecanismos de la búsqueda semántica y del modo de búsqueda con IA (RAG). Si utiliza un modelo de embeddings desplegado en OpenSearch, la búsqueda semántica no requiere ningún plugin
     - Conexión con LLM y modelos de embeddings externos (``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``), servidor MCP (``fess-webapp-mcp``), búsqueda de imágenes (``fess-webapp-multimodal``)

De los elementos de la columna "Requiere un plugin", la imagen Docker estándar solo incluye S3 y GCS, los cuatro tipos de SSO y Groovy.
Todo lo demás requiere una instalación adicional, sea cual sea el método de instalación.

Las configuraciones cuyo tipo de script es Groovy, y las configuraciones heredadas de versiones anteriores que no tienen registrado el tipo de script, se ejecutan como Groovy.
Para usarlas se necesita ``fess-script-groovy``.
En las configuraciones de almacén de datos que se crean nuevas, el tipo de script predeterminado es JavaScript.

Instale los plugins de una de las formas siguientes.
Después de instalar o eliminar un plugin, reinicie Fess.
Haga coincidir la versión del plugin con la de Fess (15.9.x para Fess 15.9).

- En la consola de administración, abra [Sistema] > [Plugin], haga clic en [Instalar] y elija en la lista
- En la línea de comandos, ejecute ``bin/fess-setup install plugin <nombre-del-plugin>:<versión>``
- En Docker, defina la variable de entorno ``FESS_PLUGINS`` con una lista separada por espacios, como ``fess-ds-slack:15.9.0 fess-webapp-mcp:15.9.0``

El uso de los plugins de almacén de datos se explica en :doc:`datastore-basics`, y cómo escribir sus propios plugins en :doc:`guide-17`.

Formatos de archivo que se pueden buscar
========================================

El texto se extrae de los archivos mediante procesos de extracción como Apache Tika.
Se puede buscar en HTML, PDF, documentos de Microsoft Office, texto, el contenido de archivos comprimidos y más.
Para ver la lista de formatos comprobados, consulte `Archivos Objetivo de Búsqueda <https://fess.codelibs.org/es/supported-files.html>`__.

El texto de las imágenes y de los PDF escaneados no se puede buscar de forma predeterminada.
Se puede buscar si instala ``tesseract`` en el host donde se ejecuta el rastreador y activa el OCR.
Para conocer los pasos, consulte `Configuración de OCR <https://fess.codelibs.org/es/stable/config/crawler-ocr.html>`__.

Elegir el método de instalación
===============================

Fess se distribuye como imagen Docker y como paquetes ZIP, RPM y DEB.
Para probarlo, Docker es la opción más rápida, ya que inicia Fess y OpenSearch a la vez.
Los pasos se describen en :doc:`guide-02`.

En producción, también puede proporcionar OpenSearch como un servidor o clúster independiente.
Para conocer las versiones de Java y OpenSearch necesarias y las recomendaciones de CPU, memoria y disco, consulte `Requisitos del Sistema <https://fess.codelibs.org/es/stable/install/prerequisites.html>`__.

Itinerarios de lectura por objetivo
===================================

Los artículos están organizados para que pueda leerlos según su objetivo.
Elija la fila más cercana a su objetivo y lea los artículos de izquierda a derecha.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Objetivo
     - Artículos que leer
   * - Quiero probar Fess primero
     - :doc:`guide-02`
   * - Quiero buscar en servidores de archivos
     - :doc:`file-server-search` → :doc:`guide-04` → :doc:`guide-05`
   * - Quiero buscar datos de la nube y de servicios SaaS
     - :doc:`datastore-basics` → :doc:`guide-07` / :doc:`guide-06` / :doc:`guide-12`
   * - Quiero integrar la búsqueda en un sitio o sistema existente
     - :doc:`guide-03` → :doc:`guide-11`
   * - Quiero mostrar información distinta a cada departamento o usuario
     - :doc:`guide-05` → :doc:`guide-15` → :doc:`guide-13`
   * - Quiero mejorar la búsqueda con IA
     - :doc:`guide-18` → :doc:`guide-19` → :doc:`guide-20`
   * - Voy a empezar a operar en producción
     - :doc:`guide-10` → :doc:`guide-16` → :doc:`guide-14`

También están disponibles los artículos siguientes:

- Mejorar la calidad de la búsqueda: :doc:`guide-08`, :doc:`guide-09`, :doc:`guide-22`
- Buscar imágenes y texto a la vez: :doc:`guide-21`
- Escribir sus propios plugins: :doc:`guide-17`
- Planificar el despliegue en toda la empresa: :doc:`guide-23`
- Casos de uso y comparaciones con otros productos: :doc:`use-cases`, :doc:`comparison`

La lista de artículos también está disponible en la página :doc:`../guide`.

Referencias
===========

- `Documentación de Fess (versión estable) <https://fess.codelibs.org/es/stable/>`__
- `Requisitos del Sistema <https://fess.codelibs.org/es/stable/install/prerequisites.html>`__
- `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `Arquitectura de Plugins <https://fess.codelibs.org/es/stable/dev/plugin-architecture.html>`__
- `Tema <https://fess.codelibs.org/es/stable/admin/theme-guide.html>`__
- `Archivos Objetivo de Búsqueda <https://fess.codelibs.org/es/supported-files.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `codelibs/fess (GitHub) <https://github.com/codelibs/fess>`__
