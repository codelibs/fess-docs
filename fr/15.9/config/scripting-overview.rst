====================================
Apercu du scripting
====================================

Apercu
======

Dans |Fess|, vous pouvez utiliser des scripts pour implementer une logique personnalisee dans diverses situations.
En tirant parti des scripts, vous pouvez controler de maniere flexible le traitement des donnees lors du crawl,
la transformation des URL et l'execution des taches planifiees.

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
     - Le langage de script integre par defaut dans |Fess|, et egalement le langage de
       script par defaut ( ``Constants.DEFAULT_SCRIPT`` ). Il s'execute sur Sai (un fork
       de Nashorn developpe par CodeLibs, deja utilise par |Fess| pour les expressions de
       ses XML de DI) ; les scripts sont executes en tant qu'ECMAScript 6.
   * - Groovy
     - ``groovy``
     - Fourni sous forme de plugin ``fess-script-groovy``. En 15.9, il est inclus dans la
       distribution et fonctionne donc sans etape supplementaire, mais **a partir de la
       15.10, il ne sera plus inclus** et devra etre installe depuis l'ecran
       d'administration.

.. note::
   Une configuration de script sans type de script enregistre est traitee comme du
   Groovy. Il ne s'agit pas d'une mesure de transition temporaire mais d'un comportement
   permanent : une configuration creee avant la 15.9 conserve son script en syntaxe
   Groovy sans type de script enregistre, et c'est precisement ce comportement par defaut
   qui lui permet de continuer a fonctionner sans changement apres une mise a niveau.
   Une configuration creee a partir de la 15.9 a son type de script explicitement
   enregistre comme ``javascript``.

   Sauf indication contraire, les exemples de scripts de cette documentation sont ecrits
   en syntaxe JavaScript. Pour la syntaxe Groovy, consultez :doc:`scripting-groovy`.

Cas d'utilisation des scripts
==============================

Configuration du Data Store
----------------------------

Dans les connecteurs Data Store, des scripts sont utilises pour mapper les donnees recuperees
vers les champs de l'index. La configuration s'ecrit au format ``nom_de_champ=expression``, une par ligne ;
chaque ligne est evaluee comme une expression de script independante (JavaScript par defaut).

::

    url=site_url
    title=name
    content=description
    last_modified=updated_at

Les noms de variables disponibles dans les scripts Data Store varient selon le type de connecteur.
Par exemple, pour les Data Stores CSV et JSON, chaque nom de colonne ou de champ est disponible
directement en tant que variable (sans prefixe commun tel que ``data``).
Pour les connecteurs de type fichier (Box, Google Drive, OneDrive, etc.), le prefixe est ``file.*`` ;
pour Slack, c'est ``message.*`` ; le prefixe differe selon le connecteur.
Consultez la documentation de chaque connecteur Data Store pour connaitre les variables disponibles.

.. note::
   Chaque ligne d'un Data Store etant evaluee comme une expression unique, les blocs ``if`` multi-lignes
   ainsi que les declarations de variables telles que ``let`` / ``const`` ne peuvent pas etre utilises.
   Pour conditionner une valeur, utilisez l'operateur ternaire pour chaque champ
   (exemple : ``title=enabled === "true" ? name : null``). Pour referencer une classe, utilisez
   le nom completement qualifie (FQCN) en ligne.

Mapping de chemin
-----------------

Le mapping de chemin est une fonctionnalite permettant de normaliser et de transformer les URL crawlees.
Par defaut, il se configure avec un couple « expression reguliere » / « chaine de remplacement » et
ne constitue pas un script. Par exemple, en indiquant ``http://`` comme expression reguliere
et ``https://`` comme chaine de remplacement, le schema de l'URL est remplace.

Lorsque la chaine de remplacement commence par ``(nom du moteur):``, la partie avant les
deux-points est lue comme le nom d'un moteur de script ; si elle correspond a un moteur
enregistre, le reste de la chaine est evalue en tant que script par ce moteur. Par
exemple, ``groovy:`` selectionne le moteur Groovy (necessite le plugin
``fess-script-groovy``), et ``javascript:`` (alias ``js:``, ``sai:``) selectionne le
moteur JavaScript. Si la partie avant les deux-points ne correspond a aucun moteur
enregistre — ``https://`` dans une chaine de remplacement ordinaire, par exemple —,
la chaine entiere n'est pas traitee comme un script et est utilisee telle quelle comme
simple chaine de remplacement d'expression reguliere. Lorsque la chaine est evaluee en
tant que script, ``url`` represente la chaine URL a transformer et ``matcher``
represente le ``java.util.regex.Matcher`` de l'expression reguliere.

