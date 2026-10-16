======================
Guía de scripting OGNL
======================

Descripción general
===================

OGNL (Object-Graph Navigation Language) es uno de los motores de script disponibles en |Fess|.
Lo proporciona el plugin ``fess-script-ognl`` y su identificador es ``ognl``.

Un script OGNL es una única expresión que produce un valor, como ``title + " - " + siteName`` o
``content.length() > 0``. No tiene sentencias, estructuras de control ni ``return``. Úselo para
expresiones cortas, por ejemplo en el mapeo de campos, el refuerzo (boost) de documentos y el
mapeo de rutas. Para un script que necesite sentencias o bucles, use
:doc:`scripting-javascript` o :doc:`scripting-groovy`.

.. important::
   El plugin **no forma parte de la distribución**. Instálelo desde la página
   **Sistema > Plugin** de la pantalla de administración o con
   ``bin/fess-setup install plugin fess-script-ognl``. Para instalarlo manualmente, coloque el
   archivo JAR (por ejemplo, ``fess-script-ognl-15.10.0.jar``) en ``app/WEB-INF/plugin/`` y
   reinicie |Fess|.

Selección de OGNL
=================

OGNL solo se usa donde su tipo de script se selecciona de forma explícita.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Dónde
     - Cómo seleccionar OGNL
   * - Data store
     - Añada ``script_type=ognl`` a los parámetros de la configuración del data store
   * - Rastreo web y de archivos
     - Añada ``config.script.type=ognl`` a los parámetros de la configuración y escriba los
       scripts de campo como ``field.script.<campo>=<expresión>``
   * - Regla de refuerzo de documentos
     - Establezca el tipo de script de la regla en ``ognl`` (cada regla tiene su propio tipo de
       script)
   * - Mapeo de rutas
     - Comience el reemplazo con ``ognl:``. El resultado de la expresión pasa a ser la URL de
       reemplazo, y la URL original y el ``Matcher`` están disponibles como ``url`` y
       ``matcher``
   * - Trabajo programado
     - Establezca el tipo de script del trabajo en ``ognl``. Un trabajo suele ser un
       procedimiento, que una única expresión no puede expresar

Cómo escribir expresiones
=========================

En los scripts de data store y de campo, escriba un ``campo=expresión`` por línea. Cada parámetro
está disponible tanto como ``name`` como ``#name``.

::

    title=title
    content=content.trim()
    digest=content.length() > 200 ? content.substring(0, 200) + "..." : content

OGNL no es un subconjunto de Groovy. Tenga en cuenta lo siguiente al portar un script:

- No hay ``return``, ni sentencias, ni ``if`` / ``for``. Use el operador ternario
  ``cond ? a : b``.
- El operador Elvis ``?:`` y el operador de navegación segura ``?.`` no son compatibles. Escriba
  ``a != null ? a.b : null``.
- ``"x${id}"`` no es un error y no se interpola. Se evalúa como la cadena literal ``x${id}``, por
  lo que el campo se indexa con un texto incorrecto. Concatene con ``+`` en su lugar.

Configuración
=============

El motor lee las siguientes claves de ``system.properties`` o de la propiedad de sistema de la
JVM ``-Dfess.system.<clave>``. Si una clave está en ambos sitios, prevalece ``system.properties``.
``system.properties`` es ``app/WEB-INF/conf/system.properties`` en el paquete ZIP y
``/etc/fess/system.properties`` en los paquetes RPM y DEB.

.. important::
   Las claves se leen solo una vez, cuando el motor se inicializa al arrancar. Tras cambiar
   cualquiera de ellas, reinicie |Fess|; el proceso en ejecución no recoge el cambio.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Clave
     - Valor predeterminado
     - Descripción
   * - ``script.ognl.mode``
     - ``compat``
     - ``compat`` o ``strict``. Consulte la sección siguiente. Cualquier otro valor se registra
       como advertencia y se trata como ``compat``
   * - ``script.ognl.allowed.classes``
     - Véase más abajo
     - Lista de clases permitidas, separadas por comas. Solo se usa en modo ``strict``
   * - ``script.ognl.denied.packages``
     - Véase más abajo
     - Lista de clases declarantes denegadas, separadas por comas. Solo se usa en modo ``strict``
   * - ``script.ognl.cache.size``
     - ``1000``
     - Número máximo de expresiones analizadas que se guardan en caché. El mínimo es ``1``
   * - ``script.ognl.expression.max.length``
     - ``4000``
     - Número máximo de caracteres de una expresión. Una expresión más larga no se evalúa y
       falla. El mínimo es ``1``
   * - ``script.ognl.max.log.length``
     - ``200``
     - Número máximo de caracteres de una expresión que se escriben en un mensaje de registro. El
       mínimo es ``3``

