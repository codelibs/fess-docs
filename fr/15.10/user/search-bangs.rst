=================================================
Recherche par bang (rechercher sur un autre site)
=================================================

Un bang envoie une recherche vers un autre site au lieu de rechercher dans |Fess|. Il fonctionne comme les bangs de DuckDuckGo : ajoutez ``!`` et un court mot déclencheur à la requête, et |Fess| envoie le reste de la requête au site que représente ce mot déclencheur.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Requête
     - Destination
   * - ``airplane !g``
     - Google, recherche de ``airplane``
   * - ``!w Ohm's law``
     - Wikipedia, recherche de ``Ohm's law``
   * - ``!g``
     - La page d'accueil de Google
   * - ``airplane !unknown``
     - |Fess|, comme une recherche normale (``!`` signifie NOT, voir :doc:`search-not`)

Les bangs sont fournis par le plugin ``fess-webapp-bangs``, qui nécessite |Fess| 15.9 ou une version ultérieure. Installez-le depuis [Système > Plugin] dans la console d'administration ou avec ``bin/fess-setup install plugin fess-webapp-bangs`` (voir :doc:`../admin/plugin-guide`), puis redémarrez |Fess|.

Comment un bang est reconnu
===========================

- Un bang est ``!`` suivi d'un mot déclencheur, écrit comme un mot distinct. Le mot déclencheur ne distingue pas les majuscules des minuscules.
- Le bang est retiré de la requête, et le reste de la requête est envoyé à l'URL du bang.
- Lorsqu'une requête contient plusieurs bangs définis, seul le premier compte.
- Un mot déclencheur qui n'est pas défini n'est pas un bang. ``!unknown`` est recherché comme d'habitude et exclut le mot ``unknown``.
- ``-g`` et ``NOT g`` continuent d'exclure le mot ``g``. Seul ``!g`` est un bang.

La page de recherche et ``/api/v2/search`` suivent la redirection : l'API renvoie ``redirect_url`` (voir :doc:`../api/api-search`), et le thème ``bootstrap`` fourni avec |Fess| navigue vers cette URL. Les autres thèmes doivent gérer ce cas de la même manière.

Les appelants qui ne peuvent pas rediriger, comme le chat, MCP, les API JSON v1 et classique et la recherche de la console d'administration, n'envoient pas la recherche vers un autre site. Ils retirent le bang et recherchent le reste de la requête.

Définir des bangs
=================

Les bangs sont définis par la propriété système ``bangs.definitions``. Définissez-la dans ``app/WEB-INF/conf/system.properties`` ou transmettez-la sous la forme ``-Dfess.system.bangs.definitions=...``. Une modification de ``system.properties`` est prise en compte sans redémarrer |Fess|.

La valeur est une liste d'entrées ``mot_déclencheur=URL`` séparées par des espaces. Dans l'URL, ``{query}`` est remplacé par le reste de la requête encodé en URL :

::

    bangs.definitions=g=https://www.google.com/search?q={query} w=https://en.wikipedia.org/wiki/Special:Search?search={query}

- Un mot déclencheur ne peut contenir ni espace, ni ``(``, ``)``, ``!``, ``"``, ``=`` ou ``:``.
- Seules les URL absolues ``http`` ou ``https`` sont acceptées.
- Une entrée qui ne respecte pas ces règles n'est pas utilisée. Un avertissement est écrit dans le journal de |Fess|, et les autres entrées restent en vigueur.
- Si le même mot déclencheur est défini deux fois, la première définition est utilisée.
- Une valeur vide désactive tous les bangs.

Lorsque ``bangs.definitions`` n'est pas définie, les cinq bangs suivants sont disponibles :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Mot déclencheur
     - Site
   * - ``g``
     - Google
   * - ``b``
     - Bing
   * - ``ddg``
     - DuckDuckGo
   * - ``w``
     - Wikipedia (anglais)
   * - ``gh``
     - GitHub

Définir ``bangs.definitions`` remplace cette liste. Pour conserver les bangs par défaut et en ajouter un, écrivez toutes les entrées dont vous avez besoin.

Voir aussi
==========

- :doc:`search-not` - Recherche NOT
- :doc:`special-char` - Caractères spéciaux et échappement
- :doc:`../api/api-search` - API de recherche
