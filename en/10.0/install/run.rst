==============
Start/Stop |Fess| Server
==============

Start |Fess| Server (ZIP package)
============

For Windows environment, double-click the fess.bat file in the bin folder to start Fess.
For Unix environments, run fess to start Fess.

::

    $ ./bin/fess

Start |Fess| Server (RPM package)
============

Start elasticsearch before |Fess|,

::

    $ sudo service elasticsearch start

and then start |Fess| service.

::

    $ sudo service fess start

Access To Browser UI 
======

|Fess| is available at http://localhost:8080/.

Administration UI is http://localhost:8080/admin.
The default administrator account is admin/admin as username/password.
In User page on administration UI, you can change the password.

Stop |Fess| Server (ZIP package)
============

To stop |Fess| server, kill the process of |Fess|.

Stop |Fess| Server (RPM package)
============

To stop |Fess| service, run the following command.

::

    $ sudo service fess stop

