===============
Mantenimiento
===============

Descripción general
===================

La página de mantenimiento se utiliza al ejecutar operaciones de datos del sistema.

|image0|

Método de operación
===================

Reindexación
------------

Puede recrear un nuevo índice a partir del índice fess existente.
Se ejecuta cuando desea cambiar el mapeo del índice, etc.


Parámetros de configuración
----------------------------

Actualizar alias
::::::::::::::::

Al habilitarlo, después de que se complete la reindexación, puede reasignar los alias fess.search y fess.update asignados al índice existente al nuevo índice.


Inicializar diccionarios
:::::::::::::::::::::::::

Al habilitarlo, puede inicializar la configuración de los diccionarios.


Número de fragmentos
:::::::::::::::::::::

Puede especificar el número de fragmentos de OpenSearch (index.number_of_shards).


Número máximo de réplicas
::::::::::::::::::::::::::

Puede especificar el número máximo de réplicas de OpenSearch (index.auto_expand_replicas).


Reconstruir índice de configuración
-------------------------------------

Puede reconstruir los índices de configuración (fess_config, fess_user, fess_log) con los mapeos más recientes.
Esta operación se ejecuta en segundo plano. Realice una copia de seguridad de la configuración antes de ejecutar.

Índices de destino
::::::::::::::::::

Seleccione los índices a reconstruir. Puede elegir entre fess_config, fess_user y fess_log.

Cargar datos predeterminados
::::::::::::::::::::::::::::

Al habilitarlo, se cargarán los datos predeterminados durante la reconstrucción. Los documentos existentes no se sobrescribirán.

Recargar índice de documentos
------------------------------

Puede recargar el índice de documentos para reflejar la configuración del índice.


Índice de Rastreador
--------------------

Puede eliminar el índice fess_crawler (información de rastreo).
No lo ejecute mientras el rastreador esté en ejecución.


Diagnóstico
-----------

Puede descargar archivos de registro en formato zip.

.. |image0| image:: ../../../resources/images/en/15.7/admin/maintenance-1.png
