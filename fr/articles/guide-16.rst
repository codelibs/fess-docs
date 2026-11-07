===========================================================
Partie 16 : Automatisation de l'infrastructure de recherche
===========================================================

Introduction
=============

Lorsque la configuration d'un système de recherche est gérée manuellement, la reproduction des environnements devient difficile et le risque d'erreurs de configuration augmente.
En adoptant les pratiques modernes de DevOps, gérons et automatisons également l'infrastructure de recherche en tant que code.

Cet article présente une approche pour gérer les configurations de Fess en tant que code et automatiser les déploiements.

Public cible
=============

- Les personnes souhaitant automatiser les opérations du système de recherche
- Les personnes souhaitant appliquer les méthodes DevOps/IaC à l'infrastructure de recherche
- Les personnes ayant des connaissances de base en Docker et CI/CD

Application de l'Infrastructure as Code
==========================================

Les éléments suivants sont gérés en tant que "code" pour les environnements Fess.

.. list-table:: Objets de gestion IaC
   :header-rows: 1
   :widths: 25 35 40

   * - Objet
     - Méthode de gestion
     - Contrôle de version
   * - Configuration Docker
     - compose.yaml
     - Git
   * - Paramètres Fess
     - Fichiers de sauvegarde / API d'administration
     - Git
   * - Données de dictionnaire
     - Exportation via l'API d'administration
     - Git
   * - Paramètres OpenSearch
     - Fichiers de configuration
     - Git

Définition d'environnement avec Docker Compose
=================================================

Fichier Docker Compose pour la production
-------------------------------------------

Nous étendons la configuration de base utilisée dans la Partie 2 pour définir une configuration adaptée aux environnements de production.

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

Les points clés sont les suivants.

- Définition du health check : Fess ne démarre qu'une fois OpenSearch prêt
- Persistance des volumes : Les données sont conservées de manière permanente
- Politique de redémarrage : Récupération automatique en cas de défaillance
- Configuration explicite du heap JVM

Automatisation de la configuration avec l'API d'administration
================================================================

En utilisant l'API d'administration de Fess, vous pouvez gérer les configurations de manière programmatique sans passer par l'interface graphique.

Exporter les paramètres
------------------------

Exportez les paramètres actuels de Fess et enregistrez-les sous forme de code.

Vous pouvez exporter depuis la console d'administration sous [Informations système] > [Sauvegarde].
Il est également possible d'exporter via des scripts en utilisant l'API d'administration.

Importer les paramètres
------------------------

Appliquez les paramètres à un nouvel environnement Fess en utilisant les fichiers de configuration sauvegardés.
Cela facilite la reconstruction ou la réplication des environnements.

Utilisation de la CLI fessctl
==============================

fessctl est un outil en ligne de commande pour Fess.
De nombreuses opérations réalisables dans la console d'administration peuvent également être exécutées depuis la ligne de commande.

Opérations principales
-----------------------

- Créer, mettre à jour et supprimer des configurations de crawl (web, système de fichiers, magasin de données)
- Exécuter des tâches planifiées
- Gérer les utilisateurs, les rôles et les groupes
- Gérer les paramètres de recherche tels que le key match, les labels et les boosts

En utilisant la CLI, vous pouvez scripter les changements de configuration et les intégrer dans les pipelines CI/CD.

Construction de pipelines CI/CD
=================================

Workflow pour les changements de configuration
-------------------------------------------------

Gérez les changements de configuration du système de recherche avec le workflow suivant.

1. **Modification** : Modifier les fichiers de configuration et les gérer dans une branche Git
2. **Revue** : Examiner les changements via des pull requests
3. **Test** : Vérifier le comportement dans un environnement de staging
4. **Déploiement** : Appliquer les paramètres à l'environnement de production

Exemple d'automatisation avec GitHub Actions
-----------------------------------------------

Voici un exemple d'application automatique des modifications à l'environnement de production lorsque des changements de fichiers de configuration sont fusionnés.

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

Automatisons également les sauvegardes régulières.

Script de sauvegarde
---------------------

Utilisez cron ou les fonctionnalités de planification CI/CD pour effectuer des sauvegardes régulières.

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

Procédure de reconstruction de l'environnement
=================================================

Documentez la procédure de reconstruction complète d'un environnement pour la reprise après sinistre ou la mise en place d'environnements de test.

1. Démarrer les conteneurs avec Docker Compose
2. Attendre que le health check d'OpenSearch renvoie green/yellow
3. Importer les paramètres Fess (via l'API d'administration ou la fonction de restauration)
4. Placer les fichiers de dictionnaire
5. Exécuter les tâches de crawl
6. Vérifier le fonctionnement (tests de recherche)

En scriptant cette procédure, vous pouvez reconstruire rapidement les environnements.

Résumé
=======

Cet article a présenté une approche pour gérer l'infrastructure de recherche Fess avec les pratiques DevOps.

- Codification des définitions d'environnement avec Docker Compose
- Automatisation de la configuration avec l'API d'administration et fessctl
- Automatisation du déploiement des changements de configuration avec les pipelines CI/CD
- Automatisation des sauvegardes et procédures de reconstruction d'environnement

Faites évoluer les opérations de votre infrastructure de recherche de "lire des manuels et configurer manuellement" à "exécuter du code et déployer automatiquement".

Le prochain article traitera de l'extension de Fess par le développement de plugins.

Références
===========

- `Fess Admin API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
