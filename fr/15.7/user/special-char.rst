====================
Caractères spéciaux
====================

Les caractères suivants ont une signification particulière dans la syntaxe des requêtes de recherche et sont donc traités comme des caractères spéciaux dans les termes de recherche. Pour utiliser ces caractères comme caractères de recherche littéraux, vous devez les échapper.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

Ces caractères permettent d'invoquer des fonctionnalités de recherche telles que les termes obligatoires/interdits (``+`` ``-``), les opérateurs booléens (``&&`` ``||`` ``!``), le regroupement (``( )``), la recherche par plage (``[ ]`` ``{ }``), la recherche avec pondération (``^``), la recherche de phrase (``"``), la recherche floue (``~``), la recherche par caractère générique (``*`` ``?``) et la recherche par champ (``:``).

Par exemple, si vous recherchez tels quels des caractères comme ``/`` ou ``:`` présents dans une URL ou un chemin de fichier, ou encore ``+`` ou ``-`` utilisés dans du code, vous risquez d'obtenir des résultats de recherche inattendus. Reportez-vous à la section ci-dessous pour la méthode d'échappement à utiliser.

Liste des caractères spéciaux et leur signification
-----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Caractère spécial
     - Signification / Rôle
     - Page associée
   * - ``+`` ``-``
     - Indique un terme obligatoire ou un terme à exclure (recherche AND / recherche NOT)
     - :doc:`search-and` / :doc:`search-not`
   * - ``&&`` ``||``
     - Recherche AND / recherche OR
     - :doc:`search-and` / :doc:`search-or`
   * - ``!``
     - Recherche NOT (recherche par exclusion)
     - :doc:`search-not`
   * - ``( )``
     - Regroupement des conditions de recherche
     - :doc:`advanced-search`
   * - ``[ ]`` ``{ }``
     - Recherche par plage (``[ ]`` inclut les bornes, ``{ }`` les exclut)
     - :doc:`search-range`
   * - ``^``
     - Recherche avec boost (pondération)
     - :doc:`search-boost`
   * - ``"``
     - Recherche de phrase (le texte entouré de guillemets est traité comme une seule expression ; peut aussi servir à échapper des caractères spéciaux)
     - :doc:`advanced-search`
   * - ``~``
     - Recherche floue (recherche approximative)
     - :doc:`search-fuzzy`
   * - ``*`` ``?``
     - Recherche avec caractères génériques
     - :doc:`search-wildcard`
   * - ``:``
     - Indique le champ de recherche
     - :doc:`search-field`
   * - ``\``
     - Caractère d'échappement
     - (cette page)
   * - ``/``
     - Barre oblique (doit être échappée lorsqu'elle apparaît, par exemple, dans une URL)
     - :doc:`search-field`

Utilisation
-----------

Échappez avec \ ou entourez le terme de recherche avec ".

::

    aaa\/bbb
    "aaa/bbb"

Par exemple, si vous souhaitez rechercher le terme « C++ » tel quel, échappez-le comme suit :

::

    C\+\+
    "C++"

Voir aussi
-----------

- :doc:`search-field`
- :doc:`search-wildcard`
- :doc:`search-fuzzy`
- :doc:`advanced-search`

