==================================
Guide de script JavaScript
==================================

Aperçu
======

JavaScript est le langage de script par défaut de |Fess| à partir de la version 15.9.
Il s'exécute sur Sai (un fork de Nashorn développé par CodeLibs, déjà utilisé par |Fess|
pour les expressions de ses XML de DI), et les scripts sont exécutés en tant qu'ECMAScript
6. Son identifiant est ``javascript`` ; il peut également être indiqué via les alias
``js`` et ``sai``.

Comment les scripts sont évalués
================================

Le moteur de script de |Fess| essaie d'abord de compiler le texte du script en tant
qu'« expression » unique. Ce n'est que si cela échoue à l'analyse qu'il recompile le
texte en tant que bloc d'« instructions ».

C'est pourquoi une expression simple qui se contente de retourner une valeur :

::

    content.length()

ainsi qu'un script contenant une instruction ``return`` de niveau supérieur :

::

    return container.getComponent("crawlJob").execute();

fonctionnent tous les deux sans problème. Le second exemple constitue normalement une
erreur de syntaxe en JavaScript pur, car un ``return`` de niveau supérieur n'est pas
autorisé. Mais comme il ne peut pas être compilé en tant qu'expression, il est
réinterprété comme un bloc d'instructions et s'exécute comme un script valide.

Aux endroits où chaque ligne est traitée comme une expression unique, comme dans les
scripts Data Store, un script compose de plusieurs instructions ne peut pas être utilisé.
Aux endroits où l'ensemble du script est évalué, comme dans les tâches planifiées, vous
pouvez librement utiliser des instructions multi-lignes, des déclarations de variables
``let`` / ``const`` et des structures de contrôle.

Syntaxe de base
===============

Déclaration de variables
------------------------

::

    // let (variable réaffectable)
    let name = "Fess";
    let count = 100;

    // const (constante non réaffectable)
    const title = "Document Title";
    const pageNum = 1;

Manipulation de chaînes
-----------------------

::

    // Littéraux de gabarit (ES6)
    const id = 123;
    const url = `https://example.com/doc/${id}`;

    // Chaînes multi-lignes (littéral de gabarit)
    const content = `
    This is a
    multi-line string
    `;

    // Remplacement (avec une expression régulière ; ECMAScript 6 ne possède pas String#replaceAll)
    title.replace(/old/g, "new");
    title.replace(/\s+/g, " ");  // Regrouper les espaces consécutifs en un seul

    // Division et jointure
    const tags = "tag1,tag2,tag3".split(",");
    const joined = tags.join(", ");

    // Conversion majuscules/minuscules
    title.toUpperCase();
    title.toLowerCase();

Opérations sur les collections
------------------------------

::

    // Tableaux
    const list = [1, 2, 3, 4, 5];
    const doubled = list.map(item => item * 2);
    const filtered = list.filter(item => item > 3);
    const total = list.reduce((sum, item) => sum + item, 0);

    // Objets
    const map = { name: "Fess", version: "15.9" };
    map.name;
    map["version"];

Conditions
----------

::

    // if-else
    if (data.status === "active") {
        return "Actif";
    } else {
        return "Inactif";
    }

    // Opérateur ternaire
    const result = data.count > 0 ? "Present" : "Absent";

    // Valeur par défaut (opérateur OR logique ; JavaScript n'a pas d'opérateur Elvis)
    const value = data.title || "Sans titre";

    // Le chaînage optionnel (?.) est une syntaxe ES2020, indisponible en ES6.
    // Vérifiez explicitement la valeur null à la place.
    const length = (data.content != null) ? data.content.length() : 0;

Boucles
-------

::

    // for...of (ES6)
    for (const item of items) {
        // traitement de chaque élément
    }

    // forEach (fonction fléchée)
    items.forEach(item => {
        // traitement de chaque élément
    });

    // Pour une plage, construisez un tableau ou utilisez une boucle for
    // (JavaScript n'a pas d'expression de plage comme en Groovy)
    for (let i = 1; i <= 10; i++) {
        // ...
    }

Scripts de Data Store
======================

Exemples de scripts pour la configuration Data Store.

