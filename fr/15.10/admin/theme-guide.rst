======
Thème
======

Présentation
============

La fonctionnalité de thèmes permet de gérer les thèmes, c'est-à-dire des ensembles d'éléments statiques (HTML / CSS / JavaScript, etc.) qui définissent l'apparence de l'écran de recherche. Un thème est téléversé sous forme d'archive ZIP, puis décompressé dans le répertoire de thèmes sur le serveur (par défaut : ``themes``, modifiable via ``theme.directory.path``). À la racine de chaque thème doit se trouver un manifeste ``theme.yml`` décrivant les métadonnées du thème.

L'écran de recherche est toujours un thème. Lorsqu'aucun thème par défaut n'est défini, |Fess| utilise ``bootstrap``, le thème fourni avec lui. Le thème fourni ne peut être ni supprimé ni remplacé ; pour le modifier, copiez-le sous un nouveau nom (voir :ref:`theme-customize-bundled`).

.. note::
   Les thèmes basés sur JSP (plugins de thème JAR ``fess-theme-*``) ont été supprimés en 15.9. Pour modifier l'apparence, utilisez un thème (voir :ref:`upgrade-159-static-theme`).
   Pour effectuer les opérations décrites sur cette page, le rôle ``admin-theme`` est requis (le rôle ``admin-theme-view`` suffit pour la consultation seule).

Obtenir un thème
================

Les thèmes développés par le projet |Fess| sont publiés sous forme d'archives ZIP sous
https://maven.codelibs.org/release/org/codelibs/fess/themes/ , en
``<name>/<version>/<name>-<version>.zip``, avec une somme ``.sha1`` à côté de chacune.

La version d'un thème indique la ligne |Fess| qu'il vise : ``15.10.0`` est un thème pour
|Fess| 15.10, et ``minFessVersion`` dit la même chose. Il n'existe pas de champ de borne
supérieure. Une archive publiée ne change jamais : une borne supérieure ne pourrait donc pas être
ajoutée après coup pour un thème qui cesse de fonctionner sur un |Fess| plus récent. Ne pas le
publier pour cette ligne dit la même chose, au moment où on le sait.

Il y a trois façons d'en installer un.

* L'installer depuis le dépôt sur cette page, comme décrit dans `Installation depuis le dépôt`_
  ci-dessous.
* ``bin/fess-setup install theme <name>`` télécharge le thème construit pour ce |Fess|, le
  vérifie contre la somme publiée et l'installe. Voir :doc:`../install/fess-setup`.
* Télécharger le ZIP et le téléverser depuis cette page, comme décrit dans
  `Téléversement d'un thème`_.

Un thème peut aussi être empaqueté depuis une copie du dépôt
`fess-themes <https://github.com/codelibs/fess-themes>`__, qui correspond toujours aux sources que
vous avez sous les yeux ; voir :doc:`../dev/theme-development`.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste des thèmes enregistrés, cliquez sur [Système > Thème] dans le menu de gauche.

Liste des thèmes
----------------

La page de liste affiche les thèmes enregistrés dans le répertoire de thèmes. Les colonnes affichées pour chaque ligne sont les suivantes :

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

Sélectionnez un thème dans le menu déroulant situé en haut de la page de liste, puis cliquez sur le bouton [Définir par défaut] pour définir le thème par défaut appliqué à l'écran de recherche. En sélectionnant [(aucun par défaut)] et en confirmant, vous annulez la désignation du thème par défaut, et le thème fourni ``bootstrap`` est de nouveau utilisé. Après la mise à jour, les informations de thème sont rechargées et les modifications prennent effet immédiatement.


Installation depuis le dépôt
----------------------------

La page de liste installe aussi les thèmes publiés dans le dépôt de thèmes (``theme.repositories``, par défaut https://maven.codelibs.org/release/org/codelibs/fess/themes/ ).

* [Thèmes disponibles] liste les thèmes publiés par le dépôt, avec une version pour chacun. Cliquez sur [Installer] sur une ligne pour installer cette version.
* [Installer par nom] installe un thème à partir de son nom et de sa version, qu'il figure ou non dans cette liste. Saisissez le [Nom] et la [Version], puis cliquez sur [Installer].

Le ZIP est téléchargé depuis le dépôt, vérifié contre sa somme ``.sha1`` publiée, puis installé de la même manière qu'un téléversement ; les mêmes vérifications s'appliquent donc. Définissez ensuite le thème comme thème par défaut pour l'utiliser.


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

À la racine d'un thème doit se trouver un fichier ``theme.yml`` (au format YAML) décrivant les métadonnées du thème. Les champs disponibles sont les suivants :

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
     - Obsolète et n'est plus lu. Depuis la version 15.9, le fichier d'entrée est toujours servi pour les chemins de l'écran de recherche.

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


.. _theme-settings:

Paramètres du thème
-------------------

Certains thèmes permettent à un administrateur de modifier leur comportement en leur transmettant des paramètres. Saisissez-les dans « Paramètres du thème » de [Système > Général] dans l'interface d'administration, un ``key=value`` par ligne (voir :doc:`general-guide`). |Fess| ne les interprète pas : il les transmet au thème sous le nom ``theme_settings`` dans ``GET /api/v2/ui/config`` (voir :doc:`../api/api-uiconfig`). Chaque thème définit les clés qu'il accepte et la signification de leurs valeurs.

Les valeurs sont visibles de tous les utilisateurs de l'interface de recherche : ne saisissez pas de secrets tels que des mots de passe.

``filesearch.roots`` du thème File Search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le thème File Search (``filesearch``, version 15.10.6 ou ultérieure) permet de choisir, avec ``filesearch.roots``, les dossiers affichés au premier niveau de son arborescence. Sans ce paramètre, l'arborescence commence aux sources (hôtes). |Fess| 15.10 ou ultérieur est requis.

::

    filesearch.roots=smb://server/share/Documents/|file:/data/docs/

- La valeur est une liste de préfixes d'URL séparés par ``|``. Les espaces autour d'un élément sont ignorés ; un espace à l'intérieur d'un élément fait partie de l'URL.
- Écrivez chaque préfixe tel que le champ ``url`` d'un résultat de recherche le stocke : les URL ``smb:`` décodées (``smb://server/share/My Docs/``), les URL ``file:`` encodées en pourcentage (``file:/data/My%20Docs/``). Un ``/`` final est ajouté s'il manque.
- 20 racines au maximum sont utilisées, et les racines encodées en pourcentage doivent aussi tenir ensemble dans une limite de taille (moins si les chemins contiennent des caractères japonais). Les racines sont prises dans l'ordre d'écriture et les suivantes sont ignorées : placez les plus importantes en premier. Une racine peut compter jusqu'à 500 caractères. Un élément qui n'est pas une URL, qui contient un caractère de contrôle ou qui se trouve à l'intérieur d'un autre élément est également ignoré.
- Le premier niveau de l'arborescence se compose exactement des dossiers indiqués, par ordre alphabétique. Un dossier sans document pour le mot-clé et les filtres en cours n'est pas affiché : un préfixe mal saisi se remarque donc par l'absence du dossier.
- Les dossiers ne changent que le point de départ de l'arborescence. Ils ne constituent pas un contrôle d'accès : le périmètre de recherche et les documents visibles restent inchangés. Pour restreindre l'accès, utilisez les rôles (voir :doc:`../config/security-role`).

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
   * - ``theme.repositories``
     - ``https://maven.codelibs.org/release/org/codelibs/fess/themes/``
     - URL des dépôts (séparées par des virgules) depuis lesquels les thèmes sont installés.

Tableau : Propriétés de configuration de la fonctionnalité de thèmes
