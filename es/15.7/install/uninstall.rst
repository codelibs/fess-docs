================================
Procedimientos de Desinstalación
================================

Esta página describe los procedimientos para desinstalar completamente |Fess|.

.. warning::

   **Notas Importantes Antes de la Desinstalación**

   - La desinstalación eliminará todos los datos
   - Si tiene datos importantes, asegúrese de hacer un respaldo
   - Para los procedimientos de respaldo, consulte :doc:`upgrade`

Preparación Antes de la Desinstalación
======================================

Obtención de Respaldo
---------------------

Haga un respaldo de los datos necesarios:

1. **Datos de configuración**

   Descargue desde la pantalla de administración en "Sistema" → "Copia de seguridad".
   Con esta operación puede exportar de forma conjunta las distintas configuraciones (incluida la configuración de rastreo) y los registros de búsqueda, entre otros.

2. **Archivos de configuración personalizados**

   Versión TAR.GZ/ZIP::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   Versión RPM/DEB::

       $ sudo cp -r /etc/fess /backup/

.. note::

   La mayor parte del índice y de la configuración de |Fess| se almacena en OpenSearch.
   Para hacer un respaldo de los datos del índice, utilice la función de instantáneas (snapshot) de OpenSearch.
   Para conocer el procedimiento detallado, consulte :doc:`upgrade`.

Detención del Servicio
----------------------

Antes de desinstalar, detenga todos los servicios.

Versión TAR.GZ/ZIP::

    $ ps aux | grep -E 'fess|opensearch'
    $ kill <fess_pid>
    $ kill <opensearch_pid>

Versión RPM/DEB::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Versión Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Desinstalación de Versión TAR.GZ/ZIP
====================================

Paso 1: Eliminación de Fess
---------------------------

Elimine el directorio de instalación::

    $ rm -rf /path/to/fess-15.7.0

Paso 2: Eliminación de OpenSearch
---------------------------------

Elimine el directorio de instalación de OpenSearch::

    $ rm -rf /path/to/opensearch-3.7.0

Paso 3: Eliminación del Directorio de Datos (Opcional)
------------------------------------------------------

Los datos del índice de |Fess| se almacenan en OpenSearch.
Por defecto se guardan dentro del directorio de instalación de OpenSearch (por ejemplo, ``opensearch-3.7.0/data``),
pero si ha especificado otra ubicación con ``path.data``, elimine también ese directorio::

    $ rm -rf /path/to/data

Paso 4: Eliminación del Directorio de Registros (Opcional)
----------------------------------------------------------

Elimine los archivos de registro::

    $ rm -rf /path/to/fess-15.7.0/logs
    $ rm -rf /path/to/opensearch-3.7.0/logs

Desinstalación de Versión RPM
=============================

Paso 1: Desinstalación de Fess
------------------------------

Desinstale el paquete RPM::

    $ sudo rpm -e fess

.. note::

   Durante la desinstalación del paquete de |Fess|, el script de eliminación del paquete
   detiene y deshabilita automáticamente el servicio ``fess`` y elimina el usuario y el grupo ``fess``.
   Los pasos siguientes se realizan para confirmar que estos se hayan eliminado correctamente o para
   eliminar manualmente los datos y los archivos de configuración.

Paso 2: Desinstalación de OpenSearch
------------------------------------

::

    $ sudo rpm -e opensearch

Paso 3: Confirmación de la Deshabilitación del Servicio
-------------------------------------------------------

Normalmente el servicio se deshabilita al eliminar el paquete, pero, por si acaso, para confirmar o deshabilitar ejecute lo siguiente.

En caso de systemd::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

En el caso de un entorno antiguo con SysV init (chkconfig)::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

Paso 4: Eliminación del Directorio de Datos
-------------------------------------------

.. warning::

   Al ejecutar esta operación se eliminarán por completo todos los datos del índice.

Dado que el directorio de datos no se elimina al desinstalar el paquete, elimínelo manualmente::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Paso 5: Eliminación de Archivos de Configuración
------------------------------------------------

Elimine los archivos de configuración y los archivos de configuración de entorno::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/sysconfig/fess
    $ sudo rm -rf /etc/opensearch

.. note::

   En RPM, los archivos de configuración dentro de ``/etc/fess`` pueden quedar con el nombre ``.rpmsave``.
   Para eliminarlos por completo, elimínelos manualmente como se indica arriba.

Paso 6: Eliminación de Archivos de Registro
-------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Paso 7: Eliminación del Directorio Temporal (Opcional)
------------------------------------------------------

::

    $ sudo rm -rf /var/tmp/fess

Paso 8: Eliminación de Usuario y Grupo (Opcional)
-------------------------------------------------

Normalmente, el usuario y el grupo ``fess`` se eliminan al eliminar el paquete.
Si permanecen, o si desea eliminar el usuario y el grupo de OpenSearch, ejecute lo siguiente::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Desinstalación de Versión DEB
=============================

Paso 1: Desinstalación de Fess
------------------------------

Desinstale el paquete DEB::

    $ sudo dpkg -r fess

Para eliminar completamente incluyendo los archivos de configuración y los archivos de configuración de entorno, utilice purge::

    $ sudo dpkg -P fess

.. note::

   Con ``dpkg -r`` (remove), los archivos de configuración (conffile) como ``/etc/default/fess`` permanecen.
   Si utiliza ``dpkg -P`` (purge), se eliminan estos archivos de configuración junto con el usuario y el grupo ``fess``.

Paso 2: Desinstalación de OpenSearch
------------------------------------

::

    $ sudo dpkg -r opensearch

O bien, para eliminar incluyendo los archivos de configuración::

    $ sudo dpkg -P opensearch

