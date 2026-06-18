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
2. 포착된 이벤트는 메모리상의 버퍼(기본 최대 1,000건)에 축적됩니다. 버퍼가 상한을 초과한 경우 가장 오래된 이벤트부터 순서대로 폐기됩니다.
3. 타이머가 30초 간격으로 버퍼 내의 이벤트를 OpenSearch 인덱스(``fess_log.notification_queue``)에 기록합니다.
4. "Log Notification" 스케줄 잡이 5분 간격으로 OpenSearch에서 이벤트를 읽어들여 로그 레벨별로 그룹화하여 레벨별로 통지를 전송합니다.
5. 통지 전송 후 처리 완료된 이벤트는 인덱스에서 삭제됩니다.

.. note::
   각 노드는 자신이 기록한 로그만을 대상으로 통지합니다(이벤트는 ``hostname`` 으로 필터링됩니다).
   클러스터 구성에서는 노드별로 개별 통지가 전송됩니다.

.. note::
   무한 루프를 방지하기 위해 통지 기능 자체에 관련된 로거
   (``LogNotificationAppender``, ``LogNotificationHelper``, ``LogNotificationTarget``,
   ``LogNotificationJob``, ``NotificationHelper``, 및 HTTP 통신에 사용되는
   ``org.codelibs.curl``)의 로그는 통지 대상에서 제외됩니다.

설정
====

활성화
------

관리 화면에서 활성화
~~~~~~~~~~~~~~~~~~~~~~

1. 관리 화면에 로그인합니다.
2. **시스템** 메뉴에서 **일반** 을 선택합니다.
3. **Log Notification** 체크박스를 활성화합니다.
4. **Log Notification Level** 에서 통지 대상 레벨을 선택합니다(``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. "업데이트" 버튼을 클릭합니다.

.. note::
   기본적으로 ``ERROR`` 레벨만 통지 대상입니다.
   ``WARN`` 을 선택하면 ``WARN`` 과 ``ERROR`` 모두 통지됩니다.

시스템 프로퍼티를 통한 활성화
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

관리 화면의 **일반** 설정에서 저장되는 시스템 프로퍼티(``system.properties``)를 직접 설정할 수도 있습니다.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

통지 대상 설정
--------------

통지 대상(메일 수신처, Slack / Google Chat의 Webhook URL)은 모두 관리 화면의
**시스템** → **일반** 설정에서 구성합니다. 적어도 하나의 통지 대상을 설정하십시오.
통지 대상이 하나도 설정되어 있지 않으면 로그 통지 잡은 아무것도 전송하지 않고 종료됩니다.

메일 통지
~~~~~~~~~

메일 통지를 이용하려면 다음 설정이 필요합니다.

1. 메일 서버 설정(``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. 관리 화면의 **일반** 설정의 **알림 메일** 에 메일 주소를 입력합니다.
   여러 주소는 쉼표로 구분하여 지정할 수 있습니다.

Slack 통지
~~~~~~~~~~

Slack의 Incoming Webhook URL을 관리 화면의 **일반** 설정의 **Slack Webhook URLs** 에 입력합니다.
여러 URL은 쉼표 또는 공백으로 구분하여 지정할 수 있습니다.
이 값은 시스템 프로퍼티 ``slack.webhook.urls`` 로 저장됩니다.

Google Chat 통지
~~~~~~~~~~~~~~~~

Google Chat의 Webhook URL을 관리 화면의 **일반** 설정의 **Google Chat Webhook URLs** 에 입력합니다.
여러 URL은 쉼표 또는 공백으로 구분하여 지정할 수 있습니다.
이 값은 시스템 프로퍼티 ``google.chat.webhook.urls`` 로 저장됩니다.

.. note::
   **알림 메일** 을 설정하지 않고 Slack 또는 Google Chat의 Webhook URL만 설정한 경우,
   메일은 전송되지 않고 Slack / Google Chat에 대한 통지만 이루어집니다.
   Slack / Google Chat에는 메일 통지와 동일한 제목과 본문이 메시지로 전송됩니다.

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
     - 통지 메시지에 표시되는 집계 기간(초). 표시 전용 값이며 실제 잡 실행 간격이 아닙니다(아래 주석 참조).
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
   ``log.notification.flush.interval`` 의 변경은 |Fess| 재시작 후에 반영됩니다.
   그 외의 프로퍼티는 다음 통지 사이클부터 반영됩니다.

.. note::
   ``log.notification.interval`` 은 통지 메시지 내의 "과거 N초 동안"이라는 표시 텍스트에
   사용되는 값이며, 잡의 실행 빈도는 변하지 않습니다. 실제 실행 간격은 "Log Notification"
   스케줄 잡의 cron 설정(기본값은 5분 간격)으로 결정됩니다. 잡의 실행 간격을
   변경하는 경우 **시스템** → **스케줄러** 에서 이 잡의 cron 식을 변경하고,
   표시가 실제 상태와 일치하도록 ``log.notification.interval`` 도 함께 조정하십시오.

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
    Total: 2 event(s) in the last 300 seconds

    --- Log Details ---
    Total: 2 event(s)

    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR와 WARN 이벤트는 레벨별로 별도의 통지로 전송됩니다.

.. note::
   표시할 이벤트 수가 ``log.notification.max.display.events`` 를 초과하는 경우, 상세 부분의
   시작 부분은 ``Total: N event(s) (showing M)`` 가 되고, 끝에 ``... and X more`` 가 추가됩니다.
   각 로그 메시지는 ``log.notification.max.message.length`` 를 초과하면 끝부분이 ``...`` 로
   잘리고, 상세 부분 전체가 ``log.notification.max.details.length`` 를 초과하면 이후는
   잘려나갑니다.

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

로그 통지 기능은 이벤트의 임시 보관에 ``fess_log.notification_queue`` 인덱스를 사용합니다
(인덱스 이름은 ``index.log`` 의 값(기본값 ``fess_log``)에 ``.notification_queue`` 를
추가한 것입니다). 이 인덱스는 기능의 최초 사용 시 자동으로 생성됩니다.
통지 전송 후 이벤트는 삭제되므로 일반적으로 인덱스 크기가 커지지 않습니다.

.. note::
   1회 잡 실행에서 처리되는 이벤트 수는 ``log.notification.search.size``(기본값
   1,000건)가 상한입니다. 이 상한을 초과하여 축적된 이벤트는 통지 전송 후 일괄 폐기되며,
   다음 실행 이후로 인계되지 않습니다. 짧은 시간에 대량의 로그가 발생하는 환경에서는 필요에 따라
   ``log.notification.search.size`` 를 상향하십시오.

문제 해결
=========

통지가 전송되지 않음
--------------------

1. **활성화 확인**

   관리 화면의 **일반** 설정에서 **Log Notification** 이 활성화되어 있는지 확인합니다.

2. **통지 대상 확인**

   적어도 하나의 통지 대상(**알림 메일**, **Slack Webhook URLs**, **Google Chat Webhook URLs** 중
   하나)이 설정되어 있는지 확인합니다. 모두 미설정인 경우, 잡은
   ``No notification targets configured.`` 를 출력하고 아무것도 전송하지 않습니다.

3. **메일 서버 설정 확인**

   메일 통지를 사용하는 경우, ``fess_env.properties`` 에서 메일 서버가 올바르게
   설정되어 있는지 확인합니다.

4. **스케줄 잡 확인**

   **시스템** → **스케줄러** 에서 "Log Notification" 잡이 활성화되어 있는지 확인합니다.
   이 잡이 비활성화되어 있으면 통지가 전송되지 않습니다.

5. **로그 확인**

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
