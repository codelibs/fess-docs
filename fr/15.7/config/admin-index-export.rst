================================
Fonction d'exportation d'index
================================

Aperçu
======

La fonction d'exportation d'index exporte les documents de recherche indexés dans OpenSearch vers des fichiers HTML ou JSON sur le système de fichiers local. Cette fonctionnalité est utile pour :

- Créer des sauvegardes statiques du contenu indexé
- Générer des copies hors ligne des documents à des fins d'archivage
- Construire des pages de résultats de recherche statiques
- Migrer du contenu vers d'autres systèmes

Les fichiers exportés conservent la structure de chemin URL d'origine des documents sources, ce qui facilite la gestion du contenu exporté.

Fonctionnement
==============

Lorsque le travail d'exportation d'index s'exécute, il effectue les opérations suivantes :

1. **Récupération des documents** : Récupère les documents depuis OpenSearch par lots efficaces grâce à l'API scroll
2. **Traitement du contenu** : Extrait les champs du document (titre, contenu, URL, etc.) et supprime les champs exclus
3. **Création de la structure des répertoires** : Reproduit la structure de chemin URL dans le répertoire d'exportation à partir du champ ``url`` du document
4. **Génération des fichiers** : Crée les fichiers (HTML ou JSON) contenant le contenu du document
5. **Traitement jusqu'à la fin** : Poursuit le traitement par lots jusqu'à ce que l'index soit entièrement exporté

L'API scroll permet de traiter efficacement de grands ensembles de documents sans problèmes de mémoire.

.. note::

   Les documents concernés par l'exportation sont ceux de l'index de recherche (``fess.search``). Les documents ne possédant pas de champ ``url`` sont ignorés.

Propriétés de configuration
============================

Configurez la fonction d'exportation d'index dans ``fess_config.properties`` :

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Propriété
     - Valeur par défaut
     - Description
   * - ``index.export.path``
     - ``/var/lib/fess/export``
     - Répertoire où les fichiers exportés sont stockés
   * - ``index.export.exclude.fields``
     - ``cache``
     - Champs à exclure de l'exportation (séparés par des virgules)
   * - ``index.export.scroll.size``
     - ``100``
     - Nombre de documents traités par lot
   * - ``index.export.format``
     - ``html``
     - Format des fichiers exportés (``html`` ou ``json``)

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
3. Trouvez **Index Exporter** dans la liste des travaux
4. Cliquez pour modifier les paramètres du travail
5. Définissez le calendrier à l'aide d'une expression cron
6. Enregistrez les paramètres

Exemples d'expressions cron :

- ``0 0 2 * * ?`` - Exécuter quotidiennement à 2h00
- ``0 0 3 ? * SUN`` - Exécuter chaque dimanche à 3h00
- ``0 0 0 1 * ?`` - Exécuter le premier jour de chaque mois à minuit

Filtrage de requête personnalisé
=================================

Vous pouvez personnaliser le travail d'exportation pour n'exporter que des documents spécifiques en modifiant le script du travail.

Le script par défaut du travail **Index Exporter** exporte tous les documents :

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.matchAllQuery())
        .execute()

Pour ajouter un filtre de requête personnalisé :

1. Naviguez vers **Système** > **Planificateur**
2. Modifiez le **Index Exporter**
3. Modifiez le script du travail pour inclure un filtre de requête

Exemple avec filtre de date (exporter uniquement les documents des 7 derniers jours) :

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.rangeQuery("created").gte("now-7d"))
        .execute()

Exemple avec filtre de site (exporter uniquement les documents d'un site spécifique) :

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.wildcardQuery("url", "*example.com*"))
        .execute()

Exemple pour exporter au format JSON :

::

    return new org.codelibs.fess.job.IndexExportJob()
        .format("json")
        .execute()

Structure des fichiers exportés
================================

Les fichiers exportés sont organisés pour refléter la structure URL d'origine.

Par exemple, un document avec l'URL ``https://example.com/docs/guide/intro.html`` serait exporté vers :

::

    /var/lib/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

Le chemin du fichier est déterminé à partir du champ ``url`` du document selon les règles suivantes :

- Le nom d'hôte devient le répertoire de premier niveau. Si l'URL ne contient pas de nom d'hôte, ``_local`` est utilisé.
- Si le chemin se termine par un slash ou si le document n'a pas de chemin, un fichier index (``index.html`` ou ``index.json``) est créé.
- Si le chemin ne contient pas d'extension de fichier, l'extension correspondant au format (``.html`` ou ``.json``) est ajoutée.
- Les caractères interdits dans les noms de fichiers (``< > : " | ? * \``) sont remplacés par ``_``, et chaque composant du chemin est tronqué à 200 caractères au maximum.
- Si l'URL ne peut pas être analysée ou qu'une traversée de répertoire est détectée, le fichier est enregistré dans le répertoire ``_invalid`` avec la valeur de hachage de l'URL comme nom de fichier.

Pour le format HTML, chaque fichier est généré avec la structure suivante :

- Champ ``title`` → élément ``<title>``
- Champ ``lang`` → attribut ``lang`` de l'élément ``<html>``
- Champ ``content`` → corps de l'élément ``<body>``
- Autres champs non exclus → balises ``<meta name="fess:nom_du_champ" content="valeur">`` dans ``<head>``

::

    <!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta charset="UTF-8">
    <title>Document exemple</title>
    <meta name="fess:url" content="https://example.com/docs/guide/intro.html">
    <meta name="fess:last_modified" content="2024-01-01T00:00:00.000Z">
    <meta name="fess:content_type" content="text/html">
    </head>
    <body>
    Contenu principal du document
    </body>
    </html>

Pour le format JSON, chaque fichier est un objet JSON contenant tous les champs non exclus :

::

    {
      "url": "https://example.com/docs/guide/intro.html",
      "title": "Document exemple",
      "content": "Contenu principal du document",
      "last_modified": "2024-01-01T00:00:00.000Z",
      "content_type": "text/html"
    }

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
  - Documents de petite taille : taille de lot plus grande (200-500)
  - Documents de grande taille : taille de lot plus petite (50-100)
- Planifiez les exportations pendant les périodes de faible utilisation
- Surveillez les E/S disque pendant les opérations d'exportation

Recommandations de sécurité
----------------------------

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
------------------------------

1. Confirmez que des documents existent dans l'index
2. Vérifiez les permissions du chemin d'exportation
3. Vérifiez que le filtre de requête (si personnalisé) correspond aux documents

::

    # Vérifier le nombre de documents dans l'index
    curl -X GET "localhost:9201/fess.search/_count?pretty"

L'exportation échoue en cours de route
---------------------------------------

1. Vérifiez l'espace disque disponible
2. Consultez les journaux pour les erreurs de mémoire ou de délai d'attente
3. Envisagez de réduire ``scroll.size`` pour les documents volumineux
4. Vérifiez les paramètres de délai d'attente du contexte scroll d'OpenSearch

Fichiers non accessibles
-------------------------

1. Vérifiez les permissions des fichiers : ``ls -la /var/lib/fess/export``
2. Vérifiez que le propriétaire du répertoire correspond à l'utilisateur du processus |Fess|
3. Confirmez que les politiques SELinux ou AppArmor autorisent l'accès

Sujets connexes
===============

- :doc:`admin-index-backup` - Procédures de sauvegarde et restauration d'index
- :doc:`admin-logging` - Configuration de la journalisation pour le dépannage
