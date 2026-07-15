==============
Recherche NOT
==============

La recherche NOT peut être utilisée pour rechercher des documents ne contenant pas un mot spécifique.

Utilisation
-----------

Pour effectuer une recherche NOT, placez NOT avant le mot à exclure. NOT
doit être écrit en majuscules et nécessite des espaces avant et après.

Par exemple, pour rechercher des documents contenant « terme1 » mais ne contenant pas « terme2 », saisissez ce qui suit :

::

    terme1 NOT terme2

.. note::

    NOT doit être écrit en majuscules. S'il est écrit en minuscules, comme ``not``, il n'est pas traité comme un opérateur, mais comme un terme de recherche ordinaire « not ». Le signe ``-`` placé directement avant le mot à exclure, comme dans ``terme1 -terme2``, a également la même signification que NOT.

En utilisant les parenthèses ``( )``, vous pouvez combiner la recherche NOT avec d'autres conditions de recherche. Par exemple, pour rechercher des documents contenant soit « terme1 » soit « terme2 », mais ne contenant pas « terme3 », saisissez ce qui suit :

::

    (terme1 OR terme2) NOT terme3

Il est également possible d'effectuer une recherche NOT en spécifiant un champ. Dans l'exemple suivant, la recherche porte sur les documents contenant « terme1 » dans le champ title, mais ne contenant pas « terme2 » dans le champ title.

::

    title:terme1 NOT title:terme2
