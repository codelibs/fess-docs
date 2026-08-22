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
   * - Groovy
     - ``groovy``
     - Langage de script enregistre par defaut. Compatible avec Java et offre des fonctionnalites puissantes

.. note::
   Le seul moteur de script enregistre par defaut dans |Fess| est Groovy.
   Le langage de script par defaut est ``groovy`` (``Constants.DEFAULT_SCRIPT``).
   Tous les exemples de scripts de cette documentation sont ecrits en syntaxe Groovy.

Cas d'utilisation des scripts
==============================

Configuration du Data Store
----------------------------

Dans les connecteurs Data Store, des scripts sont utilises pour mapper les donnees recuperees
vers les champs de l'index. La configuration s'ecrit au format ``nom_de_champ=expression``, une par ligne ;
chaque ligne est evaluee comme une expression Groovy independante.

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
   Chaque ligne d'un Data Store etant evaluee comme une expression unique, les blocs ``if`` multi-lignes,
   les instructions ``import`` et les declarations de variables avec ``def`` ne peuvent pas etre utilises.
   Pour conditionner une valeur, utilisez l'operateur ternaire pour chaque champ
   (exemple : ``title=enabled == "true" ? name : null``). Pour referencer une classe, utilisez
   le nom completement qualifie (FQCN) en ligne.

Mapping de chemin
-----------------

Le mapping de chemin est une fonctionnalite permettant de normaliser et de transformer les URL crawlees.
Par defaut, il se configure avec un couple « expression reguliere » / « chaine de remplacement » et
ne constitue pas un script Groovy. Par exemple, en indiquant ``http://`` comme expression reguliere
et ``https://`` comme chaine de remplacement, le schema de l'URL est remplace.

Lorsque la chaine de remplacement commence par ``groovy:``, la partie suivante est evaluee en tant
que script Groovy. Dans ce script, ``url`` represente la chaine URL a transformer et ``matcher``
represente le ``java.util.regex.Matcher`` de l'expression reguliere.

::

    groovy:url.replaceAll("http://", "https://")

Taches planifiees
-----------------

Dans les taches planifiees, vous pouvez ecrire une logique de traitement personnalisee en script Groovy.
L'ensemble du script est evalue comme un seul script Groovy, ce qui permet d'utiliser des instructions
multi-lignes, des instructions ``import`` et des declarations de variables avec ``def``.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Les methodes comme ``logLevel("info")`` sont des methodes de la classe du job (``ExecJob`` et ses
sous-classes) et peuvent etre enchainées. Pour la variable ``executor``, consultez la section
« Contexte d'execution et objets disponibles ».

Syntaxe de base
===============

Voici des exemples de syntaxe Groovy de base. Les commentaires utilisent ``//`` (commentaire de ligne)
ou ``/* */`` (commentaire de bloc). Notez que les commentaires commencant par ``#`` ne sont pas
utilisables en Groovy.

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

    // Remplacement
    content.replaceAll("old", "new")

    // Division
    tags.split(",")

Conditions
----------

::

    // Operateur ternaire
    status == "active" ? "Actif" : "Inactif"

    // Valeur par defaut si null ou vide (operateur Elvis)
    description ?: "Aucune description"

Manipulation de dates
---------------------

::

    // Date et heure actuelles
    new Date()

    // Formatage
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
       (uniquement lors d'un remplacement avec le prefixe ``groovy:``)
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

Dans les scripts de taches planifiees, l'ensemble du script est evalue comme un seul script Groovy,
ce qui permet d'utiliser la sortie de logs pour le debogage.
(Les scripts Data Store evaluent chaque ligne comme une expression unique ; les instructions ``import``
et les traitements multi-lignes ne sont pas utilisables.)

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("fess.script")
    logger.info("executor = {}", executor)

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

- :doc:`scripting-groovy` - Guide du scripting Groovy
- :doc:`../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../admin/scheduler-guide` - Guide de configuration du planificateur
