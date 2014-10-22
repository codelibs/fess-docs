=================
Fess Installation
=================

How to install
==============

Fess can run on any operating system with Java runtime environment.
Requirement detail is as follows.

-  Operating system: Windows, Unix, etc

-  Java: Java SE version 7 or later

Installing Java
===============

If Java is not installed please following these steps below to install
Java.

Accessing Java SE downloads page
--------------------------------

Browsers with Javascript enable are required to access Oracle's\ `Java
SE Downloads
page <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`__.

\* We recommend `Java
7u25 <http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html#jdk-7u25-oth-JPR>`__.
[2014 / 3 / 13]

Click the 'Download JDK' tab. (Without Javascript enable, download will
become invalid)

|image0|

To check whether JavaScript is enabled, you can as follows. (In case of
Internet Explorer 9)

1. Click [tools] on the menu bar.

2. Click [Internet Options].

3. Click Security tab.

4. Click [custom level].

5. Scrawl to [scripts] section.

6. In the Active Scripting section, confirm whether button is checked.

7. Turn on to enable Javascript and off to disable Javascript. Then
   click "OK" button to save change.

License verification
--------------------

Java SE's license detail is as 'The Oracle Binary Code License Agreement
for Java SE'. Check "Accept License Agreement" to agree Java SE's
license.

|image1|

Download Java SE
----------------

Different Operating System requires different version of Java SE. In
case of Windows 64-bit, you must select Windowsx64 version. In case of
Windows 32-bit, you must select Windowx86 version. Java SE's Windowx64
version is used in the following example.

You can check whether your window is 32 bits or 64 bits by following
these steps below. (In case of Windows 7)

1. In Control Panel, select "system and security"

2. [System] appears to the type of system.

|image2|

Running JDK Installer
---------------------

After downloading, JDK Installer file (jdk-7uXX-windows-x64.exe or
jdk-7uXX-windows-x86.exe) is archived. xx is Java SE's version. The
following image shows icon image of Java SE 7 version 7's JDK Installer.

|image3|

Double click JDK Installer to start installing Java SE. Depending on
Windows settings, there is case where "Accept dialog" is appeared. In
that case, click "Yes" to continue installation

JDK installation
----------------

The installer shows first dialog. Press [next] button to continue.

|image4|

You can change the installation's destination folder. We recommend using
default options. Press [next] button to continue.

|image5|

JDK installer starts installing. Wait until installation finishs.

|image6|

JRE installation
----------------

After JDK installation is finished. JRE installation will be started
automatically. JRE will be installed in the same folder as JDK's
installed folder. We recommend using the default options. Press [next]
button to continue.

|image7|

JRE installer starts installing. Wait until installation finishs.

|image8|

Completing the installation
---------------------------

After the installation finishes, following dialog will appear. Press
[close] button to finish installation.

|image9|

Installation is complete.

Installed components (JDK and JRE) can be checked by using following
step. (In case of Windows 7)

1. [Control Panel] → [programs] → [programs and features]. Two new
   installed components appear inside installed components' list.

   -  Java SE Development Kit 7 Update XX (64-bit)

   -  Java (TM) Update 7 XX (64-bit)

Setting environment variables
-----------------------------

Fess requires Windows command prompt with runable JDK command. These
steps below set up environtment variables to use JDK command from
command prompt

In case of Windows 7, do as following steps. Select "Control panel" →
"System and security" → "System" → "Advanced system settings" →
"Environment variables".

|image10|

Click "System and security".

|image11|

Click "System".

|image12|

Click "Advanced settings".

|image13|

Click "Environment variables".

|image14|

Click "New system environment variables" button which is located at
bottom of setting dialpg

|image15|

Variable name: "JAVA\_HOME".

Variable value: installed JDK location.

|image16|

To check JDK's installed folder do as following steps.

Go to C:\\Program Files zone\\scripting in the Explorer. Then searching
for folder with keywor: ' jdk... '.

