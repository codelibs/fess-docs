==================
제거 절차
==================

이 페이지에서는 |Fess| 를 완전히 제거하는 절차에 대해 설명합니다.

.. warning::

   **제거 전 중요한 주의사항**

   - 제거하면 모든 데이터가 삭제됩니다
   - 중요한 데이터가 있는 경우 반드시 백업을 취득하십시오
   - 백업 절차에 대해서는 :doc:`upgrade` 를 참조하십시오

제거 전 준비
======================

백업 취득
----------------

필요한 데이터를 백업하십시오:

1. **설정 데이터**

   관리 화면에서 "시스템"→"백업"으로 다운로드

2. **크롤 설정**

   필요에 따라 크롤 설정을 내보내기

3. **커스터마이징한 설정 파일**

   TAR.GZ/ZIP 버전::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB 버전::

       $ sudo cp -r /etc/fess /backup/

서비스 중지
------------

제거하기 전에 모든 서비스를 중지합니다.

TAR.GZ/ZIP 버전::

    $ ps aux | grep fess
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB 버전::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 버전::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

TAR.GZ/ZIP 버전 제거
=============================

단계 1: Fess 삭제
---------------------

설치 디렉터리를 삭제합니다::

    $ rm -rf /path/to/fess-15.4.0

단계 2: OpenSearch 삭제
--------------------------

OpenSearch 설치 디렉터리를 삭제합니다::

    $ rm -rf /path/to/opensearch-3.3.2

단계 3: 데이터 디렉터리 삭제(옵션)
-------------------------------------------

기본적으로 데이터 디렉터리는 Fess의 설치 디렉터리 내에 있지만
다른 위치를 지정한 경우 해당 디렉터리도 삭제하십시오::

    $ rm -rf /path/to/data

단계 4: 로그 디렉터리 삭제(옵션)
-----------------------------------------

로그 파일을 삭제합니다::

    $ rm -rf /path/to/fess/logs
    $ rm -rf /path/to/opensearch/logs

RPM 버전 제거
======================

단계 1: Fess 제거
---------------------------------

RPM 패키지를 제거합니다::

    $ sudo rpm -e fess

단계 2: OpenSearch 제거
--------------------------------------

::

    $ sudo rpm -e opensearch

단계 3: 서비스 비활성화 및 삭제
--------------------------------

chkconfig의 경우::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

systemd의 경우::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

단계 4: 데이터 디렉터리 삭제
----------------------------------

.. warning::

   이 작업을 실행하면 모든 인덱스 데이터와 설정이 완전히 삭제됩니다.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

단계 5: 설정 파일 삭제
----------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

단계 6: 로그 파일 삭제
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

단계 7: 사용자 및 그룹 삭제(옵션)
-------------------------------------------

시스템 사용자 및 그룹을 삭제하는 경우::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

DEB 버전 제거
======================

단계 1: Fess 제거
---------------------------------

DEB 패키지를 제거합니다::

    $ sudo dpkg -r fess

설정 파일도 포함하여 완전히 삭제하는 경우::

    $ sudo dpkg -P fess

단계 2: OpenSearch 제거
--------------------------------------

::

    $ sudo dpkg -r opensearch

또는 설정 파일도 포함하여 삭제::

    $ sudo dpkg -P opensearch

단계 3: 서비스 비활성화
--------------------------

::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

단계 4: 데이터 디렉터리 삭제
----------------------------------

.. warning::

   이 작업을 실행하면 모든 인덱스 데이터와 설정이 완전히 삭제됩니다.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

단계 5: 설정 파일 삭제(dpkg -P를 사용하지 않은 경우)
---------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

단계 6: 로그 파일 삭제
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

단계 7: 사용자 및 그룹 삭제(옵션)
-------------------------------------------

시스템 사용자 및 그룹을 삭제하는 경우::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Docker 버전 제거
=========================

단계 1: 컨테이너 및 네트워크 삭제
------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

단계 2: 볼륨 삭제
--------------------------

.. warning::

   이 작업을 실행하면 모든 데이터가 완전히 삭제됩니다.

볼륨 목록 확인::

    $ docker volume ls

