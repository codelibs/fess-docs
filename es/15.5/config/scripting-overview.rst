==================================
Descripcion general de scripting
==================================

Descripcion general
===================

En |Fess|, puede implementar logica personalizada usando scripts en varios escenarios.
Al aprovechar los scripts, puede controlar de manera flexible el procesamiento de datos durante el crawl,
la personalizacion de resultados de busqueda y la ejecucion de trabajos programados.

Lenguajes de scripting compatibles
==================================

|Fess| soporta los siguientes lenguajes de scripting:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Lenguaje
     - Identificador
     - Descripcion
   * - Groovy
     - ``groovy``
     - Lenguaje de scripting predeterminado. Compatible con Java y proporciona funcionalidades potentes
   * - JavaScript
     - ``javascript``
     - Lenguaje familiar para desarrolladores web

.. note::
   Groovy es el mas ampliamente utilizado, y los ejemplos en esta documentacion estan escritos en Groovy.

Casos de uso de scripting
=========================

Configuracion de Data Store
---------------------------

En los conectores de data store, se usan scripts para mapear los datos obtenidos
a los campos del indice.

::

    url="https://example.com/article/" + data.id
    title=data.name
    content=data.description
    lastModified=data.updated_at

Mapeo de rutas
--------------

Puede usar scripts para normalizar URLs o transformar rutas.

::

    # Transformar URL
    url.replaceAll("http://", "https://")

Trabajos programados
--------------------

En los trabajos programados, puede escribir logica de procesamiento personalizada en scripts Groovy.

::

    return container.getComponent("crawlJob").execute();

Sintaxis basica
===============

Acceso a variables
------------------

::

    # Acceder a datos del data store
    data.fieldName

    # Acceder a componentes del sistema
    container.getComponent("componentName")

Operaciones de cadenas
----------------------

::

    # Concatenacion
    title + " - " + category

    # Reemplazo
    content.replaceAll("old", "new")

    # Division
    tags.split(",")

Estructuras condicionales
-------------------------

::

    # Operador ternario
    data.status == "active" ? "Activo" : "Inactivo"

    # Verificacion de null
    data.description ?: "Sin descripcion"

Operaciones de fecha
--------------------

::

    # Fecha actual
    new Date()

    # Formato
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(data.date)

Objetos disponibles
===================

Principales objetos disponibles dentro de los scripts:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Objeto
     - Descripcion
   * - ``data``
     - Datos obtenidos del data store
   * - ``container``
     - Contenedor DI (acceso a componentes)
   * - ``systemHelper``
     - Helper del sistema
   * - ``fessConfig``
     - Configuracion de |Fess|

Seguridad
=========

.. warning::
   Los scripts tienen funcionalidades poderosas, por lo que solo uselos de fuentes confiables.

- Los scripts se ejecutan en el servidor
- Es posible el acceso al sistema de archivos y la red
- Asegurese de que solo los usuarios con privilegios de administrador puedan editar scripts

Rendimiento
===========

Consejos para optimizar el rendimiento de los scripts:

1. **Evitar procesamiento complejo**: Los scripts se ejecutan para cada documento
2. **Minimizar acceso a recursos externos**: Las llamadas de red causan latencia
3. **Usar cache**: Considere cache para valores usados repetidamente

Depuracion
==========

Para depurar scripts, use la salida de logs:

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")
    logger.info("data.id = {}", data.id)

Configuracion del nivel de log:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="script" level="DEBUG"/>

Informacion de referencia
=========================

- :doc:`scripting-groovy` - Guia de scripting Groovy
- :doc:`../admin/dataconfig-guide` - Guia de configuracion de Data Store
- :doc:`../admin/scheduler-guide` - Guia de configuracion del programador
