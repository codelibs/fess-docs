==================================
LDAP 통합 가이드
==================================

개요
====

|Fess| 는 LDAP(Lightweight Directory Access Protocol) 서버와의 통합을 지원하여
엔터프라이즈 환경에서의 인증과 사용자 관리를 구현할 수 있습니다.

LDAP 통합으로:

- Active Directory나 OpenLDAP에서의 사용자 인증(로그인)
- 그룹·역할 기반 접근 제어
- 관리 화면에서의 LDAP 사용자／역할／그룹 관리(옵션)

가 가능해집니다.

지원 LDAP 서버
==============

|Fess| 는 다음 LDAP 서버와의 통합을 지원합니다:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- 기타 LDAP v3 호환 서버

전제 조건
=========

- LDAP 서버로의 네트워크 접근
- LDAP 검색용 서비스 계정(바인드 DN)
- LDAP 구조(베이스 DN, 속성명 등)에 대한 이해

설정 방법 개요
==============

|Fess| 의 LDAP 설정은 용도에 따라 두 곳에서 관리됩니다.

연결·인증 설정(관리 화면 / ``system.properties``)
   LDAP 서버 연결 및 로그인 인증에 관한 설정입니다.
   관리 화면의 **「시스템 > 일반」** 페이지의 「LDAP」 섹션에서 설정할 수 있으며,
   ``app/WEB-INF/conf/system.properties`` 에 저장됩니다.

LDAP 관리 기능·동작 설정(``fess_config.properties``)
   관리 화면에서 LDAP 사용자／역할／그룹을 관리하는 기능이나,
   역할 해석 등의 동작에 관한 설정입니다. 이 설정들은
   ``app/WEB-INF/classes/fess_config.properties`` 에 정의되어 있으며,
   값을 변경하려면 이 파일을 편집합니다.

.. note::

   로그인 인증만 사용하는 경우에는 「연결·인증 설정」만으로 동작합니다.
   「LDAP 관리 기능」(``ldap.admin.enabled``)은 관리 화면에서 LDAP 측의
   사용자／역할／그룹을 생성·수정·삭제하는 경우에만 필요합니다.

연결·인증 설정
==============

이 설정들은 관리 화면 「시스템 > 일반」의 LDAP 섹션에서 설정할 수 있으며,
``app/WEB-INF/conf/system.properties`` 에 저장됩니다. 직접 파일을 편집하는 것도 가능합니다.

.. list-table:: 연결·인증 프로퍼티
   :header-rows: 1
   :widths: 30 15 55

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``ldap.provider.url``
     - (없음)
     - LDAP 서버 URL. 예: ``ldap://ldap.example.com:389``. LDAPS의 경우 ``ldaps://ldap.example.com:636``. 공백으로 구분하여 여러 개를 지정하면 페일오버가 됩니다.
   * - ``ldap.base.dn``
     - (없음)
     - LDAP 검색의 베이스 DN. 예: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - (없음)
     - 사용자 인증(바인드)에 사용하는 DN 템플릿. ``%s`` 가 사용자 이름으로 치환됩니다. 예: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - LDAP 인증 방식(JNDI의 ``java.naming.security.authentication``). 일반적으로 ``simple`` 을 사용합니다.
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - JNDI 초기 컨텍스트 팩토리 클래스. 일반적으로 변경이 불필요합니다.
   * - ``ldap.admin.security.principal``
     - (없음)
     - LDAP 검색용 서비스 계정의 바인드 DN. 예: ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - (없음)
     - 위 서비스 계정의 비밀번호.
   * - ``ldap.account.filter``
     - (없음)
     - 사용자의 역할 해석 시, 사용자 엔트리를 검색하기 위한 필터. ``%s`` 가 사용자 이름으로 치환됩니다. 예: ``uid=%s``
   * - ``ldap.group.filter``
     - (빈 값)
     - 그룹 해석 시 사용하는 검색 필터. ``%s`` 가 사용자의 DN 등으로 치환됩니다. 예: ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - 그룹 멤버십을 나타내는 속성명. Active Directory나 이 속성을 가진 서버에서 역할을 해석할 때 사용합니다.

설정 예(``system.properties`` 를 직접 편집하는 경우):

