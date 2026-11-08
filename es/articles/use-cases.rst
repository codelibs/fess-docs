=========================
Casos de uso de Fess
=========================

Introducción
============

Fess es utilizado por organizaciones de diversas industrias y escalas.
Esta página presenta casos de uso representativos y ejemplos prácticos de implementación de Fess.

.. note::

   Los siguientes ejemplos ilustran patrones de implementación comunes para Fess.
   Para estudios de casos reales, contacte al `Soporte Comercial <../support-services.html>`__.

----

Casos de uso por industria
===========================

Manufactura
-----------

**Desafío**: Los planos de diseño, documentos técnicos y documentos de gestión de calidad están dispersos en múltiples servidores de archivos, lo que hace que encontrar la información necesaria consuma mucho tiempo.

**Solución con Fess**:

- Búsqueda unificada de planos CAD, documentos técnicos en PDF y documentos de Office en servidores de archivos
- Búsqueda cruzada por números de modelo de producto, números de plano y nombres de proyecto
- Visualización de resultados de búsqueda basada en permisos de acceso (búsqueda basada en roles)

**Ejemplo de arquitectura**:

.. code-block:: text

    [Servidores de archivos]  →  [Fess]  →  [Portal interno]
         │                        │
         ├─ Planos                ├─ Cluster OpenSearch
         ├─ Docs tecnicos         └─ Integracion con Active Directory
         └─ Registros de calidad

**Funciones relacionadas**:

- `Rastreo de servidores de archivos <https://fess.codelibs.org/es/15.5/config/config-filecrawl.html>`__
- `Búsqueda basada en roles <https://fess.codelibs.org/es/15.5/config/config-role.html>`__
- `Visualización de miniaturas <https://fess.codelibs.org/es/15.5/admin/admin-general.html>`__

Servicios financieros y seguros
-------------------------------

**Desafío**: Los documentos de cumplimiento, contratos y regulaciones internas son extensos, lo que hace que las respuestas a auditorías y el manejo de consultas consuman mucho tiempo.

**Solución con Fess**:

- Búsqueda cruzada de regulaciones internas, manuales y preguntas frecuentes
- Búsqueda de texto en contratos y documentos de solicitud
- Búsqueda de conocimiento en el historial de consultas anteriores

**Funciones de seguridad**:

- Autenticación mediante integración con LDAP/Active Directory
- Inicio de sesión único mediante SAML
- Autenticación de API mediante tokens de acceso

**Funciones relacionadas**:

- `Autenticación LDAP <https://fess.codelibs.org/es/15.5/config/config-security.html>`__
- `Autenticación SAML <https://fess.codelibs.org/es/15.5/config/config-saml.html>`__

Educación
---------

**Desafío**: Los trabajos de investigación, materiales de clase y documentos del campus están distribuidos en servidores departamentales, dificultando el intercambio de información.

**Solución con Fess**:

- Búsqueda unificada desde el portal del campus
- Búsqueda en repositorios de trabajos de investigación
- Búsqueda de materiales de clase y programas de estudio

**Ejemplos de arquitectura**:

- Rastreo de sitios web del campus
- Integración con repositorios de artículos (DSpace, etc.)
- Búsqueda de materiales en Google Drive / SharePoint

**Funciones relacionadas**:

- `Rastreo web <https://fess.codelibs.org/es/15.5/config/config-webcrawl.html>`__
- `Rastreo de Google Drive <https://fess.codelibs.org/es/15.5/config/config-crawl-gsuite.html>`__

TI y Software
-------------

**Desafío**: El código fuente, la documentación, las wikis y la información del sistema de gestión de tickets están dispersos, lo que reduce la eficiencia del desarrollo.

**Solución con Fess**:

- Búsqueda de código en repositorios de GitHub/GitLab
- Búsqueda de páginas de Confluence/Wiki
- Búsqueda de mensajes de Slack/Teams

**Funciones para desarrolladores**:

- Integración con sistemas existentes mediante la API de búsqueda
- Resaltado de código
- Filtrado por tipo de archivo

**Funciones relacionadas**:

- `Rastreo de repositorios Git <https://fess.codelibs.org/es/15.5/config/config-crawl-git.html>`__
- `Rastreo de Confluence <https://fess.codelibs.org/es/15.5/config/config-crawl-atlassian.html>`__
- `Rastreo de Slack <https://fess.codelibs.org/es/15.5/config/config-crawl-slack.html>`__

----

Casos de uso por escala
========================

Pequeña empresa (hasta 100 empleados)
--------------------------------------

**Características**: Desean una implementación y operación sencillas con recursos de TI limitados.

**Configuración recomendada**:

- Implementación fácil mediante Docker Compose
- Configuración de servidor único (Fess + OpenSearch)
- Memoria requerida: 8 GB o más

**Pasos de implementación**:

.. code-block:: bash

    # Implementacion en 5 minutos
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Costo**:

- Software: Gratuito (Código abierto)
- Solo costos de servidor (Nube o local)

Mediana empresa (100-1000 empleados)
-------------------------------------

**Características**: Uso multidepartamental, requiere disponibilidad razonable.

**Configuración recomendada**:

- 2 servidores Fess (redundancia)
- Clúster OpenSearch de 3 nodos
- Balanceador de carga para distribución de tráfico
- Integración con Active Directory

**Directrices de capacidad**:

- Documentos: hasta 5 millones
- Usuarios de búsqueda simultáneos: hasta 100

**Funciones relacionadas**:

- `Configuración de clúster <https://fess.codelibs.org/es/15.5/install/clustering.html>`__
- `Copia de seguridad y restauración <https://fess.codelibs.org/es/15.5/admin/admin-backup.html>`__

Gran empresa (más de 1000 empleados)
-------------------------------------

**Características**: Datos a gran escala, alta disponibilidad, requisitos estrictos de seguridad.

**Configuración recomendada**:

- Múltiples servidores Fess (ejecutándose en Kubernetes)
- Clúster OpenSearch (configuración de nodos dedicados)
- Servidores de rastreo dedicados
- Integración con infraestructura de monitoreo y recopilación de registros

**Escalabilidad**:

- Documentos: cientos de millones posibles
- Escalado horizontal mediante división de shards de OpenSearch

**Funciones empresariales**:

- Gestión de etiquetas por departamento
- Registro detallado de accesos
- Integración con otros sistemas mediante API

.. note::

   Para implementaciones a gran escala, recomendamos utilizar el `Soporte Comercial <../support-services.html>`__.

----

Casos de uso técnicos
======================

Búsqueda en Wiki interno / Base de conocimiento
-------------------------------------------------

**Descripción**: Permitir la búsqueda cruzada en Confluence, MediaWiki y wikis internas.

**Beneficios**:

- Búsqueda unificada en múltiples sistemas wiki
- Rastreo automático basado en la frecuencia de actualización
- Los archivos adjuntos de las páginas wiki se incluyen en el alcance de la búsqueda

**Implementación**:

1. Instalar el plugin de almacén de datos de Confluence
2. Configurar los ajustes de conexión desde el panel de administración
3. Establecer el cronograma de rastreo (por ejemplo, diario)

Búsqueda unificada en servidores de archivos
---------------------------------------------

**Descripción**: Buscar documentos en servidores de archivos Windows y NAS.

**Protocolos soportados**:

- SMB/CIFS (carpetas compartidas de Windows)
- NFS
- Sistema de archivos local

**Seguridad**:

- Control de acceso basado en autenticación NTLM
- Las ACL de archivos se reflejan en los resultados de búsqueda

**Puntos de configuración**:

- Crear una cuenta dedicada para el rastreo
- Rastreo por fases para grandes volúmenes de archivos
- Considerar el ancho de banda de la red

Búsqueda en sitios web (Site Search)
-------------------------------------

**Descripción**: Agregar funcionalidad de búsqueda a sitios web públicos.

**Métodos de implementación**:

1. **Inserción de JavaScript**

   Use Fess Site Search (FSS) para agregar un cuadro de búsqueda con solo unas pocas líneas de JavaScript

2. **Integración por API**

   Construya una interfaz de búsqueda personalizada utilizando la API de búsqueda

**Ejemplo de FSS**:

.. code-block:: html

    <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      fess.src = 'https://your-fess-server/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      fess.setAttribute('fess-url', 'https://your-fess-server/json');
      document.body.appendChild(fess);
    })();
    </script>
    <fess:search></fess:search>

Búsqueda en bases de datos
---------------------------

**Descripción**: Hacer que los datos en bases de datos relacionales sean buscables.

**Bases de datos soportadas**:

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**Casos de uso**:

- Búsqueda en maestro de clientes
- Búsqueda en catálogo de productos
- Búsqueda en base de datos de preguntas frecuentes

**Implementación**:

1. Configurar el plugin de almacén de datos de base de datos
2. Especificar el objetivo de rastreo con una consulta SQL
3. Configurar el mapeo de campos

----

Resumen
=======

Fess, con su diseño flexible, puede adaptarse a diversas industrias, escalas y casos de uso.

**Para quienes están considerando la implementación**:

1. Primero, pruebe Fess con el `Inicio rápido <../quick-start.html>`__
2. Verifique las funciones requeridas en la `Documentación <../documentation.html>`__
3. Para implementación en producción, consulte el `Soporte Comercial <../support-services.html>`__

**Recursos relacionados**:

- `Lista de artículos <../articles.html>`__ - Artículos técnicos detallados
- `Foro de discusión <https://discuss.codelibs.org/c/fessen/>`__ - Soporte de la comunidad
- `GitHub <https://github.com/codelibs/fess>`__ - Código fuente y seguimiento de incidencias
