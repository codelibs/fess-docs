============================================================
제7회 클라우드 스토리지 시대의 검색 전략 -- Google Drive·SharePoint·Box의 횡단 검색
============================================================

들어가며
========

많은 기업에서 클라우드 스토리지의 이용이 당연해졌습니다.
그러나 부서나 용도에 따라 서로 다른 클라우드 스토리지를 사용하는 경우도 적지 않습니다.
"그 파일이 Google Drive에 있는지, SharePoint에 있는지, 아니면 Box에 있는지" 고민하는 시간은 생산성을 저하시킵니다.

본 기사에서는 여러 클라우드 스토리지를 Fess로 통합하여 하나의 검색창에서 모든 클라우드상의 파일을 횡단 검색할 수 있는 환경을 구축합니다.

대상 독자
========

- 여러 클라우드 스토리지를 이용하는 조직의 관리자
- 클라우드 스토리지의 검색에 과제를 느끼는 분
- OAuth 인증의 기본 개념을 이해하고 있는 분

시나리오
========

한 기업에서 다음과 같은 클라우드 스토리지를 이용하고 있습니다.

.. list-table:: 클라우드 스토리지 이용 현황
   :header-rows: 1
   :widths: 25 35 40

   * - 서비스
     - 이용 부서
     - 주요 용도
   * - Google Drive
     - 영업부·마케팅부
     - 제안서, 보고서, 스프레드시트
   * - SharePoint Online
     - 전사 공통
     - 사내 포털, 공유 문서
   * - Box
     - 법무부·경리부
     - 계약서, 청구서, 기밀 문서

클라우드 스토리지 연동 준비
=============================

데이터스토어 플러그인 설치
------------------------------------

클라우드 스토리지의 크롤에는 다음 플러그인을 사용합니다.

- ``fess-ds-gsuite``: Google Drive / Google Workspace 크롤
- ``fess-ds-microsoft365``: SharePoint Online / OneDrive 크롤
- ``fess-ds-box``: Box 크롤

관리 화면의 [시스템] > [플러그인]에서 설치합니다.

OAuth 인증 설정
----------------

클라우드 스토리지의 API에 접근하려면 OAuth 인증 설정이 필요합니다.
각 서비스의 관리 콘솔에서 애플리케이션을 등록하고 클라이언트 ID와 시크릿을 취득합니다.

**공통 절차**

1. 각 서비스의 관리 콘솔에서 애플리케이션 등록
2. 필요한 API 스코프(권한) 설정(읽기 전용으로 충분)
3. 클라이언트 ID와 클라이언트 시크릿 취득
4. Fess의 데이터스토어 설정에 이 정보를 설정

각 서비스의 설정
=================

Google Drive 설정
--------------------

Google Drive의 파일을 검색 대상으로 합니다.

**Google Cloud Console에서의 준비**

1. Google Cloud Console에서 프로젝트 생성
2. Google Drive API 활성화
3. 서비스 계정을 생성하고 JSON 키 파일 다운로드
4. 대상 드라이브나 폴더에 서비스 계정을 공유 설정

**Fess에서의 설정**

1. [크롤러] > [데이터스토어] > [새로 만들기]
2. 핸들러명: GoogleDriveDataStore를 선택
3. 파라미터와 스크립트 설정
4. 라벨: ``google-drive`` 를 설정

**파라미터 설정 예**

.. code-block:: properties

    private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----
    private_key_id=your-private-key-id
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=

**스크립트 설정 예**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_time

서비스 계정의 JSON 키 파일에서 ``private_key``, ``private_key_id``, ``client_email`` 값을 설정합니다. Google 문서, 스프레드시트, 프레젠테이션 등 Google 고유 형식도 텍스트로 추출하여 검색할 수 있습니다.

SharePoint Online 설정
-------------------------

SharePoint Online의 문서 라이브러리를 검색 대상으로 합니다.

**Entra ID(Azure AD)에서의 준비**

1. Entra ID에서 애플리케이션 등록
2. Microsoft Graph API 권한 설정(Sites.Read.All 등)
3. 클라이언트 시크릿 또는 인증서 생성

**Fess에서의 설정**

1. [크롤러] > [데이터스토어] > [새로 만들기]
2. 핸들러명: SharePointDocLibDataStore를 선택(문서 라이브러리의 경우. 용도에 따라 SharePointListDataStore, SharePointPageDataStore, OneDriveDataStore 등도 이용 가능)
3. 파라미터와 스크립트 설정
4. 라벨: ``sharepoint`` 를 설정

**파라미터 설정 예**

