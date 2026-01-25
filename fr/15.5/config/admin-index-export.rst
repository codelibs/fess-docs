================================
Fonction d'exportation d'index
================================

Aperçu
======

La fonction d'exportation d'index vous permet d'exporter des documents de recherche indexés dans OpenSearch vers des fichiers HTML sur le système de fichiers local. Cette fonctionnalité est utile pour :

- Créer des sauvegardes statiques du contenu indexé
- Générer des copies hors ligne des documents à des fins d'archivage
- Construire des pages de résultats de recherche statiques
- Migrer du contenu vers d'autres systèmes

Les fichiers exportés conservent la structure de chemin URL d'origine des documents sources, ce qui facilite la navigation et la gestion du contenu exporté.

Fonctionnement
==============

Lorsque le travail d'exportation d'index s'exécute, il effectue le processus suivant :

1. **Interroger les documents** : Récupère les documents depuis OpenSearch en utilisant l'API scroll pour un traitement par lots efficace
2. **Traiter le contenu** : Extrait les champs du document (titre, contenu, URL, etc.)
3. **Créer la structure des répertoires** : Réplique la structure du chemin URL dans le répertoire d'exportation
4. **Générer les fichiers HTML** : Crée des fichiers HTML contenant le contenu du document
5. **Continuer jusqu'à la fin** : Traite tous les documents par lots jusqu'à ce que l'index soit entièrement exporté

L'API scroll assure une gestion efficace des grands ensembles de documents sans problèmes de mémoire.

Propriétés de configuration
===========================

Configurez la fonction d'exportation d'index dans ``fess_config.properties`` :

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Propriété
     - Valeur par défaut
     - Description
   * - ``index.export.path``
     - ``/var/fess/export``
     - Répertoire où les fichiers exportés sont stockés
   * - ``index.export.exclude.fields``
     - ``cache``
     - Liste des champs à exclure séparés par des virgules
   * - ``index.export.scroll.size``
     - ``100``
     - Nombre de documents traités par lot

Exemple de configuration :

::

    index.export.path=/data/fess/export
    index.export.exclude.fields=cache,boost,role
    index.export.scroll.size=200

Activation du travail
=====================

Le travail d'exportation d'index est enregistré comme travail planifié mais est désactivé par défaut.

Pour activer le travail :

1. Connectez-vous à la console d'administration |Fess|
2. Naviguez vers **Système** > **Planificateur**
3. Trouvez **Index Export Job** dans la liste des travaux
4. Cliquez pour modifier les paramètres du travail
5. Définissez le calendrier à l'aide d'une expression cron
6. Enregistrez les paramètres

Exemples d'expressions cron :

- ``0 0 2 * * ?`` - Exécuter quotidiennement à 2h00
- ``0 0 3 ? * SUN`` - Exécuter chaque dimanche à 3h00
- ``0 0 0 1 * ?`` - Exécuter le premier jour de chaque mois à minuit

Filtrage de requête personnalisé
================================

Vous pouvez personnaliser le travail d'exportation pour n'exporter que des documents spécifiques en modifiant le script du travail.

Pour ajouter un filtre de requête personnalisé :

1. Naviguez vers **Système** > **Planificateur**
2. Modifiez le **Index Export Job**
3. Modifiez le script du travail pour inclure un filtre de requête

Exemple de script avec filtre de date :

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "created:>=now-7d"
    job.execute()

Exemple de script avec filtre de site :

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "url:*example.com*"
    job.execute()

Structure des fichiers exportés
===============================

Les fichiers exportés sont organisés pour refléter la structure URL d'origine.

Par exemple, un document avec l'URL ``https://example.com/docs/guide/intro.html`` serait exporté vers :

::

    /var/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

Chaque fichier HTML exporté contient :

- Titre du document
- Corps du contenu principal
- Métadonnées (date de dernière modification, type de contenu, etc.)
- Référence à l'URL d'origine

Bonnes pratiques
================

Considérations de stockage
--------------------------

- Assurez-vous d'avoir suffisamment d'espace disque dans le répertoire d'exportation
- Envisagez d'utiliser un stockage dédié pour les grands ensembles de documents
- Implémentez un nettoyage régulier des anciennes exportations si vous effectuez des exportations périodiques

Conseils de performance
-----------------------

- Ajustez ``index.export.scroll.size`` en fonction de la taille des documents :
  - Documents plus petits : taille de lot plus grande (200-500)
  - Documents plus grands : taille de lot plus petite (50-100)
- Planifiez les exportations pendant les périodes de faible utilisation
- Surveillez les E/S disque pendant les opérations d'exportation

Recommandations de sécurité
---------------------------

- Définissez les permissions de fichiers appropriées sur le répertoire d'exportation
- N'exposez pas le répertoire d'exportation directement sur le web
- Envisagez de chiffrer le contenu exporté s'il contient des informations sensibles
- Auditez régulièrement l'accès aux fichiers exportés

Dépannage
=========

Le travail d'exportation ne s'exécute pas
-----------------------------------------

1. Vérifiez que le travail est activé dans le Planificateur
2. Vérifiez la syntaxe de l'expression cron
3. Consultez les journaux |Fess| pour les messages d'erreur :

::

    tail -f /var/log/fess/fess.log | grep IndexExport

Répertoire d'exportation vide
-----------------------------

1. Confirmez que des documents existent dans l'index
2. Vérifiez les permissions du chemin d'exportation
3. Vérifiez que le filtre de requête (si personnalisé) correspond aux documents

::

    # Vérifier le nombre de documents dans l'index
    curl -X GET "localhost:9201/fess.YYYYMMDD/_count?pretty"

L'exportation échoue en cours de route
--------------------------------------

1. Vérifiez l'espace disque disponible
2. Consultez les journaux pour les erreurs de mémoire ou de délai d'attente
3. Envisagez de réduire ``scroll.size`` pour les documents volumineux
4. Vérifiez les paramètres de délai d'attente du contexte scroll d'OpenSearch

Fichiers non accessibles
------------------------

1. Vérifiez les permissions des fichiers : ``ls -la /var/fess/export``
2. Vérifiez que le propriétaire du répertoire correspond à l'utilisateur du processus |Fess|
3. Confirmez que les politiques SELinux ou AppArmor autorisent l'accès

Sujets connexes
===============

- :doc:`admin-index-backup` - Procédures de sauvegarde et restauration d'index
- :doc:`admin-logging` - Configuration des paramètres de journalisation pour le dépannage
