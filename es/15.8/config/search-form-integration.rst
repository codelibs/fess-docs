========================================
Integración de Formulario de Búsqueda
========================================

Cómo Integrar un Formulario de Búsqueda
========================================

Al integrar un formulario de búsqueda en su sitio web existente, puede dirigir a los usuarios a los resultados de búsqueda de |Fess|.
Esta sección explica un ejemplo en el que |Fess| está instalado en https://search.n2sm.co.jp/ y se coloca un formulario de búsqueda en cada página del sitio existente.

Formulario de Búsqueda
----------------------

Coloque el siguiente código en la ubicación donde desea que aparezca el formulario de búsqueda en su página.

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="Buscar">
    </form>

Para que coincida con el diseño de su sitio, agregue nombres de clase con el atributo class y ajuste el estilo según sea necesario usando CSS.
Cambie la URL https://search.n2sm.co.jp/ a la URL del servidor |Fess| que haya configurado.

La palabra clave de búsqueda se envía como el parámetro ``q`` a la página de búsqueda de |Fess| (``/search/``).
Establezca ``maxlength`` en un valor que coincida con ``query.max.length`` (valor predeterminado ``1000``), que es la longitud máxima de la palabra clave en el lado de |Fess|.


Sugerencias
-----------

También puede habilitar la funcionalidad de sugerencias en el formulario de búsqueda integrado.
Para configurarlo, agregue el siguiente código antes de </body>.

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.7.1.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v2/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "background-color": "#fff",
          "z-index": "10000"
        },
        minterm: 2,
        adjustWidthVal : 11,
        searchForm : $('#searchForm')
      });
    });
    </script>

Si su sitio ya utiliza jQuery, no es necesario agregar el elemento script de jQuery.

La funcionalidad de sugerencias utiliza la API de sugerencias de |Fess| (``/api/v2/suggest-words``).
Cambie ``url`` para que coincida con la URL del servidor |Fess| que haya configurado.

Las principales opciones que se pueden especificar para ``suggestor`` son las siguientes.

.. list-table:: Principales opciones de suggestor
   :header-rows: 1
   :widths: 25 75

   * - Opción
     - Descripción
   * - ``ajaxinfo.url``
     - La URL de la API de sugerencias. Especifique ``/api/v2/suggest-words`` de su servidor |Fess|.
   * - ``ajaxinfo.fn``
     - Un arreglo de nombres de campos de los que obtener sugerencias. Puede usar el valor predeterminado ``["_default", "content", "title"]`` tal cual.
   * - ``ajaxinfo.num``
     - El número máximo de candidatos de sugerencia que se muestran.
   * - ``ajaxinfo.lang``
     - El idioma utilizado para acotar los candidatos de sugerencia (opcional).
   * - ``minterm``
     - El número mínimo de caracteres de entrada antes de solicitar sugerencias.
   * - ``adjustWidthVal``
     - El valor (en píxeles) que se suma al ancho del campo de entrada para ajustar el ancho del cuadro de sugerencias.
   * - ``searchForm``
     - El elemento del formulario de búsqueda que se envía cuando se selecciona un candidato.
   * - ``boxCssInfo``
     - El CSS aplicado al cuadro de sugerencias.
   * - ``listSelectedCssInfo``
     - El CSS aplicado al candidato seleccionado (opcional).
   * - ``listDeselectedCssInfo``
     - El CSS aplicado a los candidatos no seleccionados (opcional).

Especifique un valor para "z-index" que no se superponga con otros elementos.

.. note::
    Cuando el formulario de búsqueda se coloca en una página cuyo dominio difiere del servidor |Fess|, la solicitud a la API de sugerencias se convierte en una solicitud de origen cruzado (cross-origin).
    |Fess| permite todos los orígenes de forma predeterminada (``api.cors.allow.origin=*``), por lo que funciona tal cual.
    Para restringir el acceso, cambie ``api.cors.allow.origin`` en ``fess_config.properties``.

.. note::
    ``/api/v2/suggest-words`` es la API proporcionada por el propio |Fess|.
    El endpoint ``/api/v1/suggest-words`` utilizado en versiones anteriores ya no es proporcionado por el núcleo de |Fess|, y se debe instalar el complemento ``fess-webapp-v1-api`` para usarlo.
    Para nuevas instalaciones, utilice ``/api/v2/suggest-words``.
