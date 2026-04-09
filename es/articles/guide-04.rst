============================================================
Parte 4: Buscar archivos dispersos de forma centralizada -- Construir una busqueda transversal en un entorno multiorigen
============================================================

Introduccion
============

En la entrega anterior, presentamos como integrar la funcionalidad de busqueda de Fess en un sitio web existente.
Sin embargo, en un entorno empresarial real, la informacion no se encuentra solo en sitios web, sino que esta dispersa en servidores de archivos, almacenamiento en la nube y otros lugares.

En este articulo, integraremos multiples origenes de datos en Fess para construir un entorno en el que los usuarios puedan realizar busquedas transversales en todos los documentos desde una unica barra de busqueda.

Publico objetivo
================

- Personas cuya documentacion interna esta distribuida en multiples ubicaciones
- Personas insatisfechas con la busqueda en servidores de archivos o almacenamiento en la nube
- Es necesario tener Fess en funcionamiento siguiendo los pasos de la Parte 2

Escenario
=========

Supongamos una empresa de tamano mediano. En esta empresa, los documentos estan dispersos en los siguientes lugares:

- **Sitio web interno**: Portal interno, blog interno
- **Servidor de archivos**: Carpetas compartidas por departamento (SMB/CIFS)
- **Archivos locales**: Directorios especificos en el servidor

Cuando un empleado piensa "Donde estaba ese documento?", debe buscar en cada herramienta por separado.
Vamos a centralizar esto con Fess para poder realizar busquedas transversales desde una unica barra de busqueda.

Diseno de los origenes de datos
================================

Al construir una busqueda transversal, lo primero y mas importante es disenar "que y como se incluira en los objetivos de busqueda".

Organizacion de los objetivos de busqueda
------------------------------------------

Primero, organizamos los origenes de datos que seran objetivos de busqueda.

.. list-table:: Organizacion de origenes de datos
   :header-rows: 1
   :widths: 20 25 25 30

   * - Origen de datos
     - Tipo
     - Escala estimada
     - Frecuencia de actualizacion
   * - Portal interno
     - Rastreo web
     - Cientos de paginas
     - Semanal
   * - Blog tecnico
     - Rastreo web
     - Decenas a cientos de paginas
     - Irregular
   * - Carpeta compartida
     - Rastreo de archivos
     - Decenas de miles de archivos
     - Diaria
   * - Archivo historico
     - Rastreo de archivos
     - Miles de archivos
     - Mensual

Diseno de clasificacion mediante etiquetas
-------------------------------------------

Utilizando la funcion de "etiquetas" de Fess, se pueden categorizar los objetivos de busqueda.
Los usuarios pueden seleccionar una etiqueta al buscar para restringir la busqueda a una categoria especifica.

En este escenario, configuraremos las siguientes etiquetas:

- **Portal**: Informacion del portal interno y blog
- **Archivos compartidos**: Documentos del servidor de archivos
- **Archivo historico**: Materiales anteriores

Configuracion de etiquetas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. En la pantalla de administracion, seleccionar [Rastreador] > [Etiquetas]
2. Crear una etiqueta con [Crear nuevo]

Se configuran un "nombre" y un "valor" para cada etiqueta.
El valor se establece con caracteres alfanumericos y se utiliza para vincular con la configuracion del rastreo.

Construccion de la configuracion de rastreo
============================================

Configuracion del rastreo web
------------------------------

Esta es la configuracion de rastreo para el portal interno.

1. [Rastreador] > [Web] > [Crear nuevo]
2. Configurar lo siguiente:

   - URL: ``https://portal.example.com/``
   - URLs a incluir en el rastreo: ``https://portal.example.com/.*``
   - URLs a excluir del rastreo: ``https://portal.example.com/admin/.*``
   - Numero maximo de accesos: ``500``
   - Numero de hilos: ``3``
   - Intervalo: ``5000``
   - Etiqueta: Portal

3. Hacer clic en [Crear]

Al configurar las URLs de exclusion, se pueden excluir paginas como las de administracion que no se desean incluir en la busqueda.

Configuracion del rastreo de archivos
--------------------------------------

Esta es la configuracion de rastreo para la carpeta compartida.

1. [Rastreador] > [Sistema de archivos] > [Crear nuevo]
2. Configurar lo siguiente:

   - Ruta: ``smb://fileserver.example.com/shared/``
   - Rutas a incluir en el rastreo: ``smb://fileserver.example.com/shared/.*``
   - Rutas a excluir del rastreo: ``.*\\.tmp$``
   - Numero maximo de accesos: ``10000``
   - Numero de hilos: ``5``
   - Intervalo: ``1000``
   - Etiqueta: Archivos compartidos

3. Hacer clic en [Crear]

**Configuracion de la autenticacion SMB**

En el caso de servidores de archivos que requieren autenticacion, es necesario configurar la autenticacion de archivos.

