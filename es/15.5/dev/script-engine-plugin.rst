==================================
Plugin de Motor de Scripts
==================================

Vision General
==============

Al desarrollar un plugin de motor de scripts, puede agregar soporte para
nuevos lenguajes de script a |Fess|.

Implementacion Basica
=====================

Implemente la interfaz ``ScriptEngine``:

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
            // Logica de evaluacion del script
            return executeScript(script, params);
        }
    }

Registro
========

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getScriptEngineManager().add(this);
    }

Ejemplo de Uso
==============

Seleccione como tipo de script en la pantalla de administracion:

::

    scriptType=example
    scriptData=your script here

Informacion de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`../config/scripting-overview` - Vision general de scripting
