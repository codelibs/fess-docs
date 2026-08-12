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
6. 사용자가 로그인
7. 백그라운드에서 |Fess| 가 Microsoft Graph API를 사용하여 사용자의 그룹 및 역할 정보를 취득하고, 완료되면 역할 기반 검색에 적용

.. note::
   |Fess| 15.8 이상에서는 인가 엔드포인트에 ``response_mode=query`` 를 요청하므로, 4번의 인가
   응답은 GET으로 반환됩니다. 15.7 이전에는 크로스 사이트 POST로 반환되었고, |Fess| 의 기본값인
   ``tomcat.sameSiteCookies = lax`` 에서는 세션 쿠키가 전송되지 않기 때문에
   ``tomcat.sameSiteCookies = none`` 으로 변경하는 우회 방법이 필요했습니다.
   이 우회 방법을 위해서만 ``none`` 을 설정했다면 기본값으로 되돌릴 수 있습니다.

역할 기반 검색과의 연동에 대해서는 :doc:`security-role` 을 참조하십시오.

전제조건
========

Entra ID 인증을 설정하기 전에 다음 전제조건을 확인하십시오.

- |Fess| 15.8 이상이 설치되어 있을 것
- Microsoft Entra ID（Azure AD）테넌트를 사용할 수 있을 것
- |Fess| 가 HTTPS로 접근 가능할 것（운영 환경에서는 필수）
- Entra ID 측에서 애플리케이션을 등록할 수 있는 권한이 있을 것

기본 설정
=========

SSO 기능 활성화
---------------

Entra ID 인증을 활성화하려면 ``app/WEB-INF/conf/system.properties`` 에 다음 설정을 추가합니다.

::

    sso.type=entraid

필수 설정
---------

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
   * - ``entraid.response.mode``
     - 인가 응답을 받는 방식. ``query`` 또는 ``form_post`` 를 지정합니다.
     - ``query``
   * - ``entraid.default.groups``
     - 기본 그룹（쉼표 구분）
     - （없음）
   * - ``entraid.default.roles``
     - 기본 역할（쉼표 구분）
     - （없음）
   * - ``entraid.permission.fields``
     - 권한 값으로 추가로 사용할 그룹/역할 필드（쉼표 구분）. 그룹/역할의 ID（GUID）는 항상 권한으로 사용되며, 여기서 지정한 필드（예: ``mail``）의 값이 추가됩니다.
     - ``mail``
   * - ``entraid.use.ds``
     - 도메인 서비스 연동. ``true`` 인 경우, ``name@domain`` 형식의 권한 값에서 도메인 부분을 제거한 로컬 부분（``name``）도 권한으로 추가합니다.
     - ``true``

.. note::

   그룹/역할의 ID（GUID）는 항상 권한으로 사용되지만, ``mail`` 값을 가지는 것은 메일이 활성화된
   그룹뿐입니다. Microsoft 365 그룹은 메일이 활성화되어 있으므로 그룹 이름도 권한으로 등록됩니다.
   반면 **보안 그룹은 메일이 활성화되어 있지 않아, 기본값 그대로면 GUID만 권한이 됩니다**.
   파일 시스템의 액세스 권한을 보안 그룹 이름으로 지정한 경우 권한이 일치하지 않아 검색 결과에
   나타나지 않습니다.

   이 경우 모든 그룹이 가지고 있는 ``displayName`` 을 추가하십시오.

   .. code-block:: properties

      entraid.permission.fields=mail,displayName

   ``displayName`` 은 도메인으로 한정되지 않고 고유하지도 않기 때문에 기본값에 포함되어 있지
   않습니다. 예를 들어 Entra ID에 ``Administrators`` 라는 이름의 그룹이 있으면, Windows 기본 제공
   그룹 ``Administrators`` 를 지정한 문서에도 일치합니다. 추가하기 전에 기존 액세스 권한에서
   사용 중인 이름과 충돌하지 않는지 확인하십시오.

.. note::
   기본값인 ``query`` 에서는 인가 코드가 콜백 URL의 쿼리 문자열에 포함됩니다.
   ``form_post`` 를 지정하면 인가 코드가 URL에 나타나지 않으므로 브라우저 기록이나 프런트엔드
   프록시・WAF의 액세스 로그에도 남지 않습니다. 다만 ``form_post`` 는 콜백이 크로스 사이트
   POST가 되므로 ``tomcat.sameSiteCookies = none`` 이 필요합니다. 설정하지 않으면 세션 쿠키가
   전송되지 않아 로그인에 실패하므로, 대부분의 환경에서는 기본값 그대로 사용하십시오.
   그 외의 값을 지정한 경우에는 경고를 출력하고 ``query`` 로 처리합니다.

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

   - ``User.Read`` - 로그인한 사용자의 소속 그룹（``/me/memberOf``）을 취득하기 위해 필요. 앱 등록 생성 시 기본으로 부여됩니다
   - ``GroupMember.Read.All`` - 그룹 이름 등 그룹 속성의 취득과 중첩된 그룹의 해결에 필요

6. **권한 추가** 를 클릭

7. **「<테넌트 이름>에 관리자 동의 부여」** 를 클릭

.. note::
   관리자 동의는 테넌트 관리자 권한이 필요합니다.

.. note::
   ``GroupMember.Read.All`` 대신 ``Group.Read.All`` 이나 ``Directory.Read.All`` 을 부여해도
   그룹 속성의 취득과 중첩된 그룹의 해결은 동작합니다. 다만 ``/me/memberOf`` 는
   ``Group.Read.All`` 로는 인가되지 않으므로 어느 경우에도 ``User.Read`` 는 필요합니다.

