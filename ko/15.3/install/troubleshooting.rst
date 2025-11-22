==================
문제 해결
==================

이 페이지에서는 |Fess| 의 설치, 시작, 운용 시 자주 발생하는 문제와 해결 방법에 대해 설명합니다.

설치 시 문제
==================

Java가 인식되지 않음
-----------------

**증상:**

::

    -bash: java: command not found

또는::

    'java' is not recognized as an internal or external command

**원인:**

Java가 설치되어 있지 않거나 PATH 환경 변수가 올바르게 설정되어 있지 않음.

**해결 방법:**

1. Java가 설치되어 있는지 확인::

       $ which java
       $ java -version

2. 설치되어 있지 않은 경우 Java 21 설치::

       # Ubuntu/Debian
       $ sudo apt-get update
       $ sudo apt-get install openjdk-21-jdk

       # RHEL/CentOS
       $ sudo yum install java-21-openjdk

3. JAVA_HOME 환경 변수 설정::

       $ export JAVA_HOME=/path/to/java
       $ export PATH=$JAVA_HOME/bin:$PATH

   영구적으로 설정하는 경우 ``~/.bashrc`` 또는 ``/etc/profile`` 에 추가합니다.

플러그인 설치 실패
-------------------------------

**증상:**

::

    ERROR: Plugin installation failed

**원인:**

- 네트워크 연결 문제
- 플러그인 버전이 OpenSearch 버전과 일치하지 않음
- 권한 문제

**해결 방법:**

1. OpenSearch 버전 확인::

       $ /path/to/opensearch/bin/opensearch --version

2. 플러그인 버전을 OpenSearch 버전에 맞춤::

       $ /path/to/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2

3. 권한 확인::

       $ sudo /path/to/opensearch/bin/opensearch-plugin install ...

4. 프록시를 통해 설치하는 경우::

       $ export ES_JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
       $ /path/to/opensearch/bin/opensearch-plugin install ...

시작 시 문제
==========

Fess가 시작되지 않음
---------------

**증상:**

Fess 시작 명령을 실행해도 오류가 발생하거나 즉시 종료됨.

**확인 항목:**

1. **OpenSearch가 시작되어 있는지 확인**::

       $ curl http://localhost:9200/

   정상인 경우 JSON 응답이 반환됩니다.

2. **포트 번호 충돌 확인**::

       $ sudo netstat -tuln | grep 8080

   포트 8080이 이미 사용되고 있는 경우 설정 파일에서 포트 번호를 변경하십시오.

3. **로그 파일 확인**::

       $ tail -f /path/to/fess/logs/fess.log

   오류 메시지에서 원인을 특정합니다.

4. **Java 버전 확인**::

       $ java -version

   Java 21 이상이 설치되어 있는지 확인하십시오.

5. **메모리 부족 확인**::

       $ free -h

   메모리가 부족한 경우 힙 크기를 조정하거나 시스템 메모리를 증설하십시오.

OpenSearch가 시작되지 않음
---------------------

**증상:**

::

    ERROR: bootstrap checks failed

**원인:**

시스템 설정이 OpenSearch 요구사항을 충족하지 못함.

**해결 방법:**

1. **vm.max_map_count 설정**::

       $ sudo sysctl -w vm.max_map_count=262144

   영구적으로 설정::

       $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
       $ sudo sysctl -p

2. **파일 디스크립터 상한 증가**::

       $ sudo vi /etc/security/limits.conf

   다음을 추가::

       opensearch  -  nofile  65535
       opensearch  -  nproc   4096

3. **메모리 잠금 설정**::

       $ sudo vi /etc/security/limits.conf

   다음을 추가::

       opensearch  -  memlock  unlimited

4. OpenSearch 재시작::

       $ sudo systemctl restart opensearch

포트 번호 충돌
--------------

**증상:**

::

    Address already in use

**해결 방법:**

1. 사용 중인 포트 확인::

       $ sudo netstat -tuln | grep 8080
       $ sudo lsof -i :8080

