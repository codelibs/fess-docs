================
Recherche floue
================

Recherche floue (recherche approximative)
==========================================

Lorsque vous souhaitez également rechercher des mots qui ne correspondent pas exactement au terme de recherche, vous pouvez utiliser la recherche floue (recherche approximative). La recherche floue est une méthode qui consiste à considérer un mot comme correspondant dès lors que la différence (distance d'édition) entre le terme de recherche et le mot enregistré dans l'index reste dans une plage donnée. La distance d'édition désigne le nombre minimal d'opérations d'insertion, de suppression ou de substitution de caractères nécessaires pour transformer un mot en un autre. Par défaut, |Fess| utilise la distance de Damerau-Levenshtein (optimal string alignment), qui, en plus de ces opérations, compte également l'interversion de deux caractères adjacents comme une seule différence.

Utilisation
-----------

Ajoutez « ~ » après le terme de recherche auquel vous souhaitez appliquer la recherche floue.

Par exemple, pour effectuer une recherche floue sur le mot « Fess », saisissez ce qui suit dans le formulaire de recherche pour rechercher des documents contenant des mots proches de « Fess » (tels que « Fes ») :

::

    Fess~

En ajoutant un chiffre après « ~ », vous pouvez indiquer la distance d'édition tolérée (le nombre de différences de caractères autorisées). Les valeurs possibles sont les entiers 0, 1 ou 2.

::

    Fess~1

Dans l'exemple ci-dessus, la recherche porte sur les mots dont la distance d'édition avec « Fess » est inférieure ou égale à 1.

Si vous omettez le chiffre et n'indiquez que « ~ », la distance d'édition est considérée comme égale à 2. La valeur maximale de la distance d'édition est 2 ; si vous indiquez une valeur de 3 ou plus, elle est également ramenée à 2.

Il est également possible d'effectuer une recherche floue en spécifiant un champ. Dans l'exemple suivant, la recherche porte sur les documents dont le champ title contient un mot proche de « Fess ».

::

    title:Fess~

Si aucun champ n'est spécifié, la recherche floue s'applique aux champs title et content.

Conditions d'utilisation
------------------------

Lors de l'utilisation de la recherche floue, tenez compte des points suivants :

* La recherche floue s'applique au niveau du mot. Elle ne peut pas être appliquée à une phrase entourée de guillemets. Notez que le chiffre placé après une phrase (par exemple ``"Fess Search"~2``) ne correspond pas à une recherche floue, mais à une recherche de proximité indiquant la distance entre les mots.
* La recherche floue porte sur les mots enregistrés dans l'index, et le terme de recherche n'est pas réanalysé. Par conséquent, elle peut ne pas fonctionner comme prévu pour des textes tels que le japonais, qui sont tokenisés par bi-gramme ou par analyse morphologique. La recherche floue est principalement efficace pour les mots alphanumériques.
* Pour les mots très courts, comme ceux de 1 à 2 caractères, la correspondance n'est possible que si la distance d'édition est inférieure à la longueur du mot ; l'ajout de « ~ » peut donc se comporter presque comme une correspondance exacte.

.. note::

    Le comportement de la recherche floue peut être ajusté dans ``fess_config.properties``.

    * ``query.fuzzy.prefix_length`` (valeur par défaut : ``0``) : nombre de caractères à faire correspondre exactement depuis le début du mot. Plus cette valeur est élevée, plus la marge d'erreur tolérée est réduite.
    * ``query.fuzzy.expansions`` (valeur par défaut : ``50``) : nombre maximal de mots développés comme candidats de correspondance.
    * ``query.fuzzy.transpositions`` (valeur par défaut : ``true``) : indique si l'interversion de deux caractères adjacents doit être comptée comme une seule modification. Si ``true``, il s'agit de la distance de Damerau-Levenshtein ; si ``false``, il s'agit de la distance de Levenshtein classique.

.. note::

    Même dans une recherche normale sans « ~ », |Fess| ajoute automatiquement, à titre d'appoint, une légère correspondance floue pondérée (``query.boost.fuzzy.*``) pour les termes de recherche d'une longueur supérieure ou égale à un certain seuil (4 caractères par défaut), afin d'améliorer la pertinence. Il s'agit d'une fonctionnalité destinée à ajuster le classement des résultats de recherche, distincte du mécanisme de recherche floue via « ~ ».

Voir aussi
==========

- :doc:`search-wildcard`
- :doc:`special-char`
