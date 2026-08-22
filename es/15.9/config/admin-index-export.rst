================================
Función de Exportación de Índice
================================

Descripción General
===================

La función de Exportación de Índice exporta los documentos de búsqueda indexados en OpenSearch como archivos HTML o JSON al sistema de archivos local. Esta funcionalidad es útil para:

- Crear copias de seguridad estáticas del contenido indexado
- Generar copias sin conexión de documentos para fines de archivo
- Construir páginas de resultados de búsqueda estáticas
- Migración de contenido a otros sistemas

Los archivos exportados mantienen la estructura de ruta URL original de los documentos de origen, lo que facilita la gestión del contenido exportado.

Cómo Funciona
=============

Cuando se ejecuta el trabajo de Exportación de Índice, se realiza el siguiente proceso:

1. **Obtención de documentos**: Recupera documentos de OpenSearch en lotes de forma eficiente mediante la API de scroll
2. **Procesamiento de contenido**: Extrae los campos del documento (título, contenido, URL, etc.) y elimina los campos excluidos
3. **Creación de la estructura de directorios**: Reproduce la estructura de ruta URL en el directorio de exportación basándose en el campo ``url`` del documento
4. **Generación de archivos**: Crea archivos (HTML o JSON) con el contenido del documento
5. **Continuación hasta completar**: Procesa los lotes hasta que el índice esté completamente exportado

La API de scroll permite procesar eficientemente grandes conjuntos de documentos sin problemas de memoria.

.. note::

   Los documentos exportados corresponden al índice de búsqueda (``fess.search``). Los documentos que no tengan el campo ``url`` serán omitidos.

Propiedades de Configuración
=============================

Configure la función de Exportación de Índice en ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Propiedad
     - Valor Predeterminado
     - Descripción
   * - ``index.export.path``
     - ``/var/lib/fess/export``
     - Directorio donde se almacenan los archivos exportados
   * - ``index.export.exclude.fields``
     - ``cache``
     - Campos a excluir de la exportación (separados por comas)
   * - ``index.export.scroll.size``
     - ``100``
     - Número de documentos procesados por lote
   * - ``index.export.format``
     - ``html``
     - Formato del archivo de exportación (``html`` o ``json``)

Ejemplo de configuración:

::

    index.export.path=/data/fess/export
    index.export.exclude.fields=cache,boost,role
    index.export.scroll.size=200

Habilitar el Trabajo
====================

El trabajo de Exportación de Índice está registrado como trabajo programado pero está deshabilitado por defecto.

Para habilitar el trabajo:

1. Inicie sesión en la consola de administración de |Fess|
2. Navegue a **Sistema** > **Programador**
3. Busque **Index Exporter** en la lista de trabajos
4. Haga clic para editar la configuración del trabajo
5. Establezca el horario con una expresión cron
6. Guarde la configuración

Ejemplos de expresiones cron:

- ``0 0 2 * * ?`` - Ejecutar diariamente a las 2:00 AM
- ``0 0 3 ? * SUN`` - Ejecutar cada domingo a las 3:00 AM
- ``0 0 0 1 * ?`` - Ejecutar el primer día de cada mes a medianoche

Filtrado de Consultas Personalizado
=====================================

Puede personalizar el trabajo de exportación para exportar solo documentos específicos modificando el script del trabajo.

El script predeterminado del trabajo **Index Exporter** exporta todos los documentos:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.matchAllQuery())
        .execute()

Para agregar un filtro de consulta personalizado:

1. Navegue a **Sistema** > **Programador**
2. Edite el **Index Exporter**
3. Modifique el script del trabajo para añadir el filtro de consulta

Ejemplo de filtro por fecha (exportar solo documentos de los últimos 7 días):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.rangeQuery("created").gte("now-7d"))
        .execute()

Ejemplo de filtro por sitio (exportar solo documentos de un sitio específico):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.wildcardQuery("url", "*example.com*"))
        .execute()

Ejemplo de exportación en formato JSON:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .format("json")
        .execute()

Estructura de Archivos Exportados
==================================

Los archivos exportados se organizan reflejando la estructura URL original.

Por ejemplo, un documento con la URL ``https://example.com/docs/guide/intro.html`` se exportará de la siguiente manera:

::

    /var/lib/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

La ruta del archivo se determina a partir del campo ``url`` del documento según las siguientes reglas:

