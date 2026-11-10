==================
보안 설정
==================

이 페이지에서는 운영 환경에서 |Fess| 를 안전하게 운용하기 위해 권장되는 보안 설정에 대해 설명합니다.

.. danger::

   **보안은 매우 중요합니다**

   운영 환경에서는 이 페이지에 기재된 모든 보안 설정을 실시할 것을 강력히 권장합니다.
   보안 설정을 소홀히 하면 무단 액세스, 데이터 유출, 시스템 침해 등의 위험이 높아집니다.

필수 보안 설정
====================

관리자 비밀번호 변경
--------------------

기본 관리자 비밀번호(``admin`` / ``admin``)는 반드시 변경하십시오.

**절차:**

1. 관리 화면에 로그인: http://localhost:8080/admin
2. "사용자"→"사용자" 클릭
3. ``admin`` 사용자 선택
4. 강력한 비밀번호 설정
5. "업데이트" 버튼 클릭

.. note::

   한 번 ``admin`` 에서 변경한 비밀번호는 ``admin`` 과 같은 단순한 문자열로는 다시 설정할 수 없습니다(``password.invalid.admin.passwords`` 에 의해 관리자 비밀번호의 블랙리스트가 설정되어 있습니다). 또한 최초 시작 전이라면 ``fess_config.properties`` 의 ``index.user.initial_password`` 로 ``admin`` 사용자의 초기 비밀번호를 변경할 수 있습니다. ``bin/fess-setup init`` 로 설정할 수도 있습니다( :doc:`fess-setup` 참조).

**권장 비밀번호 정책:**

|Fess| 는 비밀번호의 최소·최대 문자 수와 문자 종류 요건을 강제하는 기능을 제공합니다. ``fess_config.properties`` 에서 다음 속성을 설정하십시오(괄호 안은 기본값입니다).

- ``password.min.length`` (기본값: ``8``): 최소 문자 수. 12자 이상을 권장합니다.
- ``password.max.length`` (기본값: ``100``): 최대 문자 수.
- ``password.require.uppercase`` (기본값: ``false``): 영문 대문자를 필수로 설정합니다.
- ``password.require.lowercase`` (기본값: ``false``): 영문 소문자를 필수로 설정합니다.
- ``password.require.digit`` (기본값: ``false``): 숫자를 필수로 설정합니다.
- ``password.require.special.char`` (기본값: ``false``): 기호를 필수로 설정합니다.

.. note::

   기본값에서는 최소 문자 수가 ``8`` 이며 문자 종류 요건은 모두 비활성화되어 있습니다. 비밀번호 강도를 높이려면 위의 속성을 명시적으로 설정하십시오. 또한 |Fess| 에는 비밀번호 유효기간(정기 변경 강제) 기능이 없습니다. 정기적인 비밀번호 변경을 운영 규칙으로 정하고자 하는 경우에는 수동으로 대응하십시오.

**비밀번호 변경 후의 세션:**

로컬 사용자의 비밀번호가 변경되면(사용자 본인이 변경한 경우와, 관리자가 사용자 관리 화면 또는 Admin API에서 변경한 경우 모두) 해당 사용자의 다른 로그인 세션은 다음 확인 시 종료됩니다(아래 참조). 각 로그인 세션은 마지막 비밀번호 변경 시각을 ``fess_config.properties`` 의 ``password.changed.check.interval`` (기본값: ``60`` 초, ``0`` 이하이면 요청마다 확인)에 한 번 이하로 사용자 인덱스에서 확인하므로, 다른 세션은 어느 노드에서든 이 시간(초) 이내에 종료됩니다. LDAP나 SSO로 인증하는 사용자는 비밀번호가 |Fess| 밖에서 관리되므로 대상이 아닙니다.

암호화 키 변경
--------------

``fess_config.properties`` 의 ``app.cipher.key`` 는 크롤링 설정과 데이터 스토어 설정에 저장되는 비밀번호를 암호화하는 키입니다. 기본 제공 값(``___change__me___``)은 공개되어 있습니다. 키가 비어 있거나 기본 제공 값 그대로이면 |Fess| 는 시작할 때 ``fess.log`` 에 경고를 출력합니다( :ref:`upgrade-1510-cipher-key` 참조). |Fess| 는 키를 자동으로 변경하지 않습니다.

