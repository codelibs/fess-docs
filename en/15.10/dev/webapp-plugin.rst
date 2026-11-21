==================================
Web App Plugin
==================================

Overview
========

Web App plugins (``fess-webapp-*``) extend the |Fess| web application.
Unlike other plugin types, they do not add Action classes or JSPs
directly; instead, they extend functionality by **adding or replacing
components** in the DI container (Lasta Di). Typical use cases
include:

- Adding new components (helpers, services, etc.)
- Replacing components in the |Fess| core (via subclassing)
- Adding REST API endpoints (``WebApiManager``)
- Extending search behavior (query commands, rank fusion, etc.)

.. note::

   Web App plugins are distributed as JAR files, and their internal
   classes and DI configuration files are loaded onto the classpath of
   the |Fess| web application. They do not add JSP views. If you want
   to customize the design of the search screen, see
   :doc:`theme-development`.

Basic Structure
===============

Taking `fess-webapp-example <https://github.com/codelibs/fess-webapp-example>`__,
the implementation template for Web App plugins, as an example, a
plugin consists of an "implementation class" and a "DI registration
file":

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/webapp/example/helper/
        │   ├── ExampleHelper.java        # Component to add
        │   └── CustomSystemHelper.java   # Replacement for a core component
        └── resources/
            ├── app++.xml                 # Adds components (merge)
            └── fess+systemHelper.xml     # Replaces a component

.. note::

   The implementation class package uses
   ``org.codelibs.fess.webapp.<plugin-name>``. DI configuration files
   are placed under ``src/main/resources/``. Unlike Data Store
   plugins, there is no ``src/main/webapp/`` directory or JSP files.

pom.xml and Manifest
=====================

Web App plugins are built as a jar with ``fess-parent`` as the parent
POM. Libraries such as ``fess`` and ``opensearch``, which are supplied
by the |Fess| core at runtime, are declared with ``provided`` scope,
while libraries required at runtime such as ``lastaflute``,
``dbflute-runtime``, and ``corelib`` are declared with normal scope.

The most important part of a Web App plugin is adding
``Fess-WebAppJar: true`` to the JAR manifest. This declaration tells
|Fess| to mount the plugin's classes and DI configuration files onto
the web application's classloader. This is configured via the
``maven-jar-plugin``:

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

   If ``Fess-WebAppJar: true`` is not set, the plugin's classes and DI
   configuration files will not be loaded onto the web application's
   classpath, and component addition/replacement will not take
   effect.

For the overall structure of pom.xml (parent POM, how to declare
dependencies, etc.), see :doc:`plugin-architecture`.

Extension Patterns
==================

Adding Components (app++.xml)
------------------------------

The most basic way to extend the plugin is to add your own
components. Lasta Di **merges** ``app++.xml`` found on the classpath
into the ``app`` namespace built from the |Fess| core's ``app.xml``
(the trailing ``++`` is the convention for an additive merge). Since
the components you add use names that do not exist in the |Fess|
core, nothing is overwritten.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleHelper"
            class="org.codelibs.fess.webapp.example.helper.ExampleHelper">
        </component>
    </components>

In the component implementation, use ``@PostConstruct`` for
initialization, and retrieve and reuse |Fess| core components via
``ComponentUtil`` (do not copy or override them):

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import org.codelibs.fess.helper.SystemHelper;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;

    public class ExampleHelper {

        protected String pluginName = "fess-webapp-example";

        @PostConstruct
        public void init() {
            // Initialization logic invoked once after creation by DI
        }

        public String getPluginLabel() {
            // Reuse the core SystemHelper to get the running Fess version
            final SystemHelper systemHelper = ComponentUtil.getSystemHelper();
            final String version = systemHelper != null ? systemHelper.getProductVersion() : "unknown";
            return pluginName + " (Fess " + version + ")";
        }
    }

.. tip::

   Consider this "component addition" approach first. Unless you need
   to change core functionality, it is safer and easier to maintain
   than replacement.

