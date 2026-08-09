==========================================
Windows 통합 인증을 통한 SSO 설정
==========================================

개요
====

|Fess| 는 Windows 통합 인증(SPNEGO/Kerberos)을 사용한 싱글 사인온(SSO) 인증을 지원합니다.
Windows 통합 인증을 사용하면 Active Directory 도메인에 가입한 Windows에 로그인한 사용자는 추가 로그인 조작 없이 |Fess| 에 접근할 수 있습니다.

Windows 통합 인증의 동작 방식
------------------------------

Windows 통합 인증에서는 |Fess| 가 SPNEGO(Simple and Protected GSSAPI Negotiation Mechanism) 프로토콜을 사용하여 Kerberos 인증을 수행합니다.

1. 사용자가 Windows 도메인에 로그인
2. 사용자가 |Fess| 에 접근
3. |Fess| 가 SPNEGO 챌린지를 송신
4. 브라우저가 Kerberos 티켓을 취득하여 서버에 송신
5. |Fess| 가 티켓을 검증하고 사용자명을 취득
6. LDAP를 사용하여 사용자의 그룹 정보를 취득
7. 사용자가 로그인 상태가 되고 그룹 정보가 역할 기반 검색에 적용됨

역할 기반 검색과의 연계에 대해서는 :doc:`security-role` 을 참조하십시오.

전제조건
========

Windows 통합 인증을 설정하기 전에 다음 전제조건을 확인하십시오:

- |Fess| 15.8 이상이 설치되어 있을 것
- Active Directory(AD) 서버가 사용 가능할 것
- |Fess| 서버가 AD 도메인에서 접근 가능할 것
- AD에서 서비스 프린시펄 이름(SPN)을 설정할 권한이 있을 것
- LDAP로 사용자 정보를 취득하기 위한 계정이 있을 것

Active Directory 측 설정
=========================

서비스 프린시펄 이름(SPN) 등록
--------------------------------

|Fess| 용 SPN을 Active Directory에 등록해야 합니다.
AD 도메인에 가입한 Windows에서 명령 프롬프트를 열고 ``setspn`` 명령을 실행합니다.

::

    setspn -S HTTP/<Fess 서버의 호스트명> <AD 접속용 사용자>

예:

::

    setspn -S HTTP/fess-server.example.local svc_fess

등록을 확인하려면:

::

    setspn -L <AD 접속용 사용자>

.. note::
   SPN 등록 후 Fess 서버에서 실행한 경우에는 한 번 Windows에서 로그아웃하고 다시 로그인하십시오.

기본 설정
=========

SSO 활성화
-----------

Windows 통합 인증을 활성화하려면 ``app/WEB-INF/conf/system.properties`` 에 다음 설정을 추가합니다:

::

    sso.type=spnego

Kerberos 설정 파일
-------------------

``app/WEB-INF/classes/krb5.conf`` 를 생성하고 Kerberos 설정을 작성합니다.

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

.. note::
   ``EXAMPLE.LOCAL`` 은 사용 중인 AD 도메인 이름(대문자)으로, ``AD-SERVER.EXAMPLE.LOCAL`` 은 AD 서버의 호스트명으로 교체하십시오.

.. warning::
   ``permitted_enctypes`` 에 없는 암호화 방식으로 암호화된 서비스 티켓은 Kerberos 수신 측에서
   ``encryption type not in permitted_enctypes list`` 로 거부됩니다.
   Active Directory 는 일반적으로 AES256 서비스 티켓을 발급하므로 AES256 을 반드시 포함해야 합니다.

.. note::
   Java 17 이상에서는 RC4( ``rc4-hmac`` ), 3DES, DES 가 기본적으로 비활성화되어 있어 나열해도
   사용되지 않습니다. 위 예에서는 AES 만 지정했습니다.
   ``aes256-cts-hmac-sha384-192`` 와 ``aes128-cts-hmac-sha256-128`` 은 Windows Server 2025 가 지원하는
   AES-SHA2(RFC 8009) 암호화 방식입니다.
   RC4 키만 가진 서비스 계정은 Kerberos 인증에 사용할 수 없으므로, 비밀번호를 재설정하여
   AES 키가 생성되도록 하십시오.

로그인 설정 파일
-----------------

``app/WEB-INF/classes/auth_login.conf`` 를 생성하고 JAAS 로그인 설정을 작성합니다.

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

.. note::
   ``krb5.conf`` 와 ``auth_login.conf`` 는 ``spnego.krb5.conf`` / ``spnego.login.conf`` 로 기본 파일명이 설정되어 있지만, 파일 자체는 반드시 생성해 두어야 합니다.
   SPNEGO 는 첫 로그인 시 초기화되므로 이 파일들이 없어도 |Fess| 자체는 시작되지만 SSO 로그인이 실패합니다.

