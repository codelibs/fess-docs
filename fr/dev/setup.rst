====================
Configuration de l'environnement de développement
====================

Cette page explique en détail les procédures de configuration de l'environnement de développement pour |Fess|.
Explique étape par étape du choix de l'IDE, à l'obtention du code source, l'exécution et le débogage.

.. contents:: Table des matières
   :local:
   :depth: 2

Configuration système requise
==========

Nous recommandons la configuration matérielle suivante pour l'environnement de développement.

Configuration matérielle
--------------

- **CPU** : 4 cœurs ou plus
- **Mémoire** : 8 Go ou plus (16 Go recommandé)
- **Disque** : 20 Go ou plus d'espace libre

.. note::

   Pendant le développement, |Fess| et OpenSearch intégré fonctionnent simultanément,
   assurez-vous donc d'avoir suffisamment de mémoire et d'espace disque.

Configuration logicielle
--------------

- **OS** : Windows 10/11, macOS 11 ou supérieur, Linux (Ubuntu 20.04 ou supérieur, etc.)
- **Java** : JDK 21 ou supérieur
- **Maven** : 3.x ou supérieur
- **Git** : 2.x ou supérieur
- **IDE** : Eclipse, IntelliJ IDEA, VS Code, etc.

Installation des logiciels requis
==========================

Installation de Java
-----------------

Java 21 ou supérieur est requis pour le développement de |Fess|.

Installation d'Eclipse Temurin (recommandé)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Eclipse Temurin (anciennement AdoptOpenJDK) est recommandé.

1. Accédez à `Adoptium <https://adoptium.net/temurin/releases/>`__
2. Téléchargez la version LTS de Java 21
3. Suivez les instructions de l'installateur pour installer

Vérification de l'installation
~~~~~~~~~~~~~~

Exécutez ce qui suit dans un terminal ou une invite de commande :

.. code-block:: bash

    java -version

Si la sortie suivante s'affiche, c'est réussi :

