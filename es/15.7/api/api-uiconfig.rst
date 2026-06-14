===========================================
API de configuración de interfaz de usuario
===========================================

Descripción general
===================

La API de configuración de interfaz de usuario devuelve la configuración inicial que necesita una aplicación de página única (SPA): tema, indicadores de características, límite de paginación y, cuando se requiere CSRF, un nuevo token CSRF.
Este endpoint se llama de forma anónima antes del inicio de sesión.

Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

Obtención de la configuración de interfaz de usuario
=====================================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/ui/config``
==================  ====================================================

Devuelve la configuración inicial que necesita la SPA.

Respuesta
---------

En caso de éxito (HTTP 200, UiConfigResponse), se devuelve una respuesta con el formato de sobre común como la siguiente (extracto):

.. code-block:: json

    {
      "response": {
        "status": 0,
        "site_name": "Fess",
        "login_required": false,
        "locales": ["en", "ja"],
        "theme": {
          "name": "default",
          "display_name": "Default Theme",
          "version": "1.0.0",
          "supported_locales": ["en", "ja"]
        },
        "features": {
          "user_favorite": false,
          "popular_word": true,
          "suggest_search_log": true,
          "suggest_documents": true,
          "login_required": false,
          "eoled": false,
          "development_mode": false,
          "search_log_enabled": true,
          "thumbnail_enabled": true,
          "display_label_type": false,
          "clipboard_copy_icon": true,
          "eol_link": "",
          "installation_link": "https://fess.codelibs.org/15.7/install/",
          "login_link": true,
          "rag_chat_enabled": false
        },
        "page_size_default": 20,
        "page_size_max": 100,
        "sort_options": [
          {"value": "", "label_key": "labels.search_result_sort_score_desc"}
        ],
        "num_options": [10, 20, 30, 40, 50, 100],
        "lang_options": [
          {"value": "all", "label_key": "labels.searchoptions_all_langs"},
          {"value": "ja", "label_key": "labels.lang_ja"}
        ],
        "label_options": [],
        "notifications": {
          "search_top": "",
          "advance_search": "",
          "login": ""
        },
        "facet_views": [],
        "filetype_options": [
          {"value": "html", "label_key": "labels.facet_filetype_html"}
        ],
        "csrf_required": true,
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f"
      }
    }

Los elementos de ``response`` son los siguientes. Todos los campos son obligatorios.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Información de respuesta
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Descripción
   * - ``site_name``
     - string
     - Nombre del sitio.
   * - ``login_required``
     - boolean
     - Si se requiere inicio de sesión.
   * - ``locales``
     - string[]
     - Array de configuraciones regionales disponibles.
   * - ``theme``
     - object
     - Descriptor del tema activo. Consulte la tabla siguiente para más detalles.
   * - ``features``
     - object
     - Indicadores de características. Consulte la tabla siguiente para más detalles.
   * - ``page_size_default``
     - integer
     - Tamaño de página predeterminado.
   * - ``page_size_max``
     - integer
     - Tamaño máximo de página.
   * - ``sort_options``
     - object[]
     - Opciones de ordenación para la interfaz de búsqueda. Consulte la tabla siguiente para más detalles.
   * - ``num_options``
     - integer[]
     - Array de tamaños de página seleccionables. Se limita a valores que no superen ``page_size_max``.
   * - ``lang_options``
     - object[]
     - Opciones para el filtro de idioma. Consulte la tabla siguiente para más detalles.
   * - ``label_options``
     - object[]
     - Opciones para las etiquetas configuradas. Consulte la tabla siguiente para más detalles.
   * - ``notifications``
     - object
     - Fragmentos HTML de notificación que se muestran en la parte superior de vistas específicas. Consulte la tabla siguiente para más detalles.
   * - ``facet_views``
     - object[]
     - Grupos de vistas de consultas de faceta configurados. Consulte la tabla siguiente para más detalles.
   * - ``filetype_options``
     - object[]
     - Opciones de faceta de tipo de archivo para el formulario de búsqueda avanzada. Consulte la tabla siguiente para más detalles.
   * - ``csrf_required``
     - boolean
     - Si se requiere token CSRF.
   * - ``csrf_token``
     - string
     - Cadena vacía cuando ``csrf_required`` es ``false``; en caso contrario, el nuevo token asociado a la sesión actual.

theme
~~~~~

``theme`` siempre existe, pero es un objeto vacío cuando no hay un tema personalizado asociado a la solicitud.
Las claves derivadas del manifiesto (``display_name`` / ``version`` / ``supported_locales``) solo existen cuando el tema activo incluye un manifiesto.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: theme
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``name``
     - string
     - Nombre del tema.
   * - ``display_name``
     - string
     - Nombre para mostrar del tema.
   * - ``version``
     - string
     - Versión del tema.
   * - ``supported_locales``
     - string[]
     - Array de configuraciones regionales admitidas por el tema.

