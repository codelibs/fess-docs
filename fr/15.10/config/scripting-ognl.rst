======================
Guide des scripts OGNL
======================

Vue d'ensemble
==============

OGNL (Object-Graph Navigation Language) est l'un des moteurs de script disponibles dans |Fess|.
Il est fourni par le plugin ``fess-script-ognl`` et son identifiant est ``ognl``.

Un script OGNL est une expression unique qui produit une valeur, comme
``title + " - " + siteName`` ou ``content.length() > 0``. Il n'y a ni instruction, ni structure
de contrôle, ni ``return``. Utilisez-le pour des expressions courtes, par exemple pour le mappage
de champs, le boost de documents et le mappage de chemins. Pour un script qui nécessite des
instructions ou des boucles, utilisez :doc:`scripting-javascript` ou :doc:`scripting-groovy`.

.. important::
   Le plugin **ne fait pas partie de la distribution**. Installez-le depuis la page
   Système > Plugin de l'interface d'administration, ou avec
   ``bin/fess-setup install plugin fess-script-ognl``. Pour une installation manuelle, placez le
   fichier JAR (par exemple ``fess-script-ognl-15.10.0.jar``) dans ``app/WEB-INF/plugin/`` et
   redémarrez |Fess|.

Sélectionner OGNL
=================

OGNL n'est utilisé que là où son type de script est sélectionné explicitement.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Où
     - Comment sélectionner OGNL
   * - Magasin de données
     - Ajoutez ``script_type=ognl`` aux paramètres de la configuration du magasin de données
   * - Exploration Web et de fichiers
     - Ajoutez ``config.script.type=ognl`` aux paramètres de la configuration et écrivez les
       scripts de champ sous la forme ``field.script.<champ>=<expression>``
   * - Règle de boost de documents
     - Définissez le type de script de la règle sur ``ognl`` (chaque règle a son propre type de
       script)
   * - Mappage de chemins
     - Commencez le remplacement par ``ognl:``. Le résultat de l'expression devient l'URL de
       remplacement ; l'URL d'origine et le ``Matcher`` sont disponibles sous les noms ``url`` et
       ``matcher``
   * - Tâche planifiée
     - Définissez le type de script de la tâche sur ``ognl``. Une tâche est normalement une
       procédure, qu'une expression unique ne peut pas exprimer

Écrire des expressions
======================

Dans les scripts de magasin de données et de champ, écrivez un ``champ=expression`` par ligne.
Chaque paramètre est disponible à la fois sous la forme ``name`` et ``#name``.

::

    title=title
    content=content.trim()
    digest=content.length() > 200 ? content.substring(0, 200) + "..." : content

OGNL n'est pas un sous-ensemble de Groovy. Tenez compte des points suivants lors du portage d'un
script :

- Il n'y a ni ``return``, ni instruction, ni ``if`` / ``for``. Utilisez l'opérateur ternaire
  ``cond ? a : b``.
- L'opérateur Elvis ``?:`` et l'opérateur de navigation sûre ``?.`` ne sont pas pris en charge.
  Écrivez ``a != null ? a.b : null``.
- ``"x${id}"`` n'est pas une erreur et n'est pas interpolé. L'expression vaut la chaîne littérale
  ``x${id}``, et le champ est donc indexé avec un texte erroné. Concaténez plutôt avec ``+``.

Paramètres
==========

Le moteur lit les clés suivantes dans ``system.properties`` ou dans la propriété système JVM
``-Dfess.system.<clé>``. Si une clé figure aux deux endroits, ``system.properties`` l'emporte.
``system.properties`` est ``app/WEB-INF/conf/system.properties`` dans le paquet ZIP et
``/etc/fess/system.properties`` dans les paquets RPM et DEB.

