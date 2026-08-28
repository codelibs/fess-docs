==================================
Guía de scripting JavaScript
==================================

Descripción general
===================

JavaScript es el lenguaje de scripting predeterminado de |Fess| a partir de la versión 15.9.
Se ejecuta sobre Sai (un fork de Nashorn desarrollado por CodeLibs, que |Fess| ya utiliza
para las expresiones de sus XML de DI), y los scripts se ejecutan como ECMAScript 6.
Su identificador es ``javascript``, y también puede indicarse mediante los alias
``js`` y ``sai``.

Cómo se evalúan los scripts
============================

El motor de scripting de |Fess| primero intenta compilar el texto del script como una
única "expresión". Solo si eso falla al analizarse, vuelve a compilar el texto como un
bloque de "sentencias".

Por esta razón, tanto una expresión simple que solo devuelve un valor:

::

    content.length()

como un script que contiene una sentencia ``return`` de nivel superior:

::

    return container.getComponent("crawlJob").execute();

funcionan sin problemas. Lo segundo normalmente sería un error de sintaxis en JavaScript
puro, ya que un ``return`` de nivel superior no está permitido. Pero como no se puede
compilar como expresión, se reinterpreta como un bloque de sentencias y se ejecuta como
un script válido.

En los lugares donde cada línea se trata como una única expresión, como en los scripts
de data store, no se puede usar un script formado por varias sentencias. En los lugares
donde se evalúa el script completo, como en los trabajos programados, puede usar
libremente sentencias de varias líneas, declaraciones de variables ``let`` / ``const`` y
estructuras de control.

Sintaxis básica
===============

Declaración de variables
--------------------------

::

    // let (variable reasignable)
    let name = "Fess";
    let count = 100;

    // const (constante no reasignable)
    const title = "Document Title";
    const pageNum = 1;

Operaciones de cadenas
------------------------

::

    // Literales de plantilla (ES6)
    const id = 123;
    const url = `https://example.com/doc/${id}`;

    // Cadena multilinea (literal de plantilla)
    const content = `
    This is a
    multi-line string
    `;

    // Reemplazo (con expresion regular; ECMAScript 6 no tiene String#replaceAll)
    title.replace(/old/g, "new");
    title.replace(/\s+/g, " ");  // Colapsar espacios consecutivos en uno

    // Division y union
    const tags = "tag1,tag2,tag3".split(",");
    const joined = tags.join(", ");

    // Conversion de mayusculas/minusculas
    title.toUpperCase();
    title.toLowerCase();

Operaciones de colecciones
-----------------------------

::

    // Arrays
    const list = [1, 2, 3, 4, 5];
    const doubled = list.map(item => item * 2);
    const filtered = list.filter(item => item > 3);
    const total = list.reduce((sum, item) => sum + item, 0);

    // Objetos
    const map = { name: "Fess", version: "15.9" };
    map.name;
    map["version"];

Estructuras condicionales
-------------------------

::

    // if-else
    if (data.status === "active") {
        return "Activo";
    } else {
        return "Inactivo";
    }

    // Operador ternario
    const result = data.count > 0 ? "Hay" : "No hay";

    // Valor por defecto (operador OR logico; JavaScript no tiene operador Elvis)
    const value = data.title || "Sin titulo";

    // El encadenamiento opcional (?.) es sintaxis de ES2020 y no esta disponible en ES6.
    // Compruebe null explicitamente en su lugar.
    const length = (data.content != null) ? data.content.length() : 0;

Bucles
------

::

    // for...of (ES6)
    for (const item of items) {
        // procesar cada elemento
    }

    // forEach (funcion flecha)
    items.forEach(item => {
        // procesar cada elemento
    });

    // Para un rango, genere un array o use un bucle for
    // (JavaScript no tiene una expresion de rango como la de Groovy)
    for (let i = 1; i <= 10; i++) {
        // ...
    }

Scripts de Data Store
=====================

Ejemplos de scripts en configuración de data store.

.. note::
   En los scripts de data store, cada línea ``campo=expresion`` se evalúa de forma independiente como una única expresión.
   Por lo tanto, no se pueden usar declaraciones de variables como ``let`` / ``const`` ni estructuras de control multilínea que establezcan varios campos a la vez (como bloques ``if``).
   Al usar clases Java, escríbalas como una única expresión con el nombre de clase completamente calificado (FQCN), y use el operador ternario por campo para los valores condicionales (por ejemplo, ``url=data.published ? data.url : null`` ).
   Además, el nombre de variable ``data`` usado aquí es solo un ejemplo; el nombre de variable real depende del conector de data store utilizado. Consulte :doc:`../admin/dataconfig-guide` para más detalles.

