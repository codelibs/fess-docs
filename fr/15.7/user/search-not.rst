==============
Recherche NOT
==============

Lorsque vous souhaitez rechercher des documents ne contenant pas un mot donné (recherche par exclusion), vous pouvez utiliser la recherche NOT. Elle est pratique lorsque vous souhaitez exclure des mots-clés spécifiques des résultats de recherche afin de réduire le bruit.

Utilisation
-----------

Pour effectuer une recherche NOT, placez NOT avant le mot à exclure. NOT
doit être écrit en majuscules et nécessite des espaces avant et après.

Par exemple, pour rechercher des documents contenant « terme1 » mais ne contenant pas « terme2 », saisissez ce qui suit :

::

    terme1 NOT terme2

Il est également possible d'utiliser ``-`` (trait d'union) directement devant le mot à exclure, à la place de NOT. Ce qui suit a la même signification que l'exemple ci-dessus :

::

    terme1 -terme2

Voir aussi
----------

- :doc:`search-and`
- :doc:`search-or`
- :doc:`special-char`
