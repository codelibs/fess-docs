==================
Configuration des journaux
==================

Aperçu
====

|Fess| génère plusieurs fichiers journaux pour enregistrer l'état de fonctionnement du système et les informations d'erreur.
Une configuration appropriée des journaux facilite le dépannage et la surveillance du système.

Types de fichiers journaux
==================

Fichiers journaux principaux
------------------

Les principaux fichiers journaux générés par |Fess| sont les suivants.

.. list-table:: Liste des fichiers journaux
   :header-rows: 1
   :widths: 25 75

   * - Nom du fichier
     - Contenu
   * - ``fess.log``
     - Journaux d'opérations dans l'interface d'administration et de recherche, erreurs d'application, événements système
   * - ``fess_crawler.log``
     - Journaux lors de l'exécution de l'exploration, URL explorées, informations sur les documents récupérés, erreurs
   * - ``fess_suggest.log``
     - Journaux lors de la génération de suggestions (candidats de recherche), informations de mise à jour d'index
   * - ``server_?.log``
     - Journaux système du serveur d'applications comme Tomcat
   * - ``audit.log``
     - Journaux d'audit pour l'authentification des utilisateurs, connexion/déconnexion, opérations importantes

Emplacement des fichiers journaux
------------------

**Pour l'installation Zip :**

::

    {FESS_HOME}/logs/

**Pour les paquets RPM/DEB :**

::

    /var/log/fess/

Vérification des journaux lors du dépannage
----------------------------------

En cas de problème, vérifiez les journaux en suivant ces étapes.

1. **Identifier le type d'erreur**

   - Erreur d'application → ``fess.log``
   - Erreur d'exploration → ``fess_crawler.log``
   - Erreur d'authentification → ``audit.log``
   - Erreur de serveur → ``server_?.log``

2. **Vérifier les erreurs les plus récentes**

   ::

       tail -f /var/log/fess/fess.log

3. **Rechercher des erreurs spécifiques**

   ::

       grep -i "error" /var/log/fess/fess.log
       grep -i "exception" /var/log/fess/fess.log

4. **Vérifier le contexte de l'erreur**

   En vérifiant les journaux avant et après l'erreur, vous pouvez identifier la cause.

   ::

       grep -B 10 -A 10 "OutOfMemoryError" /var/log/fess/fess.log

Configuration du niveau de journalisation
================

À propos des niveaux de journalisation
--------------

