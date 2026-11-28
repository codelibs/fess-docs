===================================================
Exploiter Fess : supervision, sauvegarde, dépannage
===================================================

Introduction
============

Une fois Fess ouvert à toute l'organisation, les exploitants se retrouvent typiquement dans des situations comme celles-ci :
ils n'apprennent que la recherche ne fonctionne plus qu'au moment où les utilisateurs s'en plaignent, ils ne remarquent pas pendant plusieurs jours que l'exploration nocturne échoue, ou bien les paramètres ne reviennent pas après la reconstruction d'un serveur.

Cet article explique comment se préparer à ces situations à l'aide des mécanismes intégrés à Fess 15.9.

- Vérifier l'état de Fess et d'OpenSearch depuis un outil de supervision externe avec ``/api/v2/health`` et ``/api/admin/stats``
- Recevoir par e-mail, Slack ou Google Chat les notifications de fin d'exploration, de changement d'état d'OpenSearch et de journaux d'erreurs
- Savoir ce que contient chaque fichier journal et où il se trouve
- Sauvegarder les paramètres avec cron et les restaurer sur un autre serveur
- Savoir quels écrans et quels journaux de Fess consulter en cas d'incident

La gestion des paramètres sous forme de code est traitée dans :doc:`guide-16`, et la montée en charge face à l'augmentation du nombre de documents et d'utilisateurs (y compris le réglage du tas) dans :doc:`guide-14`.
Les exemples de commandes supposent l'environnement Docker de :doc:`guide-02` (``fess01`` et ``search01``).
Les différences pour la version ZIP et les paquets RPM/DEB sont indiquées au fur et à mesure.

Superviser
==========

Surveillance de disponibilité : /api/v2/health
----------------------------------------------

Fess fournit une API de vérification de l'état qui peut être appelée sans authentification.

::

    $ curl -fsS --max-time 10 http://localhost:8080/api/v2/health
    {"response":{"status":0,"engine":{"status":"GREEN","ping_status":0}}}

Les codes de statut HTTP ont la signification suivante.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Statut
     - État
   * - 200
     - Fess répond, et le cluster OpenSearch est ``GREEN`` ou ``YELLOW``
   * - 503
     - Le cluster OpenSearch est ``RED``, ou Fess ne parvient pas à se connecter à OpenSearch (``error.details.engine.status`` vaut ``UNAVAILABLE``)
   * - Pas de réponse / délai dépassé
     - Le processus Fess est arrêté, ou Fess attend un OpenSearch qui ne répond pas

L'outil de supervision doit s'appuyer sur ce code de statut.
Avec ``curl``, l'option ``-f`` rend le code de sortie non nul en cas de 503.
Si OpenSearch cesse de répondre sans que son processus s'arrête, cette API attend la réponse d'OpenSearch jusqu'à ``index.health.timeout`` (``10m`` par défaut).
Côté supervision, définissez un délai d'expiration, comme ``--max-time 10`` dans l'exemple ci-dessus, et traitez aussi le dépassement de délai comme une anomalie.
Notez que ``/api/v1/health``, présenté dans les versions précédentes de cet article, n'est pas disponible dans une installation standard de 15.9 (``/api/v1`` n'est fourni que si le plugin ``fess-webapp-v1-api`` est installé).

Sous Docker, ``fess01`` utilise cette API à travers deux mécanismes.

- Le ``healthcheck`` de ``compose.yaml`` l'appelle toutes les 30 secondes ; le résultat apparaît sous la forme ``(healthy)`` dans ``docker compose ps``
- Le script de démarrage du conteneur l'appelle également toutes les 60 secondes et, une fois Fess démarré, arrête le conteneur après 5 réponses consécutives autres que 200. Grâce à ``restart: unless-stopped``, le conteneur est ensuite redémarré

Par conséquent, si OpenSearch reste ``RED`` pendant quelques minutes, ``fess01`` redémarre en boucle.
Lorsque ``fess01`` redémarre sans cesse, vérifiez d'abord ``search01``.

