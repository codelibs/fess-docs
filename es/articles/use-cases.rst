=========================
Casos de uso de Fess
=========================

Introduccion
============

Fess es utilizado por organizaciones de diversas industrias y escalas.
Esta pagina presenta casos de uso representativos y ejemplos practicos de implementacion de Fess.

.. note::

   Los siguientes ejemplos ilustran patrones de implementacion comunes para Fess.
   Para estudios de casos reales, contacte al `Soporte Comercial <../support-services.html>`__.

----

Casos de uso por industria
===========================

Manufactura
-----------

**Desafio**: Los planos de diseno, documentos tecnicos y documentos de gestion de calidad estan dispersos en multiples servidores de archivos, lo que hace que encontrar la informacion necesaria consuma mucho tiempo.

**Solucion con Fess**:

- Busqueda unificada de planos CAD, documentos tecnicos en PDF y documentos de Office en servidores de archivos
- Busqueda cruzada por numeros de modelo de producto, numeros de plano y nombres de proyecto
- Visualizacion de resultados de busqueda basada en permisos de acceso (busqueda basada en roles)

**Ejemplo de arquitectura**:

.. code-block:: text

    [Servidores de archivos]  →  [Fess]  →  [Portal interno]
         │                        │
         ├─ Planos                ├─ Cluster OpenSearch
         ├─ Docs tecnicos         └─ Integracion con Active Directory
         └─ Registros de calidad

**Funciones relacionadas**:

- `Rastreo de servidores de archivos <https://fess.codelibs.org/es/15.5/config/config-filecrawl.html>`__
- `Busqueda basada en roles <https://fess.codelibs.org/es/15.5/config/config-role.html>`__
- `Visualizacion de miniaturas <https://fess.codelibs.org/es/15.5/admin/admin-general.html>`__

Servicios financieros y seguros
-------------------------------

**Desafio**: Los documentos de cumplimiento, contratos y regulaciones internas son extensos, lo que hace que las respuestas a auditorias y el manejo de consultas consuman mucho tiempo.

**Solucion con Fess**:

- Busqueda cruzada de regulaciones internas, manuales y preguntas frecuentes
- Busqueda de texto en contratos y documentos de solicitud
- Busqueda de conocimiento en el historial de consultas anteriores

**Funciones de seguridad**:

- Autenticacion mediante integracion con LDAP/Active Directory
- Inicio de sesion unico mediante SAML
- Autenticacion de API mediante tokens de acceso

**Funciones relacionadas**:

- `Autenticacion LDAP <https://fess.codelibs.org/es/15.5/config/config-security.html>`__
- `Autenticacion SAML <https://fess.codelibs.org/es/15.5/config/config-saml.html>`__

Educacion
---------

**Desafio**: Los trabajos de investigacion, materiales de clase y documentos del campus estan distribuidos en servidores departamentales, dificultando el intercambio de informacion.

**Solucion con Fess**:

- Busqueda unificada desde el portal del campus
- Busqueda en repositorios de trabajos de investigacion
- Busqueda de materiales de clase y programas de estudio

**Ejemplos de arquitectura**:

- Rastreo de sitios web del campus
- Integracion con repositorios de articulos (DSpace, etc.)
- Busqueda de materiales en Google Drive / SharePoint

**Funciones relacionadas**:

- `Rastreo web <https://fess.codelibs.org/es/15.5/config/config-webcrawl.html>`__
- `Rastreo de Google Drive <https://fess.codelibs.org/es/15.5/config/config-crawl-gsuite.html>`__

TI y Software
-------------

**Desafio**: El codigo fuente, la documentacion, las wikis y la informacion del sistema de gestion de tickets estan dispersos, lo que reduce la eficiencia del desarrollo.

**Solucion con Fess**:

- Busqueda de codigo en repositorios de GitHub/GitLab
- Busqueda de paginas de Confluence/Wiki
- Busqueda de mensajes de Slack/Teams

**Funciones para desarrolladores**:

- Integracion con sistemas existentes mediante la API de busqueda
- Resaltado de codigo
- Filtrado por tipo de archivo

**Funciones relacionadas**:

- `Rastreo de repositorios Git <https://fess.codelibs.org/es/15.5/config/config-crawl-git.html>`__
- `Rastreo de Confluence <https://fess.codelibs.org/es/15.5/config/config-crawl-atlassian.html>`__
- `Rastreo de Slack <https://fess.codelibs.org/es/15.5/config/config-crawl-slack.html>`__

----

Casos de uso por escala
========================

Pequena empresa (hasta 100 empleados)
--------------------------------------

**Caracteristicas**: Desean una implementacion y operacion sencillas con recursos de TI limitados.

**Configuracion recomendada**:

- Implementacion facil mediante Docker Compose
- Configuracion de servidor unico (Fess + OpenSearch)
- Memoria requerida: 8 GB o mas

