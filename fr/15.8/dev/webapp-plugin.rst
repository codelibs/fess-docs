========================
Plugin d'application Web
========================

Aperçu
======

Les plugins d'application Web (``fess-webapp-*``) sont des plugins qui
étendent l'application Web de |Fess|. Contrairement aux autres types de
plugins, ils n'ajoutent pas directement de classes Action ou de JSP, mais
étendent les fonctionnalités en **ajoutant ou remplaçant des composants**
dans le conteneur DI (Lasta Di). Les cas d'usage représentatifs sont les
suivants :

- Ajout de nouveaux composants (helpers, services, etc.)
- Remplacement de composants du cœur de |Fess| (par sous-classement)
- Ajout de points de terminaison d'API REST (``WebApiManager``)
- Extension du comportement de recherche (commandes de requête, fusion de
  classements, etc.)

.. note::

   Les plugins d'application Web sont distribués sous forme de fichier JAR ;
   les classes internes et les fichiers de configuration DI qu'ils
   contiennent sont chargés dans le classpath de l'application Web de
   |Fess|. Ils n'ajoutent pas de vues JSP. Pour personnaliser le design de
   l'écran de recherche, reportez-vous à :doc:`theme-development`.

Structure de base
=================

En prenant comme exemple
`fess-webapp-example <https://github.com/codelibs/fess-webapp-example>`__,
le modèle d'implémentation d'un plugin d'application Web, un plugin se
compose d'une « classe d'implémentation » et d'un « fichier d'enregistrement
DI » :

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/webapp/example/helper/
        │   ├── ExampleHelper.java        # Composant ajouté
        │   └── CustomSystemHelper.java   # Remplacement d'un composant du cœur
        └── resources/
            ├── app++.xml                 # Ajout de composant (fusion)
            └── fess+systemHelper.xml     # Remplacement de composant

.. note::

   Le package des classes d'implémentation utilise
   ``org.codelibs.fess.webapp.<nom-du-plugin>``. Les fichiers de
   configuration DI sont placés dans ``src/main/resources/``. Contrairement
   aux plugins DataStore, ils n'incluent pas de ``src/main/webapp/`` ni de
   JSP.

pom.xml et manifeste
====================

Les plugins d'application Web sont construits comme un jar ayant
``fess-parent`` pour POM parent. Les bibliothèques telles que ``fess`` ou
``opensearch``, fournies à l'exécution par |Fess| lui-même, doivent être
déclarées avec la portée ``provided``, tandis que les bibliothèques
nécessaires à l'exécution telles que ``lastaflute``, ``dbflute-runtime`` ou
``corelib`` sont déclarées avec la portée habituelle.

Le point le plus important pour un plugin d'application Web est d'ajouter
``Fess-WebAppJar: true`` au manifeste du JAR. Cette déclaration permet à
|Fess| de monter les classes du plugin et ses fichiers de configuration DI
dans le chargeur de classes de l'application Web. Cette configuration se
fait via ``maven-jar-plugin`` :

.. code-block:: xml

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-jar-plugin</artifactId>
                <configuration>
                    <archive>
                        <manifestEntries>
                            <Fess-WebAppJar>true</Fess-WebAppJar>
                        </manifestEntries>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>

.. warning::

   Si ``Fess-WebAppJar: true`` n'est pas ajouté, les classes du plugin et
   les fichiers de configuration DI ne seront pas chargés dans le classpath
   de l'application Web, et l'ajout ou le remplacement de composants ne
   sera pas effectif.

Pour la structure complète du pom.xml (POM parent, déclaration des
dépendances, etc.), reportez-vous à :doc:`plugin-architecture`.

Modèles d'extension
====================

Ajout d'un composant (app++.xml)
---------------------------------

La méthode d'extension la plus élémentaire consiste à ajouter vos propres
composants. Lasta Di **fusionne** le fichier ``app++.xml`` présent sur le
classpath dans l'espace de noms ``app`` construit à partir du fichier
``app.xml`` de |Fess| lui-même (le suffixe ``++`` est la convention
indiquant une fusion additive). Comme les composants ajoutés utilisent des
noms qui n'existent pas dans |Fess| lui-même, rien n'est écrasé.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleHelper"
            class="org.codelibs.fess.webapp.example.helper.ExampleHelper">
        </component>
    </components>

Dans l'implémentation du composant, utilisez ``@PostConstruct`` pour
l'initialisation, et récupérez les composants de |Fess| lui-même via
``ComponentUtil`` pour les réutiliser (sans les copier ni les écraser) :

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import org.codelibs.fess.helper.SystemHelper;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;

    public class ExampleHelper {

        protected String pluginName = "fess-webapp-example";

        @PostConstruct
        public void init() {
            // Traitement d'initialisation appelé une seule fois après la création par le conteneur DI
        }

        public String getPluginLabel() {
            // Réutilise le SystemHelper du cœur pour récupérer la version de Fess en cours d'exécution
            final SystemHelper systemHelper = ComponentUtil.getSystemHelper();
            final String version = systemHelper != null ? systemHelper.getProductVersion() : "unknown";
            return pluginName + " (Fess " + version + ")";
        }
    }

.. tip::

   Envisagez d'abord cet « ajout de composant ». À moins qu'il ne soit
   nécessaire de modifier une fonctionnalité du cœur, cette approche est
   plus sûre et plus facile à maintenir que le remplacement.

Remplacement d'un composant du cœur (fess+componentName.xml)
--------------------------------------------------------------

