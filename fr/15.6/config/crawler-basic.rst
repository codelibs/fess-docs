====================
Configuration de base du robot d'indexation
====================

Présentation
====

Le robot d'indexation (crawler) de |Fess| est une fonctionnalité qui collecte automatiquement du contenu à partir de sites Web et de systèmes de fichiers, et l'enregistre dans l'index de recherche.
Ce guide explique les concepts de base et les méthodes de configuration du robot d'indexation.

Concepts de base du robot d'indexation
====================

Qu'est-ce qu'un robot d'indexation
--------------

Un robot d'indexation (Crawler) est un programme qui collecte automatiquement du contenu en suivant des liens à partir d'une URL ou d'un chemin de fichier spécifié.

Le robot d'indexation de |Fess| présente les caractéristiques suivantes :

- **Support multi-protocole** : HTTP/HTTPS, système de fichiers, SMB, FTP, etc.
- **Exécution planifiée** : Indexation périodique automatique
- **Indexation incrémentale** : Mise à jour uniquement du contenu modifié
- **Traitement parallèle** : Indexation simultanée de plusieurs URLs
- **Conformité aux règles des robots** : Respect du fichier robots.txt

Types de robots d'indexation
----------------

|Fess| propose les types de robots d'indexation suivants selon la cible.

.. list-table:: Types de robots d'indexation
   :header-rows: 1
   :widths: 20 40 40

   * - Type
     - Cible
     - Usage
   * - **Robot Web**
     - Sites Web (HTTP/HTTPS)
     - Sites Web publics, sites Web intranet
   * - **Robot de fichiers**
     - Système de fichiers, SMB, FTP
     - Serveurs de fichiers, dossiers partagés
   * - **Robot de base de données**
     - Bases de données
     - Sources de données RDB, CSV, JSON, etc.

Création de la configuration d'indexation
==================

Ajout d'une configuration d'indexation de base
--------------------------

1. **Accéder à l'interface d'administration**

   Accédez à ``http://localhost:8080/admin`` dans votre navigateur et connectez-vous en tant qu'administrateur.

2. **Ouvrir l'écran de configuration du robot d'indexation**

   Dans le menu de gauche, sélectionnez « Crawler » → « Web » ou « File System ».

3. **Créer une nouvelle configuration**

   Cliquez sur le bouton « Nouveau ».

