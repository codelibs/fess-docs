========================
Configuration avancée du robot d'indexation
========================

Présentation
====

Ce guide explique les paramètres avancés du robot d'indexation de |Fess|.
Pour la configuration de base du robot d'indexation, consultez :doc:`crawler-basic`.

.. warning::
   Les paramètres de cette page peuvent affecter l'ensemble du système.
   Lors de la modification des paramètres, testez-les suffisamment avant de les appliquer à l'environnement de production.

Configuration générale
========

Emplacement des fichiers de configuration
------------------

La configuration détaillée du robot d'indexation s'effectue dans les fichiers suivants.

- **Configuration principale** : ``/etc/fess/fess_config.properties`` (ou ``app/WEB-INF/classes/fess_config.properties``)
- **Configuration de la longueur du contenu** : ``app/WEB-INF/classes/crawler/contentlength.xml``
- **Configuration des composants** : ``app/WEB-INF/classes/crawler/container.xml``

Script par défaut
--------------------

Configure le langage de script par défaut du robot d'indexation.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.default.script``
     - Langage de script du robot d'indexation
     - ``groovy``

::

    crawler.default.script=groovy

Pool de threads HTTP
------------------

Configuration du pool de threads du robot d'indexation HTTP.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.http.thread_pool.size``
     - Taille du pool de threads HTTP
     - ``0``

::

    # Si 0, configuration automatique
    crawler.http.thread_pool.size=0

Configuration du traitement des documents
====================

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.max.site.length``
     - Nombre maximum de lignes du site du document
     - ``100``
   * - ``crawler.document.site.encoding``
     - Encodage du site du document
     - ``UTF-8``
   * - ``crawler.document.unknown.hostname``
     - Valeur de remplacement pour un nom d'hôte inconnu
     - ``unknown``
   * - ``crawler.document.use.site.encoding.on.english``
     - Utiliser l'encodage du site pour les documents en anglais
     - ``false``
   * - ``crawler.document.append.data``
     - Ajouter des données au document
     - ``true``
   * - ``crawler.document.append.filename``
     - Ajouter le nom de fichier au document
     - ``false``

Exemple de configuration
~~~~~~

::

    crawler.document.max.site.length=100
    crawler.document.site.encoding=UTF-8
    crawler.document.unknown.hostname=unknown
    crawler.document.use.site.encoding.on.english=false
    crawler.document.append.data=true
    crawler.document.append.filename=false

Configuration du traitement des mots
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.max.alphanum.term.size``
     - Longueur maximale des mots alphanumériques
     - ``20``
   * - ``crawler.document.max.symbol.term.size``
     - Longueur maximale des mots symboles
     - ``10``
   * - ``crawler.document.duplicate.term.removed``
     - Suppression des mots en double
     - ``false``

Exemple de configuration
~~~~~~

::

    # Modifier la longueur maximale des alphanumériques à 50 caractères
    crawler.document.max.alphanum.term.size=50

    # Modifier la longueur maximale des symboles à 20 caractères
    crawler.document.max.symbol.term.size=20

    # Supprimer les mots en double
    crawler.document.duplicate.term.removed=true

.. note::
   L'augmentation de ``max.alphanum.term.size`` permet d'indexer complètement les longs ID, tokens, URLs, etc.,
   mais la taille de l'index augmentera.

Configuration du traitement des caractères
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.space.chars``
     - Définition des caractères d'espacement
     - ``\u0009\u000A...``
   * - ``crawler.document.fullstop.chars``
     - Définition des caractères de ponctuation
     - ``\u002e\u06d4...``

Exemple de configuration
~~~~~~

::

    # Valeur par défaut (incluant les caractères Unicode)
    crawler.document.space.chars=\u0009\u000A\u000B\u000C\u000D\u001C\u001D\u001E\u001F\u0020\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u202F\u205F\u3000\uFEFF\uFFFD\u00B6

    crawler.document.fullstop.chars=\u002e\u06d4\u2e3c\u3002

Configuration des protocoles
==============

Protocoles supportés
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.web.protocols``
     - Protocoles d'indexation Web
     - ``http,https``
   * - ``crawler.file.protocols``
     - Protocoles d'indexation de fichiers
     - ``file,smb,smb1,ftp,storage,s3,gcs``

Exemple de configuration
~~~~~~~~~~~~~~~~~~~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage,s3,gcs

Paramètres de variables d'environnement
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.data.env.param.key.pattern``
     - Motif de clé de paramètre de variable d'environnement
     - ``^FESS_ENV_.*``

