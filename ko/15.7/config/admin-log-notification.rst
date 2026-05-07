================
로그 통지
================

개요
====

|Fess| 에는 ERROR 또는 WARN 레벨의 로그 이벤트를 자동으로 포착하여 관리자에게 통지하는 기능이 있습니다.
이 기능을 통해 시스템 이상을 신속하게 감지하고 장애 대응을 조기에 시작할 수 있습니다.

주요 특징:

- **지원하는 통지 채널**: 메일, Slack, Google Chat
- **대상 프로세스**: 메인 애플리케이션, 크롤러, 서제스트 생성, 썸네일 생성
- **기본 비활성화**: 옵트인 방식이므로 명시적으로 활성화해야 합니다

동작 원리
=========

로그 통지는 다음 흐름으로 동작합니다.

1. Log4j2의 ``LogNotificationAppender`` 가 설정된 레벨 이상의 로그 이벤트를 포착합니다.
2. 포착된 이벤트는 메모리상의 버퍼(최대 1,000건)에 축적됩니다.
3. 타이머가 30초 간격으로 버퍼 내의 이벤트를 OpenSearch 인덱스(``fess_log.notification_queue``)에 기록합니다.
4. 스케줄 잡이 5분 간격으로 OpenSearch에서 이벤트를 읽어들여 로그 레벨별로 그룹화하여 통지를 전송합니다.
5. 통지 전송 후 처리 완료된 이벤트는 인덱스에서 삭제됩니다.

.. note::
   통지 기능 자체의 로그(``LogNotificationHelper``, ``LogNotificationJob`` 등)는
   무한 루프를 방지하기 위해 통지 대상에서 제외됩니다.

설정
====

활성화
------

관리 화면에서 활성화
~~~~~~~~~~~~~~~~~~~~

1. 관리 화면에 로그인합니다.
2. "시스템" 메뉴에서 "전반"을 선택합니다.
3. "로그 통지" 체크박스를 활성화합니다.
4. "로그 통지 레벨"에서 통지 대상 레벨을 선택합니다(``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. "업데이트" 버튼을 클릭합니다.

.. note::
   기본적으로 ``ERROR`` 레벨만 통지 대상입니다.
   ``WARN`` 을 선택하면 ``WARN`` 과 ``ERROR`` 모두 통지됩니다.

시스템 프로퍼티를 통한 활성화
~~~~~~~~~~~~~~~~~~~~~~~~

관리 화면의 "전반" 설정에서 저장되는 시스템 프로퍼티를 직접 설정할 수도 있습니다.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

통지 대상 설정
--------------

메일 통지
~~~~~~~~~~

메일 통지를 이용하려면 다음 설정이 필요합니다.

1. 메일 서버 설정(``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. 관리 화면의 "전반" 설정에서 "통지 대상"에 메일 주소를 입력합니다. 여러 주소는 쉼표로 구분하여 지정할 수 있습니다.

Slack 통지
~~~~~~~~~~

Slack의 Incoming Webhook URL을 설정하면 Slack 채널에 통지를 전송할 수 있습니다.

Google Chat 통지
~~~~~~~~~~~~~~~~

Google Chat의 Webhook URL을 설정하면 Google Chat 스페이스에 통지를 전송할 수 있습니다.

설정 프로퍼티
=============

``fess_config.properties`` 에서 다음 프로퍼티를 설정할 수 있습니다.

.. list-table:: 로그 통지 설정 프로퍼티
   :header-rows: 1
   :widths: 40 15 45

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``log.notification.flush.interval``
     - ``30``
     - 버퍼에서 OpenSearch로의 플러시 간격(초)
   * - ``log.notification.buffer.size``
     - ``1000``
     - 메모리상의 버퍼에 보관하는 이벤트의 최대 수
   * - ``log.notification.interval``
     - ``300``
     - 통지 잡의 실행 간격(초)
   * - ``log.notification.search.size``
     - ``1000``
     - 1회 잡 실행에서 OpenSearch로부터 가져오는 이벤트의 최대 수
   * - ``log.notification.max.display.events``
     - ``50``
     - 1회 통지 메시지에 포함하는 이벤트의 최대 수
   * - ``log.notification.max.message.length``
     - ``200``
     - 각 로그 메시지의 최대 문자 수(초과분은 잘림)
   * - ``log.notification.max.details.length``
     - ``3000``
     - 통지 메시지의 상세 부분의 최대 문자 수

.. note::
   이러한 프로퍼티의 변경은 |Fess| 재시작 후에 반영됩니다.

통지 메시지 형식
================

메일 통지
---------

메일 통지는 다음 형식으로 전송됩니다.

**제목:**

::

    [FESS] ERROR Log Alert: hostname

**본문:**

::

    --- Server Info ---
    Host Name: hostname

    --- Log Summary ---
    Level: ERROR
    Total: 5 event(s) in the last 300 seconds

    --- Log Details ---
    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR와 WARN 이벤트는 레벨별로 별도의 통지로 전송됩니다.

Slack / Google Chat 통지
------------------------

Slack 및 Google Chat 통지도 동일한 내용이 메시지로 전송됩니다.

운영 가이드
===========

권장 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 환경
     - 권장 레벨
     - 이유
   * - 운영 환경
     - ``ERROR``
     - 중요한 오류만 통지하여 노이즈를 줄임
   * - 스테이징 환경
     - ``WARN``
     - 잠재적인 문제도 포함하여 통지
   * - 개발 환경
     - 비활성화
     - 로그 파일을 직접 확인

OpenSearch 인덱스
-----------------

로그 통지 기능은 이벤트의 임시 보관에 ``fess_log.notification_queue`` 인덱스를 사용합니다.
이 인덱스는 기능의 최초 사용 시 자동으로 생성됩니다.
통지 전송 후 이벤트는 삭제되므로 일반적으로 인덱스 크기가 커지지 않습니다.

문제 해결
=========

통지가 전송되지 않음
--------------------

1. **활성화 확인**

   관리 화면의 "전반" 설정에서 "로그 통지"가 활성화되어 있는지 확인합니다.

2. **통지 대상 확인**

   메일 통지의 경우 "통지 대상"에 메일 주소가 설정되어 있는지 확인합니다.

3. **메일 서버 설정 확인**

   ``fess_env.properties`` 에서 메일 서버가 올바르게 설정되어 있는지 확인합니다.

4. **로그 확인**

   ``fess.log`` 에서 통지 관련 오류 메시지를 확인합니다.

   ::

       grep -i "notification" /var/log/fess/fess.log

통지가 너무 많음
----------------

1. **로그 레벨 상향**

   통지 레벨을 ``WARN`` 에서 ``ERROR`` 로 변경합니다.

2. **근본 원인 해결**

   오류가 빈번하게 발생하는 경우 오류의 근본 원인을 조사하십시오.

통지 내용이 잘림
----------------

다음 프로퍼티를 조정하십시오.

- ``log.notification.max.details.length``: 상세 부분의 최대 문자 수
- ``log.notification.max.display.events``: 표시할 이벤트의 최대 수
- ``log.notification.max.message.length``: 각 메시지의 최대 문자 수

참고 정보
=========

- :doc:`admin-logging` - 로그 설정
- :doc:`setup-memory` - 메모리 설정
