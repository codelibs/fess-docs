====================
OGNL Scripting Guide
====================

Overview
========

OGNL (Object-Graph Navigation Language) is one of the script engines available in |Fess|.
It is provided by the ``fess-script-ognl`` plugin, and its identifier is ``ognl``.

An OGNL script is a single value expression such as ``title + " - " + siteName`` or
``content.length() > 0``. It has no statements, no control flow and no ``return``. Use it for
short expressions such as field mapping, document boost and path mapping. For a script that
needs statements or loops, use :doc:`scripting-javascript` or :doc:`scripting-groovy`.

.. important::
   The plugin is **not part of the distribution**. Install it from the System > Plugin page in
   the administration screen, or run ``bin/fess-setup install plugin fess-script-ognl``.
   To install manually, place the JAR file (for example, ``fess-script-ognl-15.9.0.jar``) in
   ``app/WEB-INF/plugin/`` and restart |Fess|.

Selecting OGNL
==============

OGNL is used only where its script type is selected explicitly.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Where
     - How to select OGNL
   * - Data store
     - Add ``script_type=ognl`` to the parameters of the data store configuration
   * - Web and file crawling
     - Add ``config.script.type=ognl`` to the configuration parameters, and write the field
       scripts as ``field.script.<field>=<expression>``
   * - Boost document rule
     - Set the script type of the rule to ``ognl`` (each rule has its own script type)
   * - Path mapping
     - Start the replacement with ``ognl:``. The result of the expression becomes the
       replacement URL, and the original URL and the ``Matcher`` are available as ``url``
       and ``matcher``
   * - Scheduled job
     - Set the script type of the job to ``ognl``. A job is normally a procedure, which a
       single expression cannot express

Writing Expressions
===================

In data store and field scripts, write one ``field=expression`` per line. Each parameter is
available both as ``name`` and as ``#name``.

::

    title=title
    content=content.trim()
    digest=content.length() > 200 ? content.substring(0, 200) + "..." : content

OGNL is not a subset of Groovy. Note the following when porting a script:

- There is no ``return``, no statement and no ``if`` / ``for``. Use the ternary operator
  ``cond ? a : b``.
- The Elvis operator ``?:`` and the safe navigation operator ``?.`` are not supported. Write
  ``a != null ? a.b : null``.
- ``"x${id}"`` is not an error and is not interpolated. It evaluates to the literal string
  ``x${id}``, so the field is indexed with the wrong text. Concatenate with ``+`` instead.

Settings
========

The engine reads the following keys from ``system.properties``, or from the JVM system
property ``-Dfess.system.<key>``. If a key is in both, ``system.properties`` wins.
``system.properties`` is ``app/WEB-INF/conf/system.properties`` in the ZIP package and
``/etc/fess/system.properties`` in the RPM and DEB packages.

.. important::
   The keys are read only once, when the engine is initialized at startup. After changing any of
   them, restart |Fess|; the running process does not pick up the change.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Key
     - Default
     - Description
   * - ``script.ognl.mode``
     - ``compat``
     - ``compat`` or ``strict``. See the next section. Any other value is logged as a
       warning and treated as ``compat``
   * - ``script.ognl.allowed.classes``
     - See below
     - Comma-separated class allow list. Used only in ``strict`` mode
   * - ``script.ognl.denied.packages``
     - See below
     - Comma-separated deny list of declaring classes. Used only in ``strict`` mode
   * - ``script.ognl.cache.size``
     - ``1000``
     - Maximum number of parsed expressions that are cached. The minimum is ``1``
   * - ``script.ognl.expression.max.length``
     - ``4000``
     - Maximum number of characters in an expression. A longer expression is not evaluated and
       fails. The minimum is ``1``
   * - ``script.ognl.max.log.length``
     - ``200``
     - Maximum number of characters of an expression that is written to a log message. The
       minimum is ``3``

A value that is not an integer is ignored with a warning and the default is used. A value below
the minimum is raised to the minimum with a warning.

compat and strict Modes
=======================

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - ``compat`` (default)
     - ``strict``
   * - DI container
     - Available as ``container``
     - Not available (``container`` evaluates to ``null``)
   * - Classes
     - ``@any.Class@method(...)`` can reach any class
     - Only classes in ``script.ognl.allowed.classes`` can be reached
   * - Members
     - No restriction
     - Members declared by a class in ``script.ognl.denied.packages`` cannot be called. Members
       that are not public are always refused

``compat`` keeps the behavior of existing configurations. In ``strict`` mode an expression such
as ``@java.lang.System@getProperty("user.name")`` or ``new java.io.File("/etc/hosts")`` is
refused. A refused expression is not evaluated to ``null``. A warning is written to the log and
the evaluation fails with an error.

When the engine starts, it logs the mode in effect at ``INFO`` level
(``ognl script engine: mode=strict, ...``). Check this line to confirm that ``strict`` took
effect.

Allow list
----------

``script.ognl.allowed.classes`` matches a fully qualified class name exactly, or a package or
class name followed by ``.``. For example, ``java.time`` allows ``java.time.LocalDate`` and every
class under that package. The default is:

``java.lang.Math``, ``java.lang.String``, ``java.lang.Boolean``, ``java.lang.Integer``,
``java.lang.Long``, ``java.lang.Float``, ``java.lang.Double``, ``java.lang.Number``,
``java.util.Date``, ``java.util.Arrays``, ``java.util.List``, ``java.util.Map``,
``java.util.Set``, ``java.util.Collections``, ``java.math.BigDecimal``, ``java.time``,
``org.codelibs.core.lang.StringUtil``, ``org.codelibs.fess.util.DocumentUtil``,
``org.codelibs.fess.taglib.FessFunctions``

A nested class has ``$`` in its name (for example, ``java.util.Map$Entry``) and is not allowed by
the name of the enclosing class. Add its name with ``$`` to the list if you need it.

Deny list
---------

``script.ognl.denied.packages`` denies a member when the name of the class that declares it
starts with one of the entries. The default is:

``java.io``, ``java.nio``, ``java.net``, ``java.lang.reflect``, ``java.lang.invoke``,
``java.lang.System``, ``java.lang.Class``, ``java.lang.Runtime``, ``java.lang.ProcessBuilder``,
``java.lang.Process``, ``java.lang.Thread``, ``java.lang.ClassLoader``, ``javax.script``,
``jdk.``, ``sun.``, ``org.lastaflute.di``

.. note::
   A value that you set replaces the default list; it is not added to it. To add one class to the
   allow list, write the default entries together with the new one.

.. warning::
   ``strict`` mode limits which classes and members an expression can reach. It does not isolate
   the expression from the objects it is given. If a |Fess| helper or an entity is passed as a
   parameter, its public methods can be called from the expression in both modes.
