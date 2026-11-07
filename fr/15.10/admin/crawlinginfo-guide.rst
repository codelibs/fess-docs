=====================
Informations de crawl
=====================

Présentation
============

Les résultats d'exécution du crawl sont enregistrés et les informations de crawl peuvent être vérifiées dans cet écran d'administration.

Gestion
=======

Liste
=====

Chaque fois qu'un crawl est exécuté, il est enregistré comme informations de crawl.
Dans la liste, vous pouvez vérifier le nom de session du crawl exécuté et l'heure d'exécution.
Si vous souhaitez vérifier les détails des informations de crawl, cliquez sur les informations de crawl cibles.

|image0|

Explorations en cours
=====================

Tant que des explorations sont en cours, « Explorations en cours » s'affiche au-dessus de la liste. Il comporte une ligne par configuration d'exploration (web, système de fichiers ou magasin de données), avec les éléments suivants.

- Configuration d'exploration : le nom de la configuration d'exploration.
- Documents traités : le nombre de documents que l'exploration en cours a traités jusqu'ici. Pour les explorations web et de système de fichiers, c'est le nombre de résultats d'accès ; pour les explorations de magasins de données, c'est le nombre de documents indexés pour la configuration d'exploration.
- Progression : les documents traités en pourcentage du nombre de documents de la dernière exploration terminée. Elle ne dépasse pas 99 % tant que l'exploration n'est pas terminée. S'il n'y a pas d'exploration terminée précédente (par exemple lors de la première exploration), aucun pourcentage ne peut être calculé : ``-`` s'affiche et seul le nombre est indiqué.

Remarques :

- Le bloc affiche l'état au moment de l'ouverture de la page. Rechargez la page pour voir les valeurs les plus récentes.
- Une exploration terminée n'est plus dans le bloc à la prochaine ouverture de la page. Une exploration arrêtée, ou que le crawler interrompt sans l'enregistrer (par exemple lorsque le processus est tué), disparaît dans un délai d'environ 30 secondes (par défaut) après sa dernière mise à jour ; elle peut donc rester affichée brièvement après l'arrêt. Une exploration arrêtée ou en échec laisse inchangé le nombre de documents de la dernière exploration terminée, de même qu'une exploration qui se termine sans avoir traité aucun document.
- L'état de progression est enregistré par le système dans le champ ``metadata`` de la configuration d'exploration. Il ne peut être modifié ni dans l'interface d'administration ni par l'API d'administration.
- Les mêmes informations sont disponibles via l'API d'administration (voir :doc:`../api/admin/api-admin-crawlinginfo`).

Détails
=======

En cliquant sur l'ID de session des informations de crawl dans la liste, les détails des informations de crawl cibles s'affichent.

|image1|

Liste des éléments
------------------

ID de session
:::::::::::::

ID de session lors de l'exécution du crawl.

Heure de début du crawler
::::::::::::::::::::::::::

Heure de début de l'ensemble du crawl.

Heure de début du crawl (Web/Fichier)
::::::::::::::::::::::::::::::::::::::

Heure de début du crawl Web et du système de fichiers.

Heure de début du crawl (Magasin de données)
:::::::::::::::::::::::::::::::::::::::::::::

Heure de début du crawl du magasin de données.

Heure de fin du crawl (Web/Fichier)
::::::::::::::::::::::::::::::::::::

Heure de fin du crawl Web et du système de fichiers.

Durée d'exécution du crawl (Magasin de données)
::::::::::::::::::::::::::::::::::::::::::::::::

Durée d'exécution du crawl du magasin de données (en millisecondes).

Durée d'exécution de l'indexation (Magasin de données)
:::::::::::::::::::::::::::::::::::::::::::::::::::::::

Temps nécessaire pour indexer les résultats du crawl Web et du système de fichiers (en millisecondes).

Taille de l'index (Magasin de données)
:::::::::::::::::::::::::::::::::::::::

Nombre de documents indexés.

Heure de fin du crawl (Magasin de données)
:::::::::::::::::::::::::::::::::::::::::::

Heure de fin du crawl du magasin de données.

État du crawler
:::::::::::::::

Si le crawl a réussi ou non.

Heure de fin du crawler
::::::::::::::::::::::::

Heure de fin de l'ensemble du crawl.

Durée d'exécution du crawler
:::::::::::::::::::::::::::::

Durée d'exécution de l'ensemble du crawl (en millisecondes).

.. |image0| image:: ../../../resources/images/en/15.10/admin/crawlinginfo-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/crawlinginfo-2.png
