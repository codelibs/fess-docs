==========
Sauvegarde
==========

Présentation
============

La page de sauvegarde permet de télécharger et de téléverser les informations de configuration de |Fess|.

Téléchargement
--------------

|Fess| conserve les informations de configuration sous forme d'index.
Pour télécharger, cliquez sur le nom de l'index.

|image0|

fess_config.bulk
::::::::::::::::

fess_config.bulk contient les informations de configuration de |Fess|.

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk contient les informations de configuration de |Fess| à l'exception des URL en échec.

fess_user.bulk
::::::::::::::

fess_user.bulk contient les informations des utilisateurs, rôles et groupes.

system.properties
:::::::::::::::::

system.properties contient les informations de configuration générale.

fess.json
:::::::::

fess.json contient les informations de configuration de l'index fess.

doc.json
::::::::

doc.json contient les informations de mapping de l'index fess.

chat_log.ndjson
:::::::::::::::

chat_log.ndjson contient les informations du journal d'utilisation du chat IA.

click_log.ndjson
::::::::::::::::

click_log.ndjson contient les informations du journal des clics.

favorite_log.ndjson
:::::::::::::::::::

favorite_log.ndjson contient les informations du journal des favoris.

search_log.ndjson
:::::::::::::::::

search_log.ndjson contient les informations du journal de recherche.

user_info.ndjson
::::::::::::::::

user_info.ndjson contient les informations des utilisateurs de recherche.

Téléversement
-------------

Vous pouvez téléverser et importer les informations de configuration.
Les fichiers qui peuvent être restaurés sont \*.bulk et system.properties.

Un document d'un fichier \*.bulk qui possède un ``updatedTime`` n'est écrit que si le document
stocké n'existe pas, n'a pas de ``updatedTime`` ou est plus ancien. Un document qui n'est pas plus
récent est ignoré et consigné au niveau INFO dans ``fess.log`` : une restauration n'annule donc pas
les modifications faites après la sauvegarde, et les jobs planifiés fournis avec la version
installée (``updatedTime`` 0) sont conservés tels quels. Les documents sans ``updatedTime`` sont
toujours écrits.

  .. |image0| image:: ../../../resources/images/en/15.9/admin/backup-1.png