처음 시작하기 전에 ``admin`` 사용자의 초기 비밀번호와 함께 설정합니다::

    $ bin/fess-setup init

RPM / DEB 패키지에서는 ``/usr/share/fess/bin/fess-setup init`` 를 실행합니다. 명령은 임의의 키를 생성하며, ``--cipher-key`` 로 지정할 수도 있습니다( :doc:`fess-setup` 참조). 직접 설정하려면 ``fess_config.properties`` 의 ``app.cipher.key`` 를 편집합니다(ZIP 패키지는 ``app/WEB-INF/classes/fess_config.properties`` , RPM / DEB 패키지는 ``/etc/fess/fess_config.properties`` ). 기본 ``app.cipher.algorithm`` (``aes``)에서는 키가 16, 24 또는 32자여야 합니다.

.. warning::

   크롤링 설정이나 데이터 스토어 설정에 비밀번호를 저장한 뒤에 키를 변경하면 해당 값을 복호화할 수 없게 됩니다. 키는 ``fess_config.properties`` 백업과 함께 보관하고, 다른 환경으로 이전할 때 같은 키를 사용하십시오.

OpenSearch 보안 플러그인 활성화
--------------------------------------

**절차:**

1. ``opensearch.yml`` 에서 다음 행을 삭제하거나 주석 처리::

       # plugins.security.disabled: true

2. 보안 플러그인 설정::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. TLS/SSL 인증서 설정

4. OpenSearch 재시작

5. |Fess| 측에서 OpenSearch로의 연결 정보를 설정합니다.

   연결 URL은 환경 변수 ``SEARCH_ENGINE_HTTP_URL`` 로 지정합니다(``bin/fess.in.sh`` 또는 서비스의 환경 설정 파일을 편집합니다. 기본값은 ``fess_config.properties`` 의 ``search_engine.http.url`` 입니다)::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200

   인증 정보는 ``fess_config.properties`` 의 다음 속성으로 지정합니다(zip, RPM, DEB 패키지에는 ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD`` 환경 변수가 없습니다. docker-fess 이미지에서는 사용할 수 있습니다)::

       search_engine.username=admin
       search_engine.password=<strong_password>

