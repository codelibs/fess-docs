====================
Authentification Web
====================

Présentation
============

Cette section explique la méthode de configuration lorsqu'une authentification Web est requise pour le crawl ciblant le Web.
|Fess| prend en charge le crawl pour l'authentification BASIC, DIGEST, NTLM et FORM.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration d'authentification Web illustrée ci-dessous, cliquez sur [Robot d'exploration > Authentification Web] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration d'authentification Web.

|image1|

Paramètres de configuration
---------------------------

Nom d'hôte
::::::::::

Spécifie le nom d'hôte du site nécessitant une authentification.
Si omis, il sera appliqué à tout nom d'hôte dans la configuration de crawl Web spécifiée.

.. warning::

   Si le nom d'hôte est omis, le nom d'utilisateur et le mot de passe sont aussi envoyés aux autres hôtes que le crawl atteint par des liens ou des redirections.
   Spécifiez le nom d'hôte afin que les identifiants ne soient pas envoyés à des hôtes non souhaités.

Port
::::

Spécifie le port du site nécessitant une authentification.
Pour l'appliquer à tous les ports, laissez le champ vide. ``-1`` ne peut pas être spécifié ; seules les valeurs supérieures ou égales à 0 sont acceptées.
Dans ce cas, il sera appliqué à tout port dans la configuration de crawl Web spécifiée.

Domaine
:::::::

Spécifie le nom de domaine du site nécessitant une authentification.
Si omis, il sera appliqué à tout nom de domaine dans la configuration de crawl Web spécifiée.
Ce champ correspond au realm. Pour l'authentification BASIC et DIGEST, le realm est comparé à celui que renvoie le serveur, en distinguant majuscules et minuscules. S'ils ne correspondent pas, les identifiants ne sont pas envoyés.
Le défi NTLM ne contient pas de realm ; ce champ n'est donc pas utilisé pour l'authentification NTLM (l'authentification réussit même avec un realm incorrect).

Schéma
::::::

Sélectionnez la méthode d'authentification.
Vous pouvez utiliser l'authentification BASIC, DIGEST, NTLM ou FORM.

.. note::

   Le schéma BASIC, DIGEST ou NTLM ne limite pas la méthode d'authentification que le serveur peut demander.
   |Fess| envoie les identifiants avec la méthode que demande le serveur.
   Par exemple, une entrée enregistrée en DIGEST est envoyée en BASIC si le serveur ne demande que BASIC (en HTTP, les identifiants circulent alors pratiquement en clair).
   Une entrée enregistrée en BASIC répond en DIGEST si le serveur demande DIGEST.
   NTLM et BASIC/DIGEST ne peuvent pas se remplacer l'un l'autre.
   Si vous sélectionnez un schéma que le serveur n'utilise pas, aucun identifiant n'est envoyé et les documents du site ne sont pas indexés.
   Sélectionnez la méthode d'authentification utilisée par le serveur et, si possible, utilisez HTTPS.

Nom d'utilisateur
:::::::::::::::::

Spécifie le nom d'utilisateur pour se connecter au site d'authentification.
Si l'authentification NTLM nécessite un domaine, n'écrivez pas le nom d'utilisateur sous la forme ``DOMAINE\utilisateur`` ; indiquez le domaine avec le paramètre ``domain`` décrit ci-dessous.
Une valeur telle que ``DOMAINE\utilisateur`` n'est pas décomposée : la chaîne entière est envoyée comme nom d'utilisateur, avec un domaine vide.

Mot de passe
::::::::::::

Spécifie le mot de passe pour se connecter au site d'authentification.

Paramètres
::::::::::

Configure s'il existe des valeurs de configuration nécessaires pour se connecter au site d'authentification.
Pour l'authentification NTLM, vous pouvez définir les valeurs de workstation et domain.
Pour les configurer, décrivez comme suit :

::

    workstation=HOGE
    domain=FUGA

``domain``
    Le domaine dans lequel l'authentification est effectuée. Indiquez-le lorsque vous vous authentifiez avec un compte de domaine.
    S'il est omis, le domaine est envoyé vide et l'authentification d'un compte de domaine échoue.
    Un domaine écrit en minuscules est converti en majuscules avant l'envoi.

``workstation``
    Le nom de station de travail envoyé dans les messages NTLM.
    S'il est omis, le nom d'hôte de la machine sur laquelle |Fess| s'exécute est envoyé.

Configuration Web
:::::::::::::::::

Sélectionnez le nom de configuration Web auquel appliquer les paramètres d'authentification ci-dessus.
Vous devez enregistrer la configuration de crawl Web au préalable.

En cas d'échec de l'authentification
------------------------------------

Si les identifiants sont incorrects, ou si le nom d'hôte, le port ou le realm ne correspondent pas au site et qu'aucun identifiant n'est donc envoyé, le serveur renvoie 401 (Unauthorized) et les documents du site ne sont pas indexés.
Un 401 est enregistré comme URL en échec ; vérifiez-le dans :doc:`failureurl-guide`.
Les codes de statut HTTP enregistrés comme URL en échec peuvent être modifiés avec ``crawler.failure.url.status.codes`` (:doc:`../config/crawler-advanced`).
Notez qu'un 401 ne supprime pas les documents déjà présents dans l'index.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

.. |image0| image:: ../../../resources/images/en/15.10/admin/webauth-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/webauth-2.png