.. code-block:: properties

    tenant=your-tenant-id
    client_id=your-client-id
    client_secret=your-client-secret
    site_id=your-site-id

**스크립트 설정 예**

.. code-block:: properties

    url=url
    title=name
    content=content
    last_modified=modified

``tenant``, ``client_id``, ``client_secret`` 는 Entra ID의 애플리케이션 등록에서 취득한 값을 설정합니다. ``site_id`` 를 지정하면 특정 사이트만 크롤합니다. 생략하면 접근 가능한 모든 사이트가 대상이 됩니다.

Box 설정
-----------

Box의 파일을 검색 대상으로 합니다.

**Box Developer Console에서의 준비**

1. Box Developer Console에서 커스텀 애플리케이션 생성
2. 인증 방식으로 "서버 인증(클라이언트 자격 증명 포함)"을 선택
3. 애플리케이션 승인을 관리자에게 요청

**Fess에서의 설정**

1. [크롤러] > [데이터스토어] > [새로 만들기]
2. 핸들러명: BoxDataStore를 선택
3. 파라미터와 스크립트 설정
4. 라벨: ``box`` 를 설정

**파라미터 설정 예**

.. code-block:: properties

    client_id=your-client-id
    client_secret=your-client-secret
    enterprise_id=your-enterprise-id
    public_key_id=your-public-key-id
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE...\n-----END ENCRYPTED PRIVATE KEY-----
    passphrase=your-passphrase
    supported_mimetypes=.*

**스크립트 설정 예**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_at

Box Developer Console에서 생성한 커스텀 애플리케이션의 인증 정보를 설정합니다. ``supported_mimetypes`` 로 크롤 대상 파일 형식을 정규 표현식으로 필터링할 수 있습니다.

횡단 검색 최적화
=================

차분 크롤 활용
------------------

클라우드 스토리지의 크롤에서는 매번 전체 파일을 가져오는 것이 아니라, 이전 크롤 이후에 업데이트된 파일만 가져오는 차분 크롤이 효율적입니다.

각 플러그인의 설정에서 차분 크롤 옵션이 이용 가능한지 확인하십시오.
차분 크롤을 통해 API 호출 횟수를 줄이고 크롤 시간을 단축할 수 있습니다.

검색 결과의 URL
--------------

클라우드 스토리지에서 크롤한 문서의 경우, 검색 결과의 링크를 클릭하면 각 서비스의 Web UI에서 파일이 열립니다.
이용자에게 자연스러운 동작이며 특별한 설정은 통상 불필요합니다.

운용상의 주의 사항
===============

OAuth 토큰 갱신
--------------------

클라우드 스토리지와의 연동에서는 OAuth 토큰의 유효 기간에 주의가 필요합니다.

- **Google Drive**: 서비스 계정의 경우, 토큰은 자동 갱신됩니다
- **SharePoint Online**: 클라이언트 시크릿에는 유효 기간이 있으므로 정기적으로 갱신이 필요합니다
- **Box**: 애플리케이션의 재승인이 필요한 경우가 있습니다

토큰의 유효 기간을 캘린더에 등록하여 만료로 인한 크롤 중단을 방지하십시오.

API 사용량 모니터링
----------------

클라우드 스토리지의 API에는 사용량 제한이 있습니다.
특히 대량의 파일을 크롤하는 경우에는 API 사용량을 모니터링하고, 제한에 저촉되지 않도록 크롤 설정을 조정합니다.

권한과 보안
------------------

클라우드 스토리지의 Fess용 서비스 계정에는 읽기 전용 액세스 권한을 설정하십시오.
쓰기 권한은 불필요하며, 보안 리스크를 최소화하는 원칙을 따릅니다.

또한 제5회에서 다룬 역할 기반 검색과 조합하면, 클라우드 스토리지의 권한 체계에 따른 검색 결과 제어도 실현할 수 있습니다.

정리
======

본 기사에서는 Google Drive, SharePoint Online, Box의 3가지 클라우드 스토리지를 Fess로 통합하여 횡단 검색 환경을 구축했습니다.

- 각 클라우드 스토리지의 데이터스토어 플러그인과 OAuth 인증 설정
- 라벨을 이용한 정보 출처 구분과 필터링
- 차분 크롤을 통한 검색 경험 최적화
- OAuth 토큰 관리와 API 사용량 모니터링

"어느 클라우드에 있는지"를 고민하지 않고, 필요한 파일을 즉시 찾을 수 있는 환경이 실현됩니다.

다음 회에서는 검색 품질을 지속적으로 개선하는 튜닝 사이클에 대해 다룹니다.

참고 자료
========

- `Fess 데이터스토어 설정 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess 플러그인 목록 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
