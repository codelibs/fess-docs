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
   * - Groovy
     - ``groovy``
     - Lenguaje de scripting registrado de forma predeterminada. Compatible con Java y proporciona funcionalidades potentes

.. note::
   El único motor de scripting registrado de forma predeterminada en |Fess| es Groovy.
   El lenguaje de scripting por defecto es ``groovy`` ( ``Constants.DEFAULT_SCRIPT`` ).
   Todos los ejemplos de scripts de este documento están escritos en sintaxis Groovy.

Casos de uso del scripting
===========================

Configuración de data store
----------------------------

En los conectores de data store, se usan scripts para mapear los datos obtenidos
a los campos del índice. La configuración se escribe en formato ``nombre_de_campo=expresion``
una línea por entrada, y cada línea se evalúa como una expresión Groovy independiente.

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
   usar bloques ``if`` de varias líneas, sentencias ``import`` ni declaraciones de variables
   con ``def``. Para cambiar un valor según una condición, use el operador ternario por campo
   (por ejemplo: ``title=enabled == "true" ? name : null`` ). Para referenciar clases,
   escriba el nombre completamente cualificado (FQCN) en línea.

Mapeo de rutas
--------------

El mapeo de rutas es una función para normalizar y transformar las URLs a crawlear.
De forma predeterminada, se configura mediante un par de "expresión regular" y "cadena de
reemplazo", y no es un script Groovy. Por ejemplo, si se especifica ``http://`` como
expresión regular y ``https://`` como cadena de reemplazo, se sustituye el esquema de la URL.

Solo cuando la cadena de reemplazo comienza con el prefijo ``groovy:``, la cadena restante
se evalúa como un script Groovy. Dentro de este script, se puede usar ``url`` para la cadena
de URL a transformar y ``matcher`` para el ``java.util.regex.Matcher`` de la expresión regular.

::

    groovy:url.replaceAll("http://", "https://")

Trabajos programados
--------------------

En los trabajos programados, puede escribir lógica de procesamiento personalizada en scripts
Groovy. El script completo se evalúa como un único script Groovy, por lo que es posible
usar múltiples líneas, sentencias ``import`` y declaraciones de variables con ``def``.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Los métodos como ``logLevel("info")`` son métodos de la clase del trabajo ( ``ExecJob`` y sus
subclases) y pueden encadenarse. Consulte "Contexto de ejecución y objetos disponibles" para
obtener información sobre la variable ``executor``.

Sintaxis básica
===============

A continuación se muestran ejemplos de sintaxis básica de Groovy. Los comentarios se escriben
con ``//`` (comentario de línea) o ``/* */`` (comentario de bloque). Tenga en cuenta que los
comentarios que comienzan con ``#`` no son válidos en Groovy.

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

    // Reemplazo
    content.replaceAll("old", "new")

    // Division
    tags.split(",")

Estructuras condicionales
--------------------------

::

    // Operador ternario
    status == "active" ? "Activo" : "Inactivo"

    // Valor por defecto cuando es null o vacio (operador Elvis)
    description ?: "Sin descripcion"

Operaciones de fecha
--------------------

::

    // Fecha y hora actual
    new Date()

    // Formato
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
     - La cadena de URL a transformar y el ``Matcher`` de la expresión regular (solo cuando se usa el prefijo ``groovy:``)
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
3. **Aprovechar la cache**: Considere usar cache para valores que se usan repetidamente

Depuración
==========

En los scripts de trabajos programados, el script completo se evalúa como un único script
Groovy, por lo que puede usar la salida de logs para depurar.
(En los scripts de data store, cada línea se evalúa como una expresión individual, por lo que
no es posible usar sentencias ``import`` ni procesamiento en varias líneas.)

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("fess.script")
    logger.info("executor = {}", executor)

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

- :doc:`scripting-groovy` - Guía de scripting Groovy
- :doc:`../admin/dataconfig-guide` - Guía de configuración de data store
- :doc:`../admin/scheduler-guide` - Guía de configuración del planificador