2. 사용 중인 프로세스 중지, 또는 Fess의 포트 번호 변경

   설정 파일 (``system.properties``)에서 포트 번호 변경::

       server.port=9080

연결 문제
========

Fess가 OpenSearch에 연결할 수 없음
-------------------------------

**증상:**

로그에 다음과 같은 오류 표시::

    Connection refused
    또는
    No route to host

**해결 방법:**

1. **OpenSearch가 시작되어 있는지 확인**::

       $ curl http://localhost:9200/

2. **연결 URL 확인**

   ``fess.in.sh`` 또는 ``fess.in.bat`` 에서 설정된 URL이 올바른지 확인::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

3. **방화벽 확인**::

       $ sudo firewall-cmd --list-all

   포트 9200이 개방되어 있는지 확인합니다.

4. **네트워크 연결 확인**

   다른 호스트에서 OpenSearch를 실행하는 경우::

       $ ping opensearch-host
       $ telnet opensearch-host 9200

브라우저에서 Fess에 액세스할 수 없음
----------------------------------

**증상:**

브라우저에서 http://localhost:8080/ 에 액세스할 수 없음.

**해결 방법:**

1. **Fess가 시작되어 있는지 확인**::

       $ ps aux | grep fess

2. **로컬호스트에서 액세스 시도**::

       $ curl http://localhost:8080/

3. **방화벽 확인**::

       $ sudo firewall-cmd --list-all

   포트 8080이 개방되어 있는지 확인합니다.

4. **다른 호스트에서 액세스하는 경우**

   Fess가 로컬호스트 이외에서 수신 대기하고 있는지 확인::

       $ netstat -tuln | grep 8080

   ``127.0.0.1:8080`` 인 경우 ``0.0.0.0:8080`` 또는 특정 IP 주소에서 수신 대기하도록 설정을 변경합니다.

성능 문제
==================

검색이 느림
--------

**원인:**

- 인덱스 크기가 큼
- 메모리 부족
- 디스크 I/O가 느림
- 쿼리가 복잡함

**해결 방법:**

1. **힙 크기 증가**

   ``fess.in.sh`` 편집::

       FESS_HEAP_SIZE=4g

   OpenSearch의 힙 크기도 조정::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **인덱스 최적화**

   관리 화면에서 "시스템"→"스케줄러"로 정기적으로 최적화 실행합니다.

3. **SSD 사용**

   디스크 I/O가 병목인 경우 SSD로 이전합니다.

4. **캐시 활성화**

   설정 파일에서 쿼리 캐시를 활성화합니다.

크롤링이 느림
-----------

**원인:**

- 크롤 간격이 김
- 대상 사이트 응답이 느림
- 스레드 수가 적음

**해결 방법:**

1. **크롤 간격 조정**

   관리 화면에서 크롤 설정의 "간격"을 짧게 합니다(밀리초 단위).

   .. warning::

      간격을 너무 짧게 하면 대상 사이트에 부하가 걸립니다. 적절한 값을 설정하십시오.

2. **스레드 수 증가**

   설정 파일에서 크롤 스레드 수를 늘립니다::

       crawler.thread.count=10

3. **타임아웃 값 조정**

   응답이 느린 사이트의 경우 타임아웃 값을 늘립니다.

데이터 문제
==========

검색 결과가 표시되지 않음
--------------------

**원인:**

- 인덱스가 작성되지 않음
- 크롤링이 실패함
- 검색 쿼리가 잘못됨

**해결 방법:**

1. **인덱스 확인**::

       $ curl http://localhost:9200/_cat/indices?v

   |Fess| 의 인덱스가 존재하는지 확인합니다.

2. **크롤 로그 확인**

   관리 화면에서 "시스템"→"로그"에서 크롤 로그를 확인하여 오류가 없는지 조사합니다.

3. **크롤 재실행**

   관리 화면에서 "시스템"→"스케줄러"에서 "Default Crawler"를 실행합니다.

4. **검색 쿼리를 간단하게**

   먼저 간단한 키워드로 검색하여 결과가 반환되는지 확인합니다.

