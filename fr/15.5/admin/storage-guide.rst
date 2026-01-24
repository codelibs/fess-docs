=========
Stockage
========

Présentation
============

La page Stockage permet de gérer les fichiers sur Amazon S3, Google Cloud Storage ou un stockage compatible S3 (comme MinIO).

Gestion
=======

Configuration du serveur de stockage d'objets
---------------------------------------------

Ouvrez la configuration du stockage depuis [Système > Général] et configurez les éléments suivants en fonction de votre type de stockage.

Paramètres communs
~~~~~~~~~~~~~~~~~~

- Type : Type de stockage (Automatique/S3/GCS)
- Bucket : Nom du bucket à gérer

Paramètres S3
~~~~~~~~~~~~~

- Point de terminaison : Point de terminaison S3 (utilise AWS par défaut si vide)
- Clé d'accès : Clé d'accès AWS
- Clé secrète : Clé secrète AWS
- Région : Région AWS

Paramètres GCS
~~~~~~~~~~~~~~

- Point de terminaison : Point de terminaison GCS (utilise Google Cloud par défaut si vide)
- ID de projet : ID de projet Google Cloud
- Chemin des identifiants : Chemin du fichier JSON d'identifiants du compte de service

Paramètres MinIO (compatible S3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Point de terminaison : URL du point de terminaison du serveur MinIO
- Clé d'accès : Clé d'accès MinIO
- Clé secrète : Clé secrète MinIO


Affichage
---------

Pour ouvrir la page de liste d'objets illustrée ci-dessous, cliquez sur [Système > Stockage] dans le menu de gauche.

|image0|


Nom
::::

Nom de fichier de l'objet


Taille
::::::

Taille de l'objet


Date de dernière modification
::::::::::::::::::::::::::::::

Date de dernière modification de l'objet

Téléchargement
--------------

Vous pouvez télécharger un objet en cliquant sur le bouton Télécharger.


Suppression
-----------

Vous pouvez supprimer un objet en cliquant sur le bouton Supprimer.


Téléversement
-------------

Vous pouvez ouvrir la fenêtre de téléversement de fichier en cliquant sur le bouton Téléverser le fichier en haut à droite.


Création de dossier
-------------------

Vous pouvez ouvrir la fenêtre de création de dossier en cliquant sur le bouton Créer le dossier à droite de l'affichage du chemin. Notez que vous ne pouvez pas créer de dossiers vides.


.. |image0| image:: ../../../resources/images/en/15.5/admin/storage-1.png
