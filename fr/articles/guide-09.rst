===================================================
Rechercher des documents japonais, anglais, chinois
===================================================

Introduction
============

Lorsque des comptes rendus de réunion en japonais, des spécifications techniques en anglais et des rapports de marché en chinois cohabitent sur le même serveur de fichiers ou le même site intranet, on entend vite des remarques comme « les documents en anglais sont trouvés, mais les formes conjuguées du japonais ne correspondent pas », « je voudrais chercher uniquement dans les documents en chinois » ou « je voudrais trouver des documents rédigés en anglais à l'aide de mots japonais ».

Fess peut rechercher des documents dans n'importe quelle langue sans configuration particulière.
Cependant, si vous ajoutez des entrées de dictionnaire sans savoir où s'applique l'analyse de chaque langue, les résultats ne changeront pas.
Cet article explique, à partir des valeurs réelles des fichiers de configuration, comment Fess 15.9 indexe et recherche des documents multilingues.
Vous pourrez ensuite :

- Vérifier la langue détectée pour chaque document et limiter la recherche à une langue avec ``lang:``
- Choisir, avec ``query.default.languages`` et les paramètres associés, l'analyse de quelles langues est utilisée lors de la recherche
- Modifier les dictionnaires (synonymes, Kuromoji, mots vides, etc.) en fonction des champs sur lesquels ils agissent, et appliquer les modifications
- Confirmer qu'une modification a pris effet, à l'aide des résultats de recherche et de l'API ``_analyze``

La démarche d'amélioration à partir des journaux de recherche est traitée dans :doc:`guide-08`.

Fonctionnement de l'indexation : champs communs et champs par langue
====================================================================

Dans l'index de Fess, le corps du texte et le titre sont stockés sous deux formes.
Ils sont définis dans ``fess_indices/fess.json`` (analyseurs) et ``fess_indices/fess/doc.json`` (mappage), tous deux fournis avec Fess.

.. list-table::
   :header-rows: 1
   :widths: 28 32 40

   * - Champ
     - Analyseur
     - Nature de l'analyse
   * - ``content``, ``title``, ``important_content``
     - ``standard_analyzer`` (``standard_search_analyzer`` lors de la recherche)
     - Commun à tous les documents. Les kanji, hiragana, katakana et hangul sont découpés en unités de deux caractères (bigrammes), et la suppression des mots vides anglais ainsi que la racinisation (stemming) sont appliquées. Les synonymes ne sont développés qu'au moment de la recherche
   * - ``content_ja``, ``title_ja``, etc.
     - ``japanese_analyzer``
     - Analyse morphologique avec Kuromoji. Les verbes et autres mots sont ramenés à leur forme de base, et les particules, auxiliaires et symboles sont supprimés
   * - ``content_en``, ``title_en``, etc.
     - ``english_analyzer``
     - Suppression des mots vides anglais et racinisation
   * - ``content_zh-cn``, ``title_zh-cn``, etc.
     - ``simplified_chinese_analyzer``
     - Découpe le texte en mots avec un tokenizer pour le chinois
   * - ``content_zh-tw``, ``title_zh-tw``, etc.
     - ``traditional_chinese_analyzer``
     - Convertit les caractères traditionnels en caractères simplifiés, puis découpe le texte avec le même tokenizer que pour le chinois simplifié

Tous les documents possèdent les champs communs.
Les champs par langue ne sont créés que lorsque la langue du document a été déterminée.
Lors de l'indexation, le code de langue est placé dans le champ ``lang``, et les valeurs de ``content``, ``important_content`` et ``title`` (``indexer.language.fields``) sont copiées dans des champs ``<champ>_<langue>`` tels que ``content_ja``.
Un document ne reçoit qu'une seule langue.

Comment la langue d'un document est déterminée
----------------------------------------------

``lang`` est déterminé dans l'ordre suivant.

1. Pour le HTML issu d'un crawl web, la valeur de ``<html lang="...">`` est utilisée (``crawler.document.html.lang.xpath=//HTML/@lang``). En écrivant ``field.xpath.default.lang=<XPath>`` dans les « Paramètres de configuration » d'une configuration de crawl, vous changez l'endroit où la valeur est lue, pour cette configuration uniquement
2. Pour les documents dont la langue n'est pas déterminée à l'étape 1, elle est détectée automatiquement à partir du texte. Les 1000 premiers caractères (``indexer.language.detect.length``) de ``content``, ``important_content`` et ``title`` sont examinés, dans cet ordre. Pour les crawls de fichiers, la détection se fait uniquement à partir du corps de texte extrait
3. Si la langue détectée ne figure pas dans ``supported.languages``, ou si aucune langue ne peut être détectée, aucun ``lang`` n'est attribué et aucun champ par langue n'est créé