Mapeo básico
------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

Generación de URL
-----------------

::

    // Generacion de URL basada en ID
    url="https://example.com/article/" + data.id

    // Combinacion de multiples campos
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // URL condicional
    url=data.external_url || "https://example.com/default/" + data.id

Procesamiento de contenido
--------------------------

::

    // Eliminacion de etiquetas HTML
    content=data.html_content.replace(/<[^>]+>/g, "")

    // Concatenacion de multiples campos
    content=data.title + "\n" + data.description + "\n" + data.body

    // Limitacion de longitud
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Procesamiento de fechas
-----------------------

::

    // Parseo de fecha (expresion unica usando FQCN; la interoperabilidad con Java usa la misma notacion que Groovy)
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // Conversion desde segundos epoch (no se necesita el sufijo L de long)
    lastModified=new Date(data.timestamp * 1000)

Objetos disponibles
===================

Los objetos disponibles en los scripts varían según el contexto de ejecución.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Contexto
     - Objeto
     - Descripción
   * - Todos los contextos
     - ``container``
     - Contenedor DI. Se usa para acceder a los componentes mediante ``container.getComponent("...")``
   * - Trabajos programados
     - ``executor``
     - Control de ejecución de trabajos ( ``JobExecutor`` ). Necesario para el soporte de detención de trabajos
   * - Data Store
     - (específico del conector)
     - Variables de registro de datos proporcionadas por cada data store. El nombre de la variable depende del conector
   * - Mapeo de rutas
     - ``url`` , ``matcher``
     - La cadena de URL a convertir y el resultado de coincidencia de expresión regular ( ``Matcher`` ). Disponible cuando el reemplazo lleva el prefijo del nombre de un motor registrado, por ejemplo ``javascript:`` (alias ``js:``, ``sai:``)
   * - Boost de documento
     - (campos del documento)
     - Cada campo del documento objetivo está disponible como variable (se usa en expresiones de condición y de valor de boost)

Scripts de trabajos programados
===============================

Ejemplos de scripts JavaScript para trabajos programados.
En los trabajos programados, ``container`` y ``executor`` están disponibles.
Pasar ``executor`` al método ``execute()`` del trabajo habilita el control de detención del trabajo.

.. note::
   Un script de trabajo programado se evalúa como un único script completo.
   El motor de scripting primero intenta compilarlo como expresión y solo lo reinterpreta como un bloque de sentencias si eso falla, por lo que se pueden usar sentencias de varias líneas, declaraciones ``let`` / ``const``, estructuras de control y una sentencia ``return`` de nivel superior (consulte "Cómo se evalúan los scripts" más arriba).
   Los ejemplos de "Uso de clases Java", "Acceso a componentes de Fess", "Manejo de errores" y "Depuración y salida de logs" que aparecen a continuación también asumen este contexto de script completo.

Ejecución de trabajo de crawl
-----------------------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Crawl condicional
-----------------

::

    const cal = java.util.Calendar.getInstance();
    const hour = cal.get(java.util.Calendar.HOUR_OF_DAY);

    // Crawl solo fuera de horario laboral
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    }
    return "Skipped during business hours";

Ejecución secuencial de múltiples trabajos
------------------------------------------

::

    const results = [];

    // Actualizacion de suggest
    results.push(container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor));

    // Ejecucion de crawl
    results.push(container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor));

    return results.join("\n");

Uso de clases Java
==================

Dentro de los scripts JavaScript, gracias a la interoperabilidad con Java de Sai
(Nashorn), puede usar directamente la biblioteca estándar de Java y las clases de Fess.
JavaScript no tiene sentencia ``import``, por lo que las clases siempre se escriben con
su nombre completamente calificado (FQCN).

::

    new java.io.File("/var/log/fess/fess.log")
    java.lang.System.getProperty("user.home")
    new org.codelibs.fess.job.IndexExportJob()

Fecha y hora
------------

::

    const now = java.time.LocalDateTime.now();
    const formatted = now.format(java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME);

Operaciones de archivo
----------------------

::

    const content = new java.lang.String(
        java.nio.file.Files.readAllBytes(java.nio.file.Paths.get("/path/to/file.txt")));

Comunicación HTTP
-----------------

::

    const client = java.net.http.HttpClient.newHttpClient();
    const request = java.net.http.HttpRequest.newBuilder()
        .uri(java.net.URI.create("https://api.example.com/data"))
        .build();
    const response = client.send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
    const body = response.body();

.. warning::
   El acceso a recursos externos afecta el rendimiento,
   manténgalo al mínimo necesario.

