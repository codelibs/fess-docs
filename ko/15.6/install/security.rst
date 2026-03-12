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
2. "시스템"→"사용자" 클릭
3. ``admin`` 사용자 선택
4. 강력한 비밀번호 설정
5. "업데이트" 버튼 클릭

**권장 비밀번호 정책:**

- 최소 12자 이상
- 영문 대문자, 영문 소문자, 숫자, 기호 포함
- 사전에 있는 단어 회피
- 정기적으로 변경(90일마다 권장)

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

5. |Fess| 설정을 업데이트하여 OpenSearch 인증 정보 추가::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200
       SEARCH_ENGINE_USERNAME=admin
       SEARCH_ENGINE_PASSWORD=<strong_password>

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

**방법 2: Fess 자체에서 HTTPS 설정**

``system.properties`` 에 다음을 추가::

    server.ssl.enabled=true
    server.ssl.key-store=/path/to/keystore.p12
    server.ssl.key-store-password=<password>
    server.ssl.key-store-type=PKCS12

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

    $ sudo firewall-cmd --permanent --add-service=http
    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --remove-service=opensearch  # 사용자 정의 서비스의 경우
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

역할 기반 액세스 제어 (RBAC)
-----------------------------

|Fess| 는 여러 사용자 역할을 지원합니다. 최소 권한 원칙에 따라 사용자에게 필요 최소한의 권한만 부여하십시오.

**역할 유형:**

- **관리자**: 모든 권한
- **일반 사용자**: 검색만
- **크롤러 관리자**: 크롤 설정 관리
- **검색 결과 편집자**: 검색 결과 편집

**절차:**

1. 관리 화면에서 "시스템"→"역할" 클릭
2. 필요한 역할 생성
3. "시스템"→"사용자"에서 사용자에게 역할 할당

감사 로그 활성화
--------------

시스템 작업 이력을 기록하기 위해 감사 로그가 기본적으로 활성화되어 있습니다.

설정 파일(``log4j2.xml``)에서 감사 로그 활성화::

    <Logger name="org.codelibs.fess.audit" level="info" additivity="false">
        <AppenderRef ref="AuditFile"/>
    </Logger>

정기적인 보안 업데이트
------------------------------

|Fess| 및 OpenSearch의 보안 업데이트를 정기적으로 적용하십시오.

**권장 절차:**

1. 보안 정보를 정기적으로 확인

   - `Fess 릴리스 정보 <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch 보안 권고 <https://opensearch.org/security.html>`__

2. 테스트 환경에서 업데이트 검증
3. 운영 환경에 업데이트 적용

데이터 보호
========

백업 암호화
------------------

백업 데이터에는 기밀 정보가 포함될 수 있습니다. 백업 파일을 암호화하여 저장하십시오.

암호화 백업 예::

    $ tar czf fess-backup.tar.gz /var/lib/opensearch /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

보안 모범 사례
============================

최소 권한 원칙
------------

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

필요에 따라 Nginx 또는 Apache에서 보안 헤더를 설정하십시오::

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;

보안 체크리스트
========================

운영 환경에 배포하기 전에 다음 체크리스트를 확인하십시오:

기본 설정
--------

- [ ] 관리자 비밀번호 변경 완료
- [ ] HTTPS 활성화 완료
- [ ] 기본 포트 번호 변경(옵션)

네트워크 보안
----------------------

- [ ] 방화벽으로 불필요한 포트 폐쇄 완료
- [ ] 관리 화면에 대한 액세스 IP 제한 완료(가능한 경우)
- [ ] OpenSearch에 대한 액세스를 내부 네트워크로만 제한 완료

액세스 제어
----------

- [ ] 역할 기반 액세스 제어 설정 완료
- [ ] 불필요한 사용자 계정 삭제 완료
- [ ] 비밀번호 정책 설정 완료

모니터링 및 로그
--------

- [ ] 감사 로그 활성화 완료
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
======

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

보안에 관한 질문이나 문제가 있는 경우 다음으로 문의하십시오:

- Issues: https://github.com/codelibs/fess/issues
- 상용 지원: https://www.n2sm.net/
