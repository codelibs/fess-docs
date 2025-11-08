====================================================================
Créer un serveur de recherche basé sur Elasticsearch avec Fess 〜 Édition recherche basée sur les rôles
====================================================================

Introduction
========

Cet article présente la fonctionnalité de recherche basée sur les rôles, l'une des fonctionnalités caractéristiques de Fess.

Cet article utilise Fess 15.3.0 pour les explications.
Pour la méthode de construction de Fess, veuillez consulter l'\ `édition introduction <https://fess.codelibs.org/ja/articles/article-1.html>`__\.

Public visé
========

-  Personnes souhaitant construire un système de recherche avec authentification tel qu'un site portail

-  Personnes souhaitant construire un environnement de recherche en fonction des droits de consultation

Environnement requis
==========

Le contenu de cet article a été vérifié dans l'environnement suivant.

-  Ubuntu 22.04

-  OpenJDK 21

Recherche basée sur les rôles
================

La recherche basée sur les rôles de Fess est une fonctionnalité qui affiche différents résultats de recherche en fonction des informations d'authentification des utilisateurs authentifiés.
Par exemple, l'employé commercial A ayant le rôle du département des ventes verra les informations du rôle du département des ventes dans les résultats de recherche, mais l'employé technique B n'ayant pas le rôle du département des ventes ne les verra pas même en effectuant une recherche.
En utilisant cette fonctionnalité, il est possible de réaliser une recherche par département ou par poste pour les utilisateurs connectés dans un portail ou un environnement d'authentification unique.

La recherche basée sur les rôles de Fess peut par défaut différencier les résultats de recherche en fonction des informations utilisateur gérées par Fess.
Il est également possible de l'utiliser en intégrant avec les informations d'authentification de LDAP ou Active Directory.
En plus de ces systèmes d'authentification, les informations de rôle peuvent être obtenues des emplacements suivants.

1. Paramètres de requête

2. En-têtes de requête

3. Cookies

4. Informations d'authentification J2EE

Comme méthode d'utilisation, dans les serveurs portail ou les systèmes d'authentification unique de type agent, en stockant les informations d'authentification dans un cookie pour le domaine et le chemin où Fess fonctionne lors de l'authentification, les informations de rôle peuvent être transmises à Fess.
De plus, dans les systèmes d'authentification unique de type proxy inverse, en ajoutant les informations d'authentification aux paramètres de requête ou aux en-têtes de requête lors de l'accès à Fess, Fess peut obtenir les informations de rôle.
Ainsi, en intégrant avec divers systèmes d'authentification, il est possible de différencier les résultats de recherche pour chaque utilisateur.

Configuration pour utiliser la recherche basée sur les rôles
====================================

Nous supposons que Fess 15.3.0 est installé.
Si ce n'est pas encore fait, veuillez installer en vous référant à l'\ `édition introduction <https://fess.codelibs.org/ja/articles/article-1.html>`__\.

Cette fois, nous allons expliquer la recherche par rôle en utilisant la fonctionnalité de gestion des utilisateurs de Fess.

Aperçu de la configuration
----------

Cette fois, nous allons créer deux rôles : département des ventes (sales) et département technique (eng). L'utilisateur taro appartient au rôle sales et peut obtenir les résultats de recherche de \https://www.n2sm.net/, tandis que l'utilisateur hanako appartient au rôle eng et peut obtenir les résultats de recherche de \https://fess.codelibs.org/.

Création de rôles
------------

Tout d'abord, accédez à l'interface d'administration.
\http://localhost:8080/admin/

Depuis Utilisateurs > Rôles > Nouveau, entrez « sales » dans le nom et créez le rôle sales.
Créez également le rôle eng de la même manière.

Liste des rôles
|image0|


Création de rôles pour le crawler
----------------------

Cliquez sur Utilisateurs > Rôles > sales > Créer un nouveau rôle pour le crawler.
Entrez « Département des ventes » dans le nom, laissez la valeur à « sales » et cliquez sur [Créer].
Le paramètre Département des ventes sera alors ajouté à la liste Crawler > Rôles.

De la même manière, enregistrez le nom du rôle pour le crawler du rôle eng comme « Département technique ».

