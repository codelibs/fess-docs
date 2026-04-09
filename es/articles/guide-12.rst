============================================================
Parte 12: Hacer los datos SaaS buscables -- Escenarios de integracion con Salesforce y bases de datos
============================================================

Introduccion
=============

Los datos importantes de una empresa no solo se almacenan en servidores de archivos y almacenamiento en la nube, sino tambien en aplicaciones SaaS y bases de datos.
La informacion de clientes en Salesforce, los datos maestros de productos en bases de datos internas, los datos de listas gestionados en archivos CSV: estos datos normalmente solo son buscables dentro de sus respectivos sistemas.

Este articulo cubre escenarios para importar datos de SaaS y bases de datos al indice de Fess, permitiendo la busqueda transversal junto con otros documentos.

Audiencia objetivo
===================

- Quienes desean incluir informacion de SaaS y bases de datos en los resultados de busqueda
- Quienes desean aprender a utilizar los plugins de data store
- Quienes desean construir una plataforma de busqueda que abarque multiples fuentes de datos

Escenario
=========

Una organizacion de ventas tiene datos distribuidos en los siguientes sistemas.

.. list-table:: Situacion de las fuentes de datos
   :header-rows: 1
   :widths: 20 35 45

   * - Sistema
     - Datos almacenados
     - Desafio actual
   * - Salesforce
     - Informacion de clientes, registros de negocios, historial de actividades
     - Solo se puede buscar dentro de Salesforce
   * - BD interna
     - Maestro de productos, listas de precios, informacion de inventario
     - Solo accesible a traves de una interfaz de administracion dedicada
   * - Archivos CSV
     - Listas de clientes, listas de asistentes a eventos
     - Solo se pueden encontrar abriendolos en Excel y buscando visualmente
   * - Servidor de archivos
     - Propuestas, presupuestos, contratos
     - Ya rastreados por Fess

El objetivo es permitir la busqueda transversal de todos estos datos con Fess, de modo que la informacion necesaria para las actividades de ventas pueda encontrarse desde un unico campo de busqueda.

Integracion de datos de Salesforce
====================================

Para hacer los datos de Salesforce buscables en Fess, utilice el plugin de data store de Salesforce.

Instalacion del plugin
-----------------------

1. Navegue a [Sistema] > [Plugins] en el panel de administracion
2. Instale ``fess-ds-salesforce``

Configuracion de la conexion
------------------------------

La integracion con Salesforce requiere configurar una Connected App.

**Preparacion en el lado de Salesforce**

1. Cree una Connected App en la configuracion de Salesforce
2. Habilite la configuracion de OAuth
3. Obtenga la clave y el secreto del consumidor

**Configuracion en el lado de Fess**

