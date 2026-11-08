========================================================
Parte 4: Buscar archivos dispersos de forma centralizada
========================================================

Introducción
============

En la entrega anterior, presentamos cómo integrar la funcionalidad de búsqueda de Fess en un sitio web existente.
Sin embargo, en un entorno empresarial real, la información no se encuentra solo en sitios web, sino que está dispersa en servidores de archivos, almacenamiento en la nube y otros lugares.

En este artículo, integraremos múltiples orígenes de datos en Fess para construir un entorno en el que los usuarios puedan realizar búsquedas transversales en todos los documentos desde una única barra de búsqueda.

Público objetivo
================

- Personas cuya documentación interna está distribuida en múltiples ubicaciones
- Personas insatisfechas con la búsqueda en servidores de archivos o almacenamiento en la nube
- Es necesario tener Fess en funcionamiento siguiendo los pasos de la Parte 2

Escenario
=========

Supongamos una empresa de tamaño mediano. En esta empresa, los documentos están dispersos en los siguientes lugares:

- **Sitio web interno**: Portal interno, blog interno
- **Servidor de archivos**: Carpetas compartidas por departamento (SMB/CIFS)
- **Archivos locales**: Directorios específicos en el servidor

Cuando un empleado piensa "¿Dónde estaba ese documento?", debe buscar en cada herramienta por separado.
Vamos a centralizar esto con Fess para poder realizar búsquedas transversales desde una única barra de búsqueda.

Diseño de los orígenes de datos
================================

Al construir una búsqueda transversal, lo primero y más importante es diseñar "qué y cómo se incluirá en los objetivos de búsqueda".

Organización de los objetivos de búsqueda
------------------------------------------

Primero, organizamos los orígenes de datos que serán objetivos de búsqueda.

.. list-table:: Organización de orígenes de datos
   :header-rows: 1
   :widths: 20 25 25 30

   * - Origen de datos
     - Tipo
     - Escala estimada
     - Frecuencia de actualización
   * - Portal interno
     - Rastreo web
     - Cientos de páginas
     - Semanal
   * - Blog técnico
     - Rastreo web
     - Decenas a cientos de páginas
     - Irregular
   * - Carpeta compartida
     - Rastreo de archivos
     - Decenas de miles de archivos
     - Diaria
   * - Archivo histórico
     - Rastreo de archivos
     - Miles de archivos
     - Mensual

Diseño de clasificación mediante etiquetas
-------------------------------------------

Utilizando la función de "etiquetas" de Fess, se pueden categorizar los objetivos de búsqueda.
Los usuarios pueden seleccionar una etiqueta al buscar para restringir la búsqueda a una categoría específica.

En este escenario, configuraremos las siguientes etiquetas:

- **Portal**: Información del portal interno y blog
- **Archivos compartidos**: Documentos del servidor de archivos
- **Archivo histórico**: Materiales anteriores

Configuración de etiquetas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. En la pantalla de administración, seleccionar [Rastreador] > [Etiquetas]
2. Crear una etiqueta con [Crear nuevo]

Se configuran un "nombre" y un "valor" para cada etiqueta.
El valor se establece con caracteres alfanuméricos y se utiliza para vincular con la configuración del rastreo.

Construcción de la configuración de rastreo
============================================

Configuración del rastreo web
------------------------------

Esta es la configuración de rastreo para el portal interno.

1. [Rastreador] > [Web] > [Crear nuevo]
2. Configurar lo siguiente:

   - URL: ``https://portal.example.com/``
   - URLs a incluir en el rastreo: ``https://portal.example.com/.*``
   - URLs a excluir del rastreo: ``https://portal.example.com/admin/.*``
   - Número máximo de accesos: ``500``
   - Número de hilos: ``3``
   - Intervalo: ``5000``
   - Etiqueta: Portal

3. Hacer clic en [Crear]

Al configurar las URLs de exclusión, se pueden excluir páginas como las de administración que no se desean incluir en la búsqueda.

Configuración del rastreo de archivos
--------------------------------------

Esta es la configuración de rastreo para la carpeta compartida.

1. [Rastreador] > [Sistema de archivos] > [Crear nuevo]
2. Configurar lo siguiente:

   - Ruta: ``smb://fileserver.example.com/shared/``
   - Rutas a incluir en el rastreo: ``smb://fileserver.example.com/shared/.*``
   - Rutas a excluir del rastreo: ``.*\\.tmp$``
   - Número máximo de accesos: ``10000``
   - Número de hilos: ``5``
   - Intervalo: ``1000``
   - Etiqueta: Archivos compartidos

3. Hacer clic en [Crear]

**Configuración de la autenticación SMB**

En el caso de servidores de archivos que requieren autenticación, es necesario configurar la autenticación de archivos.

