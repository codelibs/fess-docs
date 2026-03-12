==================================
Salesforce 커넥터
==================================

개요
====

Salesforce 커넥터는 Salesforce의 오브젝트(표준 오브젝트, 사용자 정의 오브젝트)에서 데이터를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-salesforce`` 플러그인이 필요합니다.

지원 오브젝트
================

- **표준 오브젝트**: Account, Contact, Lead, Opportunity, Case, Solution 등
- **사용자 정의 오브젝트**: 직접 생성한 오브젝트
- **Knowledge 아티클**: Salesforce Knowledge

전제조건
========

1. 플러그인 설치가 필요합니다
2. Salesforce Connected App 생성이 필요합니다
3. OAuth 인증 설정이 필요합니다
4. 오브젝트에 대한 읽기 액세스 권한이 필요합니다

플러그인 설치
------------------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다.

또는 자세한 내용은 :doc:`../../admin/plugin-guide` 를 참조하세요.

설정 방법
========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - Salesforce CRM
   * - 핸들러 이름
     - SalesforceDataStore
   * - 활성화
     - 켬

파라미터 설정
----------------

OAuth Token 인증(권장):

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

OAuth Password 인증:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignoreError=true

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``base_url``
     - 예
     - Salesforce URL(프로덕션: ``https://login.salesforce.com``, Sandbox: ``https://test.salesforce.com``)
   * - ``auth_type``
     - 예
     - 인증 타입(``oauth_token`` 또는 ``oauth_password``)
   * - ``username``
     - 예
     - Salesforce 사용자명
   * - ``client_id``
     - 예
     - Connected App의 Consumer Key
   * - ``private_key``
     - oauth_token인 경우
     - 비밀 키(PEM 형식, 줄바꿈은 ``\n``)
   * - ``client_secret``
     - oauth_password인 경우
     - Connected App의 Consumer Secret
   * - ``security_token``
     - oauth_password인 경우
     - 사용자의 보안 토큰
   * - ``number_of_threads``
     - 아니오
     - 병렬 처리 스레드 수(기본값: 1)
   * - ``ignoreError``
     - 아니오
     - 오류 시에도 처리 계속(기본값: true)
   * - ``custom``
     - 아니오
     - 사용자 정의 오브젝트명(쉼표 구분)
   * - ``<오브젝트>.title``
     - 아니오
     - 제목에 사용할 필드명
   * - ``<오브젝트>.contents``
     - 아니오
     - 콘텐츠에 사용할 필드명(쉼표 구분)

스크립트 설정
--------------

::

    title="[" + object.type + "] " + object.title
    digest=object.description
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``object.type``
     - 오브젝트 타입(예: Case, User, Solution)
   * - ``object.title``
     - 오브젝트 이름
   * - ``object.description``
     - 오브젝트 설명
   * - ``object.content``
     - 오브젝트 텍스트 콘텐츠
   * - ``object.id``
     - 오브젝트 ID
   * - ``object.content_length``
     - 콘텐츠 길이
   * - ``object.created``
     - 생성 일시
   * - ``object.last_modified``
     - 최종 수정 일시
   * - ``object.url``
     - 오브젝트 URL
   * - ``object.thumbnail``
     - 썸네일 URL

Salesforce Connected App 설정
====================================

1. Connected App 생성
-----------------------------

Salesforce Setup에서:

1. "앱 관리자" 열기
2. "새 Connected App" 클릭
3. 기본 정보 입력:

   - Connected App 이름: Fess Crawler
   - API 이름: Fess_Crawler
   - 연락처 이메일: your-email@example.com

4. "API 활성화(OAuth 설정 활성화)" 체크

2. OAuth Token 인증 설정(권장)
--------------------------------

OAuth 설정에서:

1. "디지털 서명 사용" 체크
2. 인증서 업로드(후술 절차로 생성)
3. 선택한 OAuth 범위:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. "저장" 클릭
5. Consumer Key 복사

인증서 생성:

::

    # 비밀 키 생성
    openssl genrsa -out private_key.pem 2048

    # 인증서 생성
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # 비밀 키 확인
    cat private_key.pem

인증서(certificate.crt)를 Salesforce에 업로드하고,
비밀 키(private_key.pem) 내용을 파라미터에 설정합니다.

3. OAuth Password 인증 설정
---------------------------

OAuth 설정에서:

1. 콜백 URL: ``https://localhost`` (사용하지 않지만 필수)
2. 선택한 OAuth 범위:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. "저장" 클릭
4. Consumer Key와 Consumer Secret 복사

보안 토큰 취득:

1. Salesforce에서 개인 설정 열기
2. "내 보안 토큰 재설정" 클릭
3. 이메일로 전송된 토큰 복사

4. Connected App 승인
-----------------------------

"관리" → "Connected App 관리"에서:

1. 생성한 Connected App 선택
2. "편집" 클릭
3. "허용된 사용자"를 "관리자가 승인한 사용자만 사전 승인"으로 변경
4. 프로필 또는 권한 세트 할당

사용자 정의 오브젝트 설정
==========================

사용자 정의 오브젝트 크롤링
------------------------------

파라미터에서 ``custom``에 사용자 정의 오브젝트명 지정:

::

    custom=FessObj,CustomProduct,ProjectTask

각 오브젝트의 필드 매핑:

::

    FessObj.title=Name
    FessObj.contents=Name,Description__c,Notes__c

    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c,Specifications__c

    ProjectTask.title=Task_Name__c
    ProjectTask.contents=Task_Name__c,Task_Description__c

필드 매핑 규칙
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``<오브젝트명>.title`` - 제목에 사용할 필드(단일 필드)
- ``<오브젝트명>.contents`` - 콘텐츠에 사용할 필드(쉼표 구분으로 복수 지정 가능)

사용 예
======

표준 오브젝트 크롤링
--------------------------

파라미터:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true

스크립트:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

사용자 정의 오브젝트 크롤링
------------------------------

파라미터:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignoreError=true
    custom=Product__c,Contract__c
    Product__c.title=Name
    Product__c.contents=Name,Description__c,Category__c
    Contract__c.title=Contract_Name__c
    Contract__c.contents=Contract_Name__c,Terms__c,Notes__c

스크립트:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Sandbox 환경 크롤링
---------------------

파라미터:

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignoreError=true

스크립트:

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

문제 해결
======================

인증 오류
----------

**증상**: ``Authentication failed`` 또는 ``invalid_grant``

**확인 사항**:

1. OAuth Token 인증인 경우:

   - Consumer Key가 올바른지 확인
   - 비밀 키가 올바르게 복사되었는지 확인(줄바꿈이 ``\n``으로 되어 있는지)
   - 인증서가 Salesforce에 업로드되어 있는지 확인
   - 사용자명이 올바른지 확인

2. OAuth Password 인증인 경우:

   - Consumer Key와 Consumer Secret이 올바른지 확인
   - 보안 토큰이 올바른지 확인
   - 비밀번호와 보안 토큰을 연결하지 않았는지 확인(별도로 설정)

3. 공통:

   - base_url이 올바른지 확인(프로덕션 환경인지 Sandbox 환경인지)
   - Connected App이 승인되었는지 확인

오브젝트를 가져올 수 없음
--------------------------

**증상**: 크롤링은 성공하지만 오브젝트가 0개

**확인 사항**:

1. 사용자에게 오브젝트에 대한 읽기 권한이 있는지 확인
2. 사용자 정의 오브젝트인 경우 오브젝트명이 올바른지 확인(API 이름)
3. 필드 매핑이 올바른지 확인
4. 로그에서 오류 메시지 확인

사용자 정의 오브젝트 이름
--------------------------

사용자 정의 오브젝트의 API 이름 확인:

1. Salesforce Setup에서 "오브젝트 관리자" 열기
2. 사용자 정의 오브젝트 선택
3. "API 이름" 복사(보통 ``__c``로 끝남)

예:

- 표시 레이블: Product
- API 이름: Product__c (이것을 사용)

필드명 확인
------------------

사용자 정의 필드의 API 이름 확인:

1. 오브젝트의 "필드 및 관계" 열기
2. 사용자 정의 필드 선택
3. "필드명" 복사(보통 ``__c``로 끝남)

예:

- 필드 표시 레이블: Product Description
- 필드명: Product_Description__c (이것을 사용)

API 속도 제한
-------------

**증상**: ``REQUEST_LIMIT_EXCEEDED``

**해결 방법**:

1. ``number_of_threads``를 줄임(1로 설정)
2. 크롤링 간격을 늘림
3. Salesforce API 사용량 확인
4. 필요 시 API 제한 추가 구매

대량의 데이터가 있는 경우
----------------------

**증상**: 크롤링에 시간이 오래 걸리거나 타임아웃됨

**해결 방법**:

1. 오브젝트를 여러 데이터 스토어로 분할
2. ``number_of_threads`` 조정(2~4 정도)
3. 크롤링 스케줄 분산
4. 필요한 필드만 매핑

비밀 키 형식 오류
--------------------------

**증상**: ``Invalid private key format``

**해결 방법**:

비밀 키 줄바꿈이 올바르게 ``\n``으로 되어 있는지 확인:

::

    # 올바른 형식
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # 잘못된 형식(실제 줄바꿈이 포함되어 있음)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
