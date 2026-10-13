===========================
Authentification de fichier
===========================

Présentation
============

Cette section explique la méthode de configuration lorsqu'une authentification de fichier est requise pour le crawl ciblant les fichiers.
|Fess| prend en charge l'authentification FTP ou pour les dossiers partagés Windows.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste pour configurer l'authentification de fichier illustrée ci-dessous, cliquez sur [Robot d'exploration > Authentification de fichier] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration d'authentification de fichier.

|image1|

Paramètres de configuration
---------------------------

Nom d'hôte
::::::::::

Spécifie le nom d'hôte du site nécessitant une authentification.
Utilisez le même nom que le nom d'hôte de l'URL à crawler. Cette authentification n'est pas utilisée pour une URL écrite avec un autre nom (par exemple, une adresse IP au lieu d'un alias).

Port
::::

Spécifie le port du site nécessitant une authentification.
Si le champ est laissé vide, la liste affiche « N'importe lequel ». La signification d'un port vide dépend du schéma.

* FTP : utilisée pour les URL de n'importe quel port (une URL sans port est traitée comme le port 21).
* SAMBA : utilisée uniquement pour les URL qui ne contiennent pas de port (``smb://serveur/partage/``). Elle n'est pas utilisée pour une URL qui contient un port, comme ``smb://serveur:445/partage/``. Pour crawler une URL contenant un port, indiquez ici le même port.

Schéma
::::::

Sélectionnez la méthode d'authentification.
Vous pouvez utiliser FTP ou SAMBA (authentification de dossier partagé Windows).

Nom d'utilisateur
:::::::::::::::::

Spécifie le nom d'utilisateur pour se connecter au site d'authentification.

Mot de passe
::::::::::::

Spécifie le mot de passe pour se connecter au site d'authentification.

Paramètres
::::::::::

Configure s'il existe des valeurs de configuration nécessaires pour se connecter au site d'authentification. Pour SAMBA, vous pouvez définir la valeur de domain. Pour la configurer, décrivez comme suit :

::

    domain=FUGA

Configuration de crawl de fichiers
:::::::::::::::::::::::::::::::::::

Spécifie la configuration de crawl qui utilisera ces paramètres d'authentification.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

.. |image0| image:: ../../../resources/images/en/15.9/admin/fileauth-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/fileauth-2.png
