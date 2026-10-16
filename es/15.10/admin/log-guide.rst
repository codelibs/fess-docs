==================
Archivo de Registro
==================

Descripción general
===================

Aquí se explica la descarga de archivos de registro generados por |Fess|.

Método de configuración
========================

Método de visualización
-----------------------

Para abrir la página de archivos de registro que se muestra a continuación, haga clic en [Información del sistema > Archivo de registro] en el menú izquierdo.

|image0|

Descarga
--------

Puede descargar el archivo de registro haciendo clic en el nombre del archivo de registro que se muestra.

``server_*.log``
::::::::::::::::

Se registran los registros de |Fess| como servidor de aplicaciones.

fess.log
::::::::

Se registran los registros de |Fess| como aplicación.

fess-crawler.log
::::::::::::::::

Se registran los registros del rastreador.

audit.log
:::::::::

Se registran la información de inicio de sesión y los registros de acceso a la pantalla de administración.

fess-thumbnail.log
::::::::::::::::::

Se registran los registros de la función de miniaturas.

fess-suggest.log
::::::::::::::::

Se registran los registros de la función de sugerencias.

fess-urls.log
:::::::::::::

Se registra el tiempo que tardó un rastreo.

searchlog.log
:::::::::::::

Se registran los registros de búsqueda.
Si "Registro de búsqueda" de [Sistema > General] está habilitado, con la configuración predeterminada se añade una línea (JSON) por cada búsqueda.
Una línea contiene los campos de los documentos devueltos por esa búsqueda (``logging.search.docs.fields``), por lo que su tamaño crece con el número de resultados devueltos (con ``num=100``, una línea puede ocupar unos 70 KB).
Para la rotación y la retención de los registros, consulte :doc:`../config/admin-logging`.
Para no incluir los campos de los documentos devueltos en el registro de búsqueda, establezca ``logging.search.docs.enabled=false`` en ``fess_config.properties``; para dejar de escribir en este archivo, establezca ``logging.search.use.logfile=false``.

gc-crawler.log
::::::::::::::

Se registran los registros de GC del proceso de rastreo (los escribe el trabajo predeterminado "Default Crawler").

gc-fess.log
:::::::::::

Se registran los registros de GC de |Fess| en sí. Solo se escriben cuando la variable de entorno ``FESS_USE_GC_LOGGING`` tiene un valor no vacío (consulte :doc:`../install/run`).

.. |image0| image:: ../../../resources/images/en/15.10/admin/log-1.png