자세한 내용은 `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__ 을 참조하십시오.

HTTPS 활성화
------------

HTTP 통신은 암호화되지 않아 도청 및 변조 위험이 있습니다. 운영 환경에서는 반드시 HTTPS를 사용하십시오.

**방법 1: 리버스 프록시 사용(권장)**

Nginx 또는 Apache를 |Fess| 앞단에 배치하여 HTTPS 종단을 수행합니다.

Nginx 설정 예::

    server {
        listen 443 ssl http2;
        server_name your-fess-domain.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

TLS를 리버스 프록시에서 종료하는 경우, 세션 쿠키에 ``Secure`` 속성이 붙도록 ``fess_config.properties`` 에 다음 설정도 추가하세요. 변경 후에는 |Fess| 를 재시작합니다. 설정하면 HTTP로는 세션을 만들 수 없으므로, HTTP로도 접속하는 경우에는 설정하지 마세요::

    session.cookie.secure=true

**방법 2: Fess 자체에서 HTTPS 설정**

``tomcat_config.properties`` 에 다음을 추가::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[키스토어 파일 경로]
    tomcat.certificateKeystorePassword=[키스토어 파일 생성 시 지정한 비밀번호]
    tomcat.certificateKeyAlias=[인증서 별칭]
    tomcat.sslProtocol=[SSL 프로토콜 (예: TLS)]
    tomcat.enabledProtocols=활성화된 프로토콜 목록 (쉼표 구분) (예: TLSv1.2,TLSv1.3)

권장 보안 설정
====================

방화벽 설정
------------------

필요한 포트만 개방하고 불필요한 포트는 닫으십시오.

**개방해야 할 포트:**

- **8080** (또는 HTTPS의 443): |Fess| 웹 인터페이스(외부에서 액세스가 필요한 경우)
- **22**: SSH(관리용, 신뢰할 수 있는 IP 주소에서만)

**닫아야 할 포트:**

- **9200, 9300**: OpenSearch(내부 통신만, 외부 액세스 차단)

Linux (firewalld) 설정 예::

    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --add-port=8080/tcp  # 8080 포트로 직접 접속하는 경우에만
    $ sudo firewall-cmd --reload

IP 주소 제한::

    $ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'

액세스 제어 설정
----------------

관리 화면에 대한 액세스를 특정 IP 주소로 제한하는 것을 고려하십시오.

Nginx에서 액세스 제한 예::

    location /admin {
        allow 192.168.1.0/24;
        deny all;

        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }

역할과 액세스 제어
--------------------

|Fess| 에는 미리 2개의 역할이 준비되어 있습니다.

- ``admin``: 관리 화면을 포함한 모든 작업이 가능한 관리자 역할
- ``guest``: 로그인하지 않은(익명) 사용자에게 할당되는 역할

이 외의 역할은 관리 화면에서 자유롭게 생성할 수 있습니다. |Fess| 의 역할은 이름만을 가진 태그이며, 주로 검색 결과에 대한 액세스 제어(어떤 문서를 표시할 수 있는지)에 사용됩니다. 다만 ``admin-user`` 나 ``admin-scheduler`` 처럼 ``admin-`` 뒤에 관리 화면 이름을 붙인 이름의 역할은 해당 관리 화면을 열기 위한 권한이 됩니다(``admin-user-view`` 처럼 ``-view`` 를 붙인 역할은 참조 전용입니다).

.. warning::

   ``admin-*`` 역할은 일상적인 관리 화면을 운영 담당자에게 나누어 맡기기 위한 것이며, 권한의 경계가 아닙니다. 예를 들어 ``admin-user`` 를 가진 사용자는 관리자 역할을 포함한 기존의 모든 역할을 임의의 사용자에게 부여할 수 있습니다. ``admin-accesstoken`` 으로는 Admin API의 모든 기능을 사용할 수 있는 ``Radmin-api`` 권한의 액세스 토큰을 발급할 수 있고, ``admin-scheduler`` 로는 서버에서 스크립트 작업을 실행할 수 있으며, ``admin-plugin`` 으로는 플러그인을 설치할 수 있습니다. 모든 ``admin-*`` 역할을 관리자 역할(``authentication.admin.roles``, 기본값은 ``admin``)과 동등하게 취급하고, 신뢰할 수 있는 운영 담당자에게만 부여하십시오.

최소 권한 원칙에 따라 관리자 역할(``admin``)은 관리 업무를 수행하는 사용자에게만 부여하고, 일반 검색 사용자에게는 부여하지 마십시오.

**절차:**

1. 관리 화면에서 "사용자"→"역할" 클릭
2. 필요한 역할 생성
3. "사용자"→"사용자"에서 사용자에게 역할 할당

감사 로그
------------

인증이나 관리 작업 등 시스템의 작업 이력은 기본적으로 감사 로그로 기록됩니다. 감사 로그는 ``log4j2.xml`` 에 정의된 ``fess.log.audit`` 로거에 의해 출력되며, 기본 출력 대상은 ``audit.log`` 입니다.

기본적으로 활성화되어 있으므로 추가 설정은 필요하지 않습니다. 출력 대상이나 로그 레벨을 커스터마이즈하려면 ``log4j2.xml`` 의 다음 정의를 편집하십시오::

    <Logger name="fess.log.audit" additivity="false" level="info">
        <AppenderRef ref="AuditFile"/>
    </Logger>

감사 로그의 레코드 하나는 탭으로 구분한 ``key:value`` 필드를 나열한 한 줄(LTSV)입니다. ``action`` 으로 시작하고 ``ip`` (클라이언트 IP 주소)와 ``time`` (UTC, ISO 8601)으로 끝납니다. ``app.audit.log.format`` 이 ``ecs`` 이거나, 비어 있고 환경 변수 ``FESS_APP_TYPE`` 이 ``docker`` 이면 ECS 형식의 JSON으로 출력되며, 각 필드는 ``labels.<key>`` 가 됩니다.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - action
     - 필드
     - 기록되는 시점
   * - ``LOGIN``
     - ``user`` , ``permissions``
     - 사용자가 로그인했을 때.
   * - ``LOGOUT``
     - ``user`` , ``permissions``
     - 사용자가 로그아웃했을 때.
   * - ``LOGIN_FAILURE``
     - ``class`` , ``user``
     - 로그인 폼, 로그인 API 또는 SSO에서 로그인이 거부되었을 때. SSO 인증 처리가 예외로 로그인을 거부한 경우도 기록됩니다.
   * - ``ACCESS``
     - ``user`` , ``path`` , ``execute`` , ``method`` , ``id``
     - 관리 화면 또는 Admin API에 대한 요청이 처리가 실행되기 전에 도착했을 때. Admin API에서는 액세스 토큰이 받아들여진 뒤입니다.
   * - ``ACCESS_DENIED``
     - ``user`` , ``path``
     - 관리 화면에 대한 요청이 사용자의 역할 때문에 거부되었을 때, 또는 Admin API에 대한 요청이 액세스 토큰 검사에서 거부되었을 때(API는 HTTP 401을 반환합니다).
   * - ``UPDATE_PASSWORD``
     - ``user`` , ``target``
     - 비밀번호가 변경되었을 때. 사용자가 로그인 화면 또는 ``/api/v2/auth/password`` 에서 직접 변경한 경우와, 관리자가 사용자 관리 화면 또는 Admin API에서 사용자에게 새 비밀번호를 설정한 경우입니다.
   * - ``UPDATE_PERMISSION``
     - ``user`` , ``permissions``
     - LDAP 사용자의 권한이 갱신되었을 때.
   * - ``SCRIPT_EXECUTION``
     - ``scriptType`` , ``source`` , ``user`` , ``result`` , ``script``
     - 스크립트가 실행되었을 때. :doc:`../config/scripting-overview` 를 참조하십시오.

- ``LOGIN_FAILURE``: ``user`` 는 입력된 사용자 이름이고 ``class`` 는 자격 증명의 종류입니다. SSO 인증 처리가 예외로 로그인을 거부한 경우에는 자격 증명이 확정되지 않았으므로 ``user`` 와 ``class`` 가 모두 기록되지 않으며, 예외의 내용도 기록되지 않습니다.
- ``ACCESS``: ``method`` 는 HTTP 메서드입니다. ``id`` 는 요청 파라미터 ``id`` 의 값이며, 요청에 있는 경우에만 기록됩니다(업로드 요청에서는 읽지 않습니다). 관리 화면의 폼에는 비밀번호와 키가 포함되므로 그 밖의 요청 파라미터는 기록되지 않습니다.
- ``ACCESS_DENIED``: 거부된 Admin API 요청에서는 요청 경로만 기록됩니다. 액세스 토큰도, 그것을 전달한 파라미터도 기록되지 않습니다.
- ``UPDATE_PASSWORD``: ``user`` 는 비밀번호를 변경한 사용자이고 ``target`` 은 비밀번호가 변경된 사용자의 이름입니다. 비밀번호와 그 해시는 기록되지 않으며, 거부된 변경은 기록되지 않습니다.

정기적인 보안 업데이트
------------------------------

|Fess| 및 OpenSearch의 보안 업데이트를 정기적으로 적용하십시오.

**권장 절차:**

1. 보안 정보를 정기적으로 확인

   - `Fess 릴리스 정보 <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch 보안 권고 <https://github.com/opensearch-project/OpenSearch/security/advisories>`__

