==================================
Apercu du scripting
==================================

Apercu
====

Dans |Fess|, vous pouvez utiliser des scripts pour implementer une logique personnalisee dans diverses situations.
En utilisant des scripts, vous pouvez controler de maniere flexible le traitement des donnees lors du crawl,
la personnalisation des resultats de recherche, l'execution de taches planifiees, etc.

Langages de script pris en charge
==================

|Fess| prend en charge les langages de script suivants :

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Langage
     - Identifiant
     - Description
   * - Groovy
     - ``groovy``
     - Langage de script par defaut. Compatible avec Java et offre des fonctionnalites puissantes
   * - JavaScript
     - ``javascript``
     - Langage familier aux developpeurs web

.. note::
   Groovy est le plus largement utilise, et les exemples de cette documentation sont ecrits en Groovy.

Cas d'utilisation des scripts
====================

Configuration du Data Store
----------------

Dans les connecteurs Data Store, les scripts sont utilises pour mapper les donnees recuperees
aux champs d'index.

::

    url="https://example.com/article/" + data.id
    title=data.name
    content=data.description
    lastModified=data.updated_at

Mapping de chemin
--------------

Les scripts peuvent etre utilises pour la normalisation d'URL et la conversion de chemin.

::

    # Convertir l'URL
    url.replaceAll("http://", "https://")

Taches planifiees
------------------

Dans les taches planifiees, vous pouvez ecrire une logique de traitement personnalisee en script Groovy.

::

    return container.getComponent("crawlJob").execute();

Syntaxe de base
============

Acces aux variables
------------

::

    # Acceder aux donnees du data store
    data.fieldName

    # Acceder aux composants systeme
    container.getComponent("componentName")

Manipulation de chaines
----------

::

    # Concatenation
    title + " - " + category

    # Remplacement
    content.replaceAll("old", "new")

    # Division
    tags.split(",")

Conditions
--------

::

    # Operateur ternaire
    data.status == "active" ? "Actif" : "Inactif"

    # Verification de null
    data.description ?: "Pas de description"

Manipulation de dates
--------

::

    # Date et heure actuelle
    new Date()

    # Formatage
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(data.date)

Objets disponibles
======================

Principaux objets utilisables dans les scripts :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Objet
     - Description
   * - ``data``
     - Donnees recuperees du data store
   * - ``container``
     - Conteneur DI (acces aux composants)
   * - ``systemHelper``
     - Helper systeme
   * - ``fessConfig``
     - Configuration de |Fess|

Securite
============

.. warning::
   Les scripts ont des capacites puissantes, utilisez-les uniquement depuis des sources fiables.

- Les scripts sont executes sur le serveur
- L'acces au systeme de fichiers et au reseau est possible
- Assurez-vous que seuls les utilisateurs avec droits d'administration peuvent modifier les scripts

Performance
==============

Conseils pour optimiser les performances des scripts :

1. **Eviter les traitements complexes** : Les scripts sont executes pour chaque document
2. **Minimiser l'acces aux ressources externes** : Les appels reseau causent des delais
3. **Utiliser le cache** : Envisagez le cache pour les valeurs utilisees de maniere repetee

Debogage
========

Pour le debogage des scripts, utilisez la sortie de logs :

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")
    logger.info("data.id = {}", data.id)

Configuration du niveau de log :

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="script" level="DEBUG"/>

Informations de reference
========

- :doc:`scripting-groovy` - Guide de script Groovy
- :doc:`../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../admin/scheduler-guide` - Guide de configuration du planificateur
