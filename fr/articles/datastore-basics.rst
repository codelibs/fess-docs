==============================================
Bases de l'exploration des magasins de données
==============================================

Introduction
============

Le contenu de Google Drive, de Slack ou d'une base de données ne peut pas être rendu consultable par l'exploration Web ou l'exploration de fichiers.
Un fichier CSV exploré comme fichier devient lui aussi un seul document, et ses lignes ne peuvent pas être recherchées individuellement.
Fess traite ces sources comme des « magasins de données » et les importe enregistrement par enregistrement au moyen de plugins (connecteurs de magasin de données).

L'écran de configuration des magasins de données ne comporte pas les mêmes champs que les écrans de configuration Web et système de fichiers.
Vous devez indiquer vous-même quelles valeurs deviennent l'URL, le titre, etc., et avec les valeurs par défaut, les documents sont enregistrés de façon à pouvoir être recherchés sans connexion.
Même lorsque le traitement échoue, la tâche peut être affichée comme « OK ».

Cet article explique, sur la base de Fess 15.9, les mécanismes communs à tous les connecteurs.
À l'aide d'un petit exemple utilisant un fichier CSV, nous parcourons l'ensemble du processus : installation du plugin, configuration, exécution et vérification des résultats.
Pour l'authentification et les paramètres propres à chaque connecteur, consultez les articles et références listés à la fin.

Différences avec l'exploration Web et de fichiers
=================================================

Dans l'exploration Web et l'exploration de fichiers, Fess suit les liens et les dossiers, puis extrait automatiquement le titre et le corps des documents récupérés.
Dans l'exploration de magasins de données, un connecteur lit des enregistrements depuis une API ou un fichier.
La valeur de l'enregistrement qui va dans tel ou tel champ de l'index est définie dans le « Script » de la configuration.

