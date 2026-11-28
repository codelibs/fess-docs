============================================
Rechercher sites web et serveurs de fichiers
============================================

Introduction
============

Les documents internes ont tendance à être répartis entre plusieurs emplacements : le portail intranet, les dossiers partagés des services, un répertoire où l'on archive les anciens documents, etc.
Pour trouver quelque chose, il faut d'abord se souvenir de l'endroit où il se trouve, puis chercher séparément à chaque endroit.

Dans cet article, nous utilisons Fess 15.9 pour explorer les trois emplacements suivants et les rendre consultables depuis une seule zone de recherche.
Sur la page de recherche, nous permettons de restreindre les résultats à l'aide d'étiquettes, par exemple « portail uniquement » ou « dossier partagé uniquement ».

- Le portail intranet (un site web)
- Un dossier partagé sur un serveur de fichiers Windows (SMB)
- Un répertoire d'archives sur le serveur (fichiers locaux)

Les étapes supposent l'environnement Docker démarré dans :doc:`guide-02` (``fess01`` et ``search01``).
Les stockages cloud comme Google Drive, SharePoint et Box sont traités dans :doc:`guide-07`.
Les points à vérifier avant de mettre en place la recherche sur serveur de fichiers sont résumés dans :doc:`file-server-search`.

Ce que nous allons construire
=============================

