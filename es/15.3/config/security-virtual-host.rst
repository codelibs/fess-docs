========
Host Virtual
========

Acerca del Host Virtual
==============

|Fess| puede mostrar diferentes resultados de búsqueda según el nombre de host (parte de host de la URL) utilizado para acceder al sistema.
Los resultados de búsqueda se muestran en JSP individuales, por lo que también puede personalizar el diseño para cada host virtual.

Configuración del Sistema
----------

Configure el "Host Virtual" en :doc:`Guía del Administrador > Configuración General <../admin/general-guide>`. El nombre del host virtual configurado aquí se especifica en la configuración de rastreo.

**Formato**

::

   Host:nombre_host[:número_puerto]=nombre_host_virtual

.. list-table::

   * - *nombre_host*
     - Nombre de host o dirección IP que se puede resolver en el sistema (DNS)
   * - *número_puerto*
     - Opcional. Por defecto es 80.
   * - *nombre_host_virtual*
     - Nombre del host virtual que se especifica en la configuración de rastreo

**Ejemplo**

::

   Host:abc.example.com:8080=host1
   Host:192.168.1.123:8080=host2

Una vez configurado, se generan los archivos JSP de las páginas de búsqueda en ``WEB-INF/view/nombre_host_virtual``.
Puede cambiar el diseño de las páginas para cada host virtual editando estos archivos.


Configuración de Rastreo
---------

Especifique el "Host Virtual" en la configuración de rastreo web, configuración de rastreo de archivos o configuración de rastreo de almacén de datos.
Para "Host Virtual", especifique uno de los nombres de host virtual configurados en la configuración del sistema.

**Ejemplo**

.. list-table::

   * - *Host Virtual*
     - ``host1``