**Pasos de implementacion**:

.. code-block:: bash

    # Implementacion en 5 minutos
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Costo**:

- Software: Gratuito (Codigo abierto)
- Solo costos de servidor (Nube o local)

Mediana empresa (100-1000 empleados)
-------------------------------------

**Caracteristicas**: Uso multidepartamental, requiere disponibilidad razonable.

**Configuracion recomendada**:

- 2 servidores Fess (redundancia)
- Cluster OpenSearch de 3 nodos
- Balanceador de carga para distribucion de trafico
- Integracion con Active Directory

**Directrices de capacidad**:

- Documentos: hasta 5 millones
- Usuarios de busqueda simultaneos: hasta 100

**Funciones relacionadas**:

- `Configuracion de cluster <https://fess.codelibs.org/es/15.5/install/clustering.html>`__
- `Copia de seguridad y restauracion <https://fess.codelibs.org/es/15.5/admin/admin-backup.html>`__

Gran empresa (mas de 1000 empleados)
-------------------------------------

**Caracteristicas**: Datos a gran escala, alta disponibilidad, requisitos estrictos de seguridad.

**Configuracion recomendada**:

- Multiples servidores Fess (ejecutandose en Kubernetes)
- Cluster OpenSearch (configuracion de nodos dedicados)
- Servidores de rastreo dedicados
- Integracion con infraestructura de monitoreo y recopilacion de registros

**Escalabilidad**:

- Documentos: cientos de millones posibles
- Escalado horizontal mediante division de shards de OpenSearch

**Funciones empresariales**:

- Gestion de etiquetas por departamento
- Registro detallado de accesos
- Integracion con otros sistemas mediante API

.. note::

   Para implementaciones a gran escala, recomendamos utilizar el `Soporte Comercial <../support-services.html>`__.

----

Casos de uso tecnicos
======================

Busqueda en Wiki interno / Base de conocimiento
-------------------------------------------------

**Descripcion**: Permitir la busqueda cruzada en Confluence, MediaWiki y wikis internas.

**Beneficios**:

- Busqueda unificada en multiples sistemas wiki
- Rastreo automatico basado en la frecuencia de actualizacion
- Los archivos adjuntos de las paginas wiki se incluyen en el alcance de la busqueda

**Implementacion**:

1. Instalar el plugin de almacen de datos de Confluence
2. Configurar los ajustes de conexion desde el panel de administracion
3. Establecer el cronograma de rastreo (por ejemplo, diario)

Busqueda unificada en servidores de archivos
---------------------------------------------

**Descripcion**: Buscar documentos en servidores de archivos Windows y NAS.

**Protocolos soportados**:

- SMB/CIFS (carpetas compartidas de Windows)
- NFS
- Sistema de archivos local

**Seguridad**:

- Control de acceso basado en autenticacion NTLM
- Las ACL de archivos se reflejan en los resultados de busqueda

**Puntos de configuracion**:

- Crear una cuenta dedicada para el rastreo
- Rastreo por fases para grandes volumenes de archivos
- Considerar el ancho de banda de la red

Busqueda en sitios web (Site Search)
-------------------------------------

**Descripcion**: Agregar funcionalidad de busqueda a sitios web publicos.

**Metodos de implementacion**:

1. **Insercion de JavaScript**

   Use Fess Site Search (FSS) para agregar un cuadro de busqueda con solo unas pocas lineas de JavaScript

2. **Integracion por API**

   Construya una interfaz de busqueda personalizada utilizando la API de busqueda

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

Busqueda en bases de datos
---------------------------

**Descripcion**: Hacer que los datos en bases de datos relacionales sean buscables.

**Bases de datos soportadas**:

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**Casos de uso**:

- Busqueda en maestro de clientes
- Busqueda en catalogo de productos
- Busqueda en base de datos de preguntas frecuentes

**Implementacion**:

1. Configurar el plugin de almacen de datos de base de datos
2. Especificar el objetivo de rastreo con una consulta SQL
3. Configurar el mapeo de campos

----

Resumen
=======

Fess, con su diseno flexible, puede adaptarse a diversas industrias, escalas y casos de uso.

**Para quienes estan considerando la implementacion**:

1. Primero, pruebe Fess con el `Inicio rapido <../quick-start.html>`__
2. Verifique las funciones requeridas en la `Documentacion <../documentation.html>`__
3. Para implementacion en produccion, consulte el `Soporte Comercial <../support-services.html>`__

**Recursos relacionados**:

- `Lista de articulos <../articles.html>`__ - Articulos tecnicos detallados
- `Foro de discusion <https://discuss.codelibs.org/c/fessen/>`__ - Soporte de la comunidad
- `GitHub <https://github.com/codelibs/fess>`__ - Codigo fuente y seguimiento de incidencias
