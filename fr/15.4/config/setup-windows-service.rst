===================
Enregistrement en tant que service Windows
===================

Enregistrement en tant que service Windows
======================

|Fess| peut être enregistré en tant que service Windows.
Pour exécuter |Fess|, OpenSearch doit être démarré au préalable.
Nous supposons ici que |Fess| est installé dans ``c:\opt\fess`` et OpenSearch dans ``c:\opt\opensearch``.

Préparation préalable
------

Veuillez définir JAVA_HOME comme variable d'environnement système.

Enregistrement d'OpenSearch en tant que service
-------------------------

| Exécutez ``c:\opt\opensearch\bin\opensearch-service.bat`` en tant qu'administrateur depuis l'invite de commandes.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

Pour plus de détails, consultez la `documentation OpenSearch <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_.

Configuration
----

Éditez ``c:\opt\fess\bin\fess.in.bat`` et configurez SEARCH_ENGINE_HOME avec le répertoire d'installation d'OpenSearch.

::

    set SEARCH_ENGINE_HOME=c:/opt/opensearch

Le numéro de port par défaut pour l'interface de recherche et d'administration de |Fess| est 8080. Pour le changer en 80, modifiez fess.port dans ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80


Méthode d'enregistrement
------

Exécutez ``c:\opt\fess\bin\service.bat`` en tant qu'administrateur depuis l'invite de commandes.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.


Configuration du service
-----------

Pour démarrer le service manuellement, démarrez d'abord le service OpenSearch, puis démarrez le service |Fess|.
Pour un démarrage automatique, ajoutez une dépendance.

1. Dans les paramètres généraux du service, définissez le type de démarrage sur « Automatique (début différé) ».
2. Les dépendances du service sont configurées dans le registre.

Ajoutez la clé et la valeur suivantes dans l'éditeur de registre (regedit).

.. list-table::

   * - *Clé*
     - ``Ordinateur\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services \fess-service-x64\DependOnService``
   * - *Valeur*
     - ``opensearch-service-x64``

Une fois ajouté, opensearch-service-x64 apparaîtra dans les dépendances des propriétés du service |Fess|.