Les niveaux de journalisation contrôlent le niveau de détail des journaux générés.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Niveau
     - Description
   * - ``FATAL``
     - Erreur fatale (l'application ne peut pas continuer)
   * - ``ERROR``
     - Erreur (une partie des fonctionnalités ne fonctionne pas)
   * - ``WARN``
     - Avertissement (problème potentiel)
   * - ``INFO``
     - Information (événement important)
   * - ``DEBUG``
     - Informations de débogage (journaux de fonctionnement détaillés)
   * - ``TRACE``
     - Informations de trace (le plus détaillé)

Niveaux de journalisation recommandés
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Environnement
     - Niveau recommandé
     - Raison
   * - Environnement de production
     - ``WARN``
     - Priorité aux performances et à l'espace disque
   * - Environnement de staging
     - ``INFO``
     - Enregistrer les événements importants
   * - Environnement de développement
     - ``DEBUG``
     - Informations de débogage détaillées nécessaires
   * - Lors de l'investigation de problèmes
     - ``DEBUG`` ou ``TRACE``
     - Activer temporairement les journaux détaillés

Modification via l'interface d'administration
------------------

La méthode la plus simple consiste à modifier via l'interface d'administration.

1. Connectez-vous à l'interface d'administration.
2. Sélectionnez « Général » dans le menu « Système ».
3. Sélectionnez le niveau souhaité dans « Niveau de journalisation ».
4. Cliquez sur le bouton « Mettre à jour ».

.. note::
   Les modifications dans l'interface d'administration sont conservées même après le redémarrage de |Fess|.

Modification via le fichier de configuration
----------------------

Pour une configuration plus détaillée des journaux, modifiez le fichier de configuration Log4j2.

Emplacement du fichier de configuration
~~~~~~~~~~~~~~~~~~

- **Installation Zip** : ``app/WEB-INF/classes/log4j2.xml``
- **Paquets RPM/DEB** : ``/etc/fess/log4j2.xml``

Exemples de configuration de base
~~~~~~~~~~~~~~

**Niveau de journalisation par défaut :**

::

    <Logger name="org.codelibs.fess" level="warn"/>

**Exemple : Changement au niveau DEBUG**

::

    <Logger name="org.codelibs.fess" level="debug"/>

**Exemple : Modification du niveau de journalisation pour un paquet spécifique**

::

    <Logger name="org.codelibs.fess.crawler" level="info"/>
    <Logger name="org.codelibs.fess.ds" level="debug"/>
    <Logger name="org.codelibs.fess.app.web" level="warn"/>

.. warning::
   Les niveaux ``DEBUG`` et ``TRACE`` génèrent une grande quantité de journaux,
   ne les utilisez pas en environnement de production. Cela affecte l'espace disque et les performances.

Configuration via les variables d'environnement
~~~~~~~~~~~~~~~~~~

Vous pouvez également spécifier le niveau de journalisation lors du démarrage du système.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dlog.level=debug"

Configuration des journaux d'exploration
====================

Les journaux d'exploration sont générés au niveau ``INFO`` par défaut.

Configuration dans l'interface d'administration
----------------

1. Ouvrez la configuration d'exploration cible depuis le menu « Explorateur » de l'interface d'administration.
2. Sélectionnez « Script » dans l'onglet « Configuration ».
3. Ajoutez ce qui suit dans le champ script.

::

    logLevel("DEBUG")

Valeurs configurables :

- ``FATAL``
- ``ERROR``
- ``WARN``
- ``INFO``
- ``DEBUG``
- ``TRACE``

Modification du niveau de journalisation uniquement pour des modèles d'URL spécifiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    if (url.contains("example.com")) {
        logLevel("DEBUG")
    }

Modification du niveau de journalisation pour l'ensemble du processus d'exploration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration dans ``fess_config.properties`` :

::

    logging.level.org.codelibs.fess.crawler=DEBUG

Rotation des journaux
==================

Aperçu
----

Les fichiers journaux grossissent avec le temps, une rotation régulière (gestion des générations) est donc nécessaire.

Rotation automatique avec Log4j2
-------------------------------

|Fess| utilise le RollingFileAppender de Log4j2 pour effectuer automatiquement la rotation des journaux.

Configuration par défaut
~~~~~~~~~~~~~~~~

- **Taille du fichier** : Rotation lorsque 10 Mo sont dépassés
- **Nombre de générations conservées** : Maximum 10 fichiers

Exemple de fichier de configuration (``log4j2.xml``) :

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%i">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <SizeBasedTriggeringPolicy size="10MB"/>
        </Policies>
        <DefaultRolloverStrategy max="10"/>
    </RollingFile>

Configuration de rotation quotidienne
~~~~~~~~~~~~~~~~~~~~~~~~

Pour une rotation quotidienne plutôt que par taille :

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

Configuration de compression
~~~~~~~~

Pour compresser automatiquement lors de la rotation :

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}.gz">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

Rotation avec logrotate
------------------------------

Dans un environnement Linux, vous pouvez également gérer la rotation des journaux avec logrotate.

Exemple de ``/etc/logrotate.d/fess`` :

