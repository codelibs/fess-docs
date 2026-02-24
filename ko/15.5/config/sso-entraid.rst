=====================================
Microsoft Entra ID를 이용한 SSO 설정
=====================================

개요
====

|Fess| 에서는 Microsoft Entra ID（구 Azure AD）를 사용한 싱글 사인온（SSO）인증을 지원합니다.
Entra ID 인증을 사용하면 Microsoft 365 환경의 사용자 정보 및 그룹 정보를 |Fess| 의 역할 기반 검색과 연동할 수 있습니다.

Entra ID 인증의 동작 방식
--------------------------

Entra ID 인증에서는 |Fess| 가 OAuth 2.0/OpenID Connect의 클라이언트로 동작하여 Microsoft Entra ID와 연동하여 인증을 수행합니다.

1. 사용자가 |Fess| 의 SSO 엔드포인트（``/sso/``）에 접근
2. |Fess| 가 Entra ID의 인가 엔드포인트로 리다이렉트
3. 사용자가 Entra ID에서 인증（Microsoft 로그인）
4. Entra ID가 인가 코드를 |Fess| 로 리다이렉트
5. |Fess| 가 인가 코드를 사용하여 액세스 토큰을 취득
6. |Fess| 가 Microsoft Graph API를 사용하여 사용자의 그룹 및 역할 정보를 취득
7. 사용자를 로그인하고 그룹 정보를 역할 기반 검색에 적용

역할 기반 검색과의 연동에 대해서는 :doc:`security-role` 을 참조하십시오.

전제조건
========

Entra ID 인증을 설정하기 전에 다음 전제조건을 확인하십시오.

- |Fess| 15.5 이상이 설치되어 있을 것
- Microsoft Entra ID（Azure AD）테넌트를 사용할 수 있을 것
- |Fess| 가 HTTPS로 접근 가능할 것（본번 환경에서는 필수）
- Entra ID 측에서 애플리케이션을 등록할 수 있는 권한이 있을 것

기본 설정
========

SSO 기능 활성화
---------------

Entra ID 인증을 활성화하려면 ``app/WEB-INF/conf/system.properties`` 에 다음 설정을 추가합니다.

::

    sso.type=entraid

필수 설정
--------

Entra ID에서 취득한 정보를 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``entraid.tenant``
     - 테넌트 ID（예: ``xxx.onmicrosoft.com``）
     - （필수）
   * - ``entraid.client.id``
     - 애플리케이션（클라이언트）ID
     - （필수）
   * - ``entraid.client.secret``
     - 클라이언트 시크릿 값
     - （필수）
   * - ``entraid.reply.url``
     - 리다이렉트 URI（콜백 URL）
     - 요청 URL을 사용

.. note::
   ``entraid.*`` 프리픽스 대신 레거시 ``aad.*`` 프리픽스도 사용할 수 있습니다（하위 호환성）.

옵션 설정
--------------

필요에 따라 다음 설정을 추가할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``entraid.authority``
     - 인증 서버 URL
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - State 유효 기간（초）
     - ``3600``
   * - ``entraid.default.groups``
     - 기본 그룹（쉼표 구분）
     - （없음）
   * - ``entraid.default.roles``
     - 기본 역할（쉼표 구분）
     - （없음）

Entra ID 측 설정
==================

Azure Portal에서의 앱 등록
--------------------------

1. `Azure Portal <https://portal.azure.com/>`_ 에 로그인

2. **Microsoft Entra ID** 를 선택

3. 왼쪽 메뉴의 **관리** → **앱 등록** → **새 등록** 을 클릭

4. 애플리케이션을 등록:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - 설정 항목
        - 설정값
      * - 이름
        - 임의의 이름（예: Fess SSO）
      * - 지원되는 계정 유형
        - 「이 조직 디렉터리의 계정만」
      * - 플랫폼 선택
        - Web
      * - 리다이렉트 URI
        - ``https://<Fess 호스트>/sso/``

5. **등록** 을 클릭

클라이언트 시크릿 생성
------------------------------

1. 앱 세부 정보 페이지에서 **인증서 및 비밀** 을 클릭

2. **새 클라이언트 비밀** 을 클릭

3. 설명과 만료 기간을 설정하고 **추가** 를 클릭

4. 생성된 **값** 을 복사하여 저장（이 값은 다시 표시되지 않습니다）

.. warning::
   클라이언트 시크릿 값은 생성 직후에만 표시됩니다.
   다른 화면으로 이동하기 전에 반드시 기록해 두십시오.