Replacing Core Components (fess+componentName.xml)
----------------------------------------------------

If you want to change the behavior of a |Fess| core component,
subclass the target class and **re-register it under the same
component name** in a DI configuration file named
``<baseDicon>+<componentName>.xml``. For example, since ``systemHelper``
is declared in the |Fess| core's ``fess.xml``, the replacement file is
``fess+systemHelper.xml`` (not ``app+systemHelper.xml``).

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
                // Custom handling
            }
            System.setProperty("fess.webapp.plugin", "true");
        }
    }

.. warning::

   Replacement (a single ``+``) replaces the component definition
   **in its entirety**. This means the replacement file must include
   every ``<postConstruct>`` entry that the core definition performs
   (for example, ``queryHelper`` in ``app.xml``). These must be kept in
   sync with each |Fess| release. If the file keeps calling a method
   that the core removed, the component definition fails to initialize
   with a ``BeanMethodNotFoundException``. For example, 15.9 removed
   ``addDesignJspFileName`` from ``systemHelper``, so a replacement file
   that still calls it fails. This maintenance cost is why addition is
   recommended over replacement.

Adding a REST API (fess_api++.xml)
------------------------------------

To add a new REST API endpoint, implement ``WebApiManager``. Extend
``BaseApiManager`` and register itself with the
``WebApiManagerFactory`` in ``@PostConstruct``. The registered API
manager is invoked by ``WebApiFilter`` for every request. Register the
component in ``fess_api++.xml``:

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
            // Path prefix handled by this manager
            setPathPrefix("/api/example");
        }

        @PostConstruct
        public void register() {
            ComponentUtil.getWebApiManagerFactory().add(this);
        }

        @Override
        public boolean matches(final HttpServletRequest request) {
            // Determine whether this manager should handle the request
            return request.getServletPath().startsWith(pathPrefix);
        }

        @Override
        public void process(final HttpServletRequest request, final HttpServletResponse response,
                final FilterChain chain) throws IOException, ServletException {
            // Process the request and write the response
        }

        @Override
        protected void writeHeaders(final HttpServletResponse response) {
            // Set response headers (as needed)
        }
    }

For implementation examples, see
`fess-webapp-v1-api <https://github.com/codelibs/fess-webapp-v1-api>`__,
which provides ``/api/v1``, and
`fess-webapp-classic-api <https://github.com/codelibs/fess-webapp-classic-api>`__,
which provides ``/json`` / ``/suggest``.

.. _webapp-plugin-password-encoder:

Adding a Password Hash Algorithm (fess++.xml)
---------------------------------------------

The hash of the password of a local user is made by a component. A stored password is written as ``{id}hash``. |Fess| takes the ``id`` of the stored value, and for a new password the value of ``app.password.algorithm`` (``bcrypt`` by default), and looks up the DI component named ``<id>PasswordEncoder``, the same way ``<sso.type>Authenticator`` and ``<storage.type>StorageClient`` are resolved. |Fess| registers ``bcryptPasswordEncoder`` itself. To add an algorithm, implement ``org.codelibs.fess.crypto.password.PasswordEncoder`` and register the class in ``fess++.xml``, which Lasta Di merges into the ``fess.xml`` of the |Fess| core:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="argon2PasswordEncoder"
            class="com.example.Argon2PasswordEncoder">
        </component>
    </components>

The interface has the following methods:

.. list-table:: Methods of PasswordEncoder
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - ``String encode(String rawPassword)``
     - Hashes a password. The result is stored after the ``{id}`` prefix, which |Fess| adds. Throw ``IllegalArgumentException`` for a password that cannot be hashed faithfully; the message must not contain the password.
   * - ``boolean matches(String rawPassword, String encodedPassword)``
     - Verifies a password against a hash made by this encoder. Return ``false`` for a wrong password and for a malformed hash.
   * - ``boolean needsUpgrade(String encodedPassword)``
     - Optional (default ``false``). Tells whether a stored hash is weaker than what ``encode`` makes now, so that it is hashed again at the next login of its user. BCrypt returns ``true`` for a cost below ``app.password.bcrypt.cost``.
   * - ``int getMaxPasswordBytes()``
     - Optional (default ``0``, no limit). The longest password, in UTF-8 bytes, that ``encode`` accepts. BCrypt returns ``72``.
   * - ``boolean isVerificationCostly()`` and ``void applyTimingPadding()``
     - Optional (default ``false`` and nothing). A deliberately slow algorithm returns ``true`` and spends about the time of one ``matches`` in ``applyTimingPadding()``. |Fess| calls it when a login fails without a hash being verified (for example for an unknown user), so that the response time does not tell whether the user exists.