1. Navegue a [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccione SalesforceDataStore
3. Configure los parametros y scripts
4. Etiqueta: Establezca ``salesforce``

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**Ejemplo de configuracion de script**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

Para ``auth_type``, especifique ``oauth_password`` (autenticacion por nombre de usuario/contrasena) o ``oauth_token`` (autenticacion por token JWT Bearer). Al usar autenticacion JWT, establezca la clave privada RSA en ``private_key``.

Seleccion de datos objetivo
-----------------------------

Salesforce contiene muchos objetos, pero no todos necesitan ser buscables.
Concentrese en los objetos que el equipo de ventas busca con frecuencia.

.. list-table:: Ejemplo de objetos objetivo
   :header-rows: 1
   :widths: 25 35 40

   * - Objeto
     - Campos buscables
     - Proposito
   * - Account
     - Nombre, industria, direccion, descripcion
     - Buscar informacion basica de cuentas
   * - Opportunity
     - Nombre, etapa, descripcion, monto
     - Buscar negocios activos
   * - Case
     - Asunto, descripcion, estado
     - Buscar historial de consultas

Integracion con bases de datos
===============================

Para hacer los datos de bases de datos internas buscables, utilice el plugin de data store de base de datos.

Instalacion del plugin
-----------------------

Instale el plugin ``fess-ds-db``.
Este plugin puede conectarse a diversas bases de datos (MySQL, PostgreSQL, Oracle, SQL Server, etc.) a traves de JDBC.

Configuracion
--------------

1. Navegue a [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccione DatabaseDataStore
3. Configure los parametros y scripts
4. Etiqueta: Establezca ``database``

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**Ejemplo de configuracion de script**

.. code-block:: properties

    url=url
    title=product_name
    content=description

Los resultados de la consulta SQL especificada en ``sql`` son rastreados. En los scripts, utilice los nombres de columna SQL (o etiquetas de columna) para mapearlos a los campos del indice de Fess.

Diseno de consultas SQL
-------------------------

Puntos clave al disenar la consulta SQL para el parametro ``sql``:

- Incluya una columna ``url`` que sirva como destino del enlace en los resultados de busqueda (p. ej., ``CONCAT('https://.../', id) AS url``)
- Incluya columnas que sirvan como texto buscable del cuerpo
- Utilice una clausula ``WHERE`` para excluir datos innecesarios (p. ej., ``status = 'active'``)

En los scripts, utilice los nombres de columna SQL directamente para mapearlos a los campos del indice de Fess.

Integracion de archivos CSV
=============================

Los datos de archivos CSV tambien pueden hacerse buscables.

Configuracion
--------------

Utilice el plugin ``fess-ds-csv`` o la funcionalidad del data store CSV.

1. Navegue a [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccione CsvDataStore
3. Configure los parametros y scripts
4. Etiqueta: Establezca ``csv-data``

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**Ejemplo de configuracion de script** (use nombres de columna cuando haya una linea de encabezado)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

Cuando ``has_header_line=true``, los nombres de columna de la linea de encabezado pueden usarse en los scripts. Cuando no hay linea de encabezado, las columnas se referencian por numero, como ``cell1``, ``cell2``, ``cell3``. Los scripts pueden contener expresiones Groovy, incluyendo concatenacion de cadenas.

Si los archivos CSV se actualizan regularmente, fije la ubicacion de los archivos y configure un programa de rastreo para que los datos mas recientes se reflejen automaticamente en el indice.

Busqueda transversal
======================

Una vez completadas todas las configuraciones de fuentes de datos, puede experimentar la busqueda transversal.

Ejemplo de busqueda
---------------------

Al buscar "ABC Corporation", se obtienen resultados como:

1. Informacion de cuenta de Salesforce (Account)
2. Propuestas del servidor de archivos (PDF)
3. Historial de compras de productos de la base de datos
4. Lista de asistentes a ferias comerciales de CSV

Los usuarios pueden encontrar la informacion que necesitan sin tener que saber donde esta almacenada.

Filtrado por etiqueta
----------------------

Cuando hay muchos resultados de busqueda, utilice etiquetas para filtrarlos.

- ``salesforce``: Solo datos de Salesforce
- ``database``: Solo datos de la base de datos
- ``csv-data``: Solo datos CSV
- ``shared-files``: Solo documentos del servidor de archivos

Consideraciones operativas
===========================

Frescura de los datos
----------------------

Los datos de SaaS y bases de datos pueden actualizarse con frecuencia.
Configure la frecuencia de rastreo adecuadamente para mantener la frescura de los resultados de busqueda.

.. list-table:: Frecuencia de rastreo recomendada
   :header-rows: 1
   :widths: 25 25 50

   * - Fuente de datos
     - Frecuencia recomendada
     - Razon
   * - Salesforce
     - Cada 4-6 horas
     - La informacion de negocios y clientes se actualiza durante el horario laboral
   * - Base de datos
     - Cada 2-4 horas
     - Datos con alta volatilidad, como informacion de inventario
   * - CSV
     - Diariamente
     - Normalmente se actualiza mediante procesamiento por lotes

Seguridad de la conexion a la base de datos
----------------------------------------------

Al conectarse directamente a una base de datos, preste especial atencion a la seguridad.

- Utilice un usuario de base de datos de solo lectura
- Restrinja las conexiones a la direccion IP del servidor Fess
- No otorgue permisos de acceso a tablas innecesarias
- Tenga cuidado con la gestion de contrasenas

Resumen
========

Este articulo cubrio escenarios para hacer los datos de Salesforce, bases de datos y archivos CSV buscables con Fess.

- Integracion de datos CRM mediante el plugin de data store de Salesforce
- Integracion de BD interna mediante el plugin de data store de base de datos
- Integracion de datos de listas mediante el data store CSV
- Mapeo de campos y diseno de consultas SQL
- Aprovechamiento de etiquetas en la busqueda transversal

Al eliminar los silos de datos, se puede lograr un entorno donde todas las fuentes de informacion son buscables desde una unica plataforma.
Con esto concluye la seccion de Soluciones Practicas. A partir de la proxima parte, cubriremos la seccion de Arquitectura y Escalabilidad, comenzando con el diseno multitenant.

Referencias
============

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
