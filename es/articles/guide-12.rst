========================================
Parte 12: Hacer los datos SaaS buscables
========================================

Introducción
=============

Los datos importantes de una empresa no solo se almacenan en servidores de archivos y almacenamiento en la nube, sino también en aplicaciones SaaS y bases de datos.
La información de clientes en Salesforce, los datos maestros de productos en bases de datos internas, los datos de listas gestionados en archivos CSV: estos datos normalmente solo son buscables dentro de sus respectivos sistemas.

Este artículo cubre escenarios para importar datos de SaaS y bases de datos al índice de Fess, permitiendo la búsqueda transversal junto con otros documentos.

Audiencia objetivo
===================

- Quienes desean incluir información de SaaS y bases de datos en los resultados de búsqueda
- Quienes desean aprender a utilizar los plugins de data store
- Quienes desean construir una plataforma de búsqueda que abarque múltiples fuentes de datos

Escenario
=========

Una organización de ventas tiene datos distribuidos en los siguientes sistemas.

.. list-table:: Situación de las fuentes de datos
   :header-rows: 1
   :widths: 20 35 45

   * - Sistema
     - Datos almacenados
     - Desafío actual
   * - Salesforce
     - Información de clientes, registros de negocios, historial de actividades
     - Solo se puede buscar dentro de Salesforce
   * - BD interna
     - Maestro de productos, listas de precios, información de inventario
     - Solo accesible a través de una interfaz de administración dedicada
   * - Archivos CSV
     - Listas de clientes, listas de asistentes a eventos
     - Solo se pueden encontrar abriéndolos en Excel y buscando visualmente
   * - Servidor de archivos
     - Propuestas, presupuestos, contratos
     - Ya rastreados por Fess

El objetivo es permitir la búsqueda transversal de todos estos datos con Fess, de modo que la información necesaria para las actividades de ventas pueda encontrarse desde un único campo de búsqueda.

Integración de datos de Salesforce
====================================

Para hacer los datos de Salesforce buscables en Fess, utilice el plugin de data store de Salesforce.

Instalación del plugin
-----------------------

1. Navegue a [Sistema] > [Plugins] en el panel de administración
2. Instale ``fess-ds-salesforce``

Configuración de la conexión
------------------------------

La integración con Salesforce requiere configurar una Connected App.

**Preparación en el lado de Salesforce**

1. Cree una Connected App en la configuración de Salesforce
2. Habilite la configuración de OAuth
3. Obtenga la clave y el secreto del consumidor

**Configuración en el lado de Fess**

