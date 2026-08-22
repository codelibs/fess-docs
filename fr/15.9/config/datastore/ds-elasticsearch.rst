=====================================
Connecteur Elasticsearch/OpenSearch
=====================================

Aperçu
======

Le connecteur Elasticsearch/OpenSearch fournit la fonctionnalité permettant de récupérer des données
à partir d'un cluster Elasticsearch ou OpenSearch et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-elasticsearch``.

Versions prises en charge
=========================

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

Prérequis
=========

1. L'installation du plugin est requise
2. L'accès en lecture au cluster Elasticsearch/OpenSearch est nécessaire
3. Les droits d'exécution de requêtes sont nécessaires

Installation du plugin
----------------------

Méthode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # Placement
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Méthode 2 : Installation depuis l'interface d'administration

1. Ouvrir "Système" -> "Plugins"
2. Télécharger le fichier JAR
3. Redémarrer |Fess|

Configuration
=============

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - External Elasticsearch
   * - Nom du gestionnaire
     - ElasticsearchDataStore / ElasticsearchListDataStore
   * - Active
     - Oui

.. note::
   ``ElasticsearchListDataStore`` est un gestionnaire qui étend ``ElasticsearchDataStore``. Il traite les données récupérées sous forme de liste de fichiers et prend en charge l'indexation multi-thread.
   Le nombre de threads peut être spécifié avec le paramètre ``numOfThreads`` (par défaut : 1).

Configuration des paramètres
-----------------------------

Connexion de base :

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    size=100
    scroll=1m

Connexion avec authentification :

