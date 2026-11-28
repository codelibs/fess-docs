===================================================
Fess Settings as Code for Reproducible Environments
===================================================

Introduction
============

Settings built up through the admin console leave no record of who changed what, or when.
And when you take settings you validated in a staging environment to production, you end up repeating the same screen operations by hand.

In this article, we write the settings of Fess 15.9 as files in a Git repository, apply them with a script to a freshly started Docker environment, and confirm that they were applied.
We use the docker-fess Compose files, the Fess Admin API, and fessctl, its command-line client.

The scope of backups and the restore procedure are not covered here.
See :doc:`guide-10` for those.

Choosing How to Manage Each Kind of Setting
===========================================

Fess settings are not kept in a single place.
How you turn them into code depends on where they are stored.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Setting
     - Where it is stored
     - How to turn it into code
   * - Fess version, plugins
     - Docker image, container
     - Image tag in the Compose file and ``FESS_PLUGINS``
   * - Items in ``fess_config.properties`` (such as ``app.cipher.key``)
     - A file inside the container
     - ``-Dfess.config.<key>`` in ``FESS_JAVA_OPTS``
   * - Items on [System] > [General]
     - ``system.properties`` inside the container
     - ``-Dfess.system.<key>`` in ``FESS_JAVA_OPTS``
   * - Crawl configurations, labels, scheduler jobs, users, etc.
     - Configuration indices in OpenSearch
     - Admin API (fessctl)
   * - Dictionaries (synonyms, etc.)
     - ``FESS_DICTIONARY_PATH`` in the OpenSearch container
     - Dictionary upload through the Admin API (fessctl)
   * - Access tokens, the value of the encryption key
     - Tokens in OpenSearch, the encryption key in startup options
     - Keep them out of Git, in ``.env`` or CI secrets

The ``fess01`` container in docker-fess has no volume, so ``system.properties`` disappears together with the container on ``docker compose down``.
Crawl configurations and other settings stored in OpenSearch remain on its volume.

Repository Layout
=================

In this article, we manage the following files in Git.

::

    fess-infra/
    ├── compose.yaml               file from docker-fess v15.9.0
    ├── compose-opensearch3.yaml   file from docker-fess v15.9.0
    ├── compose-site.yaml          differences for your own environment
    ├── dict/
    │   └── synonym.txt            synonym dictionary
    ├── apply.sh                   script that applies the settings
    ├── .gitignore
    └── .env                       not committed to Git (encryption key and token)

Pinning the Docker Setup to a Version
=====================================

Getting the Compose Files
-------------------------

Get the files from the ``v15.9.0`` tag of docker-fess.
``compose.yaml`` points to the image ``ghcr.io/codelibs/fess:15.9.0`` and ``compose-opensearch3.yaml`` to ``ghcr.io/codelibs/fess-opensearch:3.9.0``, so the versions are pinned.

::

    $ mkdir fess-infra && cd fess-infra
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

Do not edit these two files; write the differences for your environment in a separate file.
When you upgrade docker-fess, all you need to do is get the files again.

Writing the Differences for Your Environment
--------------------------------------------

Create ``compose-site.yaml``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-ds-git:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.app.cipher.key=${FESS_CIPHER_KEY:?FESS_CIPHER_KEY is not set} -Dfess.system.purge.searchlog.day=180"

- ``FESS_PLUGINS`` lists the plugins to download at startup, separated by spaces, in the form ``name:version``. Use the same 15.9.x version as Fess. The ``fess-ds-git`` plugin in the example is used to crawl Git repositories with a data store. The download source is fixed to ``maven.codelibs.org``, so you can only list published plugins here, and the container must be able to reach the internet
- ``-Dfess.config.<key>`` takes precedence over the item of the same name in ``fess_config.properties``
- ``-Dfess.system.<key>`` becomes the default value of an item on [General]. ``purge.searchlog.day`` in the example is the number of days for "Delete old search logs" on [General]

Compose merges ``environment`` by variable name, so ``SEARCH_ENGINE_HTTP_URL`` and the other variables in ``compose.yaml`` are kept as they are.
However, if you set the same variable in more than one file, the value from the later file replaces it.
Overlays such as ``compose-openai.yaml`` also set ``FESS_PLUGINS`` and ``FESS_JAVA_OPTS``, so if you combine them, merge the values into a single file.

.. note::

   ``-Dfess.system.<key>`` is used only when ``system.properties`` does not contain that key.
   Once you save [General] in the admin console, or run ``fessctl general update``, every item on that screen is written to ``system.properties``, and from then on those values take precedence.
   In that state, changing the value in ``compose-site.yaml`` has no effect until you ``down`` the stack and recreate the container.

