=====================
Informe de documentos
=====================

Descripción general
===================

La página Informe de documentos ayuda a ordenar servidores de archivos rastreados y similares. Muestra
los documentos con el mismo contenido y los que llevan mucho tiempo sin modificarse, y cada lista se
puede descargar como CSV.

Para abrir la página, seleccione [Información del sistema > Informe de documentos] en el menú
izquierdo. Para verla se necesita el rol ``admin-docreport`` o ``admin-docreport-view``. La página
solo muestra y descarga informes; no modifica ningún documento.

Ambas pestañas se pueden acotar con "Prefijo de URL", por ejemplo ``smb://server/share/``.

Duplicados
==========

Los documentos con el mismo contenido, o casi el mismo, se agrupan, empezando por el grupo más
grande. Los grupos usan la firma de contenido calculada al indexar (``content_minhash_bits``, la
misma que agrupa los resultados de búsqueda duplicados), por lo que no hace falta reindexar. Se
excluyen los documentos cuyo contenido no tiene palabras (como los archivos vacíos).

La pantalla muestra hasta ``docreport.duplicate.group.size`` (predeterminado: 100) grupos y hasta
``docreport.duplicate.docs.size`` (predeterminado: 10) documentos por grupo. Use [Descargar CSV] para
obtener todos los grupos. El CSV lee todos los grupos, incluso en un índice grande, con las columnas
``group, groupSize, url, title, filename, contentLength, lastModified, owner, lastModifier, clickCount, docId``.

.. note::

   El informe de duplicados necesita la firma de contenido, que las definiciones de índice para un OpenSearch sin los plugins de CodeLibs (``search_engine.type`` con ``vanilla``, ``aws`` o el obsoleto ``cloud``) no calculan. Con estos tipos se oculta la pestaña «Duplicados» y solo está disponible el informe de documentos inactivos. Consulte :doc:`../config/search-engine-type`.

Documentos inactivos
====================

Se muestran, del más antiguo al más reciente, los documentos cuya última modificación es anterior al
número de días indicado ("Sin modificar durante (días)", 365 de forma predeterminada según
``docreport.dormant.days``). Los documentos sin fecha de última modificación no se muestran. Con
"Nunca abiertos desde los resultados de búsqueda" se excluyen los documentos en los que se ha hecho
clic desde los resultados de búsqueda.

La pantalla muestra el número de documentos coincidentes, su tamaño total y una lista paginada. La
paginación se detiene en ``indexer.max.result.window.size``; use [Descargar CSV] para obtener los
documentos que quedan más allá.

Configuración
=============

Los siguientes ajustes de ``fess_config.properties`` ajustan el informe.

.. list-table::
   :header-rows: 1
   :widths: 40 45 15

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``docreport.duplicate.group.size``
     - Número máximo de grupos de duplicados que muestra la pantalla
     - ``100``
   * - ``docreport.duplicate.docs.size``
     - Número máximo de documentos que la pantalla muestra por grupo
     - ``10``
   * - ``docreport.duplicate.export.page.size``
     - Número de firmas de contenido leídas por solicitud al descargar el CSV
     - ``10000``
   * - ``docreport.dormant.days``
     - Número predeterminado de días desde la última modificación a partir del cual un documento está inactivo
     - ``365``
