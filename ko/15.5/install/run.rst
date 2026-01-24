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

    $ cd /path/to/opensearch-3.3.2
    $ ./bin/opensearch

백그라운드에서 시작하는 경우::

    $ ./bin/opensearch -d

Fess 시작
~~~~~~~~~~

::

    $ cd /path/to/fess-15.5.0
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

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch.bat

Fess 시작
~~~~~~~~~~

1. Fess 설치 디렉터리를 엽니다
2. ``bin`` 폴더 내의 ``fess.bat`` 을 더블클릭합니다

또는 명령 프롬프트에서::

    C:\> cd C:\fess-15.5.0
    C:\fess-15.5.0> bin\fess.bat

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

Docker Compose를 사용하여 시작::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

시작 상태 확인::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

로그 확인::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

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

    $ tail -f /path/to/fess-15.5.0/logs/fess.log

RPM/DEB 버전::

    $ sudo tail -f /var/log/fess/fess.log

또는 journalctl 사용::

    $ sudo journalctl -u fess.service -f

Docker 버전::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

.. tip::

   정상적으로 시작된 경우 로그에 다음과 같은 메시지가 표시됩니다::

       INFO  Boot - Fess is ready.

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
4. "비밀번호" 필드에 새 비밀번호 입력
5. "확인" 버튼 클릭
6. "업데이트" 버튼 클릭

.. important::

   비밀번호는 다음 조건을 충족할 것을 권장합니다:

   - 8자 이상
   - 영문 대문자, 영문 소문자, 숫자, 기호를 조합
   - 추측하기 어려운 것

단계 2: 크롤 설정 생성
---------------------------

검색 대상 사이트나 파일 시스템을 크롤링하는 설정을 생성합니다.

1. 왼쪽 메뉴에서 "크롤러"→"웹" 클릭
2. "새로 만들기" 버튼 클릭
3. 필요한 정보 입력:

   - **이름**: 크롤 설정 이름(예: 회사 웹사이트)
   - **URL**: 크롤 대상 URL(예: https://www.example.com/)
   - **최대 액세스 수**: 크롤할 페이지 수 상한
   - **간격**: 크롤 간격(밀리초)

4. "생성" 버튼 클릭

단계 3: 크롤 실행
-----------------------

1. 왼쪽 메뉴에서 "시스템"→"스케줄러" 클릭
2. "Default Crawler" 작업의 "지금 시작" 버튼 클릭
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

메일 서버 설정
------------------

장애 알림이나 보고서를 메일로 수신하기 위해 메일 서버 설정을 수행합니다.

1. 왼쪽 메뉴에서 "시스템"→"일반" 클릭
2. "메일" 탭 클릭
3. SMTP 서버 정보 입력
4. "업데이트" 버튼 클릭

시간대 설정
----------------

1. 왼쪽 메뉴에서 "시스템"→"일반" 클릭
2. "시간대"를 적절한 값으로 설정(예: Asia/Seoul)
3. "업데이트" 버튼 클릭

로그 레벨 조정
--------------

운영 환경에서는 로그 레벨을 조정하여 디스크 사용량을 억제할 수 있습니다.

설정 파일(``app/WEB-INF/classes/log4j2.xml``)을 편집합니다.

자세한 내용은 관리자 가이드를 참조하십시오.

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

   포트 8080이 이미 사용되고 있는 경우 설정 파일에서 포트 번호를 변경하십시오.

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

- **관리자 가이드**: 크롤 설정, 검색 설정, 시스템 설정의 상세
- :doc:`security` - 운영 환경의 보안 설정
- :doc:`troubleshooting` - 일반적인 문제 및 해결 방법
- :doc:`upgrade` - 버전 업그레이드 절차
- :doc:`uninstall` - 제거 절차
