==================================
Ingest-Plugin
==================================

Ubersicht
=========

Ingest-Plugins bieten Funktionen zur Verarbeitung und Transformation von Daten,
bevor Dokumente im Index registriert werden.

Anwendungsfalle
===============

- Textnormalisierung (z.B. Vollbreite/Halbbreite-Konvertierung)
- Hinzufugen von Metadaten
- Maskierung sensibler Informationen
- Hinzufugen benutzerdefinierter Felder

Grundimplementierung
====================

Implementieren Sie das ``IngestHandler``-Interface:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import org.codelibs.fess.ingest.IngestHandler;
    import java.util.Map;

    public class ExampleIngestHandler implements IngestHandler {

        @Override
        public Map<String, Object> process(Map<String, Object> document) {
            // Inhaltsnormalisierung
            String content = (String) document.get("content");
            if (content != null) {
                content = normalizeText(content);
                document.put("content", content);
            }

            // Benutzerdefiniertes Feld hinzufugen
            document.put("processed_at", new Date());

            return document;
        }

        private String normalizeText(String text) {
            // Normalisierungslogik
            return text.trim().replaceAll("\\s+", " ");
        }
    }

Registrierung
=============

``fess_ingest.xml``:

.. code-block:: xml

    <component name="exampleIngestHandler"
               class="org.codelibs.fess.ingest.example.ExampleIngestHandler">
        <postConstruct name="register"/>
    </component>

Konfiguration
=============

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

Referenzinformationen
=====================

- :doc:`plugin-architecture` - Plugin-Architektur
