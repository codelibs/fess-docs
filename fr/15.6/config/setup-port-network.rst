======================
Configuration du port et du réseau
======================

Vue d'ensemble
====

Cette section décrit les paramètres liés au réseau de |Fess|.
Elle couvre les paramètres relatifs aux connexions réseau, tels que la modification des numéros de port, la configuration du proxy et les paramètres de communication HTTP.

Configuration des ports utilisés
================

Ports par défaut
----------------

|Fess| utilise les ports suivants par défaut.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Service
     - Numéro de port
   * - Application web Fess
     - 8080
   * - OpenSearch (HTTP)
     - 9201
   * - OpenSearch (Transport)
     - 9301

Modification du port de l'application web Fess
--------------------------------------

Configuration sous Linux
~~~~~~~~~~~~~~~~~

Pour modifier le numéro de port sous Linux, éditez ``bin/fess.in.sh``.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

Par exemple, pour utiliser le port 80 :

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=80"

.. note::
   Pour utiliser un numéro de port inférieur ou égal à 1024, vous devez disposer des privilèges root ou d'une configuration de privilèges appropriée (CAP_NET_BIND_SERVICE).

Configuration par variable d'environnement
~~~~~~~~~~~~~~~~~~

Vous pouvez également spécifier le numéro de port via une variable d'environnement.

::

    export FESS_PORT=8080

.. warning::
   La variable d'environnement ``FESS_PORT`` n'est disponible que sous Linux. Sous Windows, modifiez ``-Dfess.port`` directement dans ``bin\fess.in.bat``.

Pour les packages RPM/DEB
~~~~~~~~~~~~~~~~~~~~~~~~

Pour le package RPM, éditez ``/etc/sysconfig/fess``, et pour le package DEB, éditez ``/etc/default/fess``.

::

    FESS_PORT=8080

Configuration sous Windows
~~~~~~~~~~~~~~~~~~~

Sous Windows, éditez ``bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

Lors de l'enregistrement en tant que service Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lorsque vous utilisez un enregistrement en tant que service sous Windows, modifiez également les paramètres de port dans ``bin\service.bat``.
Consultez :doc:`setup-windows-service` pour plus de détails.

Configuration du chemin de contexte
----------------------

Si vous publiez |Fess| dans un sous-répertoire, vous pouvez configurer le chemin de contexte.

**Sous Linux :**

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"

Ou via la variable d'environnement :

::

    export FESS_CONTEXT_PATH=/search

**Sous Windows :**

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.context.path=/search

Avec cette configuration, vous pourrez accéder à ``http://localhost:8080/search/``.

.. warning::
   La variable d'environnement ``FESS_CONTEXT_PATH`` n'est disponible que sous Linux. Sous Windows, utilisez ``-Dfess.context.path`` dans ``bin\fess.in.bat``.

.. warning::
   Si vous modifiez le chemin de contexte, vous devez également configurer correctement le chemin des fichiers statiques.

Configuration du proxy
============

Vue d'ensemble
----

Lors du crawl de sites externes depuis un intranet ou de l'accès à des API externes,
les communications peuvent être bloquées par un pare-feu.
Dans de tels environnements, il est nécessaire de configurer la communication via un serveur proxy.

Configuration du proxy pour le crawler
--------------------------

Configuration de base
~~~~~~~~

Dans l'interface d'administration, spécifiez dans les paramètres de configuration du crawl comme suit.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

Configuration d'un proxy avec authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~

Si le serveur proxy nécessite une authentification, ajoutez ce qui suit.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

Exclusion d'hôtes spécifiques du proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les paramètres de proxy du crawler ne prennent pas en charge nonProxyHosts.
Pour exclure des hôtes spécifiques du proxy, utilisez la variable d'environnement ``FESS_NON_PROXY_HOSTS``.
Ce paramètre est converti en propriété système Java ``http.nonProxyHosts`` et s'applique à toutes les communications HTTP de Fess.

