================
Mapeo de Rutas
================

Descripción general
===================

Aquí se explica la configuración relacionada con el mapeo de rutas.
El mapeo de rutas es una función que utiliza expresiones regulares para transformar las URLs de los documentos rastreados por |Fess|.
Por ejemplo, se puede utilizar cuando desea rastrear documentos de un servidor de archivos (rutas que comienzan con ``file://``) y hacerlos accesibles a través de un servidor web (``http://``) desde los resultados de búsqueda.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de mapeo de rutas que se muestra a continuación, haga clic en [Rastreador > Mapeo de rutas] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de mapeo de rutas, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Expresión regular
:::::::::::::::::

Especifique la cadena que desea reemplazar.
El método de descripción sigue las expresiones regulares de Java.

Reemplazo
:::::::::

Especifique la cadena que reemplazará la expresión regular coincidente.

Tipo de procesamiento
:::::::::::::::::::::

Especifique el momento del reemplazo. Seleccione el tipo apropiado según su propósito.

Rastreo
  Reemplaza la URL después de obtener el documento durante el rastreo, antes de indexar.
  La URL convertida se guarda en el índice.
  Utilice esto cuando desee convertir rutas del servidor de archivos a URLs del servidor web y guardarlas en el índice.

Visualización
  Reemplaza la URL antes de mostrar los resultados de búsqueda y al hacer clic en los enlaces de resultados de búsqueda.
  Las URLs almacenadas en el índice no se modifican.
  Utilice esto cuando desee mantener la URL original en el índice pero convertirla a una URL diferente solo al mostrar los resultados de búsqueda.

Rastreo/Visualización
  Reemplaza la URL tanto en rastreo como en visualización.
  Utilice esto cuando desee aplicar la misma conversión en ambos momentos.

Conversión de URL extraída
  Reemplaza las URLs de enlaces al extraer enlaces de documentos HTML.
  Solo es efectivo con el rastreador web (no es efectivo con el rastreador de archivos).
  Las URLs guardadas en el índice no se modifican.
  Utilice esto cuando desee convertir URLs de enlaces extraídas de HTML y agregarlas a la cola de rastreo.

Orden de visualización
:::::::::::::::::::::::

Puede especificar el orden de procesamiento del mapeo de rutas.
Se procesa en orden ascendente.

Agente de usuario
:::::::::::::::::

Especifique esto cuando desee aplicar el mapeo de rutas solo a agentes de usuario específicos.
La coincidencia se realiza mediante expresiones regulares.
Si no se establece, se aplica a todas las solicitudes.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.

Ejemplos
========

Acceder al servidor de archivos a través del servidor web
---------------------------------------------------------

Este es un ejemplo de configuración para rastrear documentos de un servidor de archivos y hacerlos accesibles a través de un servidor web desde los resultados de búsqueda.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Elemento de configuración
     - Valor
   * - Expresión regular
     - ``file:/srv/documents/``
   * - Reemplazo
     - ``http://fileserver.example.com/documents/``
   * - Tipo de procesamiento
     - Rastreo

Con esta configuración, las URLs se guardan en el índice como ``http://fileserver.example.com/documents/...``.

Convertir URL solo en la visualización
--------------------------------------

Este es un ejemplo de configuración para mantener la ruta de archivo original en el índice y convertir a una URL del servidor web solo al mostrar los resultados de búsqueda.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Elemento de configuración
     - Valor
   * - Expresión regular
     - ``file:/srv/documents/``
   * - Reemplazo
     - ``http://fileserver.example.com/documents/``
   * - Tipo de procesamiento
     - Visualización

Con esta configuración, las URLs se guardan en el índice como ``file:/srv/documents/...`` y se convierten a ``http://...`` al hacer clic en los resultados de búsqueda.

Conversión de enlaces durante la migración del servidor
-------------------------------------------------------

Este es un ejemplo de configuración para convertir enlaces en HTML de un servidor antiguo a un servidor nuevo al rastrear un sitio web.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Elemento de configuración
     - Valor
   * - Expresión regular
     - ``http://old-server\\.example\\.com/``
   * - Reemplazo
     - ``http://new-server.example.com/``
   * - Tipo de procesamiento
     - Conversión de URL extraída

Con esta configuración, los enlaces extraídos de HTML se convierten y se agregan a la cola de rastreo.

Notas
=====

Sobre la conversión de URL extraída
-----------------------------------

La conversión de URL extraída solo es efectiva con el rastreador web.
No se aplica al rastrear sistemas de archivos.
Además, las URLs guardadas en el índice no se modifican; solo se convierten las URLs que se agregan a la cola de rastreo.

Sobre las expresiones regulares
-------------------------------

Las expresiones regulares se escriben en formato de expresiones regulares de Java.

* Se pueden usar referencias hacia atrás (``$1``, ``$2``, etc.)
* Los caracteres especiales deben escaparse (por ejemplo, ``.`` → ``\\.``)

Sobre el orden de clasificación
-------------------------------

Los mapeos de rutas se aplican secuencialmente en el orden de clasificación configurado (ascendente).
Cuando coinciden múltiples mapeos de rutas, se aplican comenzando desde la primera coincidencia.

.. |image0| image:: ../../../resources/images/en/15.4/admin/pathmap-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/pathmap-2.png
