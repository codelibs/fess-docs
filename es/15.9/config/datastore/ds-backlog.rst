==================================
Conector de Backlog
==================================

Visión General
==============

El conector de Backlog proporciona funcionalidad para obtener incidencias, páginas Wiki, documentos y archivos de un espacio de Backlog
y registrarlos en el índice de |Fess|.
Se autentica en el espacio con una clave de API.
Cada documento indexado queda restringido a los miembros de su proyecto de Backlog (consulte «Permisos» más adelante).

Esta funcionalidad requiere el plugin ``fess-ds-backlog``.

Contenido Soportado
===================

- Incidencias (con sus comentarios)
- Páginas Wiki
- Documentos
- Archivos adjuntos de incidencias, páginas Wiki y documentos
- Archivos compartidos de un proyecto

Cada rastreo es un rastreo completo. De forma predeterminada, los documentos que han desaparecido de Backlog no se eliminan
al final del rastreo; se eliminan cuando vencen (consulte «Contenido Eliminado y Acceso Revocado»).

Requisitos Previos
==================

1. Se requiere la instalación del plugin
2. Se requiere un usuario de Backlog dedicado y su clave de API
3. El usuario debe ser miembro de cada proyecto que se va a rastrear

Instalación del Plugin
----------------------

Instale desde "Sistema" -> "Plugins" en la pantalla de administración, o ejecute ``bin/fess-setup install plugin fess-ds-backlog``
y reinicie |Fess|.
Consulte :doc:`../../admin/plugin-guide` para más detalles.

Configuración en Backlog
------------------------

1. Cree un usuario de Backlog dedicado al rastreo y emita una clave de API para él («Configuración personal» -> «API»).
   El rastreo ve exactamente lo que ve este usuario.
2. Agregue el usuario a cada proyecto que se va a rastrear. El conector no solicita los proyectos a los que el usuario no se ha unido,
   aunque el usuario sea administrador del espacio.
3. Asigne al usuario un rol sin restricciones (Administrador o Usuario normal). Con un rol restringido,
   Backlog responde con HTTP 403 en algunas funciones: un usuario de «solo lectura» no puede descargar los adjuntos de las incidencias,
   y solo los usuarios sin restricciones pueden descargar los archivos compartidos.
   Ante un 403 de este tipo, el conector registra una advertencia por proyecto y función, omite esa función para ese proyecto
   (adjuntos de incidencias, adjuntos de Wiki, adjuntos de documentos o archivos compartidos) y continúa con el resto.
4. Si el espacio exige autenticación de dos factores para el acceso a la API, Backlog responde con el código de error 12
   (RequiredMFAError) y el rastreo se aborta.

La clave de API se envía únicamente en el encabezado de solicitud ``Backlog-API-Key``. No se pasa al script,
este conector no la escribe en el log, y no se siguen las redirecciones HTTP, por lo que la clave nunca sale del host del espacio.

.. warning::

   No habilite el registro ``FINE`` del logger ``org.codelibs.curl``. El cliente HTTP registra los encabezados de las solicitudes en ese nivel
   y solo enmascara los encabezados del estilo de ``Authorization`` y ``Cookie``, por lo que el encabezado ``Backlog-API-Key`` se escribiría en el log.

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
     - Company Backlog
   * - Nombre del manejador
     - BacklogDataStore
   * - Permisos
     - (déjelo vacío; consulte «Permisos»)
   * - Habilitado
     - Activado

Configuración de Parámetros
---------------------------