::

    # Les variables d'environnement commençant par FESS_ENV_ peuvent être utilisées dans la configuration d'indexation
    crawler.data.env.param.key.pattern=^FESS_ENV_.*

Configuration de robots.txt
===============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.ignore.robots.txt``
     - Ignorer robots.txt
     - ``false``
   * - ``crawler.ignore.robots.tags``
     - Balises robots à ignorer
     - (vide)
   * - ``crawler.ignore.content.exception``
     - Ignorer les exceptions de contenu
     - ``true``

Exemple de configuration
~~~~~~

::

    # Ignorer robots.txt (non recommandé)
    crawler.ignore.robots.txt=false

    # Ignorer des balises robots spécifiques
    crawler.ignore.robots.tags=

    # Ignorer les exceptions de contenu
    crawler.ignore.content.exception=true

.. warning::
   Définir ``crawler.ignore.robots.txt=true`` peut violer
   les conditions d'utilisation du site. Soyez prudent lors de l'indexation de sites externes.

Configuration de la gestion des erreurs
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.failure.url.status.codes``
     - Codes d'état HTTP considérés comme des échecs
     - ``404``

Exemple de configuration
~~~~~~

::

    # Traiter également 403 comme une erreur en plus de 404
    crawler.failure.url.status.codes=404,403

Configuration de la surveillance système
================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.system.monitor.interval``
     - Intervalle de surveillance système (secondes)
     - ``60``

::

    # Surveillance du système toutes les 30 secondes
    crawler.system.monitor.interval=30

Configuration des threads actifs
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.hotthread.ignore_idle_threads``
     - Ignorer les threads inactifs
     - ``true``
   * - ``crawler.hotthread.interval``
     - Intervalle d'instantané
     - ``500ms``
   * - ``crawler.hotthread.snapshots``
     - Nombre d'instantanés
     - ``10``
   * - ``crawler.hotthread.threads``
     - Nombre de threads surveillés
     - ``3``
   * - ``crawler.hotthread.timeout``
     - Timeout
     - ``30s``
   * - ``crawler.hotthread.type``
     - Type de surveillance
     - ``cpu``

Exemple de configuration
~~~~~~

::

    crawler.hotthread.ignore_idle_threads=true
    crawler.hotthread.interval=500ms
    crawler.hotthread.snapshots=10
    crawler.hotthread.threads=3
    crawler.hotthread.timeout=30s
    crawler.hotthread.type=cpu

Configuration des métadonnées
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.metadata.content.excludes``
     - Métadonnées à exclure
     - ``resourceName,X-Parsed-By...``
   * - ``crawler.metadata.name.mapping``
     - Mappage des noms de métadonnées
     - ``title=title:string...``

Exemple de configuration
~~~~~~

::

    # Métadonnées à exclure
    crawler.metadata.content.excludes=resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*

    # Mappage des noms de métadonnées
    crawler.metadata.name.mapping=\
        title=title:string\n\
        Title=title:string\n\
        dc:title=title:string

Configuration du robot d'indexation HTML
===================

Configuration XPath
----------

Configuration XPath pour extraire les éléments HTML.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.html.content.xpath``
     - XPath du contenu
     - ``//BODY``
   * - ``crawler.document.html.lang.xpath``
     - XPath de la langue
     - ``//HTML/@lang``
   * - ``crawler.document.html.digest.xpath``
     - XPath du résumé
     - ``//META[@name='description']/@content``
   * - ``crawler.document.html.canonical.xpath``
     - XPath de l'URL canonique
     - ``//LINK[@rel='canonical'][1]/@href``

Exemple de configuration
~~~~~~

::

    # Configuration par défaut
    crawler.document.html.content.xpath=//BODY
    crawler.document.html.lang.xpath=//HTML/@lang
    crawler.document.html.digest.xpath=//META[@name='description']/@content
    crawler.document.html.canonical.xpath=//LINK[@rel='canonical'][1]/@href

Exemples de XPath personnalisés
~~~~~~~~~~~~~~~~~~~

::

    # Extraire uniquement un élément div spécifique comme contenu
    crawler.document.html.content.xpath=//DIV[@id='main-content']

    # Inclure également les mots-clés meta dans le résumé
    crawler.document.html.digest.xpath=//META[@name='description']/@content|//META[@name='keywords']/@content

Traitement des balises HTML
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.html.pruned.tags``
     - Balises HTML à supprimer
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
   * - ``crawler.document.html.max.digest.length``
     - Longueur maximale du résumé
     - ``120``
   * - ``crawler.document.html.default.lang``
     - Langue par défaut
     - (vide)