1. [Rastreador] > [Autenticacion de archivos] > [Crear nuevo]
2. Configurar lo siguiente:

   - Nombre de host: ``fileserver.example.com``
   - Esquema: ``Samba``
   - Nombre de usuario: nombre de usuario de la cuenta de servicio
   - Contrasena: contrasena de la cuenta de servicio

3. Hacer clic en [Crear]

Rastreo de archivos locales
----------------------------

Para rastrear un directorio especifico en el servidor, se especifica la ruta del archivo directamente.

1. [Rastreador] > [Sistema de archivos] > [Crear nuevo]
2. Configurar lo siguiente:

   - Ruta: ``file:///data/archive/``
   - Rutas a incluir en el rastreo: ``file:///data/archive/.*``
   - Rutas a excluir del rastreo: ``.*\\.(log|bak)$``
   - Numero maximo de accesos: ``5000``
   - Etiqueta: Archivo historico

3. Hacer clic en [Crear]

Diseno de la programacion de rastreo
=====================================

Cuando se rastrean multiples origenes de datos, el diseno de la programacion es fundamental.
Si se ejecutan todos los rastreos simultaneamente, se genera una carga excesiva en los recursos del servidor y tambien en los servidores de destino.

Distribucion de la programacion
--------------------------------

Se distribuyen las programaciones de rastreo segun la frecuencia de actualizacion de cada origen de datos.

.. list-table:: Ejemplo de programacion de rastreo
   :header-rows: 1
   :widths: 25 25 50

   * - Origen de datos
     - Momento de ejecucion
     - Razon
   * - Portal interno
     - Todos los dias a las 2:00
     - Finaliza rapidamente porque tiene pocas paginas
   * - Carpeta compartida
     - Todos los dias a las 3:00
     - Se ejecuta de noche porque tiene muchos archivos
   * - Archivo historico
     - Todos los domingos a las 4:00
     - La frecuencia de actualizacion es baja, por lo que una vez por semana es suficiente

Configuracion del programador
-------------------------------

Desde [Sistema] > [Programador] en la pantalla de administracion, se puede configurar el momento de ejecucion de los trabajos de rastreo.
El trabajo predeterminado "Default Crawler" ejecuta todas las configuraciones de rastreo de forma conjunta.

Hacer los resultados de busqueda mas accesibles con el mapeo de rutas
======================================================================

Las URLs o rutas de archivos rastreados pueden resultar dificiles de entender para los usuarios.
Utilizando el mapeo de rutas, se pueden transformar las URLs que se muestran en los resultados de busqueda.

Ejemplo de configuracion
--------------------------

Transformar las rutas del servidor de archivos en URLs que los usuarios puedan abrir en el navegador.

1. [Rastreador] > [Mapeo de rutas] > [Crear nuevo]
2. Configurar lo siguiente:

   - Expresion regular: ``smb://fileserver.example.com/shared/(.*)``
   - Reemplazo: ``https://fileserver.example.com/shared/$1``

De esta forma, al hacer clic en un enlace de los resultados de busqueda, se podra acceder directamente al archivo desde el navegador.

Aprovechamiento de la busqueda transversal
============================================

Busqueda con filtrado por etiquetas
-------------------------------------

Una vez completado el rastreo, experimentemos la busqueda transversal en la pantalla de busqueda.

En la pantalla de busqueda se muestran pestanas o menus desplegables de etiquetas.
Si el usuario selecciona "Todos", se realiza una busqueda transversal; si selecciona una etiqueta especifica, la busqueda se limita a esa categoria.

Por ejemplo, al buscar "plan de proyecto", se obtienen resultados mixtos que incluyen articulos del portal, archivos Word de la carpeta compartida y PDFs del archivo historico.
Si se filtra por la etiqueta "Archivos compartidos", los resultados se limitan unicamente a los documentos del servidor de archivos.

Orden de los resultados de busqueda
-------------------------------------

De forma predeterminada, los resultados se ordenan por relevancia (puntuacion) con respecto a las palabras clave de busqueda.
Independientemente del tipo de origen de datos, los documentos con mayor relevancia aparecen en las primeras posiciones.

Resumen
========

En este articulo, integramos multiples origenes de datos en Fess y construimos un entorno de busqueda transversal.

- Configuracion de rastreo para tres tipos de origenes: sitios web, servidor de archivos y archivos locales
- Clasificacion por categorias y busqueda con filtrado mediante etiquetas
- Diseno de distribucion de la programacion de rastreo
- Transformacion de URLs mediante mapeo de rutas

Con la implementacion de la busqueda transversal, los usuarios podran encontrar la informacion que necesitan sin preocuparse por "donde esta almacenada".

En la proxima entrega, abordaremos el diseno de busqueda basada en roles, que controla los resultados de busqueda segun los permisos de cada departamento.

Referencias
============

- `Guia del administrador de Fess <https://fess.codelibs.org/ja/15.5/admin/index.html>`__

- `Configuracion de rastreo de archivos de Fess <https://fess.codelibs.org/ja/15.5/admin/filecrawl.html>`__