4. **Saisir les informations de base**

   - **Nom** : Nom d'identification de la configuration d'indexation (ex : Wiki d'entreprise)
   - **URL** : URL de départ de l'indexation (ex : ``https://wiki.example.com/``)
   - **Intervalle d'indexation** : Fréquence d'exécution de l'indexation (ex : toutes les heures)
   - **Nombre de threads** : Nombre d'indexations parallèles (ex : 5)
   - **Profondeur** : Profondeur des niveaux de liens à suivre (ex : 3)

5. **Enregistrer**

   Cliquez sur le bouton « Créer » pour enregistrer la configuration.

Exemples de configuration du robot Web
---------------------

Indexation d'un site intranet d'entreprise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Nom : Portail d'entreprise
    URL : http://intranet.example.com/
    Intervalle d'indexation : 1 fois par jour
    Nombre de threads : 10
    Profondeur : Illimitée (-1)
    Nombre maximum d'accès : 10000

Indexation d'un site Web public
~~~~~~~~~~~~~~~~~~~~~~~

::

    Nom : Site produit
    URL : https://www.example.com/products/
    Intervalle d'indexation : 1 fois par semaine
    Nombre de threads : 5
    Profondeur : 5
    Nombre maximum d'accès : 1000

Exemples de configuration du robot de fichiers
--------------------------

Système de fichiers local
~~~~~~~~~~~~~~~~~~~~~~~~

::

    Nom : Dossier Documents
    URL : file:///home/share/documents/
    Intervalle d'indexation : 1 fois par jour
    Nombre de threads : 3
    Profondeur : Illimitée (-1)

SMB/CIFS (Partage de fichiers Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Nom : Serveur de fichiers
    URL : smb://fileserver.example.com/share/
    Intervalle d'indexation : 1 fois par jour
    Nombre de threads : 5
    Profondeur : Illimitée (-1)

Configuration des informations d'authentification
--------------

Pour accéder à des sites ou des serveurs de fichiers nécessitant une authentification, configurez les informations d'authentification.

1. Dans l'interface d'administration, sélectionnez « Crawler » → « Authentication »
2. Cliquez sur « Nouveau »
3. Saisissez les informations d'authentification :

   ::

       Nom d'hôte : wiki.example.com
       Port : 443
       Méthode d'authentification : Basic Authentication
       Nom d'utilisateur : crawler_user
       Mot de passe : ********

4. Cliquez sur « Créer »

Exécution de l'indexation
==============

Exécution manuelle
--------

Pour exécuter immédiatement une indexation configurée :

1. Dans la liste des configurations d'indexation, sélectionnez la configuration cible
2. Cliquez sur le bouton « Démarrer »
3. Vérifiez l'état d'exécution du travail dans le menu « Scheduler »

Exécution planifiée
----------------

Pour exécuter l'indexation périodiquement :

1. Ouvrez le menu « Scheduler »
2. Sélectionnez le travail « Default Crawler »
3. Configurez l'expression de planification (format Cron)

   ::

       # Exécution quotidienne à 2h du matin
       0 0 2 * * ?

       # Exécution chaque heure à 0 minute
       0 0 * * * ?

       # Exécution du lundi au vendredi à 18h
       0 0 18 ? * MON-FRI

4. Cliquez sur « Mettre à jour »

Vérification de l'état de l'indexation
------------------

Pour vérifier l'état de l'indexation en cours :

1. Ouvrez le menu « Scheduler »
2. Vérifiez les travaux en cours d'exécution
3. Consultez les détails dans les journaux :

   ::

       tail -f /var/log/fess/fess_crawler.log

Paramètres de configuration de base
================

Limitation des cibles d'indexation
------------------

Limitation par motif d'URL
~~~~~~~~~~~~~~~~~~~~~

Vous pouvez cibler ou exclure des motifs d'URL spécifiques pour l'indexation.

**Motifs d'URL à inclure (expression régulière) :**

::

    # Indexer uniquement sous /docs/
    https://example\.com/docs/.*

**Motifs d'URL à exclure (expression régulière) :**

::

    # Exclure des répertoires spécifiques
    .*/admin/.*
    .*/private/.*

    # Exclure des extensions de fichiers spécifiques
    .*\.(jpg|png|gif|css|js)$

Limitation de profondeur
~~~~~~~~~~

Limiter la profondeur des niveaux de liens à suivre :

- **0** : URL de départ uniquement
- **1** : URL de départ et pages liées à partir de celle-ci
- **-1** : Illimitée (suivre tous les liens)

Nombre maximum d'accès
~~~~~~~~~~~~~~

Limite supérieure du nombre de pages à indexer :

::

    Nombre maximum d'accès : 1000

L'indexation s'arrête après 1000 pages.

Nombre d'indexations parallèles (nombre de threads)
--------------------------

Spécifie le nombre d'URLs à indexer simultanément.

.. list-table:: Nombre de threads recommandé
   :header-rows: 1
   :widths: 40 30 30

   * - Environnement
     - Valeur recommandée
     - Description
   * - Petits sites (jusqu'à 10 000 pages)
     - 3 à 5
     - Réduire la charge sur le serveur cible
   * - Sites moyens (10 000 à 100 000 pages)
     - 5 à 10
     - Configuration équilibrée
   * - Grands sites (plus de 100 000 pages)
     - 10 à 20
     - Indexation rapide nécessaire
   * - Serveurs de fichiers
     - 3 à 5
     - Tenir compte de la charge d'E/S des fichiers

.. warning::
   L'augmentation excessive du nombre de threads impose une charge excessive sur le serveur cible.
   Veuillez définir une valeur appropriée.

Intervalle d'indexation
------------

Spécifie la fréquence d'exécution de l'indexation.

::

    # Spécification horaire
    Intervalle d'indexation : 3600000  # millisecondes (1 heure)

    # Ou configuré dans le planificateur
    0 0 2 * * ?  # Tous les jours à 2h du matin

Configuration de la taille des fichiers
====================

Vous pouvez définir la limite supérieure de la taille des fichiers à indexer.

Limite supérieure de la taille des fichiers à récupérer
----------------------------

Ajoutez ce qui suit aux « Paramètres de configuration » de la configuration du robot d'indexation :

::

    client.maxContentLength=10485760

Récupère les fichiers jusqu'à 10 Mo. Par défaut, il n'y a pas de limite.

.. note::
   Lors de l'indexation de fichiers volumineux, ajustez également les paramètres de mémoire.
   Consultez :doc:`setup-memory` pour plus de détails.

Limite supérieure de la taille des fichiers à indexer
------------------------------------

Vous pouvez définir la limite supérieure de la taille à indexer pour chaque type de fichier.

**Valeurs par défaut :**

- Fichiers HTML : 2,5 Mo
- Autres fichiers : 10 Mo

**Fichier de configuration :** ``app/WEB-INF/classes/crawler/contentlength.xml``

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
            "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
            <include path="crawler/container.xml" />

            <component name="contentLengthHelper"
                    class="org.codelibs.fess.crawler.helper.ContentLengthHelper" instance="singleton">
                    <property name="defaultMaxLength">10485760</property><!-- 10M -->
                    <postConstruct name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440</arg><!-- 2.5M -->
                    </postConstruct>
                    <postConstruct name="addMaxLength">
                            <arg>"application/pdf"</arg>
                            <arg>5242880</arg><!-- 5M -->
                    </postConstruct>
            </component>
    </components>

Cela ajoute une configuration pour traiter les fichiers PDF jusqu'à 5 Mo.

.. warning::
   Lors de l'augmentation de la taille des fichiers traités, augmentez également les paramètres de mémoire du robot d'indexation.

.. note::
   Si la taille du document dépasse 50 Mo, vous devez également modifier les paramètres d'OpenSearch.
   OpenSearch limite par défaut la longueur maximale des champs de chaîne dans le contenu JSON à 50 Mo.

   Ajoutez ce qui suit dans ``opensearch.yml`` :

   ::

       opensearch.xcontent.string.length.max: 104857600

   L'exemple ci-dessus définit la limite à 100 Mo. Pour plus de détails, consultez la `documentation OpenSearch <https://docs.opensearch.org/latest/install-and-configure/install-opensearch/index/#important-system-properties>`_.

Limitation de la longueur des mots
==============

Présentation
----

Les longues chaînes de caractères alphanumériques uniquement ou les symboles consécutifs entraînent une augmentation de la taille de l'index et une dégradation des performances.
Par conséquent, |Fess| impose par défaut les limites suivantes :

- **Caractères alphanumériques consécutifs** : jusqu'à 20 caractères
- **Symboles consécutifs** : jusqu'à 10 caractères

Méthode de configuration
--------

Modifiez ``fess_config.properties``.

**Configuration par défaut :**

::

    crawler.document.max.alphanum.term.size=20
    crawler.document.max.symbol.term.size=10

**Exemple : pour assouplir les limites**

::

    crawler.document.max.alphanum.term.size=50
    crawler.document.max.symbol.term.size=20

.. note::
   Si vous devez rechercher de longues chaînes alphanumériques (ex : numéros de série, tokens, etc.),
   augmentez cette valeur. Cependant, la taille de l'index augmentera.

Configuration du proxy
==============

Présentation
----

Lors de l'indexation de sites externes depuis un intranet, ils peuvent être bloqués par un pare-feu.
Dans ce cas, effectuez l'indexation via un serveur proxy.

Méthode de configuration
--------

Dans la configuration d'indexation de l'interface d'administration, ajoutez ce qui suit aux « Paramètres de configuration ».

**Configuration proxy de base :**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

**Proxy nécessitant une authentification :**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

**Exclure des hôtes spécifiques du proxy :**

::

    client.nonProxyHosts=localhost|127.0.0.1|*.example.com

Configuration proxy à l'échelle du système
--------------------------

Si vous utilisez le même proxy pour toutes les configurations d'indexation, vous pouvez le configurer avec des variables d'environnement.

::

    export http_proxy=http://proxy.example.com:8080
    export https_proxy=http://proxy.example.com:8080
    export no_proxy=localhost,127.0.0.1,.example.com

Configuration de robots.txt
=================

Présentation
----

robots.txt est un fichier qui indique aux robots d'indexation s'ils peuvent ou non indexer.
|Fess| respecte robots.txt par défaut.

Méthode de configuration
--------

Pour ignorer robots.txt, modifiez ``fess_config.properties``.

::

    crawler.ignore.robots.txt=true

.. warning::
   Lors de l'indexation de sites externes, respectez robots.txt.
   L'ignorer peut imposer une charge excessive sur le serveur ou violer les conditions d'utilisation.

Configuration du User-Agent
=================

Vous pouvez modifier le User-Agent du robot d'indexation.

Configuration dans l'interface d'administration
----------------

Ajoutez aux « Paramètres de configuration » de la configuration d'indexation :

::

    client.userAgent=MyCompanyCrawler/1.0

Configuration à l'échelle du système
------------------

Configurez dans ``fess_config.properties`` :

::

    crawler.user.agent=MyCompanyCrawler/1.0

Configuration de l'encodage
====================

Encodage des données d'indexation
--------------------------------

Configurez dans ``fess_config.properties`` :

::

    crawler.crawling.data.encoding=UTF-8

Encodage des noms de fichiers
----------------------------

Encodage des noms de fichiers du système de fichiers :

::

    crawler.document.file.name.encoding=UTF-8

Dépannage de l'indexation
================================

L'indexation ne démarre pas
----------------------

**Points à vérifier :**

1. Vérifier si le planificateur est activé

   - Dans le menu « Scheduler », vérifiez si le travail « Default Crawler » est activé

2. Vérifier si la configuration d'indexation est activée

   - Dans la liste des configurations d'indexation, vérifiez si la configuration cible est activée

3. Vérifier les journaux

   ::

       tail -f /var/log/fess/fess.log
       tail -f /var/log/fess/fess_crawler.log

L'indexation s'arrête en cours de route
------------------------

**Causes possibles :**

1. **Mémoire insuffisante**

   - Vérifiez s'il y a des ``OutOfMemoryError`` dans ``fess_crawler.log``
   - Augmenter la mémoire du robot d'indexation (voir :doc:`setup-memory`)

2. **Erreur réseau**

   - Ajuster les paramètres de timeout
   - Vérifier les paramètres de nouvelle tentative

3. **Erreur de la cible d'indexation**

   - Vérifier s'il y a de nombreuses erreurs 404
   - Vérifier les détails des erreurs dans les journaux

Une page spécifique n'est pas indexée
------------------------------

**Points à vérifier :**

1. **Vérifier les motifs d'URL**

   - Vérifier si elle ne correspond pas aux motifs d'URL exclus

2. **Vérifier robots.txt**

   - Vérifier ``/robots.txt`` du site cible

3. **Vérifier l'authentification**

   - Pour les pages nécessitant une authentification, vérifier les paramètres d'authentification

4. **Limitation de profondeur**

   - Vérifier si la hiérarchie des liens dépasse la limite de profondeur

5. **Nombre maximum d'accès**

   - Vérifier si le nombre maximum d'accès a été atteint

L'indexation est lente
--------------

**Solutions :**

1. **Augmenter le nombre de threads**

   - Augmenter le nombre d'indexations parallèles (mais attention à la charge sur le serveur cible)

2. **Exclure les URLs inutiles**

   - Ajouter les images et les fichiers CSS aux motifs d'URL exclus

3. **Ajuster les paramètres de timeout**

   - Pour les sites à réponse lente, réduire le timeout

4. **Augmenter la mémoire du robot d'indexation**

   - Voir :doc:`setup-memory`

Bonnes pratiques
==================

Recommandations pour la configuration d'indexation
----------------------

1. **Définir un nombre de threads approprié**

   Définissez un nombre de threads approprié pour ne pas imposer une charge excessive sur le serveur cible.

2. **Optimisation des motifs d'URL**

   En excluant les fichiers inutiles (images, CSS, JavaScript, etc.),
   vous réduisez le temps d'indexation et améliorez la qualité de l'index.

3. **Configuration de la limitation de profondeur**

   Définissez une profondeur appropriée en fonction de la structure du site.
   Utilisez illimitée (-1) uniquement pour indexer l'ensemble du site.

4. **Configuration du nombre maximum d'accès**

   Définissez une limite supérieure pour éviter d'indexer un nombre inattendu de pages.

5. **Ajustement de l'intervalle d'indexation**

   Définissez un intervalle approprié en fonction de la fréquence de mise à jour.
   - Sites fréquemment mis à jour : toutes les 1 heure à quelques heures
   - Sites rarement mis à jour : tous les 1 jour à 1 semaine

Recommandations pour la configuration de la planification
--------------------------

1. **Exécution nocturne**

   Exécutez pendant les périodes de faible charge du serveur (ex : 2h du matin).

2. **Éviter les exécutions en double**

   Configurez pour démarrer l'indexation suivante après la fin de l'indexation précédente.

3. **Notification en cas d'erreur**

   Configurez une notification par e-mail en cas d'échec de l'indexation.

Informations de référence
========

- :doc:`crawler-advanced` - Configuration avancée du robot d'indexation
- :doc:`crawler-thumbnail` - Configuration des vignettes
- :doc:`setup-memory` - Configuration de la mémoire
- :doc:`admin-logging` - Configuration des journaux