Exemple de configuration
~~~~~~

::

    # Ajouter des balises à supprimer
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,a[rel=nofollow],form

    # Résumé de 200 caractères
    crawler.document.html.max.digest.length=200

    # Langue par défaut en japonais
    crawler.document.html.default.lang=ja

Filtre de motifs d'URL
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.html.default.include.index.patterns``
     - Motifs d'URL à inclure dans l'index
     - (vide)
   * - ``crawler.document.html.default.exclude.index.patterns``
     - Motifs d'URL à exclure de l'index
     - ``(?i).*(css|js|jpeg...)``
   * - ``crawler.document.html.default.include.search.patterns``
     - Motifs d'URL à inclure dans les résultats de recherche
     - (vide)
   * - ``crawler.document.html.default.exclude.search.patterns``
     - Motifs d'URL à exclure des résultats de recherche
     - (vide)

Exemple de configuration
~~~~~~

::

    # Motif d'exclusion par défaut
    crawler.document.html.default.exclude.index.patterns=(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)

    # Indexer uniquement des chemins spécifiques
    crawler.document.html.default.include.index.patterns=https://example\\.com/docs/.*

Configuration du robot d'indexation de fichiers
======================

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.file.name.encoding``
     - Encodage des noms de fichiers
     - (vide)
   * - ``crawler.document.file.no.title.label``
     - Étiquette pour les fichiers sans titre
     - ``No title.``
   * - ``crawler.document.file.ignore.empty.content``
     - Ignorer le contenu vide
     - ``false``
   * - ``crawler.document.file.max.title.length``
     - Longueur maximale du titre
     - ``100``
   * - ``crawler.document.file.max.digest.length``
     - Longueur maximale du résumé
     - ``200``

Exemple de configuration
~~~~~~

::

    # Traiter les noms de fichiers en Windows-31J
    crawler.document.file.name.encoding=Windows-31J

    # Étiquette pour les fichiers sans titre
    crawler.document.file.no.title.label=Sans titre

    # Ignorer les fichiers vides
    crawler.document.file.ignore.empty.content=true

    # Longueur du titre et du résumé
    crawler.document.file.max.title.length=200
    crawler.document.file.max.digest.length=500

Traitement du contenu
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.file.append.meta.content``
     - Ajouter les métadonnées au contenu
     - ``true``
   * - ``crawler.document.file.append.body.content``
     - Ajouter le corps au contenu
     - ``true``
   * - ``crawler.document.file.default.lang``
     - Langue par défaut
     - (vide)

Exemple de configuration
~~~~~~

::

    crawler.document.file.append.meta.content=true
    crawler.document.file.append.body.content=true
    crawler.document.file.default.lang=ja

Filtre de motifs d'URL de fichiers
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.file.default.include.index.patterns``
     - Motifs à inclure dans l'index
     - (vide)
   * - ``crawler.document.file.default.exclude.index.patterns``
     - Motifs à exclure de l'index
     - (vide)
   * - ``crawler.document.file.default.include.search.patterns``
     - Motifs à inclure dans les résultats de recherche
     - (vide)
   * - ``crawler.document.file.default.exclude.search.patterns``
     - Motifs à exclure des résultats de recherche
     - (vide)

Exemple de configuration
~~~~~~

::

    # Indexer uniquement des extensions spécifiques
    crawler.document.file.default.include.index.patterns=.*\\.(pdf|docx|xlsx|pptx)$

    # Exclure le dossier temp
    crawler.document.file.default.exclude.index.patterns=.*/temp/.*

Configuration du cache
==============

Cache de documents
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``crawler.document.cache.enabled``
     - Activer le cache de documents
     - ``true``
   * - ``crawler.document.cache.max.size``
     - Taille maximale du cache (octets)
     - ``2621440`` (2,5 Mo)
   * - ``crawler.document.cache.supported.mimetypes``
     - Types MIME à mettre en cache
     - ``text/html``
   * - ``crawler.document.cache.html.mimetypes``
     - Types MIME traités comme HTML
     - ``text/html``

Exemple de configuration
~~~~~~

::

    # Activer le cache de documents
    crawler.document.cache.enabled=true

    # Taille du cache à 5 Mo
    crawler.document.cache.max.size=5242880

    # Types MIME à mettre en cache
    crawler.document.cache.supported.mimetypes=text/html,application/xhtml+xml

    # Types MIME traités comme HTML
    crawler.document.cache.html.mimetypes=text/html,application/xhtml+xml