.. note::
   |Fess| 는 토큰 취득 시 ``https://graph.microsoft.com/.default`` 스코프를 요청합니다.
   15.8 이상에서는 인가 엔드포인트에도 ``openid profile offline_access https://graph.microsoft.com/.default``
   를 요청하여 동일한 범위의 동의를 요구합니다.
   이는 앱 등록에서 구성 및 동의된 모든 접근 권한이 사용됨을 의미합니다.
   따라서 그룹 정보를 취득하려면 위의 접근 권한을 앱 등록에 추가하고
   관리자 동의를 부여해야 합니다.

취득하는 정보
-------------

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
직접 소속된 그룹의 취득과 상위 그룹의 탐색은 모두 로그인 후 동일한 백그라운드 작업으로 실행되므로, 로그인 자체가 Microsoft Graph로 인해 지연되는 일은 없습니다.
상위 그룹 탐색은 일정 계층 수까지를 대상으로 하며, 취득 결과는 일정 시간 동안 캐시됩니다.
이 백그라운드 작업이 완료되면 사용자의 권한이 재계산됩니다.

기본 그룹 설정
------------------------

모든 Entra ID 사용자에게 공통 그룹을 부여하는 경우:

::

    entraid.default.groups=authenticated_users,entra_users

설정 예
=======

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

권장 구성（운영 환경용）
------------------------

다음은 운영 환경에서 사용할 때의 권장 설정 예입니다.

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
각 ``entraid.*`` 프로퍼티가 설정되지 않은 경우, 대응하는 ``aad.*`` 프로퍼티의 값이 사용됩니다.
또한 ``sso.type=aad`` 도 ``sso.type=entraid`` 와 동등하게 처리됩니다.

::

    # SSO 활성화（sso.type=aad 도 사용 가능）
    sso.type=entraid

    # 레거시 설정 키
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

문제 해결
======================

자주 발생하는 문제와 해결 방법
------------------------------

인증 후 Fess로 돌아올 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Azure Portal의 앱 등록에서 리다이렉트 URI가 올바르게 설정되어 있는지 확인하십시오
- ``entraid.reply.url`` 의 값이 Azure Portal의 설정과 완전히 일치하는지 확인하십시오
- 프로토콜（HTTP/HTTPS）이 일치하는지 확인하십시오
- 리다이렉트 URI의 끝에 ``/`` 가 포함되어 있는지 확인하십시오
- ``entraid.response.mode`` 에 ``form_post`` 를 지정한 경우에는 ``tomcat.sameSiteCookies = none`` 이 설정되어 있는지 확인하십시오. 설정되어 있지 않으면 콜백 시 세션 쿠키가 전송되지 않아 로그인 화면으로 되돌아가는 동작이 반복됩니다

인증 오류가 발생함
~~~~~~~~~~~~~~~~~~~~

- 테넌트 ID, 클라이언트 ID, 클라이언트 시크릿이 올바르게 설정되어 있는지 확인하십시오
- 클라이언트 시크릿의 유효 기간이 만료되지 않았는지 확인하십시오
- API 접근 권한에 관리자 동의가 부여되어 있는지 확인하십시오

그룹 정보를 취득할 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``User.Read`` 와 ``GroupMember.Read.All`` 의 접근 권한이 부여되어 있는지 확인하십시오
  （``GroupMember.Read.All`` 은 ``Group.Read.All`` 이나 ``Directory.Read.All`` 로 대체할 수 있지만, ``/me/memberOf`` 에는 ``User.Read`` 가 필요합니다）
- 관리자 동의가 부여되어 있는지 확인하십시오
- 사용자가 Entra ID에서 그룹에 소속되어 있는지 확인하십시오
- 중첩된 상위 그룹을 해결할 수 없는 경우에는 ``Not allowed to read the parent groups of ...`` 경고가 로그에 출력됩니다. 이 경우에는 ``GroupMember.Read.All`` 을 부여하십시오
- |Fess| 는 로그인이 완료된 후 백그라운드에서 사용자의 그룹·역할 소속을 해결하므로, 로그인 자체가 Microsoft Graph의 응답을 기다리는 일은 없습니다. 해결이 완료될 때까지 사용자에게는 그룹·역할에 연결된 권한만 없는 상태이며（사용자 본인의 사용자 수준 권한과 ``entraid.default.groups`` 및 ``entraid.default.roles`` 에 설정한 그룹·역할은 첫 요청부터 유지됩니다）, 이 때문에 원래 참조할 수 있는 문서가 일시적으로 검색 결과에 나오지 않을 수 있습니다. 해결이 진행되는 동안에는 검색 화면에 그 사실을 알리는 메시지가 표시됩니다
- 해결에 실패하면 검색 화면에 그 사실을 알리는 메시지가 표시되며, 반복해서 발생하는 경우 관리자에게 문의하도록 안내합니다. 다만 실패가 최종적인 것이 되지는 않습니다. 액세스 토큰이 갱신될 때마다 해결이 다시 실행되며, 그 후 성공하면 메시지는 사라지고 없던 권한도 복구됩니다. 바로 다시 시도하려면 일단 로그아웃한 후 다시 로그인하십시오（로그인한 상태로 SSO 로그인 URL을 열어도 검색 화면으로 리다이렉트될 뿐입니다）

디버그 설정
------------

문제를 조사할 때는 |Fess| 의 로그 레벨을 조정하면 Entra ID 관련 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml`` 에서 다음 로거를 추가하여 로그 레벨을 변경할 수 있습니다.

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

참고 정보
=========

- :doc:`security-role` - 역할 기반 검색 설정에 대하여
- :doc:`sso-saml` - SAML 인증을 이용한 SSO 설정에 대하여
- :doc:`sso-oidc` - OpenID Connect 인증을 이용한 SSO 설정에 대하여
