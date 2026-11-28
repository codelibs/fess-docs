===================================================
Améliorer la qualité de recherche avec les journaux
===================================================

Introduction
============

Une fois la recherche adoptée, les utilisateurs disent par exemple « le document que je cherche n'apparaît pas » ou « le document que je veux est enfoui tout en bas ».
Ce qui se passe pour chaque terme de recherche se lit dans les journaux de recherche et de clics enregistrés par Fess.

Dans Fess 15.9, l'écran [Informations système] > [Journal de recherche] de la console d'administration intègre un rapport d'analyse qui agrège des indicateurs comme le taux de zéro résultat et les positions de clic.
Cet article explique comment repérer sur cet écran les termes de recherche problématiques, choisir entre synonymes, correspondance de clé, boost de document, requêtes associées et mots vides pour les corriger, appliquer la correction, puis en vérifier l'effet sur le même écran.

L'agrégation personnalisée des journaux de recherche avec OpenSearch Dashboards est traitée dans :doc:`guide-22`, et l'analyse des documents mêlant japonais, anglais et chinois dans :doc:`guide-09`.

Ce qu'il faut regarder dans le journal de recherche
===================================================

Dans le menu de gauche, ouvrez [Informations système] > [Journal de recherche] : l'onglet [Aperçu] s'affiche.
Sa consultation requiert le rôle ``admin-searchlog`` ou ``admin-searchlog-view``.

En haut de chaque onglet, choisissez la période (« Aujourd’hui », « Hier », « 7 derniers jours », « 28 derniers jours », « 90 derniers jours », « Personnalisée ») et le type d'accès, puis cliquez sur [Appliquer].
Si vous activez « Comparer à la période précédente », les valeurs de la période antérieure de même durée s'affichent en regard.
Utilisez-le pour comparer l'avant et l'après d'une amélioration.

Les indicateurs qui orientent les améliorations, et les mesures efficaces pour chacun, sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 24 22 30 24

   * - Indicateur
     - Où il s'affiche
     - Ce qu'il indique
     - Principales mesures
   * - Taux de zéro résultat, requêtes sans résultat
     - Onglets [Aperçu] et [Requêtes]
     - La part des recherches qui n'ont renvoyé aucun résultat, et leurs termes de recherche
     - Synonymes, requêtes associées, ajout de documents
   * - Requêtes sans clic
     - Onglet [Requêtes]
     - Les termes de recherche qui ont renvoyé des résultats, mais dont aucun résultat n'a été cliqué
     - Correspondance de clé, boost de document
   * - Position moyenne des clics
     - Onglet [Requêtes] (par terme), onglet [Clics] (global)
     - La position à laquelle se trouvaient les résultats cliqués (le premier résultat vaut 1)
     - Correspondance de clé, boost de document
   * - Répartition des positions de clic, taux de consultation des pages suivantes
     - Onglet [Clics]
     - Si les clics se concentrent sur les positions 1 à 10, 11 à 20 ou à partir de 21, et la part des recherches où la page 2 ou suivante a été consultée
     - Correspondance de clé, boost de document
   * - Requêtes les plus fréquentes, URL les plus cliquées
     - Onglet [Aperçu], onglet [Clics]
     - Les termes les plus recherchés et les documents réellement ouverts
     - Vérifier les résultats en partant des termes en tête de liste

Gardez à l'esprit les points suivants concernant ces agrégats.

- L'enregistrement s'active avec « Journal de recherche » et « Journal utilisateur » dans [Système] > [Général] (tous deux activés par défaut). Si « Journal utilisateur » est désactivé, le nombre d'utilisateurs n'est pas compté.
- Un clic est enregistré lorsque « Journal de recherche » est activé et qu'un lien des résultats de recherche est ouvert via ``/go/``. La page de recherche du thème standard (bootstrap) construit ses liens de cette façon.
- Les indicateurs de clics par terme et les requêtes sans clic ne comptent que les clics à partir de 15.9, version depuis laquelle les clics sont enregistrés avec le terme de recherche.
- Si un nombre de jours est indiqué dans « Supprimer les anciens journaux de recherche » de [Général], les journaux plus anciens ne peuvent pas servir à la comparaison (la valeur par défaut ``-1`` ne supprime rien).
- Les journaux sont écrits par lots ; il peut donc s'écouler un peu de temps avant qu'une recherche apparaisse à l'écran.

