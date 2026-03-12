=========================
Configuration de l'Analyzer
=========================

À propos de l'Analyzer
==============

Lors de la création d'un index pour la recherche, il est nécessaire de segmenter les documents pour les enregistrer en tant qu'index.
|Fess| enregistre la fonctionnalité de décomposition des documents en mots en tant qu'Analyzer.
L'Analyzer est composé de CharFilter, Tokenizer et TokenFilter.

Fondamentalement, les éléments plus petits que l'unité segmentée par l'Analyzer ne seront pas trouvés lors d'une recherche.
Par exemple, considérons la phrase « habiter à Tokyo ».
Supposons que cette phrase ait été divisée par l'Analyzer en « Tokyo », « à » et « habiter ».
Dans ce cas, une recherche du terme « Tokyo » donnera des résultats.
Cependant, une recherche du terme « Kyo » ne donnera pas de résultats.

La configuration de l'Analyzer est enregistrée en créant l'index fess avec app/WEB-INF/classes/fess_indices/fess.json lorsque l'index fess n'existe pas au démarrage de |Fess|.
Pour savoir comment configurer l'Analyzer, consultez la documentation de l'Analyzer d'OpenSearch.

La configuration de l'Analyzer a un impact important sur la recherche.
Si vous souhaitez modifier l'Analyzer, faites-le en comprenant le fonctionnement de l'Analyzer de Lucene ou consultez le support commercial.