.. note::
   L'activation du cache affiche un lien de cache dans les résultats de recherche,
   permettant aux utilisateurs de consulter le contenu au moment de l'indexation.

Options JVM
==============

Vous pouvez configurer les options JVM du processus du robot d'indexation.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``jvm.crawler.options``
     - Options JVM du robot d'indexation
     - ``-Xms128m -Xmx512m...``

Configuration par défaut
--------------

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000 \
        -XX:-HeapDumpOnOutOfMemoryError

Description des principales options
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Option
     - Description
   * - ``-Xms128m``
     - Taille initiale du tas (128 Mo)
   * - ``-Xmx512m``
     - Taille maximale du tas (512 Mo)
   * - ``-XX:MaxMetaspaceSize=128m``
     - Taille maximale du Metaspace (128 Mo)
   * - ``-XX:+UseG1GC``
     - Utiliser le collecteur de déchets G1
   * - ``-XX:MaxGCPauseMillis=60000``
     - Objectif de temps de pause GC (60 secondes)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Désactiver le vidage du tas en cas d'OutOfMemory

Exemples de configuration personnalisée
--------------

**Pour indexer des fichiers volumineux :**

::

    jvm.crawler.options=-Xms256m -Xmx2g \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000

**Lors du débogage :**

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:+HeapDumpOnOutOfMemoryError \
        -XX:HeapDumpPath=/tmp/crawler_dump.hprof

Consultez :doc:`setup-memory` pour plus de détails.

Optimisation des performances
==========================

Optimisation de la vitesse d'indexation
--------------------

**1. Ajustement du nombre de threads**

Vous pouvez améliorer la vitesse d'indexation en augmentant le nombre d'indexations parallèles.

::

    # Ajuster le nombre de threads dans la configuration d'indexation de l'interface d'administration
    Nombre de threads : 10

Cependant, faites attention à la charge sur le serveur cible.

**2. Ajustement des timeouts**

Pour les sites à réponse lente, ajustez les timeouts.

::

    # Ajouter aux « Paramètres de configuration » de la configuration d'indexation
    client.connectionTimeout=10000
    client.socketTimeout=30000

**3. Exclusion du contenu inutile**

La vitesse d'indexation s'améliore en excluant les images, CSS, fichiers JavaScript, etc.

::

    # Motif d'URL d'exclusion
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. Configuration de nouvelle tentative**

Ajustez le nombre de nouvelles tentatives et l'intervalle en cas d'erreur.

::

    # Ajouter aux « Paramètres de configuration » de la configuration d'indexation
    client.maxRetry=3
    client.retryInterval=1000

Optimisation de l'utilisation de la mémoire
--------------------

**1. Ajustement de la taille du tas**

::

    jvm.crawler.options=-Xms256m -Xmx1g

**2. Ajustement de la taille du cache**

::

    crawler.document.cache.max.size=1048576  # 1 Mo

**3. Exclusion des fichiers volumineux**

::

    # Ajouter aux « Paramètres de configuration » de la configuration d'indexation
    client.maxContentLength=10485760  # 10 Mo

Consultez :doc:`setup-memory` pour plus de détails.

Amélioration de la qualité de l'index
----------------------

**1. Optimisation du XPath**

Excluez les éléments inutiles (navigation, publicités, etc.).

::

    crawler.document.html.content.xpath=//DIV[@id='main-content']
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,form,iframe

**2. Optimisation du résumé**

::

    crawler.document.html.max.digest.length=200

**3. Mappage des métadonnées**

::

    crawler.metadata.name.mapping=\
        title=title:string\n\
        description=digest:string\n\
        keywords=label:string

Dépannage
======================

Mémoire insuffisante
----------

**Symptômes :**

- ``OutOfMemoryError`` est enregistré dans ``fess_crawler.log``
- L'indexation s'arrête en cours de route

**Solutions :**

1. Augmenter la taille du tas du robot d'indexation

   ::

       jvm.crawler.options=-Xms256m -Xmx2g

2. Réduire le nombre de threads parallèles

3. Exclure les fichiers volumineux

Consultez :doc:`setup-memory` pour plus de détails.

L'indexation est lente
--------------

**Symptômes :**

- L'indexation prend trop de temps
- Les timeouts se produisent fréquemment

**Solutions :**

1. Augmenter le nombre de threads (attention à la charge sur le serveur cible)

2. Ajuster les timeouts

   ::

       client.connectionTimeout=5000
       client.socketTimeout=10000

3. Exclure les URLs inutiles

Impossible d'extraire un contenu spécifique
------------------------------

**Symptômes :**