API 접근 권한 설정
---------------------

1. 왼쪽 메뉴의 **API 권한** 을 클릭

2. **권한 추가** 를 클릭

3. **Microsoft Graph** 를 선택

4. **위임된 권한** 을 선택

5. 다음 접근 권한을 추가:

   - ``Group.Read.All`` - 사용자의 그룹 정보를 취득하기 위해 필요

6. **권한 추가** 를 클릭

7. **「<테넌트 이름>에 관리자 동의 부여」** 를 클릭

.. note::
   관리자 동의는 테넌트 관리자 권한이 필요합니다.

취득하는 정보
------------

다음 정보를 Fess 설정에 사용합니다.

- **애플리케이션（클라이언트）ID**: 개요 페이지의 「애플리케이션 (클라이언트) ID」
- **테넌트 ID**: 개요 페이지의 「디렉터리 (테넌트) ID」또는 ``xxx.onmicrosoft.com`` 형식
- **클라이언트 시크릿 값**: 인증서 및 비밀에서 생성한 값

그룹 및 역할 매핑
==========================

Entra ID 인증에서는 Microsoft Graph API를 사용하여 사용자가 소속된 그룹 및 역할을 자동으로 취득합니다.
취득한 그룹 ID 및 그룹 이름은 |Fess| 의 역할 기반 검색에 사용할 수 있습니다.

중첩 그룹
--------------------

|Fess| 는 사용자가 직접 소속된 그룹뿐만 아니라 해당 그룹이 소속된 상위 그룹（중첩 그룹）도 재귀적으로 취득합니다.
이 처리는 로그인 후 비동기로 실행되므로 로그인 시간에 대한 영향을 최소화합니다.

기본 그룹 설정
------------------------

모든 Entra ID 사용자에게 공통 그룹을 부여하는 경우:

::

    entraid.default.groups=authenticated_users,entra_users

설정 예
======

최소 구성（검증 환경용）
------------------------

다음은 검증 환경에서 동작을 확인하기 위한 최소한의 설정 예입니다.

::

    # SSO 활성화
    sso.type=entraid

    # Entra ID 설정
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

권장 구성（본번 환경용）
------------------------

다음은 본번 환경에서 사용할 때의 권장 설정 예입니다.

::

    # SSO 활성화
    sso.type=entraid

    # Entra ID 설정
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # 기본 그룹（옵션）
    entraid.default.groups=authenticated_users

레거시 설정（하위 호환성）
--------------------------

이전 버전과의 호환성을 위해 ``aad.*`` 프리픽스도 사용할 수 있습니다.

::

    # SSO 활성화
    sso.type=entraid

    # 레거시 설정 키
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

문제 해결
======================

자주 발생하는 문제와 해결 방법
----------------------

인증 후 Fess로 돌아올 수 없음
~~~~~~~~~~~~~~~~~~~~~~

- Azure Portal의 앱 등록에서 리다이렉트 URI가 올바르게 설정되어 있는지 확인하십시오
- ``entraid.reply.url`` 의 값이 Azure Portal의 설정과 완전히 일치하는지 확인하십시오
- 프로토콜（HTTP/HTTPS）이 일치하는지 확인하십시오
- 리다이렉트 URI의 끝에 ``/`` 가 포함되어 있는지 확인하십시오

인증 오류가 발생함
~~~~~~~~~~~~~~~~~~~~

- 테넌트 ID, 클라이언트 ID, 클라이언트 시크릿이 올바르게 설정되어 있는지 확인하십시오
- 클라이언트 시크릿의 유효 기간이 만료되지 않았는지 확인하십시오
- API 접근 권한에 관리자 동의가 부여되어 있는지 확인하십시오

그룹 정보를 취득할 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``Group.Read.All`` 의 접근 권한이 부여되어 있는지 확인하십시오
- 관리자 동의가 부여되어 있는지 확인하십시오
- 사용자가 Entra ID에서 그룹에 소속되어 있는지 확인하십시오

디버그 설정
------------

문제를 조사할 때는 |Fess| 의 로그 레벨을 조정하면 Entra ID 관련 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml`` 에서 다음 로거를 추가하여 로그 레벨을 변경할 수 있습니다.

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

참고 정보
========

- :doc:`security-role` - 역할 기반 검색 설정에 대하여
- :doc:`sso-saml` - SAML 인증을 이용한 SSO 설정에 대하여
- :doc:`sso-oidc` - OpenID Connect 인증을 이용한 SSO 설정에 대하여