필수 설정
----------

``app/WEB-INF/conf/system.properties`` 에 다음 설정을 추가합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``spnego.preauth.username``
     - AD 접속용 사용자명
     - (필수)
   * - ``spnego.preauth.password``
     - AD 접속용 비밀번호
     - (필수)
   * - ``spnego.krb5.conf``
     - Kerberos 설정 파일 경로
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - 로그인 설정 파일 경로
     - ``auth_login.conf``

.. note::
   ``spnego.preauth.username`` 과 ``spnego.preauth.password`` 를 모두 비워 두면 서버 로그인 모듈이
   keytab 을 사용합니다.
   AD 서비스 계정의 비밀번호를 |Fess| 설정 파일에 저장하고 싶지 않은 경우, keytab 을 만들고
   ``auth_login.conf`` 의 ``spnego-server`` 를 다음과 같이 설정하십시오.

   ::

       spnego-server {
           com.sun.security.auth.module.Krb5LoginModule required
           useKeyTab=true
           keyTab="/var/lib/fess/fess.keytab"
           principal="HTTP/fess-server.example.local@EXAMPLE.LOCAL"
           storeKey=true
           isInitiator=false;
       };

옵션 설정
----------

필요에 따라 다음 설정을 추가할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``spnego.login.client.module``
     - 클라이언트 모듈명
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - 서버 모듈명
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - Basic 인증 허용
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - 비보안 Basic 인증 허용
     - ``false``
   * - ``spnego.prompt.ntlm``
     - NTLM 토큰 수신 시 Basic 인증으로 폴백
     - ``true``
   * - ``spnego.allow.localhost``
     - localhost에서의 접근 허용
     - ``false``
   * - ``spnego.allow.delegation``
     - 위임 허용
     - ``false``
   * - ``spnego.allowed.realms``
     - 서버 렘에 더해 허용할 Kerberos 렘(쉼표 구분)
     - (없음)
   * - ``spnego.logger.level``
     - SPNEGO 라이브러리 내부 로그 레벨( ``1`` =FINEST, ``2`` =FINER, ``3`` =FINE, ``4`` =CONFIG, ``6`` =WARNING, ``7`` =SEVERE. 이 외의 값( ``0``, ``5`` 포함)은 INFO로 처리)
     - (자동)

.. warning::
   ``spnego.allow.unsecure.basic=true`` 는 Base64로 인코딩된 인증 정보를 암호화되지 않은 연결로 송신할 가능성이 있습니다.
   프로덕션 환경에서는 ``false`` 로 설정하고 HTTPS를 사용할 것을 강력히 권장합니다.

.. note::
   ``spnego.prompt.ntlm=true`` (기본값)인 경우, ``spnego.allow.basic`` 도 ``true`` 이어야 합니다.
   ``spnego.allow.basic=false`` 로 설정하는 경우에는 ``spnego.prompt.ntlm=false`` 도 함께 설정하십시오.
   이 조건을 충족하지 않으면 SPNEGO 초기화 시 오류가 발생합니다.

.. note::
   ``spnego.logger.level`` 은 SPNEGO 라이브러리 내부의 로거( ``java.util.logging`` 의 ``Spnego`` 라는 이름의 로거)의 로그 레벨을 제어합니다.
   미설정 시에는 |Fess| 의 로그 레벨에 따라 자동으로 결정됩니다.

LDAP 설정
=========

Windows 통합 인증으로 로그인한 사용자의 그룹 정보를 취득하기 위해 LDAP 설정이 필요합니다.
|Fess| 관리 화면의 「시스템」→「일반」에서 LDAP 설정을 수행합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 항목
     - 설정 예
   * - LDAP URL
     - ``ldap://AD-SERVER.example.local:389``
   * - Base DN
     - ``dc=example,dc=local``
   * - Bind DN
     - ``svc_fess@example.local``
   * - 비밀번호
     - AD 접속용 사용자의 비밀번호
   * - User DN
     - ``%s@example.local``
   * - 계정 필터
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - memberOf 속성
     - ``memberOf``

브라우저 설정
=============

Windows 통합 인증을 사용하려면 클라이언트 측의 브라우저 설정이 필요합니다.

Internet Explorer / Microsoft Edge
------------------------------------

1. 인터넷 옵션 열기
2. 「보안」 탭 선택
3. 「로컬 인트라넷」 영역의 「사이트」 클릭
4. 「고급」을 클릭하고 Fess의 URL 추가
5. 「로컬 인트라넷」 영역의 「사용자 지정 수준」 클릭
6. 「사용자 인증」→「로그온」→「인트라넷 영역에서만 자동으로 로그온」 선택
7. 「고급」 탭에서 「Windows 통합 인증 사용」 체크

Google Chrome
--------------

