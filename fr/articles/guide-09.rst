===========================================================================
Partie 9 : Infrastructure de recherche pour les organisations multilingues -- Mise en place d'un environnement pour rechercher correctement des documents en japonais, anglais et chinois
===========================================================================

Introduction
=============

Dans les entreprises operant a l'echelle mondiale ou dans les organisations comptant des employes de diverses nationalites, les documents internes sont rediges dans plusieurs langues.
Une infrastructure de recherche capable de traiter correctement des documents dans un environnement multilingue -- tels que des comptes-rendus de reunion en japonais, des specifications techniques en anglais et des rapports de marche en chinois -- est indispensable.

Dans cet article, nous supposons un environnement ou coexistent des documents en japonais, en anglais et en chinois, et nous mettons en place un environnement permettant de rechercher correctement les documents dans chaque langue.

Public cible
=============

- Administrateurs d'organisations gerant des documents multilingues
- Personnes souhaitant ameliorer la qualite de recherche dans des langues autres que le japonais
- Personnes souhaitant apprendre les bases des Analyzers de recherche en texte integral

Scenario
========

Nous supposons une entreprise disposant de bureaux au Japon, aux Etats-Unis et en Chine.

- Bureau du Japon : Creation de documents en japonais (specifications, comptes-rendus de reunion, rapports)
- Bureau des Etats-Unis : Creation de documents en anglais (documents techniques, supports de presentation)
- Bureau de Chine : Creation de documents en chinois (etudes de marche, informations sur les partenaires commerciaux)
- Commun : Documents de politique globale rediges en anglais

L'objectif est de creer un environnement dans lequel les employes de chaque bureau peuvent rechercher des documents quelle que soit la langue.

Fondamentaux de la recherche multilingue
==========================================

Traitement linguistique dans la recherche en texte integral
-------------------------------------------------------------

Pour qu'un moteur de recherche en texte integral rende les documents consultables, il doit decouper le texte en ``tokens`` (unites consultables).
Ce processus s'appelle la ``tokenisation``.

La methode de tokenisation differe considerablement selon la langue.

**Anglais** : Les mots separes par des espaces deviennent directement des tokens.
De plus, le stemming (par exemple, running -> run) et la mise en minuscules sont appliques.

**Japonais** : Les mots n'etant pas separes par des espaces, un analyseur morphologique (tel que Kuromoji) est utilise pour decouper le texte en mots.
Par exemple, une expression est decoupee comme suit : ``serveur de recherche en texte integral`` -> ``texte integral`` ``recherche`` ``serveur``.

**Chinois** : Comme en japonais, les mots ne sont pas separes par des espaces, un tokeniseur dedie est donc necessaire. Fess utilise son propre tokeniseur chinois pour le traitement.

Support multilingue de Fess
-----------------------------

Fess utilise OpenSearch comme backend et peut exploiter les Analyzers multilingues fournis par OpenSearch.
Dans la configuration par defaut de Fess, l'Analyzer japonais (Kuromoji) est active, mais d'autres langues sont egalement prises en charge.

Fess dispose de parametres d'index prenant en charge plus de 20 langues, avec une fonctionnalite qui detecte automatiquement la langue d'un document et applique l'Analyzer approprie.

Configuration par langue
=========================

Configuration pour le japonais
--------------------------------

Les documents en japonais sont traites par le Kuromoji Analyzer.
Le japonais etant correctement traite par les parametres par defaut de Fess, aucune configuration supplementaire speciale n'est requise.

Cependant, la qualite de recherche peut etre amelioree grace aux personnalisations suivantes.

**Dictionnaire utilisateur**

Enregistrez les termes specifiques a l'industrie et la terminologie interne dans le dictionnaire.
Cela peut etre configure en selectionnant le dictionnaire Kuromoji depuis [Systeme] > [Dictionnaire] dans la console d'administration.

Par exemple, cela est utile lorsque vous souhaitez qu'un terme compose soit traite comme un seul token plutot que d'etre decoupe en mots separes.

**Synonymes**

Gestion des variantes d'ecriture specifiques au japonais.

::

    サーバー,サーバ
    データベース,DB,ディービー
    ユーザー,ユーザ,利用者

Configuration pour l'anglais
------------------------------

Les documents en anglais sont automatiquement traites avec l'Analyzer approprie grace a l'index multilingue de Fess.

Les personnalisations specifiques a l'anglais comprennent les elements suivants.

**Mots vides (Stop Words)**

Les mots vides courants de l'anglais (the, a, an, is, are, etc.) sont exclus par defaut, mais des mots vides specifiques a l'industrie peuvent egalement etre ajoutes.

**Remplacement du Stemmer**