::

    FESS_NON_PROXY_HOSTS=localhost|*.local|192.168.*

Configuration du proxy par défaut du crawler
------------------------------

Pour définir un proxy par défaut lorsque ``client.proxyHost`` n'est pas spécifié dans les configurations de crawl individuelles, configurez dans ``fess_config.properties``.
Ce paramètre s'applique uniquement aux communications HTTP du crawler. Il ne s'applique pas à l'authentification SSO ni aux connexions d'API externes.

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

.. warning::
   Les mots de passe sont stockés sans chiffrement. Configurez les permissions de fichier appropriées.

.. note::
   Pour utiliser un proxy pour l'ensemble de l'application Fess (y compris SSO, intégration LLM, etc.), utilisez les variables d'environnement ``FESS_PROXY_HOST`` et ``FESS_PROXY_PORT``. Consultez la section « Configuration du proxy via les variables d'environnement » ci-dessous pour plus de détails.

Configuration du proxy via les variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lorsque les bibliothèques Java telles que l'authentification SSO doivent utiliser un proxy, vous devez le configurer via des variables d'environnement.
Ces variables d'environnement sont converties en propriétés système Java (``http.proxyHost``, ``https.proxyHost``, etc.).

::

    FESS_PROXY_HOST=proxy.example.com
    FESS_PROXY_PORT=8080
    FESS_NON_PROXY_HOSTS=localhost|*.local|192.168.*

Pour les packages RPM, configurez dans ``/etc/sysconfig/fess``. Pour les packages DEB, configurez dans ``/etc/default/fess``.

.. note::
   Les paramètres ``http.proxy.*`` dans ``fess_config.properties`` sont utilisés comme proxy par défaut du crawler.
   Pour utiliser un proxy pour l'ensemble de l'application Fess y compris l'authentification SSO et l'intégration LLM, configurez les variables d'environnement ci-dessus.

Configuration de la communication HTTP
============

Limitation du téléchargement de fichiers
--------------------------

Vous pouvez limiter la taille des fichiers téléchargés depuis l'interface d'administration.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Élément de configuration
     - Description
   * - ``http.fileupload.max.size``
     - Taille maximale de téléchargement de fichier (par défaut : 262144000 octets = 250 Mo)
   * - ``http.fileupload.threshold.size``
     - Taille de seuil pour la conservation en mémoire (par défaut : 262144 octets = 256 Ko)
   * - ``http.fileupload.max.file.count``
     - Nombre de fichiers pouvant être téléchargés en une fois (par défaut : 10)

Exemple de configuration dans ``fess_config.properties`` :

::

    http.fileupload.max.size=524288000
    http.fileupload.threshold.size=524288
    http.fileupload.max.file.count=20

Configuration du délai de connexion
--------------------

Vous pouvez configurer le délai de connexion à OpenSearch.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Élément de configuration
     - Description
   * - ``search_engine.http.url``
     - URL d'OpenSearch (par défaut : http://localhost:9201)
   * - ``search_engine.heartbeat_interval``
     - Intervalle de vérification de santé (millisecondes, par défaut : 10000)

Modification de la destination de connexion OpenSearch
----------------------

Pour se connecter à un cluster OpenSearch externe :

::

    search_engine.http.url=http://opensearch-cluster.example.com:9200

Connexion à plusieurs nœuds
~~~~~~~~~~~~~~~~~~

Pour se connecter à plusieurs nœuds OpenSearch, spécifiez-les séparés par des virgules.

::

    search_engine.http.url=http://node1:9200,http://node2:9200,http://node3:9200

Configuration de la connexion SSL/TLS
-----------------

Pour se connecter à OpenSearch via HTTPS :

::

    search_engine.http.url=https://opensearch.example.com:9200
    search_engine.http.ssl.certificate_authorities=/path/to/ca.crt
    search_engine.username=admin
    search_engine.password=admin_password

.. note::
   Pour effectuer la vérification du certificat, spécifiez le chemin du certificat CA dans ``certificate_authorities``.

