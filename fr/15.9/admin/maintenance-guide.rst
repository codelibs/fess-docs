===========
Maintenance
===========

Présentation
============

La page de maintenance est utilisée pour exécuter des opérations de données système.

|image0|

Méthode d'opération
===================

Réindexation
------------

Vous pouvez recréer un nouvel index à partir de l'index fess existant.
Exécutez cela lorsque vous souhaitez modifier le mapping de l'index, par exemple.


Paramètres de configuration
---------------------------

Mise à jour de l'alias
::::::::::::::::::::::

En l'activant, après la fin de la réindexation, vous pouvez réattribuer les alias fess.search et fess.update assignés à l'index existant au nouvel index.


Initialisation du dictionnaire
:::::::::::::::::::::::::::::::

En l'activant, vous pouvez initialiser la configuration du dictionnaire.

Si ``search_engine.type`` vaut ``vanilla`` ou ``aws``, cet élément n'est pas affiché.


Nombre de shards
::::::::::::::::

Vous pouvez spécifier le nombre de shards OpenSearch (index.number_of_shards).


Nombre maximum de réplicas
:::::::::::::::::::::::::::

Vous pouvez spécifier le nombre maximum de réplicas OpenSearch (index.auto_expand_replicas).


Reconstruire l'index de configuration
--------------------------------------

Vous pouvez reconstruire les index de configuration (fess_config, fess_user, fess_log) avec les mappings les plus récents.
Cette opération s'exécute en arrière-plan. Veuillez sauvegarder votre configuration avant l'exécution.

Index cibles
::::::::::::

Sélectionnez les index à reconstruire. Vous pouvez choisir parmi fess_config, fess_user et fess_log.

Charger les données par défaut
::::::::::::::::::::::::::::::

En l'activant, les données par défaut seront chargées lors de la reconstruction. Les documents existants ne seront pas écrasés.

Rechargement de l'index de documents
------------------------------------

Vous pouvez recharger l'index de documents pour appliquer la configuration de l'index.
C'est aussi ainsi que les modifications de dictionnaire sont appliquées aux recherches : les
dictionnaires enregistrés sont écrits dans leurs fichiers dans OpenSearch, puis l'index vers lequel
pointe l'alias ``fess.update`` est fermé et rouvert. Tant que l'index est fermé, il ne peut pas être
interrogé. Voir :ref:`dict-apply-changes`.

Si ``search_engine.type`` vaut ``vanilla`` ou ``aws``, cette fonction n'est pas affichée.


Index Crawler
-------------

Vous pouvez supprimer l'index fess_crawler (informations de crawl).
Ne l'exécutez pas pendant l'exécution du crawler.


Diagnostic
----------

Vous pouvez télécharger un fichier zip de diagnostic. Le zip contient les fichiers suivants dans le répertoire ``log<yyyyMMddHHmm>/``.

- Les fichiers ``*.log`` et ``*.log.gz`` du répertoire des journaux (``fess.log``, ``fess-crawler.log``, ``audit.log``, ``searchlog.log``, etc.)
- ``system.properties`` (paramètres système) et ``fess_config.properties`` (paramètres de l'application)
- ``fess_basic_config.bulk`` (contenu des index de configuration, tels que les paramètres de crawl, d'authentification et les étiquettes ; les jetons d'accès de l'API d'administration n'y figurent pas)
- ``es_cat_*.txt`` et ``es_*.json`` (sortie des API ``_cat`` d'OpenSearch et état du cluster, des nœuds et des tâches)

Dans ``system.properties`` et ``fess_config.properties``, les valeurs secrètes sont remplacées par ``XXXXXXXX`` selon la même règle que l'écran Informations système. Cela concerne par exemple la clé secrète de stockage, les URL de webhook (Slack et Google Chat), les secrets client SSO, les clés d'API des LLM et d'embedding, ainsi que la clé de chiffrement de l'application (``app.cipher.key``). Les clés sont conservées : on voit donc toujours quels paramètres existent.

.. note::

   Les fichiers journaux et le contenu de ``fess_basic_config.bulk`` ne sont pas masqués. Vérifiez le contenu avant d'envoyer le zip en dehors de votre organisation.

.. |image0| image:: ../../../resources/images/en/15.9/admin/maintenance-1.png
