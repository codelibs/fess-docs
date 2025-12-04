====================
설치 방법 선택
====================

이 페이지에서는 |Fess| 의 설치 방법 개요에 대해 설명합니다.
사용자의 환경에 맞는 적절한 설치 방법을 선택하시기 바랍니다.

.. warning::

   **운영 환경의 중요한 주의사항**

   운영 환경이나 부하 검증 등에서는 내장 OpenSearch를 사용한 운영을 권장하지 않습니다.
   반드시 외부 OpenSearch 서버를 구축하시기 바랍니다.

전제 조건 확인
============

설치를 시작하기 전에 시스템 요구사항을 확인하시기 바랍니다.

자세한 내용은 :doc:`prerequisites` 를 참조하십시오.

설치 방법 비교
====================

|Fess| 는 다음과 같은 방법으로 설치할 수 있습니다. 사용 환경 및 용도에 따라 선택하십시오.

.. list-table::
   :header-rows: 1
   :widths: 15 25 30 30

   * - 방법
     - 대상 OS
     - 권장 용도
     - 상세 문서
   * - Docker
     - Linux, Windows, macOS
     - 개발·평가 환경, 신속한 설정
     - :doc:`install-docker`
   * - TAR.GZ
     - Linux, macOS
     - 커스터마이징이 필요한 환경
     - :doc:`install-linux`
   * - RPM
     - RHEL, CentOS, Fedora
     - 운영 환경(RPM 기반)
     - :doc:`install-linux`
   * - DEB
     - Debian, Ubuntu
     - 운영 환경(DEB 기반)
     - :doc:`install-linux`
   * - ZIP
     - Windows
     - Windows 환경의 개발·운영
     - :doc:`install-windows`

각 설치 방법의 특징
======================

Docker 버전
--------

**장점:**

- 가장 신속하게 설정 가능
- 의존성 관리 불필요
- 개발 환경 구축에 최적
- 컨테이너 시작·중지가 용이

**단점:**

- Docker 지식 필요

**권장 환경:** 개발 환경, 평가 환경, POC, 운영 환경

상세: :doc:`install-docker`

Linux 패키지 버전 (TAR.GZ/RPM/DEB)
---------------------------------

**장점:**

- 네이티브 환경에서의 높은 성능
- 시스템 서비스로 관리 가능(RPM/DEB)
- 세밀한 커스터마이징 가능

**단점:**

- Java 및 OpenSearch 수동 설치 필요
- 설정에 시간이 소요됨

**권장 환경:** 운영 환경, 커스터마이징이 필요한 환경

상세: :doc:`install-linux`

Windows 버전 (ZIP)
---------------

**장점:**

- Windows 네이티브 환경에서 작동
- 설치 프로그램 불필요

**단점:**

- Java 및 OpenSearch 수동 설치 필요
- 설정에 시간이 소요됨

**권장 환경:** Windows 환경의 개발·평가, Windows Server 운영

상세: :doc:`install-windows`

설치의 기본 절차
========================

모든 설치 방법에서 기본 절차는 동일합니다.

1. **시스템 요구사항 확인**

   :doc:`prerequisites` 를 참조하여 시스템 요구사항을 충족하는지 확인합니다.

2. **소프트웨어 다운로드**

   `다운로드 사이트 <https://fess.codelibs.org/ko/downloads.html>`__ 에서 |Fess| 를 다운로드합니다.

   Docker 버전의 경우 Docker Compose 파일을 가져옵니다.

3. **OpenSearch 설정**

   Docker 버전 이외의 경우 OpenSearch를 별도로 설정해야 합니다.

   - OpenSearch 3.3.2 설치
   - 필수 플러그인 설치
   - 설정 파일 편집

4. **Fess 설정**

   - Fess 설치
   - 설정 파일 편집(OpenSearch 연결 정보 등)

5. **시작 및 확인**

   - 서비스 시작
   - 브라우저에서 액세스하여 동작 확인

   자세한 내용은 :doc:`run` 을 참조하십시오.

필요한 구성요소
==================

|Fess| 를 실행하려면 다음 구성요소가 필요합니다.

Fess 본체
--------

전문 검색 시스템의 본체입니다. 웹 인터페이스, 크롤러, 인덱서 등의 기능을 제공합니다.

OpenSearch
----------

검색 엔진으로 OpenSearch를 사용합니다.

- **지원 버전**: OpenSearch 3.3.2
- **필수 플러그인**:

  - opensearch-analysis-fess
  - opensearch-analysis-extension
  - opensearch-minhash
  - opensearch-configsync

.. important::

   OpenSearch 버전과 플러그인 버전을 일치시켜야 합니다.
   버전 불일치는 시작 오류 또는 예기치 않은 동작의 원인이 됩니다.

Java (Docker 버전 제외)
-------------------

TAR.GZ/ZIP/RPM/DEB 버전의 경우 Java 21 이상이 필요합니다.

- 권장: `Eclipse Temurin <https://adoptium.net/temurin>`__
- OpenJDK 21 이상도 사용 가능

.. note::

   Docker 버전의 경우 Java는 Docker 이미지에 포함되어 있으므로 별도로 설치할 필요가 없습니다.

다음 단계
==========

시스템 요구사항을 확인하고 적절한 설치 방법을 선택하십시오.

1. :doc:`prerequisites` - 시스템 요구사항 확인
2. 설치 방법 선택:

   - :doc:`install-docker` - Docker 설치
   - :doc:`install-linux` - Linux 설치
   - :doc:`install-windows` - Windows 설치

3. :doc:`run` - |Fess| 시작 및 초기 설정
4. :doc:`security` - 보안 설정(운영 환경의 경우)

자주 묻는 질문
==========

Q: OpenSearch는 필수입니까?
--------------------------

A: 예, 필수입니다. |Fess| 는 검색 엔진으로 OpenSearch를 사용합니다.
Docker 버전의 경우 자동으로 설정되지만, 기타 방법에서는 수동으로 설치해야 합니다.

Q: 이전 버전에서 업그레이드할 수 있습니까?
----------------------------------------------

A: 예, 가능합니다. 자세한 내용은 :doc:`upgrade` 를 참조하십시오.

Q: 여러 서버로 구성할 수 있습니까?
---------------------------------

A: 예, 가능합니다. Fess와 OpenSearch를 별도의 서버에서 실행할 수 있습니다.
또한 OpenSearch를 클러스터 구성으로 만들어 고가용성과 성능 향상을 도모할 수 있습니다.

다운로드
==========

|Fess| 및 관련 구성요소는 다음에서 다운로드할 수 있습니다:

- **Fess**: `다운로드 사이트 <https://fess.codelibs.org/ko/downloads.html>`__
- **OpenSearch**: `Download OpenSearch <https://opensearch.org/downloads.html>`__
- **Java (Adoptium)**: `Adoptium <https://adoptium.net/>`__
- **Docker**: `Get Docker <https://docs.docker.com/get-docker/>`__

버전 정보
============

이 문서는 다음 버전을 대상으로 합니다:

- **Fess**: 15.4.0
- **OpenSearch**: 3.3.2
- **Java**: 21 이상
- **Docker**: 20.10 이상
- **Docker Compose**: 2.0 이상

이전 버전의 문서에 대해서는 각 버전의 문서를 참조하십시오.
