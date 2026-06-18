========================
Fonction de recherche
========================

Aperçu
======

|Fess| offre une puissante fonction de recherche en texte intégral.
Cette section décrit les paramètres détaillés et les méthodes d'utilisation de la fonction de recherche.

Affichage du nombre de résultats de recherche
=============================================

Comportement par défaut
-----------------------

La valeur par défaut de ``query.track.total.hits`` est ``10000``.
Ainsi, lorsque les résultats de recherche dépassent 10 000 éléments, le nombre affiché sur l'écran des résultats est « environ 10 000 ou plus ».
Il s'agit du paramètre par défaut qui limite à la valeur de ``query.track.total.hits`` le nombre exact de correspondances totales calculé par OpenSearch, afin de réduire l'impact sur les performances lors de recherches à grande échelle.

Exemple de recherche

|image0|

.. |image0| image:: ../../../resources/images/fr/15.7/config/search-result.png

Affichage du nombre exact de correspondances
--------------------------------------------

Pour afficher le nombre exact de correspondances au-delà de 10 000 éléments, modifiez le paramètre ``query.track.total.hits`` dans ``fess_config.properties``.

::

    query.track.total.hits=100000

Dans l'exemple ci-dessus, le nombre exact de correspondances peut être obtenu jusqu'à 100 000 éléments.
Le seuil à partir duquel l'affichage indique « environ N ou plus » évolue également en fonction de cette valeur de configuration.
Cependant, une valeur élevée peut affecter les performances.

.. warning::
   Une valeur trop élevée peut dégrader les performances de recherche.
   Veuillez définir une valeur appropriée en fonction de votre situation d'utilisation réelle.

Options de recherche
====================

Recherche de base
-----------------

Dans |Fess|, une recherche en texte intégral est exécutée simplement en saisissant des mots-clés dans la zone de recherche.
La saisie de plusieurs mots-clés effectue une recherche ET (AND).

::

    recherche moteur

Dans l'exemple ci-dessus, les documents contenant à la fois « recherche » et « moteur » sont recherchés.

Recherche OU (OR)
-----------------

Pour effectuer une recherche OU, insérez ``OR`` entre les mots-clés.

::

    recherche OR moteur

Recherche NON (NOT)
-------------------

Pour exclure un mot-clé spécifique, ajoutez ``-`` (signe moins) devant le mot-clé.

::

    recherche -moteur

Recherche de phrase
-------------------

Pour rechercher une phrase exacte, entourez-la de guillemets doubles.

::

    "moteur de recherche"

Recherche par champ spécifique
------------------------------

Vous pouvez effectuer une recherche en spécifiant des champs particuliers.

::

    title:moteur de recherche
    url:https://fess.codelibs.org/

Principaux champs :

