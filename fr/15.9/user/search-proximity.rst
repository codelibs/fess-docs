========================
Recherche de proximité
========================
Recherche de proximité (distance entre les mots)
==================================================

La recherche de proximité permet de trouver les documents dans lesquels les mots d'une phrase apparaissent proches les uns des autres, même s'ils ne sont pas directement adjacents. Elle est utile lorsque d'autres mots peuvent s'intercaler entre les mots recherchés.

Utilisation
-------------

Entourez les mots de guillemets doubles, puis ajoutez « ~ » et un chiffre après le guillemet fermant.

Par exemple, la recherche suivante trouve les documents dans lesquels « Fess » et « recherche » apparaissent à une distance de 3 au plus :

::

    "Fess recherche"~3

Le nombre correspond au nombre maximal de déplacements de position autorisés entre les mots (voir « Comment la distance est comptée » ci-dessous). Plus le nombre est grand, plus les mots peuvent être éloignés.

Vous pouvez également effectuer une recherche de proximité sur un champ précis. Dans l'exemple suivant, la recherche porte sur le champ title.

::

    title:"Fess recherche"~3

Si vous omettez le nombre et n'indiquez que « ~ » (par exemple ``"Fess recherche"~``), la phrase est recherchée comme une phrase normale dont les mots doivent être adjacents. Un nombre décimal est tronqué à sa partie entière (``~2.5`` est traité comme ``~2``).

La recherche de proximité peut être combinée avec un boost. Dans l'exemple suivant, la recherche de proximité est pondérée par 2 (voir :doc:`search-boost`).

::

    "Fess recherche"~5^2

Comment la distance est comptée
---------------------------------

* Le nombre correspond au nombre maximal de déplacements de position autorisés entre les mots. Il est compté en tokens produits par l'analyseur du champ cible, et non en caractères ni en mots séparés par des espaces. Pour un texte en anglais, il correspond approximativement au nombre de mots situés entre les termes. Les mots supprimés comme mots vides (stop words) lors de l'analyse sont également comptés.
* Les mots peuvent apparaître dans un ordre différent, mais l'ordre inversé nécessite un nombre plus grand. Par exemple, un document contenant « quick brown fox » correspond à ``"quick fox"~1``, mais ne correspond à ``"fox quick"`` qu'à partir de ``~3``.

::

    "quick fox"~1
    "fox quick"~3

Texte japonais, chinois et coréen (CJK)
-----------------------------------------

Pour le japonais et les autres textes CJK, l'unité dans laquelle la distance est comptée dépend du champ.

* Dans les champs généraux title et content, la distance est proche du nombre de caractères situés entre les mots.
* Dans les champs propres à chaque langue, la distance est comptée en tokens morphologiques, et les particules supprimées sont également comptées.

Séparez donc les mots par des espaces et indiquez un nombre généreux.

::

    "全文 検索"~5
    "大阪 おいしい"~10

Une chaîne sans espaces (par exemple ``"大阪おいしい"~10``) peut ne pas fonctionner comme prévu en tant que recherche de proximité entre les mots, car dans les champs généraux elle est comparée comme une seule chaîne continue. Séparez les mots par des espaces. La distance ne peut pas être convertie exactement en nombre de caractères ; commencez donc par un nombre généreux, puis affinez-le en vérifiant les résultats.

Voir aussi
============

- :doc:`search-fuzzy`
- :doc:`search-boost`
- :doc:`search-field`
- :doc:`special-char`
