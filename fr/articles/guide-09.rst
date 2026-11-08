==========================================================================
Partie 9 : Infrastructure de recherche pour les organisations multilingues
==========================================================================

Introduction
=============

Dans les entreprises opérant à l'échelle mondiale ou dans les organisations comptant des employés de diverses nationalités, les documents internes sont rédigés dans plusieurs langues.
Une infrastructure de recherche capable de traiter correctement des documents dans un environnement multilingue -- tels que des comptes-rendus de réunion en japonais, des spécifications techniques en anglais et des rapports de marché en chinois -- est indispensable.

Dans cet article, nous supposons un environnement où coexistent des documents en japonais, en anglais et en chinois, et nous mettons en place un environnement permettant de rechercher correctement les documents dans chaque langue.

Public cible
=============

- Administrateurs d'organisations gérant des documents multilingues
- Personnes souhaitant améliorer la qualité de recherche dans des langues autres que le japonais
- Personnes souhaitant apprendre les bases des Analyzers de recherche en texte intégral

Scénario
========

Nous supposons une entreprise disposant de bureaux au Japon, aux États-Unis et en Chine.

- Bureau du Japon : Création de documents en japonais (spécifications, comptes-rendus de réunion, rapports)
- Bureau des États-Unis : Création de documents en anglais (documents techniques, supports de présentation)
- Bureau de Chine : Création de documents en chinois (études de marché, informations sur les partenaires commerciaux)
- Commun : Documents de politique globale rédigés en anglais

L'objectif est de créer un environnement dans lequel les employés de chaque bureau peuvent rechercher des documents quelle que soit la langue.

Fondamentaux de la recherche multilingue
==========================================

Traitement linguistique dans la recherche en texte intégral
-------------------------------------------------------------

Pour qu'un moteur de recherche en texte intégral rende les documents consultables, il doit découper le texte en ``tokens`` (unités consultables).
Ce processus s'appelle la ``tokenisation``.

La méthode de tokenisation diffère considérablement selon la langue.

**Anglais** : Les mots séparés par des espaces deviennent directement des tokens.
De plus, le stemming (par exemple, running -> run) et la mise en minuscules sont appliqués.

**Japonais** : Les mots n'étant pas séparés par des espaces, un analyseur morphologique (tel que Kuromoji) est utilisé pour découper le texte en mots.
Par exemple, une expression est découpée comme suit : ``serveur de recherche en texte integral`` -> ``texte integral`` ``recherche`` ``serveur``.

**Chinois** : Comme en japonais, les mots ne sont pas séparés par des espaces, un tokeniseur dédié est donc nécessaire. Fess utilise son propre tokeniseur chinois pour le traitement.

Support multilingue de Fess
-----------------------------

Fess utilise OpenSearch comme backend et peut exploiter les Analyzers multilingues fournis par OpenSearch.
Dans la configuration par défaut de Fess, l'Analyzer japonais (Kuromoji) est activé, mais d'autres langues sont également prises en charge.

Fess dispose de paramètres d'index prenant en charge plus de 20 langues, avec une fonctionnalité qui détecte automatiquement la langue d'un document et applique l'Analyzer approprié.

Configuration par langue
=========================

Configuration pour le japonais
--------------------------------

Les documents en japonais sont traités par le Kuromoji Analyzer.
Le japonais étant correctement traité par les paramètres par défaut de Fess, aucune configuration supplémentaire spéciale n'est requise.

Cependant, la qualité de recherche peut être améliorée grâce aux personnalisations suivantes.

**Dictionnaire utilisateur**

Enregistrez les termes spécifiques à l'industrie et la terminologie interne dans le dictionnaire.
Cela peut être configuré en sélectionnant le dictionnaire Kuromoji depuis [Système] > [Dictionnaire] dans la console d'administration.

Par exemple, cela est utile lorsque vous souhaitez qu'un terme composé soit traité comme un seul token plutôt que d'être découpé en mots séparés.

**Synonymes**

Gestion des variantes d'écriture spécifiques au japonais.

::

    サーバー,サーバ
    データベース,DB,ディービー
    ユーザー,ユーザ,利用者

Configuration pour l'anglais
------------------------------

Les documents en anglais sont automatiquement traités avec l'Analyzer approprié grâce à l'index multilingue de Fess.

Les personnalisations spécifiques à l'anglais comprennent les éléments suivants.

**Mots vides (Stop Words)**

Les mots vides courants de l'anglais (the, a, an, is, are, etc.) sont exclus par défaut, mais des mots vides spécifiques à l'industrie peuvent également être ajoutés.

**Remplacement du Stemmer**

