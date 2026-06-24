====================
시작, 중지, 초기 설정
====================

이 페이지에서는 |Fess| 서버의 시작, 중지 및 초기 설정 절차에 대해 설명합니다.

.. important::

   |Fess| 를 시작하기 전에 반드시 OpenSearch를 시작하십시오.
   OpenSearch가 시작되어 있지 않은 경우 |Fess| 는 올바르게 작동하지 않습니다.

시작 방법
========

설치 방법에 따라 시작 절차가 다릅니다.

TAR.GZ 버전의 경우
-------------

OpenSearch 시작
~~~~~~~~~~~~~~~~

::

    $ cd /path/to/opensearch-3.7.0
    $ ./bin/opensearch

백그라운드에서 시작하는 경우::

    $ ./bin/opensearch -d

Fess 시작
~~~~~~~~~~

::

    $ cd /path/to/fess-15.7.0
    $ ./bin/fess

백그라운드에서 시작하는 경우::

    $ ./bin/fess -d

.. note::

   시작에는 몇 분 정도 소요될 수 있습니다.
   로그 파일(``logs/fess.log``)에서 시작 상태를 확인할 수 있습니다.

ZIP 버전의 경우(Windows)
---------------------

OpenSearch 시작
~~~~~~~~~~~~~~~~

1. OpenSearch 설치 디렉터리를 엽니다
2. ``bin`` 폴더 내의 ``opensearch.bat`` 을 더블클릭합니다

또는 명령 프롬프트에서::

    C:\> cd C:\opensearch-3.7.0
    C:\opensearch-3.7.0> bin\opensearch.bat

Fess 시작
~~~~~~~~~~

1. Fess 설치 디렉터리를 엽니다
2. ``bin`` 폴더 내의 ``fess.bat`` 을 더블클릭합니다

또는 명령 프롬프트에서::

    C:\> cd C:\fess-15.7.0
    C:\fess-15.7.0> bin\fess.bat

RPM/DEB 버전의 경우 (chkconfig)
--------------------------

OpenSearch 시작::

    $ sudo service opensearch start

Fess 시작::

    $ sudo service fess start

시작 상태 확인::

    $ sudo service fess status

RPM/DEB 버전의 경우 (systemd)
------------------------

OpenSearch 시작::

    $ sudo systemctl start opensearch.service

Fess 시작::

    $ sudo systemctl start fess.service

시작 상태 확인::

    $ sudo systemctl status fess.service

서비스 자동 시작 활성화::

    $ sudo systemctl enable opensearch.service
    $ sudo systemctl enable fess.service

Docker 버전의 경우
-------------