.. note::
   Dans les scripts de data store, chaque ligne ``champ=expression`` est évaluée indépendamment en tant qu'expression unique.
   Par conséquent, les déclarations de variables telles que ``let`` / ``const`` et les structures de contrôle multi-lignes qui définissent plusieurs champs à la fois (comme les blocs ``if``) ne peuvent pas être utilisées.
   Lorsque vous utilisez des classes Java, écrivez-les en tant qu'expression unique avec le nom de classe complet (FQCN), et utilisez un opérateur ternaire par champ pour les valeurs conditionnelles (par exemple, ``url=data.published ? data.url : null`` ).
   Par ailleurs, le nom de variable ``data`` utilisé ici n'est qu'un exemple ; le nom de variable réel dépend du connecteur de data store utilisé. Consultez :doc:`../admin/dataconfig-guide` pour plus de détails.

Mapping de base
----------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

Génération d'URL
-----------------

::

    // Generation d'URL basee sur l'ID
    url="https://example.com/article/" + data.id

    // Combinaison de plusieurs champs
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // URL conditionnelle
    url=data.external_url || "https://example.com/default/" + data.id

Traitement du contenu
----------------------

::

    // Suppression des balises HTML
    content=data.html_content.replace(/<[^>]+>/g, "")

    // Concatenation de plusieurs champs
    content=data.title + "\n" + data.description + "\n" + data.body

    // Limitation de longueur
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Traitement des dates
---------------------

::

    // Analyse de date (expression unique utilisant FQCN ; l'interoperabilite Java utilise la meme notation qu'en Groovy)
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // Conversion depuis un timestamp Unix (le suffixe L des littéraux long n'est pas nécessaire)
    lastModified=new Date(data.timestamp * 1000)

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
     - La chaîne URL à convertir et le résultat de la correspondance par expression régulière ( ``Matcher`` ). Disponible lorsque le remplacement porte le préfixe du nom d'un moteur enregistré, par exemple ``javascript:`` (alias ``js:``, ``sai:``)
   * - Boost de document
     - (champs du document)
     - Chaque champ du document cible est disponible en tant que variable (utilisé dans les expressions de condition et de valeur de boost)

Scripts de tâches planifiées
============================

Exemples de scripts JavaScript pour les tâches planifiées.
Dans les tâches planifiées, ``container`` et ``executor`` sont disponibles.
Passer ``executor`` à la méthode ``execute()`` du job active le contrôle d'arrêt du job.

.. note::
   Un script de tâche planifiée est évalué comme un script complet unique.
   Le moteur de script essaie d'abord de le compiler en tant qu'expression, et ne le réinterprète comme un bloc d'instructions qu'en cas d'échec ; vous pouvez donc utiliser des instructions multi-lignes, des déclarations ``let`` / ``const``, des structures de contrôle et une instruction ``return`` de niveau supérieur (voir « Comment les scripts sont évalués » ci-dessus).
   Les exemples ci-dessous « Utilisation des classes Java », « Accès aux composants Fess », « Gestion des erreurs » et « Débogage et journalisation » supposent également ce contexte de script complet.

Exécution d'un job de crawl
----------------------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Crawl conditionnel
-------------------

::

    const cal = java.util.Calendar.getInstance();
    const hour = cal.get(java.util.Calendar.HOUR_OF_DAY);

    // Crawl uniquement en dehors des heures de bureau
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    }
    return "Skipped during business hours";

Exécution séquentielle de plusieurs jobs
-----------------------------------------

::

    const results = [];

    // Mise a jour des suggestions
    results.push(container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor));

    // Execution du crawl
    results.push(container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor));

    return results.join("\n");

Utilisation des classes Java
============================

Dans les scripts JavaScript, l'interopérabilité Java de Sai (Nashorn) vous permet
d'utiliser directement les bibliothèques standard Java et les classes Fess. JavaScript
n'a pas d'instruction ``import`` : les classes s'écrivent donc toujours avec leur nom
complet (FQCN).

::

    new java.io.File("/var/log/fess/fess.log")
    java.lang.System.getProperty("user.home")
    new org.codelibs.fess.job.IndexExportJob()

Date et heure
--------------

::

    const now = java.time.LocalDateTime.now();
    const formatted = now.format(java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME);

Opérations sur les fichiers
-----------------------------

::

    const content = new java.lang.String(
        java.nio.file.Files.readAllBytes(java.nio.file.Paths.get("/path/to/file.txt")));

Communication HTTP
--------------------

::

    const client = java.net.http.HttpClient.newHttpClient();
    const request = java.net.http.HttpRequest.newBuilder()
        .uri(java.net.URI.create("https://api.example.com/data"))
        .build();
    const response = client.send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
    const body = response.body();

.. warning::
   L'accès aux ressources externes affecte les performances,
   utilisez-le au minimum nécessaire.

Accès aux composants Fess
==========================

Utilisez ``container`` pour accéder aux composants Fess.

System Helper
-------------

