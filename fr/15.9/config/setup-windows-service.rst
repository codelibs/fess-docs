==========================================
Enregistrement en tant que service Windows
==========================================

Enregistrement en tant que service Windows
==========================================

|Fess| peut être enregistré en tant que service Windows. L'enregistrement en tant que service permet de démarrer automatiquement |Fess| au démarrage du système.
Pour exécuter |Fess|, OpenSearch doit être démarré au préalable.
Nous supposons ici que |Fess| est installé dans ``c:\opt\fess`` et OpenSearch dans ``c:\opt\opensearch`` (adaptez les chemins à votre environnement).

.. note::
   |Fess| et OpenSearch ne prennent en charge que les versions 64 bits.

Préparation préalable
---------------------

Veuillez définir ``JAVA_HOME`` comme variable d'environnement système. ``service.bat`` se termine avec une erreur si ``JAVA_HOME`` n'est pas défini.

Enregistrement d'OpenSearch en tant que service
-----------------------------------------------

Ouvrez une invite de commandes avec des droits d'administrateur et exécutez ``c:\opt\opensearch\bin\opensearch-service.bat``.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

Pour plus de détails, consultez la `documentation OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/windows/>`_.

Configuration de |Fess|
-----------------------

Le service est enregistré depuis ``c:\opt\fess\bin\service.bat``. Lors de l'enregistrement, ``service.bat`` lit ``bin\fess.in.bat`` et applique son contenu aux options de démarrage de |Fess|.
Ajoutez la configuration de connexion à OpenSearch dans ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=c:/opt/opensearch/data/config/

.. note::
   - ``fess.search_engine.http_address`` permet de spécifier la destination de connexion du service OpenSearch enregistré. Sans cette configuration, |Fess| ne peut pas trouver la destination de connexion et démarre une instance OpenSearch embarquée, déconseillée en environnement de production.
   - Si vous exécutez OpenSearch sur un hôte différent, modifiez le nom d'hôte ou l'adresse IP en conséquence.
   - Utilisez ``/`` comme séparateur de chemin.

Le numéro de port par défaut pour l'interface de recherche et d'administration de |Fess| est ``8080``. Pour le changer, modifiez ``-Dfess.port`` dans ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

.. note::
   Lors de l'enregistrement en tant que service, ``-Dfess.port=8080`` est également codé en dur dans ``FESS_PARAMS`` dans ``bin\service.bat``. Cette valeur est prioritaire sur la configuration de ``fess.in.bat``. Par conséquent, lors du changement de port, modifiez également ``FESS_PARAMS`` dans ``service.bat``.

Personnalisation du service (facultatif)
----------------------------------------

Vous pouvez modifier la configuration du service en définissant des variables d'environnement avant d'exécuter ``service.bat install``. Les principales variables d'environnement sont les suivantes.

.. list-table::
   :header-rows: 1

   * - Variable d'environnement
     - Description
   * - ``FESS_START_TYPE``
     - Type de démarrage (``auto`` ou ``manual``). La valeur par défaut est ``manual``.
   * - ``FESS_HEAP_SIZE``
     - Taille du tas (ex. : ``1g``). Pour spécifier séparément la taille minimale et maximale du tas, utilisez ``FESS_MIN_MEM`` (valeur par défaut ``256m``) et ``FESS_MAX_MEM`` (valeur par défaut ``1g``).
   * - ``SERVICE_USERNAME`` / ``SERVICE_PASSWORD``
     - Compte Windows sous lequel le service s'exécute.
   * - ``SERVICE_DISPLAY_NAME``
     - Nom d'affichage du service.
   * - ``SERVICE_DESCRIPTION``
     - Description du service.

Procédure d'enregistrement
---------------------------

Exécutez ``c:\opt\fess\bin\service.bat`` depuis une invite de commandes avec des droits d'administrateur.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

Configuration du service
------------------------

Pour démarrer le service manuellement, démarrez d'abord le service OpenSearch, puis démarrez le service |Fess|.
Pour un démarrage automatique au démarrage du système, configurez le type de démarrage et les dépendances.

1. Dans les paramètres généraux du service, définissez le type de démarrage sur « Automatique (début différé) ».
2. Les dépendances du service sont configurées dans le registre.

Ajoutez la clé et la valeur suivantes dans l'éditeur de registre (regedit).

.. list-table::

   * - *Clé*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *Valeur*
     - ``opensearch-service-x64``

Une fois ajouté, opensearch-service-x64 apparaîtra dans les dépendances des propriétés du service |Fess|.

.. note::
   En définissant la variable d'environnement ``FESS_START_TYPE=auto`` avant ``service.bat install``, vous pouvez enregistrer le type de démarrage sur « Automatique ». Cependant, « Automatique (début différé) » et la configuration des dépendances ne peuvent pas être effectués via ``service.bat`` ; veuillez les configurer selon la procédure décrite ci-dessus.

Gestion du service
------------------

Avec ``service.bat``, vous pouvez gérer le service à l'aide des commandes suivantes.

.. list-table::
   :header-rows: 1

   * - Commande
     - Description
   * - ``service.bat install``
     - Enregistre le service.
   * - ``service.bat remove``
     - Supprime le service.
   * - ``service.bat start``
     - Démarre le service.
   * - ``service.bat stop``
     - Arrête le service.
   * - ``service.bat manager``
     - Lance l'interface graphique de gestion du service.
