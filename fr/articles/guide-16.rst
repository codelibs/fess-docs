===============================================
Gérer Fess en code et recréer son environnement
===============================================

Introduction
============

Pour des paramètres accumulés via la console d'administration, il est impossible de retrouver après coup qui a modifié quoi, et quand.
Et lorsque vous reportez en production des paramètres validés dans un environnement de test, vous répétez à la main les mêmes manipulations à l'écran.

Dans cet article, nous écrivons les paramètres de Fess 15.9 sous forme de fichiers dans un dépôt Git, nous les appliquons par script à un environnement Docker fraîchement démarré, puis nous vérifions qu'ils ont bien été appliqués.
Nous utilisons pour cela les fichiers Compose de docker-fess, l'API d'administration de Fess (Admin API) et fessctl, son client en ligne de commande.

Le périmètre des sauvegardes et la procédure de restauration ne sont pas traités ici.
Reportez-vous à :doc:`guide-10`.

Choisir la méthode de gestion selon l'emplacement des paramètres
================================================================

Les paramètres de Fess ne sont pas regroupés en un seul endroit.
La façon de les transformer en code dépend de l'endroit où ils sont stockés.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Paramètre
     - Emplacement de stockage
     - Transformation en code
   * - Version de Fess, plugins
     - Image Docker, conteneur
     - Tag d'image dans le fichier Compose et ``FESS_PLUGINS``
   * - Éléments de ``fess_config.properties`` (comme ``app.cipher.key``)
     - Fichier dans le conteneur
     - ``-Dfess.config.<clé>`` dans ``FESS_JAVA_OPTS``
   * - Éléments de [Système] > [Général]
     - ``system.properties`` dans le conteneur
     - ``-Dfess.system.<clé>`` dans ``FESS_JAVA_OPTS``
   * - Configurations d'exploration, étiquettes, planificateur, utilisateurs, etc.
     - Index de configuration dans OpenSearch
     - Admin API (fessctl)
   * - Dictionnaires (synonymes, etc.)
     - ``FESS_DICTIONARY_PATH`` du conteneur OpenSearch
     - Téléversement de dictionnaire via l'Admin API (fessctl)
   * - Jetons d'accès, valeur de la clé de chiffrement
     - Jetons dans OpenSearch, clé de chiffrement dans les options de démarrage
     - Hors de Git, dans ``.env`` ou dans les secrets de la CI

Le conteneur ``fess01`` de docker-fess n'a pas de volume : ``system.properties`` disparaît donc avec le conteneur lors d'un ``docker compose down``.
Les paramètres stockés dans OpenSearch, comme les configurations d'exploration, restent dans son volume.

Organisation du dépôt
=====================

Dans cet article, nous gérons les fichiers suivants avec Git.

::

    fess-infra/
    ├── compose.yaml               fichier de docker-fess v15.9.0
    ├── compose-opensearch3.yaml   fichier de docker-fess v15.9.0
    ├── compose-site.yaml          différences propres à votre environnement
    ├── dict/
    │   └── synonym.txt            dictionnaire de synonymes
    ├── apply.sh                   script qui applique les paramètres
    ├── .gitignore
    └── .env                       hors de Git (clé de chiffrement et jeton)

Figer la configuration Docker sur une version
=============================================

Récupérer les fichiers Compose
------------------------------

Récupérez les fichiers du tag ``v15.9.0`` de docker-fess.
``compose.yaml`` désigne l'image ``ghcr.io/codelibs/fess:15.9.0`` et ``compose-opensearch3.yaml`` l'image ``ghcr.io/codelibs/fess-opensearch:3.9.0`` : les versions sont ainsi figées.

::

    $ mkdir fess-infra && cd fess-infra
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

Ne modifiez pas ces deux fichiers ; écrivez les différences propres à votre environnement dans un fichier séparé.
Lors d'une montée de version de docker-fess, il suffit alors de récupérer à nouveau les fichiers.

Écrire les différences propres à votre environnement
----------------------------------------------------

