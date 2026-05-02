====================================
Recherche avec caractères génériques
====================================

Vous pouvez utiliser des caractères génériques pour un ou plusieurs caractères dans les termes de recherche. ? peut être spécifié comme caractère générique pour un seul caractère, et \* peut être spécifié comme caractère générique pour plusieurs caractères. Les caractères génériques peuvent être utilisés sur des mots. La recherche avec caractères génériques sur des phrases n'est pas possible.

Utilisation
-----------

Pour utiliser un caractère générique pour un seul caractère, utilisez ? comme suit.

::

    te?t

Dans ce cas, il sera traité comme un caractère générique pour un seul caractère, tel que text ou test.

Pour utiliser un caractère générique pour plusieurs caractères, utilisez \* comme suit.

::

    test*

Dans ce cas, il sera traité comme un caractère générique pour plusieurs caractères, tel que test, tests ou tester. De plus,

::

    te*t

peut également être utilisé dans un terme de recherche.

Conditions d'utilisation
-------------------------

Les caractères génériques sont utilisés sur les chaînes de caractères enregistrées dans l'index.
Par conséquent, si l'index est créé avec bi-gram, le japonais est traité comme une chaîne de caractères de longueur fixe sans signification, donc les caractères génériques en japonais ne fonctionneront pas comme prévu.
Pour utiliser des caractères génériques en japonais, veuillez les utiliser dans des champs utilisant l'analyse morphologique.
