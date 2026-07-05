=====================================
Connecteur Elasticsearch/OpenSearch
=====================================

Apercu
======

Le connecteur Elasticsearch/OpenSearch fournit la fonctionnalite permettant de recuperer des donnees
a partir d'un cluster Elasticsearch ou OpenSearch et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-elasticsearch``.

Versions prises en charge
=========================

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

Prerequis
=========

1. L'installation du plugin est requise
2. L'acces en lecture au cluster Elasticsearch/OpenSearch est necessaire
3. Les droits d'execution de requetes sont necessaires

Installation du plugin
----------------------

Methode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # Placement
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2 : Installation depuis l'interface d'administration

1. Ouvrir "Systeme" -> "Plugins"
2. Telecharger le fichier JAR
3. Redemarrer |Fess|

Configuration
=============

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple
   * - Nom
     - External Elasticsearch
   * - Nom du gestionnaire
     - ElasticsearchDataStore / ElasticsearchListDataStore
   * - Active
     - Oui

.. note::
   ``ElasticsearchListDataStore`` est un gestionnaire qui etend ``ElasticsearchDataStore``. Il traite les donnees recuperees sous forme de liste de fichiers et prend en charge l'indexation multi-thread.
   Le nombre de threads peut etre specifie avec le parametre ``numOfThreads`` (par defaut : 1).

Configuration des parametres
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