Si vous souhaitez modifier le comportement d'un composant du cœur de
|Fess|, sous-classez la classe cible et **réenregistrez-la sous le même nom
de composant** dans un fichier de configuration DI nommé
``<baseDicon>+<componentName>.xml``. Par exemple, ``systemHelper`` étant
déclaré dans le fichier ``fess.xml`` de |Fess| lui-même, le fichier de
remplacement sera ``fess+systemHelper.xml`` (et non
``app+systemHelper.xml``).

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import java.nio.file.Path;

    import org.codelibs.fess.helper.SystemHelper;

    public class CustomSystemHelper extends SystemHelper {

        @Override
        protected void parseProjectProperties(final Path propPath) {
            try {
                super.parseProjectProperties(propPath);
            } catch (final Exception e) {
                // Traitement personnalisé
            }
            System.setProperty("fess.webapp.plugin", "true");
        }
    }

.. warning::

   Le remplacement (un seul ``+``) remplace **entièrement** la définition
   du composant. Pour cette raison, le fichier de remplacement doit
   contenir tous les éléments ``<postConstruct>`` définis par la définition
   du cœur. Par exemple, pour remplacer ``systemHelper``, vous devez copier
   intégralement le mapping des noms de JSP de design
   (``addDesignJspFileName``) depuis le ``fess.xml`` du cœur. Ces éléments
   doivent être synchronisés à chaque nouvelle version de |Fess|, et tout
   oubli empêchera la résolution de certains écrans (``chat``, ``login``,
   etc.). Ce coût de maintenance explique pourquoi l'ajout est recommandé
   plutôt que le remplacement.

Ajout d'une API REST (fess_api++.xml)
---------------------------------------

Pour ajouter un nouveau point de terminaison d'API REST, implémentez
``WebApiManager``. Héritez de ``BaseApiManager`` et enregistrez-vous auprès
de ``WebApiManagerFactory`` via ``@PostConstruct``. Le gestionnaire d'API
enregistré est invoqué par ``WebApiFilter`` à chaque requête. Enregistrez
le composant dans ``fess_api++.xml`` :

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleApiManager"
            class="org.codelibs.fess.webapp.example.api.ExampleApiManager">
        </component>
    </components>

.. code-block:: java

    package org.codelibs.fess.webapp.example.api;

    import java.io.IOException;

    import org.codelibs.fess.api.BaseApiManager;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;
    import jakarta.servlet.FilterChain;
    import jakarta.servlet.ServletException;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;

    public class ExampleApiManager extends BaseApiManager {

        public ExampleApiManager() {
            // Préfixe du chemin traité par ce gestionnaire
            setPathPrefix("/api/example");
        }

        @PostConstruct
        public void register() {
            ComponentUtil.getWebApiManagerFactory().add(this);
        }

        @Override
        public boolean matches(final HttpServletRequest request) {
            // Détermine si ce gestionnaire doit traiter la requête
            return request.getServletPath().startsWith(pathPrefix);
        }

        @Override
        public void process(final HttpServletRequest request, final HttpServletResponse response,
                final FilterChain chain) throws IOException, ServletException {
            // Traitement de la requête et écriture de la réponse
        }

        @Override
        protected void writeHeaders(final HttpServletResponse response) {
            // Configuration des en-têtes de réponse (si nécessaire)
        }
    }

Comme exemples d'implémentation, vous pouvez vous référer à
`fess-webapp-v1-api <https://github.com/codelibs/fess-webapp-v1-api>`__,
qui fournit ``/api/v1``, ou à
`fess-webapp-classic-api <https://github.com/codelibs/fess-webapp-classic-api>`__,
qui fournit ``/json`` / ``/suggest``.

Personnalisation de l'écran de recherche
=========================================

Les plugins d'application Web ne peuvent pas ajouter de vues JSP. En effet,
les vues JSP sont placées dans ``WEB-INF/view/`` du WAR de |Fess|
lui-même, alors que le JAR du plugin est monté dans le classpath
(``WEB-INF/classes``). Pour modifier le design de l'écran de recherche,
utilisez l'une des approches suivantes :

- **Thème** : personnalise le design (HTML/CSS/JavaScript) de l'écran de
  recherche. Reportez-vous à :doc:`theme-development`.
- **Remplacement de systemHelper** : comme décrit ci-dessus dans
  « Remplacement d'un composant du cœur », vous pouvez modifier le mapping
  des noms de JSP de design (les fichiers JSP eux-mêmes restent toutefois
  fournis par |Fess| lui-même).

Build et installation
======================

::

    mvn clean package

Le fichier JAR (par exemple ``fess-webapp-example-15.8.0.jar``) est généré
dans le répertoire ``target/``. Vous pouvez installer le JAR généré depuis
l'écran d'administration, ou le placer dans le répertoire
``app/WEB-INF/plugin/`` puis redémarrer |Fess|. Pour plus de détails sur la
procédure d'installation, reportez-vous à :doc:`../admin/plugin-guide`.

Exemples de plugins publiés
============================

Le projet |Fess| publie les plugins d'application Web suivants. Ils sont
publiés sur `GitHub <https://github.com/codelibs>`__ comme référence pour
le développement :

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Plugin
     - Description
   * - ``fess-webapp-example``
     - Modèle d'implémentation de plugin
   * - ``fess-webapp-v1-api``
     - API REST ``/api/v1``
   * - ``fess-webapp-classic-api``
     - API REST historique ``/json`` / ``/suggest``
   * - ``fess-webapp-mcp``
     - Serveur MCP (Model Context Protocol)
   * - ``fess-webapp-semantic-search``
     - Recherche neuronale / recherche vectorielle
   * - ``fess-webapp-multimodal``
     - Recherche multimodale (image et texte)

Informations complémentaires
=============================

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`theme-development` - Personnalisation des thèmes
- :doc:`../admin/plugin-guide` - Installation des plugins
- :doc:`overview` - Aperçu de la documentation développeur
