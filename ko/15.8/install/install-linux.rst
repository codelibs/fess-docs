======================
Linux 설치 (상세 절차)
======================

이 페이지에서는 Linux 환경에 |Fess| 를 설치하는 절차를 설명합니다.
TAR.GZ, RPM, DEB 각 패키지 형식에 대응합니다.

.. warning::

   운영 환경에서는 내장 OpenSearch를 사용한 운영을 권장하지 않습니다.
   반드시 외부 OpenSearch 서버를 구축하시기 바랍니다.

전제 조건
=========

- :doc:`prerequisites` 에 기재된 시스템 요구사항을 충족할 것
- Java 21이 설치되어 있을 것
- OpenSearch 3.7.0을 사용 가능한 상태로 할 것(또는 신규 설치)

설치 방법 선택
==============

Linux 환경에서는 다음 설치 방법 중에서 선택할 수 있습니다:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 방식
     - 권장 환경
     - 특징
   * - TAR.GZ
     - 개발 환경, 커스터마이징이 필요한 환경
     - 임의의 디렉터리에 압축 해제 가능
   * - RPM
     - RHEL, CentOS, Fedora 계열
     - systemd를 통한 서비스 관리 가능
   * - DEB
     - Debian, Ubuntu 계열
     - systemd를 통한 서비스 관리 가능

OpenSearch 실행을 위한 시스템 설정
==================================

OpenSearch를 Linux에서 안정적으로 동작시키려면 다음 커널 매개변수 및 리소스 제한을 설정합니다.
이는 주로 TAR.GZ 버전(OpenSearch를 수동으로 설치하는 경우)에서 필요합니다.
RPM / DEB 버전에서는 OpenSearch 및 |Fess| 패키지가 systemd를 통해 파일 디스크립터 수 등을 설정하지만, ``vm.max_map_count`` 는 호스트 측 커널 설정이므로 어느 방식이든 확인하시기 바랍니다.

가상 메모리 최대 맵 수
----------------------

OpenSearch는 다수의 메모리 맵을 사용하므로 ``vm.max_map_count`` 를 ``262144`` 이상으로 설정합니다.

일시적으로 설정하는 경우::

    $ sudo sysctl -w vm.max_map_count=262144

영구적으로 설정하는 경우::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

파일 디스크립터 수
------------------

OpenSearch를 수동으로 실행하는 경우(TAR.GZ 버전)에는 OpenSearch를 실행하는 사용자의 파일 디스크립터 수 상한을 ``65535`` 이상으로 설정합니다.

``/etc/security/limits.conf`` 에 다음을 추가합니다(``opensearch`` 는 OpenSearch를 실행하는 사용자 이름으로 바꿔주세요)::

    opensearch  -  nofile  65535

.. note::

   RPM / DEB 버전에서는 systemd 서비스 정의에서 파일 디스크립터 수 상한이 설정되므로 이 설정은 필요하지 않습니다.

TAR.GZ 버전 설치
================

단계 1: OpenSearch 설치
-----------------------

1. OpenSearch 다운로드

   `Download OpenSearch <https://opensearch.org/downloads.html>`__ 에서 TAR.GZ 버전을 다운로드합니다.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.tar.gz
       $ tar -xzf opensearch-3.7.0-linux-x64.tar.gz
       $ cd opensearch-3.7.0

   .. note::

      이 예제에서는 OpenSearch 3.7.0을 사용하고 있습니다.
      |Fess| 15.8은 OpenSearch 3.7.0에 대응합니다.

2. OpenSearch 플러그인 설치

   |Fess| 가 필요로 하는 플러그인을 설치합니다.

   ::

       $ cd /path/to/opensearch-3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. important::

      플러그인 버전은 OpenSearch 버전과 일치시켜야 합니다.
      위의 예제에서는 모두 3.7.0을 지정하고 있습니다.

3. OpenSearch 설정

   ``config/opensearch.yml`` 에 다음 설정을 추가합니다.

   ::

       # 설정 동기화용 경로(절대 경로로 지정)
       configsync.config_path: /path/to/opensearch-3.7.0/data/config/

       # 보안 플러그인 비활성화(개발 환경 전용)
       plugins.security.disabled: true

   .. warning::

      **보안 관련 중요 주의사항**

      ``plugins.security.disabled: true`` 는 개발 환경이나 테스트 환경에서만 사용하십시오.
      운영 환경에서는 OpenSearch의 보안 플러그인을 활성화하고 적절한 인증·인가 설정을 수행하십시오.
      OpenSearch 2.12 이후 버전에서 보안 플러그인을 활성화하는 경우, 최초 시작 시 관리자 비밀번호(환경 변수 ``OPENSEARCH_INITIAL_ADMIN_PASSWORD``)를 설정해야 합니다.
      자세한 내용은 :doc:`security` 를 참조하십시오.

   .. tip::

      클러스터 이름 및 네트워크 설정 등 기타 설정은 환경에 맞게 조정하십시오.
      설정 예::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

   .. tip::

      OpenSearch의 힙 크기는 ``config/jvm.options`` 의 ``-Xms`` / ``-Xmx`` 로 설정합니다.
      사용 가능한 물리 메모리의 절반 이하이면서 32GB 미만을 기준으로, ``-Xms`` 와 ``-Xmx`` 에 동일한 값을 지정할 것을 권장합니다.

