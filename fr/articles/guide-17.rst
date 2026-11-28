=============================
Étendre Fess avec des plugins
=============================

Introduction
============

Lorsqu'aucun plugin ``fess-ds-*`` ne convient à votre système interne, ou lorsque vous voulez traiter tous les documents avant leur indexation, vous écrivez votre propre plugin.
Cet article s'adresse aux développeurs Java. Il explique comment créer, à partir d'un modèle officiel, un plugin qui fonctionne sur Fess 15.9, l'installer et vérifier son fonctionnement.

En suivant les étapes de cet article, vous saurez :

- comprendre les types de plugins et la façon dont Fess les distingue ;
- construire un plugin de magasin de données à partir de ``fess-ds-example``, l'intégrer à Fess et indexer des documents avec ;
- créer, à partir de ``fess-ingest-example``, un Ingester qui traite les documents avant leur indexation.

Nous supposons que Java 21 ou ultérieur et Maven 3 sont disponibles, et que Fess 15.9 est en cours d'exécution (:doc:`guide-02`).
L'utilisation de l'écran de configuration des magasins de données est expliquée dans :doc:`datastore-basics` ; le lire d'abord rend les étapes plus faciles à suivre.

Types de plugins
================

Un plugin est un fichier jar placé dans ``app/WEB-INF/plugin/`` sous le répertoire d'installation de Fess.
Fess détermine le type d'un plugin d'après le début (préfixe) du nom du fichier jar (``PluginHelper.ArtifactType``).
Les types disponibles en 15.9 sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 22 43 35

   * - Préfixe
     - Rôle
     - Dépôt de référence
   * - ``fess-ds``
     - Magasin de données. Récupère des enregistrements dans un système externe et les indexe
     - ``fess-ds-example``
   * - ``fess-ingest``
     - Ingester. Traite les documents avant leur indexation
     - ``fess-ingest-example``
   * - ``fess-script``
     - Moteur de script
     - ``fess-script-groovy``
   * - ``fess-webapp``
     - Extension de l'application web (ajout d'API ou de points de terminaison)
     - ``fess-webapp-mcp``
   * - ``fess-thumbnail``
     - Génération de vignettes
     - ``fess-thumbnail-playwright``
   * - ``fess-crawler``
     - Client du robot d'exploration
     - ``fess-crawler-playwright``
   * - ``fess-llm``
     - Fournisseur LLM utilisé par le mode de recherche IA
     - ``fess-llm-openai``
   * - ``fess-storage``
     - Stockage objet (S3 / GCS)
     - ``fess-storage-s3``
   * - ``fess-sso``
     - Méthode d'authentification pour l'authentification unique (SSO)
     - ``fess-sso-oidc``

Tous ces dépôts sont publiés sur https://github.com/codelibs.

L'apparence de la page de recherche ne se modifie pas avec des plugins.
Les plugins de thème JAR ``fess-theme-*``, qui remplaçaient les JSP, ont été supprimés en 15.9 ; la page de recherche est désormais un thème ZIP composé de ``theme.yml``, ``index.html`` et ``assets/``.
Les thèmes se téléversent depuis [Système] > [Thème].
Pour en créer un, consultez le `Guide de développement des thèmes <https://fess.codelibs.org/fr/stable/dev/theme-development.html>`__ ; pour intégrer la recherche à un site existant, consultez :doc:`guide-03`.

Créer un plugin de magasin de données
=====================================

Récupérer le modèle
-------------------

``fess-ds-example`` est un dépôt publié comme squelette de plugin de magasin de données.
Sa branche par défaut suit la version en cours de développement (15.10.0-SNAPSHOT) ; pour construire pour 15.9, utilisez le commit aligné sur 15.9.0.

::

    $ git clone https://github.com/codelibs/fess-ds-example.git
    $ cd fess-ds-example
    $ git checkout 0252a8b08d7de4eeea7a88c52aa884094ef099be

Ce commit ne diffère de la branche par défaut que par deux lignes de ``pom.xml`` (la version du projet et celle du POM parent).
Vous obtenez le même résultat en restant sur la branche par défaut et en modifiant pour 15.9 les deux emplacements décrits dans la section suivante.

pom.xml
-------

Les parties essentielles de ``pom.xml`` sont les suivantes.

