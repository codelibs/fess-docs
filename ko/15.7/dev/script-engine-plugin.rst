==================================
스크립트 엔진 플러그인
==================================

개요
====

스크립트 엔진 플러그인을 개발하면 |Fess|에 새로운 스크립트 언어
지원을 추가할 수 있습니다.

기본 구현
========

``ScriptEngine`` 인터페이스를 구현합니다:

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
            // 스크립트 평가 로직
            return executeScript(script, params);
        }
    }

등록
====

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getScriptEngineManager().add(this);
    }

사용 예
======

관리 화면에서 스크립트 유형으로 선택:

::

    scriptType=example
    scriptData=your script here

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`../config/scripting-overview` - 스크립팅 개요
