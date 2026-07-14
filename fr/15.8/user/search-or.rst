=============
Recherche OR
=============

La recherche OR est utilisée pour rechercher des documents contenant n'importe lequel des termes de recherche. Si vous saisissez plusieurs mots dans le champ de recherche, la recherche sera par défaut de type AND.

Utilisation
-----------

Pour utiliser la recherche OR, saisissez OR entre les termes de recherche. OR
doit être écrit en majuscules et nécessite des espaces avant et après.

Par exemple, pour rechercher des documents contenant soit « terme1 » soit « terme2 », saisissez ce qui suit dans le formulaire de recherche :

::

    terme1 OR terme2

Il est également possible de connecter trois termes de recherche ou plus avec OR.

::

    terme1 OR terme2 OR terme3

.. note::

    OR doit être écrit en majuscules. S'il est écrit en minuscules, comme ``or``, il n'est pas traité comme un opérateur, mais comme un terme de recherche ordinaire « or ». ``||`` peut également être utilisé avec la même signification que OR.

En utilisant les parenthèses ``( )``, vous pouvez combiner la recherche OR avec d'autres conditions de recherche. Par exemple, pour rechercher des documents contenant soit « terme1 » soit « terme2 », et contenant également « terme3 », saisissez ce qui suit :

::

    (terme1 OR terme2) terme3

Il est également possible d'effectuer une recherche OR en spécifiant un champ. Dans l'exemple suivant, la recherche porte sur les documents contenant « terme1 » dans le champ title, ou « terme2 » dans le champ content.

::

    title:terme1 OR content:terme2