For example if you installed JDK version 1.7.0\_XX, installed folder
will be C:\\Program Files \\Java\\jdk1.7.0\_XX. (XX is JDK version
number

Parse folder location and then press 'OK' to close dialog.

Scroll down list of system environment variables and select variables
'Path'.

|image17|

Click Edit button. Then add "; %JAVA\_HOME%\\bin ' to the end of Path
value. Click the 'OK' to close dialog.

|image18|

Installing Fess
===============

Go to download page of Fess
---------------------------

`http://sourceforge.jp/projects/Fess/releases/ <http://sourceforge.jp/projects/fess/releases/>`__
Download latest Fess package.

Expand file list of the destination URL, then download
'fess-server-9.x.y.zip'.

|image19|

Installation
------------

Unzip downloaded zip file. In case of Windows environment, we recommend
using 7-zip. In case of Unix, we recommend using unzip command.

In case of Unix environment, start up script "startup.sh" need to be
executable. Execute following command to add executable access
permission to script files.

::

    $ unzip fess-server-9.x.y.zip
    $ cd fess-server-9.x.y
    $ chmod +x bin/*.sh   # (In case of Unix environment)

|image20|

Double-click to open un-zipped folder.

|image21|

Double-click to open bin folder.

|image22|

Launch of the Fess
------------------

In case of Windows environment, double-click the startup.bat file in the
bin folder to start Fess.

In case of Unix environments, run startup.sh to start Fess.

::

    $ ./bin/startup.sh

|image23|

After starting Fess, at the end of console message "Server startup... '
willbe appeared. If this message is not appeared, check Java
environment's validity.

|image24|

Operation check
===============

Go to http://localhost:8080/Fess to check whether Fess started normally.

Fess' management UI is located at / http://localhost:8080/fess/admin.
Default Administrator account's user name / password is admin/admin.
Administrator account is managed by the application server.
Administrators of Fess' management UI are users whose rolls are
certificated by applicatoion server .

Other
=====

Stop Fess
---------

To stop Fess, in case of Windows environment double-click shutdown.bat
file in the bin folder.

To stop Fess, in case of Unix environment run the shutdown.sh.

::

    $ ./bin/shutdown.sh

Changing administrator password
-------------------------------

Administrator account is managed by the application server. Fess'
standard server is Tomcat. So to change administrator password, you need
to modify conf/tomcat-user.xml.

::

      <user username="admin" password="admin" roles="fess"/>

Changing SOLR server password
-----------------------------

Password is required to access Solr of Fess. Change the default
passwords in production.

To change Solr password, first you must change solradmin password
attribute of conf/tomcat-user.xml.

::

      <user username="solradmin" password="solradmin" roles="solr"/>

Modifies the following three files
webapps/fess/WEB-INF/classes/solrlib.dicon, fess\_suggest.dicon and
solr/core1/conf/solrconfig.xml. These there files' user / password are
as same as user / password which are specified in tomcat-user.xml.

In case of solrlib.dicon, detail is as follows.

::

    <component class="org.apache.commons.httpclient.UsernamePasswordCredentials">
        <arg>"solradmin"</arg> <!-- ユーザー名 -->
        <arg>"solradmin"</arg> <!-- パスワード -->
    </component>

In case of fess\_suggest.dicon, detail is as follows.

::

    <component name="suggestCredentials" class="org.apache.http.auth.UsernamePasswordCredentials">
        <arg>"solradmin"</arg> <!-- ユーザー名 -->
        <arg>"solradmin"</arg> <!-- パスワード -->
    </component>

In case of SOLR/core1/conf/solrconfig.XML, detail is as follows.

::

    <!-- SuggestTranslogUpdateHandler settings -->
    <suggest>
      <solrServer class="org.codelibs.solr.lib.server.SolrLibHttpSolrServer">
        <arg>http://localhost:8080/solr/core1-suggest</arg>
        <credentials>
          <username>solradmin</username> <!-- ユーザー名 -->
          <password>solradmin</password> <!-- パスワード -->
        </credentials>

.. |image0| image:: ../resources/images/en/install/java-1.png
.. |image1| image:: ../resources/images/en/install/java-2.png
.. |image2| image:: ../resources/images/en/install/java-3.png
.. |image3| image:: ../resources/images/en/install/java-4.png
.. |image4| image:: ../resources/images/en/install/java-5.png
.. |image5| image:: ../resources/images/en/install/java-6.png
.. |image6| image:: ../resources/images/en/install/java-7.png
.. |image7| image:: ../resources/images/en/install/java-8.png
.. |image8| image:: ../resources/images/en/install/java-9.png
.. |image9| image:: ../resources/images/en/install/java-10.png
.. |image10| image:: ../resources/images/en/install/java-11.png
.. |image11| image:: ../resources/images/en/install/java-12.png
.. |image12| image:: ../resources/images/en/install/java-13.png
.. |image13| image:: ../resources/images/en/install/java-14.png
.. |image14| image:: ../resources/images/en/install/java-15.png
.. |image15| image:: ../resources/images/en/install/java-16.png
.. |image16| image:: ../resources/images/en/install/java-17.png
.. |image17| image:: ../resources/images/en/install/java-18.png
.. |image18| image:: ../resources/images/en/install/java-19.png
.. |image19| image:: ../resources/images/en/install/Fess-1.png
.. |image20| image:: ../resources/images/en/install/Fess-2.png
.. |image21| image:: ../resources/images/en/install/Fess-3.png
.. |image22| image:: ../resources/images/en/install/Fess-4.png
.. |image23| image:: ../resources/images/en/install/Fess-5.png
.. |image24| image:: ../resources/images/en/install/Fess-6.png
