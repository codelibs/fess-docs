=======================
Recherche avec boost
=======================

Recherche avec boost (recherche pondérée)
==========================================

La recherche avec boost est utilisée lorsque vous souhaitez donner la priorité à un terme de recherche spécifique parmi les termes de recherche. L'utilisation de la recherche avec boost permet d'effectuer des recherches en fonction de l'importance des termes de recherche.

Utilisation
-----------

Pour utiliser la recherche avec boost, spécifiez une valeur de boost (valeur de pondération) au format « ^valeur_boost » après le terme de recherche.

Par exemple, lors de la recherche de « pomme orange », si vous souhaitez donner la priorité aux pages contenant davantage « pomme », saisissez ce qui suit dans le formulaire de recherche :

::

    pomme^100 orange

La valeur de boost doit être un nombre entier supérieur ou égal à 1.
