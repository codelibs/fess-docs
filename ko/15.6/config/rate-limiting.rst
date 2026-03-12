==================================
속도 제한 설정
==================================

개요
====

|Fess|에는 시스템의 안정성과 성능을 유지하기 위한 속도 제한 기능이 있습니다.
이 기능을 통해 과도한 요청으로부터 시스템을 보호하고 공정한 리소스 배분을 실현할 수 있습니다.

속도 제한은 다음 장면에서 적용됩니다:

- 검색 API나 AI 모드 API를 포함한 모든 HTTP 요청(``RateLimitFilter``)
- 크롤러 요청(크롤 설정에 의한 제어)

HTTP 요청 속도 제한
==========================

|Fess|로의 HTTP 요청 수를 IP 주소 단위로 제한할 수 있습니다.
이 제한은 검색 API, AI 모드 API, 관리 화면 등 모든 HTTP 요청에 적용됩니다.

설정
----

``app/WEB-INF/conf/fess_config.properties``:

::

    # 속도 제한 활성화(기본값: false)
    rate.limit.enabled=true

    # 윈도우당 최대 요청 수(기본값: 100)
    rate.limit.requests.per.window=100

    # 윈도우 크기(밀리초)(기본값: 60000)
    rate.limit.window.ms=60000

동작
----

- 속도 제한을 초과한 요청은 HTTP 429 (Too Many Requests)를 반환합니다
- 블록 IP 목록에 포함된 IP의 요청은 HTTP 403 (Forbidden)을 반환합니다
- 제한은 IP 주소 단위로 적용됩니다
- IP별로 최초 요청부터 윈도우가 시작되며, 윈도우 기간 경과 후 카운트가 리셋됩니다(고정 윈도우 방식)
- 제한 초과 시 IP가 ``rate.limit.block.duration.ms`` 기간 동안 블록됩니다

AI 모드 속도 제한
====================

AI 모드 기능에는 LLM API 비용과 리소스 소비를 제어하기 위한 속도 제한이 있습니다.
AI 모드에는 위의 HTTP 요청 속도 제한에 더하여 AI 모드 고유의 속도 제한도 설정할 수 있습니다.

AI 모드 고유의 속도 제한 설정에 대해서는 :doc:`rag-chat`를 참조하세요.

.. note::
   AI 모드 속도 제한은 LLM 프로바이더 측의 속도 제한과 별도로 적용됩니다.
   양쪽 제한을 고려하여 설정하세요.

크롤러 속도 제한
======================

크롤러가 대상 사이트에 과도한 부하를 주지 않도록 요청 간격을 설정할 수 있습니다.

웹 크롤 설정
---------------

관리 화면의 "크롤러" -> "웹"에서 다음을 설정:

- **요청 간격**: 요청 사이의 대기 시간(밀리초)
- **스레드 수**: 병렬 크롤 스레드 수

권장 설정:

::

    # 일반적인 사이트
    intervalTime=1000
    numOfThread=1

    # 대규모 사이트(허가가 있는 경우)
    intervalTime=500
    numOfThread=3

robots.txt 준수
----------------

|Fess|는 기본적으로 robots.txt의 Crawl-delay 지시를 준수합니다.

::

    # robots.txt 예
    User-agent: *
    Crawl-delay: 10

속도 제한 전체 설정 항목
=========================

``app/WEB-INF/conf/fess_config.properties``에서 설정 가능한 모든 프로퍼티입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rate.limit.enabled``
     - 속도 제한 활성화
     - ``false``
   * - ``rate.limit.requests.per.window``
     - 윈도우당 최대 요청 수
     - ``100``
   * - ``rate.limit.window.ms``
     - 윈도우 크기(밀리초)
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - 제한 초과 시 IP 블록 기간(밀리초)
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Retry-After 헤더 값(초)
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - 속도 제한에서 제외할 IP 주소(쉼표 구분)
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - 블록할 IP 주소(쉼표 구분)
     - (비어 있음)
   * - ``rate.limit.trusted.proxies``
     - 신뢰하는 프록시 IP(X-Forwarded-For/X-Real-IP 취득원)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - 메모리 누수 방지를 위한 클린업 간격(요청 수)
     - ``1000``

고급 속도 제한 설정
====================

커스텀 속도 제한
------------------

특정 조건에 따라 다른 속도 제한 로직을 적용하려면
커스텀 컴포넌트 구현이 필요합니다.

::

    // RateLimitHelper 커스터마이즈 예
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // 커스텀 로직
        }
    }

제외 설정
========

특정 IP 주소를 속도 제한에서 제외하거나 블록할 수 있습니다.

::

    # 화이트리스트 IP(속도 제한에서 제외, 쉼표 구분)
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # 블록 IP 목록(항상 블록, 쉼표 구분)
    rate.limit.blocked.ips=203.0.113.50

    # 신뢰하는 프록시 IP(쉼표 구분)
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   리버스 프록시를 사용하는 경우 ``rate.limit.trusted.proxies``에
   프록시의 IP 주소를 설정하세요. 신뢰하는 프록시에서의 요청만
   X-Forwarded-For 및 X-Real-IP 헤더에서 클라이언트 IP를 취득합니다.

모니터링과 알림
==============

속도 제한 상황을 모니터링하기 위한 설정:

로그 출력
--------

속도 제한이 적용되면 로그에 기록됩니다:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

문제 해결
======================

정당한 요청이 차단됨
--------------------------------

**원인**: 제한값이 너무 엄격함

**해결 방법**:

1. ``rate.limit.requests.per.window`` 증가
2. 특정 IP를 화이트리스트에 추가(``rate.limit.whitelist.ips``)
3. 윈도우 크기(``rate.limit.window.ms``) 조정

속도 제한이 작동하지 않음
--------------------

**원인**: 설정이 올바르게 반영되지 않음

**확인 사항**:

1. ``rate.limit.enabled=true``가 설정되어 있는지
2. 설정 파일이 올바르게 읽혀지고 있는지
3. |Fess|를 재시작했는지

성능 영향
----------------------

속도 제한 체크 자체가 성능에 영향을 미치는 경우:

1. 화이트리스트를 활용하여 신뢰할 수 있는 IP의 체크를 스킵
2. 속도 제한을 무효화(``rate.limit.enabled=false``)

참고 정보
========

- :doc:`rag-chat` - AI 모드 기능 설정
- :doc:`../admin/webconfig-guide` - 웹 크롤 설정 가이드
- :doc:`../api/api-overview` - API 개요