1. [Rastreador] > [Autenticación de archivos] > [Crear nuevo]
2. Configurar lo siguiente:

   - Nombre de host: ``fileserver.example.com``
   - Esquema: ``Samba``
   - Nombre de usuario: nombre de usuario de la cuenta de servicio
   - Contraseña: contraseña de la cuenta de servicio

3. Hacer clic en [Crear]

Rastreo de archivos locales
----------------------------

Para rastrear un directorio específico en el servidor, se especifica la ruta del archivo directamente.

1. [Rastreador] > [Sistema de archivos] > [Crear nuevo]
2. Configurar lo siguiente:

   - Ruta: ``file:///data/archive/``
   - Rutas a incluir en el rastreo: ``file:///data/archive/.*``
   - Rutas a excluir del rastreo: ``.*\\.(log|bak)$``
   - Número máximo de accesos: ``5000``
   - Etiqueta: Archivo histórico

3. Hacer clic en [Crear]

Diseño de la programación de rastreo
=====================================

Cuando se rastrean múltiples orígenes de datos, el diseño de la programación es fundamental.
Si se ejecutan todos los rastreos simultáneamente, se genera una carga excesiva en los recursos del servidor y también en los servidores de destino.

Distribución de la programación
--------------------------------

Se distribuyen las programaciones de rastreo según la frecuencia de actualización de cada origen de datos.

.. list-table:: Ejemplo de programación de rastreo
   :header-rows: 1
   :widths: 25 25 50

   * - Origen de datos
     - Momento de ejecución
     - Razón
   * - Portal interno
     - Todos los días a las 2:00
     - Finaliza rápidamente porque tiene pocas páginas
   * - Carpeta compartida
     - Todos los días a las 3:00
     - Se ejecuta de noche porque tiene muchos archivos
   * - Archivo histórico
     - Todos los domingos a las 4:00
     - La frecuencia de actualización es baja, por lo que una vez por semana es suficiente

Configuración del programador
-------------------------------

Desde [Sistema] > [Programador] en la pantalla de administración, se puede configurar el momento de ejecución de los trabajos de rastreo.
El trabajo predeterminado "Default Crawler" ejecuta todas las configuraciones de rastreo de forma conjunta.

Hacer los resultados de búsqueda más accesibles con el mapeo de rutas
======================================================================

Las URLs o rutas de archivos rastreados pueden resultar difíciles de entender para los usuarios.
Utilizando el mapeo de rutas, se pueden transformar las URLs que se muestran en los resultados de búsqueda.

Ejemplo de configuración
--------------------------

Transformar las rutas del servidor de archivos en URLs que los usuarios puedan abrir en el navegador.

1. [Rastreador] > [Mapeo de rutas] > [Crear nuevo]
2. Configurar lo siguiente:

   - Expresión regular: ``smb://fileserver.example.com/shared/(.*)``
   - Reemplazo: ``https://fileserver.example.com/shared/$1``

De esta forma, al hacer clic en un enlace de los resultados de búsqueda, se podrá acceder directamente al archivo desde el navegador.

Aprovechamiento de la búsqueda transversal
============================================

Búsqueda con filtrado por etiquetas
-------------------------------------

Una vez completado el rastreo, experimentemos la búsqueda transversal en la pantalla de búsqueda.

En la pantalla de búsqueda se muestran pestañas o menús desplegables de etiquetas.
Si el usuario selecciona "Todos", se realiza una búsqueda transversal; si selecciona una etiqueta específica, la búsqueda se limita a esa categoría.

Por ejemplo, al buscar "plan de proyecto", se obtienen resultados mixtos que incluyen artículos del portal, archivos Word de la carpeta compartida y PDFs del archivo histórico.
Si se filtra por la etiqueta "Archivos compartidos", los resultados se limitan únicamente a los documentos del servidor de archivos.

Orden de los resultados de búsqueda
-------------------------------------

De forma predeterminada, los resultados se ordenan por relevancia (puntuación) con respecto a las palabras clave de búsqueda.
Independientemente del tipo de origen de datos, los documentos con mayor relevancia aparecen en las primeras posiciones.

Resumen
========

En este artículo, integramos múltiples orígenes de datos en Fess y construimos un entorno de búsqueda transversal.

- Configuración de rastreo para tres tipos de orígenes: sitios web, servidor de archivos y archivos locales
- Clasificación por categorías y búsqueda con filtrado mediante etiquetas
- Diseño de distribución de la programación de rastreo
- Transformación de URLs mediante mapeo de rutas

Con la implementación de la búsqueda transversal, los usuarios podrán encontrar la información que necesitan sin preocuparse por "dónde está almacenada".

En la próxima entrega, abordaremos el diseño de búsqueda basada en roles, que controla los resultados de búsqueda según los permisos de cada departamento.

Referencias
============

- `Guía del administrador de Fess <https://fess.codelibs.org/ja/15.5/admin/index.html>`__

- `Configuración de rastreo de archivos de Fess <https://fess.codelibs.org/ja/15.5/admin/filecrawl.html>`__
