============
Host Virtual
============

Acerca del Host Virtual
=======================

|Fess| puede mostrar diferentes resultados de búsqueda según el nombre de host (valor del encabezado HTTP ``Host``) utilizado para acceder al sistema.
Es posible publicar un único servidor |Fess| con múltiples nombres de host y ofrecer distintos objetivos de búsqueda (configuraciones de rastreo) y diseños de página para cada host virtual.
Los resultados de búsqueda se muestran en archivos JSP individuales por host virtual, por lo que también puede personalizar el diseño para cada uno.

La función de host virtual está deshabilitada (sin configurar) de forma predeterminada. Siga los pasos a continuación para configurarla.

Configuración del Sistema
-------------------------

Configure la "Configuración General" en :doc:`Guía del Administrador > Configuración General <../admin/general-guide>` para definir la correspondencia entre el nombre de host de origen del acceso y el nombre del host virtual. El nombre del host virtual configurado aquí se especifica en la configuración de rastreo.

**Formato**

Defina un host virtual por línea con el siguiente formato:

::

   nombre_encabezado:valor_encabezado=nombre_host_virtual

.. list-table::

   * - *nombre_encabezado*
     - Nombre del encabezado de solicitud HTTP utilizado para la determinación. Normalmente se especifica ``Host``. También puede especificarse ``X-Forwarded-Host`` cuando el acceso se realiza a través de un proxy inverso.
   * - *valor_encabezado*
     - Nombre de host (con ``nombre_host:número_puerto`` si es necesario) incluido en el encabezado anterior. Este host virtual se aplica cuando el valor coincide exactamente (sin distinción entre mayúsculas y minúsculas) con el valor del encabezado enviado por el cliente en el momento del acceso.
   * - *nombre_host_virtual*
     - Nombre del host virtual que se especifica en la configuración de rastreo

**Ejemplo**

::

   Host:abc.example.com=host1
   Host:192.168.1.123:8080=host2

.. note::

   La determinación se realiza mediante una comparación de cadenas con el valor del encabezado de solicitud, no mediante la resolución de nombres de host (DNS).
   El encabezado ``Host`` enviado por el navegador no incluye el número de puerto cuando el acceso se realiza por el puerto estándar (80 para HTTP, 443 para HTTPS); para otros puertos, incluye el número de puerto con el formato ``nombre_host:número_puerto``.
   Por lo tanto, si publica el servicio en un puerto no estándar, especifique el número de puerto de forma explícita, como en ``Host:abc.example.com:8080=host1``.

.. note::

   Solo se pueden usar caracteres alfanuméricos y guiones bajos ( ``a-z`` , ``A-Z`` , ``0-9`` , ``_`` ) en los nombres de host virtual.
   Los demás caracteres se eliminan automáticamente.

   Además, los siguientes nombres están reservados y no se pueden usar como nombres de host virtual:
   ``admin`` , ``common`` , ``error`` , ``login`` , ``profile``

Una vez guardada la configuración, los archivos JSP de las páginas de búsqueda se generan en ``WEB-INF/view/nombre_host_virtual``.
Editando estos archivos, puede cambiar el diseño de las páginas para cada host virtual. Los archivos JSP también pueden editarse desde la pantalla :doc:`Guía del Administrador > Diseño <../admin/design-guide>`.


Configuración de Rastreo
------------------------

Especifique el "Host Virtual" en la configuración de rastreo web, la configuración de rastreo de archivos o la configuración de rastreo de almacén de datos.
Para "Host Virtual", especifique uno de los nombres de host virtual configurados en la configuración del sistema. También es posible especificar múltiples hosts virtuales en una sola configuración de rastreo (uno por línea).

En las búsquedas realizadas desde un host virtual, solo se muestran en los resultados los documentos de la configuración de rastreo que tiene asignado ese host virtual.
En los accesos que no coinciden con ningún host virtual (acceso normal sin host virtual configurado), este filtrado no se aplica y se muestran todos los resultados de búsqueda de forma habitual.

**Ejemplo**

.. list-table::

   * - *Host Virtual*
     - ``host1``
