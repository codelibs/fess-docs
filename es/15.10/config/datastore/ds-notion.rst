==================================
Conector de Notion
==================================

Visión General
==============

El conector de Notion proporciona funcionalidad para obtener páginas y filas de bases de datos de Notion
y registrarlas en el índice de |Fess|.
Se autentica como una integración interna de Notion e indexa todo lo que se ha compartido con esa integración.

Esta funcionalidad requiere el plugin ``fess-ds-notion``.

Contenido Soportado
===================

- Páginas (el texto de sus bloques)
- Filas de bases de datos, junto con los valores de sus propiedades
- Archivos adjuntos de bloques de archivo y PDF alojados en Notion (cada uno se indexa como un documento propio)
- Comentarios de página sin resolver (se incorporan al documento de la página)

Quedan fuera del alcance:

- Archivos que solo están enlazados desde Notion (archivos externos); solo se descargan los bloques ``file`` y ``pdf`` alojados en Notion
- Páginas y filas de bases de datos que están en la papelera de Notion
- Control de acceso por página (consulte «Permisos» más adelante)

Requisitos Previos
==================

1. Se requiere la instalación del plugin
2. Se requiere crear una integración interna de Notion
3. La integración debe compartirse con las páginas y bases de datos que se van a rastrear

Instalación del Plugin
----------------------

Instale desde "Sistema" -> "Plugins" en la pantalla de administración, o ejecute ``bin/fess-setup install plugin fess-ds-notion``
y reinicie |Fess|.
Consulte :doc:`../../admin/plugin-guide` para más detalles.

Configuración de la Integración de Notion
-----------------------------------------

1. Cree una integración interna en Notion y copie su «Internal Integration Secret».
2. En la página «Configuration» de la integración, habilite las siguientes capacidades:

   .. list-table::
      :header-rows: 1
      :widths: 25 25 50

      * - Capacidad
        - Requerida
        - Uso
      * - Read content
        - Siempre
        - Lectura de páginas, bloques, bases de datos y filas de bases de datos. Sin ella, todas las solicitudes fallan con ``401 unauthorized`` y el rastreo se aborta de inmediato
      * - Read comments
        - Solo si ``include_comments=true`` (predeterminado)
        - Obtención de los comentarios de la página. Si falta la capacidad, se registra una advertencia una sola vez y se desactiva el rastreo de comentarios durante el resto de ese rastreo; el rastreo en sí no falla
      * - Read user information
        - Opcional
        - Resolución de los ID de usuario (``created_by``, ``last_edited_by`` y las propiedades ``people``) a nombres visibles. Sin ella, se indexa el ID de usuario en lugar del nombre

3. Comparta la integración en Notion con cada página o base de datos que deba rastrearse.
   Agregar una capacidad por sí solo no concede acceso a ningún contenido.

Método de Configuración
=======================

Configure desde la pantalla de administración en "Rastreador" -> "Almacén de datos" -> "Nuevo".

Configuración Básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo
   * - Nombre
     - Company Notion
   * - Nombre del manejador
     - NotionDataStore
   * - Habilitado
     - Activado

Configuración de Parámetros
---------------------------

::

    token=secret_************************************

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``token``
     - Sí
     - El Internal Integration Secret. No se pasa al script y no se registra en el log
   * - ``root_page_ids``
     - No
     - ID de las páginas desde las que se inicia el rastreo, separados por comas. Si este parámetro y ``database_ids`` están vacíos, se descubren mediante la búsqueda de Notion todas las páginas y bases de datos compartidas con la integración
   * - ``database_ids``
     - No
     - ID de las bases de datos desde las que se inicia el rastreo, separados por comas. Se indexa cada fila de cada base de datos
   * - ``include_comments``
     - No
     - Obtener los comentarios sin resolver de cada página e incorporar su texto a ``notion.content`` y ``notion.comments`` (predeterminado: ``true``)
   * - ``include_files``
     - No
     - Descargar los adjuntos de bloques ``file`` y ``pdf`` alojados en Notion, extraer su texto e indexar cada uno como un documento propio (predeterminado: ``true``)
   * - ``max_file_size``
     - No
     - Un adjunto mayor que este número de bytes se omite por completo, sin indexarlo ni siquiera con contenido vacío (predeterminado: ``10485760``)
   * - ``include_pattern``
     - No
     - Expresión regular que debe cumplir el ``notion.url`` de un documento para indexarse (consulte «Alcance del Rastreo»)
   * - ``exclude_pattern``
     - No
     - Expresión regular que no debe cumplir el ``notion.url`` de un documento (consulte «Alcance del Rastreo»)
   * - ``request_interval``
     - No
     - Milisegundos de espera antes de cada solicitud a la API de Notion, para mantenerse por debajo del límite de frecuencia de Notion (unas 3 solicitudes por segundo) (predeterminado: ``350``)
   * - ``max_retry_count``
     - No
     - Número máximo de reintentos para una solicitud que termina en ``429``, ``5xx`` o ``529``, o en un fallo de transporte como un tiempo de espera agotado (predeterminado: ``5``)
   * - ``connection_timeout``
     - No
     - Tiempo de espera de conexión de cada solicitud a la API, en milisegundos (predeterminado: ``10000``)
   * - ``read_timeout``
     - No
     - Tiempo de espera de lectura de cada solicitud a la API, en milisegundos (predeterminado: ``30000``)
   * - ``ignore_error``
     - No
     - Si falla la extracción de texto de un adjunto que se descargó, indexar el adjunto con contenido vacío en lugar de hacer fallar el documento (predeterminado: ``true``). Un fallo de descarga hace fallar siempre el documento, independientemente de este ajuste

