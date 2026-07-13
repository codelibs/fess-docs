====================
Caractères spéciaux
====================

Les caractères suivants ont une signification particulière dans la syntaxe des requêtes de recherche et sont donc traités comme des caractères spéciaux dans les termes de recherche. Pour utiliser ces caractères comme caractères de recherche littéraux, vous devez les échapper.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

Ces caractères permettent d'invoquer des fonctionnalités de recherche telles que les termes obligatoires/interdits (``+`` ``-``), les opérateurs booléens (``&&`` ``||`` ``!``), le regroupement (``( )``), la recherche par plage (``[ ]`` ``{ }``), la recherche avec pondération (``^``), la recherche de phrase (``"``), la recherche floue (``~``), la recherche par caractère générique (``*`` ``?``) et la recherche par champ (``:``).


Utilisation
-----------

Pour traiter un caractère spécial comme un caractère de recherche littéral, utilisez l'une des méthodes suivantes.

* Placez ``\`` immédiatement avant le caractère pour l'échapper. Le caractère unique qui suit est alors traité comme un caractère normal plutôt que comme un élément de la syntaxe de requête.
* Entourez le terme de recherche de ``"``. La chaîne ainsi entourée est traitée comme une recherche de phrase, et les caractères spéciaux qu'elle contient ne sont pas interprétés comme faisant partie de la syntaxe de requête. Notez cependant que, s'agissant d'une recherche de phrase, des fonctionnalités telles que la recherche par caractère générique (``*`` ``?``) ne sont pas disponibles.

::

    aaa\/bbb
    "aaa/bbb"
