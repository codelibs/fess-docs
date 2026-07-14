=======================
Recherche avec boost
=======================

Recherche avec boost (recherche pondérée)
==========================================

La recherche avec boost est utilisée lorsque vous souhaitez donner la priorité à un terme de recherche spécifique parmi les termes de recherche. L'utilisation de la recherche avec boost permet d'effectuer des recherches en fonction de l'importance des termes de recherche.

Utilisation
-----------

Pour utiliser la recherche avec boost, spécifiez une valeur de boost (valeur de pondération) au format « ^valeur_boost » juste après le terme de recherche. N'insérez pas d'espace entre le terme de recherche et la valeur de boost.

Par exemple, lors de la recherche de « pomme orange », si vous souhaitez donner la priorité à « pomme », saisissez ce qui suit dans le formulaire de recherche :

::

    pomme^100 orange

Dans cet exemple, la valeur de boost s'applique uniquement à « pomme », et non à « orange ».

Valeur de boost
-----------------

La valeur de boost est un nombre. Vous pouvez spécifier non seulement des entiers, mais aussi des valeurs décimales telles que ``2.5``.

- Si vous spécifiez une valeur supérieure à 1, le poids de ce terme de recherche augmente.
- Si vous spécifiez une valeur supérieure à 0 et inférieure à 1 (par exemple, ``0.5``), le poids de ce terme de recherche diminue.

La valeur de boost ne détermine pas de manière absolue le score des résultats de recherche ; elle ajuste la pondération relative par rapport aux autres termes de recherche.

Combinaison avec d'autres syntaxes de recherche
---------------------------------------------------

La recherche avec boost peut être combinée avec d'autres syntaxes de recherche. Par exemple, il est également possible d'ajouter une valeur de boost à un terme de recherche associé à un champ spécifique.

::

    title:pomme^100 orange

Dans cet exemple, les documents dont le champ ``title`` contient « pomme » sont prioritaires.
