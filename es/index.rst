===================================
Servidor de Búsqueda de Texto Completo de Código Abierto Fess
===================================

Descripción General
====

Fess es "\ **un servidor de búsqueda de texto completo que se puede construir fácilmente en 5 minutos**\ ".

.. figure:: ../resources/images/ja/demo-1.png
   :scale: 100%
   :alt: Demo Estándar
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   Demo Estándar

.. figure:: ../resources/images/ja/demo-3.png
   :scale: 100%
   :alt: Demo de Búsqueda en el Sitio
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   Demo de Búsqueda en el Sitio

.. figure:: ../resources/images/ja/demo-2.png
   :scale: 100%
   :alt: Búsqueda de Código
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   Búsqueda de Código Fuente

.. figure:: ../resources/images/ja/demo-4.png
   :scale: 100%
   :alt: Búsqueda de Documentos
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   Búsqueda de Documentos

Se puede ejecutar en cualquier sistema operativo con un entorno de ejecución de Java o Docker.
Fess se proporciona bajo la licencia Apache y está disponible de forma gratuita.


Descargas
============

- :doc:`Fess 15.3.0 <downloads>` (paquetes zip/rpm/deb)

Características
====

-  Proporcionado bajo licencia Apache (software gratuito, disponible sin costo)

-  Rastreo de web, sistemas de archivos, carpetas compartidas de Windows y bases de datos

-  Compatible con muchos formatos de archivo como MS Office (Word/Excel/PowerPoint) y PDF

-  Independiente del sistema operativo (construido en Java)

-  Proporciona JavaScript para integración en sitios existentes

-  Utiliza OpenSearch o Elasticsearch como motor de búsqueda

-  Puede buscar sitios con autenticación BASIC/DIGEST/NTLM/FORM

-  Posibilidad de diferenciar resultados de búsqueda según el estado de inicio de sesión

-  Inicio de sesión único (SSO) mediante Active Directory, SAML, etc.

-  Búsqueda de información de ubicación integrada con información de mapas

-  Configuración de destinos de rastreo y edición de pantallas de búsqueda posibles desde el navegador

-  Clasificación de resultados de búsqueda mediante etiquetas

-  Adición de información a encabezados de solicitud, configuración de dominios duplicados, conversión de rutas de resultados de búsqueda

-  Integración con sistemas externos mediante salida de resultados de búsqueda en formato JSON

-  Agregación de registros de búsqueda y registros de clics

-  Compatible con facetas y drill-down

-  Función de autocompletado y sugerencias

-  Función de edición de diccionario de usuarios y diccionario de sinónimos

-  Función de visualización de caché y miniaturas de resultados de búsqueda

-  Función de proxy de resultados de búsqueda

-  Compatible con teléfonos inteligentes (Responsive Web Design)

-  Integración con sistemas externos mediante tokens de acceso

-  Compatible con extracción de texto externo como OCR

-  Diseño flexible que se puede adaptar según el caso de uso

Noticias
========

2025-10-25
    `Lanzamiento de Fess 15.3.0 <https://github.com/codelibs/fess/releases/tag/fess-15.3.0>`__

2025-09-04
    `Lanzamiento de Fess 15.2.0 <https://github.com/codelibs/fess/releases/tag/fess-15.2.0>`__

2025-07-20
    `Lanzamiento de Fess 15.1.0 <https://github.com/codelibs/fess/releases/tag/fess-15.1.0>`__

2025-06-22
    `Lanzamiento de Fess 15.0.0 <https://github.com/codelibs/fess/releases/tag/fess-15.0.0>`__

2025-05-24
    `Lanzamiento de Fess 14.19.2 <https://github.com/codelibs/fess/releases/tag/fess-14.19.2>`__

Para noticias anteriores, consulte :doc:`aquí <news>`.

Foro
==========

Si tiene alguna pregunta, utilice el `foro <https://discuss.codelibs.org/c/FessJA/>`__.

Soporte Comercial
============

Fess es un producto de código abierto proporcionado bajo la licencia Apache y puede usarse libremente sin costo tanto para uso personal como comercial.

Si necesita servicios de soporte para personalización, implementación o construcción de Fess, consulte el `soporte comercial (de pago) <https://www.n2sm.net/products/n2search.html>`__.
El soporte comercial también cubre el ajuste de rendimiento, como mejoras en la calidad de búsqueda y la velocidad de rastreo.

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (paquete comercial optimizado de Fess)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (servicio alternativo a Google Site Search)

- :doc:`Varios servicios de soporte <support-services>`


Fess Site Search
================

