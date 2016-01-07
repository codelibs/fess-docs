============
Installation
============

Requirements
============

|Fess| can be available in these environments.

-  OS: Windows/Unix with Java environment
-  Java: Java 8 update 20 or later

If Java is not installed in your environment, see we want to |Fess| from `Oracle site <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`__ to install JDK.

Download
========

Download the latest |Fess| package from the release site, `https://github.com/codelibs/fess/releases <https://github.com/codelibs/fess/releases>`__.

Installation
============

Using ZIP package
-----------------

Unzip the downloaded fess-<version>.zip.
For UNIX environment, run the following command:

::

    $ unzip fess-<version>.zip
    $ cd fess-<version>

Using RPM package
-----------------

You need to install elasticsearch RPM package before Fess installation.
Download elasticsearch RPM package from elasticsearch site `https://www.elastic.co/downloads/elasticsearch <https://www.elastic.co/downloads/elasticsearch>`__, and then install the package.

::

    $ sudo rpm -ivh elasticsearch-<version>.rpm

To access from Fess, the following configuration needs to be added to /etc/elasticsearch/elasticsearcy.yml

::

    configsync.config_path: /var/lib/elasticsearch/config
    script.engine.groovy.inline.update: on

Next, install |Fess| RPM package.

::

    $ sudo rpm -ivh fess-<version>.rpm

|Fess| provides elasticsearch plugins to extend elasticsearch's features for |Fess|.
Copy them to elasticsearch plugins directory.

::

    $ sudo cp -r /usr/share/fess/es/plugins /usr/share/elasticsearch

To register them as a service, run the following commands if using chkconfig,

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

if using systemd.

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service

Change Encryption Key
=====================

Fess uses a cipyer to encrypt password.
Please change the default key phrase, especially in production.
The key phrase is in app/WEB-INF/classes/fess_config.properties (For RPM package, in /etc/fess/fess_config.properties). 

::

    app.cipher.key=__change_me__
