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

Installation (ZIP package)
============

Unzip the downloaded fess-x.y.zip.
For UNIX environment, run the following command:

::

    $ unzip fess-x.y.zip
    $ cd fess-x.y


Change Encryption Key
=====================

Fess uses a cipyer to encrypt password.
Please change the default key phrase, especially in production.
The key phrase is in app/WEB-INF/classes/fess_config.properties (For RPM package, in /etc/fess/fess_config.properties). 

::

    app.cipher.key=__change_me__