Fess 관련 볼륨 삭제::

    $ docker volume rm fess-es-data
    $ docker volume rm fess-data

또는 모든 볼륨을 일괄 삭제::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

단계 3: 이미지 삭제(옵션)
------------------------------------

Docker 이미지를 삭제하여 디스크 공간을 확보하는 경우::

    $ docker images | grep fess
    $ docker rmi codelibs/fess:15.4.0

    $ docker images | grep opensearch
    $ docker rmi opensearchproject/opensearch:3.3.2

단계 4: 네트워크 삭제(옵션)
----------------------------------------

Docker Compose가 생성한 네트워크를 삭제::

    $ docker network ls
    $ docker network rm <network_name>

단계 5: Compose 파일 삭제
--------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

제거 확인
====================

모든 구성요소가 삭제되었는지 확인합니다.

프로세스 확인
------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

아무것도 표시되지 않으면 프로세스가 중지되어 있습니다.

포트 확인
----------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

포트가 사용되고 있지 않은지 확인합니다.

파일 확인
------------

TAR.GZ/ZIP 버전::

    $ ls /path/to/fess-15.4.0  # 디렉터리가 존재하지 않는지 확인

RPM/DEB 버전::

    $ ls /var/lib/fess  # 디렉터리가 존재하지 않는지 확인
    $ ls /etc/fess      # 디렉터리가 존재하지 않는지 확인

Docker 버전::

    $ docker ps -a | grep fess  # 컨테이너가 존재하지 않는지 확인
    $ docker volume ls | grep fess  # 볼륨이 존재하지 않는지 확인

패키지 확인
--------------

RPM 버전::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

DEB 버전::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

아무것도 표시되지 않으면 패키지가 삭제되어 있습니다.

부분 제거
======================

Fess만 삭제하고 OpenSearch 유지
-----------------------------------

OpenSearch를 다른 애플리케이션에서도 사용하고 있는 경우 Fess만 삭제할 수 있습니다.

1. Fess 중지
2. Fess 패키지 또는 디렉터리 삭제
3. Fess 데이터 디렉터리 삭제(``/var/lib/fess`` 등)
4. OpenSearch는 삭제하지 않음

OpenSearch만 삭제하고 Fess 유지
-----------------------------------

.. warning::

   OpenSearch를 삭제하면 Fess는 작동하지 않게 됩니다.
   다른 OpenSearch 클러스터에 연결하도록 설정을 변경하십시오.

1. OpenSearch 중지
2. OpenSearch 패키지 또는 디렉터리 삭제
3. OpenSearch 데이터 디렉터리 삭제(``/var/lib/opensearch`` 등)
4. Fess 설정을 업데이트하여 다른 OpenSearch 클러스터 지정

문제 해결
====================

패키지를 삭제할 수 없음
----------------------

**증상:**

``rpm -e`` 또는 ``dpkg -r`` 에서 오류 발생.

**해결 방법:**

1. 서비스가 중지되어 있는지 확인::

       $ sudo systemctl stop fess.service

2. 종속성 확인::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. 강제 삭제(최후의 수단)::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

디렉터리를 삭제할 수 없음
------------------------

**증상:**

``rm -rf`` 로 디렉터리를 삭제할 수 없음.

**해결 방법:**

1. 권한 확인::

       $ ls -ld /path/to/directory

2. sudo로 삭제::

       $ sudo rm -rf /path/to/directory

3. 프로세스가 파일을 사용하고 있지 않은지 확인::

       $ sudo lsof | grep /path/to/directory

재설치 준비
==================

제거 후 재설치하는 경우 다음을 확인하십시오:

1. 모든 프로세스가 중지되어 있는지
2. 모든 파일과 디렉터리가 삭제되어 있는지
3. 포트 8080 및 9200이 사용되고 있지 않은지
4. 이전 설정 파일이 남아 있지 않은지

재설치 절차에 대해서는 :doc:`install` 을 참조하십시오.

다음 단계
==========

제거가 완료되면:

- 새 버전을 설치하는 경우 :doc:`install` 참조
- 데이터를 이전하는 경우 :doc:`upgrade` 참조
- 대체 검색 솔루션을 검토하는 경우 Fess 공식 사이트 참조
