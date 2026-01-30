==================================
LDAP 통합 가이드
==================================

개요
====

|Fess|는 LDAP(Lightweight Directory Access Protocol) 서버와의 통합을 지원하여
엔터프라이즈 환경에서의 인증과 사용자 관리를 구현할 수 있습니다.

LDAP 통합으로:

- Active Directory나 OpenLDAP에서의 사용자 인증
- 그룹 기반 접근 제어
- 사용자 정보 자동 동기화

가 가능해집니다.

지원 LDAP 서버
================

|Fess|는 다음 LDAP 서버와의 통합을 지원합니다:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- 기타 LDAP v3 호환 서버

전제조건
========

- LDAP 서버로의 네트워크 접근
- LDAP 검색용 서비스 계정(바인드 DN)
- LDAP 구조(베이스 DN, 속성명 등) 이해

기본 설정
========

``app/WEB-INF/conf/system.properties``에 다음 설정을 추가합니다.

LDAP 연결 설정
------------

::

    # LDAP 인증 활성화
    ldap.admin.enabled=true

    # LDAP 서버 URL
    ldap.provider.url=ldap://ldap.example.com:389

    # 보안 연결(LDAPS)인 경우
    # ldap.provider.url=ldaps://ldap.example.com:636

    # 베이스 DN
    ldap.base.dn=dc=example,dc=com

    # 바인드 DN(서비스 계정)
    ldap.security.principal=cn=fess,ou=services,dc=example,dc=com

    # 바인드 비밀번호
    ldap.admin.security.credentials=your_password

사용자 검색 설정
----------------

::

    # 사용자 검색의 베이스 DN
    ldap.user.search.base=ou=users,dc=example,dc=com

    # 사용자 검색 필터
    ldap.user.search.filter=(uid={0})

    # 사용자명 속성
    ldap.user.name.attribute=uid

그룹 검색 설정
----------------

::

    # 그룹 검색의 베이스 DN
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # 그룹 검색 필터
    ldap.group.search.filter=(member={0})

    # 그룹명 속성
    ldap.group.name.attribute=cn

Active Directory 설정
====================

Microsoft Active Directory용 설정 예입니다.

기본 설정
--------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 서비스 계정(UPN 형식)
    ldap.security.principal=fess@example.com
    ldap.admin.security.credentials=your_password

    # 사용자 검색
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.user.search.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # 그룹 검색
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.search.filter=(member={0})
    ldap.group.name.attribute=cn

Active Directory 고유 설정
--------------------------

::

    # 중첩 그룹 해결
    ldap.memberof.enabled=true

    # memberOf 속성 사용
    ldap.group.search.filter=(member:1.2.840.113556.1.4.1941:={0})

OpenLDAP 설정
============

OpenLDAP용 설정 예입니다.

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 서비스 계정
    ldap.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 사용자 검색
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.user.search.filter=(uid={0})
    ldap.user.name.attribute=uid

    # 그룹 검색
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.search.filter=(memberUid={0})
    ldap.group.name.attribute=cn

보안 설정
================

LDAPS(SSL/TLS)
----------------

암호화된 연결 사용:

::

    # LDAPS 사용
    ldap.provider.url=ldaps://ldap.example.com:636

    # StartTLS 사용
    ldap.start.tls=true

자체 서명 인증서인 경우 Java truststore에 인증서 가져오기:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

비밀번호 보호
----------------

비밀번호를 환경 변수로 설정:

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

역할 매핑
================

LDAP 그룹을 |Fess| 역할에 매핑할 수 있습니다.

자동 매핑
--------------

그룹명이 그대로 역할명으로 사용됩니다:

::

    # LDAP 그룹 "fess-users" -> Fess 역할 "fess-users"
    ldap.group.role.mapping.enabled=true

커스텀 매핑
------------------

::

    # 그룹명을 역할에 매핑
    ldap.group.role.mapping.Administrators=admin
    ldap.group.role.mapping.PowerUsers=editor
    ldap.group.role.mapping.Users=guest

사용자 정보 동기화
==================

LDAP에서 사용자 정보를 |Fess|에 동기화할 수 있습니다.

자동 동기화
--------

로그인 시 자동으로 사용자 정보 동기화:

::

    ldap.user.sync.enabled=true

동기화할 속성
------------

::

    # 이메일 주소
    ldap.user.email.attribute=mail

    # 표시 이름
    ldap.user.displayname.attribute=displayName

연결 풀링
==============

성능 향상을 위한 연결 풀 설정:

::

    # 연결 풀 활성화
    ldap.connection.pool.enabled=true

    # 최소 연결 수
    ldap.connection.pool.min=1

    # 최대 연결 수
    ldap.connection.pool.max=10

    # 연결 타임아웃(밀리초)
    ldap.connection.timeout=5000

페일오버
================

여러 LDAP 서버로의 페일오버:

::

    # 공백 구분으로 여러 URL 지정
    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

문제 해결
======================

연결 오류
----------

**증상**: LDAP 연결 실패

**확인 사항**:

1. LDAP 서버가 실행 중인지
2. 방화벽에서 포트가 열려 있는지(389 또는 636)
3. URL이 올바른지(``ldap://`` 또는 ``ldaps://``)
4. 바인드 DN과 비밀번호가 올바른지

인증 오류
----------

**증상**: 사용자 인증 실패

**확인 사항**:

1. 사용자 검색 필터가 올바른지
2. 사용자가 검색 베이스 DN 내에 존재하는지
3. 사용자명 속성이 올바른지

그룹을 가져올 수 없음
----------------------

**증상**: 사용자의 그룹을 가져올 수 없음

**확인 사항**:

1. 그룹 검색 필터가 올바른지
2. 그룹 멤버십 속성이 올바른지
3. 그룹이 검색 베이스 DN 내에 존재하는지

디버그 설정
------------

상세 로그 출력:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

참고 정보
========

- :doc:`security-role` - 역할 기반 접근 제어
- :doc:`sso-spnego` - SPNEGO(Kerberos) 인증
- :doc:`../admin/user-guide` - 사용자 관리 가이드