Créez ``compose-site.yaml``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-ds-git:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.app.cipher.key=${FESS_CIPHER_KEY:?FESS_CIPHER_KEY is not set} -Dfess.system.purge.searchlog.day=180"

- ``FESS_PLUGINS`` liste, séparés par des espaces, les plugins à télécharger au démarrage, au format ``nom:version``. Utilisez la même version 15.9.x que Fess. Le plugin ``fess-ds-git`` de l'exemple sert à explorer des dépôts Git avec un magasin de données. La source de téléchargement est fixée à ``maven.codelibs.org`` : vous ne pouvez donc indiquer ici que des plugins publiés, et le conteneur doit pouvoir accéder à Internet
- ``-Dfess.config.<clé>`` est prioritaire sur l'élément du même nom dans ``fess_config.properties``
- ``-Dfess.system.<clé>`` devient la valeur par défaut d'un élément de [Général]. ``purge.searchlog.day`` dans l'exemple est le nombre de jours de « Supprimer les anciens journaux de recherche » dans [Général]

Compose fusionne ``environment`` par nom de variable : ``SEARCH_ENGINE_HTTP_URL`` et les autres variables de ``compose.yaml`` sont donc conservées telles quelles.
En revanche, si vous définissez la même variable dans plusieurs fichiers, la valeur du dernier fichier la remplace.
Les surcouches comme ``compose-openai.yaml`` définissent elles aussi ``FESS_PLUGINS`` et ``FESS_JAVA_OPTS`` ; si vous les combinez, regroupez les valeurs dans un seul fichier.

.. note::

   ``-Dfess.system.<clé>`` n'est utilisé que lorsque ``system.properties`` ne contient pas cette clé.
   Dès que vous enregistrez une fois [Général] dans la console d'administration ou que vous exécutez ``fessctl general update``, tous les éléments de l'écran sont écrits dans ``system.properties``, et ce sont ensuite ces valeurs qui priment.
   Dans cet état, modifier la valeur dans ``compose-site.yaml`` n'a aucun effet tant que vous n'avez pas recréé le conteneur avec ``down``.

Choisir la clé de chiffrement
-----------------------------

``app.cipher.key`` est la clé qui chiffre les mots de passe de l'authentification web et de l'authentification de fichiers, ainsi que les valeurs secrètes enregistrées dans les paramètres des configurations d'exploration et de magasin de données.
N'utilisez pas la valeur par défaut ``___change__me___`` : choisissez la clé avant le premier démarrage.

La chaîne de la clé est utilisée telle quelle comme clé AES ; elle doit donc faire 16, 24 ou 32 octets.
La sortie de ``openssl rand -hex 16`` (32 caractères hexadécimaux) fait 32 octets.

::

    $ printf 'FESS_CIPHER_KEY=%s\n' "$(openssl rand -hex 16)" > .env
    $ printf '.env\nbackup/\n' > .gitignore

Si vous changez la clé après avoir enregistré des informations d'authentification, les valeurs enregistrées ne peuvent plus être déchiffrées et les explorations qui utilisent ces paramètres échouent.
La même clé est également nécessaire pour restaurer une sauvegarde dans un autre environnement (:doc:`guide-10`).
Conservez-en une copie ailleurs que dans ``.env``, par exemple dans un gestionnaire de mots de passe.

La valeur de ``FESS_JAVA_OPTS`` est visible avec ``docker inspect``.
Pour l'éviter, montez plutôt ``fess_config.properties`` dans ``/opt/fess`` (voir « Comment appliquer les fichiers de configuration » dans `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__).

Démarrer
--------

Indiquez les trois fichiers à chaque commande Compose.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-site.yaml up -d

Le contrôle de santé de ``fess01`` appelle ``/api/v2/health`` ; lorsque ``docker compose ... ps`` affiche ``fess01`` en ``(healthy)``, tout est prêt.

Créer un jeton d'accès pour l'Admin API
=======================================

