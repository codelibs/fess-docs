=====================================
Función de Exportación de Índice
=====================================

Descripción General
===================

La función de Exportación de Índice le permite exportar documentos de búsqueda indexados en OpenSearch a archivos HTML en el sistema de archivos local. Esta funcionalidad es útil para:

- Crear copias de seguridad estáticas del contenido indexado
- Generar copias sin conexión de documentos para fines de archivo
- Construir páginas de resultados de búsqueda estáticas
- Migración de contenido a otros sistemas

Los archivos exportados mantienen la estructura de ruta URL original de los documentos de origen, lo que facilita la navegación y gestión del contenido exportado.

Cómo Funciona
=============

Cuando se ejecuta el trabajo de Exportación de Índice, realiza el siguiente proceso:

1. **Consultar documentos**: Recupera documentos de OpenSearch utilizando la API de scroll para procesamiento por lotes eficiente
2. **Procesar contenido**: Extrae campos del documento (título, contenido, URL, etc.)
3. **Crear estructura de directorios**: Replica la estructura de ruta URL en el directorio de exportación
4. **Generar archivos HTML**: Crea archivos HTML que contienen el contenido del documento
5. **Continuar hasta completar**: Procesa todos los documentos en lotes hasta que el índice esté completamente exportado

La API de scroll asegura un manejo eficiente de grandes conjuntos de documentos sin problemas de memoria.

Propiedades de Configuración
============================

Configure la función de Exportación de Índice en ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Propiedad
     - Valor Predeterminado
     - Descripción
   * - ``index.export.path``
     - ``/var/fess/export``
     - Directorio donde se almacenan los archivos exportados
   * - ``index.export.exclude.fields``
     - ``cache``
     - Lista de campos a excluir separados por comas
   * - ``index.export.scroll.size``
     - ``100``
     - Número de documentos procesados por lote

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
3. Encuentre **Index Export Job** en la lista de trabajos
4. Haga clic para editar la configuración del trabajo
5. Establezca el horario usando una expresión cron
6. Guarde la configuración

Ejemplos de expresiones cron:

- ``0 0 2 * * ?`` - Ejecutar diariamente a las 2:00 AM
- ``0 0 3 ? * SUN`` - Ejecutar cada domingo a las 3:00 AM
- ``0 0 0 1 * ?`` - Ejecutar el primer día de cada mes a medianoche

Filtrado de Consultas Personalizadas
====================================

Puede personalizar el trabajo de exportación para exportar solo documentos específicos modificando el script del trabajo.

Para agregar un filtro de consulta personalizado:

1. Navegue a **Sistema** > **Programador**
2. Edite el **Index Export Job**
3. Modifique el script del trabajo para incluir un filtro de consulta

Ejemplo de script con filtro de fecha:

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "created:>=now-7d"
    job.execute()

Ejemplo de script con filtro de sitio:

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "url:*example.com*"
    job.execute()

Estructura de Archivos Exportados
=================================

Los archivos exportados se organizan para reflejar la estructura URL original.

Por ejemplo, un documento con URL ``https://example.com/docs/guide/intro.html`` se exportaría a:

::

    /var/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

Cada archivo HTML exportado contiene:

- Título del documento
- Cuerpo del contenido principal
- Metadatos (fecha de última modificación, tipo de contenido, etc.)
- Referencia a la URL original

Mejores Prácticas
=================

Consideraciones de Almacenamiento
---------------------------------

- Asegure suficiente espacio en disco en el directorio de exportación
- Considere usar almacenamiento dedicado para grandes conjuntos de documentos
- Implemente limpieza regular de exportaciones antiguas si ejecuta exportaciones periódicas

Consejos de Rendimiento
-----------------------

- Ajuste ``index.export.scroll.size`` según el tamaño del documento:
  - Documentos más pequeños: tamaño de lote mayor (200-500)
  - Documentos más grandes: tamaño de lote menor (50-100)
- Programe exportaciones durante períodos de bajo uso
- Monitoree E/S de disco durante operaciones de exportación

Recomendaciones de Seguridad
----------------------------

- Establezca permisos de archivo apropiados en el directorio de exportación
- No exponga el directorio de exportación directamente a la web
- Considere encriptar el contenido exportado si contiene información sensible
- Audite regularmente el acceso a los archivos exportados

Solución de Problemas
=====================

El Trabajo de Exportación No Se Ejecuta
---------------------------------------

1. Verifique que el trabajo esté habilitado en el Programador
2. Revise la sintaxis de la expresión cron
3. Revise los registros de |Fess| en busca de mensajes de error:

::

    tail -f /var/log/fess/fess.log | grep IndexExport

Directorio de Exportación Vacío
-------------------------------

1. Confirme que existen documentos en el índice
2. Verifique los permisos de la ruta de exportación
3. Verifique que el filtro de consulta (si es personalizado) coincida con documentos

::

    # Verificar conteo de documentos en el índice
    curl -X GET "localhost:9201/fess.YYYYMMDD/_count?pretty"

La Exportación Falla a Mitad de Camino
--------------------------------------

1. Verifique el espacio en disco disponible
2. Revise los registros en busca de errores de memoria o tiempo de espera
3. Considere reducir ``scroll.size`` para documentos grandes
4. Verifique la configuración de tiempo de espera del contexto de scroll de OpenSearch

Archivos No Accesibles
----------------------

1. Verifique los permisos de archivo: ``ls -la /var/fess/export``
2. Verifique que el propietario del directorio coincida con el usuario del proceso |Fess|
3. Confirme que las políticas de SELinux o AppArmor permitan el acceso

Temas Relacionados
==================

- :doc:`admin-index-backup` - Procedimientos de respaldo y restauración de índices
- :doc:`admin-logging` - Configuración de ajustes de registro para solución de problemas
