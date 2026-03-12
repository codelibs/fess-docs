==================================
Plugin Ingest
==================================

Vue d'ensemble
==============

Les plugins Ingest fournissent des fonctionnalites de traitement et de transformation
des donnees avant leur enregistrement dans l'index.

Cas d'utilisation
=================

- Normalisation du texte (conversion pleine largeur/demi-largeur, etc.)
- Ajout de metadonnees
- Masquage d'informations sensibles
- Ajout de champs personnalises

Implementation de base
======================

Implementez l'interface ``IngestHandler``:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import org.codelibs.fess.ingest.IngestHandler;
    import java.util.Map;

    public class ExampleIngestHandler implements IngestHandler {

        @Override
        public Map<String, Object> process(Map<String, Object> document) {
            // Normalisation du contenu
            String content = (String) document.get("content");
            if (content != null) {
                content = normalizeText(content);
                document.put("content", content);
            }

            // Ajout d'un champ personnalise
            document.put("processed_at", new Date());

            return document;
        }

        private String normalizeText(String text) {
            // Logique de normalisation
            return text.trim().replaceAll("\\s+", " ");
        }
    }

Enregistrement
==============

``fess_ingest.xml``:

.. code-block:: xml

    <component name="exampleIngestHandler"
               class="org.codelibs.fess.ingest.example.ExampleIngestHandler">
        <postConstruct name="register"/>
    </component>

Configuration
=============

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

Informations complementaires
============================

- :doc:`plugin-architecture` - Architecture des plugins