.. list-table::
   :header-rows: 1
   :widths: 18 40 14 28

   * - Cible
     - Chemin à explorer
     - Valeur de l'étiquette
     - Exécution de l'exploration
   * - Portail intranet
     - ``https://portal.example.com/``
     - ``portal``
     - Tous les jours à 2 h 00
   * - Dossier partagé
     - ``smb://fileserver.example.com/shared/``
     - ``shared``
     - Tous les jours à 3 h 00
   * - Archives
     - ``file:/data/archive/`` (``/srv/archive`` sur l'hôte)
     - ``archive``
     - Chaque dimanche à 4 h 00

Les noms d'hôte et les répertoires sont des exemples.
Adaptez-les à votre propre environnement.
Nous supposons que vous disposez d'un compte de service capable de lire le dossier partagé (la lecture seule suffit) et que le conteneur ``fess01`` peut se connecter au port SMB (445) du serveur de fichiers.

Les étiquettes sont attribuées au moment de l'exploration ; créez-les donc avant les configurations d'exploration.
Suivez les sections de cet article dans l'ordre.

Rendre le répertoire d'archives lisible depuis le conteneur
===========================================================

Dans le ``compose.yaml`` de docker-fess v15.9.0, aucun volume n'est défini pour ``fess01``.
Par conséquent, le répertoire ``/srv/archive`` de l'hôte n'est pas visible tel quel depuis l'intérieur du conteneur.
Ajoutez ``volumes`` à ``fess01`` dans ``compose.yaml``, et ajoutez également une ligne ``FESS_JAVA_OPTS`` à ``environment``.

.. code-block:: yaml

    services:
      fess01:
        image: ghcr.io/codelibs/fess:15.9.0
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_JAVA_OPTS=-Duser.timezone=Asia/Tokyo -Dfess.system.day.for.cleanup=10"
        volumes:
          - /srv/archive:/data/archive:ro
        # ports et la suite restent inchangés

- ``/srv/archive:/data/archive:ro`` monte ``/srv/archive`` de l'hôte en lecture seule sur ``/data/archive`` dans le conteneur
- ``-Duser.timezone=Asia/Tokyo`` permet d'interpréter les heures d'exécution des tâches configurées plus loin en heure du Japon. Ni compose.yaml ni l'image ne définissent de fuseau horaire ; sans cette option, les tâches s'exécutent à des heures décalées par rapport à l'heure du Japon
- ``-Dfess.system.day.for.cleanup=10`` fixe à 10 jours la valeur par défaut du délai d'expiration des documents (en jours). La raison est expliquée plus loin dans « Tâches hebdomadaires et expiration des documents »

Après la modification, recréez les conteneurs.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Comme ``fess01`` est recréé, les paramètres modifiés jusque-là dans [Système] > [Général] sont perdus (voir « Arrêt et redémarrage » dans :doc:`guide-02`).
Effectuez les modifications dans [Général] après cette étape.

Dans le conteneur, Fess s'exécute sous l'utilisateur ``fess`` (UID 1001).
Vérifiez que cet utilisateur peut lister les fichiers.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -u fess fess01 ls /data/archive

Si vous obtenez ``Permission denied``, rendez le contenu de ``/srv/archive`` sur l'hôte lisible par l'UID 1001 (par exemple en accordant aux autres utilisateurs le droit de lecture, et le droit d'exécution sur les répertoires).

Créer les étiquettes
====================

Une étiquette est attribuée lorsque l'URL d'un document correspond à une expression régulière.
Les écrans de configuration d'exploration n'ont pas de champ pour choisir une étiquette (il est masqué par défaut) ; la portée de chaque étiquette se définit donc dans le champ « Chemins inclus » de l'étiquette elle-même.

Dans [Robot d'exploration] > [Étiquette] > [Créer nouveau], créez les trois étiquettes suivantes.

.. list-table::
   :header-rows: 1
   :widths: 18 14 68

   * - Nom
     - Valeur
     - Chemins inclus
   * - Portail
     - ``portal``
     - ``https://portal.example.com/.*``
   * - Dossier partagé
     - ``shared``
     - ``smb://fileserver.example.com/shared/.*``
   * - Archives
     - ``archive``
     - ``file:/data/archive/.*``

- « Nom » est le texte affiché sur la page de recherche ; il peut contenir des caractères non ASCII, comme des lettres accentuées ou du japonais
- « Valeur » n'accepte que les caractères alphanumériques et le trait de soulignement (les traits d'union et les caractères non ASCII provoquent une erreur de saisie)
- « Chemins inclus » doit correspondre à l'URL entière ; n'omettez donc pas le ``.*`` final. S'il reste vide, l'étiquette n'est attribuée à aucun document
- « Autorisations » contient ``{role}guest``. L'étiquette est ainsi affichée aussi aux utilisateurs non connectés ; laissez-la telle quelle

Les documents explorés avant la création des étiquettes n'ont pas d'étiquette.
Si vous ajoutez ou modifiez des étiquettes par la suite, appliquez-les aux documents existants soit en relançant l'exploration, soit en exécutant « Label Updater » avec [Démarrer maintenant] dans [Système] > [Planificateur].

Créer les configurations d'exploration
======================================

Portail intranet (exploration Web)
----------------------------------

Dans [Robot d'exploration] > [Web] > [Créer nouveau], saisissez les champs suivants, puis cliquez sur [Créer].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Valeur
   * - Nom
     - ``Portail intranet``
   * - URL
     - ``https://portal.example.com/``
   * - URL incluses
     - ``https://portal.example.com/.*``
   * - URL exclues
     - Ajouter ``https://portal.example.com/admin/.*`` sous les lignes déjà présentes

« URL exclues » contient dès le départ des expressions régulières qui excluent les images, les CSS, etc.
Ne les supprimez pas : ajoutez une ligne.
« Nombre de threads » vaut ``1`` et « Intervalle » ``10000`` millisecondes par défaut, des réglages qui limitent la charge sur le portail.

Dossier partagé (SMB) et authentification de fichier
----------------------------------------------------

Créez d'abord la configuration suivante dans [Robot d'exploration] > [Système de fichiers] > [Créer nouveau].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Valeur
   * - Nom
     - ``Dossier partagé``
   * - Chemins
     - ``smb://fileserver.example.com/shared/``
   * - Chemins inclus
     - ``smb://fileserver.example.com/shared/.*``
   * - Chemins exclus
     - ``.*\.tmp$``

Pour l'exploration de fichiers, « Nombre de threads » vaut ``5`` et « Intervalle » ``1000`` millisecondes par défaut.

Associez ensuite le compte de service à cette configuration.
Une authentification de fichier se crée en sélectionnant une configuration d'exploration de fichiers.
Tant qu'aucune configuration d'exploration de fichiers n'existe, [Créer nouveau] n'est pas affiché sur l'écran [Authentification de fichier].

Dans [Robot d'exploration] > [Authentification de fichier] > [Créer nouveau], saisissez les champs suivants, puis cliquez sur [Créer].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Valeur
   * - Nom d'hôte
     - ``fileserver.example.com`` (écrit exactement comme le nom d'hôte du chemin)
   * - Port
     - Vide
   * - Schéma
     - ``Samba``
   * - Nom d'utilisateur / Mot de passe
     - Ceux du compte de service
   * - Paramètres
     - Pour un compte de domaine, indiquer le nom de domaine, par exemple ``domain=EXAMPLE``
   * - Configuration de l'exploration de fichiers
     - ``Dossier partagé``

« Nom d'hôte » doit correspondre littéralement au nom d'hôte du chemin.
Si vous avez écrit le chemin avec une adresse IP, saisissez aussi l'adresse IP ici.
Une authentification dont le « Port » est vide s'applique aux chemins qui ne précisent pas de port, comme ``smb://nom-hote/nom-partage/``.

.. note::

   Par défaut, les fichiers explorés via SMB reçoivent des rôles dérivés des droits d'accès (ACL) du fichier, qui sont ajoutés aux « Autorisations » de la configuration d'exploration.
   Tant que la valeur initiale ``{role}guest`` reste dans « Autorisations », tout le monde peut les rechercher, y compris les utilisateurs non connectés.
   Pour adapter les résultats de recherche aux droits d'accès, consultez :doc:`file-server-search` et :doc:`guide-05`.

Archives (fichiers locaux)
--------------------------

Dans [Robot d'exploration] > [Système de fichiers] > [Créer nouveau], créez la configuration suivante.
Indiquez le chemin tel qu'il apparaît dans le conteneur.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Valeur
   * - Nom
     - ``Archives``
   * - Chemins
     - ``file:/data/archive/``
   * - Chemins inclus
     - ``file:/data/archive/.*``
   * - Chemins exclus
     - ``.*\.(log|bak)$``

Les fichiers locaux s'écrivent avec une seule barre oblique après ``file:``, comme ``file:/data/archive/``.
Les URL des fichiers trouvés par le robot ont la forme ``file:/data/archive/2020/report.pdf``, et « Chemins inclus » est comparé à ces URL.
Si vous écrivez ``file:///data/archive/.*``, aucun fichier ne correspond et rien n'est indexé.

Créer une tâche par configuration
=================================

La tâche « Default Crawler » du planificateur exécute ensemble toutes les configurations d'exploration actives, tous les jours à 0 h 00.
Pour exécuter chaque cible à une heure différente, créez une tâche par configuration d'exploration.

1. Dans [Robot d'exploration] > [Web], cliquez sur « Portail intranet », puis sur [Créer une nouvelle tâche] dans l'écran de détails
2. L'écran de création de tâche s'ouvre ; « Nom » contient ``Web Crawler - Portail intranet`` et « Script » un contenu qui n'explore que cette configuration
3. « Planification » est vide ; saisissez une expression cron et cliquez sur [Créer]
4. Faites de même pour « Dossier partagé » et « Archives » dans [Robot d'exploration] > [Système de fichiers] (les noms prennent la forme ``File Crawler - Dossier partagé``)

.. list-table::
   :header-rows: 1
   :widths: 40 25 35

   * - Tâche
     - Planification
     - Signification
   * - ``Web Crawler - Portail intranet``
     - ``0 2 * * *``
     - Tous les jours à 2 h 00
   * - ``File Crawler - Dossier partagé``
     - ``0 3 * * *``
     - Tous les jours à 3 h 00
   * - ``File Crawler - Archives``
     - ``0 4 * * 0``
     - Chaque dimanche à 4 h 00

Une expression cron suit l'ordre « minute heure jour mois jour-de-la-semaine », et le jour de la semaine ``0`` correspond au dimanche.

Enfin, empêchez « Default Crawler » d'explorer à nouveau les mêmes configurations à 0 h 00.
Dans [Système] > [Planificateur], cliquez sur « Default Crawler », videz « Planification » via [Modifier], puis cliquez sur [Mettre à jour].
Si vous laissez « Activé » coché dans « Statut », vous pouvez toujours l'exécuter avec [Démarrer maintenant] lorsque vous voulez explorer toutes les configurations ensemble (si vous la désactivez, [Démarrer maintenant] n'est plus affiché).

Tâches hebdomadaires et expiration des documents
------------------------------------------------

Les documents indexés par une exploration reçoivent une date d'expiration ; une fois celle-ci passée, la tâche « Doc Purger » (exécutée chaque minute) les supprime de l'index.
La date d'expiration correspond à l'heure de début de l'exploration plus le nombre de jours défini dans « Supprimer les anciens documents » sous [Système] > [Général], soit ``3`` jours par défaut.
Si l'exploration suivante retrouve le même fichier, sa date d'expiration est prolongée.

Avec la valeur par défaut, les documents des archives, explorées uniquement le dimanche, ne sont plus trouvables dès le mercredi.
Ce nombre de jours doit donc être supérieur à l'intervalle d'exploration le plus long (7 jours).
Dans cet article, nous le fixons à ``10`` jours, avec une marge pour que les documents ne disparaissent pas même si une tâche échoue une fois.

- Dans l'environnement Docker, l'option ``-Dfess.system.day.for.cleanup=10`` mentionnée plus haut devient cette valeur par défaut. Les valeurs saisies dans [Général] sont perdues lorsque ``fess01`` est recréé ; l'inscrire dans compose.yaml est donc plus sûr
- Dans les environnements autres que Docker, réglez « Supprimer les anciens documents » à ``10`` dans [Général] et cliquez sur [Mettre à jour]

Allonger ce nombre de jours signifie aussi que les fichiers supprimés du serveur de fichiers restent dans les résultats de recherche jusqu'à ce nombre de jours après la dernière exploration qui les a trouvés.

Exécuter et vérifier les résultats
==================================

Exécuter les tâches
-------------------

Sans attendre le lendemain, dans [Système] > [Planificateur], cliquez successivement sur les trois tâches, puis sur [Démarrer maintenant] pour chacune.

Vérifier la fin de l'exécution
------------------------------

1. Dans [Informations système] > [Journal des tâches], attendez que le « Statut » des trois tâches passe de « En cours d'exécution » à « OK ». En cas d'« Échec », cliquez sur la ligne et consultez « Résultat »
2. Dans [Informations système] > [Informations sur l'exploration], consultez « Taille de l'index (Web/Fichier) » de chaque session et vérifiez que le nombre de documents indexés est proche de vos attentes
3. Si le nombre est faible, ouvrez [Informations système] > [URL d'échec]. Les URL qui n'ont pas pu être récupérées y sont enregistrées avec le type d'erreur et le journal

Les causes fréquentes sont les suivantes.

- Le dossier partagé compte 0 document et des chemins du partage figurent dans URL d'échec : vérifiez le « Nom d'hôte » de l'authentification de fichier et l'écriture du chemin, la « Configuration de l'exploration de fichiers » sélectionnée et le mot de passe. Si le journal montre des erreurs de connexion, vérifiez que le conteneur peut résoudre le nom du serveur de fichiers et atteindre le port 445
- Les archives comptent 0 document et URL d'échec est vide : vérifiez que le chemin n'est pas écrit avec ``file:///`` et que « Chemins inclus » a la même forme que le chemin
- Des erreurs de lecture se produisent sur les archives : vérifiez avec la commande ``exec -u fess`` présentée plus haut que le conteneur peut lire les fichiers

Filtrer par étiquette
---------------------

Sur ``http://localhost:8080/``, recherchez un mot susceptible de figurer aux trois emplacements.
Les résultats mêlent des pages du portail, des documents Office du dossier partagé, des PDF des archives, etc., classés par pertinence.

Sur la page de recherche de la 15.9 (thème ``bootstrap``), le filtrage par étiquette se trouve à deux endroits.

- La liste « Étiquette » affichée à côté des résultats de recherche : les étiquettes présentes dans les résultats y figurent avec leur nombre, et un clic restreint les résultats à cette étiquette
- Le bouton en forme d'engrenage à droite de la zone de recherche : il ouvre « Options de recherche », où vous sélectionnez une ou plusieurs entrées dans la liste « Étiquettes » avant de cliquer sur [Rechercher]. Si vous en sélectionnez plusieurs, les documents portant l'une de ces étiquettes sont inclus ; si vous n'en sélectionnez aucune, tout est inclus

Lors du filtrage, un paramètre comme ``fields.label=shared`` est ajouté à l'URL.
Si « Étiquette » n'apparaît pas à côté des résultats, ou si le filtrage donne 0 résultat, vérifiez que vous n'avez pas lancé l'exploration avant de créer les étiquettes (exécuter « Label Updater » corrige le problème).
Si la liste « Étiquettes » n'apparaît pas dans « Options de recherche », vérifiez que les « Autorisations » de l'étiquette incluent le rôle de la personne qui recherche.

Liens des résultats de recherche et mappage de chemin
=====================================================

Lorsque vous cliquez sur un résultat provenant du dossier partagé ou des archives, Fess lit le fichier et le renvoie au navigateur.
C'est le rôle de « Search File Proxy » dans [Général], activé par défaut.
Les fichiers peuvent ainsi être ouverts même si le navigateur ne peut pas ouvrir directement les URL ``smb://`` ou ``file:``.

Si les mêmes fichiers que les archives sont également publiés sur un serveur web interne (ici ``https://archive.example.com/``) et que vous voulez qu'ils soient ouverts depuis celui-ci, convertissez les URL avec un mappage de chemin.

Dans [Robot d'exploration] > [Mappage de chemin] > [Créer nouveau], saisissez les champs suivants, puis cliquez sur [Créer].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Valeur
   * - Expression régulière
     - ``^file:/data/archive/(.*)$``
   * - Remplacement
     - ``https://archive.example.com/$1``
   * - Type de processus
     - Affichage

« Type de processus » a initialement « Exploration » sélectionné ; changez-le impérativement en « Affichage ».

- Affichage : l'URL dans l'index reste ``file:/data/archive/...`` ; seule la destination du lien d'un résultat de recherche change. Le réglage prend effet dès sa création, sans nouvelle exploration
- Exploration : réécrit l'URL stockée elle-même dans l'index. Le réglage ne prend effet qu'après une nouvelle exploration, et les « Chemins inclus » des étiquettes doivent aussi être adaptés aux URL ``https://`` réécrites

Après la configuration, effectuez une recherche et cliquez sur un résultat des archives pour vérifier que le serveur web ``https://archive.example.com/`` s'ouvre.

Pour aller plus loin
====================

- Adapter les résultats de recherche visibles au service ou au poste de chacun : :doc:`guide-05`
- Vérifier les prérequis de la recherche sur serveur de fichiers (formats pris en charge, reprise des droits d'accès) : :doc:`file-server-search`
- Rechercher aussi les fichiers de Google Drive, SharePoint et Box : :doc:`guide-07`
- Améliorer la qualité de recherche à partir des journaux de recherche : :doc:`guide-08`
- Mettre en place la supervision et les sauvegardes pour l'exploitation en production : :doc:`guide-10`

Références
==========

- `Crawl de système de fichiers (recherche sur serveur de fichiers) <https://fess.codelibs.org/fr/stable/admin/fileconfig-guide.html>`__
- `Authentification de fichier <https://fess.codelibs.org/fr/stable/admin/fileauth-guide.html>`__
- `Étiquette <https://fess.codelibs.org/fr/stable/admin/labeltype-guide.html>`__
- `Planificateur de tâches <https://fess.codelibs.org/fr/stable/admin/scheduler-guide.html>`__
- `Général <https://fess.codelibs.org/fr/stable/admin/general-guide.html>`__
- `Mappage de chemin <https://fess.codelibs.org/fr/stable/admin/pathmap-guide.html>`__
- `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__