- ``title`` : Titre du document
- ``content`` : Corps du document
- ``url`` : URL du document
- ``filetype`` : Type de fichier (par exemple : pdf, html, doc)
- ``label`` : Étiquette (classification)
- ``mimetype`` : Type MIME (par exemple : text/html, application/pdf)
- ``filename`` : Nom du fichier
- ``host`` : Nom d'hôte
- ``site`` : Site (combinaison du nom d'hôte et du chemin)
- ``lang`` : Langue

Les champs de recherche supplémentaires peuvent être ajoutés via ``query.additional.search.fields`` dans ``fess_config.properties``.

Recherche avec caractères génériques
-------------------------------------

Les recherches utilisant des caractères génériques sont possibles.

- ``*`` : Zéro ou plusieurs caractères arbitraires
- ``?`` : Un caractère arbitraire

::

    recherche*
    recherche?oteur

Recherche floue
---------------

Une recherche floue qui gère les fautes de frappe et les variations d'orthographe est disponible.
Par défaut, pour les mots-clés de 4 caractères ou plus, une requête de recherche floue est exécutée en complément de la recherche normale.

::

    moteur de recherche~

En spécifiant une valeur numérique après ``~``, vous pouvez spécifier la distance d'édition.

Tri des résultats de recherche
===============================

Par défaut, les résultats de recherche sont triés par ordre de pertinence.
Vous pouvez spécifier différents ordres de tri via les paramètres de l'interface d'administration ou les paramètres de l'API.

- Ordre de pertinence (``score``, par défaut)
- Ordre chronologique des mises à jour (``last_modified``)
- Ordre chronologique de création (``created``)
- Ordre de taille de fichier (``content_length``)
- Ordre alphabétique par nom de fichier (``filename``)
- Ordre par nombre de clics (``click_count``)
- Ordre par nombre de favoris (``favorite_count``)

Les champs de tri supplémentaires peuvent être ajoutés via ``query.additional.sort.fields`` dans ``fess_config.properties``.

Recherche à facettes
====================

La recherche à facettes vous permet d'affiner les résultats de recherche par catégorie.
Par défaut, le champ étiquette (label) est défini comme facette.

Vous pouvez affiner les résultats de recherche en cliquant sur les facettes affichées sur le côté gauche de l'écran de recherche.

Mise en surbrillance des résultats de recherche
================================================

Les mots-clés de recherche sont mis en surbrillance dans le titre et le résumé des résultats de recherche.
Les paramètres de mise en surbrillance peuvent être personnalisés dans ``fess_config.properties``.

::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>
    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

- ``query.highlight.tag.pre`` / ``query.highlight.tag.post`` : Balises encadrant les zones mises en surbrillance (par défaut : ``<strong>`` / ``</strong>``)
- ``query.highlight.fragment.size`` : Nombre de caractères par fragment mis en surbrillance (par défaut : ``60``)
- ``query.highlight.number.of.fragments`` : Nombre maximum de fragments affichés (par défaut : ``2``)

Les champs utilisés comme source du résumé (snippet) mis en surbrillance sont définis par ``query.highlight.content.description.fields`` (par défaut : ``hl_content,digest``).

Fonction de suggestion
======================

Lorsque vous saisissez des caractères dans la zone de recherche, des suggestions (auto-complétion) s'affichent.
Les suggestions sont générées en fonction des mots-clés de recherche précédents et des mots-clés de recherche populaires.

La fonction de suggestion peut être activée/désactivée dans les paramètres « Général » de l'interface d'administration.

Journaux de recherche
=====================

|Fess| enregistre toutes les requêtes de recherche et les journaux de clics.
Ces journaux peuvent être utilisés aux fins suivantes :

- Analyse et amélioration de la qualité de recherche
- Analyse du comportement des utilisateurs
- Identification des mots-clés de recherche populaires
- Identification des mots-clés sans résultats de recherche

Les journaux de recherche et les journaux de clics sont stockés dans des index OpenSearch dont le nom commence par le préfixe ``fess_log``
(les requêtes de recherche dans l'index ``fess_log.search_log``, les journaux de clics dans l'index ``fess_log.click_log``).
Ces journaux peuvent être visualisés et analysés dans OpenSearch Dashboards.
|Fess| inclut un fichier de définition de tableau de bord pour la visualisation. Consultez :doc:`admin-opensearch-dashboards` pour plus de détails.

Optimisation des performances
==============================

Configuration du délai d'expiration de recherche
-------------------------------------------------

Vous pouvez configurer le délai d'expiration de recherche. La valeur par défaut est de 10 secondes.

::

    query.timeout=10000

Nombre maximum de caractères de requête de recherche
-----------------------------------------------------

Pour des raisons de sécurité et de performance, vous pouvez limiter le nombre maximum de caractères d'une requête de recherche.

::

    query.max.length=1000

Utilisation du cache
--------------------

|Fess| lui-même ne dispose d'aucune fonction de mise en cache des résultats de recherche (réponses de recherche).
Toutefois, OpenSearch en arrière-plan fournit un cache de requêtes de partition (shard request cache) et un cache de requêtes (query cache) au niveau du moteur, ce qui contribue à réduire le temps de réponse pour des recherches aux mêmes conditions.
Ces fonctionnalités étant propres à OpenSearch, ajustez-les si nécessaire via la configuration d'OpenSearch.

Dépannage
==========

Les résultats de recherche ne s'affichent pas
----------------------------------------------

1. Vérifiez que l'index a été créé correctement.
2. Vérifiez que l'exploration s'est terminée normalement.
3. Vérifiez que les documents cibles ne sont pas exclus pour l'utilisateur actuel (y compris les invités) par le filtrage basé sur les rôles et les permissions.
4. Vérifiez qu'OpenSearch fonctionne normalement.

La recherche est lente
-----------------------

1. Vérifiez la taille de la mémoire heap d'OpenSearch.
2. Optimisez le nombre de partitions et de répliques de l'index.
3. Vérifiez la complexité de la requête de recherche.
4. Vérifiez les ressources matérielles (CPU, mémoire, E/S disque).

Des résultats peu pertinents s'affichent
-----------------------------------------

1. Ajustez les paramètres de boost (``query.boost.title``, ``query.boost.content``, etc.).
2. Revoyez les paramètres de recherche floue.
3. Vérifiez la configuration de l'analyseur.
4. Si nécessaire, consultez le support commercial.
5. Vous pouvez également améliorer la précision de la recherche en utilisant Rank Fusion. Consultez :doc:`rank-fusion` pour plus de détails.