Chrome은 일반적으로 Windows의 인터넷 옵션 설정을 사용합니다.
추가 설정이 필요한 경우 그룹 정책 또는 레지스트리에서 ``AuthServerAllowlist`` 를 설정합니다.

Mozilla Firefox
----------------

1. 주소창에 ``about:config`` 입력
2. ``network.negotiate-auth.trusted-uris`` 검색
3. Fess 서버의 URL 또는 도메인 설정(예: ``https://fess-server.example.local``)

설정 예
=======

최소 구성(검증용)
------------------

다음은 검증 환경에서의 최소 구성 예입니다.

``app/WEB-INF/conf/system.properties``:

::

    # SSO 활성화
    sso.type=spnego

    # SPNEGO 설정
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-password

``app/WEB-INF/classes/krb5.conf``:

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

``app/WEB-INF/classes/auth_login.conf``:

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

권장 구성(프로덕션용)
-----------------------

다음은 프로덕션 환경에서의 권장 구성 예입니다.

``app/WEB-INF/conf/system.properties``:

::

    # SSO 활성화
    sso.type=spnego

    # SPNEGO 설정
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # 보안 설정(프로덕션 환경)
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.prompt.ntlm=false
    spnego.allow.localhost=false

.. note::
   ``spnego.allow.basic=false`` 로 설정하는 경우에는 ``spnego.prompt.ntlm=false`` 도 반드시 설정하십시오.
   ``spnego.prompt.ntlm`` 은 기본값이 ``true`` 이므로, 이 설정을 생략하면 초기화 시 오류가 발생합니다.

문제 해결
=========

자주 발생하는 문제와 해결 방법
--------------------------------

인증 다이얼로그가 표시되는 경우
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 브라우저 설정에서 Fess 서버가 인트라넷 영역에 추가되어 있는지 확인
- 「Windows 통합 인증 사용」이 활성화되어 있는지 확인
- SPN이 올바르게 등록되어 있는지 확인( ``setspn -L <사용자명>`` )

인증 오류가 발생하는 경우
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``krb5.conf`` 의 도메인 이름(대문자)과 AD 서버명이 올바른지 확인
- ``spnego.preauth.username`` 과 ``spnego.preauth.password`` 가 올바른지 확인
- AD 서버로의 네트워크 연결 확인

그룹 정보를 취득할 수 없는 경우
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- LDAP 설정이 올바른지 확인
- Bind DN과 비밀번호가 올바른지 확인
- 사용자가 AD에서 그룹에 속해 있는지 확인

로그인이 HTTP 400을 반환한다
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

소속 그룹이 많은 사용자는 Kerberos 티켓(PAC)이 커져 ``Authorization`` 헤더가 Tomcat의 기본 상한
(8KB)을 초과하여 400이 반환될 수 있습니다.
이때 요청은 |Fess| 에 도달하지 않으므로 로그에 아무것도 기록되지 않습니다.
``tomcat_config.properties`` 에서 상한을 늘리십시오.

::

    tomcat.maxHttpHeaderSize=65536

서비스 계정 비밀번호 변경 후 인증되지 않는다
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

서버 자격 증명은 첫 로그인 시 한 번만 취득되어 프로세스가 종료될 때까지 캐시됩니다.
AD에서 서비스 계정의 비밀번호를 변경했거나 keytab을 교체한 경우에는 |Fess| 를 재시작하십시오.
``spnego.*`` 설정을 변경한 경우에도 마찬가지로 재시작이 필요합니다.

디버그 설정
-----------

문제를 조사하기 위해 SPNEGO 관련 상세 로그를 출력할 수 있습니다.

SPNEGO 라이브러리 내부의 상세 로그를 출력하려면 ``app/WEB-INF/conf/system.properties`` 에 다음을 추가합니다.
``spnego.logger.level=1`` 은 가장 상세한 로그(FINEST)를 출력합니다.

::

    spnego.logger.level=1

|Fess| 측의 SPNEGO 연계 처리( ``org.codelibs.fess.sso.spnego`` 패키지)의 상세 로그를 출력하려면 ``app/WEB-INF/classes/log4j2.xml`` 에 다음 로거를 추가합니다.

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>

.. note::
   SPNEGO 라이브러리 자체의 로그는 ``java.util.logging`` 으로 출력되므로 ``log4j2.xml`` 이 아닌 ``spnego.logger.level`` 로 제어합니다.
   |Fess| 측의 연계 처리 로그는 ``log4j2.xml`` 의 로거로 제어합니다.

참고 정보
=========

- :doc:`security-role` - 역할 기반 검색 설정
- :doc:`sso-saml` - SAML 인증을 통한 SSO 설정
- :doc:`sso-oidc` - OpenID Connect 인증을 통한 SSO 설정
- :doc:`sso-entraid` - Microsoft Entra ID를 통한 SSO 설정
