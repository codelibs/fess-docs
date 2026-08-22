==============
Recherche AND
==============

La recherche AND est utilisée pour rechercher des documents contenant tous les termes de recherche spécifiés. Si vous saisissez plusieurs mots séparés par des espaces dans le champ de recherche, la recherche sera par défaut de type AND ; vous pouvez donc omettre AND tout en obtenant le même résultat.

Utilisation
-----------

Pour utiliser la recherche AND, saisissez AND entre les termes de recherche. AND
doit être écrit en majuscules et nécessite des espaces avant et après. AND
peut également être omis.

Par exemple, pour rechercher des documents contenant à la fois « terme1 » et « terme2 », saisissez ce qui suit dans le formulaire de recherche :

::

    terme1 AND terme2

Il est également possible d'omettre AND et d'obtenir le même résultat en saisissant simplement :

::

    terme1 terme2

Il est également possible de connecter trois termes de recherche ou plus avec AND.

::

    terme1 AND terme2 AND terme3

.. note::

    AND doit être écrit en majuscules. S'il est écrit en minuscules, comme ``and``, il n'est pas traité comme un opérateur, mais comme un terme de recherche ordinaire « and ». ``&&`` peut également être utilisé avec la même signification que AND.

En utilisant les parenthèses ``( )``, vous pouvez combiner la recherche AND avec d'autres conditions de recherche. Par exemple, pour rechercher des documents contenant « terme1 », et contenant également soit « terme2 » soit « terme3 », saisissez ce qui suit :

::

    terme1 AND (terme2 OR terme3)

Il est également possible d'effectuer une recherche AND en spécifiant un champ. Dans l'exemple suivant, la recherche porte sur les documents contenant « terme1 » dans le champ title, et « terme2 » dans le champ content.

::

    title:terme1 AND content:terme2
