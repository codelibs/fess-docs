====================================
Registro como Servicio de Windows
====================================

Registro como Servicio de Windows
==================================

Puede registrar |Fess| como un servicio de Windows.
Para ejecutar |Fess|, es necesario que OpenSearch esté en ejecución.
Aquí se asume que |Fess| está instalado en ``c:\opt\fess`` y OpenSearch en ``c:\opt\opensearch``.

Preparación Previa
------------------

Configure JAVA_HOME como variable de entorno del sistema.

Registrar OpenSearch como Servicio
-----------------------------------

| Ejecute ``c:\opt\opensearch\bin\opensearch-service.bat`` desde el símbolo del sistema como administrador.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

Para más detalles, consulte la `documentación de OpenSearch <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_.

Configuración
-------------

Edite ``c:\opt\fess\bin\fess.in.bat`` y configure el directorio de instalación de OpenSearch en SEARCH_ENGINE_HOME.

::

    set SEARCH_ENGINE_HOME=c:/opt/opensearch

El número de puerto predeterminado para la pantalla de búsqueda y pantalla de administración de |Fess| es 8080. Para cambiar al puerto 80, modifique fess.port en ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80


Método de Registro
------------------

Ejecute ``c:\opt\fess\bin\service.bat`` desde el símbolo del sistema como administrador.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.


Configuración del Servicio
---------------------------

Al iniciar el servicio manualmente, inicie primero el servicio de OpenSearch y luego el servicio de |Fess|.
Para inicio automático, agregue la relación de dependencia.

1. En la configuración general del servicio, establezca el tipo de inicio como "Automático (Inicio retrasado)".
2. La dependencia del servicio se configura en el registro.

Agregue la siguiente clave y valor en el Editor del Registro (regedit).

.. list-table::

   * - *Clave*
     - ``Equipo\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services \fess-service-x64\DependOnService``
   * - *Valor*
     - ``opensearch-service-x64``

Una vez agregado, opensearch-service-x64 se mostrará en las dependencias de las propiedades del servicio de |Fess|.
