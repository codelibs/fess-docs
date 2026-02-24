==============================
OpenID Connect SSO 설정
==============================

개요
====

|Fess| 는 OpenID Connect（OIDC）를 이용한 싱글 사인온（SSO）인증을 지원합니다.
OpenID Connect는 OAuth 2.0을 기반으로 한 인증 프로토콜로, ID Token（JWT）을 사용하여 사용자 인증을 수행합니다.
OpenID Connect 인증을 사용하면 OIDC 프로바이더（OP）에서 인증된 사용자 정보를 |Fess| 에 연동할 수 있습니다.

OpenID Connect 인증 동작 방식
------------------------------

OpenID Connect 인증에서는 |Fess| 가 Relying Party（RP）로 동작하며, 외부 OpenID 프로바이더（OP）와 연계하여 인증을 수행합니다.

1. 사용자가 |Fess| 의 SSO 엔드포인트（``/sso/``）에 접근
2. |Fess| 가 OP의 인가 엔드포인트로 리다이렉트
3. 사용자가 OP에서 인증 수행
4. OP가 인가 코드를 |Fess| 에 리다이렉트
5. |Fess| 가 인가 코드를 사용하여 토큰 엔드포인트에서 ID Token 취득
6. |Fess| 가 ID Token（JWT）을 검증하고 사용자를 로그인

역할 기반 검색과의 연동에 대해서는 :doc:`security-role` 을 참조하십시오.

전제조건
========

OpenID Connect 인증을 설정하기 전에 다음 전제조건을 확인하십시오.

- |Fess| 15.5 이상이 설치되어 있을 것
- OpenID Connect 대응 프로바이더（OP）가 사용 가능할 것
- |Fess| 가 HTTPS로 접근 가능할 것（운영 환경에서는 필수）
- OP 측에서 |Fess| 를 클라이언트（RP）로 등록할 수 있는 권한이 있을 것

지원 프로바이더 예:

- Microsoft Entra ID（Azure AD）
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- 기타 OpenID Connect 대응 프로바이더

기본 설정
========

SSO 기능 활성화
---------------

OpenID Connect 인증을 활성화하려면 ``app/WEB-INF/conf/system.properties`` 에 다음 설정을 추가합니다.

::

    sso.type=oic

프로바이더 설정
----------------

OP에서 취득한 정보를 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``oic.auth.server.url``
     - 인가 엔드포인트 URL
     - （필수）
   * - ``oic.token.server.url``
     - 토큰 엔드포인트 URL
     - （필수）

.. note::
   이 URL들은 OP의 Discovery 엔드포인트（``/.well-known/openid-configuration``）에서 취득할 수 있습니다.

클라이언트 설정
----------------

OP 측에서 등록한 클라이언트 정보를 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``oic.client.id``
     - 클라이언트 ID
     - （필수）
   * - ``oic.client.secret``
     - 클라이언트 시크릿
     - （필수）
   * - ``oic.scope``
     - 요청할 스코프
     - （필수）

.. note::
   스코프에는 최소한 ``openid`` 를 포함해야 합니다.
   사용자의 이메일 주소를 취득하는 경우 ``openid email`` 을 지정합니다.

리다이렉트 URL 설정
-------------------

인증 후 콜백 URL을 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``oic.redirect.url``
     - 리다이렉트 URL（콜백 URL）
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - |Fess| 의 베이스 URL
     - ``http://localhost:8080``

.. note::
   ``oic.redirect.url`` 을 생략한 경우 ``oic.base.url`` 에서 자동으로 구성됩니다.
   운영 환경에서는 ``oic.base.url`` 에 HTTPS URL을 설정하십시오.

OP 측 설정
============

OP 측에서 |Fess| 를 클라이언트（RP）로 등록할 때 다음 정보를 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 설정 항목
     - 설정값
   * - 애플리케이션 종류
     - 웹 애플리케이션
   * - 리다이렉트 URI / 콜백 URL
     - ``https://<Fess 호스트>/sso/``
   * - 허용 스코프
     - ``openid`` 및 필요한 스코프（``email``, ``profile`` 등）

OP에서 취득하는 정보
------------------

OP의 설정 화면 또는 Discovery 엔드포인트에서 다음 정보를 취득하여 |Fess| 설정에 사용합니다.

- **인가 엔드포인트（Authorization Endpoint）**: 사용자 인증을 시작하는 URL
- **토큰 엔드포인트（Token Endpoint）**: 토큰을 취득하는 URL
- **클라이언트 ID**: OP에서 발급된 클라이언트 식별자
- **클라이언트 시크릿**: 클라이언트 인증에 사용하는 비밀 키

.. note::
   많은 OP에서 Discovery 엔드포인트（``https://<OP>/.well-known/openid-configuration``）를 통해
   인가 엔드포인트와 토큰 엔드포인트 URL을 확인할 수 있습니다.

설정 예
======

최소 구성（검증 환경용）
------------------------

다음은 검증 환경에서 동작을 확인하기 위한 최소한의 설정 예입니다.

::

    # SSO 활성화
    sso.type=oic

    # 프로바이더 설정（OP에서 취득한 값을 설정）
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # 클라이언트 설정
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # 리다이렉트 URL（검증 환경）
    oic.redirect.url=http://localhost:8080/sso/

권장 구성（운영 환경용）
------------------------

다음은 운영 환경에서 사용할 때의 권장 설정 예입니다.

::

    # SSO 활성화
    sso.type=oic

    # 프로바이더 설정
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # 클라이언트 설정
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # 베이스 URL（운영 환경에서는 HTTPS 사용）
    oic.base.url=https://fess.example.com

문제 해결
======================

자주 발생하는 문제와 해결 방법
------------------------------

인증 후 |Fess| 로 돌아올 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- OP 측의 리다이렉트 URI가 올바르게 설정되어 있는지 확인하십시오
- ``oic.redirect.url`` 또는 ``oic.base.url`` 의 값이 OP 측 설정과 일치하는지 확인하십시오
- 프로토콜（HTTP/HTTPS）이 일치하는지 확인하십시오

인증 오류가 발생함
~~~~~~~~~~~~~~~~~~

- 클라이언트 ID와 클라이언트 시크릿이 올바르게 설정되어 있는지 확인하십시오
- 스코프에 ``openid`` 가 포함되어 있는지 확인하십시오
- 인가 엔드포인트 URL과 토큰 엔드포인트 URL이 올바른지 확인하십시오

사용자 정보를 취득할 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 스코프에 필요한 권한（``email``, ``profile`` 등）이 포함되어 있는지 확인하십시오
- OP 측에서 클라이언트에 필요한 스코프가 허용되어 있는지 확인하십시오

디버그 설정
------------

문제를 조사할 때 |Fess| 의 로그 레벨을 조정하면 OpenID Connect 관련 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml`` 에서 다음 로거를 추가하여 로그 레벨을 변경할 수 있습니다.

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

참고 정보
========

- :doc:`security-role` - 역할 기반 검색 설정에 대하여
- :doc:`sso-saml` - SAML 인증에 의한 SSO 설정에 대하여
