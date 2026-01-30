==================================
脚本引擎插件
==================================

概述
====

通过开发脚本引擎插件，可以为 |Fess| 添加新的脚本语言支持。

基本实现
========

实现 ``ScriptEngine`` 接口:

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
            // 脚本评估逻辑
            return executeScript(script, params);
        }
    }

注册
====

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getScriptEngineManager().add(this);
    }

使用示例
========

在管理界面中选择脚本类型:

::

    scriptType=example
    scriptData=your script here

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`../config/scripting-overview` - 脚本概述