::

    # LDAP 서버 URL
    ldap.provider.url=ldap://ldap.example.com:389

    # 베이스 DN
    ldap.base.dn=dc=example,dc=com

    # 사용자 인증용 바인드 DN 템플릿(%s에 사용자 이름이 삽입됨)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 검색용 서비스 계정의 바인드 DN과 비밀번호
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 역할 해석용 필터
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   ``%s`` 플레이스홀더는 Java의 ``String.format()`` 으로 처리됩니다.
   ``ldap.security.principal`` · ``ldap.account.filter`` · ``ldap.group.filter`` ·
   각 관리용 필터는 모두 ``%s`` 형식을 사용합니다(``{0}`` 형식이 아닙니다).
   또한 필터에 전달되는 사용자 이름은 LDAP 인젝션 대책으로
   |Fess| 내부에서 자동으로 이스케이프됩니다.

LDAP 관리 기능·동작 설정
========================

다음 프로퍼티들은 ``app/WEB-INF/classes/fess_config.properties`` 에 정의되어 있습니다.
값을 변경하려면 이 파일을 편집합니다.

관리 기능 활성화
----------------

.. list-table:: 관리 기능 프로퍼티
   :header-rows: 1
   :widths: 35 15 50

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``ldap.admin.enabled``
     - ``false``
     - 관리 화면에서 LDAP의 사용자／역할／그룹을 생성·수정·삭제하는 기능을 활성화합니다. **로그인 인증에는 불필요**\ 하며, 활성화하지 않아도 LDAP를 통한 로그인은 동작합니다.
   * - ``ldap.admin.sync.password``
     - ``true``
     - 관리 화면에서 사용자를 수정했을 때, |Fess| 측의 비밀번호를 LDAP와 동기화합니다.
   * - ``ldap.auth.validation``
     - ``true``
     - 로그인 시 LDAP 인증 검증을 수행합니다.

사용자／역할／그룹 관리용 필터와 베이스 DN
------------------------------------------

``ldap.admin.enabled=true`` 인 경우, 관리 화면에서 LDAP 엔트리를 조작하기 위해 사용합니다.

.. list-table:: 관리용 필터／베이스 DN
   :header-rows: 1
   :widths: 38 47 15

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``ldap.admin.user.filter``
     - 사용자 검색 필터(``%s`` 가 사용자 이름으로 치환)
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - 사용자 검색 베이스 DN
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - 사용자 생성 시의 objectClass
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - 역할 검색 필터
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - 역할 검색 베이스 DN
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - 역할 생성 시의 objectClass
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - 그룹 검색 필터
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - 그룹 검색 베이스 DN
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - 그룹 생성 시의 objectClass
     - ``groupOfNames``

역할 해석과 동작 제어
----------------------

로그인 후의 역할／그룹 해석 동작을 제어합니다.

.. list-table:: 동작 제어 프로퍼티
   :header-rows: 1
   :widths: 40 15 45

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``ldap.role.search.user.enabled``
     - ``true``
     - 사용자 이름에 기반한 역할을 부여합니다.
   * - ``ldap.role.search.group.enabled``
     - ``true``
     - 그룹에 기반한 역할을 부여합니다.
   * - ``ldap.role.search.role.enabled``
     - ``true``
     - 역할에 기반한 역할을 부여합니다.
   * - ``ldap.allow.empty.permission``
     - ``true``
     - 그룹／역할이 없는 사용자의 로그인을 허용합니다.
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - 그룹명 등에서 NetBIOS 이름(``DOMAIN\`` 형식의 접두사)을 제거합니다.
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - 그룹명에 언더스코어를 허용합니다.
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - 퍼미션 이름을 소문자로 변환합니다.
   * - ``ldap.samaccountname.group``
     - ``false``
     - 그룹명에 ``sAMAccountName`` 속성을 사용합니다(Active Directory용).
   * - ``ldap.max.username.length``
     - ``-1``
     - 사용자 이름의 최대 길이. ``-1`` 은 제한 없음을 의미합니다.

속성 매핑
---------

LDAP 속성과 |Fess| 의 사용자 속성 간의 대응은 ``ldap.attr.*`` 프로퍼티로 정의되어 있습니다.
일반적으로 변경이 불필요하지만, 스키마가 다를 경우에 조정할 수 있습니다. 대표적인 예:

::

    ldap.attr.surname=sn
    ldap.attr.givenName=givenName
    ldap.attr.mail=mail
    ldap.attr.displayName=displayName
    ldap.attr.telephoneNumber=telephoneNumber

