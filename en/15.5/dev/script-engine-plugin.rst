==================================
Script Engine Plugin
==================================

Overview
========

By developing a Script Engine plugin, you can add support for new scripting
languages to |Fess|.

Basic Implementation
====================

Implement the ``ScriptEngine`` interface:

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
            // Script evaluation logic
            return executeScript(script, params);
        }
    }

Registration
============

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getScriptEngineManager().add(this);
    }

Usage Example
=============

Select as script type in admin console:

::

    scriptType=example
    scriptData=your script here

Reference
=========

- :doc:`plugin-architecture` - Plugin Architecture
- :doc:`../config/scripting-overview` - Scripting Overview