단계 2: Fess 설치
-----------------

1. Fess 다운로드 및 압축 해제

   `다운로드 사이트 <https://fess.codelibs.org/ko/downloads.html>`__ 에서 TAR.GZ 버전을 다운로드합니다.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.tar.gz
       $ tar -xzf fess-15.8.0.tar.gz
       $ cd fess-15.8.0

2. Fess 설정

   ``bin/fess.in.sh`` 를 편집하여 OpenSearch 연결 정보를 설정합니다.
   이 파일에는 외부 OpenSearch 클러스터에 연결하기 위한 설정이 미리 주석 처리된 상태로 준비되어 있습니다.

   ::

       $ vi bin/fess.in.sh

   파일 앞부분에 있는 다음 두 줄의 주석(``#``)을 해제합니다.

   변경 전(기본 상태)::

       # External opensearch cluster
       #SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       #FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   변경 후::

       # External opensearch cluster
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.7.0/data/config/

   .. note::

      - ``FESS_DICTIONARY_PATH`` 에는 OpenSearch의 ``opensearch.yml`` 에서 지정한 ``configsync.config_path`` 와 동일한 경로를 설정하십시오.
      - OpenSearch를 다른 호스트에서 실행하는 경우 ``SEARCH_ENGINE_HTTP_URL`` 을 적절한 호스트 이름 또는 IP 주소로 변경하십시오. 예: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``
      - 새로 ``SEARCH_ENGINE_HTTP_URL=...`` 줄을 추가하지 말고, 기존 주석 줄의 주석을 해제하여 편집하십시오.

   .. tip::

      |Fess| 의 힙 크기를 변경하려면 ``bin/fess.in.sh`` 의 ``FESS_MIN_MEM`` (기본값: ``256m``) 과 ``FESS_MAX_MEM`` (기본값: ``2g``) 을 편집하거나 환경 변수 ``FESS_HEAP_SIZE`` 를 설정합니다.

3. 설치 확인

   설정 파일이 올바르게 편집되었는지 확인합니다::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

단계 3: 시작
------------

시작 절차는 :doc:`run` 을 참조하십시오.

RPM 버전 설치
=============

RPM 버전은 Red Hat Enterprise Linux, CentOS, Fedora 등 RPM 기반 Linux 배포판에서 사용합니다.

단계 1: OpenSearch 설치
-----------------------

1. OpenSearch RPM 다운로드 및 설치

   `Download OpenSearch <https://opensearch.org/downloads.html>`__ 에서 RPM 패키지를 다운로드하여 설치합니다.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.7.0-linux-x64.rpm

   또는 리포지토리를 추가하여 설치할 수도 있습니다.
   자세한 내용은 `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__ 를 참조하십시오.

2. OpenSearch 플러그인 설치

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. OpenSearch 설정

   ``/etc/opensearch/opensearch.yml`` 에 다음 설정을 추가합니다.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   추가할 설정::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      운영 환경에서는 ``plugins.security.disabled: true`` 를 사용하지 마십시오.
      :doc:`security` 를 참조하여 적절한 보안 설정을 수행하십시오.

단계 2: Fess 설치
-----------------

1. Fess RPM 설치

   `다운로드 사이트 <https://fess.codelibs.org/ko/downloads.html>`__ 에서 RPM 패키지를 다운로드하여 설치합니다.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.rpm
       $ sudo rpm -ivh fess-15.8.0.rpm

2. Fess 설정

   RPM 버전에서는 환경 변수 설정 파일 ``/etc/sysconfig/fess`` 를 편집합니다.
   이 파일은 패키지 업그레이드 시에도 유지됩니다(``/usr/share/fess/bin/fess.in.sh`` 는 업그레이드 시 덮어써지므로 직접 편집하지 마십시오).

   ::

       $ sudo vi /etc/sysconfig/fess

   OpenSearch 연결 정보를 설정합니다. 기본값은 다음과 같습니다. 필요에 따라 변경하십시오::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      ``FESS_DICTIONARY_PATH`` 는 ``opensearch.yml`` 의 ``configsync.config_path`` 와 동일한 경로를 지정하십시오.

3. 서비스 등록 및 활성화

   systemd를 사용하여 서비스를 활성화합니다(RHEL 8 이상, CentOS 8 이상에서는 systemd가 표준입니다)::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      |Fess| 서비스는 OpenSearch 서비스에 의존하므로 OpenSearch를 먼저 시작해야 합니다.

   .. note::

      systemd를 사용하지 않는 기존 환경에서는 ``chkconfig`` 로 |Fess| 를 등록할 수 있습니다::

          $ sudo /sbin/chkconfig --add fess

단계 3: 시작
------------

시작 절차는 :doc:`run` 을 참조하십시오.

DEB 버전 설치
=============

DEB 버전은 Debian, Ubuntu 등 DEB 기반 Linux 배포판에서 사용합니다.

단계 1: OpenSearch 설치
-----------------------

1. OpenSearch DEB 다운로드 및 설치

   `Download OpenSearch <https://opensearch.org/downloads.html>`__ 에서 DEB 패키지를 다운로드하여 설치합니다.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.deb
       $ sudo dpkg -i opensearch-3.7.0-linux-x64.deb

   또는 리포지토리를 추가하여 설치할 수도 있습니다.
   자세한 내용은 `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__ 를 참조하십시오.

2. OpenSearch 플러그인 설치

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. OpenSearch 설정

   ``/etc/opensearch/opensearch.yml`` 에 다음 설정을 추가합니다.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   추가할 설정::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      운영 환경에서는 ``plugins.security.disabled: true`` 를 사용하지 마십시오.
      :doc:`security` 를 참조하여 적절한 보안 설정을 수행하십시오.

단계 2: Fess 설치
-----------------

1. Fess DEB 설치

   `다운로드 사이트 <https://fess.codelibs.org/ko/downloads.html>`__ 에서 DEB 패키지를 다운로드하여 설치합니다.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.deb
       $ sudo dpkg -i fess-15.8.0.deb

2. Fess 설정

   DEB 버전에서는 환경 변수 설정 파일 ``/etc/default/fess`` 를 편집합니다.
   이 파일은 패키지 업그레이드 시에도 유지됩니다(``/usr/share/fess/bin/fess.in.sh`` 는 업그레이드 시 덮어써지므로 직접 편집하지 마십시오).

   ::

       $ sudo vi /etc/default/fess

   OpenSearch 연결 정보를 설정합니다. 기본값은 다음과 같습니다. 필요에 따라 변경하십시오::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      ``FESS_DICTIONARY_PATH`` 는 ``opensearch.yml`` 의 ``configsync.config_path`` 와 동일한 경로를 지정하십시오.

3. 서비스 등록 및 활성화

   systemd를 사용하여 서비스를 활성화합니다::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      |Fess| 서비스는 OpenSearch 서비스에 의존하므로 OpenSearch를 먼저 시작해야 합니다.

단계 3: 시작
------------

시작 절차는 :doc:`run` 을 참조하십시오.

설치 후 확인
============

설치가 완료되면 다음을 확인하십시오:

1. **설정 파일 확인**

   - OpenSearch 설정 파일(opensearch.yml)
   - |Fess| 설정 파일

     - TAR.GZ 버전: ``bin/fess.in.sh``
     - RPM 버전: ``/etc/sysconfig/fess``
     - DEB 버전: ``/etc/default/fess``

2. **디렉터리 권한**

   설정에서 지정한 디렉터리(``configsync.config_path`` / ``FESS_DICTIONARY_PATH``)가 존재하며 적절한 권한이 설정되어 있는지 확인합니다.

   TAR.GZ 버전의 경우::

       $ ls -ld /path/to/opensearch-3.7.0/data/config/

   RPM/DEB 버전의 경우::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **커널 매개변수 확인**

   ::

       $ sysctl vm.max_map_count

   값이 ``262144`` 이상인지 확인합니다.

4. **Java 버전 확인**

   ::

       $ java -version

   Java 21 이상이 설치되어 있는지 확인합니다.

다음 단계
=========

설치가 완료되면 다음 문서를 참조하십시오:

- :doc:`run` - |Fess| 시작 및 초기 설정
- :doc:`security` - 운영 환경의 보안 설정
- :doc:`troubleshooting` - 문제 해결

자주 묻는 질문
==============

Q: OpenSearch 버전은 다른 버전에서도 작동합니까?
------------------------------------------------

A: |Fess| 는 특정 버전의 OpenSearch에 의존합니다.
플러그인 호환성을 보장하기 위해 권장 버전(3.7.0)을 사용할 것을 강력히 권장합니다.
다른 버전을 사용하는 경우 플러그인 버전도 적절히 조정해야 합니다.

Q: 여러 Fess 인스턴스에서 동일한 OpenSearch를 공유할 수 있습니까?
-----------------------------------------------------------------

A: 가능하지만 권장하지 않습니다. 각 Fess 인스턴스에는 전용 OpenSearch 클러스터를 준비할 것을 권장합니다.
여러 Fess 인스턴스에서 OpenSearch를 공유하는 경우 인덱스 이름 충돌에 주의하십시오.

Q: OpenSearch를 클러스터 구성으로 만드는 방법은?
------------------------------------------------

A: OpenSearch 공식 문서 `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__ 을 참조하십시오.
클러스터 구성으로 만드는 경우 ``discovery.type: single-node`` 설정을 제거하고 적절한 클러스터 설정을 추가해야 합니다.
