======
Tema
======

Descripción general
====================

La función de temas gestiona los «temas estáticos», que agrupan el aspecto visual de la pantalla de búsqueda (conjunto de activos estáticos como HTML, CSS y JavaScript). Los temas estáticos se suben como archivos ZIP y se extraen en el directorio de temas del servidor (predeterminado: ``themes``, modificable con ``theme.directory.path``). En la raíz de cada tema debe colocarse el manifiesto ``theme.yml``, que describe los metadatos del tema.

.. note::
   Los temas basados en JSP se gestionan desde la administración de complementos y quedan fuera del ámbito de esta página.
   Para realizar las operaciones de esta página se requiere el rol ``admin-theme`` (o el rol ``admin-theme-view`` si solo se necesita acceso de lectura).

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de temas registrados, haga clic en [Sistema > Tema] en el menú izquierdo.

Lista de temas
--------------

La página de lista muestra los temas estáticos registrados en el directorio de temas. Las columnas que aparecen en cada fila son las siguientes.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Miniatura
     - Muestra el archivo ``thumbnail.png`` del directorio del tema. Si no existe, no se muestra.
   * - Nombre
     - Nombre del tema (nombre del directorio del tema). Al hacer clic se muestra la página de detalles.
   * - Nombre para mostrar
     - Campo ``displayName`` del manifiesto.
   * - Versión
     - Campo ``version`` del manifiesto.
   * - Predeterminado
     - Se marca cuando el tema está configurado como tema predeterminado.
   * - Operaciones
     - Muestra el botón Eliminar para eliminar el tema (no aparece para el tema predeterminado).

Tabla: Columnas de la lista de temas


Establecer el tema predeterminado
----------------------------------

Seleccione un tema en el menú desplegable de la parte superior de la página de lista y haga clic en el botón [Establecer como predeterminado] para configurar el tema predeterminado que se aplica a la pantalla de búsqueda. Al seleccionar [(sin predeterminado)] y confirmar la configuración, se cancela la asignación del tema predeterminado. Una vez guardado, la información del tema se recarga y los cambios se aplican de inmediato.


Subir un tema
-------------

Al hacer clic en el botón [Subir] se abre la página de carga. Seleccione el archivo ZIP del tema y haga clic en el botón [Subir] para instalar el tema.

* Solo se admiten archivos en formato ``.zip``.
* El tamaño máximo del archivo comprimido es 50 MB de forma predeterminada (``theme.upload.max.size``).
* El archivo ZIP debe contener el manifiesto ``theme.yml`` en su raíz.

Si ya existe un tema con el mismo nombre, será reemplazado. El tema original reemplazado se conserva como copia de seguridad durante un período determinado (7 días de forma predeterminada, ``theme.upload.attic.retention.days``).

Si el archivo subido no supera la validación del manifiesto, o si el tamaño extraído, el número de entradas o la tasa de compresión superan los límites del servidor (protección contra bombas ZIP), la instalación será rechazada y se mostrará un mensaje de error.


Manifiesto theme.yml
---------------------

En la raíz del tema estático debe colocarse el archivo ``theme.yml`` (formato YAML) con los metadatos del tema. Los campos disponibles son los siguientes.

.. tabularcolumns:: |p{3cm}|p{2cm}|p{7cm}|
.. list-table::
   :header-rows: 1

   * - Campo
     - Requerido
     - Descripción
   * - ``apiVersion``
     - Requerido
     - Especifique ``fess.codelibs.org/v1``.
   * - ``kind``
     - Requerido
     - Especifique ``StaticTheme``.
   * - ``name``
     - Requerido
     - Nombre del tema. Debe seguir el patrón ``^[a-z0-9][a-z0-9_-]{0,63}$`` y coincidir con el nombre del directorio del tema.
   * - ``displayName``
     - Requerido
     - Nombre que se muestra en pantalla (máximo 4096 caracteres).
   * - ``version``
     - Requerido
     - Versión en formato SemVer (por ejemplo: ``1.0.0``).
   * - ``author``
     - Opcional
     - Autor del tema.
   * - ``description``
     - Opcional
     - Descripción del tema.
   * - ``license``
     - Opcional
     - Licencia del tema.
   * - ``homepage``
     - Opcional
     - URL de la página de inicio del tema.
   * - ``minFessVersion``
     - Opcional
     - Versión mínima de |Fess| compatible.
   * - ``supportedLocales``
     - Opcional
     - Idiomas (locales) compatibles.
   * - ``entry``
     - Opcional
     - Archivo de punto de entrada (predeterminado: ``index.html``).
   * - ``spaFallback``
     - Opcional
     - Activa o desactiva el fallback de tipo SPA (predeterminado: ``true``).

Tabla: Campos de theme.yml


Eliminar un tema
-----------------

Es posible eliminar un tema desde el botón Eliminar de la página de lista o desde el botón [Eliminar] de la página de detalles. No es posible eliminar el tema configurado como predeterminado; antes de eliminarlo, cancele la asignación de tema predeterminado. El tema eliminado se conserva como copia de seguridad durante un período determinado (7 días de forma predeterminada, ``theme.upload.attic.retention.days``).


Recargar
---------

Si el directorio de temas se edita directamente en el servidor, haga clic en el botón [Recargar] para volver a cargar en memoria la información de los temas almacenada en disco.


Detalles del tema
------------------

Al hacer clic en el nombre de un tema en la página de lista se muestra la página de detalles. En ella puede consultar el contenido del manifiesto (nombre, nombre para mostrar, versión, disponibilidad como predeterminado y estado).


Propiedades de configuración
=============================

Las principales configuraciones relacionadas con la función de temas se pueden modificar en ``fess_config.properties``.

.. tabularcolumns:: |p{6cm}|p{3cm}|p{5cm}|
.. list-table::
   :header-rows: 1

   * - Propiedad
     - Valor predeterminado
     - Descripción
   * - ``theme.directory.path``
     - ``themes``
     - Directorio donde se almacenan los temas (ruta relativa al contexto del servlet o ruta absoluta).
   * - ``theme.upload.max.size``
     - ``52428800``
     - Tamaño máximo del archivo ZIP que se puede subir (bytes, aprox. 50 MB).
   * - ``theme.upload.max.extracted.size``
     - ``209715200``
     - Tamaño total máximo tras la extracción (bytes, aprox. 200 MB).
   * - ``theme.upload.max.entries``
     - ``1000``
     - Número máximo de entradas que puede contener el archivo ZIP.
   * - ``theme.upload.max.compression.ratio``
     - ``100``
     - Tasa máxima de compresión por entrada.
   * - ``theme.upload.zip.ratio.max``
     - ``50``
     - Límite superior de la tasa de compresión acumulada (protección contra bombas ZIP).
   * - ``theme.upload.zip.ratio.check.threshold.bytes``
     - ``65536``
     - Bytes comprimidos a partir de los cuales se evalúa la tasa de compresión acumulada.
   * - ``theme.upload.attic.retention.days``
     - ``7``
     - Número de días que se conserva la copia de seguridad de un tema reemplazado o eliminado.

Tabla: Propiedades de configuración de la función de temas
