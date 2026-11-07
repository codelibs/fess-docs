====================================
Aperçu du scripting
====================================

Aperçu
======

Dans |Fess|, vous pouvez utiliser des scripts pour implémenter une logique personnalisée dans diverses situations.
En tirant parti des scripts, vous pouvez contrôler de manière flexible le traitement des données lors du crawl,
la transformation des URL et l'exécution des tâches planifiées.

Langages de script pris en charge
==================================

|Fess| prend en charge les langages de script suivants :

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Langage
     - Identifiant
     - Description
   * - JavaScript
     - ``javascript`` (alias : ``js`` , ``sai`` )
     - Le langage de script intégré par défaut dans |Fess|, et également le langage de
       script par défaut ( ``Constants.DEFAULT_SCRIPT`` ). Il s'exécute sur Sai (un fork
       de Nashorn développé par CodeLibs, déjà utilisé par |Fess| pour les expressions de
       ses XML de DI) ; les scripts sont exécutés en tant qu'ECMAScript 6.
   * - Groovy
     - ``groovy``
     - Fourni sous forme de plugin ``fess-script-groovy``, qui **ne fait pas partie de la
       distribution**. Installez-le depuis l'écran d'administration ou avec
       ``bin/fess-setup install plugin fess-script-groovy``.
   * - OGNL
     - ``ognl``
     - Fourni sous forme de plugin ``fess-script-ognl``, qui **ne fait pas partie de la
       distribution**. Il évalue une expression unique (sans instruction). Voir
       :doc:`scripting-ognl`.

.. note::
   Une configuration de script sans type de script enregistré est traitée comme du
   Groovy. Il ne s'agit pas d'une mesure de transition temporaire mais d'un comportement
   permanent : une configuration créée avant la 15.9 conserve son script en syntaxe
   Groovy sans type de script enregistré, et c'est précisément ce comportement par défaut
   qui lui permet de continuer à fonctionner sans changement après une mise à niveau.
   Une configuration créée à partir de la 15.9 a son type de script explicitement
   enregistré comme ``javascript``.

   Sauf indication contraire, les exemples de scripts de cette documentation sont écrits
   en syntaxe JavaScript. Pour la syntaxe Groovy, consultez :doc:`scripting-groovy`.

Cas d'utilisation des scripts
==============================

Configuration du Data Store
----------------------------

Dans les connecteurs Data Store, des scripts sont utilisés pour mapper les données récupérées
vers les champs de l'index. La configuration s'écrit au format ``nom_de_champ=expression``, une par ligne ;
chaque ligne est évaluée comme une expression de script indépendante (JavaScript par défaut).

::

    url=site_url
    title=name
    content=description
    last_modified=updated_at

Les noms de variables disponibles dans les scripts Data Store varient selon le type de connecteur.
Par exemple, pour les Data Stores CSV et JSON, chaque nom de colonne ou de champ est disponible
directement en tant que variable (sans préfixe commun tel que ``data``).
Pour les connecteurs de type fichier (Box, Google Drive, OneDrive, etc.), le préfixe est ``file.*`` ;
pour Slack, c'est ``message.*`` ; le préfixe diffère selon le connecteur.
Consultez la documentation de chaque connecteur Data Store pour connaître les variables disponibles.

.. note::
   Chaque ligne d'un Data Store étant évaluée comme une expression unique, les blocs ``if`` multi-lignes
   ainsi que les déclarations de variables telles que ``let`` / ``const`` ne peuvent pas être utilisés.
   Pour conditionner une valeur, utilisez l'opérateur ternaire pour chaque champ
   (exemple : ``title=enabled === "true" ? name : null``). Pour référencer une classe, utilisez
   le nom complètement qualifié (FQCN) en ligne.

Mapping de chemin
-----------------

Le mapping de chemin est une fonctionnalité permettant de normaliser et de transformer les URL crawlées.
Par défaut, il se configure avec un couple « expression régulière » / « chaîne de remplacement » et
ne constitue pas un script. Par exemple, en indiquant ``http://`` comme expression régulière
et ``https://`` comme chaîne de remplacement, le schéma de l'URL est remplacé.

Lorsque la chaîne de remplacement commence par ``(nom du moteur):``, la partie avant les
deux-points est lue comme le nom d'un moteur de script ; si elle correspond à un moteur
enregistré, le reste de la chaîne est évalué en tant que script par ce moteur. Par
exemple, ``groovy:`` sélectionne le moteur Groovy (nécessite le plugin
``fess-script-groovy``), et ``javascript:`` (alias ``js:``, ``sai:``) sélectionne le
moteur JavaScript. Si la partie avant les deux-points ne correspond à aucun moteur
enregistré — ``https://`` dans une chaîne de remplacement ordinaire, par exemple —,
la chaîne entière n'est pas traitée comme un script et est utilisée telle quelle comme
simple chaîne de remplacement d'expression régulière. Lorsque la chaîne est évaluée en
tant que script, ``url`` représente la chaîne URL à transformer et ``matcher``
représente le ``java.util.regex.Matcher`` de l'expression régulière.