Liste des rôles pour le crawler
|image1|


Création d'utilisateurs
--------------

Depuis Utilisateurs > Utilisateurs > Nouveau, créez les utilisateurs taro et hanako avec les paramètres du tableau ci-dessous.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - Taro
     - Hanako
   * - Nom d'utilisateur
     - taro
     - hanako
   * - Mot de passe
     - taro
     - hanako
   * - Rôle
     - sales
     - eng


Vérification des utilisateurs enregistrés
------------------

Avec cette configuration, trois utilisateurs peuvent se connecter à Fess : admin, taro et hanako.
Veuillez vérifier que vous pouvez vous connecter avec chacun d'eux.
Accédez à \http://localhost:8080/admin/ et connectez-vous avec l'utilisateur admin pour afficher l'interface d'administration normalement.
Ensuite, déconnectez l'utilisateur admin. Cliquez sur le bouton en haut à droite de l'interface d'administration.

Bouton de déconnexion
|image2|

Connectez-vous avec taro ou hanako en entrant le nom d'utilisateur et le mot de passe.
Si la connexion réussit, l'écran de recherche \http://localhost:8080/ s'affiche.

Ajout de la configuration d'exploration
------------------

Enregistrez les cibles d'exploration.
Cette fois, les utilisateurs du rôle département des ventes ne peuvent rechercher que \https://www.n2sm.net/, et les utilisateurs du rôle département technique ne peuvent rechercher que \https://fess.codelibs.org/.
Pour enregistrer ces configurations d'exploration, cliquez sur Crawler > Web > Nouveau pour créer une configuration d'exploration web.
Cette fois, nous utilisons les paramètres suivants. Les autres sont par défaut.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - N2SM
     - Fess
   * - Nom
     - N2SM
     - Fess
   * - URL
     - \https://www.n2sm.net/
     - \https://fess.codelibs.org/
   * - URL à explorer
     - \https://www.n2sm.net/.*
     - \https://fess.codelibs.org/.*
   * - Nombre maximum d'accès
     - 10
     - 10
   * - Intervalle
     - 3000 millisecondes
     - 3000 millisecondes
   * - Rôle
     - Département des ventes
     - Département technique

Démarrage de l'exploration
--------------

Après l'enregistrement de la configuration d'exploration, cliquez sur [Démarrer maintenant] depuis Système > Planificateur > Default Crawler. Attendez que l'exploration se termine.

Recherche
----

Après la fin de l'exploration, accédez à \http://localhost:8080/, recherchez un mot comme « fess » sans être connecté, et vérifiez qu'aucun résultat de recherche n'est affiché.
Ensuite, connectez-vous avec l'utilisateur taro et effectuez la même recherche.
Comme l'utilisateur taro a le rôle sales, seuls les résultats de recherche de \https://www.n2sm.net/ sont affichés.

Écran de recherche avec le rôle sales
|image3|

Déconnectez l'utilisateur taro et connectez-vous avec l'utilisateur hanako.
En effectuant la même recherche qu'avant, comme l'utilisateur hanako a le rôle eng, seuls les résultats de recherche de \https://fess.codelibs.org/ sont affichés.

Écran de recherche avec le rôle eng
|image4|

Conclusion
======

Nous avons présenté la recherche basée sur les rôles, l'une des fonctionnalités de sécurité de Fess.
Bien que nous ayons principalement expliqué la recherche basée sur les rôles en utilisant les informations d'authentification J2EE, comme la transmission des informations d'authentification à Fess est une implémentation générique, elle devrait pouvoir s'adapter à divers systèmes d'authentification.
Comme il est possible de différencier les résultats de recherche en fonction des attributs des utilisateurs, il est également possible de réaliser des systèmes nécessitant une recherche en fonction des droits de consultation, tels que les sites portail d'entreprise ou les dossiers partagés.

Références
========

-  `Fess <https://fess.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/3/role-1.png
.. |image1| image:: ../../resources/images/ja/article/3/role-2.png
.. |image2| image:: ../../resources/images/ja/article/3/logout.png
.. |image3| image:: ../../resources/images/ja/article/3/search-by-sales.png
.. |image4| image:: ../../resources/images/ja/article/3/search-by-eng.png