Remplacez le stemming de mots spécifiques.
Cela peut être configuré en sélectionnant le dictionnaire de remplacement du Stemmer depuis [Système] > [Dictionnaire] dans la console d'administration.

Par exemple, cela est utilisé lorsque des termes techniques subissent des transformations non souhaitées.

Configuration pour le chinois
-------------------------------

Les documents en chinois utilisent le tokeniseur chinois propre à Fess.
Dans l'index multilingue de Fess, les textes en chinois simplifié et en chinois traditionnel sont tous deux correctement tokenisés.

Les considérations spécifiques au chinois comprennent les éléments suivants.

- Correspondance entre les caractères chinois simplifiés et traditionnels
- Prise en charge de la recherche par saisie Pinyin
- Configuration de synonymes spécifiques au chinois

Expérience de recherche dans un environnement multilingue
==========================================================

Considérations relatives à l'interface de recherche
------------------------------------------------------

Dans un environnement multilingue, l'interface de recherche doit également s'adapter à la langue de l'utilisateur.

Fess dispose d'une fonctionnalité qui bascule automatiquement la langue de l'interface en fonction des paramètres linguistiques du navigateur.
L'interface de l'écran de recherche est proposée dans plusieurs langues, dont le japonais, l'anglais et le chinois.

Considérations relatives à la recherche translinguistique
-----------------------------------------------------------

Il existe également un besoin de recherche translinguistique, comme ``trouver des documents en anglais a l'aide de mots-cles en japonais``.
À l'heure actuelle, Fess seul ne prend pas en charge la recherche basée sur la traduction entièrement automatique, mais les méthodes suivantes permettent d'y répondre partiellement.

**Configuration de synonymes multilingues**

Enregistrez les traductions entre le japonais et l'anglais comme synonymes.

::

    会議,meeting,ミーティング
    報告書,report,レポート
    仕様書,specification,スペック

Ainsi, une recherche avec le mot japonais pour ``reunion`` renverra également des documents en anglais contenant ``meeting``.

**Filtrage par langue avec des étiquettes**

Configurez des étiquettes pour chaque langue afin que les utilisateurs puissent sélectionner le périmètre linguistique de leur recherche.

- ``lang-ja`` : Documents en japonais
- ``lang-en`` : Documents en anglais
- ``lang-zh`` : Documents en chinois

Bonnes pratiques de gestion des dictionnaires
===============================================

Dans un environnement multilingue, la gestion des dictionnaires a un impact significatif sur la qualité de recherche.

Maintenance des dictionnaires par langue
------------------------------------------

.. list-table:: Points de maintenance des dictionnaires
   :header-rows: 1
   :widths: 20 40 40

   * - Dictionnaire
     - Japonais
     - Anglais / Chinois
   * - Synonymes
     - Variantes d'écriture, abréviations, termes techniques
     - Développement d'abréviations, synonymes
   * - Mots vides
     - Mots inutiles spécifiques à l'industrie
     - Mots inutiles spécifiques au domaine
   * - Dictionnaire utilisateur
     - Termes internes, noms de produits
     - (Spécifique à Kuromoji)
   * - Protwords (Mots protégés)
     - Mots ne devant pas être soumis au stemming
     - Termes techniques, noms propres

Maintenance régulière des dictionnaires
-----------------------------------------

Les dictionnaires ne sont pas quelque chose que l'on configure une fois pour toutes ; ils doivent être revus régulièrement.

- Ajouter de nouveaux noms de produits et de projets
- Nettoyer les termes qui ne sont plus utilisés
- Ajouter de nouveaux candidats synonymes découverts dans les journaux de recherche

Combinez cela avec le cycle d'optimisation de la qualité de recherche présenté dans la Partie 8 pour maintenir les dictionnaires de façon continue.

Synthèse
========

Dans cet article, nous avons expliqué comment mettre en place une infrastructure de recherche dans un environnement où coexistent des documents en japonais, en anglais et en chinois.

- Compréhension des différents processus de tokenisation pour chaque langue
- Index multilingue et configuration des Analyzers de Fess
- Personnalisation pour le japonais (Kuromoji), l'anglais et le chinois
- Prise en charge de la recherche translinguistique grâce aux synonymes multilingues
- Bonnes pratiques de gestion des dictionnaires

Le support multilingue ne peut pas être achevé par une seule configuration ; l'amélioration continue en fonction des modes d'utilisation est essentielle.

Dans le prochain article, nous traiterons de l'exploitation stable des systèmes de recherche.

Références
==========

- `Gestion des dictionnaires Fess <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__

- `OpenSearch Analyzer <https://opensearch.org/docs/latest/analyzers/>`__
