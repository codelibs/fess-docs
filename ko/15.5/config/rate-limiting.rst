==================================
속도 제한 설정
==================================

개요
====

|Fess|에는 시스템의 안정성과 성능을 유지하기 위한 속도 제한 기능이 있습니다.
이 기능을 통해 과도한 요청으로부터 시스템을 보호하고 공정한 리소스 배분을 실현할 수 있습니다.

속도 제한은 다음 장면에서 적용됩니다:

- 검색 API
- AI 모드 API
- 크롤러 요청

검색 API 속도 제한
===================

검색 API로의 요청 수를 제한할 수 있습니다.

설정
----

``app/WEB-INF/conf/system.properties``:

::

    # 속도 제한 활성화
    api.rate.limit.enabled=true

    # IP 주소당 1분당 최대 요청 수
    api.rate.limit.requests.per.minute=60

    # 속도 제한 윈도우 크기(초)
    api.rate.limit.window.seconds=60

동작
----

- 속도 제한을 초과한 요청은 HTTP 429 (Too Many Requests)를 반환합니다
- 제한은 IP 주소 단위로 적용됩니다
- 제한값은 슬라이딩 윈도우 방식으로 카운트됩니다

AI 모드 속도 제한
=======================

AI 모드 기능에는 LLM API 비용과 리소스 소비를 제어하기 위한 속도 제한이 있습니다.

설정
----

``app/WEB-INF/conf/system.properties``:

::

    # 채팅 속도 제한 활성화
    rag.chat.rate.limit.enabled=true

    # 1분당 최대 요청 수
    rag.chat.rate.limit.requests.per.minute=10

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

고급 속도 제한 설정
====================

커스텀 속도 제한
------------------

특정 사용자나 역할에 다른 제한을 적용하려면
커스텀 컴포넌트 구현이 필요합니다.

::

    // RateLimitHelper 커스터마이즈 예
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean isAllowed(String key) {
            // 커스텀 로직
        }
    }

버스트 제한
------------

단시간의 돌발적인 요청을 허용하면서 지속적인 고부하를 방지하는 설정:

::

    # 버스트 허용량
    api.rate.limit.burst.size=20

    # 지속적인 제한
    api.rate.limit.sustained.requests.per.second=1

제외 설정
========

특정 IP 주소나 사용자를 속도 제한에서 제외할 수 있습니다.

::

    # 제외 IP 주소(쉼표 구분)
    api.rate.limit.excluded.ips=192.168.1.100,10.0.0.0/8

    # 제외 역할
    api.rate.limit.excluded.roles=admin

모니터링과 알림
==============

속도 제한 상황을 모니터링하기 위한 설정:

로그 출력
--------

속도 제한이 적용되면 로그에 기록됩니다:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

메트릭스
----------

속도 제한에 관한 메트릭스는 시스템 통계 API에서 가져올 수 있습니다:

::

    GET /api/admin/stats

문제 해결
======================

정당한 요청이 차단됨
--------------------------------

**원인**: 제한값이 너무 엄격함

**해결 방법**:

1. ``requests.per.minute`` 증가
2. 특정 IP를 제외 목록에 추가
3. 윈도우 크기 조정

속도 제한이 작동하지 않음
--------------------

**원인**: 설정이 올바르게 반영되지 않음

**확인 사항**:

1. ``api.rate.limit.enabled=true``가 설정되어 있는지
2. 설정 파일이 올바르게 읽혀지고 있는지
3. |Fess|를 재시작했는지

성능 영향
----------------------

속도 제한 체크 자체가 성능에 영향을 미치는 경우:

1. 속도 제한 스토리지를 Redis 등으로 변경
2. 체크 빈도 조정

참고 정보
========

- :doc:`rag-chat` - AI 모드 기능 설정
- :doc:`../admin/webconfig-guide` - 웹 크롤 설정 가이드
- :doc:`../api/api-overview` - API 개요
