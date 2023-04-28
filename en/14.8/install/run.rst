==============
Start/Stop |Fess| Server
==============

Start |Fess| Server
============

Using TAR.GZ/ZIP package (Elasticsearch)
-----------------

Before starting |Fess|, Elasticsearch must be started.

To start Elasticsearch on a Windows environment, double-click on elasticsearch.bat in the bin folder.
On a Linux/Mac environment, execute the following command:

::

    $ cd $SEARCH_ENGINE_HOME
    $ ./bin/elasticsearch

Next, start |Fess|. To start |Fess| on a Windows environment, double-click on fess.bat in the bin folder.
On a Linux/Mac environment, execute the following command:

::

    $ cd $FESS_HOME
    $ ./bin/fess

Using TAR.GZ package (OpenSearch)
--------------------------------

Before starting |Fess|, OpenSearch must be started.

Execute the following command:

::

    $ cd $OPENSEARCH_HOME
    $ ./bin/opensearch

Next, start |Fess|. Execute the following command:

::

    $ cd $FESS_HOME
    $ ./bin/fess

Using RPM/DEB package (chkconfig)
--------------------------------

Before starting |Fess|, OpenSearch or Elasticsearch must be started.

(OpenSearch)

::

    $ sudo service opensearch start

(Elasticsearch)

::

    $ sudo service elasticsearch start

Next, start |Fess|.

::

    $ sudo service fess start

Using RPM/DEB package (systemd)
------------------------------

Before starting |Fess|, OpenSearch or Elasticsearch must be started.

(OpenSearch)

::

    $ sudo systemctl start opensearch.service

(Elasticsearch)

::

    $ sudo systemctl start elasticsearch.service

Next, start |Fess|.

::

    $ sudo systemctl start fess.service

Using Docker package (Elasticsearch)
-----------------------------------

Execute the following command to start Elasticsearch and |Fess|.

::

    $ docker-compose -f docker-compose.yml -f docker-compose.standalone.yml up -d

Using Docker package (OpenSearch)
--------------------------------

Execute the following command to start OpenSearch and |Fess|.

::

    $ docker-compose --env-file .env.opensearch -f docker-compose.yml -f docker-compose.opensearch.yml up -d

Access To Browser UI 
========================

|Fess| can be accessed at http://localhost:8080/.

The management UI is located at http://localhost:8080/admin.
The default admin account username/password is admin/admin.
You can change the password on the user page in the management UI.

Stop |Fess| Server
============

Using TAR.GZ/ZIP package
------------------

To stop the |Fess| server, kill the |Fess| process.

Using RPM/DEB package (chkconfig)
---------------------------

|Fess| To stop the server, enter the following command: 

::

    $ sudo service fess stop

Using RPM/DEB package (systemd)
-------------------------

|Fess| To stop the server, enter the following command: 

::

    $ sudo systemctl stop fess.service


Using Docker package (Elasticsearch)
------------------------------

Stop Elasticsearch and |Fess| by running the following commands:

::

    $ docker-compose -f docker-compose.yml -f docker-compose.standalone.yml down

Using Docker package (OpenSearch)
---------------------------

Stop OpenSearch and |Fess| by running the following commands:

::

    $ docker-compose --env-file .env.opensearch -f docker-compose.yml -f docker-compose.opensearch.yml down