Les valeurs comme ``ja-JP`` ou ``zh_CN`` sont normalisées en minuscules avec trait d'union (``ja``, ``zh-cn``) lors de l'enregistrement.

Les documents issus des magasins de données passent eux aussi par la même détection automatique lors de l'indexation.
Si un script affecte à ``lang`` une langue figurant dans ``supported.languages`` (par exemple ``ja``), cette valeur l'emporte sur la détection automatique.

Fonctionnement de la recherche : quels champs de langue sont interrogés
=======================================================================

Les termes de recherche sont toujours recherchés dans les champs communs.
En outre, pour chaque « langue de recherche » déterminée à chaque recherche, les champs correspondants de cette langue sont ajoutés à la requête.
Les conditions sur chaque champ sont combinées par OR (``should`` d'une requête ``bool``) : un document apparaît dans les résultats dès qu'il correspond dans l'un quelconque des champs.

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Champ
     - Clé de configuration
     - Valeur par défaut
   * - ``title``
     - ``query.boost.title``
     - ``0.5``
   * - ``content``
     - ``query.boost.content``
     - ``0.05``
   * - ``title_<langue de recherche>``
     - ``query.boost.title.lang``
     - ``1.0``
   * - ``content_<langue de recherche>``
     - ``query.boost.content.lang``
     - ``0.1``

Les langues de recherche sont tirées de la première des sources suivantes qui possède une valeur.

1. ``query.default.languages`` dans ``fess_config.properties`` (vide par défaut). Si une valeur est définie, toutes les autres indications sont ignorées
2. Le paramètre ``lang`` de la requête : la langue choisie dans [Options] > « Langue préférée » sur la page de recherche ou dans « Langue préférée » de la recherche avancée, ou ``lang`` de ``/api/v2/search``
3. La langue de l'en-tête ``Accept-Language`` envoyé par le navigateur

Par exemple, si vous recherchez « 会議 » (« réunion ») dans un navigateur réglé en japonais, la langue de recherche est ``ja`` et ``content_ja`` est interrogé en plus de ``content``.
Les documents en anglais n'ont pas de ``content_ja`` ; ils ne correspondent donc que par les bigrammes des champs communs.
À l'inverse, lorsqu'un document japonais correspond aussi dans ``title_ja`` ou ``content_ja``, son score augmente d'autant et il a tendance à remonter.
Comme Kuromoji ramène les formes conjuguées à leur forme de base, une recherche sur « 走った » (« a couru ») trouve aussi, via ``content_ja``, les documents japonais où figure « 走る » (« courir »).

C'est pourquoi « Langue préférée » fait remonter les documents de cette langue ; ce n'est pas un filtre qui exclut les documents des autres langues.

Limiter par langue : la recherche ``lang:``
===========================================

Pour limiter les résultats à une langue, indiquez le champ ``lang`` dans la recherche.
``lang`` est un champ de type keyword interrogeable ; il n'est donc pas nécessaire de créer une étiquette pour chaque langue.

::

    lang:en meeting
    lang:ja 会議
    lang:zh-cn 会议
    会議 -lang:ja

Le dernier exemple recherche « 会議 » en excluant les documents détectés comme japonais.
Depuis l'API, écrivez la même expression dans ``q``, ou ajoutez ``fields.lang=en`` (ce qui ajoute une condition ``lang:"en"``).

::

    $ curl -s "http://localhost:8080/api/v2/search?q=meeting&fields.lang=en"

Les documents sans ``lang`` (ceux dont la langue n'a pas pu être détectée) ne correspondent à aucune condition ``lang:``.

Vérifier la langue détectée
---------------------------

Avant de modifier les dictionnaires ou les paramètres, vérifiez quelle langue a été attribuée à vos documents.

1. Sur la page de recherche, recherchez successivement ``lang:ja``, ``lang:en``, ``lang:zh-cn`` et ``lang:zh-tw`` et comparez le nombre de résultats. Avec l'API, le nombre figure dans ``response.record_count``

   ::

       $ curl -s "http://localhost:8080/api/v2/search?q=lang:zh-cn&num=1"

2. Pour un document particulier, recherchez-le par son URL ou autre dans [Informations système] > [Rechercher] de la console d'administration et ouvrez-le ; la valeur s'affiche dans le champ ``lang``

Si la détection ne correspond pas à vos attentes, vérifiez les points suivants.

- Le ``<html lang>`` du HTML l'emporte sur la détection automatique. Si le modèle du site produit ``lang="en"`` même sur les pages japonaises, ces pages sont traitées comme de l'anglais
- Le chinois sans région, comme ``<html lang="zh">``, devient ``zh``. Il n'existe pas de champ par langue avec un analyseur chinois pour ``zh`` ; l'analyse du chinois se limite donc aux bigrammes des champs communs
- Les documents japonais courts contenant beaucoup de kanji et peu de kana peuvent être détectés comme ``zh-cn`` ou une langue similaire

Il existe aussi des paramètres qui traitent tout le HTML, ou tous les fichiers, comme une seule langue.
Si vous donnez une valeur à ``crawler.document.html.default.lang`` et ``crawler.document.file.default.lang``, ni ``<html lang>`` ni la détection automatique ne sont utilisés, et la langue est fixée à cette valeur pour tous les crawls de Fess.
Dans un environnement où les documents mélangent plusieurs langues, laissez-les vides.

Définir les langues de recherche : ``query.default.languages``
==============================================================

Par défaut, la langue de recherche varie selon la langue du navigateur de chaque utilisateur.
Par exemple, lorsqu'un employé utilisant un navigateur en anglais recherche des documents japonais, ``content_ja`` n'est pas utilisé, et l'ordre des résultats varie d'un utilisateur à l'autre.
Pour éviter cela, fixez les langues de recherche avec ``query.default.languages``.

::

    query.default.languages=ja,en,zh-cn,zh-tw

Dans cet exemple, les quatre champs par langue sont ajoutés à la requête, quels que soient l'utilisateur et sa langue.
Chaque document ne possède qu'un seul champ pour sa propre langue ; les documents de toutes les langues bénéficient donc de l'analyse propre à leur langue dans les mêmes conditions.
En contrepartie, faire remonter une langue donnée avec « Langue préférée » n'a plus d'effet.
Si vos documents sont majoritairement en japonais, vous pouvez aussi n'indiquer qu'une seule langue, par exemple ``query.default.languages=ja``.

Écrivez le paramètre dans ``fess_config.properties`` et redémarrez Fess.
Le fichier se trouve dans ``app/WEB-INF/classes/fess_config.properties`` pour la version ZIP, et dans ``/etc/fess/fess_config.properties`` pour les versions RPM/DEB.
Avec Docker, ajoutez-le comme option JVM dans ``environment`` de ``fess01`` dans ``compose.yaml``, puis recréez le conteneur.

::

    - "FESS_JAVA_OPTS=-Dfess.config.query.default.languages=ja,en,zh-cn,zh-tw"

``FESS_JAVA_OPTS`` est découpé sur les espaces : n'utilisez pas d'espaces dans la valeur.
Lorsque le conteneur est recréé, les paramètres modifiés dans [Système] > [Général] sont perdus avec le fichier ``system.properties`` du conteneur (:doc:`guide-02`).

Le poids accordé aux correspondances dans les champs par langue se règle avec ``query.boost.title.lang`` et ``query.boost.content.lang``.
Après modification, comparez l'ordre des résultats de recherche en suivant les étapes de la section « Vérifier » ci-dessous.

Utiliser les dictionnaires selon la langue
==========================================

Les dictionnaires se modifient dans [Système] > [Dictionnaire].
Chaque dictionnaire agit sur des champs précis : si vous ne choisissez pas le dictionnaire qui agit sur le champ visé, les résultats de recherche ne changeront pas.

.. list-table::
   :header-rows: 1
   :widths: 24 36 40

   * - Dictionnaire (fichier)
     - Champs concernés
     - Usage dans un environnement multilingue
   * - Synonymes (``synonym.txt``)
     - ``content``, ``title`` (à la recherche uniquement)
     - Équivalences entre langues (« 会議 » et « meeting ») et variantes d'écriture. N'agit pas sur les champs par langue
   * - Kuromoji (``ja/kuromoji.txt``)
     - Champs ``_ja`` uniquement
     - Faire traiter des termes internes et des noms de produits comme un seul mot japonais
   * - Mots vides (``ja/stopwords.txt``)
     - Champs ``_ja`` uniquement
     - Mots à ne pas utiliser pour la recherche dans les documents japonais
   * - Mots vides (``en/stopwords.txt``)
     - ``content``, ``title`` et champs ``_en``
     - Mots anglais inutiles. Comme il agit sur les champs communs, il affecte les documents de toutes les langues
   * - Protwords (``en/protwords.txt``)
     - ``content``, ``title`` et champs ``_en``
     - Mots anglais à ne pas raciniser (noms de produits, par exemple)
   * - Remplacement de racinisation (``en/stemmer_override.txt``)
     - ``content``, ``title`` et champs ``_en``
     - Imposer le résultat de la racinisation anglaise
   * - Mappage (``mapping.txt``)
     - ``content``, ``title``
     - Remplacement de caractères. ``ja/mapping.txt`` est un fichier distinct pour les champs ``_ja``

Il n'existe pas de dictionnaire de mots protégés (Protwords) pour le japonais.
En effet, ``japanese_analyzer`` ne comporte pas de filtre qui lise les mots protégés.
Les champs du chinois simplifié et traditionnel n'ont pas de dictionnaire utilisateur modifiable depuis la console d'administration (les mots vides sont dans ``zh-cn/stopwords.txt`` et ``zh-tw/stopwords.txt``).

Synonymes entre langues
-----------------------

Pour trouver des documents en anglais à l'aide de mots japonais, enregistrez les traductions comme synonymes.
Dans le format du fichier à téléverser, placez sur une ligne les mots de même sens, séparés par des virgules.

::

    会議,ミーティング,meeting
    見積,quotation

Les synonymes sont développés dans les champs communs au moment de la recherche ; aucun nouveau crawl n'est donc nécessaire.
Pour les règles d'enregistrement, par exemple saisir les hiragana en katakana et les caractères alphanumériques pleine chasse en demi-chasse, consultez `Dictionnaire de synonymes <https://fess.codelibs.org/fr/stable/admin/synonym-guide.html>`__.

Dictionnaire utilisateur Kuromoji
---------------------------------

Dans le dictionnaire Kuromoji, on enregistre un token, ses tokens découpés, sa lecture (en katakana) et sa catégorie grammaticale.
Pour qu'un terme interne ou un nom de produit que Kuromoji découpe trop finement soit traité comme un seul mot, écrivez le même mot pour le token et pour les tokens découpés.

::

    東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞

Ce dictionnaire n'agit que sur les champs ``_ja``.
Le champ commun ``content`` est découpé en bigrammes ; modifier le dictionnaire Kuromoji ne change donc pas les correspondances dans ``content``.
L'effet n'apparaît que pour les recherches dont les langues de recherche incluent ``ja``, et uniquement sur les documents détectés comme japonais.

Appliquer les modifications de dictionnaire
-------------------------------------------

Enregistrer un dictionnaire ne suffit pas à modifier les résultats de recherche.

1. Ouvrez [Informations système] > [Maintenance] et cliquez sur [Recharger] dans « Recharger l'index des documents ». L'index est fermé puis rouvert ; pendant ce temps, les recherches renvoient une erreur ou 0 résultat. Effectuez cette opération à une heure de faible utilisation
2. Les synonymes ne servent qu'à la recherche : le rechargement suffit à les appliquer
3. Les autres dictionnaires (Kuromoji, Mappage, Mots vides, Protwords, Remplacement de racinisation) modifient aussi l'analyse effectuée lors de la construction de l'index. Les documents déjà indexés restent analysés avec l'ancien dictionnaire ; recrawlez donc les contenus concernés

Lors du nouveau crawl, si « Vérifier la dernière modification » est activé dans [Système] > [Général] (par défaut), les fichiers et pages non mis à jour ne sont pas récupérés à nouveau.
Désactivez-le temporairement, lancez le crawl, puis réactivez-le une fois le crawl terminé.

Vérifier
========

Voir le découpage en tokens avec l'API ``_analyze``
---------------------------------------------------

Le moyen le plus sûr de vérifier qu'un dictionnaire a été pris en compte est de soumettre, avec l'API ``_analyze`` d'OpenSearch, la même chaîne aux analyseurs du champ commun et du champ japonais, puis de comparer les résultats.
Dans l'environnement Docker de :doc:`guide-02`, OpenSearch est joignable sur le port 9200 de l'hôte.

::

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"japanese_analyzer","text":"全文検索エンジンを導入した"}'

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"standard_analyzer","text":"全文検索エンジンを導入した"}'