.. important::
   Les clés ne sont lues qu'une seule fois, lorsque le moteur est initialisé au démarrage.
   Après toute modification, redémarrez |Fess| ; le processus en cours ne la prend pas en compte.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Clé
     - Valeur par défaut
     - Description
   * - ``script.ognl.mode``
     - ``compat``
     - ``compat`` ou ``strict``. Voir la section suivante. Toute autre valeur est consignée comme
       avertissement et traitée comme ``compat``
   * - ``script.ognl.allowed.classes``
     - Voir ci-dessous
     - Liste d'autorisation de classes, séparées par des virgules. Utilisée uniquement en mode
       ``strict``
   * - ``script.ognl.denied.packages``
     - Voir ci-dessous
     - Liste de refus de classes déclarantes, séparées par des virgules. Utilisée uniquement en
       mode ``strict``
   * - ``script.ognl.cache.size``
     - ``1000``
     - Nombre maximal d'expressions analysées conservées en cache. Le minimum est ``1``
   * - ``script.ognl.expression.max.length``
     - ``4000``
     - Nombre maximal de caractères d'une expression. Une expression plus longue n'est pas
       évaluée et échoue. Le minimum est ``1``
   * - ``script.ognl.max.log.length``
     - ``200``
     - Nombre maximal de caractères d'une expression écrits dans un message de journal. Le
       minimum est ``3``

Une valeur qui n'est pas un entier est ignorée avec un avertissement et la valeur par défaut est
utilisée. Une valeur inférieure au minimum est relevée au minimum, avec un avertissement.

Les modes compat et strict
==========================

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - ``compat`` (par défaut)
     - ``strict``
   * - Conteneur DI
     - Disponible sous le nom ``container``
     - Non disponible (``container`` vaut ``null``)
   * - Classes
     - ``@n.importe.Classe@methode(...)`` atteint n'importe quelle classe
     - Seules les classes de ``script.ognl.allowed.classes`` sont accessibles
   * - Membres
     - Aucune restriction
     - Les membres déclarés par une classe de ``script.ognl.denied.packages`` ne peuvent pas être
       appelés. Les membres non publics sont toujours refusés

``compat`` conserve le comportement des configurations existantes. En mode ``strict``, une
expression comme ``@java.lang.System@getProperty("user.name")`` ou
``new java.io.File("/etc/hosts")`` est refusée. Une expression refusée ne vaut pas ``null`` : un
avertissement est consigné dans le journal et l'évaluation échoue avec une erreur.

Au démarrage, le moteur consigne le mode effectif au niveau ``INFO``
(``ognl script engine: mode=strict, ...``). Vérifiez cette ligne pour confirmer que ``strict`` a
bien pris effet.

Liste d'autorisation
--------------------

``script.ognl.allowed.classes`` compare soit un nom de classe complet de façon exacte, soit un nom
de paquet ou de classe suivi de ``.``. Par exemple, ``java.time`` autorise
``java.time.LocalDate`` et toutes les classes de ce paquet. La valeur par défaut est :

``java.lang.Math``, ``java.lang.String``, ``java.lang.Boolean``, ``java.lang.Integer``,
``java.lang.Long``, ``java.lang.Float``, ``java.lang.Double``, ``java.lang.Number``,
``java.util.Date``, ``java.util.Arrays``, ``java.util.List``, ``java.util.Map``,
``java.util.Set``, ``java.util.Collections``, ``java.math.BigDecimal``, ``java.time``,
``org.codelibs.core.lang.StringUtil``, ``org.codelibs.fess.util.DocumentUtil``,
``org.codelibs.fess.taglib.FessFunctions``

Le nom d'une classe imbriquée contient ``$`` (par exemple ``java.util.Map$Entry``) et n'est pas
autorisé par le nom de la classe englobante. Ajoutez son nom avec ``$`` à la liste si vous en avez
besoin.

Liste de refus
--------------

``script.ognl.denied.packages`` refuse un membre lorsque le nom de la classe qui le déclare
commence par l'une des entrées. La valeur par défaut est :

``java.io``, ``java.nio``, ``java.net``, ``java.lang.reflect``, ``java.lang.invoke``,
``java.lang.System``, ``java.lang.Class``, ``java.lang.Runtime``, ``java.lang.ProcessBuilder``,
``java.lang.Process``, ``java.lang.Thread``, ``java.lang.ClassLoader``, ``javax.script``,
``jdk.``, ``sun.``, ``org.lastaflute.di``

.. note::
   Une valeur que vous définissez remplace la liste par défaut ; elle ne s'y ajoute pas. Pour
   ajouter une classe à la liste d'autorisation, écrivez les entrées par défaut ainsi que la
   nouvelle entrée.

.. warning::
   Le mode ``strict`` limite les classes et les membres qu'une expression peut atteindre. Il
   n'isole pas l'expression des objets qui lui sont transmis. Si un helper ou une entité de |Fess|
   est passé en paramètre, ses méthodes publiques peuvent être appelées depuis l'expression dans
   les deux modes.
