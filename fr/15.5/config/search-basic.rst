========
Fonction de recherche
========

Aperçu
====

|Fess| offre une puissante fonction de recherche en texte intégral.
Cette section décrit les paramètres détaillés et les méthodes d'utilisation de la fonction de recherche.

Affichage du nombre de résultats de recherche
==================

Comportement par défaut
----------------

Lorsque les résultats de recherche dépassent 10 000 éléments, le nombre affiché sur l'écran des résultats est "environ 10 000 ou plus".
Il s'agit du paramètre par défaut qui prend en compte les performances d'OpenSearch.

Exemple de recherche

|image0|

.. |image0| image:: ../../../resources/images/en/15.5/config/search-result.png

Affichage du nombre exact de correspondances
----------------------

Pour afficher le nombre exact de correspondances au-delà de 10 000 éléments, modifiez le paramètre suivant dans ``fess_config.properties``.

::

    query.track.total.hits=100000

Ce paramètre permet d'obtenir le nombre exact de correspondances jusqu'à 100 000 éléments.
Cependant, une valeur élevée peut affecter les performances.

.. warning::
   Une valeur trop élevée peut dégrader les performances de recherche.
   Veuillez définir une valeur appropriée en fonction de votre situation d'utilisation réelle.

Options de recherche
==============

Recherche de base
------------

Dans |Fess|, une recherche en texte intégral est exécutée simplement en saisissant des mots-clés dans la zone de recherche.
La saisie de plusieurs mots-clés effectue une recherche ET (AND).

::

    recherche moteur

Dans l'exemple ci-dessus, les documents contenant à la fois "recherche" et "moteur" sont recherchés.

Recherche OU (OR)
------

Pour effectuer une recherche OU, insérez ``OR`` entre les mots-clés.

::

    recherche OR moteur

Recherche NON (NOT)
-------

Pour exclure un mot-clé spécifique, ajoutez ``-`` (signe moins) devant le mot-clé.

::

    recherche -moteur

Recherche de phrase
------------

Pour rechercher une phrase exacte, entourez-la de guillemets doubles.

::

    "moteur de recherche"

Recherche par champ spécifique
------------------

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

Recherche avec caractères génériques
------------------

Les recherches utilisant des caractères génériques sont possibles.

- ``*`` : Zéro ou plusieurs caractères arbitraires
- ``?`` : Un caractère arbitraire

::

    recherche*
    recherche?oteur

Recherche floue
------------

Une recherche floue qui gère les fautes de frappe et les variations d'orthographe est disponible.
Par défaut, une recherche floue est automatiquement appliquée aux mots-clés de 4 caractères ou plus.

::

    moteur de recherche~

En spécifiant une valeur numérique après ``~``, vous pouvez spécifier la distance d'édition.

Tri des résultats de recherche
================

Par défaut, les résultats de recherche sont triés par ordre de pertinence.
Vous pouvez spécifier différents ordres de tri via les paramètres de l'interface d'administration ou les paramètres de l'API.

- Ordre de pertinence (par défaut)
- Ordre chronologique des mises à jour
- Ordre chronologique de création
- Ordre de taille de fichier

Recherche à facettes
==============

La recherche à facettes vous permet d'affiner les résultats de recherche par catégorie.
Par défaut, le champ étiquette (label) est défini comme facette.

Vous pouvez affiner les résultats de recherche en cliquant sur les facettes affichées sur le côté gauche de l'écran de recherche.

Mise en surbrillance des résultats de recherche
====================

Les mots-clés de recherche sont mis en surbrillance dans le titre et le résumé des résultats de recherche.
Les paramètres de mise en surbrillance peuvent être personnalisés dans ``fess_config.properties``.

::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>
    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Fonction de suggestion
==============

Lorsque vous saisissez des caractères dans la zone de recherche, des suggestions (auto-complétion) s'affichent.
Les suggestions sont générées en fonction des mots-clés de recherche précédents et des mots-clés de recherche populaires.

La fonction de suggestion peut être activée/désactivée dans les paramètres "Général" de l'interface d'administration.

Journaux de recherche
========

|Fess| enregistre toutes les requêtes de recherche et les journaux de clics.
Ces journaux peuvent être utilisés aux fins suivantes :

- Analyse et amélioration de la qualité de recherche
- Analyse du comportement des utilisateurs
- Identification des mots-clés de recherche populaires
- Identification des mots-clés sans résultats de recherche

Les journaux de recherche sont stockés dans l'index ``fess_log`` d'OpenSearch,
et peuvent être visualisés et analysés dans OpenSearch Dashboards.
Pour plus de détails, consultez :doc:`kibana`.

Optimisation des performances
==========================

Configuration du délai d'expiration de recherche
----------------------

Vous pouvez configurer le délai d'expiration de recherche. La valeur par défaut est de 10 secondes.

::

    query.timeout=10000

Nombre maximum de caractères de requête de recherche
----------------------

Pour des raisons de sécurité et de performance, vous pouvez limiter le nombre maximum de caractères d'une requête de recherche.

::

    query.max.length=1000

Utilisation du cache
----------------

En activant le cache des résultats de recherche, vous pouvez réduire le temps de réponse pour les mêmes requêtes de recherche.
Les paramètres de cache doivent être ajustés en fonction des exigences du système.

Dépannage
======================

Les résultats de recherche ne s'affichent pas
----------------------

1. Vérifiez que l'index a été créé correctement.
2. Vérifiez que l'exploration s'est terminée normalement.
3. Vérifiez qu'aucune permission d'accès n'est définie sur les documents de recherche.
4. Vérifiez qu'OpenSearch fonctionne normalement.

La recherche est lente
--------------

1. Vérifiez la taille de la mémoire heap d'OpenSearch.
2. Optimisez le nombre de partitions et de répliques de l'index.
3. Vérifiez la complexité de la requête de recherche.
4. Vérifiez les ressources matérielles (CPU, mémoire, E/S disque).

Des résultats peu pertinents s'affichent
----------------------------

1. Ajustez les paramètres de boost (``query.boost.title``, ``query.boost.content``, etc.).
2. Revoyez les paramètres de recherche floue.
3. Vérifiez la configuration de l'analyseur.
4. Si nécessaire, consultez le support commercial.
5. Vous pouvez également améliorer la précision de la recherche en utilisant Rank Fusion. Consultez :doc:`rank-fusion` pour plus de détails.
