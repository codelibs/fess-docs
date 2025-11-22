==========================
Development Environment Setup
==========================

This page provides detailed instructions for setting up a |Fess| development environment.
It guides you step by step from choosing an IDE to obtaining source code, running, and debugging.

.. contents:: Table of Contents
   :local:
   :depth: 2

System Requirements
==========

The following hardware requirements are recommended for the development environment.

Hardware Requirements
--------------

- **CPU**: 4 cores or more
- **Memory**: 8GB or more (16GB recommended)
- **Disk**: 20GB or more of free space

.. note::

   During development, |Fess| itself and the embedded OpenSearch run simultaneously,
   so ensure sufficient memory and disk space.

Software Requirements
--------------

- **OS**: Windows 10/11, macOS 11 or later, Linux (Ubuntu 20.04 or later, etc.)
- **Java**: JDK 21 or later
- **Maven**: 3.x or later
- **Git**: 2.x or later
- **IDE**: Eclipse, IntelliJ IDEA, VS Code, etc.

Installing Required Software
==========================

Installing Java
-----------------

Java 21 or later is required for |Fess| development.

Installing Eclipse Temurin (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Eclipse Temurin (formerly AdoptOpenJDK) is recommended.

1. Visit `Adoptium <https://adoptium.net/temurin/releases/>`__
2. Download the LTS version of Java 21
3. Follow the installer instructions to install

Verifying Installation
~~~~~~~~~~~~~~

Execute the following in a terminal or command prompt:

.. code-block:: bash

    java -version

If successful, you will see output similar to:

.. code-block:: text

    openjdk version "21.0.x" 2024-xx-xx LTS
    OpenJDK Runtime Environment Temurin-21.0.x+x (build 21.0.x+x-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.x+x (build 21.0.x+x-LTS, mixed mode, sharing)

Setting Environment Variables
~~~~~~~~~~~~

**Linux/macOS:**

Add the following to ``~/.bashrc`` or ``~/.zshrc``:

.. code-block:: bash

    export JAVA_HOME=/path/to/java21
    export PATH=$JAVA_HOME/bin:$PATH

**Windows:**

1. Open "Edit the system environment variables"
2. Click "Environment Variables"
3. Add ``JAVA_HOME``: ``C:\Program Files\Eclipse Adoptium\jdk-21.x.x.x-hotspot``
4. Add ``%JAVA_HOME%\bin`` to ``PATH``

Installing Maven
------------------

Install Maven 3.x or later.

Download and Installation
~~~~~~~~~~~~~~~~~~~~~~~~

1. Visit the `Maven download page <https://maven.apache.org/download.cgi>`__
2. Download the Binary zip/tar.gz archive
3. Extract and place in an appropriate location

**Linux/macOS:**

.. code-block:: bash

    tar xzvf apache-maven-3.x.x-bin.tar.gz
    sudo mv apache-maven-3.x.x /opt/
    sudo ln -s /opt/apache-maven-3.x.x /opt/maven

**Windows:**

1. Extract the ZIP file
2. Place in ``C:\Program Files\Apache\maven`` or similar location

Setting Environment Variables
~~~~~~~~~~~~

**Linux/macOS:**

Add the following to ``~/.bashrc`` or ``~/.zshrc``:

.. code-block:: bash

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH

**Windows:**

1. Add ``MAVEN_HOME``: ``C:\Program Files\Apache\maven``
2. Add ``%MAVEN_HOME%\bin`` to ``PATH``

Verifying Installation
~~~~~~~~~~~~~~

.. code-block:: bash

    mvn -version

If successful, you will see output similar to:

.. code-block:: text

    Apache Maven 3.x.x
    Maven home: /opt/maven
    Java version: 21.0.x, vendor: Eclipse Adoptium

Installing Git
----------------

If Git is not installed, install it from:

- **Windows**: `Git for Windows <https://git-scm.com/download/win>`__
- **macOS**: ``brew install git`` or `Git download page <https://git-scm.com/download/mac>`__
- **Linux**: ``sudo apt install git`` (Ubuntu/Debian) or ``sudo yum install git`` (RHEL/CentOS)

Verify installation:

.. code-block:: bash

    git --version

IDE Setup
===============

For Eclipse
------------

Eclipse is the IDE recommended in the official |Fess| documentation.

Installing Eclipse
~~~~~~~~~~~~~~~~~~~~

1. Visit the `Eclipse download page <https://www.eclipse.org/downloads/>`__
2. Download "Eclipse IDE for Enterprise Java and Web Developers"
3. Run the installer and follow the instructions

Recommended Plugins
~~~~~~~~~~~~

Eclipse includes the following plugins by default:

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

Importing the Project
~~~~~~~~~~~~~~~~~~~~

1. Launch Eclipse
2. Select ``File`` > ``Import``
3. Select ``Maven`` > ``Existing Maven Projects``
4. Specify the Fess source code directory
5. Click ``Finish``

Setting Run Configuration
~~~~~~~~~~~~

1. Select ``Run`` > ``Run Configurations...``
2. Right-click ``Java Application`` and select ``New Configuration``
3. Configure the following:

   - **Name**: Fess Boot
   - **Project**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``

4. Click ``Apply``

For IntelliJ IDEA
-------------------

IntelliJ IDEA is also a widely used IDE.

Installing IntelliJ IDEA
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Visit the `IntelliJ IDEA download page <https://www.jetbrains.com/idea/download/>`__
2. Download Community Edition (free) or Ultimate Edition
3. Run the installer and follow the instructions

Importing the Project
~~~~~~~~~~~~~~~~~~~~

1. Launch IntelliJ IDEA
2. Select ``Open``
3. Select the ``pom.xml`` in the Fess source code directory
4. Click ``Open as Project``
5. It will be automatically imported as a Maven project

Setting Run Configuration
~~~~~~~~~~~~

1. Select ``Run`` > ``Edit Configurations...``
2. Click the ``+`` button and select ``Application``
3. Configure the following:

   - **Name**: Fess Boot
   - **Module**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``
   - **JRE**: Java 21

4. Click ``OK``

For VS Code
------------

VS Code is also an option if you prefer a lightweight development environment.

Installing VS Code
~~~~~~~~~~~~~~~~~~~~

1. Visit the `VS Code download page <https://code.visualstudio.com/>`__
2. Download and run the installer

Installing Required Extensions
~~~~~~~~~~~~~~~~~~~~~~~~

Install the following extensions:

- **Extension Pack for Java**: A set of extensions required for Java development
- **Maven for Java**: Maven support

Opening the Project
~~~~~~~~~~~~~~~~

1. Launch VS Code
2. Select ``File`` > ``Open Folder``
3. Select the Fess source code directory

Obtaining Source Code
==============

Cloning from GitHub
-------------------

Clone the |Fess| source code from GitHub.

.. code-block:: bash

    git clone https://github.com/codelibs/fess.git
    cd fess

If using SSH:

.. code-block:: bash

    git clone git@github.com:codelibs/fess.git
    cd fess

.. tip::

   If you want to fork and develop, first fork the Fess repository on GitHub,
   then clone your forked repository:

   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/fess.git
       cd fess
       git remote add upstream https://github.com/codelibs/fess.git

Building the Project
==================

Downloading OpenSearch Plugins
---------------------------------

Plugins for OpenSearch are required to run Fess.
Download them with the following command:

.. code-block:: bash

    mvn antrun:run

This command performs the following:

- Downloads OpenSearch
- Downloads and installs required plugins
- Configures OpenSearch

.. note::

   This command only needs to be executed the first time or when updating plugins.
   You don't need to run it every time.

Initial Build
--------

Build the project:

.. code-block:: bash

    mvn clean compile

The initial build may take some time (downloading dependency libraries, etc.).

If the build is successful, you will see messages like:

.. code-block:: text

    [INFO] BUILD SUCCESS
    [INFO] Total time: xx:xx min
    [INFO] Finished at: 2024-xx-xxTxx:xx:xx+09:00

Running Fess
==========

Running from Command Line
--------------------

Run using Maven:

.. code-block:: bash

    mvn compile exec:java

Or, package and then run:

.. code-block:: bash

    mvn package
    java -jar target/fess-15.3.x.jar

Running from IDE
------------

For Eclipse
~~~~~~~~~~~~

1. Right-click the ``org.codelibs.fess.FessBoot`` class
2. Select ``Run As`` > ``Java Application``

Or, use the created run configuration:

1. Click the dropdown of the run button in the toolbar
2. Select ``Fess Boot``

For IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Right-click the ``org.codelibs.fess.FessBoot`` class
2. Select ``Run 'FessBoot.main()'``

Or, use the created run configuration:

1. Click the dropdown of the run button in the toolbar
2. Select ``Fess Boot``

For VS Code
~~~~~~~~~~~~

1. Open ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Select ``Run Without Debugging`` from the ``Run`` menu

Verifying Startup
--------

Fess startup takes 1-2 minutes.
Startup is complete when you see logs like the following in the console:

.. code-block:: text

    [INFO] Boot Thread: Boot process completed successfully.

Access the following in a browser to verify operation:

- **Search screen**: http://localhost:8080/
- **Admin screen**: http://localhost:8080/admin/

  - Default user: ``admin``
  - Default password: ``admin``

Changing the Port Number
--------------

If the default port 8080 is in use, you can change it in the following file:

``src/main/resources/fess_config.properties``

.. code-block:: properties

    # Change port number
    server.port=8080

Debug Execution
==========

Debug Execution in IDE
------------------

For Eclipse
~~~~~~~~~~~~

1. Right-click the ``org.codelibs.fess.FessBoot`` class
2. Select ``Debug As`` > ``Java Application``
3. Set breakpoints to trace code execution

For IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Right-click the ``org.codelibs.fess.FessBoot`` class
2. Select ``Debug 'FessBoot.main()'``
3. Set breakpoints to trace code execution

For VS Code
~~~~~~~~~~~~

1. Open ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Select ``Start Debugging`` from the ``Run`` menu

Remote Debugging
--------------

You can also attach a debugger to Fess started from the command line.

Start Fess in debug mode:

.. code-block:: bash

    mvn compile exec:java -Dexec.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

Connect remote debugger from IDE:

**Eclipse:**

1. Select ``Run`` > ``Debug Configurations...``
2. Right-click ``Remote Java Application`` and select ``New Configuration``
3. Set ``Port: 5005``
4. Click ``Debug``

**IntelliJ IDEA:**

1. Select ``Run`` > ``Edit Configurations...``
2. Select ``+`` > ``Remote JVM Debug``
3. Set ``Port: 5005``
4. Click ``OK`` and run ``Debug``

Useful Development Settings
==============

Changing Log Level
--------------

Changing the log level during debugging allows you to see detailed information.

Edit ``src/main/resources/log4j2.xml``:

.. code-block:: xml

    <Configuration status="INFO">
        <Loggers>
            <Logger name="org.codelibs.fess" level="DEBUG"/>
            <Root level="INFO">
                <AppenderRef ref="console"/>
            </Root>
        </Loggers>
    </Configuration>

Enabling Hot Deploy
-------------------

LastaFlute can reflect some changes without restarting.

Configure the following in ``src/main/resources/fess_config.properties``:

.. code-block:: properties

    # Enable hot deploy
    development.here=true

However, the following changes require a restart:

- Changes to class structure (adding/removing methods, etc.)
- Changes to configuration files
- Changes to dependency libraries

Operating Embedded OpenSearch
------------------------

In the development environment, an embedded OpenSearch is used.

OpenSearch location:

.. code-block:: text

    target/fess/es/

Direct access to OpenSearch API:

.. code-block:: bash

    # List indices
    curl -X GET http://localhost:9201/_cat/indices?v

    # Search documents
    curl -X GET http://localhost:9201/fess.search/_search?pretty

    # Check mapping
    curl -X GET http://localhost:9201/fess.search/_mapping?pretty

Using External OpenSearch
--------------------

To use an external OpenSearch server,
edit ``src/main/resources/fess_config.properties``:

.. code-block:: properties

    # Disable embedded OpenSearch
    opensearch.cluster.name=fess
    opensearch.http.url=http://localhost:9200

Code Generation with DBFlute
======================

|Fess| uses DBFlute to automatically generate
Java code from OpenSearch schemas.

Regenerating When Schema Changes
----------------------------

If you change the OpenSearch mapping, regenerate the
corresponding Java code with the following commands:

.. code-block:: bash

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format

Explanation of each command:

- ``rm -rf mydbflute``: Remove existing DBFlute working directory
- ``mvn antrun:run``: Download OpenSearch plugins
- ``mvn dbflute:freegen``: Generate Java code from schema
- ``mvn license:format``: Add license headers

Troubleshooting
==================

Build Errors
----------

**Error: Java version is old**

.. code-block:: text

    [ERROR] Failed to execute goal ... requires at least Java 21

Solution: Install Java 21 or later and set ``JAVA_HOME`` appropriately.

**Error: Failed to download dependencies**

.. code-block:: text

    [ERROR] Failed to collect dependencies

Solution: Check network connection, clear Maven local repository and retry:

.. code-block:: bash

    rm -rf ~/.m2/repository
    mvn clean compile

Runtime Errors
--------

**Error: Port 8080 is already in use**

.. code-block:: text

    Address already in use

Solution:

1. Terminate the process using port 8080
2. Or, change the port number in ``fess_config.properties``

**Error: OpenSearch won't start**

Check the log files in ``target/fess/es/logs/``.

Common causes:

- Insufficient memory: Increase JVM heap size
- Port 9201 in use: Change port number
- Insufficient disk space: Free up disk space

Project Not Recognized in IDE
----------------------------

**Update Maven Project**

- **Eclipse**: Right-click project > ``Maven`` > ``Update Project``
- **IntelliJ IDEA**: Click ``Reload All Maven Projects`` in the ``Maven`` tool window
- **VS Code**: Run ``Java: Clean Java Language Server Workspace`` from the command palette

Next Steps
==========

After completing the development environment setup, refer to the following documents:

- :doc:`architecture` - Understanding code structure
- :doc:`workflow` - Learning the development workflow
- :doc:`building` - Build and test methods
- :doc:`contributing` - Creating pull requests

Resources
========

- `Eclipse Download <https://www.eclipse.org/downloads/>`__
- `IntelliJ IDEA Download <https://www.jetbrains.com/idea/download/>`__
- `VS Code Download <https://code.visualstudio.com/>`__
- `Maven Documentation <https://maven.apache.org/guides/>`__
- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