::

    javascript:url.replace(/http:\/\//g, "https://")

Tâches planifiées
-----------------

Dans les tâches planifiées, vous pouvez écrire une logique de traitement personnalisée dans un
script. L'ensemble du script est évalué comme un seul script, ce qui permet d'utiliser des
instructions multi-lignes, y compris, en JavaScript, des déclarations de variables
``let`` / ``const`` et des structures de contrôle.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Une instruction ``return`` de niveau supérieur est normalement une erreur de syntaxe en
JavaScript. Le moteur de script de |Fess| essaie d'abord de compiler le script en tant
qu'expression, et ne le recompile en bloc d'instructions que si cela échoue. Cet exemple ne
peut pas être compilé en tant qu'expression ; il est donc compilé en bloc d'instructions et
s'exécute tel quel. Voir :doc:`scripting-javascript` pour plus de détails.

Les méthodes comme ``logLevel("info")`` sont des méthodes de la classe du job (``ExecJob`` et ses
sous-classes) et peuvent être enchaînées. Pour la variable ``executor``, consultez la section
« Contexte d'exécution et objets disponibles ».

Syntaxe de base
===============

Voici des exemples de syntaxe JavaScript de base. Les commentaires utilisent ``//`` (commentaire de ligne)
ou ``/* */`` (commentaire de bloc). Notez que les commentaires commençant par ``#`` ne sont pas non plus
utilisables en JavaScript.

Accès aux variables
-------------------

::

    // Champ d'un Data Store (CSV/JSON : acces par nom de colonne ou de champ)
    title

    // Recuperer un composant depuis le conteneur DI
    container.getComponent("systemHelper")

Manipulation de chaînes
------------------------

::

    // Concatenation
    title + " - " + category

    // Remplacement (avec une expression reguliere ; ECMAScript 6 ne possede pas String#replaceAll)
    content.replace(/old/g, "new")

    // Division
    tags.split(",")

Conditions
----------

::

    // Operateur ternaire
    status === "active" ? "Actif" : "Inactif"

    // Valeur par defaut si null ou vide (operateur OR logique ; JavaScript n'a pas d'operateur Elvis)
    description || "Aucune description"

Manipulation de dates
---------------------

::

    // Date et heure actuelles
    new Date()

    // Formatage (l'interoperabilite Java utilise la meme notation qu'en Groovy)
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(updated_at)

Contexte d'exécution et objets disponibles
===========================================

Les objets disponibles dans un script dépendent du contexte dans lequel il est exécuté.
Seul ``container`` est disponible dans tous les contextes.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Contexte d'exécution
     - Objets disponibles
     - Description
   * - Tous les contextes
     - ``container``
     - Conteneur DI. Accès aux composants via ``container.getComponent("systemHelper")``
       ou ``container.getComponent("fessConfig")``
   * - Scripts Data Store
     - Variables de champs spécifiques au connecteur
     - Chaque champ récupéré du Data Store est disponible en tant que variable
       (le nom de variable et le préfixe varient selon le connecteur ; CSV/JSON utilisent
       directement le nom du champ comme variable)
   * - Mapping de chemin
     - ``url`` ``matcher``
     - La chaîne URL à transformer et le ``Matcher`` de l'expression régulière
       (uniquement lorsque le remplacement porte le préfixe ``(nom du moteur):`` ; le nom
       indiqué, par exemple ``groovy`` ou ``javascript``, détermine le langage exécuté)
   * - Tâches planifiées
     - ``executor``
     - Instance d'exécution du job (``JobExecutor``). Utilisé pour contrôler l'arrêt du job

.. note::
   Les objets autres que ``container`` ne sont injectés que dans des contextes spécifiques.
   Par exemple, ``executor`` n'est disponible que dans les tâches planifiées et ne l'est pas
   dans les scripts Data Store ni dans le mapping de chemin.

Sécurité
========

.. warning::
   Les scripts disposant de capacités puissantes, utilisez-les uniquement depuis des sources fiables.

- Les scripts sont exécutés sur le serveur
- L'accès au système de fichiers et au réseau est possible
- Assurez-vous que seuls les utilisateurs disposant de droits d'administration peuvent modifier les scripts
- L'exécution des scripts est enregistrée dans le journal d'audit (``audit.log``).
  L'enregistrement est contrôlé par ``script.audit.log.enabled`` (valeur par défaut : ``true``).
  La longueur maximale de la chaîne de script enregistrée est contrôlée par
  ``script.audit.log.max.length`` (valeur par défaut : ``100`` caractères).

Performance
===========

Conseils pour optimiser les performances des scripts :

1. **Éviter les traitements complexes** : les scripts Data Store sont exécutés pour chaque document
2. **Minimiser l'accès aux ressources externes** : les appels réseau sont source de latence
3. **Tirer parti du cache** : envisagez la mise en cache pour les valeurs utilisées de manière répétée

Débogage
========

Dans les scripts de tâches planifiées, l'ensemble du script est évalué comme un seul script,
ce qui permet d'utiliser la sortie de logs pour le débogage.
(Les scripts Data Store évaluent chaque ligne comme une expression unique ; le traitement
multi-lignes n'est pas utilisable.)

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("fess.script");
    logger.info("executor = {}", executor);

L'exemple ci-dessus utilise un logger nommé ``fess.script``.
Pour activer la sortie de ce log, ajoutez la configuration du logger correspondant
dans ``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="fess.script" level="DEBUG"/>

Pour activer les logs de débogage du moteur de script lui-même, configurez le niveau de log
du package ``org.codelibs.fess.script`` à ``DEBUG``.

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

Informations de référence
==========================

- :doc:`scripting-javascript` - Guide du scripting JavaScript
- :doc:`scripting-groovy` - Guide du scripting Groovy (plugin)
- :doc:`scripting-ognl` - Guide des scripts OGNL (plugin)
- :doc:`../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../admin/scheduler-guide` - Guide de configuration du planificateur