features
~~~~~~~~

Todos los campos son obligatorios.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: features
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``user_favorite``
     - boolean
     - Si la función de favoritos de usuario está habilitada.
   * - ``popular_word``
     - boolean
     - Si la función de palabras populares está habilitada.
   * - ``suggest_search_log``
     - boolean
     - Si las sugerencias basadas en el registro de búsqueda están habilitadas.
   * - ``suggest_documents``
     - boolean
     - Si las sugerencias basadas en documentos están habilitadas.
   * - ``login_required``
     - boolean
     - Si se requiere inicio de sesión.
   * - ``eoled``
     - boolean
     - Si esta compilación de |Fess| ha alcanzado el fin de vida útil (EOL).
   * - ``development_mode``
     - boolean
     - ``true`` cuando se utiliza el motor de búsqueda integrado (para desarrollo).
   * - ``search_log_enabled``
     - boolean
     - Si el registro de búsqueda está habilitado.
   * - ``thumbnail_enabled``
     - boolean
     - Si las miniaturas están habilitadas.
   * - ``display_label_type``
     - boolean
     - ``true`` cuando hay una o más etiquetas configuradas.
   * - ``clipboard_copy_icon``
     - boolean
     - Si se muestra el icono de copiar al portapapeles.
   * - ``eol_link``
     - string
     - URL resuelta de información de EOL. Cadena vacía si no está en EOL o no se puede resolver.
   * - ``installation_link``
     - string
     - URL resuelta de la guía de instalación. Cadena vacía si no se puede resolver.
   * - ``login_link``
     - boolean
     - Si se debe mostrar el enlace de inicio de sesión.
   * - ``rag_chat_enabled``
     - boolean
     - Si la función de chat RAG está disponible.

sort_options
~~~~~~~~~~~~

Array de opciones de ordenación para la interfaz de búsqueda.
Cada elemento tiene ``value`` y ``label_key``.
Los elementos ``click_count.*`` solo existen cuando el registro de búsqueda está habilitado; los elementos ``favorite_count.*`` solo existen cuando los favoritos de usuario están habilitados.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elementos de sort_options
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``value``
     - string
     - Valor de ordenación.
   * - ``label_key``
     - string
     - Clave de etiqueta.

num_options
~~~~~~~~~~~

Array de enteros con los tamaños de página seleccionables. Se limita a valores que no superen ``page_size_max``.

lang_options
~~~~~~~~~~~~

Array de opciones para el filtro de idioma.
Cada elemento tiene ``value`` y ``label_key``.
El primer elemento es el centinela ``all``, seguido de un elemento por cada código de idioma admitido.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elementos de lang_options
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``value``
     - string
     - Valor de idioma.
   * - ``label_key``
     - string
     - Clave de etiqueta.

label_options
~~~~~~~~~~~~~

Array de opciones para las etiquetas configuradas. Devuelve un array vacío cuando no hay etiquetas definidas.
Cada elemento tiene ``value`` y ``name``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elementos de label_options
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``value``
     - string
     - Valor de etiqueta.
   * - ``name``
     - string
     - Nombre de etiqueta.

notifications
~~~~~~~~~~~~~

Fragmentos HTML de notificación que se muestran en la parte superior de vistas específicas. Una cadena vacía significa que no hay notificación para esa vista.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: notifications
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``search_top``
     - string
     - Notificación que se muestra en la página principal de búsqueda.
   * - ``advance_search``
     - string
     - Notificación que se muestra en la búsqueda avanzada.
   * - ``login``
     - string
     - Notificación que se muestra en el inicio de sesión.

facet_views
~~~~~~~~~~~

Array de grupos de vistas de consultas de faceta configurados. Devuelve un array vacío cuando no está definido.
Cada elemento tiene ``group_name`` y ``queries``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elementos de facet_views
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``group_name``
     - string
     - Nombre del grupo.
   * - ``queries``
     - object[]
     - Array de consultas de faceta de ese grupo. Cada elemento tiene ``label_key`` (string) y ``value`` (string).

filetype_options
~~~~~~~~~~~~~~~~

Array de opciones de faceta de tipo de archivo para el formulario de búsqueda avanzada.
Cada elemento tiene ``value`` y ``label_key``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elementos de filetype_options
   :header-rows: 1
   :widths: 28 15 57

   * - Campo
     - Tipo
     - Descripción
   * - ``value``
     - string
     - Valor del tipo de archivo.
   * - ``label_key``
     - string
     - Clave de etiqueta.

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error
   :header-rows: 1
   :widths: 25 75

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.
