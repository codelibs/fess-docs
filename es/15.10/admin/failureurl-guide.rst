============
URL de fallo
============

Descripción general
===================

Aquí se explica sobre las URL de fallo.
Las URL que no se pudieron obtener durante el rastreo se registran y se pueden verificar como URL de fallo.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista para verificar las URL de fallo, haga clic en [Información del sistema > URL de fallo] en el menú izquierdo.

|image0|

Al hacer clic en el enlace de verificación de URL de fallo, se muestran los detalles.

Elementos de la lista
---------------------

La lista muestra la URL, el tipo, el tipo MIME, el estado HTTP, el tamaño (bytes) y la fecha del último acceso.

El tipo MIME, el estado HTTP y el tamaño se registran solo cuando el rastreador los conocía; en caso contrario quedan en blanco.

- Se registran cuando: el procesamiento falló después de obtener el documento (por ejemplo, se superó un límite de tamaño), o el servidor devolvió un estado HTTP incluido en ``crawler.failure.url.status.codes``. Cuando un documento se rechaza por superar un límite de tamaño antes de obtenerlo, solo se registra el tamaño.
- No se registran cuando: no se obtuvo respuesta, como en un tiempo de espera agotado o un error de conexión, ni en los fallos de rastreos de almacenes de datos. Un fallo al extraer el texto (por ejemplo, un PDF ilegible) tampoco se registra con el valor predeterminado ``crawler.ignore.content.exception=true``: el documento se indexa sin cuerpo. Solo se registra cuando esta clave es ``false``.
- El estado HTTP solo se registra para URL ``http`` / ``https``. Queda en blanco para archivos, SMB y otros protocolos.
- En una URL de fallo registrada antes de |Fess| 15.10, estos elementos quedan en blanco hasta que la URL vuelva a fallar.

Descarga de CSV
---------------

El botón [Descargar CSV] de la lista descarga en un archivo CSV las URL de fallo que coinciden con las condiciones introducidas en el formulario de búsqueda (URL, número de errores y tipo). El nombre del archivo es ``failureurl_yyyyMMddHHmmss.csv``.

- La primera fila contiene los nombres de las columnas, en este orden: ``url``, ``errorName``, ``errorCount``, ``lastAccessTime``, ``httpStatusCode``, ``mimeType`` y ``contentLength``. El registro (traza de pila) no se incluye.
- Se escriben todas las filas coincidentes, primero la de último acceso más reciente. La paginación no se aplica y no hay límite en el número de filas.
- ``lastAccessTime`` está en formato ISO 8601 en UTC (por ejemplo, ``2026-01-01T00:00:00.000Z``).
- La codificación de caracteres sigue "Codificación de archivo CSV" en [Sistema > General]; un archivo UTF-8 empieza con una marca de orden de bytes.
- Para que una hoja de cálculo no ejecute un valor como fórmula, un valor que empiece por ``=``, ``+``, ``-``, ``@``, un tabulador o un retorno de carro lleva un ``'`` delante.

Detalles de URL de fallo
==========================

Los detalles de URL de fallo registran las excepciones que ocurrieron durante el rastreo.

|image1|

Contenido de los detalles
--------------------------

URL
:::

URL en la que ocurrió la excepción.

Nombre del hilo
:::::::::::::::

Nombre del hilo que estaba ejecutando el rastreo.
Se puede utilizar al verificar archivos de registro.

Tipo
::::

Tipo de excepción.

Estado HTTP
:::::::::::

Estado HTTP de la respuesta para el documento. Se registra solo para URL ``http`` / ``https`` y solo cuando el rastreador lo conocía.

Tipo MIME
:::::::::

Tipo MIME del documento. Se registra solo cuando el rastreador lo conocía.

Tamaño (bytes)
::::::::::::::

Tamaño del documento. Se registra solo cuando el rastreador lo conocía.

Registro
::::::::

Contenido de la excepción.

Número de errores
:::::::::::::::::

Número de veces que ocurrió esta excepción.

Fecha del último acceso
:::::::::::::::::::::::

Hora en la que ocurrió esta excepción.


.. |image0| image:: ../../../resources/images/en/15.10/admin/failureurl-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/failureurl-2.png