.. note::

   En un parámetro numérico, un valor vacío o no numérico vuelve a su valor predeterminado con una advertencia en el log.
   Lo mismo ocurre con un ``request_interval`` o ``max_retry_count`` negativo (``0`` es válido para ambos) y con un
   parámetro ``true``/``false`` establecido en cualquier otro valor.

Configuración de Script
-----------------------

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time
    created=notion.created_time

Campos Disponibles
~~~~~~~~~~~~~~~~~~

Todos los documentos, ya sean páginas, filas de bases de datos o adjuntos, se exponen al script bajo el objeto ``notion``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``notion.type``
     - ``page`` para una página o fila de base de datos, ``file`` para un adjunto
   * - ``notion.id``
     - El ID de la página o, en un adjunto, el ID del bloque
   * - ``notion.title``
     - El título de la página (la propiedad de tipo ``title``, sea cual sea su nombre) o el nombre de archivo de un adjunto
   * - ``notion.content``
     - En una página: los valores de las propiedades que no son el título (solo filas de bases de datos), el texto de sus bloques y el texto de los comentarios, unidos. En un adjunto: el texto extraído
   * - ``notion.url``
     - La URL de Notion de la página. En un adjunto, la URL de la página que lo contiene con ``#<ID del bloque>`` añadido
   * - ``notion.mimetype``
     - ``text/html`` para una página, el tipo MIME detectado para un adjunto
   * - ``notion.created_time``
     - Fecha de creación de la página. No disponible en un adjunto
   * - ``notion.last_edited_time``
     - Fecha de la última edición de la página o del bloque del adjunto
   * - ``notion.created_by``
     - Creador de la página: el nombre si Notion devolvió uno, de lo contrario el ID de usuario. No disponible en un adjunto
   * - ``notion.last_edited_by``
     - Último editor, con el mismo formato. No disponible en un adjunto
   * - ``notion.parent_id``
     - ID de la página, base de datos, fuente de datos o bloque padre. Vacío en una página situada directamente en el espacio de trabajo. No disponible en un adjunto
   * - ``notion.properties``
     - Mapa de nombre de columna a texto con formato, para una fila de base de datos. Vacío en una página normal. No disponible en un adjunto
   * - ``notion.comments``
     - El texto de los comentarios de la página, unido. Vacío con ``include_comments=false`` o si la página no tiene comentarios. No disponible en un adjunto
   * - ``notion.page_url``
     - URL de la página que contiene el adjunto. Solo en adjuntos
   * - ``notion.page_title``
     - Título de la página que contiene el adjunto. Solo en adjuntos
   * - ``notion.size``
     - Tamaño del adjunto en bytes, cuando Notion lo informó. Solo en adjuntos

Alcance del Rastreo
===================

- Si no se establece ni ``root_page_ids`` ni ``database_ids``, el conector usa la búsqueda de Notion para descubrir todas las páginas y bases de datos compartidas con la integración.
  Notion no garantiza que la búsqueda sea exhaustiva; si falta contenido en el índice, establezca ``root_page_ids`` o ``database_ids`` de forma explícita.
