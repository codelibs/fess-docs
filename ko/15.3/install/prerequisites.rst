============
시스템 요구사항
============

이 페이지에서는 |Fess| 를 실행하는 데 필요한 하드웨어 및 소프트웨어 요구사항에 대해 설명합니다.

하드웨어 요구사항
==============

최소 요구사항
--------

다음은 평가 및 개발 환경의 최소 요구사항입니다:

- CPU: 2코어 이상
- 메모리: 4GB 이상
- 디스크 용량: 10GB 이상의 여유 공간

권장 사양
--------

운영 환경에서는 다음 사양을 권장합니다:

- CPU: 4코어 이상
- 메모리: 8GB 이상(인덱스 크기에 따라 증설)
- 디스크 용량:

  - 시스템 영역: 20GB 이상
  - 데이터 영역: 인덱스 크기의 3배 이상(복제본 포함)

- 네트워크: 1Gbps 이상

.. note::

   인덱스 크기가 커지거나 고빈도 크롤링을 수행하는 경우
   메모리 및 디스크 용량을 적절히 증설하시기 바랍니다.

소프트웨어 요구사항
==============

운영 체제
--------------------

|Fess| 는 다음 운영 체제에서 작동합니다:

**Linux**

- Red Hat Enterprise Linux 8 이상
- CentOS 8 이상
- Ubuntu 20.04 LTS 이상
- Debian 11 이상
- 기타 Linux 배포판(Java 21 실행 가능 환경)

**Windows**

- Windows Server 2019 이상
- Windows 10 이상

**기타**

- macOS 11 (Big Sur) 이상(개발 환경에만 권장)
- Docker 실행 가능 환경

필수 소프트웨어
--------------

설치 방법에 따라 다음 소프트웨어가 필요합니다:

TAR.GZ/ZIP/RPM/DEB 버전
~~~~~~~~~~~~~~~~~~~~

- **Java 21**: `Eclipse Temurin <https://adoptium.net/temurin>`__ 권장

  - OpenJDK 21 이상
  - Eclipse Temurin 21 이상

- **OpenSearch 3.3.2**: 운영 환경에서는 필수(내장 버전은 비권장)

  - 지원 버전: OpenSearch 3.3.2
  - 기타 버전에서는 플러그인 호환성에 주의 필요

Docker 버전
~~~~~~~~~

- **Docker**: 20.10 이상
- **Docker Compose**: 2.0 이상

네트워크 요구사항
==============

필요한 포트
----------

|Fess| 가 사용하는 주요 포트는 다음과 같습니다:

.. list-table::
   :header-rows: 1
   :widths: 15 15 50

   * - 포트
     - 프로토콜
     - 용도
   * - 8080
     - HTTP
     - |Fess| 웹 인터페이스(검색 화면·관리 화면)
   * - 9200
     - HTTP
     - OpenSearch HTTP API(|Fess| 에서 OpenSearch로의 통신)
   * - 9300
     - TCP
     - OpenSearch 트랜스포트 통신(클러스터 구성 시)

.. warning::

   운영 환경에서는 외부에서 포트 9200 및 9300에 직접 액세스하는 것을 제한할 것을 강력히 권장합니다.
   이러한 포트는 |Fess| 와 OpenSearch 간의 내부 통신에만 사용되어야 합니다.

방화벽 설정
------------------

|Fess| 를 외부에서 액세스할 수 있게 하려면 포트 8080을 개방해야 합니다.

**Linux (firewalld 사용 시)**

::

    $ sudo firewall-cmd --permanent --add-port=8080/tcp
    $ sudo firewall-cmd --reload

**Linux (iptables 사용 시)**

::

    $ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    $ sudo iptables-save

브라우저 요구사항
============

|Fess| 의 관리 화면 및 검색 화면에는 다음 브라우저를 권장합니다:

- Google Chrome(최신 버전)
- Mozilla Firefox(최신 버전)
- Microsoft Edge(최신 버전)
- Safari(최신 버전)

.. note::

   Internet Explorer는 지원되지 않습니다.

설치 전 체크리스트
====================

설치 전에 다음 항목을 확인하시기 바랍니다:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 확인 항목
     - 상태
   * - 하드웨어 요구사항을 충족하는가
     - □
   * - Java 21이 설치되어 있는가(Docker 버전 제외)
     - □
   * - Docker가 설치되어 있는가(Docker 버전)
     - □
   * - 필요한 포트를 사용할 수 있는가
     - □
   * - 방화벽 설정이 적절한가
     - □
   * - 디스크 용량에 충분한 여유가 있는가
     - □
   * - 네트워크 연결이 정상인가(외부 사이트 크롤링 수행 시)
     - □

다음 단계
==========

시스템 요구사항을 확인했으면 사용 환경에 맞는 설치 절차로 진행하시기 바랍니다:

- :doc:`install-linux` - Linux (TAR.GZ/RPM/DEB) 설치
- :doc:`install-windows` - Windows (ZIP) 설치
- :doc:`install-docker` - Docker 설치
- :doc:`install` - 설치 방법 개요
