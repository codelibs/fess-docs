==================================
스크립팅 개요
==================================

개요
====

|Fess|에서는 다양한 장면에서 스크립트를 사용하여 커스텀 로직을 구현할 수 있습니다.
스크립트를 활용하면 크롤링 시 데이터 가공, 검색 결과 커스터마이즈,
스케줄 작업 실행 등을 유연하게 제어할 수 있습니다.

지원 스크립트 언어
==================

|Fess|는 다음 스크립트 언어를 지원합니다:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 언어
     - 식별자
     - 설명
   * - Groovy
     - ``groovy``
     - 기본 스크립트 언어. Java 호환으로 강력한 기능 제공
   * - JavaScript
     - ``javascript``
     - 웹 개발자에게 친숙한 언어

.. note::
   Groovy가 가장 널리 사용되며, 본 문서의 예제는 Groovy로 작성되어 있습니다.

스크립트 사용 장면
====================

데이터 스토어 설정
----------------

데이터 스토어 커넥터에서는 가져온 데이터를 인덱스 필드에 매핑하기 위해
스크립트를 사용합니다.

::

    url="https://example.com/article/" + data.id
    title=data.name
    content=data.description
    lastModified=data.updated_at

경로 매핑
--------------

URL 정규화나 경로 변환에 스크립트를 사용할 수 있습니다.

::

    # URL 변환
    url.replaceAll("http://", "https://")

스케줄 작업
------------------

스케줄 작업에서는 커스텀 처리 로직을 Groovy 스크립트로 작성할 수 있습니다.

::

    return container.getComponent("crawlJob").execute();

기본 구문
============

변수 접근
------------

::

    # 데이터 스토어의 데이터에 접근
    data.fieldName

    # 시스템 컴포넌트에 접근
    container.getComponent("componentName")

문자열 조작
----------

::

    # 연결
    title + " - " + category

    # 치환
    content.replaceAll("old", "new")

    # 분할
    tags.split(",")

조건 분기
--------

::

    # 삼항 연산자
    data.status == "active" ? "활성화" : "비활성화"

    # null 체크
    data.description ?: "설명 없음"

날짜 조작
--------

::

    # 현재 날짜/시간
    new Date()

    # 포맷
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(data.date)

사용 가능한 객체
======================

스크립트 내에서 사용 가능한 주요 객체:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 객체
     - 설명
   * - ``data``
     - 데이터 스토어에서 가져온 데이터
   * - ``container``
     - DI 컨테이너(컴포넌트에 접근)
   * - ``systemHelper``
     - 시스템 헬퍼
   * - ``fessConfig``
     - |Fess| 설정

보안
============

.. warning::
   스크립트는 강력한 기능을 가지므로 신뢰할 수 있는 소스에서만 사용하세요.

- 스크립트는 서버에서 실행됩니다
- 파일 시스템이나 네트워크에 접근할 수 있습니다
- 관리자 권한을 가진 사용자만 스크립트를 편집할 수 있도록 하세요

성능
==============

스크립트의 성능을 최적화하기 위한 팁:

1. **복잡한 처리 피하기**: 스크립트는 문서마다 실행됩니다
2. **외부 리소스 접근 최소화**: 네트워크 호출은 지연의 원인이 됩니다
3. **캐시 활용**: 반복적으로 사용하는 값은 캐시 검토

디버그
========

스크립트 디버깅에는 로그 출력을 활용합니다:

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")
    logger.info("data.id = {}", data.id)

로그 레벨 설정:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="script" level="DEBUG"/>

참고 정보
========

- :doc:`scripting-groovy` - Groovy 스크립트 가이드
- :doc:`../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../admin/scheduler-guide` - 스케줄러 설정 가이드
