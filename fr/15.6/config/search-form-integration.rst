==============
Placement du formulaire de recherche
==============

Méthode de placement du formulaire de recherche
=================

En plaçant un formulaire de recherche sur un site existant, vous pouvez rediriger vers les résultats de recherche de |Fess|.
Ici, nous expliquons avec un exemple où |Fess| est configuré sur https://search.n2sm.co.jp/ et où un formulaire de recherche est placé sur chaque page d'un site existant.

Formulaire de recherche
---------

Placez le code suivant à l'endroit où vous souhaitez afficher le formulaire de recherche sur la page.

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="Rechercher">
    </form>

Ajustez selon les besoins avec CSS en ajoutant un nom de classe avec l'attribut class pour correspondre au design de votre site.
Modifiez l'URL https://search.n2sm.co.jp/ avec l'URL de votre serveur |Fess| configuré.


Suggestions
--------

Vous pouvez également configurer la fonction de suggestion dans le formulaire de recherche placé.
Pour configurer cela, ajoutez le code suivant avant </body>.

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

Si vous utilisez déjà jQuery sur votre site, il n'est pas nécessaire d'ajouter l'élément script jQuery.

Pour la valeur spécifiée dans "z-index", veuillez spécifier une valeur qui ne chevauche pas avec d'autres éléments.
