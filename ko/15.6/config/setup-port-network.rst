======================
포트 및 네트워크 설정
======================

개요
====

본 섹션에서는 |Fess| 의 네트워크 관련 설정에 대해 설명합니다.
포트 번호 변경, 프록시 설정, HTTP 통신 설정 등 네트워크 연결에 관한 설정을 다룹니다.

사용 포트 설정
================

기본 포트
----------------

|Fess| 는 기본적으로 다음 포트를 사용합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 서비스
     - 포트 번호
   * - Fess 웹 애플리케이션
     - 8080
   * - OpenSearch (HTTP)
     - 9201
   * - OpenSearch (Transport)
     - 9301

Fess 웹 애플리케이션의 포트 변경
--------------------------------------

Linux 환경 설정
~~~~~~~~~~~~~~~~~

Linux 환경에서 포트 번호를 변경하는 경우 ``bin/fess.in.sh`` 를 편집합니다.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

예를 들어 포트 80을 사용하는 경우:

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=80"

.. note::
   1024 이하의 포트 번호를 사용하는 경우 root 권한 또는 적절한 권한 설정(CAP_NET_BIND_SERVICE)이 필요합니다.

환경 변수를 통한 설정
~~~~~~~~~~~~~~~~~~

환경 변수로 포트 번호를 지정할 수도 있습니다.

::

    export FESS_PORT=8080

RPM/DEB 패키지의 경우
~~~~~~~~~~~~~~~~~~~~~~~~

RPM 패키지에서는 ``/etc/sysconfig/fess``, DEB 패키지에서는 ``/etc/default/fess`` 를 편집합니다.

::

    FESS_PORT=8080

Windows 환경 설정
~~~~~~~~~~~~~~~~~~~

Windows 환경에서는 ``bin\fess.in.bat`` 를 편집합니다.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

Windows 서비스로 등록하는 경우
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Windows 환경에서 서비스 등록하여 사용하는 경우 ``bin\service.bat`` 의 포트 설정도 변경하십시오.
자세한 내용은 :doc:`setup-windows-service` 를 참조하십시오.

컨텍스트 경로 설정
----------------------

|Fess| 를 서브디렉터리에서 공개하는 경우 컨텍스트 경로를 설정할 수 있습니다.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"

이 설정으로 ``http://localhost:8080/search/`` 에서 접근할 수 있게 됩니다.

.. warning::
   컨텍스트 경로를 변경한 경우 정적 파일의 경로도 적절히 설정해야 합니다.

프록시 설정
============

개요
----

인트라넷 내부에서 외부 사이트를 크롤링하거나 외부 API에 접근하는 경우,
방화벽에 의해 통신이 차단될 수 있습니다.
이러한 환경에서는 프록시 서버를 경유하여 통신하도록 설정해야 합니다.

크롤러용 프록시 설정
--------------------------

기본 설정
~~~~~~~~

관리 화면의 크롤 설정에서 설정 파라미터에 다음과 같이 지정합니다.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

인증이 필요한 프록시 설정
~~~~~~~~~~~~~~~~~~~~~~~~~~

프록시 서버에서 인증이 필요한 경우 다음과 같이 추가합니다.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

특정 호스트를 프록시에서 제외
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

특정 호스트(인트라넷 내의 서버 등)를 프록시를 경유하지 않고 연결하는 경우:

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.nonProxyHosts=localhost|*.local|192.168.*

시스템 전체의 HTTP 프록시 설정
------------------------------

|Fess| 애플리케이션 전체에서 HTTP 프록시를 사용하는 경우 ``fess_config.properties`` 에서 설정합니다.

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

.. warning::
   비밀번호는 암호화되지 않고 저장됩니다. 적절한 파일 권한을 설정하십시오.

환경 변수를 통한 프록시 설정
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SSO 인증과 같은 Java 라이브러리가 프록시를 사용해야 하는 경우 환경 변수를 통해 구성해야 합니다.
이러한 환경 변수는 Java 시스템 속성(``http.proxyHost``, ``https.proxyHost`` 등)으로 변환됩니다.

::

    FESS_PROXY_HOST=proxy.example.com
    FESS_PROXY_PORT=8080
    FESS_NON_PROXY_HOSTS=localhost|*.local|192.168.*

RPM 패키지의 경우 ``/etc/sysconfig/fess`` 에서 구성합니다. DEB 패키지의 경우 ``/etc/default/fess`` 에서 구성합니다.

.. note::
   ``fess_config.properties`` 의 ``http.proxy.*`` 설정은 Fess 내부의 HTTP 통신에 사용됩니다.
   SSO 인증과 같은 외부 Java 라이브러리가 프록시를 사용해야 하는 경우 위의 환경 변수도 구성하십시오.

HTTP 통신 설정
============

파일 업로드 제한
--------------------------

관리 화면에서의 파일 업로드 크기를 제한할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 설정 항목
     - 설명
   * - ``http.fileupload.max.size``
     - 최대 파일 업로드 크기(기본값: 262144000바이트 = 250MB)
   * - ``http.fileupload.threshold.size``
     - 메모리에 보관할 임계값 크기(기본값: 262144바이트 = 256KB)
   * - ``http.fileupload.max.file.count``
     - 한 번에 업로드 가능한 파일 수(기본값: 10)

``fess_config.properties`` 에서의 설정 예:

