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

  .. |image0| image:: ../../../resources/images/en/15.3/admin/backup-1.png