::

    javascript:url.replace(/http:\/\//g, "https://")

Taches planifiees
-----------------

Dans les taches planifiees, vous pouvez ecrire une logique de traitement personnalisee dans un
script. L'ensemble du script est evalue comme un seul script, ce qui permet d'utiliser des
instructions multi-lignes, y compris, en JavaScript, des declarations de variables
``let`` / ``const`` et des structures de controle.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Une instruction ``return`` de niveau superieur est normalement une erreur de syntaxe en
JavaScript. Le moteur de script de |Fess| essaie d'abord de compiler le script en tant
qu'expression, et ne le recompile en bloc d'instructions que si cela echoue. Cet exemple ne
peut pas etre compile en tant qu'expression ; il est donc compile en bloc d'instructions et
s'execute tel quel. Voir :doc:`scripting-javascript` pour plus de details.

Les methodes comme ``logLevel("info")`` sont des methodes de la classe du job (``ExecJob`` et ses
sous-classes) et peuvent etre enchainées. Pour la variable ``executor``, consultez la section
« Contexte d'execution et objets disponibles ».

Syntaxe de base
===============

Voici des exemples de syntaxe JavaScript de base. Les commentaires utilisent ``//`` (commentaire de ligne)
ou ``/* */`` (commentaire de bloc). Notez que les commentaires commencant par ``#`` ne sont pas non plus
utilisables en JavaScript.

Acces aux variables
-------------------

::

    // Champ d'un Data Store (CSV/JSON : acces par nom de colonne ou de champ)
    title

    // Recuperer un composant depuis le conteneur DI
    container.getComponent("systemHelper")

Manipulation de chaines
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

Contexte d'execution et objets disponibles
===========================================

Les objets disponibles dans un script dependent du contexte dans lequel il est execute.
Seul ``container`` est disponible dans tous les contextes.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Contexte d'execution
     - Objets disponibles
     - Description
   * - Tous les contextes
     - ``container``
     - Conteneur DI. Acces aux composants via ``container.getComponent("systemHelper")``
       ou ``container.getComponent("fessConfig")``
   * - Scripts Data Store
     - Variables de champs specifiques au connecteur
     - Chaque champ recupere du Data Store est disponible en tant que variable
       (le nom de variable et le prefixe varient selon le connecteur ; CSV/JSON utilisent
       directement le nom du champ comme variable)
   * - Mapping de chemin
     - ``url`` ``matcher``
     - La chaine URL a transformer et le ``Matcher`` de l'expression reguliere
       (uniquement lorsque le remplacement porte le prefixe ``(nom du moteur):`` ; le nom
       indique, par exemple ``groovy`` ou ``javascript``, determine le langage execute)
   * - Taches planifiees
     - ``executor``
     - Instance d'execution du job (``JobExecutor``). Utilise pour controler l'arret du job

.. note::
   Les objets autres que ``container`` ne sont injectes que dans des contextes specifiques.
   Par exemple, ``executor`` n'est disponible que dans les taches planifiees et ne l'est pas
   dans les scripts Data Store ni dans le mapping de chemin.

Securite
========

.. warning::
   Les scripts disposant de capacites puissantes, utilisez-les uniquement depuis des sources fiables.

- Les scripts sont executes sur le serveur
- L'acces au systeme de fichiers et au reseau est possible
- Assurez-vous que seuls les utilisateurs disposant de droits d'administration peuvent modifier les scripts
- L'execution des scripts est enregistree dans le journal d'audit (``audit.log``).
  L'enregistrement est controle par ``script.audit.log.enabled`` (valeur par defaut : ``true``).
  La longueur maximale de la chaine de script enregistree est controlee par
  ``script.audit.log.max.length`` (valeur par defaut : ``100`` caracteres).

Performance
===========

Conseils pour optimiser les performances des scripts :

1. **Eviter les traitements complexes** : les scripts Data Store sont executes pour chaque document
2. **Minimiser l'acces aux ressources externes** : les appels reseau sont source de latence
3. **Tirer parti du cache** : envisagez la mise en cache pour les valeurs utilisees de maniere repetee

Debogage
========

Dans les scripts de taches planifiees, l'ensemble du script est evalue comme un seul script,
ce qui permet d'utiliser la sortie de logs pour le debogage.
(Les scripts Data Store evaluent chaque ligne comme une expression unique ; le traitement
multi-lignes n'est pas utilisable.)

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("fess.script");
    logger.info("executor = {}", executor);

L'exemple ci-dessus utilise un logger nomme ``fess.script``.
Pour activer la sortie de ce log, ajoutez la configuration du logger correspondant
dans ``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="fess.script" level="DEBUG"/>

Pour activer les logs de debogage du moteur de script lui-meme, configurez le niveau de log
du package ``org.codelibs.fess.script`` a ``DEBUG``.

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

Informations de reference
==========================

- :doc:`scripting-javascript` - Guide du scripting JavaScript
- :doc:`scripting-groovy` - Guide du scripting Groovy (plugin)
- :doc:`../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../admin/scheduler-guide` - Guide de configuration du planificateur