Les appels à l'Admin API nécessitent un jeton d'accès, et l'API qui crée les jetons ne peut pas non plus être appelée sans jeton.
Pour chaque nouvel environnement, vous créez donc le premier jeton une seule fois dans la console d'administration.

1. Connectez-vous à ``http://localhost:8080/admin/`` avec ``admin`` / ``admin`` et définissez le nouveau mot de passe demandé (8 caractères minimum)
2. Ouvrez [Système] > [Jeton d'accès] et cliquez sur [Créer nouveau]
3. Saisissez ``fess-infra`` dans « Nom » et ``{role}admin-api`` dans « Autorisations », puis cliquez sur [Créer]
4. Ouvrez le jeton créé depuis la liste et copiez la valeur de « Jeton »

Ajoutez la valeur copiée à ``.env``.

::

    $ echo 'FESS_ACCESS_TOKEN=<valeur copiée>' >> .env

Un jeton disposant de ``{role}admin-api`` peut effectuer toutes les opérations de l'Admin API.
Cela inclut la modification des paramètres, la création d'utilisateurs et même le téléchargement des sauvegardes, et il n'est pas possible de créer un jeton limité à un usage particulier.
Traitez-le comme le mot de passe administrateur et ne le placez jamais dans Git ni dans du JavaScript exécuté dans le navigateur.

Préparer fessctl
================

fessctl est un outil en ligne de commande qui appelle l'Admin API.
Installez la version 0.4.0, dont les valeurs par défaut visent Fess 15.9, en figeant la version.
Python 3.13 ou ultérieur est requis.

::

    $ pipx install fessctl==0.4.0

``uv tool install fessctl==0.4.0`` convient également.
Les scripts qui suivent utilisent aussi ``jq`` et ``curl`` pour extraire des valeurs des réponses.

fessctl lit le point de terminaison dans ``FESS_ENDPOINT`` (valeur par défaut ``http://localhost:8080``), le jeton dans ``FESS_ACCESS_TOKEN`` et la version du Fess auquel il se connecte dans ``FESS_VERSION``.
Indiquez ``15.9.0`` dans ``FESS_VERSION``.
En effet, la manière d'appeler l'API change selon la version.

Vérifiez la connexion.

::

    $ set -a; . ./.env; set +a
    $ export FESS_VERSION=15.9.0
    $ fessctl ping
    $ fessctl webconfig list

``ping`` se termine avec le code 0 si l'état du cluster est GREEN ou YELLOW.
Le contrôle de santé réussit même sans jeton : vérifiez donc la validité du jeton avec ``webconfig list``.
En cas d'erreur d'authentification, vérifiez la valeur du jeton et ses autorisations.
Avec ``-o json``, toutes les commandes affichent la réponse de l'Admin API telle quelle, ce qui permet d'en extraire des valeurs avec ``jq``.

Mettre le contenu initial du dictionnaire dans Git
--------------------------------------------------

Le téléversement d'un dictionnaire remplace le fichier entier.
Pour ne pas perdre le contenu par défaut, téléchargez d'abord le dictionnaire de synonymes actuel, placez-le dans le dépôt, puis modifiez-le.

::

    $ mkdir -p dict
    $ SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    $ fessctl dict synonym download "$SYNONYM_ID" --file dict/synonym.txt

Le fichier téléchargé contient déjà la ligne de synonymes par défaut ``fess,フエス``.
Ajoutez une ligne de synonymes à la fin du fichier.
Les mots séparés par des virgules deviennent interchangeables : une recherche sur l'un d'eux trouve aussi les documents qui contiennent les autres (pour le format, voir `Dictionnaire de synonymes <https://fess.codelibs.org/fr/stable/admin/synonym-guide.html>`__).

::

    paramètres,réglages

Pour enregistrer des mots japonais, écrivez les hiragana en katakana, les petits katakana en katakana de taille normale (« フェス » devient « フエス ») et les caractères alphanumériques pleine chasse en demi-chasse.

Le script qui applique les paramètres
=====================================

Dans ``apply.sh``, écrivez sous forme de commandes fessctl les paramètres que l'environnement doit recevoir.
Il est prévu pour être exécuté sur un nouvel environnement, mais il saute la création lorsqu'un paramètre du même nom existe déjà : l'exécuter une seconde fois ne crée donc pas de doublons.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_ENDPOINT="${FESS_ENDPOINT:-http://localhost:8080}"
    export FESS_VERSION=15.9.0

    until curl -fsS "$FESS_ENDPOINT/api/v2/health" > /dev/null; do sleep 10; done
    fessctl ping

    # Étiquette : attribuée lors de l'exploration aux documents qui correspondent au chemin cible
    if ! fessctl labeltype list -o json | jq -e '.response.settings[] | select(.value == "fess_docs")' > /dev/null; then
      fessctl labeltype create --name "Documentation Fess" --value fess_docs --version-no 1 \
        --included-path 'https://fess\.codelibs\.org/fr/stable/.*' \
        --permission '{role}guest'
    fi

    # Configuration d'exploration web
    if ! fessctl webconfig list -o json | jq -e '.response.settings[] | select(.name == "Guide de recherche Fess")' > /dev/null; then
      fessctl webconfig create --name "Guide de recherche Fess" \
        --url https://fess.codelibs.org/fr/stable/user/index.html \
        --included-url 'https://fess\.codelibs\.org/fr/stable/user/.*' \
        --depth 2 --max-access-count 50 \
        --permission '{role}guest'
    fi

    # Dictionnaire de synonymes : remplacer le fichier entier, puis rouvrir l'index des documents pour le charger
    SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    fessctl dict synonym upload "$SYNONYM_ID" dict/synonym.txt --yes
    curl -fsS -X POST "localhost:9200/_configsync/flush" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_close" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_open" > /dev/null

    # Lancer l'exploration et attendre la fin de la tâche
    SCHEDULER_ID=$(fessctl scheduler list -o json | jq -er '.response.settings[] | select(.name == "Default Crawler") | .id')
    JOBLOG_ID=$(fessctl scheduler start "$SCHEDULER_ID" -o json | jq -er '.response.job_log_id')
    until fessctl joblog get "$JOBLOG_ID" -o json \
        | jq -e '.response.log.job_status == "ok" or .response.log.job_status == "fail"' > /dev/null; do
      sleep 30
    done
    fessctl joblog get "$JOBLOG_ID" -o json | jq -e '.response.log.job_status == "ok"'

Les points clés du script sont les suivants.

- Avec sa sortie texte par défaut, fessctl se termine avec un code différent de 0 lorsque l'API renvoie une erreur, si bien que ``set -e`` arrête le script à cet endroit. Avec ``-o json``, de nombreuses commandes affichent la réponse d'erreur et se terminent avec 0 : la valeur extraite est donc vérifiée avec ``jq -e``. Si la valeur est absente, jq échoue et le script s'arrête là
- ``--version-no`` de ``labeltype create`` est obligatoire dans fessctl 0.4.0. Indiquez ``1`` pour une création
- Les éléments omis dans ``webconfig create`` prennent les valeurs par défaut de fessctl. ``--depth`` vaut ``1`` et ``--max-access-count`` vaut ``1000000`` : écrivez donc explicitement les valeurs voulues. La valeur par défaut de ``--permission`` est ``{role}guest``
- La valeur d'une étiquette ne peut contenir que des caractères alphanumériques et ``_``. Les étiquettes étant attribuées lors de l'exploration, créez-les avant la configuration d'exploration
- Sans ``--yes``, le téléversement du dictionnaire s'arrête pour demander une confirmation
- Le dictionnaire de synonymes agit au moment de la recherche, mais OpenSearch ne construit les analyseurs qu'à l'ouverture d'un index. C'est pourquoi ``_configsync/flush`` écrit d'abord le dictionnaire dans un fichier, puis ``fess.update`` est fermé et rouvert. La recherche est impossible pendant ce temps : sur un environnement en service, exécutez le script à une heure de faible affluence. Il s'agit de la même opération que « Recharger l'index des documents » dans [Informations système] > [Maintenance] de la console d'administration
- Le ``job_log_id`` de la réponse de ``scheduler start`` correspond directement à l'ID affiché dans [Journal des tâches]. Le script attend que l'état de la tâche devienne ``ok`` ou ``fail``, et se termine en échec s'il ne vaut pas ``ok``. « Default Crawler » exécute toutes les configurations d'exploration activées

Pour modifier la valeur d'un paramètre existant, ce script se contente de sauter la création et ne réécrit pas la valeur.
Mettez-le à jour en indiquant son ID, comme ``fessctl webconfig update <ID> --max-access-count 100``, ou réexécutez le script sur un environnement reconstruit avec ses volumes.

Pour exécuter le script depuis une CI, ne placez pas de ``.env`` et transmettez ``FESS_ACCESS_TOKEN`` et ``FESS_ENDPOINT`` comme variables d'environnement issues des secrets de la CI.
Dans ce cas, remplacez la destination des trois lignes ``localhost:9200`` par une adresse qui atteint OpenSearch.

Vérifier que les paramètres ont été appliqués
=============================================

Une fois que ``apply.sh`` s'est terminé avec le code 0, vérifiez les points suivants dans l'ordre.

1. Le plugin est installé

   ::

       $ fessctl plugin installed

   Si ``fess-ds-git`` 15.9.0 figure dans la liste, il est installé.
   Même si le téléchargement d'un plugin de ``FESS_PLUGINS`` échoue, Fess démarre quand même et seul ``Failed to download`` apparaît dans ``docker compose ... logs fess01`` : vérifiez-le donc ici.

2. La valeur de [Général] est prise en compte

   ::

       $ fessctl general get -o json | jq '.response.setting.purge_search_log_day'

   Si ``180`` est renvoyé, ``-Dfess.system.purge.searchlog.day`` est effectif.
   Dans l'Admin API, les noms sont en snake_case comme ``purge_search_log_day`` et diffèrent des clés qui suivent ``-Dfess.system.``.

3. Le dictionnaire a été remplacé

   ::

       $ fessctl dict synonym download "$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')" | grep 'réglages'

   Si la ligne ajoutée s'affiche, le téléversement a réussi.
   Vous pouvez aussi vérifier avec ``fessctl dict synonym list``, mais l'affichage se fait par défaut par pages de 100 entrées : une ligne ajoutée à la fin peut ne pas apparaître sur la première page.

4. La recherche avec l'étiquette fonctionne

   ::

       $ curl -fsS --get --data-urlencode 'q=recherche' --data-urlencode 'fields.label=fess_docs' \
           http://localhost:8080/api/v2/search | jq '.response.record_count'

   Si une valeur supérieure ou égale à 1 est renvoyée, toute la chaîne, de l'exploration à la recherche en passant par l'attribution d'étiquettes, fonctionne.
   Si 0 est renvoyé, consultez [Informations système] > [URL d'échec] et le résultat dans [Journal des tâches] de la console d'administration.

Appeler directement l'Admin API
===============================

fessctl appelle l'Admin API sous ``/api/admin/``.
Toutes les ressources qui contiennent des paramètres, comme les configurations d'exploration, ont la forme suivante (``<resource>`` vaut ``webconfig``, ``fileconfig``, ``dataconfig``, ``labeltype``, ``keymatch``, etc.).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Requête
     - Opération
   * - ``GET /api/admin/<resource>/settings``
     - Liste
   * - ``GET /api/admin/<resource>/setting/<ID>``
     - Obtention d'un élément
   * - ``POST /api/admin/<resource>/setting``
     - Création
   * - ``PUT /api/admin/<resource>/setting``
     - Mise à jour
   * - ``DELETE /api/admin/<resource>/setting/<ID>``
     - Suppression

fessctl dispose de sous-commandes du même nom (``create``, ``list``, ``get``, ``update``, ``delete``), et vous pouvez vérifier les éléments avec par exemple ``fessctl fileconfig create --help``.
Le téléversement d'un dictionnaire s'envoie en multipart à ``POST /api/admin/dict/<type>/upload/<ID du dictionnaire>``.
Le nom du champ de fichier diffère selon le type ; pour les synonymes, c'est ``synonymFile``.
Les noms de champ JSON sont en snake_case, comme ``max_access_count``.
Pour chaque champ, consultez les pages propres à chaque ressource accessibles depuis `Vue d'ensemble de l'API Admin <https://fess.codelibs.org/fr/stable/api/admin/api-admin-overview.html>`__.

La commande suivante renvoie le nombre de configurations d'exploration web.

::

    $ curl -fsS -H "Authorization: Bearer $FESS_ACCESS_TOKEN" \
        http://localhost:8080/api/admin/webconfig/settings | jq '.response.total'

Sans ``-f``, curl considère même une réponse 404 ou 401 comme un succès, et le script ne remarque pas l'échec.

Télécharger une copie des paramètres
====================================

Pour couvrir les paramètres qui ne sont pas écrits dans Git (comme ceux modifiés directement dans la console d'administration), téléchargez aussi régulièrement des sauvegardes.
Les fichiers concernés et la procédure de restauration sont décrits dans :doc:`guide-10`.
Nous ne montrons ici qu'un exemple de script qui fonctionne avec la même préparation que ``apply.sh``.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_VERSION=15.9.0
    dest="backup/$(date +%Y%m%d)"
    umask 077
    mkdir -p "$dest"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      fessctl backup download "$id" --dest "$dest/$id" --force
    done

``fessctl backup download`` appelle ``/api/admin/backup/file/<ID>/`` avec le ``/`` final nécessaire lorsque l'ID contient un point.
Si vous l'appelez avec curl, n'oubliez ni le ``/`` final ni ``-f``.
Sans le ``/`` final, la requête renvoie 404.

L'Admin API ne permet que le téléchargement ; la restauration ne peut se faire que depuis [Informations système] > [Sauvegarde] de la console d'administration.
Les sauvegardes ne constituent donc pas une procédure pour reconstruire un autre environnement : gardez la version de référence des paramètres dans ``apply.sh``.

Ce qui ne doit pas aller dans Git
=================================

- ``.env`` (clé de chiffrement et jeton d'accès)
- Les fichiers de sauvegarde. Les ``*.bulk`` contiennent aussi des valeurs non chiffrées et doivent être traités comme des fichiers confidentiels. ``system.properties`` contient lui aussi des valeurs saisies dans [Général], comme les clés secrètes de stockage ou les secrets client SSO

C'est pour cette raison que ``.env`` et ``backup/`` ont été ajoutés à ``.gitignore``.
Conservez les sauvegardes dans un emplacement à accès restreint, par exemple un stockage chiffré.

Articles à lire ensuite
=======================

- Mettre en place le périmètre des sauvegardes, la restauration et la surveillance : :doc:`guide-10`
- Revoir les bases du démarrage et de l'arrêt avec Docker : :doc:`guide-02`
- Appeler l'API de recherche depuis des systèmes métier : :doc:`guide-11`
- Protéger la console d'administration, y compris la gestion des jetons d'accès et le SSO : :doc:`guide-15`
- Créer vos propres plugins : :doc:`guide-17`

Références
==========

- `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__
- `Vue d'ensemble de l'API Admin <https://fess.codelibs.org/fr/stable/api/admin/api-admin-overview.html>`__
- `API Dict <https://fess.codelibs.org/fr/stable/api/admin/api-admin-dict.html>`__
- `API Backup <https://fess.codelibs.org/fr/stable/api/admin/api-admin-backup.html>`__
- `Dictionnaire (moment de la prise en compte) <https://fess.codelibs.org/fr/stable/admin/dict-guide.html>`__
- `Jeton d'accès <https://fess.codelibs.org/fr/stable/admin/accesstoken-guide.html>`__
- `fessctl (GitHub) <https://github.com/codelibs/fessctl>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
