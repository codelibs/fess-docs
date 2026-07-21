==================================
Guía de scripting Groovy
==================================

Descripción general
===================

Groovy es el lenguaje de scripting predeterminado de |Fess|.
Se ejecuta en la máquina virtual Java (JVM) y permite escribir scripts con una sintaxis más concisa
mientras mantiene alta compatibilidad con Java.

Sintaxis básica
===============

Declaración de variables
------------------------

::

    // Inferencia de tipo (def)
    def name = "Fess"
    def count = 100

    // Especificacion de tipo explicita
    String title = "Document Title"
    int pageNum = 1

Operaciones de cadenas
----------------------

::

    // Interpolacion de cadenas (GString)
    def id = 123
    def url = "https://example.com/doc/${id}"

    // Cadena multilinea
    def content = """
    This is a
    multi-line string
    """

    // Reemplazo
    title.replace("old", "new")
    title.replaceAll(/\s+/, " ")  // Expresion regular

    // Division y union
    def tags = "tag1,tag2,tag3".split(",")
    def joined = tags.join(", ")

    // Conversion de mayusculas/minusculas
    title.toUpperCase()
    title.toLowerCase()

Operaciones de colecciones
--------------------------

::

    // Lista
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // Mapa
    def map = [name: "Fess", version: "15.8"]
    println map.name
    println map["version"]

Estructuras condicionales
-------------------------

::

    // if-else
    if (data.status == "active") {
        return "Activo"
    } else {
        return "Inactivo"
    }

    // Operador ternario
    def result = data.count > 0 ? "Hay" : "No hay"

    // Operador Elvis (operador de coalescencia null)
    def value = data.title ?: "Sin titulo"

    // Operador de navegacion segura
    def length = data.content?.length() ?: 0

Bucles
------

::

    // for-each
    for (item in items) {
        println item
    }

    // Closure
    items.each { item ->
        println item
    }

    // Rango
    (1..10).each { println it }

Scripts de Data Store
=====================

Ejemplos de scripts en configuración de data store.

.. note::
   En los scripts de data store, cada línea ``campo=expresion`` se evalúa de forma independiente como una única expresión.
   Por lo tanto, no se pueden usar sentencias ``import``, declaraciones ``def`` multilínea ni estructuras de control multilínea que establezcan varios campos a la vez (como bloques ``if``).
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
    url=data.external_url ?: "https://example.com/default/" + data.id

Procesamiento de contenido
--------------------------

::

    // Eliminacion de etiquetas HTML
    content=data.html_content.replaceAll(/<[^>]+>/, "")

    // Concatenacion de multiples campos
    content=data.title + "\n" + data.description + "\n" + data.body

    // Limitacion de longitud
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Procesamiento de fechas
-----------------------

::

    // Parseo de fecha (expresion unica usando FQCN)
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // Conversion desde segundos epoch
    lastModified=new Date(data.timestamp * 1000L)

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
     - La cadena de URL a convertir y el resultado de coincidencia de expresión regular ( ``Matcher`` ). Disponible en configuraciones de reemplazo con el prefijo ``groovy:``
   * - Boost de documento
     - (campos del documento)
     - Cada campo del documento objetivo está disponible como variable (se usa en expresiones de condición y de valor de boost)

Scripts de trabajos programados
===============================

Ejemplos de scripts Groovy para trabajos programados.
En los trabajos programados, ``container`` y ``executor`` están disponibles.
Pasar ``executor`` al método ``execute()`` del trabajo habilita el control de detención del trabajo.

.. note::
   Un script de trabajo programado se evalúa como un único script Groovy completo.
   Por lo tanto, a diferencia de los scripts de data store, puede usar sentencias ``import``, declaraciones ``def`` multilínea y estructuras de control multilínea.
   Los ejemplos de "Uso de clases Java", "Acceso a componentes de Fess", "Manejo de errores" y "Depuración y salida de logs" que aparecen a continuación también asumen este contexto de script completo.

Ejecución de trabajo de crawl
-----------------------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Crawl condicional
-----------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // Crawl solo fuera de horario laboral
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor)
    }
    return "Skipped during business hours"

Ejecución secuencial de múltiples trabajos
------------------------------------------

::

    def results = []

    // Actualizacion de suggest
    results << container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor)

    // Ejecucion de crawl
    results << container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor)

    return results.join("\n")

Uso de clases Java
==================

Dentro de los scripts Groovy, puede usar la biblioteca estándar de Java y las clases de Fess.

Fecha y hora
------------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

Operaciones de archivo
----------------------

::

    import java.nio.file.Files
    import java.nio.file.Paths

    def content = new String(Files.readAllBytes(Paths.get("/path/to/file.txt")))

Comunicación HTTP
-----------------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   El acceso a recursos externos afecta el rendimiento,
   manténgalo al mínimo necesario.

Acceso a componentes de Fess
============================

Puede acceder a los componentes de Fess usando ``container``.

System Helper
-------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

Obtención de valores de configuración
-------------------------------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

Ejecución de búsqueda
---------------------

::

    def searchHelper = container.getComponent("searchHelper")
    // Configurar parametros de busqueda y ejecutar

Manejo de errores
=================

Las sentencias ``import`` deben colocarse al principio del script (no pueden colocarse dentro de bloques como ``try-catch`` ).
Puede capturar excepciones con ``try-catch`` para controlar los errores del trabajo.

::

    import org.apache.logging.log4j.LogManager

    def logger = LogManager.getLogger("script")

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor)
    } catch (Exception e) {
        logger.error("Failed to execute crawl job: {}", e.message, e)
        return "Error: " + e.message
    }

Depuración y salida de logs
===========================

Salida de logs
--------------

::

    import org.apache.logging.log4j.LogManager

    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", value)
    logger.info("Processing: {}", title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message, e)

Salida de depuración
--------------------

::

    // Salida a consola (solo durante desarrollo)
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

Mejores prácticas
=================

1. **Mantenerlo simple**: Evitar lógica compleja, escribir código legible
2. **Verificación de null**: Usar operadores ``?.`` y ``?:``
3. **Manejo de excepciones**: Manejar errores inesperados con try-catch apropiado
4. **Salida de logs**: Registrar logs para facilitar la depuración
5. **Rendimiento**: Minimizar acceso a recursos externos

Información de referencia
=========================

- `Documentación oficial de Groovy <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - Descripción general de scripting
- :doc:`../admin/dataconfig-guide` - Guía de configuración de Data Store
- :doc:`../admin/scheduler-guide` - Guía de configuración del programador