.. note::

   ``compose.yaml`` 및 ``compose-opensearch3.yaml`` 은 |Fess| 자체에 포함되어 있지 않습니다.
   이 파일들은 docker-fess 프로젝트(https://github.com/codelibs/docker-fess)에서 제공됩니다.
   해당 리포지터리를 취득하여 ``compose`` 디렉터리 안에서 다음 명령을 실행하십시오.

Docker Compose를 사용하여 시작::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

시작 상태 확인::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

로그 확인::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

시작 확인
==========

|Fess| 가 정상적으로 시작되었는지 확인합니다.

헬스 체크
------------

브라우저 또는 curl 명령으로 다음 URL에 액세스합니다::

    http://localhost:8080/

정상적으로 시작된 경우 Fess의 검색 화면이 표시됩니다.

명령줄에서 확인::

    $ curl -I http://localhost:8080/

``HTTP/1.1 200 OK`` 가 반환되면 정상적으로 시작된 것입니다.

로그 확인
--------

시작 로그를 확인하여 오류가 없는지 확인합니다.

TAR.GZ/ZIP 버전::

    $ tail -f /path/to/fess-15.7.0/logs/fess.log

RPM/DEB 버전::

    $ sudo tail -f /var/log/fess/fess.log

또는 journalctl 사용::

    $ sudo journalctl -u fess.service -f

Docker 버전::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

.. tip::

   시작이 정상적으로 완료되면 콘솔 및 로그에 다음과 같은 시작 완료 메시지가 표시됩니다::

       ...Booting the Tomcat: port=8080 contextPath=/
       ...
       Boot successful: url -> http://localhost:8080

브라우저에서 액세스
====================

다음 URL에 액세스하여 웹 인터페이스를 확인합니다.

검색 화면
--------

**URL**: http://localhost:8080/

Fess의 검색 화면이 표시됩니다. 초기 상태에서는 크롤 설정이 수행되지 않았기 때문에 검색 결과가 표시되지 않습니다.

관리 화면
--------

**URL**: http://localhost:8080/admin

기본 관리자 계정:

- **사용자 이름**: ``admin``
- **비밀번호**: ``admin``

.. warning::

   **보안 관련 중요 주의사항**

   기본 비밀번호는 반드시 변경하십시오.
   특히 운영 환경에서는 최초 로그인 후 즉시 비밀번호를 변경할 것을 강력히 권장합니다.

초기 설정
==============

관리 화면에 로그인한 후 다음 초기 설정을 수행합니다.

단계 1: 관리자 비밀번호 변경
-------------------------------

1. 관리 화면에 로그인(http://localhost:8080/admin)
2. 왼쪽 메뉴에서 "시스템"→"사용자" 클릭
3. ``admin`` 사용자 클릭
4. 「비밀번호」 필드에 새 비밀번호를 입력합니다
5. 「비밀번호(확인)」 필드에 같은 비밀번호를 다시 입력합니다
6. 「갱신」 버튼을 클릭합니다

.. important::

   비밀번호는 다음 조건을 충족할 것을 권장합니다:

   - 8자 이상(``password.min.length`` 로 설정된 최소 길이)
   - 영문 대문자, 영문 소문자, 숫자, 기호를 조합
   - 추측하기 어려운 것

   기본적으로 최소 길이(8자) 조건만 적용되며, 문자 종류의 조합은 강제되지 않습니다.
   ``password.require.uppercase`` 등의 설정을 사용하여 문자 종류 조건을 활성화할 수 있습니다.

단계 2: 크롤 설정 생성
---------------------------

검색 대상 사이트나 파일 시스템을 크롤링하는 설정을 생성합니다.

1. 왼쪽 메뉴에서 "크롤러"→"웹" 클릭
2. "새로 만들기" 버튼 클릭
3. 필요한 정보 입력:

   - **이름**: 크롤 설정 이름(예: 회사 웹사이트)
   - **URL**: 크롤 대상 URL(예: https://www.example.com/). 여러 URL을 지정하려면 한 줄에 하나씩 입력하십시오
   - **최대 액세스 수**: 크롤할 문서 수의 상한(선택 사항)
   - **간격**: 각 액세스 간의 대기 시간(밀리초. 기본값: ``10000``)

   .. note::

      위 항목 이외의 설정(사용자 에이전트, 스레드 수, 깊이 등)은
      미입력 시 기본값이 사용됩니다.

4. "생성" 버튼 클릭

단계 3: 크롤 실행
-----------------------

1. 왼쪽 메뉴에서 [시스템] → [스케줄러] 클릭
2. [Default Crawler] 작업을 열고 "지금 시작" 버튼을 클릭합니다
3. 크롤이 완료될 때까지 기다립니다(진행 상황은 대시보드에서 확인 가능)

단계 4: 검색 확인
-------------------

1. 검색 화면(http://localhost:8080/)에 액세스
2. 검색 키워드 입력
3. 검색 결과가 표시되는지 확인

.. note::

   크롤에는 시간이 소요될 수 있습니다.
   대규모 사이트의 경우 수 시간에서 수일이 걸릴 수도 있습니다.

기타 권장 설정
==============

운영 환경에서 운용하는 경우 다음 설정도 검토하십시오.

환경 변수를 통한 주요 설정
--------------------------

포트 번호, JVM 힙 크기, OpenSearch 연결 URL 등의 설정은 환경 변수를 통해 변경할 수 있습니다.
TAR.GZ 버전은 ``bin/fess.in.sh``, RPM 버전은 ``/etc/sysconfig/fess``, DEB 버전은 ``/etc/default/fess`` 를 편집하십시오.
변경 후 |Fess| 를 재시작할 필요가 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - 환경 변수
     - 기본값
     - 설명
   * - ``FESS_PORT``
     - ``8080``
     - |Fess| 가 수신 대기하는 HTTP 포트입니다.
   * - ``FESS_HEAP_SIZE``
     - (미설정)
     - JVM 힙 크기입니다. 최솟값과 최댓값에 동일한 값을 설정합니다. 미설정 시 최솟값 ``256m``, 최댓값 ``2g`` 가 사용되며(Windows ZIP 버전은 최댓값 ``1g``), RPM/DEB 버전은 ``512m`` 이 사용됩니다.
   * - ``SEARCH_ENGINE_HTTP_URL``
     - (미설정)
     - 접속할 OpenSearch의 URL입니다. 미설정 시 내부 기본값 ``http://localhost:9201`` 이 사용됩니다. OpenSearch를 다른 포트나 호스트에서 실행하는 경우 변경하십시오(:doc:`install-linux` 절차에서는 OpenSearch 수신 포트에 맞춰 ``http://localhost:9200`` 으로 설정합니다). RPM/DEB 버전은 패키지 환경 설정 파일에 의해 기본값으로 ``http://localhost:9200`` 이 설정됩니다.
   * - ``FESS_LOG_LEVEL``
     - ``warn``
     - |Fess| 의 로그 레벨입니다.

.. note::

   Windows ZIP 버전의 ``bin\fess.in.bat`` 은 프록시 관련 항목을 제외하고 이러한 환경 변수를 읽지 않습니다.
   값은 파일 안에 직접 기술되어 있으므로, 변경하려면 ``bin\fess.in.bat`` 을 직접 편집하십시오.

메일 서버 설정
------------------

장애 알림 등을 메일로 수신하려면 SMTP 서버와 알림 수신 주소를 설정합니다.

1. 설정 파일 ``app/WEB-INF/classes/fess_env.properties`` 의 ``mail.smtp.server.main.host.and.port`` (기본값: ``localhost:25``) 에 SMTP 서버 호스트와 포트를 지정합니다. 변경 후 |Fess| 를 재시작할 필요가 있습니다.
2. 관리 UI에서 왼쪽 메뉴의 [시스템] → [일반] 을 클릭합니다.
3. [알림 메일] 필드에 수신자 메일 주소를 입력합니다.
4. [갱신] 버튼을 클릭합니다.
5. [테스트 메일 보내기] 버튼으로 메일이 올바르게 발송되는지 확인할 수 있습니다.

시간대 설정
----------------

|Fess| 는 서버(OS / JVM)의 시간대를 사용합니다. 관리 UI에서 시간대를 변경하는 설정은 없습니다.
변경하려면 OS의 시간대 설정을 변경하거나, ``bin/fess.in.sh`` (Windows의 경우 ``bin\fess.in.bat``) 의 ``FESS_JAVA_OPTS`` 에 JVM 옵션 ``-Duser.timezone=Asia/Tokyo`` 를 추가하십시오.

로그 레벨 조정
--------------

운영 환경에서는 로그 레벨을 조정하여 디스크 사용량을 억제할 수 있습니다.

|Fess| 전체의 로그 레벨은 ``FESS_LOG_LEVEL`` 환경 변수(기본값: ``warn``)로 변경할 수 있습니다.
개별 로거를 세밀하게 제어하려면 설정 파일 ``app/WEB-INF/classes/log4j2.xml`` 을 편집하십시오.
크롤링, 서제스트, 썸네일 생성은 별도 프로세스로 실행되므로, 각각의 로그 레벨을 ``app/WEB-INF/env/{crawler,suggest,thumbnail}/resources/log4j2.xml`` 에서 개별적으로 설정하십시오.

자세한 내용은 :doc:`../admin/index` 를 참조하십시오.

중지 방법
========

TAR.GZ/ZIP 버전의 경우
-----------------

Fess 중지
~~~~~~~~~~

프로세스를 kill합니다::

    $ ps aux | grep fess
    $ kill <PID>

또는 ``Ctrl+C`` 로 콘솔에서 중지할 수 있습니다(포어그라운드에서 실행 중인 경우).

OpenSearch 중지::

    $ ps aux | grep opensearch
    $ kill <PID>

RPM/DEB 버전의 경우 (chkconfig)
--------------------------

Fess 중지::

    $ sudo service fess stop

OpenSearch 중지::

    $ sudo service opensearch stop

RPM/DEB 버전의 경우 (systemd)
------------------------

Fess 중지::

    $ sudo systemctl stop fess.service

OpenSearch 중지::

    $ sudo systemctl stop opensearch.service

Docker 버전의 경우
-------------

컨테이너 중지::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

컨테이너 중지 및 삭제::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` 명령으로 볼륨도 삭제하는 경우 ``-v`` 옵션을 추가합니다.
   이 경우 모든 데이터가 삭제되므로 주의하십시오.

재시작 방법
==========

TAR.GZ/ZIP 버전의 경우
-----------------

중지한 후 시작합니다.

RPM/DEB 버전의 경우
--------------

chkconfig::

    $ sudo service fess restart

systemd::

    $ sudo systemctl restart fess.service

Docker 버전의 경우
-------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml restart

문제 해결
====================

시작되지 않는 경우
------------

1. **OpenSearch가 시작되어 있는지 확인**

   ::

       $ curl http://localhost:9200/

   OpenSearch가 시작되어 있지 않은 경우 먼저 OpenSearch를 시작하십시오.

2. **포트 번호 충돌 확인**

   ::

       $ sudo netstat -tuln | grep 8080

   포트 8080이 이미 사용되고 있는 경우 포트 번호를 변경하십시오.

   - TAR.GZ 버전: ``bin/fess.in.sh`` 의 ``FESS_PORT`` 를 변경합니다
   - ZIP 버전(Windows): ``bin\fess.in.bat`` 에서 ``-Dfess.port=8080`` 을 직접 편집합니다
   - RPM 버전: ``/etc/sysconfig/fess`` 의 ``FESS_PORT`` 를 변경합니다
   - DEB 버전: ``/etc/default/fess`` 의 ``FESS_PORT`` 를 변경합니다

3. **로그 확인**

   오류 메시지를 확인하여 문제를 특정합니다.

4. **Java 버전 확인**

   ::

       $ java -version

   Java 21 이상이 설치되어 있는지 확인하십시오.

자세한 문제 해결에 대해서는 :doc:`troubleshooting` 을 참조하십시오.

다음 단계
==========

|Fess| 가 정상적으로 시작되면 다음 문서를 참조하여 운용을 시작하십시오:

- :doc:`../admin/index` - 크롤 설정, 검색 설정, 시스템 설정의 상세
- :doc:`security` - 운영 환경의 보안 설정
- :doc:`troubleshooting` - 일반적인 문제 및 해결 방법
- :doc:`upgrade` - 버전 업그레이드 절차
- :doc:`uninstall` - 제거 절차
