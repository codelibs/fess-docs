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

   관리 화면의 "시스템" → "백업" 에서 다운로드합니다.
   이 작업으로 각종 설정(크롤 설정 포함)이나 검색 로그 등을 한꺼번에 내보낼 수 있습니다.

2. **커스터마이징한 설정 파일**

   TAR.GZ/ZIP 버전::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB 버전::

       $ sudo cp -r /etc/fess /backup/

.. note::

   |Fess| 의 인덱스나 설정의 대부분은 OpenSearch 에 저장됩니다.
   인덱스 데이터를 백업하는 경우 OpenSearch 의 스냅샷 기능을 사용합니다.
   자세한 절차는 :doc:`upgrade` 를 참조하십시오.

서비스 중지
------------

제거하기 전에 모든 서비스를 중지합니다.

TAR.GZ/ZIP 버전::

    $ ps aux | grep -E 'fess|opensearch'
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

    $ rm -rf /path/to/fess-15.7.0

단계 2: OpenSearch 삭제
--------------------------

OpenSearch 설치 디렉터리를 삭제합니다::

    $ rm -rf /path/to/opensearch-3.7.0

단계 3: 데이터 디렉터리 삭제(옵션)
-------------------------------------------

|Fess| 의 인덱스 데이터는 OpenSearch 에 저장됩니다.
기본적으로 OpenSearch 의 설치 디렉터리 내(``opensearch-3.7.0/data`` 등)에 저장되지만,
``path.data`` 로 다른 위치를 지정한 경우 해당 디렉터리도 삭제하십시오::

    $ rm -rf /path/to/data

단계 4: 로그 디렉터리 삭제(옵션)
-----------------------------------------

로그 파일을 삭제합니다::

    $ rm -rf /path/to/fess-15.7.0/logs
    $ rm -rf /path/to/opensearch-3.7.0/logs

RPM 버전 제거
======================

단계 1: Fess 제거
---------------------------------

RPM 패키지를 제거합니다::

    $ sudo rpm -e fess

.. note::

   |Fess| 패키지를 제거할 때에는 패키지의 삭제 스크립트에 의해
   ``fess`` 서비스의 중지·비활성화와 ``fess`` 사용자 및 그룹의 삭제가 자동으로 실행됩니다.
   이후 단계는 이러한 항목이 확실히 삭제되었는지 확인하기 위해, 또는
   데이터나 설정 파일을 수동으로 삭제하기 위해 실시합니다.

단계 2: OpenSearch 제거
--------------------------------------

::

    $ sudo rpm -e opensearch

단계 3: 서비스 비활성화 확인
-------------------------------

일반적으로 패키지 삭제 시 서비스가 비활성화되지만, 만약을 위해 확인·비활성화하는 경우 다음을 실행합니다.

systemd 의 경우::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

오래된 SysV init(chkconfig) 환경의 경우::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

단계 4: 데이터 디렉터리 삭제
----------------------------------

.. warning::

   이 작업을 실행하면 모든 인덱스 데이터가 완전히 삭제됩니다.

데이터 디렉터리는 패키지 제거로는 삭제되지 않으므로 수동으로 삭제합니다::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

단계 5: 설정 파일 삭제
----------------------------

설정 파일과 환경 설정 파일을 삭제합니다::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/sysconfig/fess
    $ sudo rm -rf /etc/opensearch

.. note::

   RPM 에서는 ``/etc/fess`` 내의 설정 파일이 ``.rpmsave`` 라는 이름으로 남는 경우가 있습니다.
   완전히 삭제하려면 위와 같이 수동으로 삭제하십시오.

단계 6: 로그 파일 삭제
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

단계 7: 임시 디렉터리 삭제(옵션)
-----------------------------------------

::

    $ sudo rm -rf /var/tmp/fess

단계 8: 사용자 및 그룹 삭제(옵션)
-------------------------------------------

일반적으로 패키지 삭제 시 ``fess`` 사용자·그룹은 삭제됩니다.
남아 있는 경우나 OpenSearch 용 사용자·그룹을 삭제하는 경우 다음을 실행합니다::

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

