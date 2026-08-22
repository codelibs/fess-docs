==================================
スクリプトエンジンプラグイン
==================================

概要
====

スクリプトエンジンプラグインを開発することで、|Fess| に新しいスクリプト言語の
サポートを追加できます。

基本実装
========

``ScriptEngine`` インターフェースを実装します:

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
            // スクリプトの評価ロジック
            return executeScript(script, params);
        }
    }

登録
====

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getScriptEngineManager().add(this);
    }

使用例
======

管理画面でスクリプトタイプとして選択:

::

    scriptType=example
    scriptData=your script here

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
- :doc:`../config/scripting-overview` - スクリプティング概要
