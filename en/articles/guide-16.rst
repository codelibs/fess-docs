============================================================
Part 16: Search Infrastructure Automation -- Management with CI/CD Pipelines and Infrastructure as Code
============================================================

Introduction
============

When search system configurations are managed manually, reproducing environments becomes difficult and the risk of configuration errors increases.
By adopting modern DevOps practices, let's manage and automate search infrastructure as code.

This article introduces an approach to managing Fess configurations as code and automating deployments.

Target Audience
===============

- Those who want to automate search system operations
- Those who want to apply DevOps/IaC practices to search infrastructure
- Those who have basic knowledge of Docker and CI/CD

Applying Infrastructure as Code
================================

The following items are managed as "code" for Fess environments.

.. list-table:: IaC Management Targets
   :header-rows: 1
   :widths: 25 35 40

   * - Target
     - Management Method
     - Version Control
   * - Docker Configuration
     - compose.yaml
     - Git
   * - Fess Settings
     - Backup Files / Admin API
     - Git
   * - Dictionary Data
     - Export via Admin API
     - Git
   * - OpenSearch Settings
     - Configuration Files
     - Git

Environment Definition with Docker Compose
=============================================

Docker Compose File for Production
-------------------------------------

We extend the basic configuration used in Part 2 to define a configuration suitable for production environments.

.. code-block:: yaml

    services:
      fess:
        image: ghcr.io/codelibs/fess:15.5.1
        environment:
          - SEARCH_ENGINE_HTTP_URL=http://opensearch:9200
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        ports:
          - "8080:8080"
        depends_on:
          opensearch:
            condition: service_healthy
        restart: unless-stopped

      opensearch:
        image: ghcr.io/codelibs/fess-opensearch:3.6.0
        environment:
          - discovery.type=single-node
          - OPENSEARCH_JAVA_OPTS=-Xmx4g -Xms4g
          - DISABLE_INSTALL_DEMO_CONFIG=true
          - DISABLE_SECURITY_PLUGIN=true
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        volumes:
          - opensearch-data:/usr/share/opensearch/data
          - opensearch-dictionary:/usr/share/opensearch/config/dictionary
        healthcheck:
          test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 90s
        restart: unless-stopped

    volumes:
      opensearch-data:
      opensearch-dictionary:

The key points are as follows.

- Health check definition: Start Fess only after OpenSearch is ready
- Volume persistence: Persist data across restarts
- Restart policy: Automatic recovery from failures
- Explicit JVM heap configuration

Automating Configuration with the Admin API
=============================================

By using the Fess Admin API, you can manage configurations programmatically without using the GUI.

Exporting Settings
------------------

Export the current Fess settings and save them as code.

You can export from the admin console under [System Info] > [Backup].
It is also possible to export via scripts using the Admin API.

Importing Settings
------------------

Apply settings to a new Fess environment using saved configuration files.
This makes it easy to rebuild or replicate environments.

Using the fessctl CLI
======================

fessctl is a command-line tool for Fess.
Many operations that can be performed in the admin console can also be executed from the command line.

Main Operations
----------------

- Create, update, and delete crawl settings (web, file system, data store)
- Execute scheduler jobs
- Manage users, roles, and groups
- Manage search settings such as key match, labels, and boosts

By using the CLI, you can script configuration changes and integrate them into CI/CD pipelines.

Building CI/CD Pipelines
==========================

Configuration Change Workflow
------------------------------

Manage search system configuration changes with the following workflow.

1. **Change**: Modify configuration files and manage them in a Git branch
2. **Review**: Review changes through pull requests
3. **Test**: Verify behavior in a staging environment
4. **Deploy**: Apply settings to the production environment

GitHub Actions Automation Example
-----------------------------------

This is an example of automatically applying changes to the production environment when configuration file changes are merged.

.. code-block:: yaml

    name: Deploy Fess Config
    on:
      push:
        branches: [main]
        paths:
          - 'fess-config/**'
          - 'dictionary/**'

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Apply dictionary updates
            run: |
              # Transfer dictionary files to the Fess server
              scp dictionary/* fess-server:/opt/fess/dictionary/

          - name: Verify Fess health
            run: |
              # Check Fess operational status using the health API
              curl -s https://fess.example.com/api/v1/health

Automating Backups
===================

Let's also automate regular backups.

Backup Script
--------------

Use cron or CI/CD scheduling features to take regular backups.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    BACKUP_DIR="/backup/fess/$(date +%Y%m%d)"
    mkdir -p "${BACKUP_DIR}"

    # Retrieve the list of Fess backup files
    curl -s -o "${BACKUP_DIR}/fess-backup-files.json" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/files"

    # Download configuration data (e.g., fess_config.bulk)
    curl -s -o "${BACKUP_DIR}/fess_config.bulk" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/file/fess_config.bulk"

    # Delete old backups (older than 30 days)
    find /backup/fess -type d -mtime +30 -exec rm -rf {} +

    echo "Backup completed: ${BACKUP_DIR}"

Environment Reconstruction Procedure
======================================

Document the procedure for fully reconstructing an environment for disaster recovery or test environment setup.

1. Start containers with Docker Compose
2. Wait until the OpenSearch health check returns green/yellow
3. Import Fess settings (via Admin API or restore feature)
4. Place dictionary files
5. Execute crawl jobs
6. Verify operation (search tests)

By scripting this procedure, you can quickly reconstruct environments.

Summary
========

This article introduced an approach to managing Fess search infrastructure using DevOps practices.

- Codifying environment definitions with Docker Compose
- Automating configuration with the Admin API and fessctl
- Automating configuration change deployment with CI/CD pipelines
- Automating backups and environment reconstruction procedures

Evolve your search infrastructure operations from "reading manuals and configuring manually" to "running code and deploying automatically."

The next article will cover extending Fess through plugin development.

References
==========

- `Fess Admin API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
