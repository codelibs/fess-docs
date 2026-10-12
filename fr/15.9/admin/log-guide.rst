=================
Fichiers journaux
=================

Présentation
============

Cette section explique le téléchargement des fichiers journaux générés par |Fess|.

Méthode de configuration
========================

Affichage
---------

Pour ouvrir la page des fichiers journaux illustrée ci-dessous, cliquez sur [Informations système > Fichier journal] dans le menu de gauche.

|image0|

Téléchargement
--------------

Vous pouvez télécharger un fichier journal en cliquant sur le nom du fichier journal affiché.

``server_*.log``
::::::::::::::::

Les journaux de |Fess| en tant que serveur d'application sont enregistrés.

fess.log
::::::::

Les journaux de |Fess| en tant qu'application sont enregistrés.

fess-crawler.log
::::::::::::::::

Les journaux du crawler sont enregistrés.

audit.log
:::::::::

Les informations de connexion et les journaux d'accès à l'écran d'administration sont enregistrés.

fess-thumbnail.log
::::::::::::::::::

Les journaux de la fonctionnalité de vignettes sont enregistrés.

fess-suggest.log
::::::::::::::::

Les journaux de la fonctionnalité de suggestion sont enregistrés.

fess-urls.log
:::::::::::::

Le temps nécessaire pour un crawl est enregistré.

searchlog.log
:::::::::::::

Les journaux de recherche sont enregistrés.
Si « Journal de recherche » de [Système > Général] est activé, une ligne (JSON) est ajoutée à chaque recherche dans la configuration par défaut.
Une ligne contient les champs des documents retournés par cette recherche (``logging.search.docs.fields``) ; sa taille augmente donc avec le nombre de résultats retournés (avec ``num=100``, une ligne peut atteindre environ 70 Ko).
Pour la rotation et la conservation des journaux, voir :doc:`../config/admin-logging`.
Pour ne pas inclure les champs des documents retournés dans le journal de recherche, définissez ``logging.search.docs.enabled=false`` dans ``fess_config.properties`` ; pour ne plus écrire dans ce fichier, définissez ``logging.search.use.logfile=false``.

gc-crawler.log
::::::::::::::

Les journaux GC du processus de crawl sont enregistrés (écrits par le travail par défaut « Default Crawler »).

gc-fess.log
:::::::::::

Les journaux GC de |Fess| lui-même sont enregistrés. Ils ne sont écrits que si la variable d'environnement ``FESS_USE_GC_LOGGING`` a une valeur non vide (voir :doc:`../install/run`).

.. |image0| image:: ../../../resources/images/en/15.9/admin/log-1.png