인덱스가 손상됨
------------------------

**증상:**

검색 시 오류 발생 또는 예기치 않은 결과 반환.

**해결 방법:**

1. **인덱스 삭제 후 재작성**

   .. warning::

      인덱스를 삭제하면 모든 검색 데이터가 손실됩니다. 반드시 백업을 취득하십시오.

   ::

       $ curl -X DELETE http://localhost:9200/fess*

2. **크롤 재실행**

   관리 화면에서 "Default Crawler"를 실행하여 인덱스를 재작성합니다.

Docker 고유 문제
===============

컨테이너가 시작되지 않음
------------------

**증상:**

``docker compose up`` 으로 컨테이너가 시작되지 않음.

**해결 방법:**

1. **로그 확인**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. **메모리 부족 확인**

   Docker에 할당된 메모리를 늘립니다(Docker Desktop 설정에서).

3. **포트 충돌 확인**::

       $ docker ps

   다른 컨테이너가 포트 8080 또는 9200을 사용하고 있지 않은지 확인합니다.

4. **Docker Compose 파일 확인**

   YAML 파일의 구문 오류가 없는지 확인합니다::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml config

컨테이너는 시작되지만 Fess에 액세스할 수 없음
----------------------------------------

**해결 방법:**

1. **컨테이너 상태 확인**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

2. **로그 확인**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs fess

3. **네트워크 설정 확인**::

       $ docker network ls
       $ docker network inspect <network_name>

Windows 고유 문제
================

경로 문제
--------

**증상:**

경로에 공백이나 한국어가 포함된 경우 오류 발생.

**해결 방법:**

경로에 공백이나 한국어를 포함하지 않은 디렉터리에 설치하십시오.

예::

    C:\opensearch  (권장)
    C:\Program Files\opensearch  (비권장)

서비스로 등록할 수 없음
------------------------

**해결 방법:**

NSSM 등의 타사 도구를 사용하여 Windows 서비스로 등록합니다.

자세한 내용은 :doc:`install-windows` 를 참조하십시오.

기타 문제
==========

로그 레벨 변경
--------------

상세한 로그를 확인하는 경우 로그 레벨을 DEBUG로 변경합니다.

``log4j2.xml`` 편집::

    <Logger name="org.codelibs.fess" level="debug"/>

데이터베이스 재설정
--------------------

설정을 재설정하는 경우 OpenSearch의 인덱스를 삭제합니다::

    $ curl -X DELETE http://localhost:9200/.fess_config*

.. warning::

   이 명령을 실행하면 모든 설정 데이터가 삭제됩니다.

지원 정보
==========

문제가 해결되지 않는 경우 다음 지원 리소스를 이용하십시오:

커뮤니티 지원
------------------

- **Issues**: https://github.com/codelibs/fess/issues

  문제를 보고할 때는 다음 정보를 포함하십시오:

  - Fess 버전
  - OpenSearch 버전
  - OS 및 버전
  - 오류 메시지(로그에서 발췌)
  - 재현 절차

- **포럼**: https://discuss.codelibs.org/

상용 지원
----------

상용 지원이 필요한 경우 N2SM, Inc.에 문의하십시오:

- **Web**: https://www.n2sm.net/

디버그 정보 수집
================

문제를 보고할 때 다음 정보를 수집해 두면 도움이 됩니다:

1. **버전 정보**::

       $ cat /path/to/fess/VERSION
       $ /path/to/opensearch/bin/opensearch --version
       $ java -version

2. **시스템 정보**::

       $ uname -a
       $ cat /etc/os-release
       $ free -h
       $ df -h

3. **로그 파일**::

       $ tar czf fess-logs.tar.gz /path/to/fess/logs/

4. **설정 파일**(기밀 정보를 삭제한 후)::

       $ tar czf fess-config.tar.gz /path/to/fess/app/WEB-INF/conf/

5. **OpenSearch 상태**::

       $ curl http://localhost:9200/_cluster/health?pretty
       $ curl http://localhost:9200/_cat/indices?v
