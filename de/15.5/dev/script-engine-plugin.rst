==================================
Script-Engine-Plugin
==================================

Ubersicht
=========

Durch die Entwicklung eines Script-Engine-Plugins konnen Sie |Fess| Unterstutzung
fur neue Skriptsprachen hinzufugen.

Grundimplementierung
====================

Implementieren Sie das ``ScriptEngine``-Interface:

.. code-block:: java

    package org.codelibs.fess.script.example;

    import org.codelibs.fess.script.ScriptEngine;
    import java.util.Map;

    public class ExampleScriptEngine implements ScriptEngine {

        @Override
        public String getName() {
            return "example";
        }

        @Override
        public Object evaluate(String script, Map<String, Object> params) {
            // Skript-Auswertungslogik
            return executeScript(script, params);
        }
    }

Registrierung
=============

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getScriptEngineManager().add(this);
    }

Verwendungsbeispiel
===================

Auswahl als Skripttyp in der Administrationsoberflache:

::

    scriptType=example
    scriptData=your script here

Referenzinformationen
=====================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`../config/scripting-overview` - Scripting-Ubersicht
