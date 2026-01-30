==================================
Guide de script Groovy
==================================

Apercu
====

Groovy est le langage de script par defaut de |Fess|.
Il fonctionne sur la machine virtuelle Java (JVM) et, tout en etant hautement compatible avec Java,
permet d'ecrire des scripts avec une syntaxe plus concise.

Syntaxe de base
========

Declaration de variables
--------

::

    // Inference de type (def)
    def name = "Fess"
    def count = 100

    // Specification de type explicite
    String title = "Document Title"
    int pageNum = 1

Manipulation de chaines
----------

::

    // Interpolation de chaines (GString)
    def id = 123
    def url = "https://example.com/doc/${id}"

    // Chaines multi-lignes
    def content = """
    This is a
    multi-line string
    """

    // Remplacement
    title.replace("old", "new")
    title.replaceAll(/\s+/, " ")  // Expression reguliere

    // Division et jointure
    def tags = "tag1,tag2,tag3".split(",")
    def joined = tags.join(", ")

    // Conversion majuscules/minuscules
    title.toUpperCase()
    title.toLowerCase()

Operations sur les collections
----------------

::

    // Listes
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // Maps
    def map = [name: "Fess", version: "15.5"]
    println map.name
    println map["version"]

Conditions
--------

::

    // if-else
    if (data.status == "active") {
        return "Actif"
    } else {
        return "Inactif"
    }

    // Operateur ternaire
    def result = data.count > 0 ? "Present" : "Absent"

    // Operateur Elvis (operateur de coalescence null)
    def value = data.title ?: "Sans titre"

    // Operateur de navigation securisee
    def length = data.content?.length() ?: 0

Boucles
----------

::

    // for-each
    for (item in items) {
        println item
    }

    // Closure
    items.each { item ->
        println item
    }

    // Plage
    (1..10).each { println it }

Scripts de Data Store
======================

Exemples de scripts pour la configuration Data Store.

Mapping de base
------------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

Generation d'URL
---------

::

    // Generation d'URL basee sur l'ID
    url="https://example.com/article/" + data.id

    // Combinaison de plusieurs champs
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // URL conditionnelle
    url=data.external_url ?: "https://example.com/default/" + data.id

Traitement du contenu
----------------

::

    // Suppression des balises HTML
    content=data.html_content.replaceAll(/<[^>]+>/, "")

    // Concatenation de plusieurs champs
    content=data.title + "\n" + data.description + "\n" + data.body

    // Limitation de longueur
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Traitement des dates
----------

::

    // Analyse de date
    import java.text.SimpleDateFormat
    def sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    lastModified=sdf.parse(data.date_string)

    // Conversion depuis un timestamp Unix
    lastModified=new Date(data.timestamp * 1000L)

Scripts de taches planifiees
============================

Exemples de scripts Groovy pour les taches planifiees.

Execution d'un job de crawl
--------------------

::

    return container.getComponent("crawlJob").execute();

Crawl conditionnel
----------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // Crawl uniquement en dehors des heures de bureau
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").execute()
    }
    return "Skipped during business hours"

Execution sequentielle de plusieurs jobs
------------------------

::

    def results = []

    // Optimisation de l'index
    results << container.getComponent("optimizeJob").execute()

    // Execution du crawl
    results << container.getComponent("crawlJob").execute()

    return results.join("\n")

Utilisation des classes Java
================

Dans les scripts Groovy, vous pouvez utiliser les bibliotheques standard Java et les classes Fess.

Date et heure
----------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

Operations sur les fichiers
------------

::

    import java.nio.file.Files
    import java.nio.file.Paths

    def content = new String(Files.readAllBytes(Paths.get("/path/to/file.txt")))

Communication HTTP
--------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   L'acces aux ressources externes affecte les performances,
   utilisez-le au minimum necessaire.

Acces aux composants Fess
==============================

Utilisez ``container`` pour acceder aux composants Fess.

System Helper
----------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

Recuperation des valeurs de configuration
------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

Execution de recherche
----------

::

    def searchHelper = container.getComponent("searchHelper")
    // Configurer les parametres de recherche et executer

Gestion des erreurs
==================

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

Debogage et journalisation
==================

Sortie de logs
--------

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", data.id)
    logger.info("Processing document: {}", data.title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message)

Sortie de debogage
----------------

::

    // Sortie console (developpement uniquement)
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

Bonnes pratiques
==================

1. **Garder la simplicite** : Eviter les logiques complexes, privilegier un code lisible
2. **Verification de null** : Utiliser les operateurs ``?.`` et ``?:``
3. **Gestion des exceptions** : Gerer les erreurs inattendues avec try-catch approprie
4. **Sortie de logs** : Afficher des logs pour faciliter le debogage
5. **Performance** : Minimiser les acces aux ressources externes

Informations de reference
========

- `Documentation officielle Groovy <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - Apercu du scripting
- :doc:`../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../admin/scheduler-guide` - Guide de configuration du planificateur
