==========================
Procedimientos de Desinstalación
==========================

Esta página describe los procedimientos para desinstalar completamente |Fess|.

.. warning::

   **Notas Importantes Antes de la Desinstalación**

   - La desinstalación eliminará todos los datos
   - Si tiene datos importantes, asegúrese de hacer un respaldo
   - Para los procedimientos de respaldo, consulte :doc:`upgrade`

Preparación Antes de la Desinstalación
=======================================

Obtención de Respaldo
----------------------

Haga un respaldo de los datos necesarios:

1. **Datos de configuración**

   Descargue desde la pantalla de administración en "Sistema" → "Respaldo"

2. **Configuración de rastreo**

   Exporte la configuración de rastreo según sea necesario

3. **Archivos de configuración personalizados**

   Versión TAR.GZ/ZIP::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   Versión RPM/DEB::

       $ sudo cp -r /etc/fess /backup/

Detención del Servicio
-----------------------

Antes de desinstalar, detenga todos los servicios.

Versión TAR.GZ/ZIP::

    $ ps aux | grep fess
    $ kill <fess_pid>
    $ kill <opensearch_pid>

Versión RPM/DEB::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Versión Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Desinstalación de Versión TAR.GZ/ZIP
=====================================

Paso 1: Eliminación de Fess
----------------------------

Elimine el directorio de instalación::

    $ rm -rf /path/to/fess-15.4.0

Paso 2: Eliminación de OpenSearch
----------------------------------

Elimine el directorio de instalación de OpenSearch::

    $ rm -rf /path/to/opensearch-3.3.2

Paso 3: Eliminación del Directorio de Datos (Opcional)
-------------------------------------------------------

Por defecto, el directorio de datos está dentro del directorio de instalación de Fess,
pero si especificó otra ubicación, elimine también ese directorio::

    $ rm -rf /path/to/data

Paso 4: Eliminación del Directorio de Registros (Opcional)
-----------------------------------------------------------

Elimine los archivos de registro::

    $ rm -rf /path/to/fess/logs
    $ rm -rf /path/to/opensearch/logs

Desinstalación de Versión RPM
==============================

Paso 1: Desinstalación de Fess
-------------------------------

Desinstale el paquete RPM::

    $ sudo rpm -e fess

Paso 2: Desinstalación de OpenSearch
-------------------------------------

::

    $ sudo rpm -e opensearch

Paso 3: Deshabilitación y Eliminación del Servicio
---------------------------------------------------

En caso de chkconfig::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

En caso de systemd::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Paso 4: Eliminación del Directorio de Datos
--------------------------------------------

.. warning::

   Ejecutar esta operación eliminará completamente todos los datos de índice y configuración.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Paso 5: Eliminación de Archivos de Configuración
-------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Paso 6: Eliminación de Archivos de Registro
--------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Paso 7: Eliminación de Usuario y Grupo (Opcional)
--------------------------------------------------

Si desea eliminar el usuario y grupo del sistema::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Desinstalación de Versión DEB
==============================

Paso 1: Desinstalación de Fess
-------------------------------

Desinstale el paquete DEB::

    $ sudo dpkg -r fess

Para eliminar completamente incluyendo archivos de configuración::

    $ sudo dpkg -P fess

Paso 2: Desinstalación de OpenSearch
-------------------------------------

::

    $ sudo dpkg -r opensearch

O para eliminar incluyendo archivos de configuración::

    $ sudo dpkg -P opensearch

Paso 3: Deshabilitación del Servicio
-------------------------------------

::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Paso 4: Eliminación del Directorio de Datos
--------------------------------------------

.. warning::

   Ejecutar esta operación eliminará completamente todos los datos de índice y configuración.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Paso 5: Eliminación de Archivos de Configuración (Si no usó dpkg -P)
---------------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Paso 6: Eliminación de Archivos de Registro
--------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Paso 7: Eliminación de Usuario y Grupo (Opcional)
--------------------------------------------------

Si desea eliminar el usuario y grupo del sistema::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Desinstalación de Versión Docker
=================================

Paso 1: Eliminación de Contenedores y Red
------------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Paso 2: Eliminación de Volúmenes
---------------------------------

.. warning::

   Ejecutar esta operación eliminará completamente todos los datos.

Verificar lista de volúmenes::

    $ docker volume ls

Eliminar volúmenes relacionados con Fess::

    $ docker volume rm fess-es-data
    $ docker volume rm fess-data

O eliminar todos los volúmenes en lote::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Paso 3: Eliminación de Imágenes (Opcional)
-------------------------------------------

Si desea eliminar las imágenes Docker para liberar espacio en disco::

    $ docker images | grep fess
    $ docker rmi codelibs/fess:15.4.0

    $ docker images | grep opensearch
    $ docker rmi opensearchproject/opensearch:3.3.2

Paso 4: Eliminación de Red (Opcional)
--------------------------------------

Elimine la red creada por Docker Compose::

    $ docker network ls
    $ docker network rm <network_name>

Paso 5: Eliminación de Archivos Compose
----------------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

Verificación de la Desinstalación
==================================

Verifique que se hayan eliminado todos los componentes.

Verificación de Procesos
-------------------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

Si no se muestra nada, los procesos están detenidos.

Verificación de Puertos
------------------------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

Verifique que los puertos no estén en uso.

Verificación de Archivos
-------------------------

Versión TAR.GZ/ZIP::

    $ ls /path/to/fess-15.4.0  # Verifique que el directorio no exista

Versión RPM/DEB::

    $ ls /var/lib/fess  # Verifique que el directorio no exista
    $ ls /etc/fess      # Verifique que el directorio no exista

Versión Docker::

    $ docker ps -a | grep fess  # Verifique que no existan contenedores
    $ docker volume ls | grep fess  # Verifique que no existan volúmenes

Verificación de Paquetes
-------------------------

Versión RPM::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

Versión DEB::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

Si no se muestra nada, los paquetes están eliminados.

Desinstalación Parcial
=======================

Eliminar Solo Fess y Mantener OpenSearch
-----------------------------------------

Si OpenSearch se utiliza también en otras aplicaciones, puede eliminar solo Fess.

1. Detenga Fess
2. Elimine el paquete o directorio de Fess
3. Elimine el directorio de datos de Fess (``/var/lib/fess``, etc.)
4. No elimine OpenSearch

Eliminar Solo OpenSearch y Mantener Fess
-----------------------------------------

.. warning::

   Si elimina OpenSearch, Fess dejará de funcionar.
   Cambie la configuración para conectarse a otro clúster de OpenSearch.

1. Detenga OpenSearch
2. Elimine el paquete o directorio de OpenSearch
3. Elimine el directorio de datos de OpenSearch (``/var/lib/opensearch``, etc.)
4. Actualice la configuración de Fess para especificar otro clúster de OpenSearch

Solución de Problemas
======================

No se Puede Eliminar el Paquete
--------------------------------

**Síntoma:**

Se produce un error con ``rpm -e`` o ``dpkg -r``.

**Solución:**

1. Verifique que el servicio esté detenido::

       $ sudo systemctl stop fess.service

2. Verifique dependencias::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. Eliminación forzada (último recurso)::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

No se Puede Eliminar el Directorio
-----------------------------------

**Síntoma:**

No se puede eliminar el directorio con ``rm -rf``.

**Solución:**

1. Verificar permisos::

       $ ls -ld /path/to/directory

2. Eliminar con sudo::

       $ sudo rm -rf /path/to/directory

3. Verificar que ningún proceso esté usando archivos::

       $ sudo lsof | grep /path/to/directory

Preparación para Reinstalación
===============================

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
