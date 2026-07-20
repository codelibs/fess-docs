================
Recherche floue
================

Recherche floue (recherche approximative)
==========================================

La recherche floue (recherche approximative) est disponible pour rechercher également des mots qui ne correspondent pas exactement au terme de recherche. Elle est utile lorsque vous souhaitez retrouver des documents contenant des fautes de frappe, des variations orthographiques ou des mots mal orthographiés qui ne correspondent pas exactement au terme saisi. |Fess| prend en charge la recherche floue (recherche approximative) basée sur la distance d'édition (distance de Levenshtein), qui indique le degré de différence entre deux mots.

Utilisation
-----------

Ajoutez « ~ » après le terme de recherche auquel vous souhaitez appliquer la recherche floue.

Par exemple, pour effectuer une recherche floue sur le mot « Fess », saisissez ce qui suit dans le formulaire de recherche pour rechercher des documents contenant des mots proches de « Fess » (tels que « Fes ») :

::

    Fess~

Le degré d'approximation peut être précisé en ajoutant un chiffre de 0 à 2 après ``~``. Ce chiffre indique la limite supérieure de la distance d'édition tolérée (le nombre maximal d'insertions, de suppressions ou de substitutions de caractères) ; si vous l'omettez, la distance d'édition par défaut est appliquée.

::

    Fess~1
    Fess~2

En spécifiant ``~2``, la recherche tolère jusqu'à 2 caractères de différence par rapport à ``Fess``.

Voir aussi
==========

- :doc:`search-wildcard`
- :doc:`special-char`