- Le texte de la page n'est pas extrait correctement
- Les informations importantes ne sont pas incluses dans les résultats de recherche

**Solutions :**

1. Vérifier et ajuster le XPath

   ::

       crawler.document.html.content.xpath=//DIV[@class='content']

2. Vérifier les balises supprimées

   ::

       crawler.document.html.pruned.tags=script,style

3. Pour le contenu généré dynamiquement par JavaScript, envisagez une autre méthode (indexation API, etc.)

Des caractères corrompus apparaissent
------------------

**Symptômes :**

- Des caractères corrompus apparaissent dans les résultats de recherche
- Certaines langues ne s'affichent pas correctement

**Solutions :**

1. Vérifier les paramètres d'encodage

   ::

       crawler.document.site.encoding=UTF-8
       crawler.crawling.data.encoding=UTF-8

2. Configurer l'encodage des noms de fichiers

   ::

       crawler.document.file.name.encoding=Windows-31J

3. Vérifier les erreurs d'encodage dans les journaux

   ::

       grep -i "encoding" /var/log/fess/fess_crawler.log

Bonnes pratiques
==================

1. **Valider dans un environnement de test**

   Avant d'appliquer en production, validez suffisamment dans un environnement de test.

2. **Ajustement progressif**

   Ne modifiez pas les paramètres de manière importante en une seule fois, ajustez progressivement et vérifiez les effets.

3. **Surveillance des journaux**

   Après avoir modifié les paramètres, surveillez les journaux pour vérifier qu'il n'y a pas d'erreurs ou de problèmes de performance.

   ::

       tail -f /var/log/fess/fess_crawler.log

4. **Sauvegarde**

   Avant de modifier les fichiers de configuration, effectuez toujours une sauvegarde.

   ::

       cp /etc/fess/fess_config.properties /etc/fess/fess_config.properties.bak

5. **Documentation**

   Documentez les paramètres modifiés et leur raison.

Configuration du crawler S3/GCS
===============================

Crawler S3
----------

Configuration pour crawler S3 et le stockage compatible S3 (comme MinIO).
Ajoutez ce qui suit aux « Paramètres de configuration » dans les paramètres de crawl de fichiers.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Paramètre
     - Description
     - Par défaut
   * - ``client.endpoint``
     - URL du point de terminaison S3
     - (Obligatoire)
   * - ``client.accessKey``
     - Clé d'accès
     - (Obligatoire)
   * - ``client.secretKey``
     - Clé secrète
     - (Obligatoire)
   * - ``client.region``
     - Région AWS
     - ``us-east-1``
   * - ``client.connectTimeout``
     - Délai de connexion (ms)
     - ``10000``
   * - ``client.readTimeout``
     - Délai de lecture (ms)
     - ``10000``

Exemple de configuration
~~~~~~~~~~~~~~~~~~~~~~~~

::

    client.endpoint=https://s3.ap-northeast-1.amazonaws.com
    client.accessKey=AKIAIOSFODNN7EXAMPLE
    client.secretKey=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    client.region=ap-northeast-1

Crawler GCS
-----------

Configuration pour crawler Google Cloud Storage.
Ajoutez ce qui suit aux « Paramètres de configuration » dans les paramètres de crawl de fichiers.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Paramètre
     - Description
     - Par défaut
   * - ``client.projectId``
     - ID de projet Google Cloud
     - (Obligatoire)
   * - ``client.credentialsFile``
     - Chemin du fichier JSON du compte de service
     - (Optionnel)
   * - ``client.endpoint``
     - Point de terminaison personnalisé
     - (Optionnel)
   * - ``client.connectTimeout``
     - Délai de connexion (ms)
     - ``10000``
   * - ``client.writeTimeout``
     - Délai d'écriture (ms)
     - ``10000``
   * - ``client.readTimeout``
     - Délai de lecture (ms)
     - ``10000``

Exemple de configuration
~~~~~~~~~~~~~~~~~~~~~~~~

::

    client.projectId=mon-projet-gcp
    client.credentialsFile=/etc/fess/gcs-credentials.json

.. note::
   Si ``credentialsFile`` est omis, la variable d'environnement ``GOOGLE_APPLICATION_CREDENTIALS`` est utilisée.

Informations de référence
=========================

- :doc:`crawler-basic` - Configuration de base du robot d'indexation
- :doc:`crawler-thumbnail` - Configuration des vignettes
- :doc:`setup-memory` - Configuration de la mémoire
- :doc:`admin-logging` - Configuration des journaux
- :doc:`search-advanced` - Configuration de recherche avancée