::

    /var/log/fess/*.log {
        daily
        rotate 14
        compress
        delaycompress
        missingok
        notifempty
        create 0644 fess fess
        sharedscripts
        postrotate
            systemctl reload fess > /dev/null 2>&1 || true
        endscript
    }

Explication de la configuration :

- ``daily`` : Rotation quotidienne
- ``rotate 14`` : Conserver 14 générations
- ``compress`` : Compresser les anciens journaux
- ``delaycompress`` : Ne pas compresser la génération précédente (l'application peut être en cours d'écriture)
- ``missingok`` : Pas d'erreur si le fichier journal n'existe pas
- ``notifempty`` : Ne pas effectuer de rotation pour les fichiers journaux vides
- ``create 0644 fess fess`` : Permissions et propriétaire du nouveau fichier journal

Surveillance des journaux
========

En environnement de production, il est recommandé de surveiller les fichiers journaux pour détecter rapidement les erreurs.

Modèles de journaux à surveiller
----------------------

Modèles d'erreurs importants
~~~~~~~~~~~~~~~~~~~~

- Journaux de niveau ``ERROR`` et ``FATAL``
- ``OutOfMemoryError``
- ``Connection refused``
- ``Timeout``
- ``Exception``
- ``circuit_breaker_exception``
- ``Too many open files``

Modèles d'alerte
~~~~~~~~~~~~~~~~~~

- Journaux de niveau ``WARN`` fréquents
- ``Retrying``
- ``Slow query``
- ``Queue full``

Surveillance en temps réel
----------------

Surveillance en temps réel avec la commande tail :

::

    tail -f /var/log/fess/fess.log | grep -i "error\|exception"

Surveillance simultanée de plusieurs fichiers journaux :

::

    tail -f /var/log/fess/*.log

Exemples d'outils de surveillance
--------------

**Logwatch**

Analyse et rapport périodiques des fichiers journaux.

::

    # Installation (CentOS/RHEL)
    yum install logwatch

    # Envoi de rapport quotidien
    logwatch --service fess --mailto admin@example.com

**Logstash + OpenSearch + OpenSearch Dashboards**

Analyse de journaux en temps réel et visualisation.

**Fluentd**

Collecte et transfert de journaux.

::

    <source>
      @type tail
      path /var/log/fess/fess.log
      pos_file /var/log/fluentd/fess.log.pos
      tag fess.app
      <parse>
        @type multiline
        format_firstline /^\d{4}-\d{2}-\d{2}/
        format1 /^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?<thread>.*?)\] (?<level>\w+)\s+(?<logger>.*?) - (?<message>.*)/
      </parse>
    </source>

**Prometheus + Grafana**

Surveillance des métriques et alertes.

Configuration des alertes
------------

Exemple de notification lors de la détection d'erreur :

::

    # Script simple de notification par e-mail
    tail -n 0 -f /var/log/fess/fess.log | while read line; do
        echo "$line" | grep -i "error\|fatal" && \
        echo "$line" | mail -s "Fess Error Alert" admin@example.com
    done

Format des journaux
================

Format par défaut
----------------------

Format de journal par défaut de |Fess| :

::

    %d{ISO8601} [%t] %-5p %c - %m%n

Explication de chaque élément :

- ``%d{ISO8601}`` : Horodatage (format ISO8601)
- ``[%t]`` : Nom du thread
- ``%-5p`` : Niveau de journalisation (largeur de 5 caractères, aligné à gauche)
- ``%c`` : Nom du logger (nom du paquet)
- ``%m`` : Message
- ``%n`` : Saut de ligne

Exemples de formats personnalisés
----------------------

Sortie des journaux au format JSON
~~~~~~~~~~~~~~~~~~

::

    <PatternLayout>
        <pattern>{"timestamp":"%d{ISO8601}","thread":"%t","level":"%-5p","logger":"%c","message":"%m"}%n</pattern>
    </PatternLayout>

Inclure des informations plus détaillées
~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c{1.} [%F:%L] - %m%n"/>

Informations supplémentaires :

- ``%c{1.}`` : Nom de paquet abrégé
- ``%F`` : Nom du fichier
- ``%L`` : Numéro de ligne

Impact sur les performances
======================

La sortie des journaux affecte les E/S disque et les performances.

Bonnes pratiques
------------------

1. **Utiliser le niveau WARN ou supérieur en production**

   Éviter de générer des journaux détaillés inutiles.

2. **Nettoyage régulier des fichiers journaux**

   Supprimer ou compresser les anciens fichiers journaux.

3. **Utilisation de la sortie de journaux asynchrone**

   Utiliser l'appender asynchrone de Log4j2 pour réduire la surcharge de sortie des journaux.

   ::

       <Async name="AsyncFile">
           <AppenderRef ref="FessFile"/>
       </Async>

4. **Assurer un espace disque suffisant**

   Assurer un espace disque suffisant pour les fichiers journaux.

5. **Sélection appropriée du niveau de journalisation**

   Configurer le niveau de journalisation en fonction de l'environnement.

Mesure des performances
------------------

Mesurer l'impact de la sortie des journaux :

::

    # Vérifier la quantité de journaux générés
    du -sh /var/log/fess/

    # Augmentation des journaux par heure
    watch -n 3600 'du -sh /var/log/fess/'

Dépannage
======================

Les journaux ne sont pas générés
------------------

**Causes et solutions :**

1. **Permissions du répertoire des journaux**

   ::

       ls -ld /var/log/fess/
       # Modifier les permissions si nécessaire
       sudo chown -R fess:fess /var/log/fess/
       sudo chmod 755 /var/log/fess/

2. **Espace disque**

   ::

       df -h /var/log
       # En cas d'espace insuffisant, supprimer les anciens journaux
       find /var/log/fess/ -name "*.log.*" -mtime +30 -delete

3. **Fichier de configuration Log4j2**

   ::

       # Vérifier la syntaxe du fichier de configuration
       xmllint --noout /etc/fess/log4j2.xml

4. **Vérifier SELinux**

   ::

       # Si SELinux est activé
       getenforce
       # Définir le contexte si nécessaire
       restorecon -R /var/log/fess/

Le fichier journal devient trop volumineux
------------------------------

1. **Ajuster le niveau de journalisation**

   Définir au niveau ``WARN`` ou supérieur.

2. **Vérifier la configuration de rotation des journaux**

   ::

       # Vérifier la configuration de log4j2.xml
       grep -A 5 "RollingFile" /etc/fess/log4j2.xml

3. **Désactiver les sorties de journaux inutiles**

   ::

       # Supprimer les journaux pour un paquet spécifique
       <Logger name="org.apache.http" level="error"/>

4. **Solution temporaire**

   ::

       # Compresser les anciens fichiers journaux
       gzip /var/log/fess/fess.log.[1-9]

       # Supprimer les anciens fichiers journaux
       find /var/log/fess/ -name "*.log.*" -mtime +7 -delete

Impossible de trouver un journal spécifique
------------------------

1. **Vérifier le niveau de journalisation**

   Si le niveau de journalisation est trop bas, il ne sera pas généré.

   ::

       grep "org.codelibs.fess" /etc/fess/log4j2.xml

2. **Vérifier le chemin du fichier journal**

   ::

       # Vérifier la destination réelle de sortie des journaux
       ps aux | grep fess
       lsof -p <PID> | grep log

3. **Vérifier l'horodatage**

   Vérifiez que l'heure système est correcte.

   ::

       date
       timedatectl status

4. **Mise en mémoire tampon des journaux**

   Les journaux peuvent ne pas être écrits immédiatement.

   ::

       # Forcer le vidage des journaux
       systemctl reload fess

Caractères corrompus dans les journaux
------------------------

1. **Configuration de l'encodage**

   Spécifier l'encodage des caractères dans ``log4j2.xml`` :

   ::

       <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n" charset="UTF-8"/>

2. **Configuration des variables d'environnement**

   ::

       export LANG=ja_JP.UTF-8
       export LC_ALL=ja_JP.UTF-8

Informations de référence
========

- :doc:`setup-memory` - Configuration de la mémoire
- :doc:`crawler-advanced` - Configuration avancée de l'explorateur
- :doc:`admin-index-backup` - Sauvegarde de l'index
- `Documentation Log4j2 <https://logging.apache.org/log4j/2.x/>`_