Surveillance des ressources : /api/admin/stats
----------------------------------------------

L'utilisation du tas et l'espace disque libre s'obtiennent avec l'API d'administration ``GET /api/admin/stats``.
[Informations système] > [Informations de configuration] ne contient qu'une liste de propriétés et n'affiche pas l'utilisation de la mémoire.

L'API d'administration nécessite un jeton d'accès.

1. Ouvrez [Système] > [Jeton d'accès] et cliquez sur [Créer nouveau]
2. Saisissez l'usage dans « Nom » (par exemple ``monitoring``) et ``{role}admin-api`` dans « Autorisations », puis cliquez sur [Créer]
3. Ouvrez le jeton créé depuis la liste et notez la valeur de « Jeton »

.. warning::

   Un jeton ``{role}admin-api`` permet d'utiliser toutes les API d'administration, y compris celles qui modifient ou suppriment des paramètres.
   Aucun paramètre ne permet de le restreindre à la lecture seule.
   Conservez-le, par exemple dans un fichier du serveur de supervision, avec le même soin que le mot de passe administrateur.

Transmettez le jeton dans l'en-tête ``Authorization``.
L'exemple suivant extrait l'utilisation du tas (%) et le taux d'utilisation de chaque système de fichiers.

::

    $ curl -fsS -H "Authorization: Bearer <jeton>" http://localhost:8080/api/admin/stats \
        | jq '{heap: .response.stats.jvm.memory.heap.percent, fs: [.response.stats.fs[] | {path, percent}]}'

La réponse contient aussi le nombre et la durée cumulée des GC (``jvm.gc``), l'utilisation du CPU et la charge moyenne du système d'exploitation (``os``), ainsi que l'état du cluster OpenSearch et le nombre de shards (``engine``).
Pour la liste complète des champs, consultez `API Stats <https://fess.codelibs.org/fr/stable/api/admin/api-admin-stats.html>`__.

Gardez à l'esprit les deux points suivants en lisant les valeurs.

- ``jvm`` correspond à la JVM de Fess lui-même (l'application web). Les explorations s'exécutent dans un processus JVM distinct ; un manque de mémoire du robot d'exploration n'apparaît donc pas ici. Vérifiez-le dans ``fess-crawler.log`` (voir plus loin)
- ``fs`` correspond aux systèmes de fichiers de l'hôte sur lequel tourne Fess (le conteneur sous Docker). Pour connaître l'espace libre de la zone de données d'OpenSearch, interrogez directement OpenSearch

::

    $ curl -s "http://localhost:9200/_cat/allocation?v"

Pour modifier la taille du tas, consultez :doc:`guide-14`.

Recevoir des notifications
--------------------------

Les destinataires des notifications de Fess se configurent avec trois champs de la section « Notification » de [Système] > [Général].

- « E-mail de notification » : adresses e-mail des destinataires (séparées par des virgules s'il y en a plusieurs)
- « Slack Webhook URLs » : URL d'Incoming Webhook de Slack
- « Google Chat Webhook URLs » : URL de Webhook de Google Chat

Dès que l'un d'eux est renseigné, les trois types de notifications suivants sont envoyés aux mêmes destinataires.

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Notification
     - Condition d'envoi
     - Paramètres supplémentaires requis
   * - Fin d'exploration (objet ``[FESS] Crawler completed``)
     - Envoyée à chaque fin de tâche d'exploration, qu'elle ait réussi ou non. Elle indique le statut (OK/FAIL) et le nombre de documents indexés
     - Aucun
   * - Changement d'état d'OpenSearch (objet ``[FESS] Status Change``)
     - La tâche du planificateur « Search Engine Monitor » interroge OpenSearch chaque minute et envoie une notification lorsque le cluster passe à ``RED`` et lorsqu'il quitte l'état ``RED``
     - Aucun
   * - Notification des journaux (objet ``[FESS] ERROR Log Alert``)
     - La tâche « Log Notification » regroupe toutes les 5 minutes les journaux ERROR (ou de niveau supérieur ou égal au niveau choisi) écrits par Fess, le robot d'exploration et les autres processus, et les envoie ensemble
     - Activer « Log Notification » dans [Général] et choisir un « Log Notification Level »

Si Fess ne parvient pas à se connecter à OpenSearch, la tâche « Search Engine Monitor » elle-même échoue et aucune notification de changement d'état n'est envoyée.
Détectez les pertes de connexion en surveillant ``/api/v2/health`` depuis l'extérieur, comme décrit dans la section précédente.

Le niveau par défaut de la notification des journaux est ``ERROR``.
Les tâches planifiées en échec sont journalisées au niveau ``WARN`` (``Failed to execute job: ...``) ; pour être averti aussi des échecs de tâches, réglez « Log Notification Level » sur ``WARN``.
Dans ce cas, tous les autres messages ``WARN`` sont également notifiés.

Pour recevoir des e-mails, configurez le serveur SMTP dans deux fichiers et redémarrez Fess.

::

    mail.smtp.server.main.host.and.port=smtp.example.com:587

- ``fess_env_web.properties`` : utilisé pour la notification des journaux, les changements d'état et le bouton [Envoyer un e-mail de test]
- ``fess_env_crawler.properties`` : utilisé pour la notification de fin d'exploration (car l'exploration s'exécute dans un processus distinct)

Ces fichiers se trouvent dans ``app/WEB-INF/classes/`` pour la version ZIP et dans ``/etc/fess/`` pour les paquets RPM/DEB.
Après la configuration, vérifiez la réception avec [Envoyer un e-mail de test] dans [Général].

Pour recevoir rapidement des notifications sous Docker, un webhook Slack ou Google Chat est le plus simple, car aucun fichier n'est à modifier.
Toutefois, les paramètres de [Général] sont enregistrés dans ``system.properties`` à l'intérieur du conteneur ``fess01`` ; ils sont donc perdus lorsque le conteneur est recréé avec ``docker compose down`` (voir la section sur l'arrêt et le redémarrage dans :doc:`guide-02`).
Incluez ``system.properties`` dans la sauvegarde décrite plus loin.

Suivre les temps de réponse de la recherche et les résultats des explorations
-----------------------------------------------------------------------------

En plus de la supervision externe, consultez régulièrement les trois écrans d'administration suivants.

- [Informations système] > [Journal des tâches] : l'état (OK/Échec) et le résultat des tâches comme « Default Crawler ». Les tâches exécutées chaque minute ou toutes les quelques minutes, comme « Search Engine Monitor » et « Log Notification », n'y sont pas enregistrées
- [Informations système] > [Informations sur l'exploration] : « Statut du robot d'exploration », « Taille de l'index (Web/Fichier) » et « Taille de l'index (Magasin de données) » pour chaque session. Vérifiez qu'ils n'ont pas fortement baissé depuis la fois précédente
- L'onglet [Performances] de [Informations système] > [Journal de recherche] : la médiane, le p95 et le p99 des temps de réponse, ainsi que les termes de recherche aux réponses lentes. Pour l'analyse des journaux de recherche, consultez :doc:`guide-08`

Lire les journaux
=================

Types de fichiers journaux
--------------------------

Fess écrit ses journaux dans un fichier distinct pour chaque type de traitement.
Choisissez le fichier à ouvrir selon ce que vous voulez examiner.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Fichier
     - Contenu
   * - ``fess.log``
     - Journal de Fess lui-même (page de recherche, administration, API, planificateur). Échecs de démarrage, erreurs de connexion à OpenSearch, échecs d'import des sauvegardes, etc.
   * - ``fess-crawler.log``
     - Journal du processus d'exploration. Erreurs de récupération par URL, échecs d'authentification, manque de mémoire du robot d'exploration, etc.
   * - ``audit.log``
     - Journal d'audit des connexions, déconnexions et opérations d'administration
   * - ``fess-suggest.log`` / ``fess-thumbnail.log``
     - Journaux de la génération des suggestions et des vignettes
   * - ``fess-llm.log``
     - Journal du mode de recherche IA (RAG) et de l'intégration LLM
   * - ``searchlog.log``
     - Un enregistrement par recherche (lorsque « Journal de recherche » est activé dans [Général])
   * - ``server_*.log``
     - Journaux de Tomcat

Leur emplacement dépend du mode d'installation.

- Version ZIP : ``logs/`` dans le répertoire où Fess a été décompressé
- Paquets RPM/DEB : ``/var/log/fess/``
- Docker : ``/var/log/fess/`` dans le conteneur. ``fess.log``, ``fess-crawler.log``, ``audit.log`` et d'autres sont aussi envoyés sur la sortie standard et peuvent donc être lus avec ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01``. Ils sont perdus lorsque le conteneur est recréé

Quel que soit le mode d'installation, vous pouvez télécharger un fichier en cliquant sur son nom dans [Informations système] > [Fichier journal].
Les personnes qui ne peuvent pas se connecter au serveur peuvent ainsi consulter les journaux.

Chaque journal est compressé en ``.log.gz`` et renouvelé au changement de date ou lorsqu'il dépasse 100 Mo.
Les fichiers compressés sont supprimés automatiquement au bout de 90 jours pour ``fess.log`` et ``searchlog.log``, et au bout de 360 jours pour ``audit.log``.
En revanche, les fichiers compressés des journaux du robot d'exploration et des processus enfants, comme ``fess-crawler.log``, ``fess-suggest.log`` et ``fess-thumbnail.log``, ne sont pas supprimés automatiquement.
Surveillez l'espace occupé par le répertoire des journaux et supprimez régulièrement les anciens fichiers.

Examiner plus en détail
-----------------------

Par défaut, ``fess.log`` enregistre les messages de niveau WARN et supérieur, et ``fess-crawler.log`` ceux de niveau INFO et supérieur.
Pour rendre ``fess.log`` plus détaillé, élevez « Niveau de journalisation » dans [Système] > [Général] à ``INFO`` ou ``DEBUG``.
Cette modification est annulée au redémarrage de Fess.
Le niveau de journalisation du robot d'exploration est déterminé par le script de la tâche.
Le script de « Default Crawler » contient ``logLevel("info")`` ; si vous le remplacez par ``logLevel("debug")`` dans [Système] > [Planificateur], des journaux détaillés sont écrits dès l'exploration suivante.
Rétablissez la valeur une fois l'analyse terminée.
Pour modifier le niveau de façon permanente, consultez `Configuration des journaux <https://fess.codelibs.org/fr/stable/config/admin-logging.html>`__.

Pour demander de l'aide sur un forum ou ailleurs, le bouton [Télécharger les journaux] de la section « Diagnostics » de [Informations système] > [Maintenance] est utile.
Il télécharge un fichier zip regroupant les journaux, ``system.properties``, ``fess_config.properties``, le contenu des index de configuration et l'état d'OpenSearch.
Les valeurs telles que les clés d'API et ``app.cipher.key`` sont remplacées par ``XXXXXXXX``, mais le corps des journaux et le contenu des index de configuration ne sont pas masqués.
Vérifiez le contenu avant de le transmettre à l'extérieur.

Sauvegarder
===========

Où se trouvent les données
--------------------------

Les données de Fess sont réparties en trois endroits.
[Informations système] > [Sauvegarde] ne permet d'obtenir que le premier.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Données
     - Emplacement
     - Méthode de sauvegarde
   * - Configurations d'exploration, planificateur, étiquettes, utilisateurs, paramètres de [Général]
     - Index de configuration d'OpenSearch et ``system.properties``
     - [Informations système] > [Sauvegarde], ou l'API d'administration
   * - Documents explorés, dictionnaires (synonymes, mots vides, etc.)
     - Index ``fess.*`` et index ``configsync`` d'OpenSearch
     - Snapshots OpenSearch (pour les dictionnaires seuls, une copie des fichiers suffit)
   * - ``fess_config.properties`` (y compris ``app.cipher.key``), paramètres de démarrage, plugins installés
     - Fichiers sur le serveur Fess
     - Copie des fichiers, ou gestion de configuration

Les documents explorés peuvent être reconstruits par une nouvelle exploration, à condition que les paramètres aient été restaurés.
Ne prenez des snapshots que si une nouvelle exploration prendrait trop de temps.

Fichiers disponibles dans [Sauvegarde]
--------------------------------------

[Informations système] > [Sauvegarde] affiche les fichiers suivants.
Cliquez sur un nom pour télécharger le fichier correspondant.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Fichier
     - Contenu
   * - ``fess_basic_config.bulk``
     - Paramètres tels que les configurations d'exploration, le planificateur, les étiquettes, les correspondances de mots-clés et l'authentification web/fichier
   * - ``fess_config.bulk``
     - Tout ce qui précède, plus les informations d'exploration, les URL en échec, les journaux des tâches, les étiquettes utilisateur, etc.
   * - ``fess_user.bulk``
     - Utilisateurs, rôles et groupes
   * - ``system.properties``
     - Les paramètres de [Système] > [Général]
   * - ``fess.json`` / ``doc.json``
     - Paramètres et mapping de l'index des documents
   * - ``*.ndjson``
     - Journaux de recherche, journaux de clics, favoris, journaux du chat IA et utilisateurs de recherche. Ils peuvent être téléchargés, mais pas téléversés pour être restaurés

Les fichiers servant à restaurer les paramètres sont ``fess_basic_config.bulk``, ``fess_user.bulk`` et ``system.properties``.
Si vous utilisez des étiquettes utilisateur, récupérez aussi ``fess_config.bulk``.

À l'exception des informations d'authentification décrites plus loin, les fichiers ``*.bulk`` contiennent les valeurs des paramètres en clair.
Conservez-les comme des fichiers confidentiels.

Sauvegarde quotidienne avec cron
--------------------------------

L'API d'administration ``GET /api/admin/backup/file/<nom-de-fichier>/`` renvoie les mêmes fichiers que l'écran.
Créez un jeton en suivant la même procédure que dans « Surveillance des ressources » ci-dessus, et enregistrez-le dans un fichier lisible uniquement par l'utilisateur qui exécute le script.

::

    $ sudo mkdir -p /etc/fess-backup
    $ sudo sh -c 'umask 077; echo "<jeton>" > /etc/fess-backup/token'

Le script suivant enregistre les fichiers dans un répertoire par date et supprime les répertoires de plus de 30 jours (la durée de conservation est un exemple).

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    FESS_URL=http://localhost:8080
    FESS_TOKEN=$(cat /etc/fess-backup/token)
    BASE_DIR=/var/backups/fess
    BACKUP_DIR="${BASE_DIR}/$(date +%Y%m%d)"

    umask 077
    mkdir -p "${BACKUP_DIR}"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      curl -fsS -H "Authorization: Bearer ${FESS_TOKEN}" \
        -o "${BACKUP_DIR}/${id}" "${FESS_URL}/api/admin/backup/file/${id}/"
      test -s "${BACKUP_DIR}/${id}"
    done

    # Environnement Docker : copier aussi les fichiers de dictionnaire
    docker cp search01:/usr/share/opensearch/config/dictionary/. "${BACKUP_DIR}/dictionary"

    find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

Points importants :

- Le ``/`` final de l'URL ne peut pas être omis. Comme les noms de fichiers contiennent un point, une requête sans ``/`` est traitée comme une demande de fichier statique et renvoie 404
- Sans ``-f``, ``curl`` enregistre aussi les réponses 404 et autres erreurs dans le fichier, et le script semble avoir réussi. ``-f`` combiné à ``set -e`` interrompt le script en cas d'échec
- Pour la version ZIP et les paquets RPM/DEB, remplacez la ligne ``docker cp`` par une copie du répertoire des dictionnaires côté OpenSearch (l'emplacement désigné par ``FESS_DICTIONARY_PATH`` de Fess)

Enregistrez le script sous ``/usr/local/bin/fess-backup.sh``, rendez-le exécutable et ajoutez-le à la crontab de root (dans cet exemple, exécution quotidienne à 2 h 30).

::

    30 2 * * * /usr/local/bin/fess-backup.sh

Après l'avoir ajouté, exécutez-le une fois manuellement.
Ouvrez ``fess_basic_config.bulk`` et vérifiez que les lignes commençant par ``{"index":{"_index":`` alternent avec des lignes JSON contenant les paramètres.
Le même traitement peut aussi s'écrire avec ``fessctl`` (voir :doc:`guide-16`).

Conserver app.cipher.key
------------------------

Fess 15.9 chiffre, avec ``app.cipher.key`` de ``fess_config.properties``, les mots de passe de l'authentification web et de l'authentification de fichiers, ainsi que les mots de passe et secrets enregistrés dans les paramètres des configurations d'exploration et de magasin de données.
Ils restent chiffrés dans les fichiers ``*.bulk``.
Pour restaurer sur un autre serveur, le même ``app.cipher.key`` doit y être configuré.
Avec une clé différente, le déchiffrement est impossible : ``CipherFailureException`` est consigné dans ``fess-crawler.log`` et les explorations qui utilisent ces informations d'authentification échouent.

``fess_config.properties`` se trouve dans ``app/WEB-INF/classes/`` pour la version ZIP et dans ``/etc/fess/`` pour les paquets RPM/DEB.
Si vous avez modifié la valeur, traitez ce fichier comme confidentiel, au même titre que les fichiers ``*.bulk``, et conservez-le dans un autre endroit.
Pour modifier la valeur sous Docker, indiquez ``-Dfess.config.app.cipher.key=<valeur>`` dans ``FESS_JAVA_OPTS`` de ``compose.yaml``.
Ainsi, la même clé est utilisée même après la recréation du conteneur.

.. warning::

   Si vous modifiez ``app.cipher.key`` après avoir enregistré des informations d'authentification, les valeurs enregistrées jusque-là ne peuvent plus être déchiffrées.
   Si vous la modifiez, faites-le avant d'enregistrer les informations d'authentification web, de fichiers ou de magasin de données.
   Dans un environnement déjà en exploitation, ne modifiez pas la valeur et conservez-en une trace.

Snapshots de l'index des documents
----------------------------------

Pour restaurer les documents sans nouvelle exploration, utilisez les snapshots d'OpenSearch.
En plus de ``fess*``, incluez toujours l'index ``configsync``, qui contient les dictionnaires.
Sans ``configsync``, les fichiers de dictionnaire manquent lors d'une restauration dans un nouvel OpenSearch, et l'index des documents ne peut pas être ouvert.

Pour utiliser les snapshots, le chemin du dépôt (``path.repo``) doit être configuré côté OpenSearch.
Il n'est pas défini dans ``compose-opensearch3.yaml`` de docker-fess ; ajoutez-le si vous utilisez les snapshots.
La procédure d'enregistrement du dépôt, de création et de restauration est décrite dans `Gestion des index <https://fess.codelibs.org/fr/stable/config/admin-index-backup.html>`__.
Effectuez la restauration avec Fess arrêté, et restaurez ``configsync`` en premier.

Restaurer
=========

À savoir avant de restaurer
---------------------------

La restauration depuis [Sauvegarde] ne remplace pas entièrement le contenu d'OpenSearch.

- La restauration se fait uniquement par téléversement. L'API d'administration ne sert qu'au téléchargement ; il n'existe pas d'API de restauration
- Chaque paramètre d'un fichier ``*.bulk`` n'est écrit que si le même paramètre n'existe pas sur le serveur ou s'il est plus récent que celui du serveur. Les paramètres modifiés après la sauvegarde ne reviennent pas à leur ancien contenu
- Les paramètres créés après la sauvegarde ne sont pas supprimés et sont conservés

Elle ne convient donc pas pour « remettre dans l'état d'hier un paramètre modifié par erreur ».
Utilisez-la pour migrer vers un nouveau serveur ou restaurer un environnement reconstruit.

Restaurer les paramètres sur un autre serveur
---------------------------------------------

1. Installez la même version de Fess sur le serveur de destination et donnez à ``app.cipher.key`` dans ``fess_config.properties`` la même valeur que sur le serveur d'origine
2. Installez les plugins utilisés sur le serveur d'origine (magasins de données, SSO, etc.) et redémarrez Fess
3. Connectez-vous à l'administration et ouvrez [Informations système] > [Sauvegarde]
4. Sélectionnez ``fess_basic_config.bulk`` dans « Fichier en vrac » et cliquez sur [Téléverser]. Le message « Démarrage d'un processus en vrac. » s'affiche
5. Téléversez de la même manière ``fess_user.bulk`` et ``system.properties``. Si vous utilisez des étiquettes utilisateur, téléversez aussi ``fess_config.bulk`` (les informations d'exploration et les journaux des tâches du serveur d'origine sont alors également importés)

L'import s'effectue en arrière-plan.
Patientez un peu, puis vérifiez les points suivants.

- Les paramètres du serveur d'origine apparaissent dans [Robot d'exploration] > [Web], [Système de fichiers] et [Magasin de données], ainsi que dans [Système] > [Planificateur]
- Les utilisateurs du serveur d'origine apparaissent dans [Utilisateur] > [Utilisateur]
- Les destinataires des notifications et autres paramètres de [Système] > [Général] ont les valeurs du serveur d'origine

Enfin, restaurez les dictionnaires et reconstruisez les documents.

- Dictionnaires : dans [Système] > [Dictionnaire], ouvrez l'écran de chaque type et téléversez le fichier de dictionnaire sauvegardé. Exécutez ensuite « Recharger l'index des documents » dans [Informations système] > [Maintenance]. Pendant le rechargement, la recherche est brièvement indisponible
- Documents : dans [Système] > [Planificateur], cliquez sur [Démarrer maintenant] pour « Default Crawler » afin de relancer l'exploration. Pour restaurer depuis un snapshot, suivez la procédure décrite plus haut

Une fois l'exploration terminée, vérifiez le nombre de documents indexés dans [Informations système] > [Informations sur l'exploration].
Si une configuration d'exploration avec authentification affiche 0 document, recherchez ``CipherFailureException`` dans ``fess-crawler.log``.
S'il y figure, ``app.cipher.key`` ne correspond pas à celui du serveur d'origine.

Réagir aux incidents
====================

Voici les symptômes courants et les endroits de Fess où les vérifier.

La page de recherche ne s'ouvre pas, ou /api/v2/health renvoie 503
------------------------------------------------------------------

1. Vérifiez l'état d'OpenSearch. Si ``status`` dans ``curl -s "http://localhost:9200/_cluster/health?pretty"`` vaut ``red``, le problème vient d'OpenSearch. Sous Docker, consultez ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs search01``
2. Si OpenSearch est en bon état mais que Fess ne répond pas, recherchez les erreurs de démarrage dans ``fess.log``
3. Si le cluster passe à ``red`` juste après une restauration depuis un snapshot, ``configsync`` n'a peut-être pas été restauré (voir plus haut)

Les explorations échouent, ou le nombre de documents indexés a baissé
---------------------------------------------------------------------

1. Dans [Informations système] > [Journal des tâches], ouvrez la ligne de la tâche concernée et vérifiez « Résultat »
2. Dans [Informations système] > [Informations sur l'exploration], comparez « Statut du robot d'exploration » et les tailles d'index de la dernière session avec la précédente
3. Dans [Informations système] > [URL d'échec], vérifiez « Type », « Journal » et « Nombre d'erreurs » des URL qui n'ont pas pu être récupérées. Les codes HTTP 404, 403, 410 et 401 y sont aussi enregistrés
4. Les détails se trouvent dans ``fess-crawler.log``. En recherchant le « Nom du thread » indiqué dans le détail de l'URL en échec, vous pouvez suivre les journaux autour de ce moment

Si ``fess-crawler.log`` contient ``OutOfMemoryError``, le tas du processus d'exploration est insuffisant.
Le tas du robot d'exploration est défini par ``jvm.crawler.options`` dans ``fess_config.properties`` (``-Xmx512m`` par défaut) et est distinct de celui de Fess lui-même.
Pour l'ajuster, consultez :doc:`guide-14`.

Les notifications n'arrivent pas
--------------------------------

Pour les e-mails, vérifiez d'abord la réception avec [Envoyer un e-mail de test] dans [Général].
Si seul l'e-mail de fin d'exploration n'arrive pas, vérifiez le serveur SMTP dans ``fess_env_crawler.properties``.
Sous Docker, vérifiez aussi que les paramètres de [Général] n'ont pas été perdus parce que le conteneur a été recréé avec ``down`` et ``up``.
Si seule la notification des journaux n'arrive pas, vérifiez que « Log Notification » est activé, que la tâche « Log Notification » est activée et que « Log Notification Level » est approprié (``WARN`` pour les échecs de tâches).
D'autres points à vérifier figurent dans la section « Dépannage » de `Notification des journaux <https://fess.codelibs.org/fr/stable/config/admin-log-notification.html>`__.

La recherche est lente
----------------------

1. Dans l'onglet [Performances] de [Informations système] > [Journal de recherche], déterminez si ce sont certains termes de recherche qui sont lents ou l'ensemble des recherches
2. Comparez ``jvm.memory.heap.percent`` et la durée cumulée de ``jvm.gc`` dans ``/api/admin/stats`` avec les valeurs d'avant le ralentissement

Pour aller plus loin
====================

- Gérer les paramètres avec des scripts ou ``fessctl`` : :doc:`guide-16`
- Ajuster le tas, ou répartir OpenSearch et Fess sur plusieurs serveurs : :doc:`guide-14`
- Renforcer la protection des accès avec le SSO, les journaux d'audit, etc. : :doc:`guide-15`
- Améliorer la qualité de la recherche à partir des journaux de recherche : :doc:`guide-08`

Références
==========

- `Health API <https://fess.codelibs.org/fr/stable/api/api-health.html>`__
- `API Stats <https://fess.codelibs.org/fr/stable/api/admin/api-admin-stats.html>`__
- `Notification des journaux <https://fess.codelibs.org/fr/stable/config/admin-log-notification.html>`__
- `Configuration des journaux <https://fess.codelibs.org/fr/stable/config/admin-logging.html>`__
- `Fichiers journaux <https://fess.codelibs.org/fr/stable/admin/log-guide.html>`__
- `Sauvegarde <https://fess.codelibs.org/fr/stable/admin/backup-guide.html>`__
- `API Backup <https://fess.codelibs.org/fr/stable/api/admin/api-admin-backup.html>`__
- `Gestion des index <https://fess.codelibs.org/fr/stable/config/admin-index-backup.html>`__
- `URL en échec <https://fess.codelibs.org/fr/stable/admin/failureurl-guide.html>`__
- `Maintenance <https://fess.codelibs.org/fr/stable/admin/maintenance-guide.html>`__
