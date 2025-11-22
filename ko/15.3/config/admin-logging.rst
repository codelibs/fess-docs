============
로그 설정
============

개요
====

|Fess| 는 시스템의 동작 상황이나 오류 정보를 기록하기 위해 여러 로그 파일을 출력합니다.
적절한 로그 설정을 통해 문제 해결이나 시스템 모니터링이 용이해집니다.

로그 파일의 종류
==================

주요 로그 파일
------------------

|Fess| 가 출력하는 주요 로그 파일은 다음과 같습니다.

.. list-table:: 로그 파일 목록
   :header-rows: 1
   :widths: 25 75

   * - 파일명
     - 내용
   * - ``fess.log``
     - 관리 화면이나 검색 화면에서의 작업 로그, 애플리케이션 오류, 시스템 이벤트
   * - ``fess_crawler.log``
     - 크롤 실행 시의 로그, 크롤 대상 URL, 취득한 문서 정보, 오류
   * - ``fess_suggest.log``
     - 제안(검색 후보) 생성 시의 로그, 인덱스 업데이트 정보
   * - ``server_?.log``
     - Tomcat 등 애플리케이션 서버의 시스템 로그
   * - ``audit.log``
     - 사용자 인증, 로그인/로그아웃, 중요한 작업의 감사 로그

로그 파일 위치
------------------

**Zip 설치의 경우:**

::

    {FESS_HOME}/logs/

**RPM/DEB 패키지의 경우:**

::

    /var/log/fess/

문제 해결 시 로그 확인
----------------------------------

문제가 발생한 경우 다음 순서로 로그를 확인하십시오.

1. **오류 유형 식별**

   - 애플리케이션 오류 → ``fess.log``
   - 크롤 오류 → ``fess_crawler.log``
   - 인증 오류 → ``audit.log``
   - 서버 오류 → ``server_?.log``

2. **최신 오류 확인**

   ::

       tail -f /var/log/fess/fess.log

3. **특정 오류 검색**

   ::

       grep -i "error" /var/log/fess/fess.log
       grep -i "exception" /var/log/fess/fess.log

4. **오류 컨텍스트 확인**

   오류 발생 전후의 로그를 확인하여 원인을 식별할 수 있습니다.

   ::

       grep -B 10 -A 10 "OutOfMemoryError" /var/log/fess/fess.log

로그 레벨 설정
================

로그 레벨이란
--------------

로그 레벨은 출력할 로그의 상세도를 제어합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 레벨
     - 설명
   * - ``FATAL``
     - 치명적인 오류(애플리케이션이 계속할 수 없음)
   * - ``ERROR``
     - 오류(기능의 일부가 작동하지 않음)
   * - ``WARN``
     - 경고(잠재적인 문제)
   * - ``INFO``
     - 정보(중요한 이벤트)
   * - ``DEBUG``
     - 디버그 정보(상세한 동작 로그)
   * - ``TRACE``
     - 추적 정보(가장 상세함)

권장 로그 레벨
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 환경
     - 권장 레벨
     - 이유
   * - 운영 환경
     - ``WARN``
     - 성능과 디스크 용량 중시
   * - 스테이징 환경
     - ``INFO``
     - 중요한 이벤트 기록
   * - 개발 환경
     - ``DEBUG``
     - 상세한 디버그 정보 필요
   * - 문제 조사 시
     - ``DEBUG`` 또는 ``TRACE``
     - 일시적으로 상세 로그 활성화

관리 화면에서 변경
------------------

가장 간단한 방법은 관리 화면에서 변경하는 것입니다.

1. 관리 화면에 로그인합니다.
2. "시스템" 메뉴에서 "전반"을 선택합니다.
3. "로그 레벨"에서 원하는 레벨을 선택합니다.
4. "업데이트" 버튼을 클릭합니다.

.. note::
   관리 화면에서의 변경은 |Fess| 재시작 후에도 유지됩니다.

설정 파일을 통한 변경
----------------------

더 상세한 로그 설정을 수행하는 경우 Log4j2의 설정 파일을 편집합니다.

설정 파일 위치
~~~~~~~~~~~~~~~~~~

- **Zip 설치**: ``app/WEB-INF/classes/log4j2.xml``
- **RPM/DEB 패키지**: ``/etc/fess/log4j2.xml``

기본 설정 예
~~~~~~~~~~~~~~

**기본 로그 레벨:**

::

    <Logger name="org.codelibs.fess" level="warn"/>

**예: DEBUG 레벨로 변경**

::

    <Logger name="org.codelibs.fess" level="debug"/>

**예: 특정 패키지의 로그 레벨 변경**

::

    <Logger name="org.codelibs.fess.crawler" level="info"/>
    <Logger name="org.codelibs.fess.ds" level="debug"/>
    <Logger name="org.codelibs.fess.app.web" level="warn"/>

.. warning::
   ``DEBUG`` 나 ``TRACE`` 레벨은 대량의 로그를 출력하므로
   운영 환경에서는 사용하지 마십시오. 디스크 용량과 성능에 영향을 줍니다.

환경 변수를 통한 설정
~~~~~~~~~~~~~~~~~~

