======
Thème
======

Présentation
============

La fonctionnalité de thèmes permet de gérer les « thèmes statiques », c'est-à-dire des ensembles d'éléments statiques (HTML / CSS / JavaScript, etc.) qui définissent l'apparence de l'écran de recherche. Un thème statique est téléversé sous forme d'archive ZIP, puis décompressé dans le répertoire de thèmes sur le serveur (par défaut : ``themes``, modifiable via ``theme.directory.path``). À la racine de chaque thème doit se trouver un manifeste ``theme.yml`` décrivant les métadonnées du thème.

.. note::
   Les thèmes basés sur JSP sont gérés via la page de configuration des plugins et ne font pas l'objet de cette page.
   Pour effectuer les opérations décrites sur cette page, le rôle ``admin-theme`` est requis (le rôle ``admin-theme-view`` suffit pour la consultation seule).

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste des thèmes enregistrés, cliquez sur [Système > Thème] dans le menu de gauche.

Liste des thèmes
----------------

La page de liste affiche les thèmes statiques enregistrés dans le répertoire de thèmes. Les colonnes affichées pour chaque ligne sont les suivantes :

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Vignette
     - Affiche le fichier ``thumbnail.png`` situé dans le répertoire du thème. Si ce fichier est absent, rien n'est affiché.
   * - Nom
     - Nom du thème (nom du répertoire du thème). Cliquez dessus pour afficher la page de détails.
   * - Nom d'affichage
     - Valeur du champ ``displayName`` dans le manifeste.
   * - Version
     - Valeur du champ ``version`` dans le manifeste.
   * - Par défaut
     - Une coche est affichée si le thème est défini comme thème par défaut.
   * - Actions
     - Un bouton Supprimer permettant de supprimer le thème (non affiché pour le thème par défaut).

Tableau : Colonnes de la liste des thèmes


Définition du thème par défaut
-------------------------------

Sélectionnez un thème dans le menu déroulant situé en haut de la page de liste, puis cliquez sur le bouton [Définir par défaut] pour définir le thème par défaut appliqué à l'écran de recherche. En sélectionnant [(aucun par défaut)] et en confirmant, vous annulez la désignation du thème par défaut. Après la mise à jour, les informations de thème sont rechargées et les modifications prennent effet immédiatement.


Téléversement d'un thème
-------------------------

Cliquez sur le bouton [Téléverser] pour ouvrir la page de téléversement. Sélectionnez le fichier ZIP du thème, puis cliquez sur le bouton [Téléverser] pour installer le thème.

* Seules les archives au format ``.zip`` peuvent être téléversées.
* La taille maximale du fichier compressé est de 50 Mo par défaut (``theme.upload.max.size``).
* L'archive ZIP doit contenir un manifeste ``theme.yml`` à sa racine.

Si un thème portant le même nom existe déjà, il est remplacé. L'ancien thème remplacé est conservé en sauvegarde pendant une période définie (7 jours par défaut, ``theme.upload.attic.retention.days``).

Si l'archive téléversée échoue à la validation du manifeste, ou si la taille totale après décompression, le nombre d'entrées ou le taux de compression dépassent les limites du serveur (protection contre les bombes ZIP), l'installation est refusée et un message d'erreur est affiché.


Manifeste theme.yml
--------------------

À la racine d'un thème statique doit se trouver un fichier ``theme.yml`` (au format YAML) décrivant les métadonnées du thème. Les champs disponibles sont les suivants :

.. tabularcolumns:: |p{3cm}|p{2cm}|p{7cm}|
.. list-table::
   :header-rows: 1

   * - Champ
     - Requis
     - Description
   * - ``apiVersion``
     - Requis
     - Indiquez ``fess.codelibs.org/v1``.
   * - ``kind``
     - Requis
     - Indiquez ``StaticTheme``.
   * - ``name``
     - Requis
     - Nom du thème. Doit respecter le motif ``^[a-z0-9][a-z0-9_-]{0,63}$`` et correspondre au nom du répertoire du thème.
   * - ``displayName``
     - Requis
     - Nom affiché à l'écran (4 096 caractères maximum).
   * - ``version``
     - Requis
     - Version au format SemVer (ex. : ``1.0.0``).
   * - ``author``
     - Optionnel
     - Auteur du thème.
   * - ``description``
     - Optionnel
     - Description du thème.
   * - ``license``
     - Optionnel
     - Licence du thème.
   * - ``homepage``
     - Optionnel
     - URL de la page d'accueil du thème.
   * - ``minFessVersion``
     - Optionnel
     - Version minimale de |Fess| prise en charge.
   * - ``supportedLocales``
     - Optionnel
     - Paramètres régionaux pris en charge.
   * - ``entry``
     - Optionnel
     - Fichier servant de point d'entrée (par défaut : ``index.html``).
   * - ``spaFallback``
     - Optionnel
     - Active ou désactive le fallback en mode SPA (par défaut : ``true``).

Tableau : Champs du fichier theme.yml


Suppression d'un thème
-----------------------

Vous pouvez supprimer un thème via le bouton Supprimer de la page de liste ou via le bouton [Supprimer] de la page de détails. Un thème défini comme thème par défaut ne peut pas être supprimé. Annulez d'abord la désignation du thème par défaut avant de le supprimer. Le thème supprimé est conservé en sauvegarde pendant une période définie (7 jours par défaut, ``theme.upload.attic.retention.days``).


Rechargement
-------------

Si vous avez modifié directement le répertoire de thèmes sur le serveur, cliquez sur le bouton [Recharger] pour recharger en mémoire les informations de thèmes présentes sur le disque.


Détails du thème
-----------------

Cliquez sur le nom d'un thème dans la page de liste pour afficher la page de détails. La page de détails permet de consulter le contenu du manifeste (nom, nom d'affichage, version, statut par défaut, état).


Propriétés de configuration
============================

Les principaux paramètres liés à la fonctionnalité de thèmes peuvent être modifiés dans ``fess_config.properties``.

.. tabularcolumns:: |p{6cm}|p{3cm}|p{5cm}|
.. list-table::
   :header-rows: 1

   * - Propriété
     - Valeur par défaut
     - Description
   * - ``theme.directory.path``
     - ``themes``
     - Répertoire de stockage des thèmes (chemin relatif au contexte de la servlet, ou chemin absolu).
   * - ``theme.upload.max.size``
     - ``52428800``
     - Taille maximale du fichier ZIP pouvant être téléversé (en octets, environ 50 Mo).
   * - ``theme.upload.max.extracted.size``
     - ``209715200``
     - Taille totale maximale après décompression (en octets, environ 200 Mo).
   * - ``theme.upload.max.entries``
     - ``1000``
     - Nombre maximal d'entrées autorisées dans le fichier ZIP.
   * - ``theme.upload.max.compression.ratio``
     - ``100``
     - Taux de compression maximal par entrée.
   * - ``theme.upload.zip.ratio.max``
     - ``50``
     - Limite du taux de compression cumulé (protection contre les bombes ZIP).
   * - ``theme.upload.zip.ratio.check.threshold.bytes``
     - ``65536``
     - Nombre d'octets compressés à partir duquel l'évaluation du taux de compression cumulé est déclenchée.
   * - ``theme.upload.attic.retention.days``
     - ``7``
     - Nombre de jours de conservation de la sauvegarde des thèmes remplacés ou supprimés.

Tableau : Propriétés de configuration de la fonctionnalité de thèmes
