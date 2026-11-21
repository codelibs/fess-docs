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
|Fess|, cree una subclase de la clase de destino y **vuelva a
registrarla con el mismo nombre de componente** en un archivo de
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
   definición del núcleo (por ejemplo, ``queryHelper`` en ``app.xml``).
   Esto debe sincronizarse en cada versión de |Fess|. Si el archivo
   sigue llamando a un método que se eliminó del núcleo, la
   inicialización de esa definición de componente falla con
   ``BeanMethodNotFoundException``. Por ejemplo, en 15.9 se eliminó
   ``addDesignJspFileName`` de ``systemHelper``, por lo que un archivo
   de sustitución que lo llame falla. Este coste de mantenimiento es la
   razón por la que se recomienda la adición en lugar de la sustitución.

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

.. _webapp-plugin-password-encoder:

Adición de un Algoritmo de Hash de Contraseñas (fess++.xml)
-----------------------------------------------------------

El hash de la contraseña de un usuario local lo genera un componente. Una contraseña almacenada se escribe como ``{id}hash``. |Fess| toma el ``id`` del valor almacenado y, para una contraseña nueva, el valor de ``app.password.algorithm`` (``bcrypt`` por defecto), y busca el componente DI llamado ``<id>PasswordEncoder``, de la misma forma que se resuelven ``<sso.type>Authenticator`` y ``<storage.type>StorageClient``. |Fess| registra por sí mismo ``bcryptPasswordEncoder``. Para añadir un algoritmo, implemente ``org.codelibs.fess.crypto.password.PasswordEncoder`` y registre la clase en ``fess++.xml``, que Lasta Di fusiona con el ``fess.xml`` del núcleo de |Fess|:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="argon2PasswordEncoder"
            class="com.example.Argon2PasswordEncoder">
        </component>
    </components>

La interfaz tiene los siguientes métodos:

.. list-table:: Métodos de PasswordEncoder
   :header-rows: 1
   :widths: 35 65

   * - Método
     - Descripción
   * - ``String encode(String rawPassword)``
     - Calcula el hash de una contraseña. El resultado se almacena después del prefijo ``{id}``, que añade |Fess|. Lance ``IllegalArgumentException`` para una contraseña que no se pueda convertir en hash de forma fiel; el mensaje no debe contener la contraseña.
   * - ``boolean matches(String rawPassword, String encodedPassword)``
     - Verifica una contraseña frente a un hash generado por este codificador. Devuelva ``false`` para una contraseña incorrecta y para un hash mal formado.
   * - ``boolean needsUpgrade(String encodedPassword)``
     - Opcional (por defecto ``false``). Indica si un hash almacenado es más débil que lo que ``encode`` genera ahora, de modo que se calcule de nuevo en el siguiente inicio de sesión de su usuario. BCrypt devuelve ``true`` si el coste es inferior a ``app.password.bcrypt.cost``.
   * - ``int getMaxPasswordBytes()``
     - Opcional (por defecto ``0``, sin límite). La contraseña más larga, en bytes UTF-8, que acepta ``encode``. BCrypt devuelve ``72``.
   * - ``boolean isVerificationCostly()`` y ``void applyTimingPadding()``
     - Opcional (por defecto ``false`` y ninguna acción). Un algoritmo deliberadamente lento devuelve ``true`` y emplea en ``applyTimingPadding()`` un tiempo similar al de un ``matches``. |Fess| lo llama cuando un inicio de sesión falla sin que se haya verificado un hash (por ejemplo, con un usuario desconocido), para que el tiempo de respuesta no revele si el usuario existe.

Para usar el codificador:

#. Coloque el jar en el directorio ``WEB-INF/plugin``. Como en cualquier plugin de aplicación web, el manifiesto necesita ``Fess-WebAppJar: true`` (consulte "pom.xml y el Manifiesto"); sin él, el componente no se encuentra.
#. Establezca ``app.password.algorithm`` en ``fess_config.properties`` con el id (``argon2`` para ``argon2PasswordEncoder``). El id debe estar en minúsculas y no debe contener ``}``. A partir de ese momento, las contraseñas nuevas y las modificadas se procesan con él. Las contraseñas almacenadas con otro id, o como un hash antiguo sin id, se calculan de nuevo en el siguiente inicio de sesión correcto de su usuario mientras ``app.password.upgrade.enabled`` sea ``true`` (valor por defecto).

Tenga en cuenta lo siguiente:

- El codificador es un singleton compartido por todos los hilos, por lo que debe ser seguro para hilos.
- El límite de longitud pertenece al codificador. Cuando se establece una contraseña (pantalla de gestión de usuarios, cambio de contraseña forzado, ``/api/v2/auth/password`` y la API de administración), |Fess| rechaza una contraseña más larga que ``getMaxPasswordBytes()`` del algoritmo de ``app.password.algorithm`` con "La contraseña no debe superar los N bytes."; con ``0`` o menos, solo comprueba ``password.max.length``. |Fess| no aplica ningún límite de longitud al verificar un hash almacenado; que una contraseña más larga pueda coincidir depende de ``matches``.
- Mantenga el plugin instalado mientras haya contraseñas almacenadas con su id. Sin el componente, un hash con ese id nunca coincide: esos usuarios no pueden iniciar sesión y sus hashes no se calculan de nuevo.
- Si ``app.password.algorithm`` nombra un id sin componente (por ejemplo, tras eliminar el jar del plugin), |Fess| arranca igualmente y los usuarios cuyo hash tiene otro id pueden seguir iniciando sesión, pero establecer una contraseña falla con un error que nombra ``app.password.algorithm``.

Personalización de la Pantalla de Búsqueda
============================================

Los plugins de aplicación web no pueden añadir vistas JSP. Esto se debe
a que las vistas JSP se ubican en ``WEB-INF/view/`` del WAR del propio
|Fess|, mientras que el JAR del plugin se monta en el classpath
(``WEB-INF/classes``). Si desea modificar el diseño de la pantalla de
búsqueda, utilice un tema. El tema personaliza el
diseño de la pantalla de búsqueda (HTML/CSS/JavaScript). Consulte
:doc:`theme-development`.

Construcción e Instalación
============================

::

    mvn clean package

En el directorio ``target/`` se generará un archivo JAR (por ejemplo,
``fess-webapp-example-15.10.0.jar``). El JAR generado se puede instalar
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
   * - ``fess-webapp-bangs``
     - Bangs al estilo de DuckDuckGo (``!g``) que envían una búsqueda a otro sitio
   * - ``fess-webapp-semantic-search``
     - Búsqueda neuronal/búsqueda vectorial (obsoleto; reemplazado por la integración en el
       núcleo en la 15.8)
   * - ``fess-webapp-multimodal``
     - Búsqueda multimodal (imágenes y texto)

Información de Referencia
===========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`theme-development` - Personalización de temas
- :doc:`../admin/plugin-guide` - Instalación de plugins
- :doc:`overview` - Visión general de documentación para desarrolladores
