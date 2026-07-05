==================================
Plugin Script Engine
==================================

Vue d'ensemble
==============

En developpant un plugin Script Engine, vous pouvez ajouter le support de nouveaux
langages de script a |Fess|.

Implementation de base
======================

Implementez l'interface ``ScriptEngine``:

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
            // Logique d'evaluation du script
            return executeScript(script, params);
        }
    }

Enregistrement
==============

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getScriptEngineManager().add(this);
    }

Exemple d'utilisation
=====================

Selection du type de script dans l'interface d'administration:

::

    scriptType=example
    scriptData=your script here

Informations complementaires
============================

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`../config/scripting-overview` - Vue d'ensemble du scripting
