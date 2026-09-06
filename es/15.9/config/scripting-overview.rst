=======================================
Descripción general del scripting
=======================================

Descripción general
===================

En |Fess|, puede implementar lógica personalizada usando scripts en diversos escenarios.
Al aprovechar los scripts, puede controlar de manera flexible el procesamiento de datos
durante el crawl, la transformación de URLs y la ejecución de trabajos programados.

Lenguajes de scripting compatibles
===================================

|Fess| soporta los siguientes lenguajes de scripting:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Lenguaje
     - Identificador
     - Descripción
   * - JavaScript
     - ``javascript`` (alias: ``js`` , ``sai`` )
     - El lenguaje de scripting integrado en |Fess| de forma predeterminada, y también el
       lenguaje de scripting por defecto ( ``Constants.DEFAULT_SCRIPT`` ). Se ejecuta sobre
       Sai (un fork de Nashorn desarrollado por CodeLibs, que |Fess| ya utiliza para las
       expresiones de sus XML de DI); los scripts se ejecutan como ECMAScript 6.
   * - Groovy
     - ``groovy``
     - Se proporciona como el plugin ``fess-script-groovy``. En 15.9 viene incluido en la
       distribución, por lo que funciona sin pasos adicionales, pero **a partir de 15.10
       dejará de venir incluido** y deberá instalarse desde la pantalla de administración.

.. note::
   Una configuración de script que no tiene registrado un tipo de script se trata como
   Groovy. Esto no es una medida de transición temporal, sino un comportamiento
   permanente: una configuración creada antes de 15.9 conserva su script en sintaxis
   Groovy sin tipo de script registrado, y este valor predeterminado es precisamente lo
   que hace que siga funcionando sin cambios tras la actualización. Una configuración
   creada a partir de 15.9 tiene registrado explícitamente el tipo de script
   ``javascript``.

   Salvo que se indique lo contrario, los ejemplos de scripts de este documento están
   escritos en sintaxis JavaScript. Para la sintaxis de Groovy, consulte
   :doc:`scripting-groovy`.

Casos de uso del scripting
===========================

Configuración de data store
----------------------------

En los conectores de data store, se usan scripts para mapear los datos obtenidos
a los campos del índice. La configuración se escribe en formato ``nombre_de_campo=expresion``
una línea por entrada, y cada línea se evalúa como una expresión de script independiente
(JavaScript de forma predeterminada).

::

    url=site_url
    title=name
    content=description
    last_modified=updated_at

Los nombres de variables disponibles en los scripts de data store varían según el tipo de conector.
Por ejemplo, en el data store CSV y en el data store JSON, cada nombre de columna o campo
puede usarse directamente como variable (sin prefijo común como ``data``).
En los conectores de tipo archivo (Box, Google Drive, OneDrive, etc.) se usa el prefijo ``file.*``,
en Slack se usa ``message.*``, y cada conector tiene su propio prefijo.
Consulte la documentación de cada conector de data store para conocer las variables disponibles.

.. note::
   Cada línea de un data store se evalúa como una expresión única, por lo que no es posible
   usar bloques ``if`` de varias líneas ni sentencias de declaración de variables como
   ``let`` / ``const``. Para cambiar un valor según una condición, use el operador ternario por campo
   (por ejemplo: ``title=enabled === "true" ? name : null`` ). Para referenciar clases,
   escriba el nombre completamente cualificado (FQCN) en línea.

Mapeo de rutas
--------------

El mapeo de rutas es una función para normalizar y transformar las URLs a crawlear.
De forma predeterminada, se configura mediante un par de "expresión regular" y "cadena de
reemplazo", y no es un script. Por ejemplo, si se especifica ``http://`` como
expresión regular y ``https://`` como cadena de reemplazo, se sustituye el esquema de la URL.

Cuando la cadena de reemplazo comienza con ``(nombre_de_motor):``, la parte anterior a
los dos puntos se interpreta como el nombre de un motor de scripting; si coincide con
un motor registrado, el resto de la cadena se evalúa como un script mediante ese motor.
Por ejemplo, ``groovy:`` selecciona el motor Groovy (requiere el plugin
``fess-script-groovy``), y ``javascript:`` (alias ``js:``, ``sai:``) selecciona el motor
JavaScript. Si la parte anterior a los dos puntos no coincide con ningún motor
registrado —por ejemplo, ``https://`` en una cadena de reemplazo normal—, la cadena
completa no se trata como un script, sino que se usa tal cual como una cadena de
reemplazo de expresión regular. Cuando la cadena se evalúa como un script, dentro de
ella se puede usar ``url`` para la cadena de URL a transformar y ``matcher`` para el
``java.util.regex.Matcher`` de la expresión regular.