2. 테스트 환경에서 업데이트 검증
3. 운영 환경에 업데이트 적용

데이터 보호
===========

백업 암호화
------------------

백업 데이터에는 기밀 정보가 포함될 수 있습니다. 백업 파일을 암호화하여 저장하십시오.

암호화 백업 예::

    $ tar czf fess-backup.tar.gz /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

실행 중인 OpenSearch의 데이터 디렉터리(``/var/lib/opensearch``)는 파일을 복사하는 방식으로는 일관된 백업을 만들 수 없습니다. 인덱스 데이터에는 `OpenSearch 스냅샷 기능 <https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`__ 을 사용하세요. |Fess| 의 설정 데이터는 관리 화면의 백업 페이지에서 다운로드할 수 있습니다(:doc:`../admin/backup-guide` 참조).

보안 모범 사례
============================

최소 권한 원칙
--------------

- Fess 및 OpenSearch를 root 사용자로 실행하지 않음
- 전용 사용자 계정으로 실행
- 필요 최소한의 파일 시스템 권한 부여

네트워크 분리
--------------

- OpenSearch를 프라이빗 네트워크에 배치
- 내부 통신에는 VPN 또는 프라이빗 네트워크 사용
- DMZ에 |Fess| 의 웹 인터페이스만 배치