Paso 3: Confirmación de la Deshabilitación del Servicio
-------------------------------------------------------

Normalmente el servicio se deshabilita al eliminar el paquete. Por si acaso, para confirmar o deshabilitar ejecute lo siguiente::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Paso 4: Eliminación del Directorio de Datos
-------------------------------------------

.. warning::

   Al ejecutar esta operación se eliminarán por completo todos los datos del índice.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Paso 5: Eliminación de Archivos de Configuración (Si no usó dpkg -P)
--------------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/default/fess
    $ sudo rm -rf /etc/opensearch

Paso 6: Eliminación de Archivos de Registro
-------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Paso 7: Eliminación de Usuario y Grupo (Opcional)
-------------------------------------------------

Si no utilizó ``dpkg -P``, el usuario y el grupo ``fess`` permanecen.
Si desea eliminarlos, ejecute lo siguiente::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Desinstalación de Versión Docker
================================

Paso 1: Eliminación de Contenedores y Red
-----------------------------------------

Elimine los contenedores y la red creada por Docker Compose (``search_net``)::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Paso 2: Eliminación de Volúmenes
--------------------------------

.. warning::

   Al ejecutar esta operación se eliminarán por completo todos los datos.

Los datos de |Fess| (índices, diccionarios, etc.) se almacenan en los volúmenes de OpenSearch.
Primero, verifique la lista de volúmenes::

    $ docker volume ls

Elimine los volúmenes relacionados con OpenSearch::

    $ docker volume rm <project>_search01_data
    $ docker volume rm <project>_search01_dictionary

.. note::

   Los nombres de los volúmenes llevan como prefijo el nombre del proyecto de Docker Compose (normalmente el nombre
   del directorio en el que se ubicó el archivo Compose). Verifique el nombre real con ``docker volume ls``.

Para eliminar los contenedores y los volúmenes de una sola vez, añada la opción ``-v`` a ``down``::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Paso 3: Eliminación de Imágenes (Opcional)
------------------------------------------

Si desea eliminar las imágenes Docker para liberar espacio en disco::

    $ docker images | grep fess
    $ docker rmi ghcr.io/codelibs/fess:15.7.0
    $ docker rmi ghcr.io/codelibs/fess-opensearch:3.7.0

Paso 4: Eliminación de Archivos Compose
---------------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

Verificación de la Desinstalación
=================================

Verifique que se hayan eliminado todos los componentes.

Verificación de Procesos
------------------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

Si no se muestra nada, los procesos están detenidos.

Verificación de Puertos
-----------------------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

Verifique que los puertos no estén en uso.

Verificación de Archivos
------------------------

Versión TAR.GZ/ZIP::

    $ ls /path/to/fess-15.7.0  # Verifique que el directorio no exista

Versión RPM/DEB::

    $ ls /var/lib/fess  # Verifique que el directorio no exista
    $ ls /etc/fess      # Verifique que el directorio no exista

Versión Docker::

    $ docker ps -a | grep -E 'fess01|search01'  # Verifique que no existan contenedores
    $ docker volume ls | grep search01           # Verifique que no existan volúmenes

Verificación de Paquetes
------------------------

Versión RPM::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

Versión DEB::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

Si no se muestra nada, los paquetes están eliminados.

Desinstalación Parcial
======================

Eliminar Solo Fess y Mantener OpenSearch
----------------------------------------

Si OpenSearch se utiliza también en otras aplicaciones, puede eliminar solo Fess.

1. Detenga Fess
2. Elimine el paquete o el directorio de Fess
3. Elimine el directorio de datos de Fess (``/var/lib/fess``, etc.)
4. Elimine los índices de |Fess| creados dentro de OpenSearch (``fess.*``, ``.fess_*``, etc.)
5. No elimine OpenSearch

Eliminar Solo OpenSearch y Mantener Fess
----------------------------------------

.. warning::

   Si elimina OpenSearch, Fess dejará de funcionar.
   Cambie la configuración para conectarse a otro clúster de OpenSearch.

1. Detenga OpenSearch
2. Elimine el paquete o el directorio de OpenSearch
3. Elimine el directorio de datos de OpenSearch (``/var/lib/opensearch``, etc.)
4. Actualice la configuración de Fess para especificar otro clúster de OpenSearch

Solución de Problemas
=====================

No se Puede Eliminar el Paquete
-------------------------------

**Síntoma:**

Se produce un error con ``rpm -e`` o ``dpkg -r``.

**Solución:**

1. Verifique que el servicio esté detenido::

       $ sudo systemctl stop fess.service

2. Verifique las dependencias::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. Eliminación forzada (último recurso)::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

No se Puede Eliminar el Directorio
----------------------------------

**Síntoma:**

No se puede eliminar el directorio con ``rm -rf``.

**Solución:**

1. Verifique los permisos::

       $ ls -ld /path/to/directory

2. Elimine con sudo::

       $ sudo rm -rf /path/to/directory

3. Verifique que ningún proceso esté usando archivos::

       $ sudo lsof | grep /path/to/directory

Preparación para la Reinstalación
=================================

Si va a reinstalar después de desinstalar, verifique lo siguiente:

1. Que todos los procesos estén detenidos
2. Que se hayan eliminado todos los archivos y directorios
3. Que los puertos 8080 y 9200 no estén en uso
4. Que no queden archivos de configuración anteriores

Para los procedimientos de reinstalación, consulte :doc:`install`.

Próximos Pasos
==============

Una vez completada la desinstalación:

- Para instalar una nueva versión, consulte :doc:`install`
- Para migrar datos, consulte :doc:`upgrade`
- Para considerar soluciones de búsqueda alternativas, consulte el sitio oficial de Fess
