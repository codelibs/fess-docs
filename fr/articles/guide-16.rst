============================================================
Partie 16 : Automatisation de l'infrastructure de recherche -- Gestion avec les pipelines CI/CD et l'Infrastructure as Code
============================================================

Introduction
=============

Lorsque la configuration d'un systeme de recherche est geree manuellement, la reproduction des environnements devient difficile et le risque d'erreurs de configuration augmente.
En adoptant les pratiques modernes de DevOps, gerons et automatisons egalement l'infrastructure de recherche en tant que code.

Cet article presente une approche pour gerer les configurations de Fess en tant que code et automatiser les deploiements.

Public cible
=============

- Les personnes souhaitant automatiser les operations du systeme de recherche
- Les personnes souhaitant appliquer les methodes DevOps/IaC a l'infrastructure de recherche
- Les personnes ayant des connaissances de base en Docker et CI/CD

Application de l'Infrastructure as Code
==========================================

Les elements suivants sont geres en tant que "code" pour les environnements Fess.

.. list-table:: Objets de gestion IaC
   :header-rows: 1
   :widths: 25 35 40

   * - Objet
     - Methode de gestion
     - Controle de version
   * - Configuration Docker
     - compose.yaml
     - Git
   * - Parametres Fess
     - Fichiers de sauvegarde / API d'administration
     - Git
   * - Donnees de dictionnaire
     - Exportation via l'API d'administration
     - Git
   * - Parametres OpenSearch
     - Fichiers de configuration
     - Git

Definition d'environnement avec Docker Compose
=================================================

Fichier Docker Compose pour la production
-------------------------------------------

Nous etendons la configuration de base utilisee dans la Partie 2 pour definir une configuration adaptee aux environnements de production.

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

Les points cles sont les suivants.

- Definition du health check : Fess ne demarre qu'une fois OpenSearch pret
- Persistance des volumes : Les donnees sont conservees de maniere permanente
- Politique de redemarrage : Recuperation automatique en cas de defaillance
- Configuration explicite du heap JVM

Automatisation de la configuration avec l'API d'administration
================================================================

En utilisant l'API d'administration de Fess, vous pouvez gerer les configurations de maniere programmatique sans passer par l'interface graphique.

Exporter les parametres
------------------------

Exportez les parametres actuels de Fess et enregistrez-les sous forme de code.

Vous pouvez exporter depuis la console d'administration sous [Informations systeme] > [Sauvegarde].
Il est egalement possible d'exporter via des scripts en utilisant l'API d'administration.

Importer les parametres
------------------------

Appliquez les parametres a un nouvel environnement Fess en utilisant les fichiers de configuration sauvegardes.
Cela facilite la reconstruction ou la replication des environnements.

Utilisation de la CLI fessctl
==============================

fessctl est un outil en ligne de commande pour Fess.
De nombreuses operations realisables dans la console d'administration peuvent egalement etre executees depuis la ligne de commande.

Operations principales
-----------------------

- Creer, mettre a jour et supprimer des configurations de crawl (web, systeme de fichiers, magasin de donnees)
- Executer des taches planifiees
- Gerer les utilisateurs, les roles et les groupes
- Gerer les parametres de recherche tels que le key match, les labels et les boosts

En utilisant la CLI, vous pouvez scripter les changements de configuration et les integrer dans les pipelines CI/CD.

Construction de pipelines CI/CD
=================================

Workflow pour les changements de configuration
-------------------------------------------------

Gerez les changements de configuration du systeme de recherche avec le workflow suivant.

1. **Modification** : Modifier les fichiers de configuration et les gerer dans une branche Git
2. **Revue** : Examiner les changements via des pull requests
3. **Test** : Verifier le comportement dans un environnement de staging
4. **Deploiement** : Appliquer les parametres a l'environnement de production

Exemple d'automatisation avec GitHub Actions
-----------------------------------------------

Voici un exemple d'application automatique des modifications a l'environnement de production lorsque des changements de fichiers de configuration sont fusionnes.

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
              # Transferer les fichiers de dictionnaire vers le serveur Fess
              scp dictionary/* fess-server:/opt/fess/dictionary/

          - name: Verify Fess health
            run: |
              # Verifier l'etat operationnel de Fess via l'API de sante
              curl -s https://fess.example.com/api/v1/health

Automatisation des sauvegardes
================================

Automatisons egalement les sauvegardes regulieres.

Script de sauvegarde
---------------------

Utilisez cron ou les fonctionnalites de planification CI/CD pour effectuer des sauvegardes regulieres.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    BACKUP_DIR="/backup/fess/$(date +%Y%m%d)"
    mkdir -p "${BACKUP_DIR}"

    # Recuperer la liste des fichiers de sauvegarde Fess
    curl -s -o "${BACKUP_DIR}/fess-backup-files.json" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/files"

    # Telecharger les donnees de configuration (ex. : fess_config.bulk)
    curl -s -o "${BACKUP_DIR}/fess_config.bulk" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/file/fess_config.bulk"

    # Supprimer les anciennes sauvegardes (plus de 30 jours)
    find /backup/fess -type d -mtime +30 -exec rm -rf {} +

    echo "Backup completed: ${BACKUP_DIR}"

Procedure de reconstruction de l'environnement
=================================================

Documentez la procedure de reconstruction complete d'un environnement pour la reprise apres sinistre ou la mise en place d'environnements de test.

1. Demarrer les conteneurs avec Docker Compose
2. Attendre que le health check d'OpenSearch renvoie green/yellow
3. Importer les parametres Fess (via l'API d'administration ou la fonction de restauration)
4. Placer les fichiers de dictionnaire
5. Executer les taches de crawl
6. Verifier le fonctionnement (tests de recherche)

En scriptant cette procedure, vous pouvez reconstruire rapidement les environnements.

Resume
=======

Cet article a presente une approche pour gerer l'infrastructure de recherche Fess avec les pratiques DevOps.

- Codification des definitions d'environnement avec Docker Compose
- Automatisation de la configuration avec l'API d'administration et fessctl
- Automatisation du deploiement des changements de configuration avec les pipelines CI/CD
- Automatisation des sauvegardes et procedures de reconstruction d'environnement

Faites evoluer les operations de votre infrastructure de recherche de "lire des manuels et configurer manuellement" a "executer du code et deployer automatiquement".

Le prochain article traitera de l'extension de Fess par le developpement de plugins.

References
===========

- `Fess Admin API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