정기적인 보안 감사
----------------------

- 액세스 로그를 정기적으로 확인
- 비정상적인 액세스 패턴 검출
- 정기적으로 취약점 스캔 실시

보안 헤더 설정
------------------------

|Fess| 는 기본적으로 HTML 응답에 ``X-Frame-Options: SAMEORIGIN`` 을 추가하므로(``fess_config.properties`` 의 ``response.headers``) 프록시에서 추가할 필요가 없습니다.

필요에 따라 Nginx 또는 Apache에서 보안 헤더를 설정하십시오::

    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

보안 체크리스트
========================

운영 환경에 배포하기 전에 다음 체크리스트를 확인하십시오:

기본 설정
---------

- [ ] 관리자 비밀번호 변경 완료
- [ ] 암호화 키(``app.cipher.key``)를 기본 제공 값에서 변경 완료
- [ ] HTTPS 활성화 완료
- [ ] 기본 포트 번호 변경(옵션)

네트워크 보안
----------------------

- [ ] 방화벽으로 불필요한 포트 폐쇄 완료
- [ ] 관리 화면에 대한 액세스 IP 제한 완료(가능한 경우)
- [ ] OpenSearch에 대한 액세스를 내부 네트워크로만 제한 완료

액세스 제어
-----------

- [ ] 역할과 액세스 권한을 적절히 설정 완료(관리자 역할을 필요한 사용자에게만 부여)
- [ ] 불필요한 사용자 계정 삭제 완료
- [ ] 비밀번호 정책 설정 완료

모니터링 및 로그
----------------

- [ ] 감사 로그가 활성화되어 있음을 확인 완료
- [ ] 로그 보존 기간 설정 완료
- [ ] 로그 모니터링 체계 구축 완료(가능한 경우)

백업 및 복구
--------------------

- [ ] 정기적인 백업 일정 설정 완료
- [ ] 백업 데이터 암호화 완료
- [ ] 복원 절차 검증 완료

업데이트 및 패치 관리
----------------------

- [ ] 보안 업데이트 알림 수신 체계 구축 완료
- [ ] 업데이트 절차 문서화 완료
- [ ] 테스트 환경에서 업데이트 검증 체제 구축 완료

보안 사고 대응
==========================

보안 사고가 발생한 경우의 대응 절차:

1. **사고 감지**

   - 로그 확인
   - 비정상적인 액세스 패턴 검출
   - 시스템 동작 이상 확인

2. **초기 대응**

   - 영향 범위 특정
   - 피해 확산 방지(해당 서비스 중지 등)
   - 증거 보전

3. **조사 및 분석**

   - 로그 상세 분석
   - 침입 경로 특정
   - 유출되었을 가능성이 있는 데이터 특정

4. **복구**

   - 취약점 수정
   - 시스템 복구
   - 모니터링 강화

5. **사후 대응**

   - 사고 보고서 작성
   - 재발 방지 대책 실시
   - 관계자에게 보고

참고 정보
=========

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

보안에 관한 질문이나 문제가 있는 경우 다음으로 문의하십시오:

- Issues: https://github.com/codelibs/fess/issues
- 상용 지원: https://www.n2sm.net/
