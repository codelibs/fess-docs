==================================
Guide de script Groovy
==================================

Aperçu
====

Groovy est le langage de script par défaut de |Fess|.
Il fonctionne sur la machine virtuelle Java (JVM) et, tout en étant hautement compatible avec Java,
permet d'écrire des scripts avec une syntaxe plus concise.

Syntaxe de base
========

Déclaration de variables
--------

::

    // Inference de type (def)
    def name = "Fess"
    def count = 100

    // Specification de type explicite
    String title = "Document Title"
    int pageNum = 1

Manipulation de chaînes
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

Opérations sur les collections
----------------

::

    // Listes
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // Maps
    def map = [name: "Fess", version: "15.8"]
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
   Dans les scripts de data store, chaque ligne ``champ=expression`` est évaluée indépendamment en tant qu'expression unique.
   Par conséquent, les instructions ``import``, les déclarations ``def`` multi-lignes et les structures de contrôle multi-lignes qui définissent plusieurs champs à la fois (comme les blocs ``if``) ne peuvent pas être utilisées.
   Lorsque vous utilisez des classes Java, écrivez-les en tant qu'expression unique avec le nom de classe complet (FQCN), et utilisez un opérateur ternaire par champ pour les valeurs conditionnelles (par exemple, ``url=data.published ? data.url : null`` ).
   Par ailleurs, le nom de variable ``data`` utilisé ici n'est qu'un exemple ; le nom de variable réel dépend du connecteur de data store utilisé. Consultez :doc:`../admin/dataconfig-guide` pour plus de détails.

Mapping de base
------------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

Génération d'URL
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

Les objets disponibles dans les scripts varient en fonction du contexte d'exécution.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Contexte
     - Objet
     - Description
   * - Tous les contextes
     - ``container``
     - Conteneur DI. Utilisé pour accéder aux composants via ``container.getComponent("...")``
   * - Tâches planifiées
     - ``executor``
     - Contrôle d'exécution des jobs ( ``JobExecutor`` ). Nécessaire pour le support de l'arrêt des jobs
   * - Data Store
     - (spécifique au connecteur)
     - Variables d'enregistrement de données fournies par chaque data store. Le nom de la variable dépend du connecteur
   * - Mappage de chemins
     - ``url`` , ``matcher``
     - La chaîne URL à convertir et le résultat de la correspondance par expression régulière ( ``Matcher`` ). Disponible dans les paramètres de remplacement avec le préfixe ``groovy:``
   * - Boost de document
     - (champs du document)
     - Chaque champ du document cible est disponible en tant que variable (utilisé dans les expressions de condition et de valeur de boost)

Scripts de tâches planifiées
============================

Exemples de scripts Groovy pour les tâches planifiées.
Dans les tâches planifiées, ``container`` et ``executor`` sont disponibles.
Passer ``executor`` à la méthode ``execute()`` du job active le contrôle d'arrêt du job.

.. note::
   Un script de tâche planifiée est évalué en tant que script Groovy unique et complet.
   Par conséquent, contrairement aux scripts de data store, vous pouvez utiliser des instructions ``import``, des déclarations ``def`` multi-lignes et des structures de contrôle multi-lignes.
   Les exemples ci-dessous « Utilisation des classes Java », « Accès aux composants Fess », « Gestion des erreurs » et « Débogage et journalisation » supposent également ce contexte de script complet.

Exécution d'un job de crawl
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

Exécution séquentielle de plusieurs jobs
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

Dans les scripts Groovy, vous pouvez utiliser les bibliothèques standard Java et les classes Fess.

Date et heure
----------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

Opérations sur les fichiers
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
   L'accès aux ressources externes affecte les performances,
   utilisez-le au minimum nécessaire.

Accès aux composants Fess
==============================

Utilisez ``container`` pour accéder aux composants Fess.

System Helper
----------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

Récupération des valeurs de configuration
------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

Exécution de recherche
----------

::

    def searchHelper = container.getComponent("searchHelper")
    // Configurer les parametres de recherche et executer

Gestion des erreurs
==================

Les instructions ``import`` doivent être placées en haut du script (elles ne peuvent pas être placées dans des blocs tels que ``try-catch`` ).
Vous pouvez intercepter les exceptions avec ``try-catch`` pour contrôler les erreurs de job.

::

    import org.apache.logging.log4j.LogManager

    def logger = LogManager.getLogger("script")

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor)
    } catch (Exception e) {
        logger.error("Failed to execute crawl job: {}", e.message, e)
        return "Error: " + e.message
    }

Débogage et journalisation
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

Sortie de débogage
----------------

::

    // Sortie console (developpement uniquement)
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

Bonnes pratiques
==================

1. **Garder la simplicité** : Éviter les logiques complexes, privilégier un code lisible
2. **Vérification de null** : Utiliser les opérateurs ``?.`` et ``?:``
3. **Gestion des exceptions** : Gérer les erreurs inattendues avec try-catch approprié
4. **Sortie de logs** : Afficher des logs pour faciliter le débogage
5. **Performance** : Minimiser les accès aux ressources externes

Informations de référence
========

- `Documentation officielle Groovy <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - Aperçu du scripting
- :doc:`../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../admin/scheduler-guide` - Guide de configuration du planificateur
