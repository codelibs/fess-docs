====================================
Registro como Servicio de Windows
====================================

Registro como Servicio de Windows
==================================

Puede registrar |Fess| como un servicio de Windows. Al registrarlo como servicio, |Fess| puede iniciarse automáticamente al arrancar el sistema.
Para ejecutar |Fess|, es necesario que OpenSearch esté en ejecución.
Aquí se asume que |Fess| está instalado en ``c:\opt\fess`` y OpenSearch en ``c:\opt\opensearch`` (ajuste las rutas según su entorno).

.. note::
   |Fess| y OpenSearch solo admiten la versión de 64 bits.

Preparación Previa
------------------

Configure ``JAVA_HOME`` como variable de entorno del sistema. Si ``JAVA_HOME`` no está definida, ``service.bat`` finalizará con un error.

Registrar OpenSearch como Servicio
-----------------------------------

Abra el símbolo del sistema con privilegios de administrador y ejecute ``c:\opt\opensearch\bin\opensearch-service.bat``.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

Para más detalles, consulte la `documentación de OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/windows/>`_.

Configuración de |Fess|
------------------------

El servicio se registra mediante ``c:\opt\fess\bin\service.bat``. Al registrarlo, ``service.bat`` lee ``bin\fess.in.bat`` y aplica su contenido a las opciones de inicio de |Fess|.
Agregue la configuración de conexión a OpenSearch en ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=c:/opt/opensearch/data/config/

.. note::
   - En ``fess.search_engine.http_address`` especifique el destino de conexión del servicio OpenSearch registrado. Si no se configura esta opción, |Fess| no podrá encontrar el destino de conexión e iniciará la versión embebida de OpenSearch, que no es recomendada para entornos de producción.
   - Si OpenSearch se ejecuta en un host diferente, cambie el nombre de host o la dirección IP según corresponda.
   - Utilice ``/`` como separador de ruta.

El número de puerto predeterminado para la pantalla de búsqueda y la pantalla de administración de |Fess| es ``8080``. Para cambiar a otro puerto, edite ``-Dfess.port`` en ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

.. note::
   Al registrar como servicio, ``-Dfess.port=8080`` también está codificado en ``FESS_PARAMS`` dentro de ``bin\service.bat``. Este valor tiene prioridad sobre la configuración de ``fess.in.bat``, por lo que al cambiar el puerto también debe editar ``FESS_PARAMS`` en ``service.bat`` de la misma manera.

Personalización del Servicio (opcional)
-----------------------------------------

Es posible modificar la configuración del servicio estableciendo variables de entorno antes de ejecutar ``service.bat install``. Las principales variables de entorno son las siguientes.

.. list-table::
   :header-rows: 1

   * - Variable de entorno
     - Descripción
   * - ``FESS_START_TYPE``
     - Tipo de inicio (``auto`` o ``manual``). El valor predeterminado es ``manual``.
   * - ``FESS_HEAP_SIZE``
     - Tamaño del heap (por ejemplo: ``1g``). Para especificar el tamaño mínimo y máximo del heap de forma individual, use ``FESS_MIN_MEM`` (predeterminado ``256m``) y ``FESS_MAX_MEM`` (predeterminado ``1g``).
   * - ``SERVICE_USERNAME`` / ``SERVICE_PASSWORD``
     - Cuenta de Windows bajo la que se ejecuta el servicio.
   * - ``SERVICE_DISPLAY_NAME``
     - Nombre para mostrar del servicio.
   * - ``SERVICE_DESCRIPTION``
     - Descripción del servicio.

Método de Registro
------------------

Ejecute ``c:\opt\fess\bin\service.bat`` desde el símbolo del sistema con privilegios de administrador.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

Configuración del Servicio
---------------------------

Al iniciar el servicio manualmente, inicie primero el servicio de OpenSearch y luego el servicio de |Fess|.
Para que se inicie automáticamente al arrancar el sistema, configure el tipo de inicio y las dependencias.

1. En la configuración general del servicio, establezca el tipo de inicio como "Automático (Inicio retrasado)".
2. La dependencia del servicio se configura en el registro.

Agregue la siguiente clave y valor en el Editor del Registro (regedit).

.. list-table::

   * - *Clave*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *Valor*
     - ``opensearch-service-x64``

Una vez agregado, opensearch-service-x64 se mostrará en las dependencias de las propiedades del servicio de |Fess|.

.. note::
   Si establece la variable de entorno ``FESS_START_TYPE=auto`` antes de ejecutar ``service.bat install``, el servicio se registrará con el tipo de inicio "Automático". Sin embargo, "Automático (Inicio retrasado)" y la configuración de dependencias no pueden realizarse mediante ``service.bat``, por lo que deberá configurarlos siguiendo el procedimiento indicado anteriormente.

Gestión del Servicio
---------------------

Con ``service.bat`` puede administrar el servicio mediante los siguientes comandos.

.. list-table::
   :header-rows: 1

   * - Comando
     - Descripción
   * - ``service.bat install``
     - Registra el servicio.
   * - ``service.bat remove``
     - Elimina el servicio.
   * - ``service.bat start``
     - Inicia el servicio.
   * - ``service.bat stop``
     - Detiene el servicio.
   * - ``service.bat manager``
     - Inicia la interfaz gráfica de administración del servicio.