Avec ``japanese_analyzer``, le texte est découpé en mots et « を » et « た » sont supprimés.
Avec ``standard_analyzer``, il est découpé en unités de deux caractères comme « 全文 », « 文検 » et « 検索 ».
Après avoir enregistré « 東京スカイツリー » dans le dictionnaire Kuromoji et rechargé l'index, l'analyse de ce mot avec ``japanese_analyzer`` renvoie un seul token.
Un synonyme enregistré se vérifie en analysant « 会議 » avec ``"analyzer":"standard_search_analyzer"`` et en constatant qu'un token issu de « meeting » (racinisé en ``meet``) apparaît.

Vérifier dans les résultats de recherche
----------------------------------------

1. Sur la page de recherche, recherchez un mot présent à la fois dans des documents japonais et anglais
2. Dans [Options], basculez « Langue préférée » entre « Japonais » et « Anglais » et vérifiez que la langue des premiers documents change. Si vous avez défini ``query.default.languages``, vérifiez que l'ordre ne change pas lors du basculement
3. Après avoir enregistré des synonymes de traduction et rechargé l'index, vérifiez que ``lang:en 会議`` trouve des documents en anglais
4. Après avoir modifié le dictionnaire Kuromoji et recrawlé, recherchez le mot enregistré et vérifiez que les documents japonais qui le contiennent sont trouvés. Vérifiez le changement de découpage lui-même avec ``_analyze`` comme indiqué plus haut

