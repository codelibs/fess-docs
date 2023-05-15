=========================
Start/Stop |Fess| Server
=========================

Start |Fess| Server
====================

Using TAR.GZ package
---------------------

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
---------------------------------

Before starting |Fess|, OpenSearch must be started.

::

    $ sudo service opensearch start

Next, start |Fess|.

::

    $ sudo service fess start

Using RPM/DEB package (systemd)
--------------------------------

Before starting |Fess|, OpenSearch must be started.

::

    $ sudo systemctl start opensearch.service

Next, start |Fess|.

::

    $ sudo systemctl start fess.service

Using Docker package
--------------------

Execute the following command to start OpenSearch and |Fess|.

::

    $ docker compose -f compose.yaml -f compose-opensearch2.yaml up -d

Access To Browser UI 
========================

|Fess| can be accessed at http://localhost:8080/.

The management UI is located at http://localhost:8080/admin.
The default admin account username/password is admin/admin.
You can change the password on the user page in the management UI.

Stop |Fess| Server
===================

Using TAR.GZ/ZIP package
-------------------------

To stop the |Fess| server, kill the |Fess| process.

Using RPM/DEB package (chkconfig)
---------------------------------

|Fess| To stop the server, enter the following command: 

::

    $ sudo service fess stop

Using RPM/DEB package (systemd)
-------------------------------

|Fess| To stop the server, enter the following command: 

::

    $ sudo systemctl stop fess.service


Using Docker package
---------------------

Stop OpenSearch and |Fess| by running the following commands:

::

    $ docker compose -f compose.yaml -f compose-opensearch2.yaml down
