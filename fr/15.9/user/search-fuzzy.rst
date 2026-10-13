================
Recherche floue
================

Recherche floue (recherche approximative)
==========================================

Lorsque vous souhaitez également rechercher des mots qui ne correspondent pas exactement au terme de recherche, vous pouvez utiliser la recherche floue (recherche approximative). La recherche floue est une méthode qui consiste à considérer un mot comme correspondant dès lors que la différence (distance d'édition) entre le terme de recherche et le mot enregistré dans l'index reste dans une plage donnée. La distance d'édition désigne le nombre minimal d'opérations d'insertion, de suppression ou de substitution de caractères nécessaires pour transformer un mot en un autre. Par défaut, |Fess| utilise la distance de Damerau-Levenshtein (optimal string alignment), qui, en plus de ces opérations, compte également l'interversion de deux caractères adjacents comme une seule différence.

Utilisation
-----------

Ajoutez « ~ » après le terme de recherche auquel vous souhaitez appliquer la recherche floue.

Par exemple, pour effectuer une recherche floue sur le mot « fess », saisissez ce qui suit dans le formulaire de recherche pour rechercher des documents contenant des mots proches de « fess » (tels que « fes ») :

::

    fess~

En ajoutant un chiffre après « ~ », vous pouvez indiquer la distance d'édition tolérée (le nombre de différences de caractères autorisées). Les valeurs possibles sont les entiers 0, 1 ou 2.

::

    fess~1

Dans l'exemple ci-dessus, la recherche porte sur les mots dont la distance d'édition avec « fess » est inférieure ou égale à 1.

Si vous omettez le chiffre et n'indiquez que « ~ », la distance d'édition est considérée comme égale à 2. La valeur maximale de la distance d'édition est 2 ; si vous indiquez une valeur de 3 ou plus, elle est également ramenée à 2.

Il est également possible d'effectuer une recherche floue en spécifiant un champ. Dans l'exemple suivant, la recherche porte sur les documents dont le champ title contient un mot proche de « fess ».

::

    title:fess~

Si aucun champ n'est spécifié, la recherche floue s'applique aux champs title et content.

Conditions d'utilisation
------------------------

Lors de l'utilisation de la recherche floue, tenez compte des points suivants :

* La recherche floue s'applique au niveau du mot. Elle ne peut pas être appliquée à une phrase entourée de guillemets. Notez que le chiffre placé après une phrase (par exemple ``"Fess Search"~2``) ne correspond pas à une recherche floue, mais à une :doc:`recherche de proximité <search-proximity>` indiquant la distance entre les mots.
* La recherche floue porte sur les mots enregistrés dans l'index, et le terme de recherche n'est pas réanalysé. Par conséquent, elle peut ne pas fonctionner comme prévu pour des textes tels que le japonais, qui sont tokenisés par bi-gramme ou par analyse morphologique. La recherche floue est principalement efficace pour les mots alphanumériques.
* Le terme d'une recherche floue est comparé tel quel pour le calcul de la distance d'édition, majuscules et minuscules comprises. Les mots alphabétiques enregistrés dans l'index sont généralement convertis en minuscules ; utilisez donc des minuscules dans le terme de recherche. Par exemple, ``Fess~1`` épuise déjà la distance d'édition 1 avec la seule majuscule initiale ``F`` et ne donne donc pas le même résultat que ``fess~1``. De même, ``Fess~0`` ne correspond à rien, car l'index ne contient aucun mot correspondant au mot en majuscule ``Fess`` (le ``fess~0`` en minuscules est une correspondance exacte).
* Si vous ajoutez « ~ » (distance d'édition 2) à un mot très court, comme ceux de 1 à 2 caractères, il correspond aussi à des mots dont seul un nombre de caractères proche de la longueur du mot a été remplacé. Par exemple, ``ab~`` correspond à ``ab`` et ``ac``, mais aussi à ``xy``, dont les deux caractères sont différents. Cela multiplie les résultats non voulus ; pour les mots courts, indiquez donc une petite distance d'édition, comme ``ab~1``.

.. note::

    Le comportement de la recherche floue peut être ajusté dans ``fess_config.properties``.

    * ``query.fuzzy.prefix_length`` (valeur par défaut : ``0``) : nombre de caractères à faire correspondre exactement depuis le début du mot. Plus cette valeur est élevée, plus la marge d'erreur tolérée est réduite.
    * ``query.fuzzy.expansions`` (valeur par défaut : ``50``) : nombre maximal de mots développés comme candidats de correspondance.
    * ``query.fuzzy.transpositions`` (valeur par défaut : ``true``) : indique si l'interversion de deux caractères adjacents doit être comptée comme une seule modification. Si ``true``, il s'agit de la distance de Damerau-Levenshtein ; si ``false``, il s'agit de la distance de Levenshtein classique.

.. note::

    Même dans une recherche normale sans « ~ », |Fess| ajoute automatiquement, à titre d'appoint, une légère correspondance floue pondérée (``query.boost.fuzzy.*``) pour les termes de recherche d'une longueur supérieure ou égale à un certain seuil (4 caractères par défaut), afin d'améliorer la pertinence. Il s'agit d'une fonctionnalité destinée principalement à ajuster le classement des résultats de recherche, distincte du mécanisme de recherche floue via « ~ ». Toutefois, cette correspondance d'appoint est elle aussi incluse dans les résultats : des documents ne contenant pas le terme de recherche lui-même, mais uniquement un mot qui en diffère d'un caractère, peuvent donc s'ajouter aux résultats (les documents contenant le terme lui-même sont mieux classés). Pour supprimer ce comportement, indiquez une valeur négative (par exemple ``-1``) pour ``query.boost.fuzzy.min.length``.

Voir aussi
==========

- :doc:`search-wildcard`
- :doc:`search-proximity`
- :doc:`special-char`