::

    http.fileupload.max.size=524288000
    http.fileupload.threshold.size=524288
    http.fileupload.max.file.count=20

연결 타임아웃 설정
--------------------

OpenSearch에 대한 연결 타임아웃을 설정할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 설정 항목
     - 설명
   * - ``search_engine.http.url``
     - OpenSearch의 URL(기본값: http://localhost:9201)
   * - ``search_engine.heartbeat_interval``
     - 헬스체크 간격(밀리초, 기본값: 10000)

OpenSearch 연결 대상 변경
----------------------

외부 OpenSearch 클러스터에 연결하는 경우:

::

    search_engine.http.url=http://opensearch-cluster.example.com:9200

여러 노드에 연결
~~~~~~~~~~~~~~~~~~

여러 OpenSearch 노드에 연결하는 경우 쉼표로 구분하여 지정합니다.

::

    search_engine.http.url=http://node1:9200,http://node2:9200,http://node3:9200

SSL/TLS 연결 설정
-----------------

OpenSearch에 HTTPS로 연결하는 경우:

::

    search_engine.http.url=https://opensearch.example.com:9200
    search_engine.http.ssl.certificate_authorities=/path/to/ca.crt
    search_engine.username=admin
    search_engine.password=admin_password

.. note::
   인증서 검증을 수행하는 경우 ``certificate_authorities`` 에 CA 인증서 경로를 지정합니다.

가상 호스트 설정
==============

개요
----

|Fess| 에 접근한 호스트명에 따라 검색 결과를 구분할 수 있습니다.
자세한 내용은 :doc:`security-virtual-host` 를 참조하십시오.

기본 설정
--------

``fess_config.properties`` 에서 가상 호스트 헤더를 설정합니다.

::

    virtual.host.headers=X-Forwarded-Host,Host

리버스 프록시와의 연계
========================

Nginx 설정 예
--------------

::

    server {
        listen 80;
        server_name search.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Apache 설정 예
---------------

::

    <VirtualHost *:80>
        ServerName search.example.com

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/

        RequestHeader set X-Forwarded-Proto "http"
        RequestHeader set X-Forwarded-Host "search.example.com"
    </VirtualHost>

SSL/TLS 종단
-----------

리버스 프록시에서 SSL/TLS 종단을 수행하는 경우의 설정 예(Nginx):

::

    server {
        listen 443 ssl http2;
        server_name search.example.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

방화벽 설정
====================

필요한 포트 개방
------------------

|Fess| 를 외부에서 접근 가능하게 하는 경우 다음 포트를 개방합니다.

**iptables 설정 예:**

::

    # Fess 웹 애플리케이션
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

    # HTTPS로 접근하는 경우(리버스 프록시 경유)
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT

**firewalld 설정 예:**

::

    # Fess 웹 애플리케이션
    firewall-cmd --permanent --add-port=8080/tcp
    firewall-cmd --reload

보안 그룹 설정(클라우드 환경)
------------------------------------------

AWS, GCP, Azure 등의 클라우드 환경에서는 보안 그룹이나 네트워크 ACL에서
적절한 포트를 개방하십시오.

권장 설정:
- 인바운드: 80/443 포트(HTTP 리버스 프록시 경유)
- 8080 포트는 내부에서만 접근 가능하도록 제한
- OpenSearch의 9201/9301 포트는 내부에서만 접근 가능하도록 제한

문제 해결
======================

포트 변경 후 접근할 수 없음
------------------------------

1. |Fess| 를 재시작했는지 확인하십시오.
2. 방화벽에서 해당 포트가 개방되어 있는지 확인하십시오.
3. 로그 파일(``fess.log``)에서 오류를 확인하십시오.

프록시를 경유하여 크롤링할 수 없음
------------------------------

1. 프록시 서버의 호스트명과 포트가 올바른지 확인하십시오.
2. 프록시 서버에서 인증이 필요한 경우 사용자명과 비밀번호를 설정하십시오.
3. 프록시 서버의 로그에서 연결 시도가 기록되어 있는지 확인하십시오.
4. ``nonProxyHosts`` 설정이 적절한지 확인하십시오.

OpenSearch에 연결할 수 없음
-------------------------

1. OpenSearch가 시작되어 있는지 확인하십시오.
2. ``search_engine.http.url`` 설정이 올바른지 확인하십시오.
3. 네트워크 연결을 확인하십시오: ``curl http://localhost:9201``
4. OpenSearch의 로그에서 오류를 확인하십시오.

리버스 프록시를 경유하여 접근하면 정상 작동하지 않음
----------------------------------------------------

1. ``X-Forwarded-Host`` 헤더가 올바르게 설정되어 있는지 확인하십시오.
2. ``X-Forwarded-Proto`` 헤더가 올바르게 설정되어 있는지 확인하십시오.
3. 컨텍스트 경로가 올바르게 설정되어 있는지 확인하십시오.
4. 리버스 프록시의 로그에서 오류를 확인하십시오.

참고 정보
========

- :doc:`setup-memory` - 메모리 설정
- :doc:`setup-windows-service` - Windows 서비스 설정
- :doc:`security-virtual-host` - 가상 호스트 설정
- :doc:`crawler-advanced` - 크롤러 고급 설정
- `OpenSearch Configuration <https://opensearch.org/docs/latest/install-and-configure/configuration/>`_