::

    api_key=**********************************************
    space_url=https://example.backlog.com

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``api_key``
     - Sí
     - La clave de API de Backlog. No se pasa al script y no se registra en el log
   * - ``space_url``
     - Sí
     - La URL del espacio, por ejemplo ``https://example.backlog.com``. Solo se acepta ``https`` y solo pueden indicarse el esquema y el host (se ignora una barra final). Un valor ausente, mal formado o ``http`` aborta el rastreo
   * - ``project_keys``
     - No
     - Claves de proyecto que se rastrean, separadas por comas (no distingue mayúsculas de minúsculas). Si está vacío, se rastrean todos los proyectos que el usuario puede ver. Una clave que el usuario no puede ver se registra como advertencia
   * - ``include_archived``
     - No
     - Rastrear también los proyectos archivados (predeterminado: ``false``)
   * - ``include_issues``
     - No
     - Indexar las incidencias (predeterminado: ``true``)
   * - ``include_comments``
     - No
     - Incorporar los comentarios de las incidencias al documento de la incidencia (predeterminado: ``true``)
   * - ``include_wikis``
     - No
     - Indexar las páginas Wiki, en los proyectos en los que el Wiki está habilitado (predeterminado: ``true``)
   * - ``include_documents``
     - No
     - Indexar los documentos, en los proyectos en los que los documentos están habilitados (predeterminado: ``true``)
   * - ``include_attachments``
     - No
     - Descargar e indexar los adjuntos de incidencias, páginas Wiki y documentos (predeterminado: ``true``)
   * - ``include_shared_files``
     - No
     - Descargar e indexar los archivos compartidos, en los proyectos en los que el uso compartido de archivos está habilitado (predeterminado: ``true``)
   * - ``permission_sync``
     - No
     - Dar a cada documento de un proyecto un rol ``{user}`` por cada miembro del proyecto (predeterminado: ``true``). Consulte «Permisos»
   * - ``default_permissions``
     - No
     - Permisos separados por comas (``{user}name``, ``{group}name`` o ``{role}name``) que se añaden a cada documento
   * - ``max_file_size``
     - No
     - Los archivos mayores que este número de bytes se omiten y no se indexan (predeterminado: ``10485760``)
   * - ``include_pattern``
     - No
     - Expresión regular que debe cumplir ``backlog.url`` para indexarse
   * - ``exclude_pattern``
     - No
     - Expresión regular que no debe cumplir ``backlog.url``. Cuando se filtra una incidencia, una página Wiki o un documento, también se omiten sus adjuntos
   * - ``request_interval``
     - No
     - Milisegundos de espera antes de cada solicitud a la API (predeterminado: ``200``)
   * - ``search_request_interval``
     - No
     - Milisegundos mínimos entre dos solicitudes de tipo búsqueda (lista de incidencias, lista de Wiki). Backlog pide a los clientes que dejen al menos un segundo entre ellas (predeterminado: ``1000``)
   * - ``max_retry_count``
     - No
     - Número de reintentos ante HTTP 429, 5xx y fallos de conexión (predeterminado: ``5``)
   * - ``connection_timeout``
     - No
     - Tiempo de espera de conexión en milisegundos (predeterminado: ``10000``)
   * - ``read_timeout``
     - No
     - Tiempo de espera de lectura en milisegundos (predeterminado: ``30000``)
   * - ``ignore_error``
     - No
     - Si falla la extracción de texto de un archivo descargado, indexar el archivo con contenido vacío en lugar de registrar un fallo (predeterminado: ``true``)

.. note::

   Un valor no válido (un valor no numérico, un intervalo o número de reintentos negativo, un tiempo de espera o ``max_file_size`` no positivo,
   o un booleano distinto de ``true``/``false``) se registra como advertencia y se usa el valor predeterminado.
   ``0`` es válido para ``request_interval``, ``search_request_interval`` y ``max_retry_count``.

Configuración de Script
-----------------------

::

    title=backlog.title
    content=backlog.content
    url=backlog.url
    mimetype=backlog.mimetype
    created=backlog.created
    last_modified=backlog.updated
    role=backlog.roles

.. important::

   ``role=backlog.roles`` es necesario para que la restricción a los miembros del proyecto surta efecto.
   Sin él, al índice llega únicamente el campo «Permisos» de la configuración del almacén de datos.

Campos Disponibles
~~~~~~~~~~~~~~~~~~

Todos los documentos se exponen al script bajo el objeto ``backlog``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Campo
     - Tipos
     - Descripción
   * - ``backlog.type``
     - todos
     - ``issue``, ``wiki``, ``document``, ``attachment`` o ``file``
   * - ``backlog.id``
     - todos
     - El ID de Backlog de la incidencia, página Wiki, documento, adjunto o archivo compartido
   * - ``backlog.project_key``, ``backlog.project_name``
     - todos
     - El proyecto
   * - ``backlog.title``
     - todos
     - ``[KEY-1] resumen`` en una incidencia; en los demás casos, el nombre de la página, el título del documento o el nombre del archivo
   * - ``backlog.content``
     - todos
     - Incidencia: descripción, atributos, campos personalizados y comentarios. Página Wiki: el contenido de la página. Documento: texto plano. Adjunto y archivo: el texto extraído
   * - ``backlog.url``
     - todos
     - Consulte «URL»
   * - ``backlog.mimetype``
     - todos
     - ``text/plain`` para incidencias, páginas Wiki y documentos; el tipo detectado para los archivos
   * - ``backlog.created``, ``backlog.updated``
     - todos
     - Fechas ISO 8601 en UTC, cuando Backlog las devuelve
   * - ``backlog.created_by``, ``backlog.updated_by``
     - todos
     - Nombres de usuario, cuando Backlog los devuelve
   * - ``backlog.roles``
     - todos
     - Los roles de búsqueda (consulte «Permisos»)
   * - ``backlog.issue_key``, ``backlog.issue_type``, ``backlog.status``, ``backlog.priority``, ``backlog.assignee``
     - incidencia
     - Atributos de la incidencia (nombres)
   * - ``backlog.categories``, ``backlog.milestones``, ``backlog.versions``
     - incidencia
     - Listas de nombres
   * - ``backlog.custom_fields``
     - incidencia
     - Mapa de nombre de campo personalizado a texto del valor
   * - ``backlog.comments``
     - incidencia
     - Texto de los comentarios con la forma ``autor: contenido``, separados por líneas en blanco
   * - ``backlog.tags``
     - página Wiki, documento
     - Lista de nombres de etiquetas
   * - ``backlog.parent_type``, ``backlog.parent_url``, ``backlog.parent_title``
     - adjunto
     - La incidencia, página Wiki o documento al que pertenece el adjunto
   * - ``backlog.size``
     - adjunto, archivo
     - Tamaño descargado en bytes
   * - ``backlog.path``
     - archivo
     - Ruta del archivo compartido, por ejemplo ``/docs/spec.pdf``