시스템 시작 시 로그 레벨을 지정할 수도 있습니다.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dlog.level=debug"

크롤러 로그 설정
====================

크롤러 로그는 기본적으로 ``INFO`` 레벨로 출력됩니다.

관리 화면에서 설정
----------------

1. 관리 화면의 "크롤러" 메뉴에서 대상 크롤 설정을 엽니다.
2. "설정" 탭에서 "스크립트"를 선택합니다.
3. 스크립트 란에 다음을 추가합니다.

::

    logLevel("DEBUG")

설정 가능한 값:

- ``FATAL``
- ``ERROR``
- ``WARN``
- ``INFO``
- ``DEBUG``
- ``TRACE``

특정 URL 패턴만 로그 레벨 변경
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    if (url.contains("example.com")) {
        logLevel("DEBUG")
    }

크롤러 프로세스 전체의 로그 레벨 변경
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` 에서 설정:

::

    logging.level.org.codelibs.fess.crawler=DEBUG

로그 로테이션
==================

개요
----

로그 파일은 시간이 지남에 따라 비대해지므로 정기적인 로테이션(세대 관리)이 필요합니다.

Log4j2를 통한 자동 로테이션
-------------------------------

|Fess| 에서는 Log4j2의 RollingFileAppender를 사용하여 자동으로 로그 로테이션을 수행합니다.

기본 설정
~~~~~~~~~~~~~~~~

- **파일 크기**: 10MB를 초과하면 로테이션
- **보존 세대 수**: 최대 10개 파일

설정 파일 예(``log4j2.xml``):

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%i">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <SizeBasedTriggeringPolicy size="10MB"/>
        </Policies>
        <DefaultRolloverStrategy max="10"/>
    </RollingFile>

일일 로테이션 설정
~~~~~~~~~~~~~~~~~~~~~~~~

크기가 아닌 일일 로테이션하는 경우:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

압축 설정
~~~~~~~~

로테이션 시 자동으로 압축하는 경우:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}.gz">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

logrotate를 통한 로테이션
------------------------------

Linux 환경에서는 logrotate를 사용하여 로그 로테이션을 관리할 수도 있습니다.

``/etc/logrotate.d/fess`` 의 예:

::

    /var/log/fess/*.log {
        daily
        rotate 14
        compress
        delaycompress
        missingok
        notifempty
        create 0644 fess fess
        sharedscripts
        postrotate
            systemctl reload fess > /dev/null 2>&1 || true
        endscript
    }

설정 설명:

- ``daily``: 일일 로테이션
- ``rotate 14``: 14세대 보존
- ``compress``: 오래된 로그 압축
- ``delaycompress``: 1세대 전 로그는 압축하지 않음(애플리케이션이 쓰기 중일 가능성)
- ``missingok``: 로그 파일이 없어도 오류로 처리하지 않음
- ``notifempty``: 빈 로그 파일은 로테이션하지 않음
- ``create 0644 fess fess``: 새 로그 파일의 권한과 소유자

로그 모니터링
========

운영 환경에서는 로그 파일을 모니터링하여 오류를 조기에 감지하는 것을 권장합니다.

모니터링해야 할 로그 패턴
----------------------

중요한 오류 패턴
~~~~~~~~~~~~~~~~~~~~

- ``ERROR``, ``FATAL`` 레벨의 로그
- ``OutOfMemoryError``
- ``Connection refused``
- ``Timeout``
- ``Exception``
- ``circuit_breaker_exception``
- ``Too many open files``

경고해야 할 패턴
~~~~~~~~~~~~~~~~~~

- ``WARN`` 레벨의 로그가 빈번함
- ``Retrying``
- ``Slow query``
- ``Queue full``

실시간 모니터링
----------------

tail 명령으로 실시간 모니터링:

::

    tail -f /var/log/fess/fess.log | grep -i "error\|exception"

여러 로그 파일 동시 모니터링:

::

    tail -f /var/log/fess/*.log

모니터링 도구 예
--------------

**Logwatch**

로그 파일의 정기적인 분석 및 리포트.

::

    # 설치(CentOS/RHEL)
    yum install logwatch

    # 일일 리포트 전송
    logwatch --service fess --mailto admin@example.com

**Logstash + OpenSearch + OpenSearch Dashboards**

실시간 로그 분석 및 시각화.

**Fluentd**

로그 수집 및 전송.

::

    <source>
      @type tail
      path /var/log/fess/fess.log
      pos_file /var/log/fluentd/fess.log.pos
      tag fess.app
      <parse>
        @type multiline
        format_firstline /^\d{4}-\d{2}-\d{2}/
        format1 /^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?<thread>.*?)\] (?<level>\w+)\s+(?<logger>.*?) - (?<message>.*)/
      </parse>
    </source>

**Prometheus + Grafana**

메트릭 모니터링 및 알림.

알림 설정
------------

오류 감지 시 알림 예:

::

    # 간단한 메일 알림 스크립트
    tail -n 0 -f /var/log/fess/fess.log | while read line; do
        echo "$line" | grep -i "error\|fatal" && \
        echo "$line" | mail -s "Fess Error Alert" admin@example.com
    done

로그 형식
================

기본 형식
----------------------

|Fess| 의 기본 로그 형식:

::

    %d{ISO8601} [%t] %-5p %c - %m%n

각 요소의 설명:

- ``%d{ISO8601}``: 타임스탬프(ISO8601 형식)
- ``[%t]``: 스레드 이름
- ``%-5p``: 로그 레벨(5자 너비, 왼쪽 정렬)
- ``%c``: 로거 이름(패키지 이름)
- ``%m``: 메시지
- ``%n``: 줄 바꿈

사용자 정의 형식 예
----------------------

JSON 형식으로 로그 출력
~~~~~~~~~~~~~~~~~~

::

    <PatternLayout>
        <pattern>{"timestamp":"%d{ISO8601}","thread":"%t","level":"%-5p","logger":"%c","message":"%m"}%n</pattern>
    </PatternLayout>

더 상세한 정보 포함
~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c{1.} [%F:%L] - %m%n"/>

추가되는 정보:

- ``%c{1.}``: 축약된 패키지 이름
- ``%F``: 파일 이름
- ``%L``: 행 번호

성능에 대한 영향
======================

로그 출력은 디스크 I/O와 성능에 영향을 줍니다.

모범 사례
------------------

1. **운영 환경에서는 WARN 레벨 이상 사용**

   불필요한 상세 로그를 출력하지 않도록 합니다.

2. **로그 파일의 정기적인 정리**

   오래된 로그 파일을 삭제하거나 압축합니다.

3. **비동기 로그 출력 사용**

   Log4j2의 비동기 어펜더를 사용하여 로그 출력의 오버헤드를 줄입니다.

   ::

       <Async name="AsyncFile">
           <AppenderRef ref="FessFile"/>
       </Async>

4. **적절한 디스크 용량 확보**

   로그 파일용 충분한 디스크 용량을 확보합니다.

5. **로그 레벨의 적절한 선택**

   환경에 맞는 로그 레벨을 설정합니다.

성능 측정
------------------

로그 출력의 영향을 측정:

::

    # 로그 출력량 확인
    du -sh /var/log/fess/

    # 1시간당 로그 증가량
    watch -n 3600 'du -sh /var/log/fess/'

문제 해결
======================

로그가 출력되지 않음
------------------

**원인과 대책:**

1. **로그 디렉터리 권한**

   ::

       ls -ld /var/log/fess/
       # 필요시 권한 변경
       sudo chown -R fess:fess /var/log/fess/
       sudo chmod 755 /var/log/fess/

2. **디스크 용량**

   ::

       df -h /var/log
       # 용량 부족 시 오래된 로그 삭제
       find /var/log/fess/ -name "*.log.*" -mtime +30 -delete

3. **Log4j2 설정 파일**

   ::

       # 설정 파일 구문 검사
       xmllint --noout /etc/fess/log4j2.xml

4. **SELinux 확인**

   ::

       # SELinux가 활성화된 경우
       getenforce
       # 필요시 컨텍스트 설정
       restorecon -R /var/log/fess/

로그 파일이 너무 커짐
------------------------------

1. **로그 레벨 조정**

   ``WARN`` 이상으로 설정하십시오.

2. **로그 로테이션 설정 확인**

   ::

       # log4j2.xml 설정 확인
       grep -A 5 "RollingFile" /etc/fess/log4j2.xml

3. **불필요한 로그 출력 비활성화**

   ::

       # 특정 패키지의 로그 억제
       <Logger name="org.apache.http" level="error"/>

4. **일시적인 대처**

   ::

       # 오래된 로그 파일 압축
       gzip /var/log/fess/fess.log.[1-9]

       # 오래된 로그 파일 삭제
       find /var/log/fess/ -name "*.log.*" -mtime +7 -delete

특정 로그를 찾을 수 없음
------------------------

1. **로그 레벨 확인**

   로그 레벨이 너무 낮으면 출력되지 않습니다.

   ::

       grep "org.codelibs.fess" /etc/fess/log4j2.xml

2. **로그 파일 경로 확인**

   ::

       # 실제 로그 출력 대상 확인
       ps aux | grep fess
       lsof -p <PID> | grep log

3. **타임스탬프 확인**

   시스템 시각이 올바른지 확인하십시오.

   ::

       date
       timedatectl status

4. **로그 버퍼링**

   로그가 즉시 기록되지 않을 수 있습니다.

   ::

       # 로그 강제 플러시
       systemctl reload fess

로그에 문자 깨짐 발생
------------------------

1. **인코딩 설정**

   ``log4j2.xml`` 에서 문자 인코딩을 지정:

   ::

       <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n" charset="UTF-8"/>

2. **환경 변수 설정**

   ::

       export LANG=ko_KR.UTF-8
       export LC_ALL=ko_KR.UTF-8

참고 정보
========

- :doc:`setup-memory` - 메모리 설정
- :doc:`crawler-advanced` - 크롤러 고급 설정
- :doc:`admin-index-backup` - 인덱스 백업
- `Log4j2 Documentation <https://logging.apache.org/log4j/2.x/>`_