Acceso a componentes de Fess
============================

Puede acceder a los componentes de Fess usando ``container``.

System Helper
-------------

::

    const systemHelper = container.getComponent("systemHelper");
    const currentTime = systemHelper.getCurrentTimeAsLong();

Obtención de valores de configuración
-------------------------------------

::

    const fessConfig = container.getComponent("fessConfig");
    const indexName = fessConfig.getIndexDocumentUpdateIndex();

Ejecución de búsqueda
---------------------

::

    const searchHelper = container.getComponent("searchHelper");
    // Configurar parametros de busqueda y ejecutar

Manejo de errores
=================

JavaScript no tiene sentencia ``import``, por lo que no aplican las restricciones de
ubicación de Groovy. Puede capturar excepciones con ``try-catch`` para controlar los
errores del trabajo.

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    } catch (e) {
        logger.error("Failed to execute crawl job: {}", e.getMessage(), e);
        return "Error: " + e.getMessage();
    }

Depuración y salida de logs
===========================

Salida de logs
--------------

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    logger.debug("Debug message: {}", value);
    logger.info("Processing: {}", title);
    logger.warn("Warning: {}", message);
    logger.error("Error: {}", e.getMessage(), e);

Salida de depuración
--------------------

Si desea inspeccionar rápidamente el contenido de una variable, conviértala en cadena
con ``JSON.stringify`` y regístrela en el log.

::

    logger.debug("data = {}", JSON.stringify({ id: data.id, title: data.title }));

Migración desde Groovy
=======================

Tenga en cuenta las siguientes diferencias al migrar un script Groovy existente a
JavaScript.

Precisión aritmética
---------------------

Las operaciones numéricas de JavaScript siempre usan coma flotante de doble precisión.
Por ejemplo, la siguiente expresión devuelve el entero ``34`` en Groovy, pero el número
de coma flotante ``34.0`` en JavaScript.

::

    10 * boost1 + boost2

Por otro lado, el tipo de retorno de un método invocado a través de la interoperabilidad
con Java conserva el tipo del lado Java, por lo que ``content.length()`` sigue
devolviendo un entero.

Reescritura de sintaxis exclusiva de Groovy
---------------------------------------------

La siguiente sintaxis exclusiva de Groovy debe reescribirse para JavaScript.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Groovy
     - JavaScript
     - Descripción
   * - ``1000L``
     - ``1000``
     - El sufijo ``L`` de literal long no es necesario; escriba el número literal tal cual
   * - ``["a", "b"] as String[]``
     - ``["a", "b"]``
     - Un array de JavaScript se convierte automáticamente en un array de Java al pasarlo
       a un método que espera ``String[]``, por lo que no se necesita conversión (cast)

Interoperabilidad con Java
---------------------------

La notación de la interoperabilidad con Java es la misma que la de Nashorn, y es casi
idéntica a la de Groovy. Las llamadas a constructores totalmente calificados como
``new java.io.File(...)``, ``java.lang.System.getProperty(...)`` y
``new org.codelibs.fess.job.IndexExportJob()`` se resuelven tal cual.

Sintaxis ES6
------------

Dado que el motor JavaScript de |Fess| se ejecuta como ECMAScript 6, puede usar sintaxis
ES6 como ``let`` / ``const``, funciones flecha, literales de plantilla, desestructuración,
``for...of`` y ``class``. Sin embargo, el encadenamiento opcional (``?.``) y el operador
de fusión nula (``??``) son sintaxis de ES2020 en adelante y no se pueden usar.

Mejores prácticas
=================

1. **Mantenerlo simple**: Evitar lógica compleja, escribir código legible
2. **Valores por defecto**: Use el operador OR lógico (``||``) en lugar del operador Elvis
3. **Manejo de excepciones**: Manejar errores inesperados con try-catch apropiado
4. **Salida de logs**: Registrar logs para facilitar la depuración
5. **Rendimiento**: Minimizar acceso a recursos externos
6. **Operaciones numéricas**: Donde se espera un entero, use directamente el resultado de una llamada a un método por interoperabilidad con Java, o conviértalo explícitamente si es necesario

Información de referencia
=========================

- `Referencia de JavaScript de MDN <https://developer.mozilla.org/es/docs/Web/JavaScript>`__
- :doc:`scripting-overview` - Descripción general de scripting
- :doc:`scripting-groovy` - Guía de scripting Groovy (plugin)
- :doc:`../admin/dataconfig-guide` - Guía de configuración de data store
- :doc:`../admin/scheduler-guide` - Guía de configuración del programador