.. code-block:: xml

    <artifactId>fess-ds-example</artifactId>
    <packaging>jar</packaging>
    <version>15.9.0-SNAPSHOT</version>

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.9.0</version>
        <relativePath />
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.opensearch</groupId>
            <artifactId>opensearch</artifactId>
            <version>${opensearch.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

Alignez la version de ``fess-parent`` sur la version de Fess dans laquelle le plugin sera installé.
Dans ``fess-parent`` 15.9.0, ``fess.version`` vaut ``15.9.0`` : le plugin est donc compilé avec l'API de Fess 15.9.0.
Fess lui-même et les classes OpenSearch sont fournis par Fess à l'exécution ; ils sont donc en ``provided``.
Le ``pom.xml`` réel contient aussi d'autres dépendances et paramètres de construction ; commencez par l'utiliser tel quel.
Le jar ``fess`` n'est pas récupéré depuis Maven Central, mais depuis le dépôt CodeLibs déclaré par ``fess-parent`` (``https://maven.codelibs.org/release/``).
Dans un environnement qui passe par un proxy ou un miroir, assurez-vous que ce dépôt est accessible.

Lorsque vous en faites votre propre plugin, commencez toujours l'``artifactId`` par ``fess-ds-``.
Comme expliqué plus loin, les choix proposés pour « Nom du gestionnaire » dans la console d'administration ne sont collectés qu'à partir des jars dont le nom de fichier commence par ``fess-ds``.

Classe du magasin de données
----------------------------

Un magasin de données hérite de ``org.codelibs.fess.ds.AbstractDataStore`` et implémente ``getName()`` et ``storeData(...)``.
Voici ``ExampleDataStore`` réduit au squelette de son traitement.
Il sert à comprendre le fonctionnement ; pour la construction, utilisez tel quel le ``ExampleDataStore`` du dépôt (les tests utilisent des méthodes absentes du squelette, si bien que remplacer la classe fait échouer la compilation des tests).

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.HashMap;
    import java.util.LinkedHashMap;
    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback, final DataStoreParams paramMap,
                final Map<String, String> scriptMap, final Map<String, Object> defaultDataMap) {
            final String scriptType = getScriptType(paramMap);
            final int dataSize = Integer.parseInt(paramMap.getAsString("data.size", "10"));

            for (int i = 0; i < dataSize && alive; i++) {
                // Un enregistrement récupéré dans le système externe (ici, des valeurs fixes)
                final Map<String, Object> source = new HashMap<>();
                source.put("title", "Sample " + i);
                source.put("body", "Sample body text for record " + i);
                source.put("url", "http://fess.codelibs.org/?sample=" + i);

                // Les scripts sont évalués sur « paramètres + enregistrement »
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(source);

                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }
                callback.store(paramMap, dataMap);
            }
        }
    }

Le rôle de chaque partie est le suivant.

- La valeur renvoyée par ``getName()`` est enregistrée dans ``DataStoreFactory`` comme nom de ce magasin de données. Par convention, elle renvoie le nom simple de la classe
- ``paramMap`` contient les valeurs du champ « Paramètres » de la configuration du magasin de données. On les lit avec ``getAsString(clé, valeurParDéfaut)``
- ``scriptMap`` contient les lignes du champ « Script », de la forme ``nomDuChamp=expression``. ``convertValue()`` évalue l'expression et le résultat est placé dans le champ d'index correspondant
- ``defaultDataMap`` contient les valeurs déterminées par la configuration du magasin de données, comme l'ID de configuration, les autorisations (rôles), la valeur de boost et les hôtes virtuels. Copiez-la d'abord, puis ajoutez chaque champ
- ``callback.store()`` indexe les enregistrements un par un. ``alive`` passe à ``false`` lorsque la tâche est arrêtée ; incluez-le donc dans la condition de la boucle

Autrement dit, ce n'est pas le plugin qui décide quelle valeur d'un enregistrement va dans quel champ : c'est l'administrateur, dans le champ « Script ».
Le rôle du plugin est de récupérer les enregistrements et de les disposer dans ``resultMap``.