.. code-block:: text

    openjdk version "21.0.x" 2024-xx-xx LTS
    OpenJDK Runtime Environment Temurin-21.0.x+x (build 21.0.x+x-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.x+x (build 21.0.x+x-LTS, mixed mode, sharing)

Configuration des variables d'environnement
~~~~~~~~~~~~

**Linux/macOS:**

Ajoutez ce qui suit à ``~/.bashrc`` ou ``~/.zshrc`` :

.. code-block:: bash

    export JAVA_HOME=/path/to/java21
    export PATH=$JAVA_HOME/bin:$PATH

**Windows:**

1. Ouvrez « Modifier les variables d'environnement système »
2. Cliquez sur « Variables d'environnement »
3. Ajoutez ``JAVA_HOME`` : ``C:\Program Files\Eclipse Adoptium\jdk-21.x.x.x-hotspot``
4. Ajoutez ``%JAVA_HOME%\bin`` à ``PATH``

Installation de Maven
------------------

Installez Maven 3.x ou supérieur.

Téléchargement et installation
~~~~~~~~~~~~~~~~~~~~~~~~

1. Accédez à la `page de téléchargement Maven <https://maven.apache.org/download.cgi>`__
2. Téléchargez l'archive zip/tar.gz binaire
3. Décompressez et placez dans un emplacement approprié

**Linux/macOS:**

.. code-block:: bash

    tar xzvf apache-maven-3.x.x-bin.tar.gz
    sudo mv apache-maven-3.x.x /opt/
    sudo ln -s /opt/apache-maven-3.x.x /opt/maven

**Windows:**

1. Décompressez le fichier ZIP
2. Placez dans ``C:\Program Files\Apache\maven`` etc.

Configuration des variables d'environnement
~~~~~~~~~~~~

**Linux/macOS:**

Ajoutez ce qui suit à ``~/.bashrc`` ou ``~/.zshrc`` :

.. code-block:: bash

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH

**Windows:**

1. Ajoutez ``MAVEN_HOME`` : ``C:\Program Files\Apache\maven``
2. Ajoutez ``%MAVEN_HOME%\bin`` à ``PATH``

Vérification de l'installation
~~~~~~~~~~~~~~

.. code-block:: bash

    mvn -version

Si la sortie suivante s'affiche, c'est réussi :

.. code-block:: text

    Apache Maven 3.x.x
    Maven home: /opt/maven
    Java version: 21.0.x, vendor: Eclipse Adoptium

Installation de Git
----------------

Si Git n'est pas installé, installez-le depuis les sources suivantes.

- **Windows** : `Git for Windows <https://git-scm.com/download/win>`__
- **macOS** : ``brew install git`` ou `page de téléchargement Git <https://git-scm.com/download/mac>`__
- **Linux** : ``sudo apt install git`` (Ubuntu/Debian) ou ``sudo yum install git`` (RHEL/CentOS)

Vérification de l'installation :

.. code-block:: bash

    git --version

Configuration de l'IDE
===============

Cas d'Eclipse
------------

Eclipse est l'IDE recommandé dans la documentation officielle de |Fess|.

Installation d'Eclipse
~~~~~~~~~~~~~~~~~~~~

1. Accédez à la `page de téléchargement Eclipse <https://www.eclipse.org/downloads/>`__
2. Téléchargez « Eclipse IDE for Enterprise Java and Web Developers »
3. Exécutez l'installateur et suivez les instructions pour installer

Plugins recommandés
~~~~~~~~~~~~

Eclipse inclut les plugins suivants par défaut :

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

Importation du projet
~~~~~~~~~~~~~~~~~~~~

1. Lancez Eclipse
2. Sélectionnez ``File`` > ``Import``
3. Sélectionnez ``Maven`` > ``Existing Maven Projects``
4. Spécifiez le répertoire du code source Fess
5. Cliquez sur ``Finish``

Configuration de l'exécution
~~~~~~~~~~~~

1. Sélectionnez ``Run`` > ``Run Configurations...``
2. Cliquez droit sur ``Java Application`` et sélectionnez ``New Configuration``
3. Configurez ce qui suit :

   - **Name** : Fess Boot
   - **Project** : fess
   - **Main class** : ``org.codelibs.fess.FessBoot``

4. Cliquez sur ``Apply``

Cas d'IntelliJ IDEA
-------------------

IntelliJ IDEA est également un IDE largement utilisé.

Installation d'IntelliJ IDEA
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Accédez à la `page de téléchargement IntelliJ IDEA <https://www.jetbrains.com/idea/download/>`__
2. Téléchargez Community Edition (gratuit) ou Ultimate Edition
3. Exécutez l'installateur et suivez les instructions pour installer

Importation du projet
~~~~~~~~~~~~~~~~~~~~

1. Lancez IntelliJ IDEA
2. Sélectionnez ``Open``
3. Sélectionnez ``pom.xml`` du répertoire du code source Fess
4. Cliquez sur ``Open as Project``
5. Il sera automatiquement importé comme projet Maven

Configuration de l'exécution
~~~~~~~~~~~~

1. Sélectionnez ``Run`` > ``Edit Configurations...``
2. Cliquez sur le bouton ``+`` et sélectionnez ``Application``
3. Configurez ce qui suit :

   - **Name** : Fess Boot
   - **Module** : fess
   - **Main class** : ``org.codelibs.fess.FessBoot``
   - **JRE** : Java 21

4. Cliquez sur ``OK``

Cas de VS Code
------------

VS Code est également une option si vous préférez un environnement de développement léger.

Installation de VS Code
~~~~~~~~~~~~~~~~~~~~

1. Accédez à la `page de téléchargement VS Code <https://code.visualstudio.com/>`__
2. Téléchargez et exécutez l'installateur

Installation des extensions nécessaires
~~~~~~~~~~~~~~~~~~~~~~~~

Installez les extensions suivantes :

- **Extension Pack for Java** : Ensemble d'extensions nécessaires pour le développement Java
- **Maven for Java** : Support Maven

Ouvrir le projet
~~~~~~~~~~~~~~~~

1. Lancez VS Code
2. Sélectionnez ``File`` > ``Open Folder``
3. Sélectionnez le répertoire du code source Fess

Obtention du code source
==============

Clonage depuis GitHub
-------------------

Clonez le code source de |Fess| depuis GitHub.

.. code-block:: bash

    git clone https://github.com/codelibs/fess.git
    cd fess

Pour utiliser SSH :

.. code-block:: bash

    git clone git@github.com:codelibs/fess.git
    cd fess

.. tip::

   Pour développer en forkant, forkez d'abord le dépôt Fess sur GitHub,
   puis clonez le dépôt forké :

   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/fess.git
       cd fess
       git remote add upstream https://github.com/codelibs/fess.git

Compilation du projet
==================

Téléchargement des plugins OpenSearch
---------------------------------

Les plugins OpenSearch sont nécessaires pour exécuter Fess.
Téléchargez-les avec la commande suivante :

.. code-block:: bash

    mvn antrun:run

Cette commande effectue les opérations suivantes :

- Téléchargement d'OpenSearch
- Téléchargement et installation des plugins requis
- Configuration d'OpenSearch

.. note::

   Cette commande doit être exécutée uniquement lors de la première fois ou lors de la mise à jour des plugins.
   Il n'est pas nécessaire de l'exécuter à chaque fois.

Première compilation
--------

Compilez le projet :

.. code-block:: bash

    mvn clean compile

La première compilation peut prendre du temps (téléchargement des bibliothèques dépendantes, etc.).

Si la compilation réussit, le message suivant s'affiche :

.. code-block:: text

    [INFO] BUILD SUCCESS
    [INFO] Total time: xx:xx min
    [INFO] Finished at: 2024-xx-xxTxx:xx:xx+09:00

Exécution de Fess
==========

Exécution depuis la ligne de commande
--------------------

Exécutez avec Maven :

.. code-block:: bash

    mvn compile exec:java

Ou empaquez puis exécutez :

.. code-block:: bash

    mvn package
    java -jar target/fess-15.3.x.jar

Exécution depuis l'IDE
------------

Cas d'Eclipse
~~~~~~~~~~~~

1. Cliquez droit sur la classe ``org.codelibs.fess.FessBoot``
2. Sélectionnez ``Run As`` > ``Java Application``

Ou utilisez la configuration d'exécution créée :

1. Cliquez sur le menu déroulant du bouton d'exécution dans la barre d'outils
2. Sélectionnez ``Fess Boot``

Cas d'IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Cliquez droit sur la classe ``org.codelibs.fess.FessBoot``
2. Sélectionnez ``Run 'FessBoot.main()'``

Ou utilisez la configuration d'exécution créée :

1. Cliquez sur le menu déroulant du bouton d'exécution dans la barre d'outils
2. Sélectionnez ``Fess Boot``

Cas de VS Code
~~~~~~~~~~~~

1. Ouvrez ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Sélectionnez ``Run Without Debugging`` dans le menu ``Run``

Vérification du démarrage
--------

Le démarrage de Fess prend 1 à 2 minutes.
Le démarrage est terminé lorsque les journaux suivants s'affichent dans la console :

.. code-block:: text

    [INFO] Boot Thread: Boot process completed successfully.

Vérifiez le fonctionnement en accédant aux URL suivantes dans le navigateur :

- **Écran de recherche** : http://localhost:8080/
- **Écran d'administration** : http://localhost:8080/admin/

  - Utilisateur par défaut : ``admin``
  - Mot de passe par défaut : ``admin``

Changement du numéro de port
--------------

Si le port par défaut 8080 est utilisé, vous pouvez le changer dans le fichier suivant :

``src/main/resources/fess_config.properties``

.. code-block:: properties

    # Changer le numéro de port
    server.port=8080

Exécution en débogage
==========

Exécution en débogage dans l'IDE
------------------

Cas d'Eclipse
~~~~~~~~~~~~

1. Cliquez droit sur la classe ``org.codelibs.fess.FessBoot``
2. Sélectionnez ``Debug As`` > ``Java Application``
3. Définissez des points d'arrêt et suivez le comportement du code

Cas d'IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Cliquez droit sur la classe ``org.codelibs.fess.FessBoot``
2. Sélectionnez ``Debug 'FessBoot.main()'``
3. Définissez des points d'arrêt et suivez le comportement du code

Cas de VS Code
~~~~~~~~~~~~

1. Ouvrez ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Sélectionnez ``Start Debugging`` dans le menu ``Run``

Débogage à distance
--------------

Vous pouvez également connecter un débogueur à Fess démarré depuis la ligne de commande.

Démarrez Fess en mode débogage :

.. code-block:: bash

    mvn compile exec:java -Dexec.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

Connexion de débogage à distance depuis l'IDE :

**Eclipse:**

1. Sélectionnez ``Run`` > ``Debug Configurations...``
2. Cliquez droit sur ``Remote Java Application`` et sélectionnez ``New Configuration``
3. Configurez ``Port: 5005``
4. Cliquez sur ``Debug``

**IntelliJ IDEA:**

1. Sélectionnez ``Run`` > ``Edit Configurations...``
2. Sélectionnez ``+`` > ``Remote JVM Debug``
3. Configurez ``Port: 5005``
4. Cliquez sur ``OK`` et exécutez ``Debug``

Paramètres utiles pour le développement
==============

Changement du niveau de journalisation
--------------

Changer le niveau de journalisation lors du débogage permet de vérifier des informations détaillées.

Modifiez ``src/main/resources/log4j2.xml`` :

.. code-block:: xml

    <Configuration status="INFO">
        <Loggers>
            <Logger name="org.codelibs.fess" level="DEBUG"/>
            <Root level="INFO">
                <AppenderRef ref="console"/>
            </Root>
        </Loggers>
    </Configuration>

Activation du hot deploy
-------------------

LastaFlute peut refléter certaines modifications sans redémarrage.

Configurez ce qui suit dans ``src/main/resources/fess_config.properties`` :

.. code-block:: properties

    # Activer le hot deploy
    development.here=true

Cependant, les modifications suivantes nécessitent un redémarrage :

- Modifications de la structure de classe (ajout/suppression de méthodes, etc.)
- Modifications des fichiers de configuration
- Modifications des bibliothèques dépendantes

Manipulation d'OpenSearch intégré
------------------------

Dans l'environnement de développement, OpenSearch intégré est utilisé.

Emplacement d'OpenSearch :

.. code-block:: text

    target/fess/es/

Accès direct à l'API OpenSearch :

.. code-block:: bash

    # Liste des index
    curl -X GET http://localhost:9201/_cat/indices?v

    # Recherche de documents
    curl -X GET http://localhost:9201/fess.search/_search?pretty

    # Vérification du mapping
    curl -X GET http://localhost:9201/fess.search/_mapping?pretty

Utilisation d'OpenSearch externe
--------------------

Pour utiliser un serveur OpenSearch externe,
modifiez ``src/main/resources/fess_config.properties`` :

.. code-block:: properties

    # Désactiver OpenSearch intégré
    opensearch.cluster.name=fess
    opensearch.http.url=http://localhost:9200

Génération de code par DBFlute
======================

|Fess| utilise DBFlute pour générer automatiquement
le code Java à partir du schéma OpenSearch.

Régénération en cas de modification du schéma
----------------------------

Si vous modifiez le mapping OpenSearch, régénérez
le code Java correspondant avec les commandes suivantes :

.. code-block:: bash

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format

Explication de chaque commande :

- ``rm -rf mydbflute`` : Supprime le répertoire de travail DBFlute existant
- ``mvn antrun:run`` : Télécharge les plugins OpenSearch
- ``mvn dbflute:freegen`` : Génère le code Java à partir du schéma
- ``mvn license:format`` : Ajoute les en-têtes de licence

Dépannage
==================

Erreurs de compilation
----------

**Erreur : Version Java obsolète**

.. code-block:: text

    [ERROR] Failed to execute goal ... requires at least Java 21

Solution : Installez Java 21 ou supérieur et configurez correctement ``JAVA_HOME``.

**Erreur : Échec du téléchargement des bibliothèques dépendantes**

.. code-block:: text

    [ERROR] Failed to collect dependencies

Solution : Vérifiez la connexion réseau, nettoyez le dépôt local Maven et réessayez :

.. code-block:: bash

    rm -rf ~/.m2/repository
    mvn clean compile

Erreurs d'exécution
--------

**Erreur : Port 8080 déjà utilisé**

.. code-block:: text

    Address already in use

Solution :

1. Terminez le processus utilisant le port 8080
2. Ou changez le numéro de port dans ``fess_config.properties``

**Erreur : OpenSearch ne démarre pas**

Vérifiez les fichiers journaux ``target/fess/es/logs/``.

Causes courantes :

- Mémoire insuffisante : Augmentez la taille du tas JVM
- Port 9201 utilisé : Changez le numéro de port
- Espace disque insuffisant : Libérez de l'espace disque

Projet non reconnu dans l'IDE
----------------------------

**Mise à jour du projet Maven**

- **Eclipse** : Cliquez droit sur le projet > ``Maven`` > ``Update Project``
- **IntelliJ IDEA** : Cliquez sur ``Reload All Maven Projects`` dans la fenêtre d'outil ``Maven``
- **VS Code** : Exécutez ``Java: Clean Java Language Server Workspace`` depuis la palette de commandes

Étapes suivantes
==========

Une fois la configuration de l'environnement de développement terminée, consultez la documentation suivante :

- :doc:`architecture` - Compréhension de la structure du code
- :doc:`workflow` - Apprentissage du flux de développement
- :doc:`building` - Méthodes de compilation et de test
- :doc:`contributing` - Création de pull requests

Ressources
========

- `Téléchargement Eclipse <https://www.eclipse.org/downloads/>`__
- `Téléchargement IntelliJ IDEA <https://www.jetbrains.com/idea/download/>`__
- `Téléchargement VS Code <https://code.visualstudio.com/>`__
- `Documentation Maven <https://maven.apache.org/guides/>`__
- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