설정 파일이나 환경 설정 파일도 포함하여 완전히 삭제하는 경우 purge 를 사용합니다::

    $ sudo dpkg -P fess

.. note::

   ``dpkg -r``(remove)에서는 설정 파일(conffile)인 ``/etc/default/fess`` 등은 남습니다.
   ``dpkg -P``(purge)를 사용하면 이러한 설정 파일과 ``fess`` 사용자·그룹도 삭제됩니다.

단계 2: OpenSearch 제거
--------------------------------------

::

    $ sudo dpkg -r opensearch

또는 설정 파일도 포함하여 삭제::

    $ sudo dpkg -P opensearch

단계 3: 서비스 비활성화 확인
-------------------------------

일반적으로 패키지 삭제 시 서비스가 비활성화됩니다. 만약을 위해 확인·비활성화하는 경우 다음을 실행합니다::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

단계 4: 데이터 디렉터리 삭제
----------------------------------

.. warning::

   이 작업을 실행하면 모든 인덱스 데이터가 완전히 삭제됩니다.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

단계 5: 설정 파일 삭제(dpkg -P 를 사용하지 않은 경우)
---------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/default/fess
    $ sudo rm -rf /etc/opensearch

단계 6: 로그 파일 삭제
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

단계 7: 사용자 및 그룹 삭제(옵션)
-------------------------------------------

``dpkg -P`` 를 사용하지 않은 경우 ``fess`` 사용자·그룹이 남습니다.
삭제하는 경우 다음을 실행합니다::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Docker 버전 제거
=========================

단계 1: 컨테이너 및 네트워크 삭제
------------------------------------

컨테이너 및 Docker Compose 가 생성한 네트워크(``search_net``)를 삭제합니다::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

단계 2: 볼륨 삭제
--------------------------

.. warning::

   이 작업을 실행하면 모든 데이터가 완전히 삭제됩니다.

|Fess| 의 데이터(인덱스나 사전 등)는 OpenSearch 의 볼륨에 저장됩니다.
먼저 볼륨 목록을 확인합니다::

    $ docker volume ls

OpenSearch 관련 볼륨을 삭제합니다::

    $ docker volume rm <project>_search01_data
    $ docker volume rm <project>_search01_dictionary

.. note::

   볼륨 이름에는 Docker Compose 의 프로젝트 이름(일반적으로 Compose 파일을 배치한
   디렉터리 이름)이 접두사로 붙습니다. ``docker volume ls`` 로 실제 이름을 확인하십시오.

컨테이너와 볼륨을 일괄로 삭제하는 경우 ``down`` 에 ``-v`` 옵션을 붙입니다::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

단계 3: 이미지 삭제(옵션)
------------------------------------

Docker 이미지를 삭제하여 디스크 공간을 확보하는 경우::

    $ docker images | grep fess
    $ docker rmi ghcr.io/codelibs/fess:15.7.0
    $ docker rmi ghcr.io/codelibs/fess-opensearch:3.7.0

단계 4: Compose 파일 삭제
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

    $ ls /path/to/fess-15.7.0  # 디렉터리가 존재하지 않는지 확인

RPM/DEB 버전::

    $ ls /var/lib/fess  # 디렉터리가 존재하지 않는지 확인
    $ ls /etc/fess      # 디렉터리가 존재하지 않는지 확인

Docker 버전::

    $ docker ps -a | grep -E 'fess01|search01'  # 컨테이너가 존재하지 않는지 확인
    $ docker volume ls | grep search01           # 볼륨이 존재하지 않는지 확인

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

OpenSearch 를 다른 애플리케이션에서도 사용하고 있는 경우 Fess 만 삭제할 수 있습니다.

1. Fess 중지
2. Fess 패키지 또는 디렉터리 삭제
3. Fess 데이터 디렉터리 삭제(``/var/lib/fess`` 등)
4. OpenSearch 내에 생성된 |Fess| 의 인덱스(``fess.*``、``.fess_*`` 등) 삭제
5. OpenSearch 는 삭제하지 않음

OpenSearch만 삭제하고 Fess 유지
-----------------------------------

.. warning::

   OpenSearch 를 삭제하면 Fess 는 작동하지 않게 됩니다.
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
