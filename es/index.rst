===================================
Servidor de Búsqueda de Texto Completo de Código Abierto Fess
===================================

Descripción General
====

Fess es "\ **un servidor de búsqueda de texto completo que se puede construir fácilmente en 5 minutos**\ ".

.. figure:: ../resources/images/en/demo-1.png
   :scale: 100%
   :alt: Demo Estándar
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   Demo Estándar

.. figure:: ../resources/images/en/demo-3.png
   :scale: 100%
   :alt: Demo de Búsqueda en el Sitio
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   Demo de Búsqueda en el Sitio

.. figure:: ../resources/images/en/demo-2.png
   :scale: 100%
   :alt: Búsqueda de Código
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   Búsqueda de Código Fuente

.. figure:: ../resources/images/en/demo-4.png
   :scale: 100%
   :alt: Búsqueda de Documentos
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   Búsqueda de Documentos

Se puede ejecutar en cualquier sistema operativo con un entorno de ejecución de Java o Docker.
Fess se proporciona bajo la licencia Apache y está disponible de forma gratuita.


Descargas
============

- :doc:`Fess 15.5.0 <downloads>` (paquetes zip/rpm/deb)

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

2026-02-14
    `Lanzamiento de Fess 15.5.0 <https://github.com/codelibs/fess/releases/tag/fess-15.5.0>`__

2025-12-25
    `Lanzamiento de Fess 15.4.0 <https://github.com/codelibs/fess/releases/tag/fess-15.4.0>`__

2025-10-25
    `Lanzamiento de Fess 15.3.0 <https://github.com/codelibs/fess/releases/tag/fess-15.3.0>`__

2025-09-04
    `Lanzamiento de Fess 15.2.0 <https://github.com/codelibs/fess/releases/tag/fess-15.2.0>`__

2025-07-20
    `Lanzamiento de Fess 15.1.0 <https://github.com/codelibs/fess/releases/tag/fess-15.1.0>`__

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


.. |image0| image:: ../resources/images/en/demo-1.png
.. |image1| image:: ../resources/images/en/demo-2.png
.. |image2| image:: ../resources/images/en/demo-3.png
.. |image3| image:: ../resources/images/en/n2search_225x50.png
   :target: https://www.n2sm.net/products/n2search.html
.. |image4| image:: ../resources/images/en/n2search_b.png


.. toctree::
   :hidden:

   overview
   basic
   documentation
   tutorial
   development
   others
   archives


