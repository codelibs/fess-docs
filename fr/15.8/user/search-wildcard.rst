====================================
Recherche avec caractères génériques
====================================

Vous pouvez utiliser des caractères génériques pour un ou plusieurs caractères dans les termes de recherche. ? peut être spécifié comme caractère générique pour un seul caractère, et \* peut être spécifié comme caractère générique pour plusieurs caractères. Les caractères génériques peuvent être utilisés sur des mots. La recherche avec caractères génériques sur des phrases n'est pas possible.

Utilisation
-----------

Pour utiliser un caractère générique pour un seul caractère, utilisez ? comme suit.

::

    te?t

Dans ce cas, cela correspond à un caractère quelconque à la position de ?, comme dans text ou test.

Pour utiliser un caractère générique pour plusieurs caractères, utilisez \* comme suit.

::

    test*

Dans ce cas, cela correspond à une chaîne de caractères quelconque de longueur nulle ou plus à la position de \*, comme dans test, tests ou tester. De plus,

::

    te*t

peut également être utilisé au milieu d'un terme de recherche, comme ci-dessus. Par ailleurs,

::

    *test

peut également être utilisé en début de terme de recherche, comme ci-dessus.

Il est également possible d'effectuer une recherche avec caractères génériques en spécifiant un champ. Dans l'exemple suivant, la recherche porte sur les documents dont le champ title contient un mot commençant par te et se terminant par t.

::

    title:te*t

Si aucun champ n'est spécifié, la recherche porte sur les champs title et content.

Conditions d'utilisation
------------------------

Lors de l'utilisation de la recherche avec caractères génériques, tenez compte des points suivants :

* Les caractères génériques correspondent aux chaînes de caractères (tokens) enregistrées dans l'index. Le terme de recherche n'étant pas réanalysé, si l'index est créé avec bi-gram par exemple, le japonais est traité comme une chaîne de caractères de longueur fixe sans signification, et les caractères génériques en japonais ne fonctionneront pas comme prévu. Pour utiliser des caractères génériques en japonais, utilisez-les dans des champs utilisant l'analyse morphologique.
* Les motifs de caractères génériques sont sensibles à la casse. Les mots enregistrés dans l'index étant généralement convertis en minuscules, utilisez des minuscules dans le motif. Par exemple, ``Test*`` ne correspond pas à ``test``, qui a été enregistré après conversion en minuscules.
* Une recherche avec un caractère générique en début de terme (par exemple ``*test``) parcourt tous les mots de l'index et peut donc prendre du temps.