Si les résultats ne changent pas, comparez la colonne « Champs concernés » du tableau des dictionnaires avec le ``lang`` du document.
Par exemple, ajouter à ``en/stopwords.txt`` un mot japonais de trois caractères ou plus n'a aucun effet, car dans les champs communs le texte devient des tokens de deux caractères qui ne correspondent jamais à ce mot.

Résumé
======

- Tous les documents sont interrogeables via les champs communs (``content``, ``title``), qui appliquent les bigrammes et la racinisation anglaise
- La langue détectée dans ``lang`` et les champs par langue (comme ``content_ja``) ajoutent une analyse adaptée à la langue
- Les langues de recherche sont déterminées dans l'ordre ``query.default.languages``, ``lang`` de la requête, puis langue du navigateur ; elles font remonter les documents au lieu de les filtrer
- Pour limiter par langue, indiquez le champ ``lang``, comme dans ``lang:en``
- Modifiez le dictionnaire qui agit sur le champ visé, et appliquez-le en rechargeant l'index des documents et, si nécessaire, en recrawlant

Pour aller plus loin
====================

- Trouver des points d'amélioration dans les journaux de recherche et les corriger avec des synonymes et des correspondances de clé : :doc:`guide-08`
- Crawler ensemble les sites web internes et les serveurs de fichiers : :doc:`guide-04`
- Trouver des documents de sens proche même lorsque les mots-clés ne correspondent pas : :doc:`guide-18`
- Appeler l'API de recherche depuis des systèmes métier : :doc:`guide-11`

Références
==========

- `Dictionnaire <https://fess.codelibs.org/fr/stable/admin/dict-guide.html>`__
- `Dictionnaire Kuromoji <https://fess.codelibs.org/fr/stable/admin/kuromoji-guide.html>`__
- `Dictionnaire de synonymes <https://fess.codelibs.org/fr/stable/admin/synonym-guide.html>`__
- `Dictionnaire de mots vides <https://fess.codelibs.org/fr/stable/admin/stopwords-guide.html>`__
- `Maintenance <https://fess.codelibs.org/fr/stable/admin/maintenance-guide.html>`__
- `Paramètres avancés liés à la recherche (langue par défaut pour la recherche) <https://fess.codelibs.org/fr/stable/config/search-advanced.html>`__
- `Configuration avancée du robot d'indexation <https://fess.codelibs.org/fr/stable/config/crawler-advanced.html>`__
- `Recherche par champ <https://fess.codelibs.org/fr/stable/user/search-field.html>`__
- `API de recherche <https://fess.codelibs.org/fr/stable/api/api-search.html>`__