::

    const systemHelper = container.getComponent("systemHelper");
    const currentTime = systemHelper.getCurrentTimeAsLong();

Récupération des valeurs de configuration
-------------------------------------------

::

    const fessConfig = container.getComponent("fessConfig");
    const indexName = fessConfig.getIndexDocumentUpdateIndex();

Exécution de recherche
------------------------

::

    const searchHelper = container.getComponent("searchHelper");
    // Configurer les parametres de recherche et executer

Gestion des erreurs
====================

JavaScript n'a pas d'instruction ``import`` ; les contraintes de placement propres à
Groovy ne s'appliquent donc pas ici. Vous pouvez intercepter les exceptions avec
``try-catch`` pour contrôler les erreurs de job.

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    } catch (e) {
        logger.error("Failed to execute crawl job: {}", e.getMessage(), e);
        return "Error: " + e.getMessage();
    }

Débogage et journalisation
============================

Sortie de logs
--------------

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    logger.debug("Debug message: {}", value);
    logger.info("Processing: {}", title);
    logger.warn("Warning: {}", message);
    logger.error("Error: {}", e.getMessage(), e);

Sortie de débogage
--------------------

Pour inspecter rapidement le contenu d'une variable, convertissez-la en chaîne avec
``JSON.stringify`` et journalisez le résultat.

::

    logger.debug("data = {}", JSON.stringify({ id: data.id, title: data.title }));

Migration depuis Groovy
=======================

Gardez à l'esprit les différences suivantes lorsque vous portez un script Groovy
existant vers JavaScript.

Précision arithmétique
----------------------

Les opérations numériques de JavaScript utilisent toujours des nombres à virgule
flottante en double précision. Par exemple, l'expression suivante retourne l'entier
``34`` en Groovy, mais le nombre à virgule flottante ``34.0`` en JavaScript.

::

    10 * boost1 + boost2

En revanche, le type de retour d'une méthode appelée via l'interopérabilité Java
conserve le type du côté Java, si bien que ``content.length()`` continue de retourner
un entier.

Réécriture de la syntaxe propre à Groovy
-----------------------------------------

La syntaxe suivante, propre à Groovy, doit être réécrite pour JavaScript.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Groovy
     - JavaScript
     - Description
   * - ``1000L``
     - ``1000``
     - Le suffixe ``L`` des littéraux long n'est pas nécessaire ; écrivez le nombre tel quel
   * - ``["a", "b"] as String[]``
     - ``["a", "b"]``
     - Un tableau JavaScript est automatiquement converti en tableau Java lorsqu'il est
       passé à une méthode attendant ``String[]`` ; aucun cast n'est nécessaire

Interopérabilité Java
----------------------

La notation de l'interopérabilité Java est la même que celle de Nashorn, et diffère peu
de celle de Groovy. Les appels de constructeurs entièrement qualifiés tels que
``new java.io.File(...)``, ``java.lang.System.getProperty(...)`` et
``new org.codelibs.fess.job.IndexExportJob()`` se résolvent tels quels.

Syntaxe ES6
-----------

Le moteur JavaScript de |Fess| s'exécutant en tant qu'ECMAScript 6, vous pouvez utiliser
la syntaxe ES6 telle que ``let`` / ``const``, les fonctions fléchées, les littéraux de
gabarit, la déstructuration, ``for...of`` et ``class``. En revanche, le chaînage
optionnel (``?.``) et l'opérateur de coalescence des nuls (``??``) sont des syntaxes
ES2020 et ultérieures, et ne peuvent pas être utilisés.

Bonnes pratiques
================

1. **Garder la simplicité** : Éviter les logiques complexes, privilégier un code lisible
2. **Valeurs par défaut** : Utiliser l'opérateur OR logique (``||``) à la place de l'opérateur Elvis
3. **Gestion des exceptions** : Gérer les erreurs inattendues avec try-catch approprié
4. **Sortie de logs** : Afficher des logs pour faciliter le débogage
5. **Performance** : Minimiser les accès aux ressources externes
6. **Opérations numériques** : Là où un entier est attendu, utilisez directement le résultat d'un appel de méthode via l'interopérabilité Java, ou convertissez explicitement si nécessaire

Informations de référence
==========================

- `Référence JavaScript de MDN <https://developer.mozilla.org/fr/docs/Web/JavaScript>`__
- :doc:`scripting-overview` - Aperçu du scripting
- :doc:`scripting-groovy` - Guide du scripting Groovy (plugin)
- :doc:`../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../admin/scheduler-guide` - Guide de configuration du planificateur
