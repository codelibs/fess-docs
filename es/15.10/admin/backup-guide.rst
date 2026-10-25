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

.. note::

   Los archivos de diccionario (sinónimos, palabras vacías, etc.) no forman parte de la copia de seguridad.
   Se guardan en el directorio de diccionarios del motor de búsqueda (``FESS_DICTIONARY_PATH``),
   por lo que debe copiarlos aparte si los necesita.

fess_config.bulk
::::::::::::::::

fess_config.bulk contiene la información de configuración de |Fess|.

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk contiene la información de configuración de |Fess| excluyendo la información de rastreo, las URL con falla, los registros de tareas, la cola de miniaturas, las etiquetas de usuario y datos similares.

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
Los archivos que se pueden restaurar son los siguientes:

- ``*.bulk``
- ``system.properties``
- ``fess.json`` y ``doc.json``: sustituyen los archivos de definición de índice que usa |Fess|. La configuración y el mapeo de un índice existente no se modifican en ese momento.
- ``gsa*.xml``: un archivo de configuración de Google Search Appliance. Se importa como configuración de rastreo web, configuración de rastreo de archivos y etiquetas.

Los archivos ``*.ndjson`` (registros de búsqueda y otros registros) no se pueden cargar para restaurarlos.

Un documento de un archivo \*.bulk que tiene ``updatedTime`` solo se escribe si el documento
almacenado no existe, no tiene ``updatedTime`` o es más antiguo. Un documento que no es más
reciente se omite y se registra con nivel INFO en ``fess.log``, de modo que una restauración no
deshace los cambios hechos después de la copia de seguridad y los trabajos programados que incluye
la versión instalada (``updatedTime`` 0) se conservan tal cual. Los documentos sin ``updatedTime``
siempre se escriben.

.. note::

   La omisión se registra con nivel INFO, por lo que con el nivel de registro predeterminado (``warn``) no se escribe en ``fess.log``. Para ver estas entradas, cambie el nivel de registro a ``info`` antes de la restauración. Puede cambiarlo en "Nivel de Registro" de [Sistema > General] en la pantalla de administración (vuelve al valor configurado al reiniciar |Fess|) o, en Linux, con ``FESS_LOG_LEVEL=info``. Consulte :doc:`../config/admin-logging` para más detalles.

.. note::

   |Fess| 15.9 guarda el ``password`` de la autenticación web y de archivos cifrado con la clave de cifrado de la
   aplicación (``app.cipher.key`` de ``fess_config.properties``), por lo que ``fess_basic_config.bulk`` y
   ``fess_config.bulk`` contienen los valores cifrados. Al restaurar una copia de seguridad en otra instalación,
   traslade la misma ``app.cipher.key``. Con una clave distinta, los rastreos que usan estas credenciales fallan con un
   error. Una copia de seguridad creada antes de 15.9 las contiene en texto sin cifrar y sigue funcionando.

   Los demás valores de un archivo ``*.bulk`` no están cifrados, así que conserve estos archivos como archivos
   confidenciales.

  .. |image0| image:: ../../../resources/images/en/15.10/admin/backup-1.png