.. note::

   ``ldap.attr.state`` 는 ``st``, ``ldap.attr.city`` 는 ``l`` 에 매핑되는 등,
   프로퍼티명과 LDAP 속성명이 일치하지 않는 것도 있습니다.
   전체 목록은 ``fess_config.properties`` 의 ``ldap.attr.`` 로 시작하는 행을 참조하세요.

Active Directory 설정
=====================

Microsoft Active Directory용 설정 예입니다(``system.properties`` 또는 관리 화면).

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 사용자 인증용 바인드 DN 템플릿(UPN 형식)
    ldap.security.principal=%s@example.com

    # 검색용 서비스 계정
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 계정 필터
    ldap.account.filter=sAMAccountName=%s

    # memberOf 속성 사용
    ldap.memberof.attribute=memberOf

    # 그룹 필터
    ldap.group.filter=(member=%s)

중첩 그룹(네스트 그룹)을 해석하는 경우에는 Active Directory 고유의
``LDAP_MATCHING_RULE_IN_CHAIN`` 을 사용할 수 있습니다.

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

OpenLDAP 설정
=============

OpenLDAP용 설정 예입니다.

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 사용자 인증용 바인드 DN 템플릿
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 검색용 서비스 계정
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 계정 필터
    ldap.account.filter=uid=%s

    # 그룹 필터(posixGroup의 경우)
    ldap.group.filter=(memberUid=%s)

.. note::

   표준 OpenLDAP는 ``memberOf`` 속성을 가지지 않으므로,
   ``ldap.group.filter`` 를 사용하여 그룹을 해석합니다.
   ``memberof`` 오버레이를 활성화한 경우에는 ``ldap.memberof.attribute`` 도 이용할 수 있습니다.

보안 설정
=========

LDAPS(SSL/TLS)
--------------

암호화된 연결 사용:

::

    # LDAPS 사용
    ldap.provider.url=ldaps://ldap.example.com:636

자체 서명 인증서인 경우, Java truststore에 인증서를 가져옵니다.

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

비밀번호 보호
-------------

``ldap.admin.security.credentials`` 는 ``system.properties`` 에 저장됩니다.
관리 화면에서 설정한 인증 정보는 내부적으로 암호화되어 저장됩니다.
파일의 접근 권한을 적절히 제한하세요.

페일오버
========

여러 LDAP 서버로 페일오버하는 경우, ``ldap.provider.url`` 에
공백으로 구분하여 여러 URL을 지정합니다.

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

문제 해결
=========

연결 오류
---------

**증상**: LDAP 연결에 실패함

**확인 사항**:

1. LDAP 서버가 실행 중인지
2. 방화벽에서 포트가 열려 있는지(389 또는 636)
3. ``ldap.provider.url`` 이 올바른지(``ldap://`` 또는 ``ldaps://``)
4. ``ldap.admin.security.principal`` 과 비밀번호가 올바른지

인증 오류
---------

**증상**: 사용자 인증에 실패함

**확인 사항**:

1. ``ldap.security.principal`` 의 템플릿이 올바른지(``%s`` 가 포함되어 있는지)
2. 사용자가 지정한 베이스 DN 내에 존재하는지
3. ``ldap.account.filter`` 가 올바른지

그룹／역할을 가져올 수 없음
---------------------------

**증상**: 사용자의 그룹이나 역할을 가져올 수 없음

**확인 사항**:

1. ``ldap.group.filter`` 가 올바른지
2. ``ldap.memberof.attribute`` 가 올바른지(Active Directory의 경우)
3. 그룹이 검색 베이스 DN 내에 존재하는지
4. ``ldap.role.search.*.enabled`` 가 활성화되어 있는지

관리 화면에서 사용자 관리를 할 수 없음
--------------------------------------

**증상**: 관리 화면에서 LDAP 사용자를 생성·편집·삭제할 수 없음

**확인 사항**:

1. ``ldap.admin.enabled`` 가 ``true`` 로 설정되어 있는지
2. ``ldap.admin.user.base.dn`` 등의 관리용 베이스 DN이 올바른지
3. ``ldap.admin.security.principal`` 의 서비스 계정에 쓰기 권한이 있는지

디버그 설정
-----------

상세 로그를 출력하려면, ``app/WEB-INF/classes/log4j2.xml`` 에 로거를 추가합니다.

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

참고 정보
=========

- :doc:`security-role` - 역할 기반 접근 제어
- :doc:`sso-spnego` - SPNEGO(Kerberos) 인증
- :doc:`../admin/user-guide` - 사용자 관리 가이드