URL
---

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Tipo
     - URL
   * - incidencia
     - ``{space_url}/view/{ISSUE-KEY}``
   * - página Wiki
     - ``{space_url}/alias/wiki/{ID}``
   * - documento
     - ``{space_url}/document/{PROJECT}/{ID}``
   * - archivo
     - ``{space_url}/file/{PROJECT}{directorio}{nombre}`` (cada segmento de la ruta se codifica con porcentaje)
   * - adjunto
     - ``{URL del elemento padre}#attachment-{ID}``

.. note::

   Las formas de URL de los documentos y archivos compartidos, y el endpoint de descarga de los adjuntos de documentos,
   no se han confirmado con un espacio de Backlog real. Si un enlace no abre la página esperada,
   el documento sigue indexado y es buscable; solo el destino del enlace es incorrecto.

Permisos
========

Con ``permission_sync=true`` (predeterminado), cada documento de un proyecto recibe los siguientes roles:

- un rol ``{user}`` para el ``mailAddress`` y otro para el ``userId`` de cada miembro del proyecto
  (los valores vacíos se omiten), de modo que un miembro puede iniciar sesión en |Fess| con cualquiera de los dos
- el valor de ``default_permissions``
- el valor del campo «Permisos» de la configuración del almacén de datos

Si no se pueden obtener los miembros del proyecto, o ninguno de ellos tiene un ``mailAddress`` o ``userId`` utilizable,
se omite todo el proyecto y se registra en "Rastreador" -> "URL de fallo". Nunca se indexa sin los roles de sus miembros.

Con ``permission_sync=false``, solo se aplican ``default_permissions`` y el campo «Permisos».

.. warning::

   Vacíe el campo «Permisos» de la configuración del almacén de datos. La pantalla de administración lo rellena de antemano con ``{role}guest``,
   que tienen todos los usuarios, incluidos los buscadores anónimos. Si se deja, se combina con los roles de cada documento
   y todo el contenido de Backlog pasa a ser buscable por todos.
   Con ``permission_sync=true``, el conector registra una advertencia por proyecto cuando un rol de invitado acaba entre sus roles.

Qué conviene saber antes de confiar en los roles de los miembros:

- El identificador de un miembro es un nombre de inicio de sesión de |Fess|. Un ``userId`` de Backlog como ``tanaka`` concede acceso al inicio de sesión de |Fess| llamado ``tanaka``,
  que no tiene por qué ser la misma persona (por ejemplo, un nombre de cuenta de LDAP o Active Directory). El rol basado en ``mailAddress`` no tiene este problema.
  Use ``permission_sync`` solo cuando los nombres de inicio de sesión de |Fess| sean los ID de usuario o las direcciones de correo de Backlog.
- Un miembro cuyo identificador se correspondería con el rol de invitado o con otro inicio de sesión se ignora, con una advertencia que nombra el proyecto y el ID del miembro:
  un ``userId`` ``guest`` y cualquier identificador que contenga una barra invertida (|Fess| elimina de un nombre de usuario todo lo anterior a la barra invertida).
- Todos los miembros del proyecto pueden encontrar cualquier elemento indexado del proyecto, incluidos los adjuntos y archivos compartidos, incluso cuando el propio Backlog
  le negaría la descarga a ese miembro (un usuario de «solo lectura» no puede descargar los adjuntos de las incidencias). Los roles son por proyecto, no por función.