El proyecto CodeLibs proporciona `Fess Site Search (FSS) <https://fss-generator.codelibs.org/ja/>`__.
Puede integrar la página de búsqueda de Fess simplemente colocando JavaScript en su sitio existente.
Al usar FSS, también puede migrar fácilmente desde Google Site Search o Yahoo! Custom Search.
Si necesita un servidor Fess asequible, consulte `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__.

Complementos de Data Store
====================

- `Confluence/Jira <https://github.com/codelibs/fess-ds-atlassian>`__
- `Box <https://github.com/codelibs/fess-ds-box>`__
- `CSV <https://github.com/codelibs/fess-ds-csv>`__
- `Database <https://github.com/codelibs/fess-ds-db>`__
- `Dropbox <https://github.com/codelibs/fess-ds-dropbox>`__
- `Elasticsearch <https://github.com/codelibs/fess-ds-elasticsearch>`__
- `Git <https://github.com/codelibs/fess-ds-git>`__
- `Gitbucket <https://github.com/codelibs/fess-ds-gitbucket>`__
- `G Suite <https://github.com/codelibs/fess-ds-gsuite>`__
- `JSON <https://github.com/codelibs/fess-ds-json>`__
- `Office 365 <https://github.com/codelibs/fess-ds-office365>`__
- `S3 <https://github.com/codelibs/fess-ds-s3>`__
- `Salesforce <https://github.com/codelibs/fess-ds-salesforce>`__
- `SharePoint <https://github.com/codelibs/fess-ds-sharepoint>`__
- `Slack <https://github.com/codelibs/fess-ds-slack>`__

Complementos de Theme
===============

- `Simple <https://github.com/codelibs/fess-theme-simple>`__
- `Classic <https://github.com/codelibs/fess-theme-classic>`__

Complementos de Ingester
==================

- `Logger <https://github.com/codelibs/fess-ingest-logger>`__
- `NDJSON <https://github.com/codelibs/fess-ingest-ndjson>`__

Complementos de Script
==================

- `Groovy <https://github.com/codelibs/fess-script-groovy>`__
- `OGNL <https://github.com/codelibs/fess-script-ognl>`__

Proyectos Relacionados
================

- `Code Search <https://github.com/codelibs/docker-codesearch>`__
- `Document Search <https://github.com/codelibs/docker-docsearch>`__
- `Fione <https://github.com/codelibs/docker-fione>`__
- `Form Assist <https://github.com/codelibs/docker-formassist>`__

Medios Publicados
============

- `【Episodio 48】Inicio de sesión único mediante SAML <https://news.mynavi.jp/techplus/article/_ossfess-48/>`__

- `【Episodio 47】Gestión de almacenamiento y rastreo con MinIO <https://news.mynavi.jp/techplus/article/_ossfess-47/>`__

- `【Episodio 46】Rastreo de Amazon S3 <https://news.mynavi.jp/techplus/article/_ossfess-46/>`__

- `【Episodio 45】Método de inicio con Compose V2 <https://news.mynavi.jp/techplus/article/_ossfess-45/>`__

- `【Episodio 44】Uso de OpenSearch en Fess <https://news.mynavi.jp/techplus/article/_ossfess-44/>`__

- `【Episodio 43】Cómo utilizar Elasticsearch 8 <https://news.mynavi.jp/techplus/article/_ossfess-43/>`__

- `【Episodio 42】Cómo utilizar la API de búsqueda con tokens de acceso <https://news.mynavi.jp/techplus/article/_ossfess-42/>`__

- `【Episodio 41】Rastreo de Microsoft Teams <https://news.mynavi.jp/itsearch/article/bizapp/5880>`__

- `【Episodio 40】Métodos de configuración de diversas funciones (impulso de documentos, contenido relacionado, consultas relacionadas) <https://news.mynavi.jp/itsearch/article/bizapp/5804>`__

- `【Episodio 39】Métodos de configuración de diversas funciones (mapeo de rutas, encabezados de solicitud, hosts duplicados) <https://news.mynavi.jp/itsearch/article/bizapp/5686>`__

- `【Episodio 38】Métodos de configuración de diversas funciones (etiquetas, coincidencias clave) <https://news.mynavi.jp/itsearch/article/bizapp/5646>`__

- `【Episodio 37】Cómo utilizar AWS Elasticsearch Service <https://news.mynavi.jp/itsearch/article/devsoft/5557>`__

- `【Episodio 36】Cómo utilizar Elastic Cloud <https://news.mynavi.jp/itsearch/article/devsoft/5507>`__

- `【Episodio 35】Rastreo de SharePoint Server <https://news.mynavi.jp/itsearch/article/devsoft/5457>`__

- `【Episodio 34】Método de autenticación con OpenID Connect <https://news.mynavi.jp/itsearch/article/devsoft/5338>`__

- `【Episodio 33】Método de construcción de entorno de asistencia de entrada <https://news.mynavi.jp/itsearch/article/devsoft/5292>`__

- `【Episodio 32】Gestión de índices <https://news.mynavi.jp/itsearch/article/devsoft/5233>`__