::

    settings.http.hosts=https://elasticsearch.example.com:9200
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    index=myindex
    size=100
    scroll=1m

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``settings.http.hosts``
     - Non
     - URL des hôtes Elasticsearch/OpenSearch. Plusieurs hôtes peuvent être spécifiés en les séparant par des virgules (ex : ``http://host1:9200,http://host2:9200``). Une erreur de connexion se produit si non spécifié
   * - ``settings.fesen.username``
     - Non
     - Nom d'utilisateur pour l'authentification
   * - ``settings.fesen.password``
     - Non
     - Mot de passe pour l'authentification
   * - ``index``
     - Non
     - Nom de l'index cible (par défaut : ``_all``). Plusieurs index peuvent être spécifiés en les séparant par des virgules
   * - ``size``
     - Non
     - Nombre d'éléments récupérés lors du scroll (si non spécifié, la valeur par défaut du serveur Elasticsearch/OpenSearch est utilisée)
   * - ``scroll``
     - Non
     - Timeout du scroll (par défaut : 1m)
   * - ``timeout``
     - Non
     - Timeout de la requête (par défaut : 1m)
   * - ``query``
     - Non
     - JSON de requête (par défaut : match_all). Spécifier uniquement le corps de la requête (le wrapper externe ``{"query":...}`` n'est pas nécessaire)
   * - ``fields``
     - Non
     - Champs à récupérer (séparés par des virgules)
   * - ``preference``
     - Non
     - Préférence de réplique de shard pour l'exécution de la recherche (par défaut : ``_local``)
   * - ``delete.processed.doc``
     - Non
     - Supprimer les documents traités de l'index source (par défaut : false)
   * - ``readInterval``
     - Non
     - Temps d'attente entre le traitement de chaque document en millisecondes (par défaut : 0)
   * - ``numOfThreads``
     - Non
     - Nombre de threads pour l'indexation (valide uniquement pour ``ElasticsearchListDataStore``, par défaut : 1)

Paramètres de connexion supplémentaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les paramètres préfixés par ``settings.`` sont transmis comme configuration du client HTTP Elasticsearch/OpenSearch interne (client HTTP fesen).
Les principaux paramètres supplémentaires sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Paramètre
     - Description
   * - ``settings.http.ssl.certificate_authorities``
     - Chemin du fichier de certificat CA de confiance (format X.509) pour les connexions HTTPS
   * - ``settings.http.compression``
     - Activer la compression HTTP (par défaut : true)
   * - ``settings.http.proxy_host``
     - Nom d'hôte du serveur proxy (``settings.https.proxy_host`` est également accepté)
   * - ``settings.http.proxy_port``
     - Numéro de port du serveur proxy (``settings.https.proxy_port`` est également accepté)
   * - ``settings.http.proxy_username``
     - Nom d'utilisateur pour l'authentification proxy (``settings.https.proxy_username`` est également accepté)
   * - ``settings.http.proxy_password``
     - Mot de passe pour l'authentification proxy (``settings.https.proxy_password`` est également accepté)

Configuration du script
-----------------------

Mapping de base :

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Accès aux champs imbriqués :

::

    url=source.metadata.url
    title=source.title
    content=source.body.content
    author=source.author.name
    created=source.created_at
    last_modified=source.updated_at

Champs disponibles
~~~~~~~~~~~~~~~~~~

- ``source.<field_name>`` - Champ ``_source`` du document Elasticsearch
- ``id`` - ID du document
- ``index`` - Nom de l'index
- ``score`` - Score de recherche
- ``version`` - Version du document
- ``seqNo`` - Numéro de séquence
- ``primaryTerm`` - Terme primaire
- ``clusterAlias`` - Alias du cluster (pour la recherche inter-clusters)
- ``hit`` - Objet SearchHit (utilisation avancée)

Configuration des requêtes
==========================

Récupération de tous les documents
------------------------------------

Par défaut, tous les documents sont récupérés.
Si le paramètre ``query`` n'est pas spécifié, ``match_all`` est utilisé.

Filtrage par conditions spécifiques
------------------------------------

::

    query={"term":{"status":"published"}}

Spécification de plage :

::

    query={"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}

Conditions multiples :

::

    query={"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}

.. note::
   Le paramètre ``query`` n'accepte que le corps de la requête. Le wrapper externe ``{"query":...}`` n'est pas nécessaire.
   Les options de niveau recherche telles que le tri ne peuvent pas être spécifiées dans ce paramètre.

Récupération de champs spécifiques uniquement
=============================================

Limitation des champs avec le paramètre fields
-----------------------------------------------

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    size=100

Pour récupérer tous les champs, ne spécifiez pas ``fields`` ou laissez-le vide.

Exemples d'utilisation
======================

Crawl d'un index de base
-------------------------

Paramètres :

::

    settings.http.hosts=http://localhost:9200
    index=articles
    size=100
    scroll=1m

Script :

::

    url=source.url
    title=source.title
    content=source.content
    created=source.created_at
    last_modified=source.updated_at

Crawl d'un cluster avec authentification
-----------------------------------------

Paramètres :

::

    settings.http.hosts=https://es.example.com:9200
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    index=products
    size=200
    scroll=10m

Script :

::

    url="https://shop.example.com/product/" + source.product_id
    title=source.name
    content=source.description + " " + source.specifications
    digest=source.category
    last_modified=source.updated_at

Crawl de plusieurs index
--------------------------

Paramètres :

::

    settings.http.hosts=http://localhost:9200
    index=logs-2024-*
    query={"term":{"level":"error"}}
    size=100

Script :

::

    url="https://logs.example.com/view/" + id
    title=source.message
    content=source.stack_trace
    digest=source.service + " - " + source.level
    last_modified=source.timestamp

Crawl d'un cluster OpenSearch
-------------------------------

Paramètres :

::

    settings.http.hosts=https://opensearch.example.com:9200
    settings.fesen.username=admin
    settings.fesen.password=admin
    index=documents
    size=100
    scroll=1m

Script :

::

    url=source.url
    title=source.title
    content=source.body
    last_modified=source.modified_date

Crawl avec limitation de champs
---------------------------------

Paramètres :

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    size=100

Script :

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Répartition de charge multi-hôtes
-----------------------------------

En spécifiant plusieurs hôtes séparés par des virgules dans ``settings.http.hosts``, les requêtes sont distribuées entre chaque hôte.

Paramètres :

::

    settings.http.hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    size=100
    scroll=1m

Script :

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Dépannage
=========

Erreur de connexion
--------------------

**Symptôme** : ``Connection refused`` ou ``No route to host``

**Points à vérifier** :

1. Vérifier si l'URL de l'hôte est correcte (protocole, nom d'hôte, port)
2. Vérifier si Elasticsearch/OpenSearch est en cours d'exécution
3. Vérifier les paramètres du pare-feu
4. Pour HTTPS, vérifier si le certificat est valide

Erreur d'authentification
--------------------------

**Symptôme** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points à vérifier** :

1. Vérifier si le nom d'utilisateur et le mot de passe sont corrects
2. Vérifier si l'utilisateur a les droits appropriés :

   - Droits de lecture sur l'index
   - Droits d'utilisation de l'API scroll

3. Si Elasticsearch Security (X-Pack) est activé, vérifier si la configuration est correcte

Index introuvable
------------------

**Symptôme** : ``index_not_found_exception``

**Points à vérifier** :

1. Vérifier si le nom de l'index est correct (incluant la casse)
2. Vérifier si l'index existe :

   ::

       GET /_cat/indices

3. Vérifier si le pattern wildcard est correct (ex : ``logs-*``)

Erreur de requête
------------------

**Symptôme** : ``parsing_exception`` ou ``search_phase_execution_exception``

**Points à vérifier** :

1. Vérifier si le JSON de la requête est correct
2. Vérifier si la requête est compatible avec la version d'Elasticsearch/OpenSearch
3. Vérifier si les noms de champs sont corrects
4. Tester la requête directement sur Elasticsearch/OpenSearch :

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

Timeout du scroll
------------------

**Symptôme** : ``No search context found`` ou ``Scroll timeout``

**Solution** :

1. Augmenter ``scroll`` :

   ::

       scroll=10m

2. Réduire ``size`` :

   ::

       size=50

3. Vérifier les ressources du cluster

Crawl de données volumineuses
------------------------------

**Symptôme** : Le crawl est lent ou expire

**Solution** :

1. Ajuster ``size`` (trop grand le ralentit) :

   ::

       size=100
       size=500  # Plus grand

2. Limiter les champs récupérés avec ``fields``
3. Filtrer les documents nécessaires avec ``query``
4. Diviser en plusieurs data stores (par index, par période, etc.)

Mémoire insuffisante
---------------------

**Symptôme** : OutOfMemoryError

**Solution** :

1. Réduire ``size``
2. Limiter les champs récupérés avec ``fields``
3. Augmenter la taille du tas de |Fess|
4. Exclure les champs volumineux (données binaires, etc.)

Connexion SSL/TLS
=================

Cas de certificat auto-signé
------------------------------

.. warning::
   Utilisez des certificats signés de manière appropriée en environnement de production.

Méthode 1 : Spécifier le certificat CA avec le paramètre ``settings.http.ssl.certificate_authorities`` (recommandé)

Indiquez le chemin du fichier de certificat CA de confiance (format X.509). Cette méthode n'affecte pas le keystore global de |Fess|.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.ssl.certificate_authorities=/path/to/es-cert.crt
    index=myindex

Méthode 2 : Ajouter le certificat au keystore Java

Ajoutez le certificat au trust store de la JVM qui démarre |Fess|.

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Connexion via un proxy
-----------------------

Pour se connecter via un serveur proxy, spécifiez ``settings.http.proxy_host`` et ``settings.http.proxy_port``.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.proxy_host=proxy.example.com
    settings.http.proxy_port=8080
    index=myindex

Exemples de requêtes avancées
==============================

Requête avec agrégation
------------------------

.. note::
   Le paramètre ``query`` n'accepte que le corps de la requête. Les agrégations (aggs), le tri et autres
   options de niveau recherche ne peuvent pas être spécifiés. Seuls les documents sont récupérés.

Champs de script
-----------------

.. note::
   Les champs de script Elasticsearch/OpenSearch ne sont pas inclus dans ``_source`` et ne peuvent donc pas
   être accédés via le préfixe ``source.*``. Pour utiliser les champs de script, accédez-y via l'objet
   ``hit`` en utilisant ``hit.getFields()``.

Informations de référence
==========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-database` - Connecteur de base de données
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