Contenido Eliminado y Acceso Revocado
=====================================

De forma predeterminada, |Fess| asigna a cada documento una fecha de expiración (el ajuste «Eliminar documentos anteriores» de General, tres días de forma predeterminada)
y no elimina al final de un rastreo los documentos que la tienen. Los documentos vencidos los elimina el Doc Purger. Por tanto, de forma predeterminada:

- el contenido eliminado en Backlog sigue siendo buscable durante unos tres días como máximo
- cuando un miembro abandona un proyecto, conserva el acceso a los documentos ya indexados del proyecto durante unos tres días como máximo.
  El siguiente rastreo los indexa de nuevo con nuevos ID de documento (el ID incluye la lista de roles), y las copias antiguas, con los roles antiguos,
  permanecen hasta que vencen. Durante ese tiempo, los miembros restantes ven resultados duplicados

Para eliminar esos documentos al final del rastreo, añada ``keep_expires_docs=false`` a los parámetros de la configuración del almacén de datos.
|Fess| elimina entonces todos los documentos de esa configuración que el rastreo no reindexó, lo que también se aplica a todo lo que el rastreo no alcanzó (consulte «Manejo de Errores»).

Ejemplos de Uso
===============

Rastrear proyectos concretos
----------------------------

Parámetros:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    project_keys=PROJ,DOCS
    include_shared_files=false

Solo incidencias y páginas Wiki, sin adjuntos
---------------------------------------------

Parámetros:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    include_documents=false
    include_attachments=false
    include_shared_files=false

Eliminar al final del rastreo los documentos borrados en Backlog
----------------------------------------------------------------

Parámetros:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    keep_expires_docs=false

Manejo de Errores
=================

- El rastreo se aborta solo ante HTTP ``401``, el código de error de Backlog 11 (AuthenticationError) o 12 (RequiredMFAError),
  un ``api_key`` o ``space_url`` ausente o mal formado, o un fallo al listar los proyectos.
- Ante HTTP ``429``, la solicitud espera hasta el momento indicado por el encabezado ``X-RateLimit-Reset`` (como máximo 120 segundos; 60 segundos si falta el encabezado) y se reintenta.
  Ante HTTP ``5xx`` y fallos de conexión, la solicitud se reintenta con retroceso exponencial (1 segundo, 2 segundos, 4 segundos, hasta 60 segundos).
  Cuando se agotan los ``max_retry_count`` reintentos, ese elemento falla.
- Cualquier otro fallo (``403``, ``404``, reintentos agotados) se registra para ese único elemento y el rastreo continúa.
- Un elemento fallido no hace fallar el trabajo de rastreo. Tras un rastreo, revise "Rastreador" -> "URL de fallo" y el log del rastreador.
- Con ``keep_expires_docs=false``, el contenido bajo un fallo no se reindexa y por tanto se elimina al final de ese rastreo:
  todo lo que cuelga de un listado fallido, de un proyecto omitido o de una función omitida por un 403 desaparece del índice hasta que un rastreo posterior se complete sin ese fallo.
  Lo mismo ocurre con un rastreo que se aborta. De forma predeterminada, ese contenido sigue siendo buscable hasta que vence.

Solución de Problemas
=====================

El rastreo se aborta al iniciarse
---------------------------------

1. Compruebe que ``api_key`` es correcta y se emitió para un usuario de este espacio
2. Compruebe que ``space_url`` es una URL ``https`` solo con el host, como ``https://example.backlog.com``
3. Si el espacio exige autenticación de dos factores para el acceso a la API, el rastreo se aborta con RequiredMFAError

Un proyecto no se indexa
------------------------

1. Compruebe que el usuario de la API es miembro del proyecto
2. Con ``permission_sync=true``, se omite un proyecto cuyos miembros no se pueden obtener, o ninguno de los cuales tiene una dirección de correo o un ID de usuario utilizable. Consulte "Rastreador" -> "URL de fallo"
3. Revise ``project_keys`` y ``include_archived``

Faltan adjuntos o archivos compartidos
--------------------------------------

Asigne al usuario de la API un rol sin restricciones. El log contiene una advertencia por cada proyecto y función omitidos ante un HTTP 403.

Información de Referencia
=========================

- :doc:`ds-overview` - Visión general de conectores de almacén de datos
- :doc:`ds-atlassian` - Conector de Atlassian
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
- :doc:`../../admin/failureurl-guide` - URL de fallo
- :doc:`../../admin/plugin-guide` - Guía de gestión de plugins
- `Backlog API Documentation <https://developer.nulab.com/docs/backlog/>`_
