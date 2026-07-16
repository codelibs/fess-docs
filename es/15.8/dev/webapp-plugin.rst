==================================
Plugin de Aplicación Web
==================================

Visión General
==============

Los plugins de aplicación web (``fess-webapp-*``) son plugins que amplían
la aplicación web de |Fess|. A diferencia de otros tipos de plugins, no
añaden directamente clases Action ni JSP, sino que amplían la
funcionalidad **añadiendo o sustituyendo componentes** en el contenedor
DI (Lasta Di). Los usos representativos son los siguientes:

- Adición de nuevos componentes (helpers, servicios, etc.)
- Sustitución de componentes del núcleo de |Fess| (mediante subclases)
- Adición de endpoints de API REST (``WebApiManager``)
- Ampliación del comportamiento de búsqueda (comandos de consulta,
  fusión de rangos, etc.)

.. note::

   Los plugins de aplicación web se distribuyen como JAR, y sus clases
   internas y archivos de configuración DI se cargan en el classpath de
   la aplicación web de |Fess|. No permiten añadir vistas JSP. Si desea
   personalizar el diseño de la pantalla de búsqueda, consulte
   :doc:`theme-development`.

Estructura Básica
=================

Tomando como ejemplo `fess-webapp-example
<https://github.com/codelibs/fess-webapp-example>`__, la plantilla de
implementación de un plugin de aplicación web, un plugin se compone de
una «clase de implementación» y un «archivo de registro DI»:

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/webapp/example/helper/
        │   ├── ExampleHelper.java        # Componente a añadir
        │   └── CustomSystemHelper.java   # Sustitución de un componente del núcleo
        └── resources/
            ├── app++.xml                 # Adición de componentes (fusión)
            └── fess+systemHelper.xml     # Sustitución de componentes

.. note::

   El paquete de las clases de implementación utiliza
   ``org.codelibs.fess.webapp.<nombre-del-plugin>``. Los archivos de
   configuración DI se colocan en ``src/main/resources/``. A diferencia
   de los plugins de almacén de datos, no incluyen ``src/main/webapp/``
   ni JSP.

pom.xml y el Manifiesto
=======================

Los plugins de aplicación web se construyen como jar con ``fess-parent``
como POM padre. Las bibliotecas ``fess`` y ``opensearch``, que son
proporcionadas en tiempo de ejecución por el propio |Fess|, se declaran
con el ámbito ``provided``, mientras que las bibliotecas necesarias en
tiempo de ejecución, como ``lastaflute``, ``dbflute-runtime`` y
``corelib``, se declaran con el ámbito habitual.

Lo más importante en un plugin de aplicación web es añadir
``Fess-WebAppJar: true`` al manifiesto del JAR. Gracias a esta
declaración, |Fess| monta las clases del plugin y sus archivos de
configuración DI en el cargador de clases de la aplicación web. Esta
configuración se realiza con ``maven-jar-plugin``:

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

   Si no se añade ``Fess-WebAppJar: true``, las clases del plugin y los
   archivos de configuración DI no se cargarán en el classpath de la
   aplicación web, y la adición o sustitución de componentes no surtirá
   efecto.

Para conocer la configuración completa de pom.xml (el POM padre, la
forma de declarar las dependencias, etc.), consulte
:doc:`plugin-architecture`.

Patrones de Extensión
======================

Adición de Componentes (app++.xml)
-----------------------------------

La forma más básica de extensión es añadir sus propios componentes.
Lasta Di **fusiona** el archivo ``app++.xml`` presente en el classpath
con el espacio de nombres ``app`` construido a partir del ``app.xml``
del propio |Fess| (el sufijo ``++`` es la convención para la fusión
aditiva). Dado que los componentes añadidos utilizan nombres que no
existen en el propio |Fess|, no se sobrescribe nada.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleHelper"
            class="org.codelibs.fess.webapp.example.helper.ExampleHelper">
        </component>
    </components>

En la implementación del componente, utilice ``@PostConstruct`` para la
inicialización, y reutilice los componentes del propio |Fess|
obteniéndolos mediante ``ComponentUtil`` (no los copie ni los
sobrescriba):

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import org.codelibs.fess.helper.SystemHelper;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;

    public class ExampleHelper {

        protected String pluginName = "fess-webapp-example";

        @PostConstruct
        public void init() {
            // Procesamiento de inicialización invocado una sola vez tras la creación por DI
        }

        public String getPluginLabel() {
            // Reutiliza el SystemHelper del núcleo para obtener la versión de Fess en ejecución
            final SystemHelper systemHelper = ComponentUtil.getSystemHelper();
            final String version = systemHelper != null ? systemHelper.getProductVersion() : "unknown";
            return pluginName + " (Fess " + version + ")";
        }
    }

.. tip::

   Considere primero esta opción de «adición de componentes». A menos
   que sea necesario modificar la funcionalidad del núcleo, es más
   segura y ofrece mejor mantenibilidad que la sustitución.

Sustitución de Componentes del Núcleo (fess+componentName.xml)
------------------------------------------------------------------