To use the encoder:

#. Put the jar in the ``WEB-INF/plugin`` directory. As for any Web App plugin, the manifest needs ``Fess-WebAppJar: true`` (see "pom.xml and Manifest"); without it the component is not found.
#. Set ``app.password.algorithm`` in ``fess_config.properties`` to the id (``argon2`` for ``argon2PasswordEncoder``). The id must be lower case and must not contain ``}``. New and changed passwords are then hashed with it. Passwords stored with another id, or as a legacy hash without an id, are hashed again at the next successful login of their user while ``app.password.upgrade.enabled`` is ``true`` (the default).

Keep the following in mind:

- The encoder is a singleton shared by all threads, so it must be thread-safe.
- The length limit belongs to the encoder. When a password is set (user management screen, forced password change, ``/api/v2/auth/password`` and the Admin API), |Fess| refuses a password longer than ``getMaxPasswordBytes()`` of the algorithm of ``app.password.algorithm`` with "Password must be no longer than N bytes."; with ``0`` or less it checks only ``password.max.length``. |Fess| applies no length limit when it verifies a stored hash; whether a longer password may match is up to ``matches``.
- Keep the plugin installed as long as passwords with its id are stored. Without the component, a hash with that id never matches: those users cannot log in, and their hashes are not hashed again.
- If ``app.password.algorithm`` names an id without a component (for example after the plugin jar was removed), |Fess| still starts and users whose hash has another id can still log in, but setting a password fails with an error that names ``app.password.algorithm``.

Customizing the Search Screen
==============================

Web App plugins cannot add JSP views. JSP views are located under
``WEB-INF/view/`` in the |Fess| core WAR, while plugin JARs are mounted
onto the classpath (``WEB-INF/classes``). To change the design of the
search screen, use a theme, which customizes the design
(HTML/CSS/JavaScript) of the search screen. See :doc:`theme-development`.

Build and Installation
========================

::

    mvn clean package

A JAR file (e.g., ``fess-webapp-example-15.10.0.jar``) is generated in
the ``target/`` directory. Install the generated JAR from the admin
console, or place it in the ``app/WEB-INF/plugin/`` directory and
restart |Fess|. For details on the installation procedure, see
:doc:`../admin/plugin-guide`.

Examples of Published Plugins
===============================

The |Fess| project publishes the following Web App plugins. They are
published on `GitHub <https://github.com/codelibs>`__ as a reference
for development:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Plugin
     - Description
   * - ``fess-webapp-example``
     - Plugin implementation template
   * - ``fess-webapp-v1-api``
     - ``/api/v1`` REST API
   * - ``fess-webapp-classic-api``
     - Legacy REST API for ``/json`` / ``/suggest``
   * - ``fess-webapp-mcp``
     - MCP (Model Context Protocol) server
   * - ``fess-webapp-bangs``
     - DuckDuckGo-style bangs (``!g``) that send a search to another site
   * - ``fess-webapp-semantic-search``
     - Neural search / vector search (deprecated; superseded by the core integration in 15.8)
   * - ``fess-webapp-multimodal``
     - Multimodal (image/text) search

Reference
=========

- :doc:`plugin-architecture` - Plugin Architecture
- :doc:`theme-development` - Theme customization
- :doc:`../admin/plugin-guide` - Plugin installation
- :doc:`overview` - Developer Documentation Overview