Configuration de l'hôte virtuel
==============

Vue d'ensemble
----

Vous pouvez différencier les résultats de recherche en fonction du nom d'hôte utilisé pour accéder à |Fess|.
Consultez :doc:`security-virtual-host` pour plus de détails.

Configuration de base
--------

Configurez l'en-tête de l'hôte virtuel dans ``fess_config.properties``.

::

    virtual.host.headers=X-Forwarded-Host,Host

Intégration avec un reverse proxy
========================

Exemple de configuration Nginx
--------------

::

    server {
        listen 80;
        server_name search.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Exemple de configuration Apache
---------------

::

    <VirtualHost *:80>
        ServerName search.example.com

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/

        RequestHeader set X-Forwarded-Proto "http"
        RequestHeader set X-Forwarded-Host "search.example.com"
    </VirtualHost>

Terminaison SSL/TLS
-----------

Exemple de configuration pour la terminaison SSL/TLS sur le reverse proxy (Nginx) :

::

    server {
        listen 443 ssl http2;
        server_name search.example.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Configuration du pare-feu
====================

Ouverture des ports nécessaires
------------------

Pour rendre |Fess| accessible depuis l'extérieur, ouvrez les ports suivants.

**Exemple de configuration iptables :**

::

    # Application web Fess
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

    # Pour accès HTTPS (via reverse proxy)
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT

**Exemple de configuration firewalld :**

::

    # Application web Fess
    firewall-cmd --permanent --add-port=8080/tcp
    firewall-cmd --reload

Configuration du groupe de sécurité (environnements cloud)
------------------------------------------

Dans les environnements cloud comme AWS, GCP ou Azure, ouvrez les ports appropriés
avec les groupes de sécurité ou les ACL réseau.

Configuration recommandée :
- Entrant : ports 80/443 (via reverse proxy HTTP)
- Restreindre l'accès au port 8080 uniquement depuis l'interne
- Restreindre l'accès aux ports 9201/9301 d'OpenSearch uniquement depuis l'interne

Dépannage
======================

Impossible d'accéder après modification du port
------------------------------

1. Vérifiez si vous avez redémarré |Fess|.
2. Vérifiez si le port correspondant est ouvert dans le pare-feu.
3. Vérifiez les erreurs dans le fichier journal (``fess.log``).

Impossible de crawler via le proxy
------------------------------

1. Vérifiez si le nom d'hôte et le port du serveur proxy sont corrects.
2. Si le serveur proxy nécessite une authentification, configurez le nom d'utilisateur et le mot de passe.
3. Vérifiez si les tentatives de connexion sont enregistrées dans les journaux du serveur proxy.
4. Vérifiez si la configuration de ``nonProxyHosts`` est appropriée.

Impossible de se connecter à OpenSearch
-------------------------

1. Vérifiez si OpenSearch est démarré.
2. Vérifiez si la configuration de ``search_engine.http.url`` est correcte.
3. Vérifiez la connexion réseau : ``curl http://localhost:9201``
4. Vérifiez les erreurs dans les journaux d'OpenSearch.

Fonctionnement anormal lors de l'accès via reverse proxy
----------------------------------------------------

1. Vérifiez si l'en-tête ``X-Forwarded-Host`` est correctement configuré.
2. Vérifiez si l'en-tête ``X-Forwarded-Proto`` est correctement configuré.
3. Vérifiez si le chemin de contexte est correctement configuré.
4. Vérifiez les erreurs dans les journaux du reverse proxy.

Informations de référence
========

- :doc:`setup-memory` - Configuration de la mémoire
- :doc:`setup-windows-service` - Configuration du service Windows
- :doc:`security-virtual-host` - Configuration de l'hôte virtuel
- :doc:`crawler-advanced` - Configuration avancée du crawler
- `OpenSearch Configuration <https://opensearch.org/docs/latest/install-and-configure/configuration/>`_
