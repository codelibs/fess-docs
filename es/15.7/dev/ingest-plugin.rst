==================================
Plugin Ingest
==================================

Visión General
==============

Los plugins Ingest proporcionan funcionalidad para procesar y transformar
datos antes de que los documentos se registren en el índice.

Casos de Uso
============

- Normalización de texto (conversión de ancho completo/medio, etc.)
- Adición de metadatos
- Enmascaramiento de información sensible
- Adición de campos personalizados

Implementación Básica
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

Configuración
=============

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

Información de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