- `【Episodio 31】Rastreo de Office 365 <https://news.mynavi.jp/itsearch/article/bizapp/5180>`__

- `【Episodio 30】Método de autenticación con Azure AD <https://news.mynavi.jp/itsearch/article/bizapp/5136>`__

- `【Episodio 29】Cómo usar con Docker <https://news.mynavi.jp/itsearch/article/devsoft/5058>`__

- `【Episodio 28】Método de referencia de archivos de registro <https://news.mynavi.jp/itsearch/article/devsoft/5032>`__

- `【Episodio 27】Agrupación de Fess <https://news.mynavi.jp/itsearch/article/devsoft/4994>`__

- `【Episodio 26】Búsqueda de información de ubicación <https://news.mynavi.jp/itsearch/article/devsoft/4963>`__

- `【Episodio 25】Uso de Tesseract OCR <https://news.mynavi.jp/itsearch/article/devsoft/4928>`__

- `【Episodio 24】Rastreo de GitBucket <https://news.mynavi.jp/itsearch/article/devsoft/4924>`__

- `【Episodio 23】Cómo usar la función de sugerencias <https://news.mynavi.jp/itsearch/article/bizapp/4890>`__

- `【Episodio 22】Rastreo de Dropbox <https://news.mynavi.jp/itsearch/article/bizapp/4844>`__

- `【Episodio 21】Rastreo de mensajes de Slack <https://news.mynavi.jp/itsearch/article/bizapp/4808>`__

- `【Episodio 20】Visualización de registros de búsqueda <https://news.mynavi.jp/itsearch/article/devsoft/4781>`__

- `【Episodio 19】Rastreo de archivos CSV <https://news.mynavi.jp/itsearch/article/devsoft/4761>`__

- `【Episodio 18】Rastreo de Google Drive <https://news.mynavi.jp/itsearch/article/devsoft/4732>`__

- `【Episodio 17】Rastreo de bases de datos <https://news.mynavi.jp/itsearch/article/devsoft/4659>`__

- `【Episodio 16】Cómo utilizar la API de búsqueda <https://news.mynavi.jp/itsearch/article/devsoft/4613>`__

- `【Episodio 15】Rastreo de servidores de archivos que requieren autenticación <https://news.mynavi.jp/itsearch/article/devsoft/4569>`__

- `【Episodio 14】Cómo usar la API de administración <https://news.mynavi.jp/itsearch/article/devsoft/4514>`__

- `【Episodio 13】Método para mostrar imágenes en miniatura en los resultados de búsqueda <https://news.mynavi.jp/itsearch/article/devsoft/4456>`__

- `【Episodio 12】Cómo usar la función de host virtual <https://news.mynavi.jp/itsearch/article/devsoft/4394>`__

- `【Episodio 11】Inicio de sesión único con Fess <https://news.mynavi.jp/itsearch/article/devsoft/4357>`__

- `【Episodio 10】Método de construcción en entorno Windows <https://news.mynavi.jp/itsearch/article/bizapp/4320>`__

- `【Episodio 9】Integración de Fess con Active Directory <https://news.mynavi.jp/itsearch/article/bizapp/4283>`__

- `【Episodio 8】Búsqueda basada en roles <https://news.mynavi.jp/itsearch/article/hardware/4201>`__

- `【Episodio 7】Rastreo de sitios con autenticación <https://news.mynavi.jp/itsearch/article/hardware/4158>`__

- `【Episodio 6】Analizador para búsqueda de texto completo en japonés <https://news.mynavi.jp/itsearch/article/devsoft/3671>`__

- `【Episodio 5】Procesamiento de tokenización para búsqueda de texto completo <https://news.mynavi.jp/itsearch/article/devsoft/3539>`__

- `【Episodio 4】Procesamiento de lenguaje natural con Fess <https://news.mynavi.jp/itsearch/article/bizapp/3445>`__

- `【Episodio 3】Web scraping que se puede hacer solo con configuración <https://news.mynavi.jp/itsearch/article/bizapp/3341>`__

- `【Episodio 2】Migración sencilla desde Google Site Search <https://news.mynavi.jp/itsearch/article/bizapp/3260>`__

- `【Episodio 1】Introducción al servidor de búsqueda de texto completo Fess <https://news.mynavi.jp/itsearch/article/bizapp/3154>`__

.. |image0| image:: ../resources/images/ja/demo-1.png
.. |image1| image:: ../resources/images/ja/demo-2.png
.. |image2| image:: ../resources/images/ja/demo-3.png
.. |image3| image:: ../resources/images/ja/n2search_225x50.png
   :target: https://www.n2sm.net/products/n2search.html
.. |image4| image:: ../resources/images/ja/n2search_b.png


.. toctree::
   :hidden:

   overview
   basic
   documentation
   tutorial
   development
   others
   archives