Si desea modificar el comportamiento de un componente del propio
|Fess|, cree una subclase de la clase de destino y \*\*vuelva a
registrarla con el mismo nombre de componente\*\* en un archivo de
configuración DI denominado ``<baseDicon>+<componentName>.xml``. Por
ejemplo, dado que ``systemHelper`` está declarado en ``fess.xml`` del
propio |Fess|, el archivo de sustitución será ``fess+systemHelper.xml``
(no ``app+systemHelper.xml``).

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
                // Procesamiento propio
            }
            System.setProperty("fess.webapp.plugin", "true");
        }
    }

.. warning::

   La sustitución (con un único ``+``) reemplaza **por completo** la
   definición del componente. Por ello, el archivo de sustitución debe
   incluir todos los elementos ``<postConstruct>`` que realiza la
   definición del núcleo. Por ejemplo, al sustituir ``systemHelper``, es
   necesario copiar y describir todo el mapeo de nombres de JSP de
   diseño (``addDesignJspFileName``) desde el ``fess.xml`` del núcleo.
   Esto debe sincronizarse en cada versión de |Fess|, y cualquier
   omisión hará que algunas pantallas (como ``chat`` o ``login``) no
   puedan resolverse. Este coste de mantenimiento es la razón por la
   que se recomienda la adición en lugar de la sustitución.

Adición de una API REST (fess_api++.xml)
-------------------------------------------

Para añadir un nuevo endpoint de API REST, implemente
``WebApiManager``. Herede de ``BaseApiManager`` y regístrese a sí mismo
en ``WebApiManagerFactory`` mediante ``@PostConstruct``. El gestor de
API registrado es invocado por ``WebApiFilter`` en cada solicitud.
Registre el componente en ``fess_api++.xml``:

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
            // Prefijo de la ruta que gestiona este manejador
            setPathPrefix("/api/example");
        }

        @PostConstruct
        public void register() {
            ComponentUtil.getWebApiManagerFactory().add(this);
        }

        @Override
        public boolean matches(final HttpServletRequest request) {
            // Determina si este manejador procesa la solicitud
            return request.getServletPath().startsWith(pathPrefix);
        }

        @Override
        public void process(final HttpServletRequest request, final HttpServletResponse response,
                final FilterChain chain) throws IOException, ServletException {
            // Procesamiento de la solicitud y escritura de la respuesta
        }

        @Override
        protected void writeHeaders(final HttpServletResponse response) {
            // Configuración de las cabeceras de la respuesta (según sea necesario)
        }
    }

Como ejemplos de implementación, resultan útiles como referencia
`fess-webapp-v1-api <https://github.com/codelibs/fess-webapp-v1-api>`__,
que proporciona ``/api/v1``, y `fess-webapp-classic-api
<https://github.com/codelibs/fess-webapp-classic-api>`__, que
proporciona ``/json`` y ``/suggest``.

Personalización de la Pantalla de Búsqueda
============================================

Los plugins de aplicación web no pueden añadir vistas JSP. Esto se debe
a que las vistas JSP se ubican en ``WEB-INF/view/`` del WAR del propio
|Fess|, mientras que el JAR del plugin se monta en el classpath
(``WEB-INF/classes``). Si desea modificar el diseño de la pantalla de
búsqueda, utilice una de las siguientes opciones:

- **Tema**: personaliza el diseño de la pantalla de búsqueda
  (HTML/CSS/JavaScript). Consulte :doc:`theme-development`.
- **Sustitución de systemHelper**: mediante la «sustitución de
  componentes del núcleo» descrita anteriormente, puede cambiar el
  mapeo de nombres de JSP de diseño (aunque los propios archivos JSP
  los proporciona el núcleo de |Fess|).

Construcción e Instalación
============================

::

    mvn clean package

En el directorio ``target/`` se generará un archivo JAR (por ejemplo,
``fess-webapp-example-15.8.0.jar``). El JAR generado se puede instalar
desde la consola de administración, o bien colocarlo en el directorio
``app/WEB-INF/plugin/`` y reiniciar |Fess|. Para más detalles sobre el
procedimiento de instalación, consulte :doc:`../admin/plugin-guide`.

Ejemplos de Plugins Públicos
==============================

En el proyecto |Fess| se publican los siguientes plugins de aplicación
web. Se publican en `GitHub <https://github.com/codelibs>`__ como
referencia para el desarrollo:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Plugin
     - Descripción
   * - ``fess-webapp-example``
     - Plantilla de implementación de plugins
   * - ``fess-webapp-v1-api``
     - API REST ``/api/v1``
   * - ``fess-webapp-classic-api``
     - API REST heredada ``/json`` / ``/suggest``
   * - ``fess-webapp-mcp``
     - Servidor MCP (Model Context Protocol)
   * - ``fess-webapp-semantic-search``
     - Búsqueda neuronal/búsqueda vectorial
   * - ``fess-webapp-multimodal``
     - Búsqueda multimodal (imágenes y texto)

Información de Referencia
===========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`theme-development` - Personalización de temas
- :doc:`../admin/plugin-guide` - Instalación de plugins
- :doc:`overview` - Visión general de documentación para desarrolladores
