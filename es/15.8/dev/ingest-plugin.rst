==================================
Plugin Ingest
==================================

Vision General
==============

Los plugins Ingest proporcionan funcionalidad para procesar y transformar
datos antes de que los documentos se registren en el indice.

Casos de Uso
============

- Normalizacion de texto (conversion de ancho completo/medio, etc.)
- Adicion de metadatos
- Enmascaramiento de informacion sensible
- Adicion de campos personalizados

Implementacion Basica
=====================

Implemente la interfaz ``IngestHandler``:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import org.codelibs.fess.ingest.IngestHandler;
    import java.util.Map;

    public class ExampleIngestHandler implements IngestHandler {

        @Override
        public Map<String, Object> process(Map<String, Object> document) {
            // Normalizacion de contenido
            String content = (String) document.get("content");
            if (content != null) {
                content = normalizeText(content);
                document.put("content", content);
            }

            // Adicion de campo personalizado
            document.put("processed_at", new Date());

            return document;
        }

        private String normalizeText(String text) {
            // Logica de normalizacion
            return text.trim().replaceAll("\\s+", " ");
        }
    }

Registro
========

``fess_ingest.xml``:

.. code-block:: xml

    <component name="exampleIngestHandler"
               class="org.codelibs.fess.ingest.example.ExampleIngestHandler">
        <postConstruct name="register"/>
    </component>

Configuracion
=============

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

Informacion de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