1. Navegue a [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccione SalesforceDataStore
3. Configure los parámetros y scripts
4. Etiqueta: Establezca ``salesforce``

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**Ejemplo de configuración de script**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

Para ``auth_type``, especifique ``oauth_password`` (autenticación por nombre de usuario/contraseña) o ``oauth_token`` (autenticación por token JWT Bearer). Al usar autenticación JWT, establezca la clave privada RSA en ``private_key``.

Selección de datos objetivo
-----------------------------

Salesforce contiene muchos objetos, pero no todos necesitan ser buscables.
Concéntrese en los objetos que el equipo de ventas busca con frecuencia.

.. list-table:: Ejemplo de objetos objetivo
   :header-rows: 1
   :widths: 25 35 40

   * - Objeto
     - Campos buscables
     - Propósito
   * - Account
     - Nombre, industria, dirección, descripción
     - Buscar información básica de cuentas
   * - Opportunity
     - Nombre, etapa, descripción, monto
     - Buscar negocios activos
   * - Case
     - Asunto, descripción, estado
     - Buscar historial de consultas

Integración con bases de datos
===============================

Para hacer los datos de bases de datos internas buscables, utilice el plugin de data store de base de datos.

Instalación del plugin
-----------------------

Instale el plugin ``fess-ds-db``.
Este plugin puede conectarse a diversas bases de datos (MySQL, PostgreSQL, Oracle, SQL Server, etc.) a través de JDBC.

Configuración
--------------

1. Navegue a [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccione DatabaseDataStore
3. Configure los parámetros y scripts
4. Etiqueta: Establezca ``database``

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**Ejemplo de configuración de script**

.. code-block:: properties

    url=url
    title=product_name
    content=description

Los resultados de la consulta SQL especificada en ``sql`` son rastreados. En los scripts, utilice los nombres de columna SQL (o etiquetas de columna) para mapearlos a los campos del índice de Fess.

Diseño de consultas SQL
-------------------------

Puntos clave al diseñar la consulta SQL para el parámetro ``sql``:

- Incluya una columna ``url`` que sirva como destino del enlace en los resultados de búsqueda (p. ej., ``CONCAT('https://.../', id) AS url``)
- Incluya columnas que sirvan como texto buscable del cuerpo
- Utilice una cláusula ``WHERE`` para excluir datos innecesarios (p. ej., ``status = 'active'``)

En los scripts, utilice los nombres de columna SQL directamente para mapearlos a los campos del índice de Fess.

Integración de archivos CSV
=============================

Los datos de archivos CSV también pueden hacerse buscables.

Configuración
--------------

Utilice el plugin ``fess-ds-csv`` o la funcionalidad del data store CSV.

1. Navegue a [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccione CsvDataStore
3. Configure los parámetros y scripts
4. Etiqueta: Establezca ``csv-data``

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**Ejemplo de configuración de script** (use nombres de columna cuando haya una línea de encabezado)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

Cuando ``has_header_line=true``, los nombres de columna de la línea de encabezado pueden usarse en los scripts. Cuando no hay línea de encabezado, las columnas se referencian por número, como ``cell1``, ``cell2``, ``cell3``. Los scripts pueden contener expresiones Groovy, incluyendo concatenación de cadenas.

Si los archivos CSV se actualizan regularmente, fije la ubicación de los archivos y configure un programa de rastreo para que los datos más recientes se reflejen automáticamente en el índice.

Búsqueda transversal
======================

Una vez completadas todas las configuraciones de fuentes de datos, puede experimentar la búsqueda transversal.

Ejemplo de búsqueda
---------------------

Al buscar "ABC Corporation", se obtienen resultados como:

1. Información de cuenta de Salesforce (Account)
2. Propuestas del servidor de archivos (PDF)
3. Historial de compras de productos de la base de datos
4. Lista de asistentes a ferias comerciales de CSV

Los usuarios pueden encontrar la información que necesitan sin tener que saber dónde está almacenada.

Filtrado por etiqueta
----------------------

Cuando hay muchos resultados de búsqueda, utilice etiquetas para filtrarlos.

- ``salesforce``: Solo datos de Salesforce
- ``database``: Solo datos de la base de datos
- ``csv-data``: Solo datos CSV
- ``shared-files``: Solo documentos del servidor de archivos

Consideraciones operativas
===========================

Frescura de los datos
----------------------

Los datos de SaaS y bases de datos pueden actualizarse con frecuencia.
Configure la frecuencia de rastreo adecuadamente para mantener la frescura de los resultados de búsqueda.

.. list-table:: Frecuencia de rastreo recomendada
   :header-rows: 1
   :widths: 25 25 50

   * - Fuente de datos
     - Frecuencia recomendada
     - Razón
   * - Salesforce
     - Cada 4-6 horas
     - La información de negocios y clientes se actualiza durante el horario laboral
   * - Base de datos
     - Cada 2-4 horas
     - Datos con alta volatilidad, como información de inventario
   * - CSV
     - Diariamente
     - Normalmente se actualiza mediante procesamiento por lotes

Seguridad de la conexión a la base de datos
----------------------------------------------

Al conectarse directamente a una base de datos, preste especial atención a la seguridad.

- Utilice un usuario de base de datos de solo lectura
- Restrinja las conexiones a la dirección IP del servidor Fess
- No otorgue permisos de acceso a tablas innecesarias
- Tenga cuidado con la gestión de contraseñas

Resumen
========

Este artículo cubrió escenarios para hacer los datos de Salesforce, bases de datos y archivos CSV buscables con Fess.

- Integración de datos CRM mediante el plugin de data store de Salesforce
- Integración de BD interna mediante el plugin de data store de base de datos
- Integración de datos de listas mediante el data store CSV
- Mapeo de campos y diseño de consultas SQL
- Aprovechamiento de etiquetas en la búsqueda transversal

Al eliminar los silos de datos, se puede lograr un entorno donde todas las fuentes de información son buscables desde una única plataforma.
Con esto concluye la sección de Soluciones Prácticas. A partir de la próxima parte, cubriremos la sección de Arquitectura y Escalabilidad, comenzando con el diseño multitenant.

Referencias
============

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