::

    javascript:url.replace(/http:\/\//g, "https://")

Trabajos programados
--------------------

En los trabajos programados, puede escribir lógica de procesamiento personalizada en un
script. El script completo se evalúa como un único script, por lo que es posible usar
sentencias de varias líneas, incluidas —en JavaScript— declaraciones de variables
``let`` / ``const`` y estructuras de control.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Una sentencia ``return`` de nivel superior normalmente es un error de sintaxis en
JavaScript. El motor de scripting de |Fess| primero intenta compilar el script como una
expresión, y solo recurre a compilarlo como un bloque de sentencias cuando eso falla.
Este ejemplo no se puede compilar como expresión, por lo que se compila como un bloque
de sentencias y se ejecuta tal como se muestra. Consulte :doc:`scripting-javascript`
para más detalles.

Los métodos como ``logLevel("info")`` son métodos de la clase del trabajo ( ``ExecJob`` y sus
subclases) y pueden encadenarse. Consulte "Contexto de ejecución y objetos disponibles" para
obtener información sobre la variable ``executor``.

Sintaxis básica
===============

A continuación se muestran ejemplos de sintaxis básica de JavaScript. Los comentarios se
escriben con ``//`` (comentario de línea) o ``/* */`` (comentario de bloque). Tenga en
cuenta que los comentarios que comienzan con ``#`` tampoco son válidos en JavaScript.

Acceso a variables
------------------

::

    // Campo del data store (en CSV/JSON, se accede por nombre de columna o campo)
    title

    // Obtener un componente del contenedor DI
    container.getComponent("systemHelper")

Operaciones de cadenas
----------------------

::

    // Concatenacion
    title + " - " + category

    // Reemplazo (con expresion regular; ECMAScript 6 no tiene String#replaceAll)
    content.replace(/old/g, "new")

    // Division
    tags.split(",")

Estructuras condicionales
--------------------------

::

    // Operador ternario
    status === "active" ? "Activo" : "Inactivo"

    // Valor por defecto cuando es null o vacio (operador OR logico; JavaScript no tiene operador Elvis)
    description || "Sin descripcion"

Operaciones de fecha
--------------------

::

    // Fecha y hora actual
    new Date()

    // Formato (la interoperabilidad con Java usa la misma notacion que Groovy)
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(updated_at)

Contexto de ejecución y objetos disponibles
============================================

Los objetos disponibles dentro de un script varían según el contexto en que se ejecuta.
Solo ``container`` está disponible en todos los contextos.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Contexto de ejecución
     - Objetos disponibles
     - Descripción
   * - Todos los contextos
     - ``container``
     - Contenedor DI. Acceso a componentes mediante
       ``container.getComponent("systemHelper")`` o
       ``container.getComponent("fessConfig")``
   * - Script de data store
     - Variables de campo específicas del conector
     - Cada campo obtenido del data store está disponible como variable
       (los nombres de variable y prefijos varían según el conector; en CSV/JSON el nombre del campo se usa directamente como variable)
   * - Mapeo de rutas
     - ``url`` ``matcher``
     - La cadena de URL a transformar y el ``Matcher`` de la expresión regular (solo cuando el reemplazo lleva el prefijo ``(nombre_de_motor):``; el nombre indicado, por ejemplo ``groovy`` o ``javascript``, determina el lenguaje ejecutado)
   * - Trabajos programados
     - ``executor``
     - Instancia de ejecución del trabajo ( ``JobExecutor`` ). Se usa para controlar el apagado del trabajo

.. note::
   Los objetos distintos de ``container`` solo se inyectan en contextos específicos.
   Por ejemplo, ``executor`` solo está disponible en trabajos programados y no puede
   usarse en scripts de data store ni en mapeo de rutas.

Seguridad
=========

.. warning::
   Los scripts tienen funcionalidades muy potentes; úselos únicamente desde fuentes de confianza.

- Los scripts se ejecutan en el servidor
- Es posible acceder al sistema de archivos y a la red
- Asegúrese de que solo los usuarios con privilegios de administrador puedan editar scripts
- La ejecución de scripts se registra en el log de auditoría ( ``audit.log`` ).
  El registro puede controlarse con ``script.audit.log.enabled`` y está activado por defecto ( ``true`` ).
  La longitud máxima de la cadena de script registrada se controla con ``script.audit.log.max.length``
  y el valor por defecto es ``100`` caracteres.

Rendimiento
===========

Consejos para optimizar el rendimiento de los scripts:

1. **Evitar procesamiento complejo**: Los scripts de data store se ejecutan por cada documento
2. **Minimizar el acceso a recursos externos**: Las llamadas de red son una fuente de latencia
3. **Aprovechar la caché**: Considere usar caché para valores que se usan repetidamente

Depuración
==========

En los scripts de trabajos programados, el script completo se evalúa como un único
script, por lo que puede usar la salida de logs para depurar.
(En los scripts de data store, cada línea se evalúa como una expresión individual, por lo que
no es posible usar procesamiento en varias líneas.)

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("fess.script");
    logger.info("executor = {}", executor);

El ejemplo anterior usa un logger denominado ``fess.script``.
Para que este log se emita, agregue la configuración del logger correspondiente
en ``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="fess.script" level="DEBUG"/>

Además, para activar los logs de depuración del propio motor de scripting, establezca
el nivel de log del paquete ``org.codelibs.fess.script`` en ``DEBUG``.

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

Información de referencia
==========================

- :doc:`scripting-javascript` - Guía de scripting JavaScript
- :doc:`scripting-groovy` - Guía de scripting Groovy (plugin)
- :doc:`../admin/dataconfig-guide` - Guía de configuración de data store
- :doc:`../admin/scheduler-guide` - Guía de configuración del planificador
