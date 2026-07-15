==================================
Ingest 플러그인
==================================

개요
====

Ingest 플러그인은 문서가 인덱스에 등록되기 직전에
데이터를 가공·변환하는 기능을 제공합니다. 크롤링으로 수집한 각 문서는,
인덱스로 전송되기 전에 등록된 Ingester를 통과합니다.

용도
====

- 텍스트 정규화(전각/반각 변환, 공백 정리 등)
- 메타데이터나 커스텀 필드 추가
- 민감한 정보 마스킹
- 값 변환(예: 인코딩된 벡터 임베딩 디코딩)

Ingester 클래스
===============

Ingest 기능은 ``org.codelibs.fess.ingest.Ingester`` 추상 클래스를 상속하여
구현합니다. ``Ingester``에는 크롤링 종류나 처리 단계에 따라
호출되는 ``process`` 메서드가 준비되어 있습니다. 기본 구현은
모두 전달받은 ``target``을 그대로 반환(아무 작업도 하지 않음)하므로,
필요한 메서드만 오버라이드합니다.

- ``protected Map<String, Object> process(Map<String, Object> target)``

  두 ``Map`` 버전 메서드가 공통으로 위임하는 대상입니다. 이 메서드를 오버라이드하면
  데이터 스토어 크롤링과 Web/파일 크롤링(인덱스 등록 시) 양쪽 문서에 모두 적용됩니다.
  대부분의 용도에서는 이 메서드만 오버라이드하면 충분합니다.

- ``public Map<String, Object> process(Map<String, Object> target, DataStoreParams params)``

  데이터 스토어 크롤링 시 호출됩니다. 기본적으로
  ``process(target)``에 위임합니다.

- ``public Map<String, Object> process(Map<String, Object> target, AccessResult<String> accessResult)``

  Web/파일 크롤링의 인덱스 등록 시 호출됩니다.
  기본적으로 ``process(target)``에 위임합니다.

- ``public ResultData process(ResultData target, ResponseData responseData)``

  Web/파일 크롤링의 응답 처리 시(액세스 결과를 저장하기 전)에
  호출됩니다. 기본적으로 ``target``을 그대로 반환합니다.

실행 순서(priority)
--------------------

여러 Ingester가 등록되어 있는 경우 ``priority`` 필드의 오름차순
(값이 작은 것이 먼저)으로 실행됩니다. 기본값은 ``99``입니다.
생성자에서 직접 설정하거나 ``setPriority(int)``로 변경할 수 있습니다.

.. code-block:: java

    public int getPriority()
    public void setPriority(final int priority)

구현 예시
======

``process(Map<String, Object>)``를 오버라이드하여 콘텐츠를 정규화하고
커스텀 필드를 추가하는 예시입니다:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {

        public ExampleIngester() {
            // 실행 순서를 설정(값이 작을수록 먼저 실행됨. 기본값은 99)
            setPriority(50);
        }

        @Override
        protected Map<String, Object> process(final Map<String, Object> target) {
            // 콘텐츠 정규화
            final Object content = target.get("content");
            if (content instanceof String) {
                target.put("content", ((String) content).trim().replaceAll("\\s+", " "));
            }

            // 커스텀 필드 추가
            target.put("ingested_by", ExampleIngester.class.getSimpleName());

            // 가공한 문서를 반환
            return target;
        }
    }

.. note::

    ``process`` 메서드에서 ``null``을 반환하면 인덱스 등록이 실패합니다.
    문서를 건너뛰는 방법은 없으므로 반드시 ``target``을 반환해야 합니다.

등록
====

Ingester는 DI 컨테이너를 통해 등록합니다. 플러그인에는 ``fess_ingest++.xml``
을 포함합니다. 파일명 끝의 ``++``는 |Fess| 본체의 ``fess_ingest.xml``
(Ingester를 관리하는 ``ingestFactory``를 정의)에 설정을 추가하는 병합 규칙입니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleIngester"
                   class="org.codelibs.fess.ingest.example.ExampleIngester">
            <postConstruct name="register"/>
        </component>
    </components>

``<postConstruct name="register"/>``에 의해 컴포넌트 생성 후
``Ingester#register()``가 호출되어 ``ingestFactory``에 자신이 등록됩니다.

Ingest 기능과 관련된 ``fess_config.properties`` 설정 항목은 없습니다.
활성화 여부는 플러그인 도입 여부로, 실행 순서는 ``priority``로 제어합니다.

실행 흐름
==========

Ingester는 가공된 문서가 인덱스로 전송되기 직전에,
다음 위치에서 ``priority`` 오름차순으로 호출됩니다:

- **데이터 스토어 크롤링**: 문서를 전송하기 직전에
  ``process(Map, DataStoreParams)``가 호출됩니다.
- **Web/파일 크롤링(응답 처리 시)**: 크롤링 결과를 저장하기 전에
  ``process(ResultData, ResponseData)``가 호출됩니다.
- **Web/파일 크롤링(인덱스 등록 시)**: 문서를 전송하기 직전에
  ``process(Map, AccessResult)``가 호출됩니다.

어느 위치에서든 특정 Ingester가 예외를 던지면 경고 로그를 출력하고
처리를 계속합니다(해당 문서의 인덱스 등록은 중단되지 않습니다).

.. note::

    Ingester는 크롤러 실행 환경(``ingestFactory``)에 등록되므로
    크롤링 처리의 일부로 동작합니다.

참고 구현
========

구현 참고 자료로 다음 플러그인이 GitHub의
`CodeLibs <https://github.com/codelibs>`__ 에 공개되어 있습니다:

- ``fess-ingest-example`` - 최소 구성의 샘플 구현
- ``fess-webapp-multimodal`` - 벡터 임베딩을 디코딩하는 ``EmbeddingIngester``를 포함하는 플러그인

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