Remplacez le stemming de mots specifiques.
Cela peut etre configure en selectionnant le dictionnaire de remplacement du Stemmer depuis [Systeme] > [Dictionnaire] dans la console d'administration.

Par exemple, cela est utilise lorsque des termes techniques subissent des transformations non souhaitees.

Configuration pour le chinois
-------------------------------

Les documents en chinois utilisent le tokeniseur chinois propre a Fess.
Dans l'index multilingue de Fess, les textes en chinois simplifie et en chinois traditionnel sont tous deux correctement tokenises.

Les considerations specifiques au chinois comprennent les elements suivants.

- Correspondance entre les caracteres chinois simplifies et traditionnels
- Prise en charge de la recherche par saisie Pinyin
- Configuration de synonymes specifiques au chinois

Experience de recherche dans un environnement multilingue
==========================================================

Considerations relatives a l'interface de recherche
------------------------------------------------------

Dans un environnement multilingue, l'interface de recherche doit egalement s'adapter a la langue de l'utilisateur.

Fess dispose d'une fonctionnalite qui bascule automatiquement la langue de l'interface en fonction des parametres linguistiques du navigateur.
L'interface de l'ecran de recherche est proposee dans plusieurs langues, dont le japonais, l'anglais et le chinois.

Considerations relatives a la recherche translinguistique
-----------------------------------------------------------

Il existe egalement un besoin de recherche translinguistique, comme ``trouver des documents en anglais a l'aide de mots-cles en japonais``.
A l'heure actuelle, Fess seul ne prend pas en charge la recherche basee sur la traduction entierement automatique, mais les methodes suivantes permettent d'y repondre partiellement.

**Configuration de synonymes multilingues**

Enregistrez les traductions entre le japonais et l'anglais comme synonymes.

::

    会議,meeting,ミーティング
    報告書,report,レポート
    仕様書,specification,スペック

Ainsi, une recherche avec le mot japonais pour ``reunion`` renverra egalement des documents en anglais contenant ``meeting``.

**Filtrage par langue avec des etiquettes**

Configurez des etiquettes pour chaque langue afin que les utilisateurs puissent selectionner le perimetre linguistique de leur recherche.

- ``lang-ja`` : Documents en japonais
- ``lang-en`` : Documents en anglais
- ``lang-zh`` : Documents en chinois

Bonnes pratiques de gestion des dictionnaires
===============================================

Dans un environnement multilingue, la gestion des dictionnaires a un impact significatif sur la qualite de recherche.

Maintenance des dictionnaires par langue
------------------------------------------

.. list-table:: Points de maintenance des dictionnaires
   :header-rows: 1
   :widths: 20 40 40

   * - Dictionnaire
     - Japonais
     - Anglais / Chinois
   * - Synonymes
     - Variantes d'ecriture, abreviations, termes techniques
     - Developpement d'abreviations, synonymes
   * - Mots vides
     - Mots inutiles specifiques a l'industrie
     - Mots inutiles specifiques au domaine
   * - Dictionnaire utilisateur
     - Termes internes, noms de produits
     - (Specifique a Kuromoji)
   * - Protwords (Mots proteges)
     - Mots ne devant pas etre soumis au stemming
     - Termes techniques, noms propres

Maintenance reguliere des dictionnaires
-----------------------------------------

Les dictionnaires ne sont pas quelque chose que l'on configure une fois pour toutes ; ils doivent etre revus regulierement.

- Ajouter de nouveaux noms de produits et de projets
- Nettoyer les termes qui ne sont plus utilises
- Ajouter de nouveaux candidats synonymes decouverts dans les journaux de recherche

Combinez cela avec le cycle d'optimisation de la qualite de recherche presente dans la Partie 8 pour maintenir les dictionnaires de facon continue.

Synthese
========

Dans cet article, nous avons explique comment mettre en place une infrastructure de recherche dans un environnement ou coexistent des documents en japonais, en anglais et en chinois.

- Comprehension des differents processus de tokenisation pour chaque langue
- Index multilingue et configuration des Analyzers de Fess
- Personnalisation pour le japonais (Kuromoji), l'anglais et le chinois
- Prise en charge de la recherche translinguistique grace aux synonymes multilingues
- Bonnes pratiques de gestion des dictionnaires

Le support multilingue ne peut pas etre acheve par une seule configuration ; l'amelioration continue en fonction des modes d'utilisation est essentielle.

Dans le prochain article, nous traiterons de l'exploitation stable des systemes de recherche.

References
==========

- `Gestion des dictionnaires Fess <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__

- `OpenSearch Analyzer <https://opensearch.org/docs/latest/analyzers/>`__
