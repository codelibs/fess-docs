==================================
Plugin Ingest
==================================

Visión General
==============

Los plugins Ingest proporcionan la funcionalidad de procesar y transformar
datos justo antes de que los documentos se registren en el índice. Cada
documento obtenido mediante el rastreo pasa por los Ingester registrados
antes de enviarse al índice.

Casos de Uso
============

- Normalización de texto (conversión de ancho completo/medio, ajuste de
  espacios en blanco, etc.)
- Adición de metadatos y campos personalizados
- Enmascaramiento de información sensible
- Conversión de valores (por ejemplo: decodificación de embeddings
  vectoriales codificados)

Clase Ingester
==============

La funcionalidad de Ingest se implementa heredando de la clase abstracta
``org.codelibs.fess.ingest.Ingester``. ``Ingester`` proporciona métodos
``process`` que se invocan según el tipo de rastreo y la etapa de
procesamiento. Dado que todas las implementaciones por defecto devuelven
el ``target`` recibido tal cual (sin hacer nada), solo es necesario
sobrescribir los métodos que se necesiten.

- ``protected Map<String, Object> process(Map<String, Object> target)``

  Es el destino común de delegación de las dos versiones de métodos
  ``Map``. Si se sobrescribe, se aplica tanto a los documentos del
  rastreo de almacén de datos como a los del rastreo web/de archivos
  (durante el registro en el índice). Para la mayoría de los casos de
  uso, basta con sobrescribir únicamente este método.

- ``public Map<String, Object> process(Map<String, Object> target, DataStoreParams params)``

  Se invoca durante el rastreo de almacén de datos. Por defecto,
  delega en ``process(target)``.

- ``public Map<String, Object> process(Map<String, Object> target, AccessResult<String> accessResult)``

  Se invoca durante el registro en el índice del rastreo web/de
  archivos. Por defecto, delega en ``process(target)``.

- ``public ResultData process(ResultData target, ResponseData responseData)``

  Se invoca durante el procesamiento de la respuesta del rastreo
  web/de archivos (antes de guardar el resultado de acceso). Por
  defecto, devuelve el ``target`` tal cual.

Orden de ejecución (priority)
-----------------------------

Cuando hay varios Ingester registrados, se ejecutan en orden ascendente
del campo ``priority`` (los valores más pequeños se ejecutan primero).
El valor por defecto es ``99``. Se puede establecer directamente en el
constructor o modificar mediante ``setPriority(int)``.

.. code-block:: java

    public int getPriority()
    public void setPriority(final int priority)

Ejemplo de Implementación
=========================

Ejemplo que sobrescribe ``process(Map<String, Object>)`` para normalizar
el contenido y añadir un campo personalizado:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {

        public ExampleIngester() {
            // Establece el orden de ejecución (los valores más pequeños se ejecutan primero; el valor por defecto es 99)
            setPriority(50);
        }

        @Override
        protected Map<String, Object> process(final Map<String, Object> target) {
            // Normalización del contenido
            final Object content = target.get("content");
            if (content instanceof String) {
                target.put("content", ((String) content).trim().replaceAll("\\s+", " "));
            }

            // Adición de un campo personalizado
            target.put("ingested_by", ExampleIngester.class.getSimpleName());

            // Devuelve el documento procesado
            return target;
        }
    }

.. note::

    Si el método ``process`` devuelve ``null``, el registro en el
    índice fallará. Como no existe un mecanismo para omitir documentos,
    asegúrese siempre de devolver ``target``.

Registro
========

Los Ingester se registran a través del contenedor DI. El plugin debe
incluir ``fess_ingest++.xml``. El sufijo ``++`` al final del nombre del
archivo es una convención de fusión que añade la configuración a
``fess_ingest.xml`` (que define ``ingestFactory``, encargado de
gestionar los Ingester) del núcleo de |Fess|.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleIngester"
                   class="org.codelibs.fess.ingest.example.ExampleIngester">
            <postConstruct name="register"/>
        </component>
    </components>

Gracias a ``<postConstruct name="register"/>``, tras crear el componente
se invoca ``Ingester#register()``, con lo que se registra a sí mismo en
``ingestFactory``.

No existen elementos de configuración relacionados con la
funcionalidad de Ingest en ``fess_config.properties``. La activación o
desactivación depende de si el plugin está instalado, y el orden de
ejecución se controla mediante ``priority``.

Flujo de Ejecución
==================

Los Ingester se invocan en orden ascendente de ``priority`` justo antes
de que el documento procesado se envíe al índice, en los siguientes
puntos:

- **Rastreo de almacén de datos**: se invoca
  ``process(Map, DataStoreParams)`` justo antes de enviar el documento.
- **Rastreo web/de archivos (procesamiento de la respuesta)**: se
  invoca ``process(ResultData, ResponseData)`` antes de guardar el
  resultado del rastreo.
- **Rastreo web/de archivos (registro en el índice)**: se invoca
  ``process(Map, AccessResult)`` justo antes de enviar el documento.

En cualquiera de estos puntos, si un Ingester lanza una excepción, se
emite un registro de advertencia y el procesamiento continúa (el
registro en el índice de ese documento no se interrumpe).

.. note::

    Dado que los Ingester se registran en el entorno de ejecución del
    rastreador (``ingestFactory``), funcionan como parte del proceso
    de rastreo.

Implementación de Referencia
============================

Como referencia de implementación, los siguientes plugins están
publicados en `CodeLibs <https://github.com/codelibs>`__ en GitHub:

- ``fess-ingest-example`` - Implementación de ejemplo con la
  configuración mínima
- ``fess-webapp-multimodal`` - Plugin que incluye ``EmbeddingIngester``,
  encargado de decodificar embeddings vectoriales

Información de Referencia
==========================

- :doc:`plugin-architecture` - Arquitectura de plugins
