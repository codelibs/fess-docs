=========================
Fess 활용 사례
=========================

소개
============

Fess는 다양한 업종과 규모의 조직에서 활용되고 있습니다.
이 페이지에서는 Fess 도입의 대표적인 활용 사례와 실용적인 예시를 소개합니다.

.. note::

   다음 예시는 Fess의 일반적인 도입 패턴을 설명하고 있습니다.
   실제 도입 사례에 대해서는 `상용 지원 <../support-services.html>`__ 으로 문의해 주세요.

----

업종별 활용 사례
===========================

제조업
-------------

**과제**: 설계 도면, 기술 문서, 품질 관리 문서가 여러 파일 서버에 분산되어 있어 필요한 정보를 찾는 데 시간이 많이 소요됩니다.

**Fess 솔루션**:

- 파일 서버의 CAD 도면, PDF 기술 문서, Office 문서를 통합 검색
- 제품 모델 번호, 도면 번호, 프로젝트 이름으로 교차 검색
- 접근 권한에 기반한 검색 결과 표시 (역할 기반 검색)

**아키텍처 예시**:

.. code-block:: text

    [파일 서버]  →  [Fess]  →  [사내 포털]
         │               │
         ├─ 도면          ├─ OpenSearch 클러스터
         ├─ 기술 문서     └─ Active Directory 연계
         └─ 품질 기록

**관련 기능**:

- `파일 서버 크롤링 <https://fess.codelibs.org/ko/15.5/config/config-filecrawl.html>`__
- `역할 기반 검색 <https://fess.codelibs.org/ko/15.5/config/config-role.html>`__
- `썸네일 표시 <https://fess.codelibs.org/ko/15.5/admin/admin-general.html>`__

금융·보험업
------------------------------

**과제**: 컴플라이언스 문서, 계약서, 사내 규정이 방대하여 감사 대응이나 문의 처리에 시간이 많이 소요됩니다.

**Fess 솔루션**:

- 사내 규정, 매뉴얼, FAQ의 교차 검색
- 계약서 및 신청서의 텍스트 검색
- 과거 문의 이력에서의 지식 검색

**보안 기능**:

- LDAP/Active Directory 연계를 통한 인증
- SAML을 통한 싱글 사인온
- 액세스 토큰을 통한 API 인증

**관련 기능**:

- `LDAP 인증 <https://fess.codelibs.org/ko/15.5/config/config-security.html>`__
- `SAML 인증 <https://fess.codelibs.org/ko/15.5/config/config-saml.html>`__

교육 기관
---------

**과제**: 연구 논문, 강의 자료, 캠퍼스 문서가 학과별 서버에 분산되어 있어 정보 공유가 어렵습니다.

**Fess 솔루션**:

- 캠퍼스 포털에서의 통합 검색
- 연구 논문 리포지토리 검색
- 강의 자료 및 실러버스 검색

**아키텍처 예시**:

- 캠퍼스 웹사이트 크롤링
- 논문 리포지토리(DSpace 등)와의 연계
- Google Drive / SharePoint의 자료 검색

**관련 기능**:

- `웹 크롤링 <https://fess.codelibs.org/ko/15.5/config/config-webcrawl.html>`__
- `Google Drive 크롤링 <https://fess.codelibs.org/ko/15.5/config/config-crawl-gsuite.html>`__

IT·소프트웨어업
-------------

**과제**: 소스 코드, 문서, 위키, 티켓 관리 시스템의 정보가 분산되어 개발 효율이 저하됩니다.

**Fess 솔루션**:

- GitHub/GitLab 리포지토리의 코드 검색
- Confluence/Wiki 페이지 검색
- Slack/Teams 메시지 검색

**개발자 기능**:

- 검색 API를 통한 기존 시스템과의 연계
- 코드 하이라이트
- 파일 형식별 필터링

**관련 기능**:

- `Git 리포지토리 크롤링 <https://fess.codelibs.org/ko/15.5/config/config-crawl-git.html>`__
- `Confluence 크롤링 <https://fess.codelibs.org/ko/15.5/config/config-crawl-atlassian.html>`__
- `Slack 크롤링 <https://fess.codelibs.org/ko/15.5/config/config-crawl-slack.html>`__

----

규모별 활용 사례
=====================

소규모 기업 (직원 100명 이하)
------------------------------------

**특징**: IT 리소스가 제한적이므로 간단한 도입과 운용을 원합니다.

**권장 구성**:

- Docker Compose를 통한 간편 배포
- 단일 서버 구성 (Fess + OpenSearch)
- 필요 메모리: 8GB 이상

**배포 절차**:

.. code-block:: bash

    # 5분 만에 배포
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**비용**:

- 소프트웨어: 무료 (오픈소스)
- 서버 비용만 발생 (클라우드 또는 온프레미스)

중견 기업 (직원 100~1000명)
----------------------------------------

**특징**: 여러 부서에서 이용하며 어느 정도의 가용성이 필요합니다.

**권장 구성**:

- Fess 서버 2대 (이중화)
- OpenSearch 클러스터 3노드
- 로드 밸런서에 의한 트래픽 분산
- Active Directory 연계

**용량 가이드라인**:

- 문서 수: 최대 500만 건
- 동시 검색 사용자 수: 최대 100명

**관련 기능**:

- `클러스터 구성 <https://fess.codelibs.org/ko/15.5/install/clustering.html>`__
- `백업 및 복원 <https://fess.codelibs.org/ko/15.5/admin/admin-backup.html>`__

대기업 (직원 1000명 이상)
----------------------------------

**특징**: 대규모 데이터, 높은 가용성, 엄격한 보안 요구 사항이 있습니다.

**권장 구성**:

- 다수의 Fess 서버 (Kubernetes에서 운용)
- OpenSearch 클러스터 (전용 노드 구성)
- 전용 크롤 서버
- 모니터링 및 로그 수집 인프라와의 연계

**확장성**:

- 문서 수: 수억 건 가능
- OpenSearch 샤드 분할에 의한 수평 확장

**엔터프라이즈 기능**:

- 부서별 라벨 관리
- 상세한 접근 로그 기록
- API를 통한 다른 시스템과의 연계

.. note::

   대규모 배포에서는 `상용 지원 <../support-services.html>`__ 의 이용을 권장합니다.

----

기술별 활용 사례
===================

사내 위키 / 지식 기반 검색
-------------------------------------

**개요**: Confluence, MediaWiki, 사내 위키를 교차 검색할 수 있습니다.

**이점**:

- 여러 위키 시스템의 통합 검색
- 업데이트 빈도에 따른 자동 크롤링
- 위키 페이지의 첨부 파일도 검색 대상

**구현 방법**:

1. Confluence Data Store 플러그인 설치
2. 관리 화면에서 연결 설정
3. 크롤 스케줄 설정 (예: 매일)

파일 서버 통합 검색
--------------------------

**개요**: Windows 파일 서버 및 NAS의 문서를 검색합니다.

**지원 프로토콜**:

- SMB/CIFS (Windows 공유 폴더)
- NFS
- 로컬 파일 시스템

**보안**:

- NTLM 인증 기반 접근 제어
- 파일 ACL이 검색 결과에 반영

**설정 포인트**:

- 전용 크롤 계정 작성
- 대량 파일의 단계적 크롤링
- 네트워크 대역폭 고려

웹사이트 검색 (사이트 검색)
----------------------------

**개요**: 공개 웹사이트에 검색 기능을 추가합니다.

**배포 방법**:

1. **JavaScript 삽입**

   Fess Site Search (FSS)를 사용하여 몇 줄의 JavaScript로 검색 상자를 추가

2. **API 연계**

   검색 API를 사용하여 커스텀 검색 UI 구축

**FSS 예시**:

.. code-block:: html

    <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      fess.src = 'https://your-fess-server/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      fess.setAttribute('fess-url', 'https://your-fess-server/json');
      document.body.appendChild(fess);
    })();
    </script>
    <fess:search></fess:search>

데이터베이스 검색
---------------

**개요**: RDB의 데이터를 검색 가능하게 합니다.

**지원 데이터베이스**:

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**활용 사례**:

- 고객 마스터 검색
- 상품 카탈로그 검색
- FAQ 데이터베이스 검색

**구현 방법**:

1. Database Data Store 플러그인 설정
2. SQL 쿼리로 크롤 대상 지정
3. 필드 매핑 설정

----

요약
=======

Fess는 유연한 설계로 다양한 업종, 규모, 활용 사례에 대응할 수 있습니다.

**도입을 검토하시는 분께**:

1. 먼저 `빠른 구축 가이드 <../quick-start.html>`__ 에서 Fess를 시험해 보세요
2. `문서 목록 <../documentation.html>`__ 에서 필요한 기능을 확인하세요
3. 프로덕션 도입에는 `상용 지원 <../support-services.html>`__ 에 상담하세요

**관련 리소스**:

- `게재 기사 목록 <../articles.html>`__ - 상세한 기술 기사
- `디스커션 포럼 <https://discuss.codelibs.org/c/fessja/>`__ - 커뮤니티 지원
- `GitHub <https://github.com/codelibs/fess>`__ - 소스 코드 및 이슈 추적