Un valor que no es un entero se ignora con una advertencia y se usa el valor predeterminado. Un
valor inferior al mínimo se eleva al mínimo, también con una advertencia.

Los modos compat y strict
=========================

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - ``compat`` (predeterminado)
     - ``strict``
   * - Contenedor DI
     - Disponible como ``container``
     - No disponible (``container`` se evalúa como ``null``)
   * - Clases
     - ``@cualquier.Clase@metodo(...)`` alcanza cualquier clase
     - Solo se pueden alcanzar las clases de ``script.ognl.allowed.classes``
   * - Miembros
     - Sin restricción
     - No se pueden llamar los miembros declarados por una clase de
       ``script.ognl.denied.packages``. Los miembros que no son públicos siempre se rechazan

``compat`` mantiene el comportamiento de las configuraciones existentes. En modo ``strict``, una
expresión como ``@java.lang.System@getProperty("user.name")`` o
``new java.io.File("/etc/hosts")`` se rechaza. Una expresión rechazada no se evalúa como
``null``: se escribe una advertencia en el registro y la evaluación falla con un error.

Al arrancar, el motor registra el modo vigente en el nivel ``INFO``
(``ognl script engine: mode=strict, ...``). Compruebe esta línea para confirmar que ``strict``
ha surtido efecto.

Lista de permitidos
-------------------

``script.ognl.allowed.classes`` compara un nombre de clase completo de forma exacta, o un nombre
de paquete o de clase seguido de ``.``. Por ejemplo, ``java.time`` permite
``java.time.LocalDate`` y todas las clases de ese paquete. El valor predeterminado es:

``java.lang.Math``, ``java.lang.String``, ``java.lang.Boolean``, ``java.lang.Integer``,
``java.lang.Long``, ``java.lang.Float``, ``java.lang.Double``, ``java.lang.Number``,
``java.util.Date``, ``java.util.Arrays``, ``java.util.List``, ``java.util.Map``,
``java.util.Set``, ``java.util.Collections``, ``java.math.BigDecimal``, ``java.time``,
``org.codelibs.core.lang.StringUtil``, ``org.codelibs.fess.util.DocumentUtil``,
``org.codelibs.fess.taglib.FessFunctions``

El nombre de una clase anidada contiene ``$`` (por ejemplo, ``java.util.Map$Entry``) y no queda
permitido por el nombre de la clase que la contiene. Añada su nombre con ``$`` a la lista si la
necesita.

Lista de denegados
------------------

``script.ognl.denied.packages`` deniega un miembro cuando el nombre de la clase que lo declara
empieza por alguna de las entradas. El valor predeterminado es:

``java.io``, ``java.nio``, ``java.net``, ``java.lang.reflect``, ``java.lang.invoke``,
``java.lang.System``, ``java.lang.Class``, ``java.lang.Runtime``, ``java.lang.ProcessBuilder``,
``java.lang.Process``, ``java.lang.Thread``, ``java.lang.ClassLoader``, ``javax.script``,
``jdk.``, ``sun.``, ``org.lastaflute.di``

.. note::
   Un valor que usted establece sustituye a la lista predeterminada; no se añade a ella. Para
   añadir una clase a la lista de permitidos, escriba las entradas predeterminadas junto con la
   nueva.

.. warning::
   El modo ``strict`` limita las clases y los miembros que una expresión puede alcanzar. No aísla
   la expresión de los objetos que recibe. Si se pasa como parámetro un helper o una entidad de
   |Fess|, sus métodos públicos se pueden llamar desde la expresión en ambos modos.
