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
    <input type="submit" name="search" value="検索">
    </form>

Para que coincida con el diseño de su sitio, agregue nombres de clase con el atributo class y ajuste el estilo según sea necesario usando CSS.
Cambie la URL https://search.n2sm.co.jp/ a la URL del servidor |Fess| que haya configurado.


Sugerencias
-----------

También puede habilitar la funcionalidad de sugerencias en el formulario de búsqueda integrado.
Para configurarlo, agregue el siguiente código antes de </body>.

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.6.3.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v1/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "-webkit-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "-moz-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
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

Especifique un valor para "z-index" que no se superponga con otros elementos.