Choosing the Encryption Key
---------------------------

``app.cipher.key`` is the key that encrypts the passwords of web authentication and file authentication, as well as secret values stored in the parameters of crawl configurations and data store configurations.
Do not keep the default value ``___change__me___``; decide on a key before the first startup.

The key string is used as-is as an AES key, so it must be 16, 24 or 32 bytes long.
The output of ``openssl rand -hex 16`` (32 hexadecimal characters) is 32 bytes.

::

    $ printf 'FESS_CIPHER_KEY=%s\n' "$(openssl rand -hex 16)" > .env
    $ printf '.env\nbackup/\n' > .gitignore

If you change the key after credentials have been saved, the stored values can no longer be decrypted, and crawls that use those settings fail.
You also need the same key when you restore a backup into another environment (:doc:`guide-10`).
Keep a copy somewhere other than ``.env`` as well, such as a password manager.

The value of ``FESS_JAVA_OPTS`` is visible through ``docker inspect``.
If you want to avoid that, mount ``fess_config.properties`` under ``/opt/fess`` instead (see "How to Apply Configuration Files" in `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__).

Starting the Stack
------------------

Specify all three files every time you run a Compose command.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-site.yaml up -d

The health check of ``fess01`` calls ``/api/v2/health``; once ``docker compose ... ps`` shows ``fess01`` as ``(healthy)``, it is ready.

Creating an Access Token for the Admin API
==========================================

Calling the Admin API requires an access token, and the API that creates tokens cannot be called without one either.
So for each new environment, create the first token once in the admin console.

1. Log in to ``http://localhost:8080/admin/`` as ``admin`` / ``admin`` and set the new password you are asked for (at least 8 characters)
2. Open [System] > [Access Token] and click [Create New]
3. Enter ``fess-infra`` in "Name" and ``{role}admin-api`` in "Permissions", then click [Create]
4. Open the token you created from the list and copy the value of "Token"

Append the copied value to ``.env``.

::

    $ echo 'FESS_ACCESS_TOKEN=<copied value>' >> .env

A token with ``{role}admin-api`` can perform every operation of the Admin API.
That includes changing settings, creating users and downloading backups, and you cannot create a token limited to a narrower purpose.
Treat it like the administrator password, and never put it in Git or in JavaScript that runs in a browser.

Preparing fessctl
=================

fessctl is a command-line tool that calls the Admin API.
Install version 0.4.0, which has defaults for Fess 15.9, with the version pinned.
It requires Python 3.13 or later.

::

    $ pipx install fessctl==0.4.0

``uv tool install fessctl==0.4.0`` works too.
The scripts below also use ``jq`` and ``curl`` to extract values from responses.

fessctl reads the endpoint from ``FESS_ENDPOINT`` (default ``http://localhost:8080``), the token from ``FESS_ACCESS_TOKEN``, and the version of the Fess it connects to from ``FESS_VERSION``.
Set ``FESS_VERSION`` to ``15.9.0``.
This is because the way the API is called differs between versions.

Check the connection.

::

    $ set -a; . ./.env; set +a
    $ export FESS_VERSION=15.9.0
    $ fessctl ping
    $ fessctl webconfig list

``ping`` exits with code 0 if the cluster status is GREEN or YELLOW.
The health check passes even without a token, so use ``webconfig list`` to confirm that the token is valid.
If you get an authentication error, check the token value and its permissions.
With ``-o json``, every command prints the Admin API response as it is, so you can extract values with ``jq``.

Putting the Initial Dictionary into Git
---------------------------------------

Uploading a dictionary replaces the whole file.
To avoid losing the default contents, first download the current synonym dictionary into the repository and edit that.

::

    $ mkdir -p dict
    $ SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    $ fessctl dict synonym download "$SYNONYM_ID" --file dict/synonym.txt

The downloaded file already contains the default synonym line ``fess,フエス``.
Append one synonym line to the end of the file.
Words separated by commas become interchangeable: searching for any one of them also finds documents that contain the others (for the format, see `Synonym Dictionary <https://fess.codelibs.org/stable/admin/synonym-guide.html>`__).

::

    crawler,spider

When you register Japanese words, write hiragana as katakana, small katakana as full-size katakana ("フェス" becomes "フエス"), and full-width alphanumeric characters as half-width ones.

The Script That Applies the Settings
====================================

In ``apply.sh``, write the settings you want in the environment as fessctl commands.
It is meant to be run against a new environment, but it skips creation when a setting with the same name exists, so running it again does not create duplicates.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_ENDPOINT="${FESS_ENDPOINT:-http://localhost:8080}"
    export FESS_VERSION=15.9.0

    until curl -fsS "$FESS_ENDPOINT/api/v2/health" > /dev/null; do sleep 10; done
    fessctl ping

    # Label: attached at crawl time to documents that match the target path
    if ! fessctl labeltype list -o json | jq -e '.response.settings[] | select(.value == "fess_docs")' > /dev/null; then
      fessctl labeltype create --name "Fess documentation" --value fess_docs --version-no 1 \
        --included-path 'https://fess\.codelibs\.org/stable/.*' \
        --permission '{role}guest'
    fi

    # Web crawl configuration
    if ! fessctl webconfig list -o json | jq -e '.response.settings[] | select(.name == "Fess search guide")' > /dev/null; then
      fessctl webconfig create --name "Fess search guide" \
        --url https://fess.codelibs.org/stable/user/index.html \
        --included-url 'https://fess\.codelibs\.org/stable/user/.*' \
        --depth 2 --max-access-count 50 \
        --permission '{role}guest'
    fi

    # Synonym dictionary: replace the whole file, then reopen the document index so it is loaded
    SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    fessctl dict synonym upload "$SYNONYM_ID" dict/synonym.txt --yes
    curl -fsS -X POST "localhost:9200/_configsync/flush" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_close" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_open" > /dev/null

    # Start the crawl and wait for the job to finish
    SCHEDULER_ID=$(fessctl scheduler list -o json | jq -er '.response.settings[] | select(.name == "Default Crawler") | .id')
    JOBLOG_ID=$(fessctl scheduler start "$SCHEDULER_ID" -o json | jq -er '.response.job_log_id')
    until fessctl joblog get "$JOBLOG_ID" -o json \
        | jq -e '.response.log.job_status == "ok" or .response.log.job_status == "fail"' > /dev/null; do
      sleep 30
    done
    fessctl joblog get "$JOBLOG_ID" -o json | jq -e '.response.log.job_status == "ok"'

The key points of the script are as follows.

- With its default text output, fessctl exits with a non-zero code when the API returns an error, so ``set -e`` stops the script there. With ``-o json``, many commands print the error response and exit with 0, so the extracted value is checked with ``jq -e``. If the value is missing, jq fails and the script stops there
- ``--version-no`` of ``labeltype create`` is required in fessctl 0.4.0. Specify ``1`` when creating a new label
- Items omitted from ``webconfig create`` take fessctl's defaults. ``--depth`` defaults to ``1`` and ``--max-access-count`` to ``1000000``, so write the values you intend instead of omitting them. ``--permission`` defaults to ``{role}guest``
- A label value can contain only alphanumeric characters and ``_``. Labels are attached at crawl time, so create them before the crawl configuration
- Without ``--yes``, the dictionary upload stops and asks for confirmation
- The synonym dictionary takes effect at search time, but OpenSearch builds analyzers only when an index is opened. That is why ``_configsync/flush`` first writes the dictionary out to a file, and then ``fess.update`` is closed and opened. Searches are not possible during this time, so on an environment in operation, run it at a time with little traffic. It is the same operation as "Reload Document Index" on [System Info] > [Maintenance] in the admin console
- The ``job_log_id`` in the ``scheduler start`` response is the ID shown in [Job Log]. The script waits until the job status becomes ``ok`` or ``fail``, and exits as a failure if it is not ``ok``. "Default Crawler" runs all enabled crawl configurations

When you change the value of an existing setting, this script only skips creation and does not overwrite the value.
Either update it by ID, as in ``fessctl webconfig update <ID> --max-access-count 100``, or run the script again against an environment rebuilt together with its volumes.

When you run the script from CI, do not place ``.env``; pass ``FESS_ACCESS_TOKEN`` and ``FESS_ENDPOINT`` as environment variables from the CI secrets.
In that case, rewrite the three ``localhost:9200`` lines to an address that reaches OpenSearch.

Confirming That the Settings Were Applied
=========================================

Once ``apply.sh`` exits with code 0, check the following in order.

1. The plugin is installed

   ::

       $ fessctl plugin installed

   If ``fess-ds-git`` 15.9.0 is in the list, it has been installed.
   Even if a plugin in ``FESS_PLUGINS`` fails to download, Fess still starts and ``Failed to download`` only appears in ``docker compose ... logs fess01``, so check it here.

2. The value on [General] has been applied

   ::

       $ fessctl general get -o json | jq '.response.setting.purge_search_log_day'

   If it returns ``180``, ``-Dfess.system.purge.searchlog.day`` is in effect.
   In the Admin API, the names are snake_case like ``purge_search_log_day``, which differ from the keys that follow ``-Dfess.system.``.

3. The dictionary has been replaced

   ::

       $ fessctl dict synonym download "$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')" | grep 'spider'

   If the line you added is shown, the upload succeeded.
   You can also check with ``fessctl dict synonym list``, but it shows 100 entries per page by default, so a line added at the end may not appear on the first page.

4. You can search with the label

   ::

       $ curl -fsS --get --data-urlencode 'q=search' --data-urlencode 'fields.label=fess_docs' \
           http://localhost:8080/api/v2/search | jq '.response.record_count'

   If it returns 1 or more, everything from crawling through labeling to searching is connected.
   If it returns 0, check [System Info] > [Failure URL] and the result in [Job Log] in the admin console.

Calling the Admin API Directly
==============================

What fessctl calls is the Admin API under ``/api/admin/``.
Every resource that holds settings, such as crawl configurations, has the following shape (``<resource>`` is ``webconfig``, ``fileconfig``, ``dataconfig``, ``labeltype``, ``keymatch``, and so on).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Request
     - Operation
   * - ``GET /api/admin/<resource>/settings``
     - List
   * - ``GET /api/admin/<resource>/setting/<ID>``
     - Get one
   * - ``POST /api/admin/<resource>/setting``
     - Create
   * - ``PUT /api/admin/<resource>/setting``
     - Update
   * - ``DELETE /api/admin/<resource>/setting/<ID>``
     - Delete

fessctl has subcommands with the same names (``create``, ``list``, ``get``, ``update``, ``delete``), and you can check the items with ``fessctl fileconfig create --help`` and the like.
A dictionary upload is sent as multipart to ``POST /api/admin/dict/<type>/upload/<dictionary ID>``.
The name of the file field differs by type; for synonyms it is ``synonymFile``.
JSON field names are snake_case like ``max_access_count``.
For each field, see the per-resource pages reachable from `Admin API Overview <https://fess.codelibs.org/stable/api/admin/api-admin-overview.html>`__.

The following command returns the number of web crawl configurations.

::

    $ curl -fsS -H "Authorization: Bearer $FESS_ACCESS_TOKEN" \
        http://localhost:8080/api/admin/webconfig/settings | jq '.response.total'

Without ``-f``, curl treats even a 404 or 401 response as success, and the script does not notice the failure.

Downloading a Copy of the Settings
==================================

To cover settings that are not written in Git (such as those changed directly in the admin console), also download backups regularly.
The files involved and the restore procedure are described in :doc:`guide-10`.
Here we only show an example script that runs with the same preparation as ``apply.sh``.

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

``fessctl backup download`` calls ``/api/admin/backup/file/<ID>/`` with the trailing ``/`` that is needed when the ID contains a dot.
If you call it with curl, do not forget the trailing ``/`` and ``-f``.
Without the trailing ``/``, the request returns 404.

The Admin API only goes as far as downloading; a restore can only be done from [System Info] > [Backup] in the admin console.
Backups therefore do not give you a procedure for rebuilding another environment, so keep the source of truth for your settings in ``apply.sh``.

What Must Not Go into Git
=========================

- ``.env`` (the encryption key and the access token)
- Backup files. ``*.bulk`` files also contain values that are not encrypted and must be handled as confidential files. ``system.properties`` also contains values entered on [General], such as storage secret keys and SSO client secrets

This is why ``.env`` and ``backup/`` were added to ``.gitignore``.
Store backups in a place with restricted access, such as encrypted storage.

What to Read Next
=================

- To set up backup targets, restore and monitoring: :doc:`guide-10`
- To review the basics of starting and stopping with Docker: :doc:`guide-02`
- To call the search API from business systems: :doc:`guide-11`
- To protect the admin console, including access token handling and SSO: :doc:`guide-15`
- To build your own plugin: :doc:`guide-17`

References
==========

- `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__
- `Admin API Overview <https://fess.codelibs.org/stable/api/admin/api-admin-overview.html>`__
- `Dict API <https://fess.codelibs.org/stable/api/admin/api-admin-dict.html>`__
- `Backup API <https://fess.codelibs.org/stable/api/admin/api-admin-backup.html>`__
- `Dictionary (when changes take effect) <https://fess.codelibs.org/stable/admin/dict-guide.html>`__
- `Access Token <https://fess.codelibs.org/stable/admin/accesstoken-guide.html>`__
- `fessctl (GitHub) <https://github.com/codelibs/fessctl>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