- El nombre de host se convierte en el directorio de nivel superior. Si la URL no contiene nombre de host, se utiliza ``_local``.
- Si la ruta termina en barra o no tiene ruta, se crea un archivo índice (``index.html`` o ``index.json``).
- Si la ruta no contiene extensión de archivo, se añade la extensión correspondiente al formato (``.html`` o ``.json``).
- Los caracteres no válidos en nombres de archivo (``< > : " | ? * \``) se reemplazan por ``_``, y cada componente de la ruta se trunca a un máximo de 200 caracteres.
- Si no es posible analizar la URL o se detecta un path traversal, el archivo se guarda en el directorio ``_invalid`` usando el hash de la URL como nombre de archivo.

En el caso del formato HTML, cada archivo se genera con la siguiente estructura:

- Campo ``title`` → elemento ``<title>``
- Campo ``lang`` → atributo ``lang`` del elemento ``<html>``
- Campo ``content`` → cuerpo del elemento ``<body>``
- Resto de campos no excluidos → etiquetas ``<meta name="fess:nombre_campo" content="valor">`` dentro de ``<head>``

::

    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Documento de ejemplo</title>
    <meta name="fess:url" content="https://example.com/docs/guide/intro.html">
    <meta name="fess:last_modified" content="2024-01-01T00:00:00.000Z">
    <meta name="fess:content_type" content="text/html">
    </head>
    <body>
    Contenido del cuerpo del documento
    </body>
    </html>

En el caso del formato JSON, cada archivo es un objeto JSON que contiene todos los campos no excluidos:

::

    {
      "url": "https://example.com/docs/guide/intro.html",
      "title": "Documento de ejemplo",
      "content": "Contenido del cuerpo del documento",
      "last_modified": "2024-01-01T00:00:00.000Z",
      "content_type": "text/html"
    }

Mejores Prácticas
=================

Consideraciones de Almacenamiento
----------------------------------

- Asegure suficiente espacio en disco en el directorio de exportación
- Considere usar almacenamiento dedicado para grandes conjuntos de documentos
- Implemente una limpieza periódica de exportaciones antiguas si ejecuta exportaciones regulares

Consejos de Rendimiento
------------------------

- Ajuste ``index.export.scroll.size`` según el tamaño de los documentos:
  - Documentos pequeños: tamaño de lote mayor (200-500)
  - Documentos grandes: tamaño de lote menor (50-100)
- Programe las exportaciones en períodos de bajo uso
- Monitoree la E/S de disco durante las operaciones de exportación

Recomendaciones de Seguridad
------------------------------

- Establezca permisos de archivo apropiados en el directorio de exportación
- No exponga el directorio de exportación directamente a la web
- Considere cifrar el contenido exportado si contiene información sensible
- Audite regularmente el acceso a los archivos exportados

Solución de Problemas
=====================

El Trabajo de Exportación No Se Ejecuta
-----------------------------------------

1. Verifique que el trabajo esté habilitado en el Programador
2. Compruebe la sintaxis de la expresión cron
3. Revise los registros de |Fess| en busca de mensajes de error:

::

    tail -f /var/log/fess/fess.log | grep IndexExport

Directorio de Exportación Vacío
---------------------------------

1. Confirme que existen documentos en el índice
2. Verifique los permisos de la ruta de exportación
3. Compruebe que el filtro de consulta (si es personalizado) coincida con documentos

::

    # Verificar el conteo de documentos en el índice
    curl -X GET "localhost:9201/fess.search/_count?pretty"

La Exportación Falla a Mitad de Proceso
-----------------------------------------

1. Verifique el espacio en disco disponible
2. Revise los registros en busca de errores de memoria o de tiempo de espera
3. Considere reducir ``scroll.size`` para documentos de gran tamaño
4. Verifique la configuración del tiempo de espera del contexto de scroll de OpenSearch

Archivos No Accesibles
------------------------

1. Verifique los permisos de archivo: ``ls -la /var/lib/fess/export``
2. Compruebe que el propietario del directorio coincida con el usuario del proceso |Fess|
3. Confirme que las políticas de SELinux o AppArmor permitan el acceso

Temas Relacionados
==================

- :doc:`admin-index-backup` - Procedimientos de copia de seguridad y restauración del índice
- :doc:`admin-logging` - Configuración del registro para la solución de problemas