Fess lui-même ne contient aucun gestionnaire de magasin de données.
La liste déroulante « Nom du gestionnaire » de [Robot d'exploration] > [Magasin de données] n'affiche que les gestionnaires fournis par les plugins ``fess-ds-*`` installés.

Les configurations de magasin de données diffèrent aussi sur les points suivants (expliqués dans les sections suivantes) :

- L'écran de configuration ne comporte pas de champ « Étiquette »
- Les règles de [Robot d'exploration] > [Boost de document] ne sont pas appliquées

Installer le plugin
===================

Nous prenons ici comme exemple le connecteur CSV ``fess-ds-csv``.
La version du plugin doit correspondre à la version mineure de Fess que vous utilisez (15.9.x pour Fess 15.9).

Pour l'installer depuis la console d'administration, cliquez sur [Installer] dans [Système] > [Plugin].
Dans l'onglet [Distant], sélectionnez ``fess-ds-csv`` dans la liste déroulante et cliquez sur [Installer].
Pour utiliser un fichier jar dont vous disposez localement, utilisez l'onglet [Local].

Dans les environnements installés à partir du paquet ZIP ou de RPM / DEB, vous pouvez aussi l'installer en ligne de commande.

.. code-block:: bash

    bin/fess-setup install plugin fess-ds-csv:15.9.0

Avec Docker, ajoutez ``FESS_PLUGINS`` à l'``environment`` de ``fess01`` dans ``compose.yaml`` pour que le plugin soit installé au démarrage.
Pour plusieurs plugins, séparez-les par des espaces (et non par des virgules).

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-csv:15.9.0"

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Avec Docker, un plugin installé depuis la console d'administration est placé dans le conteneur et disparaît donc lorsque le conteneur est recréé.
Avec Docker, ``FESS_PLUGINS`` est la méthode la plus fiable.
Modifier une variable d'environnement puis exécuter ``up -d`` recrée le conteneur.
Pour les paramètres perdus à ce moment-là, consultez :doc:`guide-02`.

Si vous avez installé le plugin depuis la console d'administration ou avec ``fess-setup``, redémarrez Fess (``FESS_PLUGINS`` installe les plugins avant le démarrage de Fess, aucun redémarrage n'est donc nécessaire).
Après le redémarrage, le plugin est installé si ``CsvDataStore`` apparaît dans « Nom du gestionnaire » sous [Robot d'exploration] > [Magasin de données] > [Créer nouveau].

Les trois champs principaux de l'écran de configuration
=======================================================

Une configuration de magasin de données s'articule autour de trois champs : « Nom du gestionnaire », « Paramètres » et « Script ».

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Champ
     - Contenu
   * - Nom du gestionnaire
     - Le connecteur à utiliser. Exemples : ``CsvDataStore``, ``SlackDataStore``
   * - Paramètres
     - Les instructions pour le connecteur. Un ``clé=valeur`` par ligne (fichiers à lire, cible de connexion, identifiants, etc.)
   * - Script
     - La correspondance avec les champs de l'index. Un ``nom_du_champ=expression`` par ligne

``script_type`` dans les paramètres
-----------------------------------

Sur l'écran de création, le champ « Paramètres » contient déjà ``script_type=javascript``.
Cela indique que les expressions du champ « Script » sont évaluées en JavaScript.
Conservez cette ligne et ajoutez les paramètres du connecteur en dessous.

Si vous supprimez la ligne ``script_type``, le script est évalué en Groovy (la valeur par défaut, qui permet aux configurations créées avant la 15.9 de continuer à fonctionner).
L'évaluation en Groovy nécessite le plugin ``fess-script-groovy``.
Il est inclus dans l'image Docker standard, mais pas dans l'image slim.
Dans un environnement sans ce plugin, l'évaluation d'une ligne contenant une expression échoue avec l'erreur ``groovy is not found`` et l'enregistrement n'est pas indexé (une ligne dont le membre de droite n'est qu'un nom d'élément, comme ``title=subject``, utilise la valeur telle quelle sans passer par un moteur de script).
À l'inverse, avec l'image Docker standard, la configuration continue de fonctionner avec Groovy même si vous supprimez la ligne, ce qui rend le problème difficile à remarquer.
Lorsque vous collez un exemple tiré de la référence d'un connecteur dans le champ « Paramètres », veillez à ne pas supprimer la ligne ``script_type=javascript``.

Écrire le script
----------------

Chaque ligne du champ « Script » comporte à gauche le nom d'un champ de l'index et à droite une expression JavaScript.
Encadrez les chaînes de caractères par des guillemets doubles.
Ne mettez pas de point-virgule en fin de ligne.
Avec un point-virgule, la valeur de l'expression devient ``null`` et le champ n'est pas renseigné.
Aucune erreur ni aucun message de journal n'est produit : vous ne pouvez vous en apercevoir qu'en constatant que le champ est vide (pour plus de détails, consultez le « Guide de script JavaScript » dans les références à la fin).

Les noms d'éléments utilisables dans le membre de droite varient selon le connecteur.

- Les connecteurs CSV, JSON et de base de données font directement référence aux noms de colonnes et de champs (pour le CSV, on peut aussi utiliser ``cell1``, ``cell2``, etc.)
- De nombreux connecteurs cloud transmettent l'objet récupéré avec un préfixe. Par exemple, Box, Google Drive et OneDrive utilisent ``file.*``, Slack ``message.*``, Jira ``issue.*`` et Salesforce ``object.*``

Vérifiez les noms d'éléments disponibles dans la description du script de la référence de chaque connecteur (``https://fess.codelibs.org/fr/stable/config/datastore/ds-<nom>.html``).
Si vous faites référence à un nom non défini, par exemple ``url`` au lieu de ``file.url``, l'évaluation de l'expression échoue et l'enregistrement n'est pas indexé.

Exemple : rendre un fichier CSV consultable
===========================================

Dans cet exemple, une FAQ interne est gérée sous forme de fichier CSV, et nous la rendons consultable.
Enregistrez le contenu suivant en UTF-8 sous le nom ``faq.csv``.

.. code-block:: text

    faq_id,question,answer
    1,Quelle est la date limite des notes de frais,Soumettez vos notes de frais avant la fin de chaque mois.
    2,Comment se connecter aux systèmes internes depuis l'extérieur,Connectez-vous à l'aide du client VPN.
    3,Que faire en cas de perte du badge d'accès,Contactez les services généraux pour en demander un nouveau.

Un fichier CSV enregistré avec Excel n'est souvent pas en UTF-8, mais dans un ancien encodage Windows : par exemple windows-1252 avec un Excel en français, ou MS932 avec un Excel en japonais.
Dans ce cas, indiquez l'encodage dans les paramètres présentés plus loin, par exemple ``file_encoding=windows-1252`` ou ``file_encoding=MS932``.
Placez le fichier dans un chemin que le robot d'exploration de Fess peut lire.
Le robot d'exploration s'exécute sur le même serveur que Fess ; dans un environnement ZIP ou RPM / DEB, placez donc le fichier dans un répertoire lisible par l'utilisateur qui exécute Fess.
Si vous voulez simplement essayer avec Docker, le plus simple est de copier le fichier dans le conteneur (il disparaît lorsque le conteneur est recréé).

.. code-block:: bash

    docker cp faq.csv fess01:/tmp/faq.csv

Dans [Robot d'exploration] > [Magasin de données], cliquez sur [Créer nouveau] et saisissez les valeurs suivantes.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Champ
     - Valeur
   * - Nom
     - FAQ interne
   * - Nom du gestionnaire
     - ``CsvDataStore``
   * - Paramètres
     - Voir ci-dessous
   * - Script
     - Voir ci-dessous
   * - Autorisations
     - Laisser ``{role}guest`` (la FAQ peut être recherchée sans connexion)

Paramètres :

.. code-block:: properties

    script_type=javascript
    files=/tmp/faq.csv
    file_encoding=UTF-8
    has_header_line=true

Script :

.. code-block:: javascript

    url="https://intranet.example.com/faq/" + faq_id
    title=question
    content=question + " " + answer
    digest=answer
    label="faq"

Avec ``has_header_line=true``, les noms de colonnes de la première ligne (``faq_id``, ``question``, ``answer``) peuvent être utilisés dans le script.
Pour ``url``, indiquez l'URL d'une page capable d'afficher l'enregistrement ; c'est elle qui s'ouvre lorsqu'on clique sur le lien dans les résultats de recherche.
L'URL de cet exemple est fictive.
Remplacez-la par l'URL de votre véritable page de FAQ.

Après avoir enregistré avec [Créer], créez et exécutez une tâche comme décrit dans la section « Planification » ci-dessous, puis vérifiez le résultat comme décrit dans la section « Vérifier les résultats ».
Si tout fonctionne, une recherche sur « VPN » depuis la page de recherche, en étant déconnecté (ou dans une fenêtre de navigation privée), trouve la deuxième entrée de la FAQ.
Les documents avec ``{role}guest`` sont affichés aux utilisateurs non connectés et aux utilisateurs qui ont le rôle ``guest`` (y compris l'utilisateur initial ``admin``). Ils ne sont pas affichés si vous êtes connecté avec un autre utilisateur.

Pour afficher l'étiquette ``faq`` dans les filtres de la page de recherche, créez dans [Robot d'exploration] > [Étiquette] une étiquette dont la « Valeur » est ``faq`` (voir la section suivante, « Étiquettes »).

Champs de l'index
=================

Les champs couramment définis dans un script sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Champ
     - Description
   * - ``url``
     - Obligatoire. Cible du lien dans les résultats de recherche. Doit être unique pour chaque enregistrement
   * - ``title``
     - Titre dans les résultats de recherche. Recherchable
   * - ``content``
     - Corps du texte. Recherchable
   * - ``digest``
     - Résumé affiché dans les résultats de recherche
   * - ``label``
     - Valeur de l'étiquette (voir plus loin)
   * - ``role``
     - Rôles autorisés à consulter le document. Utilisé lorsque le connecteur fournit des ACL (voir plus loin)

En outre, ``config_id``, ``boost``, ``role``, ``virtual_host``, ``mimetype`` et d'autres champs sont définis automatiquement (``boost``, ``role`` et ``virtual_host`` correspondent aux valeurs de « Boost », « Autorisations » et « Hôtes virtuels » de l'écran de configuration).
Si le script définit le même champ, la valeur du script l'écrase.

Notez les points suivants concernant ``url``.

- Un enregistrement dont l'expression vaut ``null`` n'est pas indexé. Le connecteur CSV n'enregistre pas ces lignes comme URL d'échec ; il écrit seulement une ligne WARN avec leur nombre dans ``fess-crawler.log``
- L'ID de document est construit à partir de l'URL, des rôles et de l'hôte virtuel. Les enregistrements dont ``url`` est une chaîne vide, ou ceux qui ont la même ``url``, obtiennent le même ID de document si leurs rôles et leur hôte virtuel sont aussi identiques ; ils s'écrasent mutuellement et seul le dernier subsiste

Autorisations
=============

Sur l'écran de création, « Autorisations » contient déjà ``{role}guest``.
Cette valeur devient le rôle de tous les documents enregistrés depuis ce magasin de données.
Le rôle invité est attribué aux utilisateurs non connectés ; en l'état, les documents peuvent donc être recherchés sans connexion.
Pour des données qui peuvent être publiques, comme une FAQ interne, vous pouvez laisser cette valeur.

Pour des données dont vous voulez restreindre les lecteurs, contrôlez l'accès de l'une des manières suivantes.

- Remplacez le champ « Autorisations » par les groupes ou rôles qui doivent voir les données (par exemple ``{group}sales``). Tous les documents du magasin de données reçoivent les mêmes autorisations
- Si le connecteur construit des rôles à partir des paramètres de partage (ACL) du service source, faites la correspondance dans le script, par exemple ``role=file.roles``. Le nom de l'élément varie selon le connecteur (``message.roles`` pour Slack), et certains connecteurs nécessitent des paramètres supplémentaires pour récupérer les ACL (comme ``permission_sync=true`` pour Slack). Consultez la référence de chaque connecteur

Lorsque vous utilisez les ACL, supprimez ``{role}guest`` du champ « Autorisations ».
Les connecteurs tels que Box, Slack et Microsoft 365 (OneDrive) incluent aussi la valeur du champ « Autorisations » dans ``file.roles`` / ``message.roles``.
Si vous laissez ``{role}guest``, les documents restent donc consultables sans connexion même si les ACL sont configurées.

À l'inverse, si vous laissez le champ « Autorisations » vide et ne définissez pas non plus ``role`` dans le script, les documents n'ont aucun rôle.
Ces documents ne sont affichés à personne sur la page de recherche.

Les rôles sont écrits lors de l'enregistrement des documents.
Si vous modifiez les autorisations ou le script, les documents existants ne sont pas mis à jour avant la prochaine exploration.
La conception des rôles et des groupes est expliquée dans :doc:`guide-05`.

Étiquettes
==========

L'écran de configuration des magasins de données ne comporte pas le champ « Étiquette » présent sur les écrans de configuration Web et système de fichiers.
Pour attribuer des étiquettes, utilisez l'une des méthodes suivantes.

- Écrivez par exemple ``label="faq"`` dans le script. L'étiquette est attribuée à tous les documents de ce magasin de données
- Dans [Robot d'exploration] > [Étiquette], indiquez dans « Chemins inclus » une expression régulière correspondant aux URL des documents. Lors de l'enregistrement, l'URL est comparée à cette expression régulière et l'étiquette est attribuée aux documents correspondants

« Chemins inclus » est évalué par rapport à l'URL entière ; pour une correspondance par préfixe, ajoutez ``.*`` à la fin (par exemple ``https://intranet\.example\.com/faq/.*``).

Remarque : une étiquette attribuée dans le script est perdue si une seule étiquette de [Robot d'exploration] > [Étiquette] correspond à l'URL du document ; seules les étiquettes correspondantes subsistent.
Les étiquettes créées pour l'exploration Web (par exemple ``https://intranet\.example\.com/.*``) et celles qui ne définissent que « Chemins exclus » sont également prises en compte.
Si vous attribuez des étiquettes dans le script, vérifiez qu'aucune étiquette ne correspond aux URL des documents.

Indiquez la « Valeur » d'une étiquette uniquement avec des caractères alphanumériques et des traits de soulignement (les traits d'union et les caractères non ASCII comme le japonais ne sont pas acceptés).
Pour afficher l'étiquette parmi les choix d'étiquettes de la page de recherche, enregistrez une étiquette de même valeur dans [Robot d'exploration] > [Étiquette], même si vous l'attribuez dans le script.
Dans ce cas, « Chemins inclus » peut rester vide.

Boost
=====

La valeur « Boost » de l'écran de configuration des magasins de données (``1.0`` par défaut) est appliquée à tous les documents enregistrés depuis ce magasin de données.
La valeur de boost est multipliée par le score lors de la recherche.
Pour faire remonter les documents d'une source de données particulière, modifiez cette valeur de boost.

Les règles de [Robot d'exploration] > [Boost de document] ne s'appliquent qu'aux documents enregistrés par l'exploration Web et l'exploration de fichiers.
Elles ne s'appliquent pas aux documents des magasins de données.

Planification
=============

La tâche « Default Crawler » présente par défaut s'exécute tous les jours à 0:00 et explore toutes les configurations Web, système de fichiers et magasin de données activées.
Pour exécuter chaque magasin de données à une fréquence différente, créez une tâche par configuration.

1. Dans la liste de [Robot d'exploration] > [Magasin de données], cliquez sur le nom de la configuration pour ouvrir l'écran de détails
2. Cliquez sur [Créer une nouvelle tâche]. L'écran de création du planificateur s'ouvre, avec « Nom » (``Data Crawler - FAQ interne``) et un script qui n'explore que cette configuration déjà renseignés
3. Saisissez l'heure d'exécution dans « Planification » au format cron (minute heure jour mois jour-de-la-semaine), puis cliquez sur [Créer]. Exemple : ``0 2 * * *`` (tous les jours à 2:00)

Une tâche dont la « Planification » est vide ne s'exécute pas périodiquement ; elle ne s'exécute que manuellement.
Pour l'essayer immédiatement, ouvrez la tâche créée dans [Système] > [Planificateur] et cliquez sur [Démarrer maintenant].

Même si vous créez une tâche pour une configuration, « Default Crawler » continue aussi d'explorer cette configuration.
Pour éviter une double exécution, désactivez le « Statut » de cette configuration de magasin de données.
« Default Crawler » ne traite que les configurations activées, mais une tâche qui indique un ID de configuration explore aussi les configurations désactivées.
Si vous créez une tâche dédiée pour chaque configuration, vous pouvez aussi vider la « Planification » de « Default Crawler » (voir :doc:`guide-04`).

Expiration des documents
========================

Les documents enregistrés depuis un magasin de données ont une date d'expiration.
Elle correspond à l'heure de début de l'exploration plus le nombre de jours de « Supprimer les anciens documents » dans [Système] > [Général] (``3`` jours par défaut).
Les documents expirés sont supprimés de l'index par la tâche « Doc Purger », exécutée toutes les minutes.
Lorsque le même document est réenregistré lors de l'exploration suivante, son expiration est prolongée.

Par conséquent, les documents disparaissent des résultats de recherche dans les deux cas suivants.

- L'intervalle entre les exécutions de la tâche est plus long que le nombre de jours de « Supprimer les anciens documents »
- Dans une exploration incrémentale qui ne lit que les éléments modifiés (comme ``incremental=true`` pour Git ou Google Drive), les documents inchangés ne sont pas réenregistrés

Pour modifier l'expiration par configuration, indiquez ``time_to_live`` en minutes dans les paramètres (par exemple ``time_to_live=11520`` pour 8 jours).
Les éléments supprimés des données sources ne disparaissent eux aussi des résultats de recherche qu'à l'expiration de ce délai.
Si le délai est trop long, les suppressions mettent très longtemps à être prises en compte.

Vérifier les résultats
======================

Dans l'exploration de magasins de données, un statut de tâche « OK » ne signifie pas forcément que tout a réussi.
Même lorsqu'une exception se produit dans le connecteur, Fess l'enregistre par configuration ou par enregistrement et poursuit le traitement.
Le statut du journal des tâches est donc « OK », et le « Statut du robot d'exploration » de [Informations système] > [Informations sur l'exploration] ne change pas non plus.
Vérifiez les points suivants dans l'ordre.

1. Dans [Informations système] > [Journal des tâches], vérifiez que la tâche est terminée. La ligne ``Data Config Id:`` du « Résultat » indique l'ID de la configuration concernée
2. Dans [Informations système] > [Informations sur l'exploration], vérifiez la « Taille de l'index (Magasin de données) » de la session. Il s'agit du nombre de documents enregistrés pendant cette session (pour « Default Crawler », le total de tous les magasins de données)
3. Dans [Informations système] > [URL d'échec], vérifiez qu'aucune erreur n'a été enregistrée
4. Téléchargez ``fess-crawler.log`` depuis [Informations système] > [Fichier journal] et vérifiez les lignes ERROR et WARN (le fichier se trouve dans ``/var/log/fess/`` pour Docker et RPM / DEB, et dans ``logs/`` pour le paquet ZIP)
5. Dans [Informations système] > [Rechercher], recherchez par exemple ``label:faq`` et vérifiez le nombre de résultats

L'endroit où subsistent les indices dépend de la manière dont l'exploration échoue.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Situation
     - URL d'échec
     - fess-crawler.log
   * - Le gestionnaire est introuvable (par exemple si le plugin a été supprimé après la création de la configuration)
     - Aucun enregistrement
     - ``DataStore(...) is not found.``
   * - Échec de toute la configuration (erreur d'authentification empêchant le connecteur de continuer, paramètre obligatoire manquant, etc.)
     - Une entrée. La colonne URL contient ``D<ID de configuration>:<nom de configuration>``
     - ``Failed to process a data crawling: <nom de configuration>``
   * - Échec d'un enregistrement (erreur d'évaluation du script, etc.)
     - Une entrée par enregistrement. Pour le CSV, ``<chemin du fichier>:<numéro de ligne>``
     - Lignes WARN

Avec le connecteur CSV, ce n'est pas non plus une erreur lorsque le fichier indiqué dans ``files`` est introuvable ou que son extension n'est pas ``.csv`` / ``.tsv``.
Le connecteur émet les messages WARN ``is not found.`` et ``No CSV file.`` et se termine avec 0 document.

[Informations système] > [Rechercher] affiche tous les documents sans filtrage par autorisations, ce qui le rend adapté à la vérification du nombre de documents.
En revanche, il ne permet pas de vérifier si les autorisations sont conformes à vos intentions.
Vérifiez les autorisations sur la page de recherche normale, connecté avec l'utilisateur concerné (ou déconnecté pour les documents avec ``{role}guest``) (:doc:`guide-05`).

Si vous ne savez pas quels noms d'éléments un connecteur transmet, certains connecteurs écrivent les valeurs récupérées dans le journal lorsque le niveau de journalisation du robot d'exploration est réglé sur DEBUG (le connecteur CSV affiche les valeurs de chaque ligne).
Pour la configuration, consultez « Configuration de débogage » dans l'`Aperçu des connecteurs DataStore <https://fess.codelibs.org/fr/stable/config/datastore/ds-overview.html>`__.

Articles et références par connecteur
=====================================

Les paramètres de chaque connecteur sont expliqués dans les articles suivants.

- :doc:`guide-06` - Git, Confluence, Jira, Slack
- :doc:`guide-07` - Google Drive, SharePoint Online / OneDrive, Box
- :doc:`guide-12` - Bases de données, CSV, Salesforce

Références :

- `Aperçu des connecteurs DataStore <https://fess.codelibs.org/fr/stable/config/datastore/ds-overview.html>`__ (liste de tous les connecteurs et noms des plugins)
- `Connecteur CSV <https://fess.codelibs.org/fr/stable/config/datastore/ds-csv.html>`__ / `Connecteur JSON <https://fess.codelibs.org/fr/stable/config/datastore/ds-json.html>`__ / `Connecteur de base de données <https://fess.codelibs.org/fr/stable/config/datastore/ds-database.html>`__
- `Google Drive <https://fess.codelibs.org/fr/stable/config/datastore/ds-gsuite.html>`__ / `Microsoft 365 <https://fess.codelibs.org/fr/stable/config/datastore/ds-microsoft365.html>`__ / `Box <https://fess.codelibs.org/fr/stable/config/datastore/ds-box.html>`__
- `Atlassian <https://fess.codelibs.org/fr/stable/config/datastore/ds-atlassian.html>`__ / `Slack <https://fess.codelibs.org/fr/stable/config/datastore/ds-slack.html>`__ / `Git <https://fess.codelibs.org/fr/stable/config/datastore/ds-git.html>`__ / `Salesforce <https://fess.codelibs.org/fr/stable/config/datastore/ds-salesforce.html>`__
- `Crawl de magasin de données (console d'administration) <https://fess.codelibs.org/fr/stable/admin/dataconfig-guide.html>`__ / `Planificateur de tâches <https://fess.codelibs.org/fr/stable/admin/scheduler-guide.html>`__ / `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__ / `Étiquette <https://fess.codelibs.org/fr/stable/admin/labeltype-guide.html>`__ / `Guide de script JavaScript <https://fess.codelibs.org/fr/stable/config/scripting-javascript.html>`__