Liste des parametres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``settings.http.hosts``
     - Non
     - URL des hotes Elasticsearch/OpenSearch. Plusieurs hotes peuvent etre specifies en les separant par des virgules (ex : ``http://host1:9200,http://host2:9200``). Une erreur de connexion se produit si non specifie
   * - ``settings.fesen.username``
     - Non
     - Nom d'utilisateur pour l'authentification
   * - ``settings.fesen.password``
     - Non
     - Mot de passe pour l'authentification
   * - ``index``
     - Non
     - Nom de l'index cible (par defaut : ``_all``). Plusieurs index peuvent etre specifies en les separant par des virgules
   * - ``size``
     - Non
     - Nombre d'elements recuperes lors du scroll (si non specifie, la valeur par defaut du serveur Elasticsearch/OpenSearch est utilisee)
   * - ``scroll``
     - Non
     - Timeout du scroll (par defaut : 1m)
   * - ``timeout``
     - Non
     - Timeout de la requete (par defaut : 1m)
   * - ``query``
     - Non
     - JSON de requete (par defaut : match_all). Specifier uniquement le corps de la requete (le wrapper externe ``{"query":...}`` n'est pas necessaire)
   * - ``fields``
     - Non
     - Champs a recuperer (separes par des virgules)
   * - ``preference``
     - Non
     - Preference de replique de shard pour l'execution de la recherche (par defaut : ``_local``)
   * - ``delete.processed.doc``
     - Non
     - Supprimer les documents traites de l'index source (par defaut : false)
   * - ``readInterval``
     - Non
     - Temps d'attente entre le traitement de chaque document en millisecondes (par defaut : 0)
   * - ``numOfThreads``
     - Non
     - Nombre de threads pour l'indexation (valide uniquement pour ``ElasticsearchListDataStore``, par defaut : 1)

Parametres de connexion supplementaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les parametres prefixes par ``settings.`` sont transmis comme configuration du client HTTP Elasticsearch/OpenSearch interne (client HTTP fesen).
Les principaux parametres supplementaires sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Parametre
     - Description
   * - ``settings.http.ssl.certificate_authorities``
     - Chemin du fichier de certificat CA de confiance (format X.509) pour les connexions HTTPS
   * - ``settings.http.compression``
     - Activer la compression HTTP (par defaut : true)
   * - ``settings.http.proxy_host``
     - Nom d'hote du serveur proxy (``settings.https.proxy_host`` est egalement accepte)
   * - ``settings.http.proxy_port``
     - Numero de port du serveur proxy (``settings.https.proxy_port`` est egalement accepte)
   * - ``settings.http.proxy_username``
     - Nom d'utilisateur pour l'authentification proxy (``settings.https.proxy_username`` est egalement accepte)
   * - ``settings.http.proxy_password``
     - Mot de passe pour l'authentification proxy (``settings.https.proxy_password`` est egalement accepte)

Configuration du script
-----------------------

Mapping de base :

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Acces aux champs imbriques :

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
- ``seqNo`` - Numero de sequence
- ``primaryTerm`` - Terme primaire
- ``clusterAlias`` - Alias du cluster (pour la recherche inter-clusters)
- ``hit`` - Objet SearchHit (utilisation avancee)

Configuration des requetes
==========================

Recuperation de tous les documents
------------------------------------

Par defaut, tous les documents sont recuperes.
Si le parametre ``query`` n'est pas specifie, ``match_all`` est utilise.

Filtrage par conditions specifiques
------------------------------------

::

    query={"term":{"status":"published"}}

Specification de plage :

::

    query={"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}

Conditions multiples :

::

    query={"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}

.. note::
   Le parametre ``query`` n'accepte que le corps de la requete. Le wrapper externe ``{"query":...}`` n'est pas necessaire.
   Les options de niveau recherche telles que le tri ne peuvent pas etre specifiees dans ce parametre.

Recuperation de champs specifiques uniquement
=============================================

Limitation des champs avec le parametre fields
-----------------------------------------------

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    size=100

Pour recuperer tous les champs, ne specifiez pas ``fields`` ou laissez-le vide.

Exemples d'utilisation
======================

Crawl d'un index de base
-------------------------

Parametres :

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

Parametres :

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

Parametres :

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

Parametres :

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

Parametres :

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

Repartition de charge multi-hotes
-----------------------------------

En specifiant plusieurs hotes separes par des virgules dans ``settings.http.hosts``, les requetes sont distribuees entre chaque hote.

Parametres :

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

Depannage
=========

Erreur de connexion
--------------------

**Symptome** : ``Connection refused`` ou ``No route to host``

**Points a verifier** :

1. Verifier si l'URL de l'hote est correcte (protocole, nom d'hote, port)
2. Verifier si Elasticsearch/OpenSearch est en cours d'execution
3. Verifier les parametres du pare-feu
4. Pour HTTPS, verifier si le certificat est valide

Erreur d'authentification
--------------------------

**Symptome** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points a verifier** :

1. Verifier si le nom d'utilisateur et le mot de passe sont corrects
2. Verifier si l'utilisateur a les droits appropries :

   - Droits de lecture sur l'index
   - Droits d'utilisation de l'API scroll

3. Si Elasticsearch Security (X-Pack) est active, verifier si la configuration est correcte

Index introuvable
------------------

**Symptome** : ``index_not_found_exception``

**Points a verifier** :

1. Verifier si le nom de l'index est correct (incluant la casse)
2. Verifier si l'index existe :

   ::

       GET /_cat/indices

3. Verifier si le pattern wildcard est correct (ex : ``logs-*``)

Erreur de requete
------------------

**Symptome** : ``parsing_exception`` ou ``search_phase_execution_exception``

**Points a verifier** :

1. Verifier si le JSON de la requete est correct
2. Verifier si la requete est compatible avec la version d'Elasticsearch/OpenSearch
3. Verifier si les noms de champs sont corrects
4. Tester la requete directement sur Elasticsearch/OpenSearch :

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

Timeout du scroll
------------------

**Symptome** : ``No search context found`` ou ``Scroll timeout``

**Solution** :

1. Augmenter ``scroll`` :

   ::

       scroll=10m

2. Reduire ``size`` :

   ::

       size=50

3. Verifier les ressources du cluster

Crawl de donnees volumineuses
------------------------------

**Symptome** : Le crawl est lent ou expire

**Solution** :

1. Ajuster ``size`` (trop grand le ralentit) :

   ::

       size=100
       size=500  # Plus grand

2. Limiter les champs recuperes avec ``fields``
3. Filtrer les documents necessaires avec ``query``
4. Diviser en plusieurs data stores (par index, par periode, etc.)

Memoire insuffisante
---------------------

**Symptome** : OutOfMemoryError

**Solution** :

1. Reduire ``size``
2. Limiter les champs recuperes avec ``fields``
3. Augmenter la taille du tas de |Fess|
4. Exclure les champs volumineux (donnees binaires, etc.)

Connexion SSL/TLS
=================

Cas de certificat auto-signe
------------------------------

.. warning::
   Utilisez des certificats signes de maniere appropriee en environnement de production.

Methode 1 : Specifier le certificat CA avec le parametre ``settings.http.ssl.certificate_authorities`` (recommande)

Indiquez le chemin du fichier de certificat CA de confiance (format X.509). Cette methode n'affecte pas le keystore global de |Fess|.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.ssl.certificate_authorities=/path/to/es-cert.crt
    index=myindex

Methode 2 : Ajouter le certificat au keystore Java

Ajoutez le certificat au trust store de la JVM qui demarre |Fess|.

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Connexion via un proxy
-----------------------

Pour se connecter via un serveur proxy, specifiez ``settings.http.proxy_host`` et ``settings.http.proxy_port``.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.proxy_host=proxy.example.com
    settings.http.proxy_port=8080
    index=myindex

Exemples de requetes avancees
==============================

Requete avec agregation
------------------------

.. note::
   Le parametre ``query`` n'accepte que le corps de la requete. Les agregations (aggs), le tri et autres
   options de niveau recherche ne peuvent pas etre specifies. Seuls les documents sont recuperes.

Champs de script
-----------------

.. note::
   Les champs de script Elasticsearch/OpenSearch ne sont pas inclus dans ``_source`` et ne peuvent donc pas
   etre accedes via le prefixe ``source.*``. Pour utiliser les champs de script, accedez-y via l'objet
   ``hit`` en utilisant ``hit.getFields()``.

Informations de reference
==========================

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
