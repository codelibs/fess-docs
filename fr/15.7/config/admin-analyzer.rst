==============================
Configuration de l'Analyzeur
==============================

À propos de l'Analyzeur
========================

Lors de la création d'un index pour la recherche, il est nécessaire de segmenter les documents pour les enregistrer en tant qu'entrées d'index.
|Fess| enregistre la fonctionnalité de décomposition des documents en mots en tant qu'Analyzer.
L'Analyzer est composé de CharFilter, de Tokenizer et de TokenFilter.

Fondamentalement, les éléments plus petits que l'unité segmentée par l'Analyzer ne seront pas trouvés lors d'une recherche.
Par exemple, considérons la phrase « Habiter à Tokyo ».
Supposons que cette phrase ait été divisée par l'Analyzer en « Tokyo », « à » et « habiter ».
Dans ce cas, une recherche du terme « Tokyo » donnera des résultats.
Cependant, une recherche du terme « Kyo » ne donnera pas de résultats.

|Fess| fournit un Analyzer dédié par langue.
L'Analyzer à appliquer est automatiquement sélectionné en fonction du suffixe du nom de champ dans l'index (par exemple : ``content_ja``, ``content_en``).

Fichiers de définition de l'Analyzeur
======================================

L'Analyzer ne dispose pas d'un écran d'administration dédié ; sa configuration se modifie en éditant directement les fichiers de configuration.
Les fichiers concernés se trouvent sous ``app/WEB-INF/classes/fess_indices/``.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Fichier
     - Contenu
   * - ``fess_indices/fess.json``
     - Configuration de l'index des documents. Contient les définitions de CharFilter, Tokenizer, TokenFilter et Analyzer.
   * - ``fess_indices/fess/doc.json``
     - Mapping de l'index des documents. Associe l'Analyzer à appliquer à chaque modèle de nom de champ tel que ``*_ja`` ou ``*_en``.
   * - ``fess_indices/fess/<langue>/``
     - Fichiers de dictionnaire par langue (par exemple : ``ja/kuromoji.txt``, ``ko/nori.txt``, ``en/protwords.txt``, ``en/stemmer_override.txt``, ``stopwords.txt`` pour chaque langue).
   * - ``fess_indices/fess/mapping.txt``, ``fess_indices/fess/synonym.txt``
     - Dictionnaire de mapping de caractères et dictionnaire de synonymes partagés par toutes les langues.

La définition de l'Analyzer lui-même (combinaison de Tokenizer et de TokenFilter) est effectuée dans ``fess.json``, et la spécification de l'Analyzer à appliquer à chaque champ est réalisée dans ``fess/doc.json``.

.. note::
   Lorsque vous utilisez un service géré tel qu'Amazon OpenSearch Service, le fichier de configuration correspondant au type de moteur de recherche, comme ``fess_indices/_aws/fess.json`` ou ``fess_indices/_cloud/fess.json``, est utilisé en priorité.

Enregistrement de l'Analyzeur
==============================

La configuration de l'Analyzer est enregistrée en créant l'index de recherche à partir des fichiers de configuration ci-dessus, au démarrage de |Fess|, lorsque l'index de recherche n'existe pas encore.
L'index est créé avec un nom horodaté (par exemple : ``fess.20240101120000000``) et les alias ``fess.search`` et ``fess.update`` lui sont attribués.

Les variables de substitution telles que ``${fess.dictionary.path}`` dans les fichiers de configuration sont remplacées par leurs valeurs réelles lors de la création de l'index.
L'emplacement des fichiers de dictionnaire peut être modifié via la propriété système ``fess.dictionary.path``.

Si un index existant est présent, la configuration déjà définie est réutilisée.
Par conséquent, si vous modifiez la définition de l'Analyzer, il est nécessaire de recréer l'index pour que les modifications soient prises en compte.

Ajustement par dictionnaire
============================

Les dictionnaires référencés par l'Analyzer peuvent être modifiés depuis l'écran d'administration.

* :doc:`../admin/kuromoji-guide` - Dictionnaire utilisateur pour l'analyse morphologique japonaise
* :doc:`../admin/synonym-guide` - Dictionnaire de synonymes
* :doc:`../admin/mapping-guide` - Mapping de caractères
* :doc:`../admin/stopwords-guide` - Mots vides (stopwords)
* :doc:`../admin/protwords-guide` - Mots protégés
* :doc:`../admin/stemmeroverride-guide` - Substitution de la racinisation (stemming)

Pour en savoir plus sur la configuration de l'Analyzer, consultez la documentation de l'Analyzer d'OpenSearch.

Remarques importantes
======================

La configuration de l'Analyzer a un impact important sur la recherche.
Si vous souhaitez modifier l'Analyzer, faites-le en comprenant le fonctionnement de l'Analyzer de Lucene, ou consultez le support commercial.
