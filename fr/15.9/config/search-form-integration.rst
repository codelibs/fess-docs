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

Le mot-clé de recherche est envoyé en tant que paramètre ``q`` à la page de recherche de |Fess| (``/search/``).
Définissez ``maxlength`` sur une valeur qui correspond à ``query.max.length`` (valeur par défaut ``1000``), qui est la longueur maximale du mot-clé du côté de |Fess|.


Suggestions
--------

Vous pouvez également configurer la fonction de suggestion dans le formulaire de recherche placé.
Pour configurer cela, ajoutez le code suivant avant </body>.

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

Si vous utilisez déjà jQuery sur votre site, il n'est pas nécessaire d'ajouter l'élément script jQuery.

La fonction de suggestion utilise l'API de suggestion de |Fess| (``/api/v2/suggest-words``).
Modifiez ``url`` pour qu'elle corresponde à l'URL de votre serveur |Fess| configuré.

Les principales options pouvant être spécifiées pour ``suggestor`` sont les suivantes.

.. list-table:: Principales options de suggestor
   :header-rows: 1
   :widths: 25 75

   * - Option
     - Description
   * - ``ajaxinfo.url``
     - L'URL de l'API de suggestion. Spécifiez ``/api/v2/suggest-words`` de votre serveur |Fess|.
   * - ``ajaxinfo.fn``
     - Un tableau de noms de champs à partir desquels obtenir des suggestions. Vous pouvez utiliser la valeur par défaut ``["_default", "content", "title"]`` telle quelle.
   * - ``ajaxinfo.num``
     - Le nombre maximal de candidats de suggestion affichés.
   * - ``ajaxinfo.lang``
     - La langue utilisée pour affiner les candidats de suggestion (facultatif).
   * - ``minterm``
     - Le nombre minimal de caractères saisis avant que les suggestions ne soient demandées.
   * - ``adjustWidthVal``
     - La valeur (en pixels) ajoutée à la largeur du champ de saisie pour ajuster la largeur de la zone de suggestion.
   * - ``searchForm``
     - L'élément du formulaire de recherche qui est envoyé lorsqu'un candidat est sélectionné.
   * - ``boxCssInfo``
     - Le CSS appliqué à la zone de suggestion.
   * - ``listSelectedCssInfo``
     - Le CSS appliqué au candidat sélectionné (facultatif).
   * - ``listDeselectedCssInfo``
     - Le CSS appliqué aux candidats non sélectionnés (facultatif).

Pour la valeur spécifiée dans "z-index", veuillez spécifier une valeur qui ne chevauche pas avec d'autres éléments.

.. note::
    Lorsque le formulaire de recherche est placé sur une page dont le domaine diffère du serveur |Fess|, la requête vers l'API de suggestion devient une requête cross-origin.
    |Fess| autorise toutes les origines par défaut (``api.cors.allow.origin=*``), elle fonctionne donc telle quelle.
    Pour restreindre l'accès, modifiez ``api.cors.allow.origin`` dans ``fess_config.properties``.

.. note::
    ``/api/v2/suggest-words`` est l'API fournie par |Fess| lui-même.
    Le point de terminaison ``/api/v1/suggest-words`` utilisé dans les versions antérieures n'est plus fourni par le cœur de |Fess|, et le plugin ``fess-webapp-v1-api`` doit être installé pour l'utiliser.
    Pour les nouvelles installations, utilisez ``/api/v2/suggest-words``.
