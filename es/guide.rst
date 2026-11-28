=============
Guía Práctica
=============

Aprovechar el conocimiento con Fess
===================================

Esta guía práctica explica cómo hacer que la información de su organización se pueda buscar con Fess y convertirla en una plataforma de búsqueda que se siga utilizando.
Cada artículo se basa en Fess 15.9 y explica de forma concreta los campos de las pantallas de configuración, las claves de configuración y cómo comprobar que todo ha funcionado.
Las funciones que solo están disponibles a partir de la versión 15.10 se indican de forma explícita en los artículos.

Elegir según el objetivo
========================

- **Quiero probar Fess primero**: :doc:`articles/guide-01` → :doc:`articles/guide-02`
- **Quiero buscar en servidores de archivos**: :doc:`articles/file-server-search` → :doc:`articles/guide-04` → :doc:`articles/guide-05`
- **Quiero buscar datos de la nube y de servicios SaaS**: :doc:`articles/datastore-basics` → :doc:`articles/guide-07` / :doc:`articles/guide-06` / :doc:`articles/guide-12`
- **Quiero integrar la búsqueda en un sitio o sistema existente**: :doc:`articles/guide-03` → :doc:`articles/guide-11`
- **Quiero mostrar información distinta a cada departamento o usuario**: :doc:`articles/guide-05` → :doc:`articles/guide-15` → :doc:`articles/guide-13`
- **Quiero mejorar la búsqueda con IA**: :doc:`articles/guide-18` → :doc:`articles/guide-19` → :doc:`articles/guide-20`
- **Voy a empezar a operar en producción**: :doc:`articles/guide-10` → :doc:`articles/guide-16` → :doc:`articles/guide-14`

Primeros pasos
==============

- :doc:`articles/guide-01` - La estructura de Fess, el reparto de funciones entre Fess y los plugins, y los itinerarios de lectura por objetivo
- :doc:`articles/guide-02` - Iniciar Fess con Docker Compose y probar todo el proceso, desde el rastreo hasta la búsqueda

Recopilar información
=====================

- :doc:`articles/guide-04` - Rastrear sitios web y servidores de archivos, y permitir acotar los resultados con etiquetas
- :doc:`articles/datastore-basics` - Ajustes de los plugins de almacén de datos, permisos, etiquetas, programación y cómo comprobar los resultados
- :doc:`articles/guide-07` - Hacer que se puedan buscar los archivos de Google Drive, SharePoint Online / OneDrive y Box
- :doc:`articles/guide-06` - Hacer que se puedan buscar los repositorios Git, Confluence, Jira y Slack
- :doc:`articles/guide-12` - Hacer que se puedan buscar los datos de bases de datos, archivos CSV y Salesforce

Integrar la búsqueda y cambiar su aspecto
=========================================

- :doc:`articles/guide-03` - Colocar un cuadro de búsqueda en un sitio existente y ajustar el aspecto de la página de búsqueda con temas
- :doc:`articles/guide-11` - Buscar y registrar documentos desde aplicaciones de negocio con la API de búsqueda y tokens de acceso

Controlar el acceso
===================

- :doc:`articles/guide-05` - Mostrar resultados de búsqueda distintos según roles y grupos, e integrarse con LDAP / Active Directory
- :doc:`articles/guide-15` - Implantar SSO (OIDC / SAML / Entra ID / SPNEGO) y proteger el acceso desde el exterior
- :doc:`articles/guide-13` - Compartir una sola instancia de Fess entre varias organizaciones con hosts virtuales y roles

Mejorar la calidad de la búsqueda
=================================

- :doc:`articles/guide-08` - Detectar problemas en las pantallas de análisis de los registros de búsqueda y corregirlos con sinónimos y coincidencias de clave
- :doc:`articles/guide-09` - Entender cómo se indexan y buscan los documentos multilingües, y ajustar cada idioma
- :doc:`articles/guide-22` - Agregar y visualizar los registros de búsqueda a su manera con OpenSearch Dashboards

Operación
=========

- :doc:`articles/guide-10` - Comprobaciones de estado, registros, notificaciones, copia de seguridad y restauración, y tratamiento de las URL de fallo
- :doc:`articles/guide-16` - Gestionar la configuración como código con fessctl y la API de administración, y reproducir entornos
- :doc:`articles/guide-14` - Ajustes de memoria, clúster externo de OpenSearch y ejecución de Fess en varios servidores
- :doc:`articles/guide-17` - Añadir funciones escribiendo sus propios plugins de almacén de datos e ingesters

Mejorar la búsqueda con IA
==========================

- :doc:`articles/guide-18` - Usar la búsqueda vectorial y la fusión de rankings para encontrar documentos aunque estén redactados de otra forma
- :doc:`articles/guide-19` - Conectar un LLM y usar el modo de búsqueda con IA, que responde basándose en los documentos internos
- :doc:`articles/guide-20` - Permitir que agentes de IA busquen en Fess mediante el plugin de servidor MCP
- :doc:`articles/guide-21` - Crear una búsqueda multimodal que busque imágenes y texto a la vez

Planificar el despliegue en toda la empresa
===========================================

- :doc:`articles/guide-23` - Qué configurar y comprobar en cada etapa, desde la implantación hasta el despliegue en toda la empresa

Casos de uso y comparaciones
============================

- :doc:`articles/use-cases` - Casos de uso por sector y tamaño, y los artículos útiles para cada uno
- :doc:`articles/comparison` - Comparación de Fess con otras soluciones de búsqueda (OpenSearch por sí solo, Solr, productos comerciales, etc.)
- :doc:`articles/file-server-search` - Qué comprobar antes de implantar la búsqueda de texto completo en servidores de archivos

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-04
   articles/datastore-basics
   articles/guide-07
   articles/guide-06
   articles/guide-12
   articles/guide-03
   articles/guide-11
   articles/guide-05
   articles/guide-15
   articles/guide-13
   articles/guide-08
   articles/guide-09
   articles/guide-22
   articles/guide-10
   articles/guide-16
   articles/guide-14
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-23
   articles/use-cases
   articles/comparison
   articles/file-server-search