Distinguer les causes des requêtes sans résultat
================================================

Cliquer sur une requête sans résultat dans l'onglet [Aperçu] ou [Requêtes] affiche, dans l'onglet [Journaux], les journaux de recherche de ce terme filtrés avec « Nombre de résultats » = « Sans résultat uniquement ».
Après avoir vérifié quand et avec quel type d'accès il a été recherché, recherchez réellement ce terme sur la page de recherche et classez la cause dans l'un des trois cas suivants.

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Situation
     - Mesure
     - Opération nécessaire pour l'appliquer
   * - Les documents existent mais emploient d'autres mots (p. ex. les utilisateurs cherchent « vacances », les documents parlent de « congés »)
     - Synonymes
     - Rechargement de l'index des documents
   * - Vous voulez orienter vers la formulation officielle (abréviations, anciens noms, fautes de frappe)
     - Requêtes associées
     - Aucune (appliqué à l'enregistrement)
   * - Aucun document correspondant dans l'index
     - Ajout de cibles d'exploration (:doc:`guide-04`)
     - Lancement d'une exploration

La correspondance de clé et le boost de document sont sans effet sur les requêtes sans résultat.
Tous deux font remonter les documents qui correspondent au terme de recherche, et aucun n'ajoute aux résultats des documents qui n'y correspondent pas.

Exemple pratique : corriger la requête sans résultat « vacances » avec un synonyme
==================================================================================

Supposons que « vacances » revienne sans cesse parmi les requêtes sans résultat de l'onglet [Requêtes], alors que les règlements internes emploient le mot « congés ».
Nous partons de cette situation pour aller de la correction jusqu'à la vérification.

1. Confirmer la cause
---------------------

Recherchez « congés » sur la page de recherche et vérifiez que les documents que les utilisateurs cherchaient vraisemblablement sont trouvés.
S'ils ne le sont pas, le problème ne vient pas des mots : les documents ne sont pas dans l'index.
Revoyez alors les cibles d'exploration plutôt que d'ajouter un synonyme.

2. Enregistrer le synonyme
--------------------------

1. Ouvrez [Système] > [Dictionnaire] et, dans la liste, cliquez sur la ligne dont le « Type » est ``synonym`` (celle dont le nom se termine par ``synonym.txt``).
2. Cliquez sur [Créer nouveau].
3. Saisissez les deux lignes suivantes à la fois dans « Source » et dans « Cible », puis cliquez sur [Créer].

::

    vacances
    congés

Si « Source » et « Cible » contiennent les mêmes mots, le dictionnaire les enregistre sur une seule ligne ``vacances,congés``, et une recherche sur l'un des deux mots trouve aussi les documents qui contiennent l'autre.
Pour n'élargir que les recherches sur « vacances », mettez la seule ligne « vacances » dans « Source » et les deux lignes ci-dessus dans « Cible » (cela donne ``vacances=>vacances,congés``).
Attention : si « Cible » ne contient pas le mot d'origine, la recherche ne porte plus sur ce mot lui-même.

Écrivez un mot par ligne dans les champs de saisie.
Les mots contenant une virgule (,) ou ``=>`` ne peuvent pas être enregistrés.
La référence du dictionnaire de synonymes énonce les règles d'enregistrement suivantes.

- Enregistrer les hiragana en katakana, les petits katakana en katakana de taille normale, et les caractères alphanumériques pleine chasse en demi-chasse
- Par défaut, le texte japonais et les autres textes CJK sont indexés en bi-grammes découpés tous les deux caractères ; n'enregistrez donc pas de mots d'un seul caractère
- Ne pas enregistrer plusieurs fois le même mot

Les synonymes s'appliquent aux champs ``content`` et ``title`` et développent les mots au moment de la recherche.
Il n'est pas nécessaire de réindexer.

3. Appliquer la modification du dictionnaire
--------------------------------------------

Le simple enregistrement du dictionnaire ne modifie pas les résultats de recherche.
L'index ouvert continue de fonctionner avec l'ancien dictionnaire.

1. Ouvrez [Informations système] > [Maintenance].
2. Sous « Recharger l'index des documents », cliquez sur [Recharger].

Ce bouton écrit les dictionnaires enregistrés dans des fichiers, puis ferme l'index des documents et le rouvre.

.. warning::

   Pendant que l'index est fermé, puis après sa réouverture jusqu'à l'allocation des shards, aucune recherche n'est possible : elles renvoient des erreurs ou 0 résultat.
   Plus l'index est volumineux, plus cela prend de temps ; exécutez donc l'opération à un moment de faible utilisation.

4. Vérifier l'effet
-------------------

Recherchez d'abord « vacances » sur la page de recherche et vérifiez que des documents contenant « congés » sont trouvés.

Ensuite, dans l'onglet [Journaux] de [Informations système] > [Journal de recherche], filtrez en saisissant « vacances » dans « Mot recherché » et en choisissant « Un résultat ou plus » pour « Nombre de résultats ».
Si les recherches effectuées par les utilisateurs après la modification sont enregistrées avec des résultats, la correction fonctionne.

Après quelques jours, dans l'onglet [Aperçu], réglez la période sur « Personnalisée », fixez la date de début au lendemain de la modification et activez « Comparer à la période précédente ».
Les périodes sont découpées par jour (dates dans le fuseau horaire du serveur) ; si vous incluez le jour de la modification, les recherches sans résultat antérieures à la modification sont aussi comptées.
Vérifiez que le taux de zéro résultat est inférieur à celui de la période précédente et que « vacances » a disparu de la liste des requêtes sans résultat.
Si vous laissez la période sur « 7 derniers jours » par exemple, les recherches sans résultat antérieures à la modification restent dans la période, et le terme ne disparaît pas immédiatement de la liste.

Le contenu du dictionnaire peut être enregistré dans un fichier avec [Télécharger] sur l'écran de liste.
En l'enregistrant avant et après une modification, vous pourrez revenir en arrière si nécessaire.

Faire remonter un document ciblé : correspondance de clé
========================================================

Les termes dont la position moyenne des clics est élevée dans l'onglet [Requêtes], ou qui figurent parmi les requêtes sans clic, correspondent peut-être à des cas où le bon document est trouvé mais enfoui loin dans les résultats.
Les URL les plus cliquées de l'onglet [Clics] montrent quels documents les utilisateurs finissent par ouvrir.
La correspondance de clé permet de faire remonter un tel document pour un terme de recherche donné.

Dans [Robot d'exploration] > [Correspondance de clé], cliquez sur [Créer nouveau], saisissez les valeurs suivantes et cliquez sur [Créer].

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Champ
     - Exemple
     - Description
   * - Terme
     - ``remboursement``
     - S'applique lorsqu'un mot des mots-clés de recherche correspond à cette valeur (sans distinction de casse). Indiquez un seul mot
   * - Requête
     - ``url:"https://portal.example.com/manual/expense.html"``
     - Requête de recherche qui sélectionne les documents à faire remonter
   * - Taille
     - ``10`` (valeur par défaut)
     - Nombre maximal de documents correspondant à la requête qui sont ciblés
   * - Boost
     - ``100`` (valeur par défaut)
     - Poids multiplié au score des documents ciblés

Entourez toujours l'URL de la requête de ``"``.
Sans guillemets, comme dans ``url:https://...``, l'analyse de la requête échoue sur le ``:`` de l'URL ; la correspondance de clé n'est pas chargée et n'a aucun effet (seul un WARN est écrit dans ``fess.log``).
Le champ ``url`` exige une correspondance exacte : la valeur doit être identique, caractère pour caractère, à l'URL indexée.
Avant l'enregistrement, lancez la même requête sur la page de recherche et vérifiez qu'elle trouve exactement le document visé.

Aucun rechargement comme pour les dictionnaires n'est nécessaire.
L'enregistrement lance en arrière-plan le rechargement des correspondances de clé, et la bascule a lieu une fois toutes les entrées lues.
Le chargement marque une pause d'une seconde entre chaque entrée ; avec beaucoup d'entrées, la prise d'effet prend donc du temps.

Vérifiez le résultat sur l'écran de détail de la correspondance de clé enregistrée, ouvert depuis la liste.
Si l'URL du document visé s'affiche dans le champ « URL », elle est active.
Juste après l'enregistrement, le rechargement n'est pas forcément terminé et le champ peut être vide.
S'il est toujours vide après un court délai et une réouverture de l'écran de détail, la requête ne correspond à aucun document.
Les documents correspondant à la requête sont recalculés à l'enregistrement et à la fin de chaque tâche d'exploration.
Un document pas encore exploré devient donc une cible après la prochaine exploration.

Notez aussi que seuls les documents correspondant au terme de recherche sont ciblés.
Si une recherche sur « remboursement » ne trouve pas du tout le document visé, enregistrer une correspondance de clé ne le fera pas apparaître dans les résultats.

Faire remonter un site ou un ensemble de documents : boost de document
======================================================================

Pour faire remonter un ensemble de documents donné, comme le site des manuels officiels, quel que soit le terme de recherche, utilisez [Robot d'exploration] > [Boost de document].

Cliquez sur [Créer nouveau] et saisissez les valeurs suivantes.

- Condition : ``url.startsWith("https://portal.example.com/manual/")``
- Expression de boost : ``10``
- Type de Script : ``javascript`` (prérempli à la création)
- Ordre de tri : ``0``

La condition et l'expression de boost sont évaluées comme des expressions de script, et chaque champ du document est utilisable comme variable.
Pour les documents dont la condition renvoie ``true``, la valeur de l'expression de boost est placée dans le champ ``boost``.
Il s'agit du même champ que « Boost » des configurations d'exploration web et de système de fichiers (1.0 par défaut) ; pour les documents qui correspondent à une règle, c'est la valeur de la règle qui est utilisée.
Si un document correspond à plusieurs règles, c'est la règle dont l'ordre de tri est le plus petit qui s'applique.
En JavaScript, ne terminez pas l'expression par un point-virgule.
Avec un point-virgule, la valeur devient ``null`` et la règle n'a aucun effet.

Le boost de document ne prend pas effet de la même manière que la correspondance de clé et les synonymes.

- Les règles sont évaluées lorsque les documents sont enregistrés dans l'index par l'exploration web ou de fichiers. Elles ne s'appliquent pas aux documents issus d'une exploration de magasin de données.
- Ajouter ou modifier une règle ne change pas les valeurs des documents déjà indexés.
- Lorsque « Vérifier la dernière modification » est activé dans [Général] (par défaut), les documents dont le contenu n'a pas changé ne sont pas réenregistrés lors d'une nouvelle exploration. Pour appliquer la règle aux documents existants, supprimez les documents concernés dans [Informations système] > [Rechercher], puis relancez l'exploration.

Une fois la règle appliquée, recherchez des mots qui correspondent à cet ensemble de documents pour vérifier que leur position a progressé, puis, après un certain temps, comparez la position moyenne des clics de l'onglet [Requêtes] avec la période précédente.

Proposer une autre formulation : requêtes associées
===================================================

Pour suggérer une recherche avec un autre mot sans élargir le terme de recherche de l'utilisateur, utilisez les requêtes associées.
Dans [Robot d'exploration] > [Requête associée], cliquez sur [Créer nouveau], saisissez le mot des utilisateurs dans « Terme » (p. ex. ``VPN``) et les mots suggérés dans « Requêtes », un par ligne (p. ex. ``accès à distance``, ``connexion externe``).

Avec le thème standard (bootstrap), lorsque le terme de recherche correspond, des boutons s'affichent au-dessus des résultats sous « Recherches associées: ».
Ils s'affichent aussi sur une page de résultats vide, ce qui permet de guider les utilisateurs depuis les requêtes sans résultat.
Le terme est comparé à l'ensemble de la chaîne de recherche saisie (sans distinction de casse).
La modification prend effet à l'enregistrement, sans rechargement.

Avec [Générer à partir des journaux de recherche] sur l'écran de liste, des requêtes associées peuvent être créées automatiquement à partir de paires de mots que le même utilisateur a recherchées de nouveau à court intervalle.
Il faut pour cela que « Journal de recherche » et « Journal utilisateur » soient tous deux activés dans [Général].
Les termes qui ont déjà une requête associée ne sont pas modifiés.
Pour les conditions de génération et les paramètres permettant de les ajuster, consultez `Requête associée <https://fess.codelibs.org/fr/stable/admin/relatedquery-guide.html>`__.

Avant d'utiliser les mots vides
===============================

Si un mot présent dans tous les documents (par exemple un mot anglais du pied de page de toutes les pages) se mêle aux termes de recherche et élargit trop les résultats, vous pouvez l'exclure de l'analyse avec les mots vides.
Chaque fichier de dictionnaire de mots vides ne s'applique toutefois qu'à certains champs.

- ``en/stopwords.txt`` sert à l'analyse de ``content``, ``title`` et des champs se terminant par ``_en``.
- ``ja/stopwords.txt`` ne sert qu'aux champs se terminant par ``_ja``, comme ``content_ja`` et ``title_ja``, des documents détectés comme japonais. Il est vide par défaut.

Prenons l'exemple d'un texte japonais : les particules comme « の » et « は » sont supprimées par le filtre de catégories grammaticales dans les champs ``_ja``, mais pas dans ``content`` et ``title``.
Dans ``content`` et ``title``, le texte japonais est découpé par unités de deux caractères, et les hiragana sont convertis en katakana avant la comparaison (« VPNとは » devient ``vpn`` et ``トハ``).
Ajouter un mot japonais à ``en/stopwords.txt`` ne le supprime donc que s'il correspond exactement à une unité de deux caractères issue de ce découpage.
Utilisez les mots vides principalement pour des mots anglais, et vérifiez leur effet avec l'API ``_analyze`` d'OpenSearch.

.. code-block:: bash

    curl -X POST "localhost:9200/fess.search/_analyze" -H "Content-Type: application/json" \
      -d '{"analyzer": "standard_search_analyzer", "text": "VPNとは"}'

Les mots vides s'appliquent à la fois à l'indexation et à la recherche.
Après avoir enregistré le dictionnaire, rechargez l'index des documents comme pour les synonymes, et relancez l'exploration pour retirer aussi les mots des documents déjà indexés.
Pour le fonctionnement des champs propres à chaque langue, consultez :doc:`guide-09`.

En cas de problème
==================

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptôme
     - Points à vérifier
   * - Le synonyme est enregistré mais les résultats ne changent pas
     - L'index des documents a-t-il été rechargé ? L'entrée respecte-t-elle les règles d'enregistrement (hiragana, mots d'un seul caractère, etc.) ?
   * - La correspondance de clé ne fonctionne pas
     - Le champ « URL » de l'écran de détail est-il vide ? L'URL de la requête est-elle entourée de ``"`` ? Les mots-clés de l'utilisateur contiennent-ils exactement le même mot que le terme, en tant que mot distinct (une autre forme, comme le pluriel « remboursements », ne correspond pas) ? Le document visé est-il trouvé avec ce mot ?
   * - Le boost de document ne fonctionne pas
     - S'agit-il de documents d'un magasin de données ? Les documents ont-ils été réenregistrés après l'ajout de la règle ? La condition se termine-t-elle par un point-virgule ?
   * - Les requêtes associées ne s'affichent pas
     - Le terme correspond-il à l'ensemble de la chaîne de recherche ? Si vous utilisez votre propre thème, est-il conçu pour afficher les requêtes associées ?
   * - Les indicateurs de clics sont vides
     - « Journal de recherche » est-il activé dans [Général] ? Les liens des résultats passent-ils par ``/go/`` ? La période ne contient-elle que des clics enregistrés avant 15.9 ?

Pour aller plus loin
====================

- Agréger soi-même les journaux de recherche avec OpenSearch Dashboards : :doc:`guide-22`
- Améliorer la recherche dans des documents mêlant japonais, anglais et chinois : :doc:`guide-09`
- La cause des recherches sans résultat était l'absence de documents : :doc:`guide-04`
- Afficher des documents proches par le sens même quand les mots ne correspondent pas : :doc:`guide-18`
- Gérer les paramètres de dictionnaire et de correspondance de clé sous forme de code : :doc:`guide-16`

Références
==========

- `Journal de recherche <https://fess.codelibs.org/fr/stable/admin/searchlog-guide.html>`__
- `Dictionnaire <https://fess.codelibs.org/fr/stable/admin/dict-guide.html>`__
- `Dictionnaire de synonymes <https://fess.codelibs.org/fr/stable/admin/synonym-guide.html>`__
- `Dictionnaire de mots vides <https://fess.codelibs.org/fr/stable/admin/stopwords-guide.html>`__
- `Correspondance de clé <https://fess.codelibs.org/fr/stable/admin/keymatch-guide.html>`__
- `Boost de document <https://fess.codelibs.org/fr/stable/admin/boostdoc-guide.html>`__
- `Requête associée <https://fess.codelibs.org/fr/stable/admin/relatedquery-guide.html>`__
- `Maintenance <https://fess.codelibs.org/fr/stable/admin/maintenance-guide.html>`__
