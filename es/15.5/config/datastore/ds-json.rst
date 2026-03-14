==================================
Conector JSON
==================================

Descripcion general
===================

El conector JSON proporciona la funcionalidad para obtener datos de archivos JSON o APIs JSON
y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-json``.

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Se requiere acceso a archivos JSON o APIs
3. Es necesario comprender la estructura del JSON

Instalacion del plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Colocar
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Metodo 2: Instalar desde la pantalla de administracion

1. Abrir "Sistema" -> "Plugins"
2. Subir el archivo JAR
3. Reiniciar |Fess|

Configuracion
=============

Configure desde la pantalla de administracion en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuracion basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Ejemplo
   * - Nombre
     - Products JSON
   * - Handler
     - JsonDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
---------------------------

Archivo local:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

Archivo HTTP:

::

    files=https://api.example.com/products.json
    fileEncoding=UTF-8

API REST (con autenticacion):

::

    files=https://api.example.com/v1/items
    fileEncoding=UTF-8

Multiples archivos:

::

    files=/path/to/data1.json,https://api.example.com/data2.json
    fileEncoding=UTF-8

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``files``
     - Si
     - Ruta del archivo JSON o URL de API (multiples separados por comas)
   * - ``fileEncoding``
     - No
     - Codificacion de caracteres (predeterminado: UTF-8)
