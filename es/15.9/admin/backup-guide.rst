==================
Copia de Seguridad
==================

Descripción general
===================

La página de copia de seguridad le permite descargar y cargar la información de configuración de |Fess|.

Descarga
--------

|Fess| mantiene la información de configuración como índice.
Para descargar, haga clic en el nombre del índice.

|image0|

fess_config.bulk
::::::::::::::::

fess_config.bulk contiene la información de configuración de |Fess|.

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk contiene la información de configuración de |Fess| excluyendo las URL con falla.

fess_user.bulk
::::::::::::::

fess_user.bulk contiene información de usuarios, roles y grupos.

system.properties
:::::::::::::::::

system.properties contiene información de configuración general.

fess.json
:::::::::

fess.json contiene información de configuración del índice fess.

doc.json
::::::::

doc.json contiene información de mapeo del índice fess.

chat_log.ndjson
:::::::::::::::

chat_log.ndjson contiene información de los registros de uso del chat con IA.

click_log.ndjson
::::::::::::::::

click_log.ndjson contiene información de registros de clics.

favorite_log.ndjson
:::::::::::::::::::

favorite_log.ndjson contiene información de registros de favoritos.

search_log.ndjson
:::::::::::::::::

search_log.ndjson contiene información de registros de búsqueda.

user_info.ndjson
::::::::::::::::

user_info.ndjson contiene información de usuarios de búsqueda.

Carga
-----

Puede cargar e importar información de configuración.
Los archivos que se pueden restaurar son \*.bulk y system.properties.

Un documento de un archivo \*.bulk que tiene ``updatedTime`` solo se escribe si el documento
almacenado no existe, no tiene ``updatedTime`` o es más antiguo. Un documento que no es más
reciente se omite y se registra con nivel INFO en ``fess.log``, de modo que una restauración no
deshace los cambios hechos después de la copia de seguridad y los trabajos programados que incluye
la versión instalada (``updatedTime`` 0) se conservan tal cual. Los documentos sin ``updatedTime``
siempre se escriben.

.. note::

   |Fess| 15.9 guarda el ``password`` de la autenticación web y de archivos cifrado con la clave de cifrado de la
   aplicación (``app.cipher.key`` de ``fess_config.properties``), por lo que ``fess_basic_config.bulk`` y
   ``fess_config.bulk`` contienen los valores cifrados. Al restaurar una copia de seguridad en otra instalación,
   traslade la misma ``app.cipher.key``. Con una clave distinta, los rastreos que usan estas credenciales fallan con un
   error. Una copia de seguridad creada antes de 15.9 las contiene en texto sin cifrar y sigue funcionando.

   Los demás valores de un archivo ``*.bulk`` no están cifrados, así que conserve estos archivos como archivos
   confidenciales.

  .. |image0| image:: ../../../resources/images/en/15.9/admin/backup-1.png
