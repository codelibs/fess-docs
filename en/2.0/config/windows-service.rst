================================
Register for the Windows service
================================

This page is generated by Machine Translation from Japanese.

Registered as a Windows service
===============================

You can register the |Fess| as a Windows service in a Windows environment.
How to register a service is similar to the Tomcat.

How to register
---------------

First, after installing the |Fess| from the command prompt service.bat
performs (such as Vista to launch as administrator you must). |Fess| was
installed on C:\\Java\\fess-server-2.0.0.

::

    > cd C:\Java\fess-server-2.0.0\bin
    > service.bat install fess
    ...
    The service 'fess' has been installed.

Then add properties for |Fess| . To run the following, Tomcat Properties
window appears.

::

    > tomcat6w.exe //ES//fess

Set the following in the Java Options in the Java tab.

::

    -Dcatalina.base=C:\Java\fess-server-2.0.0
    -Dcatalina.home=C:\Java\fess-server-2.0.0
    -Djava.endorsed.dirs=C:\Java\fess-server-2.0.0\endorsed
    -Djava.io.tmpdir=C:\Java\fess-server-2.0.0\temp
    -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
    -Djava.util.logging.config.file=C:\Java\fess-server-2.0.0\conf\logging.properties
    -Dsolr.solr.home=C:\Java\fess-server-2.0.0\solr
    -Dsolr.data.dir=C:\Java\fess-server-2.0.0\solr\data
    -Dfess.log.file=C:\Java\fess-server-2.0.0\webapps\fess\WEB-INF\logs\fess.out
    -Djava.awt.headless=true
    -XX:+UseGCOverheadLimit
    -XX:+UseConcMarkSweepGC
    -XX:+CMSIncrementalMode
    -XX:+UseTLAB
    -Dpdfbox.cjk.support=true
    -XX:MaxPermSize=128m

Modifies the value of the maximum memory pool to 512. Settings to save
the settings and then press OK button. Please start later as normal
Windows services and.