Le véritable ``ExampleDataStore`` implémente en outre la gestion des exceptions par enregistrement (consignation dans [URL d'échec]) et les statistiques d'exploration (``CrawlerStatsHelper``).
Pour créer votre propre plugin, copiez ``ExampleDataStore`` plutôt que ce squelette, et réécrivez les endroits marqués ``// CUSTOMIZE:`` (la partie qui récupère les enregistrements).

Fichier de configuration DI
---------------------------

Créer la classe ne suffit pas pour que Fess la charge.
Enregistrez-la comme composant dans ``src/main/resources/fess_ds++.xml``.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Le conteneur DI (Lasta Di) intègre tout ``fess_ds++.xml`` présent dans le classpath au ``fess_ds.xml`` de Fess.
Grâce à ``<postConstruct name="register">``, ``AbstractDataStore.register()`` est appelé après la création du composant, et le magasin de données est enregistré sous le nom renvoyé par ``getName()``.
Si vous changez le nom de la classe ou le package, modifiez aussi l'attribut ``class``.

Construire
----------

::

    $ mvn clean package

Trois jars sont créés dans ``target/``.
Celui à installer dans Fess est ``fess-ds-example-15.9.0-SNAPSHOT.jar``, sans ``-sources`` ni ``-javadoc``.
Vous pouvez vérifier avec ``unzip -l`` qu'il contient ``fess_ds++.xml`` et ``ExampleDataStore.class``.

Installer
=========

Le plus simple est d'installer le plugin depuis la console d'administration.

1. Dans [Système] > [Plugin], cliquez sur [Installer]
2. Laissez la liste déroulante de l'onglet [Distant] sur la première entrée, ``-``. Si un autre plugin est sélectionné, c'est lui qui est installé
3. Dans l'onglet [Local], sélectionnez le jar construit dans « Fichier Jar » et cliquez sur [Installer]
4. Redémarrez Fess

Le jar téléversé est enregistré dans ``app/WEB-INF/plugin/`` sous la forme ``<nom>-<version>.jar``.
Le nom et la version sont lus dans le nom du fichier ; téléversez donc le jar sans modifier le nom que Maven lui a donné.
Au lieu de passer par la console d'administration, vous pouvez aussi copier le jar directement dans ce répertoire et redémarrer (``/usr/share/fess/app/WEB-INF/plugin/`` dans l'image Docker).

Avec Docker, ``FESS_PLUGINS`` récupère des plugins publiés dans un dépôt ; il ne peut donc pas servir pour votre propre jar.
Installez le jar depuis la console d'administration, puis redémarrez avec ``docker compose -f compose.yaml -f compose-opensearch3.yaml restart fess01``.
Le jar se trouve dans le conteneur ; il disparaît donc si vous recréez le conteneur avec ``down`` et ``up``.
Dans ce cas, installez-le à nouveau.

Vérifier le fonctionnement
==========================

Vérifier le nom du gestionnaire
-------------------------------

Après le redémarrage, ouvrez [Robot d'exploration] > [Magasin de données] > [Créer nouveau] et vérifiez que ``ExampleDataStore`` figure dans la liste déroulante « Nom du gestionnaire ».
Ces choix sont construits à partir des jars de ``app/WEB-INF/plugin/`` dont le nom de fichier commence par ``fess-ds``.
Fess lit le ``fess_ds++.xml`` contenu dans le jar et propose le nom simple de la classe indiquée dans l'attribut ``class`` (mis en cache pendant 60 secondes).
S'il n'apparaît pas, vérifiez le nom du fichier jar, le ``fess_ds++.xml`` contenu dans le jar et que vous avez bien redémarré.

Créer la configuration du magasin de données
--------------------------------------------

Sur le même écran, saisissez les valeurs suivantes et cliquez sur [Créer].

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Champ
     - Valeur
   * - Nom
     - ``Example``
   * - Nom du gestionnaire
     - ``ExampleDataStore``
   * - Paramètres
     - Ajouter ``data.size=5`` sur la ligne qui suit le ``script_type=javascript`` prérempli
   * - Script
     - Trois lignes : ``title=title``, ``content=body`` et ``url=url``

Lorsque la partie droite d'une ligne de script correspond à une clé de l'enregistrement (``title``, ``body``, ``url``), ``convertValue()`` renvoie cette valeur telle quelle, sans passer par un moteur de script.
Une expression comme ``content=title + " " + body`` est évaluée par le moteur indiqué dans ``script_type``.
Si vous supprimez ``script_type``, le script est traité comme ``groovy`` et l'évaluation des expressions échoue dans un environnement sans ``fess-script-groovy`` ; conservez-le donc.

``url`` est obligatoire.
``callback.store()`` refuse un document sans ``url`` et lève une exception.

Exécuter la tâche
-----------------

1. Dans la liste [Robot d'exploration] > [Magasin de données], cliquez sur ``Example``, puis sur [Créer une nouvelle tâche]
2. L'écran de création du planificateur s'ouvre ; cliquez sur [Créer] sans rien modifier
3. Dans [Système] > [Planificateur], ouvrez la tâche créée et cliquez sur [Démarrer maintenant]

Vérifier les résultats
----------------------

Vérifiez les quatre points suivants.

1. Dans [Informations système] > [Journal des tâches], l'état de la tâche est « OK »
2. Dans [Informations système] > [Informations sur l'exploration], « Taille de l'index (Magasin de données) » vaut ``5`` pour cette session
3. Rien n'est consigné dans [Informations système] > [URL d'échec]
4. Une recherche de ``Sample`` dans [Informations système] > [Rechercher] affiche cinq résultats, de ``Sample 0`` à ``Sample 4``

Un état « OK » de la tâche ne signifie pas forcément que le traitement du magasin de données a réussi.
Par exemple, si vous supprimez ``url=url`` du script et lancez la tâche, ``callback.store()`` lève une exception pour chaque enregistrement et rien n'est indexé.
``ExampleDataStore`` intercepte les exceptions enregistrement par enregistrement : ``record:0`` à ``record:4`` sont donc consignés dans [URL d'échec] et des messages WARN apparaissent dans ``fess-crawler.log``, mais le journal des tâches reste à « OK ».
Avec un code qui n'intercepte pas les exceptions, comme le squelette, toute la configuration échoue et une seule entrée est consignée dans [URL d'échec], sous la forme ``D<IDdeConfiguration>:Example``.
Les étapes de vérification et l'emplacement des journaux sont résumés dans la section sur la vérification des résultats de :doc:`datastore-basics`.

Une fois tout cela vérifié, remplacez la partie qui récupère les enregistrements, par exemple ``createSourceRecord()``, par du code qui lit votre véritable API ou vos fichiers.
N'écrivez pas en dur la destination de connexion ni les identifiants du système externe : recevez-les via ``paramMap`` depuis le champ « Paramètres ».

Le ``src/test`` du modèle contient des tests qui utilisent ``LastaDiTestCase`` d'UTFlute.
Une classe de test qui implémente ``IndexUpdateCallback`` collecte les ``dataMap`` passés à ``store()``, et les tests vérifient leur nombre et les valeurs des champs.
Vous pouvez ainsi exécuter ``mvn test`` sans OpenSearch.
Lorsque vous réécrivez la partie qui récupère les enregistrements, adaptez aussi ces tests.

Traiter les documents avant l'indexation avec un Ingester
=========================================================

Un Ingester est appelé juste avant l'envoi d'un document à l'index, pour tous les types d'exploration : magasin de données, web et système de fichiers.
Il sert par exemple à ajouter un champ commun à tous les documents ou à normaliser des valeurs.
Il n'existe aucun moyen de l'activer ou de le désactiver par configuration : une fois installé, il s'applique à toutes les explorations.

Héritez de ``org.codelibs.fess.ingest.Ingester`` et ne redéfinissez que les méthodes ``process`` dont vous avez besoin.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Méthode
     - Moment de l'appel
   * - ``process(Map<String, Object> target, DataStoreParams params)``
     - Exploration d'un magasin de données (dans ``callback.store()``)
   * - ``process(Map<String, Object> target, AccessResult<String> accessResult)``
     - Indexation lors d'une exploration web ou de fichiers
   * - ``process(ResultData target, ResponseData responseData)``
     - Traitement de la réponse récupérée lors d'une exploration web ou de fichiers
   * - ``protected process(Map<String, Object> target)``
     - Méthode appelée par défaut par les deux variantes ``Map`` ci-dessus. Redéfinissez uniquement celle-ci pour que le traitement s'applique à la fois aux magasins de données et aux explorations web et de fichiers

Voici ``ExampleIngester`` de ``fess-ingest-example``, réduit au traitement destiné aux magasins de données.

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.apache.logging.log4j.LogManager;
    import org.apache.logging.log4j.Logger;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {
        private static final Logger logger = LogManager.getLogger(ExampleIngester.class);

        public ExampleIngester() {
            setPriority(50);
        }

        @Override
        public Map<String, Object> process(final Map<String, Object> target, final DataStoreParams params) {
            target.put("ingested_by", ExampleIngester.class.getSimpleName());
            logger.info("DATASTORE CRAWL: {}", target);
            return target;
        }
    }

L'enregistrement se fait dans ``src/main/resources/fess_ingest++.xml``.
Sa forme est la même que celle de ``fess_ds++.xml`` : un composant nommé ``exampleIngester`` avec ``<postConstruct name="register">``.
``Ingester.register()`` ajoute l'Ingester lui-même à ``IngestFactory``.

La récupération du modèle, la construction, l'installation et le redémarrage suivent les mêmes étapes que pour le magasin de données (le commit pour 15.9 est ``8a1e45ddb63a118802287120effd3ce49fb60bfb`` et le jar est ``fess-ingest-example-15.9.0-SNAPSHOT.jar``).
Pour votre propre plugin, commencez l'artifactId par ``fess-ingest-``.

Tenez compte des points suivants lors de l'implémentation.

- Renvoyez toujours ``target`` après l'avoir modifié. La valeur renvoyée est transmise telle quelle à l'Ingester suivant et à l'indexeur, sans vérification de ``null``. Renvoyer ``null`` n'exclut pas le document : cela casse le traitement d'indexation
- Plusieurs Ingesters s'exécutent par ordre croissant de ``priority`` (99 par défaut). Chaque Ingester reçoit le ``target`` modifié par le précédent
- Si ``process`` lève une exception, Fess consigne un WARN et passe à l'Ingester suivant. L'indexation du document ne s'arrête pas. Les modifications apportées à ``target`` avant l'exception sont conservées

Pour vérifier son fonctionnement, relancez la tâche de la configuration de magasin de données créée dans « Vérifier le fonctionnement » ci-dessus.
Les Ingesters s'exécutent dans le processus du robot d'exploration : si ``fess-crawler.log`` contient une ligne ``DATASTORE CRAWL:`` pour chaque document, l'Ingester est bien appelé.
Le ``ExampleIngester`` du dépôt consigne aussi un par un les documents des explorations web et de fichiers sous la forme ``WEB/FILE CRAWL:``.
Comme il agit sur toutes les explorations, supprimez-le dans [Système] > [Plugin] une fois la vérification terminée, puis redémarrez Fess.

Mettre à niveau Fess
====================

Construisez un plugin avec le ``fess-parent`` de la même version mineure que le Fess dans lequel il est installé (15.9.x pour Fess 15.9).
Les plugins publiés sont eux aussi publiés dans une version correspondante pour chaque version mineure de Fess.

Lorsque vous passez Fess en 15.10, alignez la version de ``fess-parent`` dans ``pom.xml`` et reconstruisez.
Dans la liste [Système] > [Plugin], supprimez l'ancien jar, installez le nouveau et redémarrez.
``bin/fess-setup upgrade plugins`` récupère les nouvelles versions dans le dépôt de plugins ; il ne peut donc pas mettre à jour vos propres plugins absents de ce dépôt.

Pour aller plus loin
====================

- Pour en savoir plus sur les paramètres, scripts, autorisations et planifications des magasins de données : :doc:`datastore-basics`
- Pour voir des exemples de configuration de plugins de magasin de données publiés : :doc:`guide-06`, :doc:`guide-07` et :doc:`guide-12`
- Pour modifier l'apparence de la page de recherche : :doc:`guide-03`
- Pour activer le mode de recherche IA avec un plugin LLM : :doc:`guide-19`
- Pour utiliser un plugin d'application web (serveur MCP) : :doc:`guide-20`

Références
==========

- `Architecture des plugins <https://fess.codelibs.org/fr/stable/dev/plugin-architecture.html>`__
- `Développement de plugins DataStore <https://fess.codelibs.org/fr/stable/dev/datastore-plugin.html>`__
- `Plugin Ingest <https://fess.codelibs.org/fr/stable/dev/ingest-plugin.html>`__
- `Guide de développement des thèmes <https://fess.codelibs.org/fr/stable/dev/theme-development.html>`__
- `Plugins (console d'administration) <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `fess-ds-example (GitHub) <https://github.com/codelibs/fess-ds-example>`__
- `fess-ingest-example (GitHub) <https://github.com/codelibs/fess-ingest-example>`__