- Desde cada punto de partida también se rastrean todas las subpáginas y subbases de datos alcanzables, por lo que normalmente basta una sola página raíz para llegar a toda una sección de un espacio de trabajo.
- ``include_pattern`` y ``exclude_pattern`` solo deciden si se indexa el documento de esa página (o adjunto).
  Nunca impiden descubrir los descendientes: los bloques de una página se recorren siempre antes de comprobar el patrón contra la URL de la propia página,
  de modo que las subpáginas de una página excluida se rastrean igualmente y se indexan bajo sus propias URL.
  Para excluir un subárbol completo, el patrón debe coincidir con todas las URL que cuelgan de él, no solo con la raíz.
- Una página o fila de base de datos que está en la papelera de Notion se omite.

Permisos
========

La API de Notion no expone la configuración de uso compartido de una página, por lo que este conector no puede sincronizar el control de acceso por página.
Cada documento se indexa únicamente con los permisos establecidos en el campo «Permisos» de la configuración del almacén de datos.

.. warning::

   Todo lo que se comparte con la integración pasa a ser buscable por los roles concedidos en ese campo, con independencia de quién pueda verlo en Notion.
   Comparta la integración solo con las páginas y bases de datos que esos roles deban poder buscar.

Manejo de Errores
=================

- El rastreo se aborta solo ante HTTP ``401`` (el token no puede autenticarse) o ante una respuesta ``429`` que nombra ``public_api_request_blocked`` (el limitador de frecuencia de Notion está bloqueando la integración).
  El rastreo también se aborta si falla la búsqueda de Notion mientras no se ha establecido ni ``root_page_ids`` ni ``database_ids``, porque no hay punto de partida.
- Cualquier otro fallo se trata por documento: un ``404`` o ``403`` en una página, base de datos, hilo de comentarios o bloque, o agotar ``max_retry_count`` en una solicitud, se registra y se omite, y el rastreo continúa.
- Cada fallo por documento se registra en "Rastreador" -> "URL de fallo" con la URL de ese documento (la URL de Notion de una página, ``<URL de la página>#<ID del bloque>`` en un adjunto).
  La URL de descarga firmada de un adjunto nunca se registra ni se escribe en el log.
- Con ``keep_expires_docs=false`` en los parámetros, los documentos del almacén de datos que no se reindexaron en un rastreo se eliminan al final de este, incluido un rastreo que se aborta.
  De forma predeterminada, los documentos llevan una fecha de expiración y permanecen en el índice hasta que esta pasa.

Ejemplos de Uso
===============

Rastrear un árbol de páginas concreto
-------------------------------------

Parámetros:

::

    token=secret_************************************
    root_page_ids=0123456789abcdef0123456789abcdef
    include_comments=false

Script:

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time

Rastrear una base de datos
--------------------------

Parámetros:

::

    token=secret_************************************
    database_ids=fedcba9876543210fedcba9876543210
    include_files=false

Script:

::

    title=notion.title
    content=notion.content
    url=notion.url
    created=notion.created_time
    last_modified=notion.last_edited_time

Rastrear todo lo compartido con la integración
----------------------------------------------

Parámetros:

::

    token=secret_************************************
    request_interval=500

Solución de Problemas
=====================

El rastreo se aborta de inmediato con ``401``
---------------------------------------------

Compruebe que el token es el «Internal Integration Secret» de la integración y que la capacidad «Read content» está habilitada.

Faltan páginas en el índice
---------------------------

1. Compruebe que la integración se ha compartido con la página o base de datos
2. Si se basa en el descubrimiento automático, establezca ``root_page_ids`` o ``database_ids`` de forma explícita, porque la búsqueda de Notion no garantiza ser exhaustiva
3. Revise ``include_pattern`` y ``exclude_pattern``
4. Revise "Rastreador" -> "URL de fallo" para ver los documentos que fallaron individualmente

Los comentarios no se indexan
-----------------------------

Habilite la capacidad «Read comments» de la integración. Sin ella, se registra una advertencia una sola vez y los comentarios se omiten en ese rastreo.
Solo se indexan los comentarios sin resolver.

Información de Referencia
=========================

- :doc:`ds-overview` - Visión general de conectores de almacén de datos
- :doc:`ds-slack` - Conector de Slack
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
- :doc:`../../admin/failureurl-guide` - URL de fallo
- :doc:`../../admin/plugin-guide` - Guía de gestión de plugins
- `Notion API Documentation <https://developers.notion.com/>`_
