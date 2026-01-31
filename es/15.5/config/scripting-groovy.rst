==================================
Guia de scripting Groovy
==================================

Descripcion general
===================

Groovy es el lenguaje de scripting predeterminado de |Fess|.
Se ejecuta en la maquina virtual Java (JVM) y permite escribir scripts con una sintaxis mas concisa
mientras mantiene alta compatibilidad con Java.

Sintaxis basica
===============

Declaracion de variables
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
    def map = [name: "Fess", version: "15.5"]
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

Ejemplos de scripts en configuracion de data store.

Mapeo basico
------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

Generacion de URL
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

    // Parseo de fecha
    import java.text.SimpleDateFormat
    def sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    lastModified=sdf.parse(data.date_string)

    // Conversion desde segundos epoch
    lastModified=new Date(data.timestamp * 1000L)

Scripts de trabajos programados
===============================

Ejemplos de scripts Groovy para trabajos programados.

Ejecucion de trabajo de crawl
-----------------------------

::

    return container.getComponent("crawlJob").execute();

Crawl condicional
-----------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // Crawl solo fuera de horario laboral
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").execute()
    }
    return "Skipped during business hours"

Ejecucion secuencial de multiples trabajos
------------------------------------------

::

    def results = []

    // Optimizacion de indice
    results << container.getComponent("optimizeJob").execute()

    // Ejecucion de crawl
    results << container.getComponent("crawlJob").execute()

    return results.join("\n")

Uso de clases Java
==================

Dentro de los scripts Groovy, puede usar la biblioteca estandar de Java y las clases de Fess.

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

Comunicacion HTTP
-----------------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   El acceso a recursos externos afecta el rendimiento,
   mantengalo al minimo necesario.

Acceso a componentes de Fess
============================

Puede acceder a los componentes de Fess usando ``container``.

System Helper
-------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

Obtencion de valores de configuracion
-------------------------------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

Ejecucion de busqueda
---------------------

::

    def searchHelper = container.getComponent("searchHelper")
    // Configurar parametros de busqueda y ejecutar

Manejo de errores
=================

::

    try {
        def result = processData(data)
        return result
    } catch (Exception e) {
        import org.apache.logging.log4j.LogManager
        def logger = LogManager.getLogger("script")
        logger.error("Error processing data: {}", e.message, e)
        return "Error: " + e.message
    }

Depuracion y salida de logs
===========================

Salida de logs
--------------

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", data.id)
    logger.info("Processing document: {}", data.title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message)

Salida de depuracion
--------------------

::

    // Salida a consola (solo durante desarrollo)
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

Mejores practicas
=================

1. **Mantenerlo simple**: Evitar logica compleja, escribir codigo legible
2. **Verificacion de null**: Usar operadores ``?.`` y ``?:``
3. **Manejo de excepciones**: Manejar errores inesperados con try-catch apropiado
4. **Salida de logs**: Registrar logs para facilitar la depuracion
5. **Rendimiento**: Minimizar acceso a recursos externos

Informacion de referencia
=========================

- `Documentacion oficial de Groovy <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - Descripcion general de scripting
- :doc:`../admin/dataconfig-guide` - Guia de configuracion de Data Store
- :doc:`../admin/scheduler-guide` - Guia de configuracion del programador
