==================================
Connecteur Elasticsearch/OpenSearch
==================================

Apercu
====

Le connecteur Elasticsearch/OpenSearch fournit la fonctionnalite permettant de recuperer des donnees
a partir d'un cluster Elasticsearch ou OpenSearch et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-elasticsearch``.

Versions prises en charge
==============

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

Prerequis
========

1. L'installation du plugin est requise
2. L'acces en lecture au cluster Elasticsearch/OpenSearch est necessaire
3. Les droits d'execution de requetes sont necessaires

Installation du plugin
------------------------

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
========

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple
   * - Nom
     - External Elasticsearch
   * - Nom du gestionnaire
     - ElasticsearchDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

Connexion de base :

::

    hosts=http://localhost:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

Connexion avec authentification :

::

    hosts=https://elasticsearch.example.com:9200
    index=myindex
    username=elastic
    password=changeme
    scroll_size=100
    scroll_timeout=5m

Configuration multi-hotes :

::

    hosts=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``hosts``
     - Oui
     - Hotes Elasticsearch/OpenSearch (plusieurs hotes separes par des virgules)
   * - ``index``
     - Oui
     - Nom de l'index cible
   * - ``username``
     - Non
     - Nom d'utilisateur pour l'authentification
   * - ``password``
     - Non
     - Mot de passe pour l'authentification
   * - ``scroll_size``
     - Non
     - Nombre d'elements recuperes lors du scroll (par defaut : 100)
   * - ``scroll_timeout``
     - Non
     - Timeout du scroll (par defaut : 5m)
   * - ``query``
     - Non
     - JSON de requete (par defaut : match_all)
   * - ``fields``
     - Non
     - Champs a recuperer (separes par des virgules)

Configuration du script
--------------

Mapping de base :

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Acces aux champs imbriques :

::

    url=data.metadata.url
    title=data.title
    content=data.body.content
    author=data.author.name
    created=data.created_at
    last_modified=data.updated_at

Champs disponibles
~~~~~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - Champ du document Elasticsearch
- ``data._id`` - ID du document
- ``data._index`` - Nom de l'index
- ``data._type`` - Type de document (Elasticsearch < 7)
- ``data._score`` - Score de recherche

Configuration des requetes
============

Recuperation de tous les documents
--------------------

Par defaut, tous les documents sont recuperes.
Si le parametre ``query`` n'est pas specifie, ``match_all`` est utilise.

Filtrage par conditions specifiques
--------------------------

::

    query={"query":{"term":{"status":"published"}}}

Specification de plage :

::

    query={"query":{"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}}

Conditions multiples :

::

    query={"query":{"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}}

Specification de tri :

::

    query={"query":{"match_all":{}},"sort":[{"timestamp":{"order":"desc"}}]}

Recuperation de champs specifiques uniquement
========================

Limitation des champs avec le parametre fields
----------------------------------------

::

    hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    scroll_size=100

Pour recuperer tous les champs, ne specifiez pas ``fields`` ou laissez-le vide.

Exemples d'utilisation
======

Crawl d'un index de base
------------------------------

Parametres :

::

    hosts=http://localhost:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

Script :

::

    url=data.url
    title=data.title
    content=data.content
    created=data.created_at
    last_modified=data.updated_at

Crawl d'un cluster avec authentification
------------------------------

Parametres :

::

    hosts=https://es.example.com:9200
    index=products
    username=elastic
    password=changeme
    scroll_size=200
    scroll_timeout=10m

Script :

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " " + data.specifications
    digest=data.category
    last_modified=data.updated_at

Crawl de plusieurs index
------------------------------

Parametres :

::

    hosts=http://localhost:9200
    index=logs-2024-*
    query={"query":{"term":{"level":"error"}}}
    scroll_size=100

Script :

::

    url="https://logs.example.com/view/" + data._id
    title=data.message
    content=data.stack_trace
    digest=data.service + " - " + data.level
    last_modified=data.timestamp

Crawl d'un cluster OpenSearch
----------------------------

Parametres :

::

    hosts=https://opensearch.example.com:9200
    index=documents
    username=admin
    password=admin
    scroll_size=100
    scroll_timeout=5m

Script :

::

    url=data.url
    title=data.title
    content=data.body
    last_modified=data.modified_date

Crawl avec limitation de champs
----------------------------

Parametres :

::

    hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    scroll_size=100

Script :

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Repartition de charge multi-hotes
----------------------

Parametres :

::

    hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

Script :

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Depannage
======================

Erreur de connexion
----------

**Symptome** : ``Connection refused`` ou ``No route to host``

**Points a verifier** :

1. Verifier si l'URL de l'hote est correcte (protocole, nom d'hote, port)
2. Verifier si Elasticsearch/OpenSearch est en cours d'execution
3. Verifier les parametres du pare-feu
4. Pour HTTPS, verifier si le certificat est valide

Erreur d'authentification
----------

**Symptome** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points a verifier** :

1. Verifier si le nom d'utilisateur et le mot de passe sont corrects
2. Verifier si l'utilisateur a les droits appropries :

   - Droits de lecture sur l'index
   - Droits d'utilisation de l'API scroll

3. Si Elasticsearch Security (X-Pack) est active, verifier la configuration

Index introuvable
--------------------------

**Symptome** : ``index_not_found_exception``

**Points a verifier** :

1. Verifier si le nom de l'index est correct (incluant la casse)
2. Verifier si l'index existe :

   ::

       GET /_cat/indices

3. Verifier si le pattern wildcard est correct (ex: ``logs-*``)

Erreur de requete
------------

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
----------------------

**Symptome** : ``No search context found`` ou ``Scroll timeout``

**Solution** :

1. Augmenter ``scroll_timeout`` :

   ::

       scroll_timeout=10m

2. Reduire ``scroll_size`` :

   ::

       scroll_size=50

3. Verifier les ressources du cluster

Crawl de donnees volumineuses
--------------------

**Symptome** : Le crawl est lent ou expire

**Solution** :

1. Ajuster ``scroll_size`` (trop grand le ralentit) :

   ::

       scroll_size=100  # Par defaut
       scroll_size=500  # Plus grand

2. Limiter les champs recuperes avec ``fields``
3. Filtrer les documents necessaires avec ``query``
4. Diviser en plusieurs data stores (par index, par periode, etc.)

Memoire insuffisante
----------

**Symptome** : OutOfMemoryError

**Solution** :

1. Reduire ``scroll_size``
2. Limiter les champs recuperes avec ``fields``
3. Augmenter la taille du tas de |Fess|
4. Exclure les champs volumineux (donnees binaires, etc.)

Connexion SSL/TLS
===========

Cas de certificat auto-signe
--------------------

.. warning::
   Utilisez des certificats signes de maniere appropriee en environnement de production.

Pour utiliser des certificats auto-signes, ajoutez le certificat au keystore Java :

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Authentification par certificat client
----------------------

Si un certificat client est necessaire, des parametres supplementaires sont requis.
Consultez la documentation du client Elasticsearch pour plus de details.

Exemples de requetes avancees
==============

Requete avec agregation
----------------

.. note::
   Les resultats d'agregation ne sont pas recuperes, seuls les documents sont recuperes.

::

    query={"query":{"match_all":{}},"aggs":{"categories":{"terms":{"field":"category"}}}}

Champs de script
--------------------

::

    query={"query":{"match_all":{}},"script_fields":{"full_url":{"script":"doc['protocol'].value + '://' + doc['host'].value + doc['path'].value"}}}

Script :

::

    url=data.full_url
    title=data.title
    content=data.content

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
