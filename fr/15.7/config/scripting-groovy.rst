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
    def map = [name: "Fess", version: "15.7"]
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

.. note::
   Dans les scripts de data store, chaque ligne ``champ=expression`` est evaluee independamment en tant qu'expression unique.
   Par consequent, les instructions ``import``, les declarations ``def`` multi-lignes et les structures de controle multi-lignes qui definissent plusieurs champs a la fois (comme les blocs ``if``) ne peuvent pas etre utilisees.
   Lorsque vous utilisez des classes Java, ecrivez-les en tant qu'expression unique avec le nom de classe complet (FQCN), et utilisez un operateur ternaire par champ pour les valeurs conditionnelles (par exemple, ``url=data.published ? data.url : null`` ).
   Par ailleurs, le nom de variable ``data`` utilise ici n'est qu'un exemple ; le nom de variable reel depend du connecteur de data store utilise. Consultez :doc:`../admin/dataconfig-guide` pour plus de details.

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

    // Analyse de date (expression unique utilisant FQCN)
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // Conversion depuis un timestamp Unix
    lastModified=new Date(data.timestamp * 1000L)

Objets disponibles
==================

Les objets disponibles dans les scripts varient en fonction du contexte d'execution.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Contexte
     - Objet
     - Description
   * - Tous les contextes
     - ``container``
     - Conteneur DI. Utilise pour acceder aux composants via ``container.getComponent("...")``
   * - Taches planifiees
     - ``executor``
     - Controle d'execution des jobs ( ``JobExecutor`` ). Necessaire pour le support de l'arret des jobs
   * - Data Store
     - (specifique au connecteur)
     - Variables d'enregistrement de donnees fournies par chaque data store. Le nom de la variable depend du connecteur
   * - Mappage de chemins
     - ``url`` , ``matcher``
     - La chaine URL a convertir et le resultat de la correspondance par expression reguliere ( ``Matcher`` ). Disponible dans les parametres de remplacement avec le prefixe ``groovy:``
   * - Boost de document
     - (champs du document)
     - Chaque champ du document cible est disponible en tant que variable (utilise dans les expressions de condition et de valeur de boost)

Scripts de taches planifiees
============================

Exemples de scripts Groovy pour les taches planifiees.
Dans les taches planifiees, ``container`` et ``executor`` sont disponibles.
Passer ``executor`` a la methode ``execute()`` du job active le controle d'arret du job.

.. note::
   Un script de tache planifiee est evalue en tant que script Groovy unique et complet.
   Par consequent, contrairement aux scripts de data store, vous pouvez utiliser des instructions ``import``, des declarations ``def`` multi-lignes et des structures de controle multi-lignes.
   Les exemples ci-dessous « Utilisation des classes Java », « Acces aux composants Fess », « Gestion des erreurs » et « Debogage et journalisation » supposent egalement ce contexte de script complet.

Execution d'un job de crawl
--------------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Crawl conditionnel
----------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // Crawl uniquement en dehors des heures de bureau
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor)
    }
    return "Skipped during business hours"

Execution sequentielle de plusieurs jobs
------------------------

::

    def results = []

    // Mise a jour des suggestions
    results << container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor)

    // Execution du crawl
    results << container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor)

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

Les instructions ``import`` doivent etre placees en haut du script (elles ne peuvent pas etre placees dans des blocs tels que ``try-catch`` ).
Vous pouvez intercepter les exceptions avec ``try-catch`` pour controler les erreurs de job.

::

    import org.apache.logging.log4j.LogManager

    def logger = LogManager.getLogger("script")

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor)
    } catch (Exception e) {
        logger.error("Failed to execute crawl job: {}", e.message, e)
        return "Error: " + e.message
    }

Debogage et journalisation
==================

Sortie de logs
--------

::

    import org.apache.logging.log4j.LogManager

    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", value)
    logger.info("Processing: {}", title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message, e)

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
