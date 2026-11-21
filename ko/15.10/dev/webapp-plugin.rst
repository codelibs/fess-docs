==================================
웹앱 플러그인
==================================

개요
====

웹앱 플러그인(``fess-webapp-*``)은 |Fess| 의 웹 애플리케이션을 확장하는
플러그인입니다. 다른 종류의 플러그인과 달리 Action 클래스나 JSP 를 직접
추가하는 것이 아니라, DI 컨테이너(Lasta Di)에 대해 **컴포넌트를 추가하거나
교체** 함으로써 기능을 확장합니다. 대표적인 용도는 다음과 같습니다:

- 새로운 컴포넌트(헬퍼·서비스 등)의 추가
- |Fess| 본체 컴포넌트의 교체(서브클래스화)
- REST API 엔드포인트의 추가(``WebApiManager``)
- 검색 동작의 확장(쿼리 커맨드, 랭크 퓨전 등)

.. note::

   웹앱 플러그인은 JAR 로 배포되며, 내부의 클래스와 DI 설정 파일이
   |Fess| 웹 애플리케이션의 클래스패스에 로드됩니다. JSP 뷰를 추가하는
   것은 아닙니다. 검색 화면의 디자인을 커스터마이즈하려면
   :doc:`theme-development` 를 참조하십시오.

기본 구조
=========

웹앱 플러그인의 구현 템플릿인
`fess-webapp-example <https://github.com/codelibs/fess-webapp-example>`__ 를
예로 들면, 플러그인은 「구현 클래스」와 「DI 등록 파일」로 구성됩니다:

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/webapp/example/helper/
        │   ├── ExampleHelper.java        # 추가할 컴포넌트
        │   └── CustomSystemHelper.java   # 코어 컴포넌트의 교체
        └── resources/
            ├── app++.xml                 # 컴포넌트의 추가(병합)
            └── fess+systemHelper.xml     # 컴포넌트의 교체

.. note::

   구현 클래스의 패키지는 ``org.codelibs.fess.webapp.<플러그인 이름>`` 을
   사용합니다. DI 설정 파일은 ``src/main/resources/`` 에 배치합니다.
   데이터스토어 플러그인과 달리 ``src/main/webapp/`` 나 JSP 는 포함하지
   않습니다.

pom.xml과 매니페스트
====================

웹앱 플러그인은 ``fess-parent`` 를 부모 POM 으로 하는 jar 로 빌드합니다.
|Fess| 본체에서 실행 시 제공되는 ``fess`` 나 ``opensearch`` 는 ``provided``
스코프로 선언하고, ``lastaflute``·``dbflute-runtime``·``corelib`` 등 실행
시 필요한 라이브러리는 일반 스코프로 선언합니다.

웹앱 플러그인에서 가장 중요한 것은 JAR 매니페스트에 ``Fess-WebAppJar: true``
를 부여하는 것입니다. 이 선언에 의해 |Fess| 는 플러그인의 클래스와 DI 설정
파일을 웹 애플리케이션의 클래스로더에 마운트합니다. 이 설정은
``maven-jar-plugin`` 으로 수행합니다:

.. code-block:: xml

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-jar-plugin</artifactId>
                <configuration>
                    <archive>
                        <manifestEntries>
                            <Fess-WebAppJar>true</Fess-WebAppJar>
                        </manifestEntries>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>

.. warning::

   ``Fess-WebAppJar: true`` 를 부여하지 않으면 플러그인의 클래스나 DI
   설정 파일이 웹 애플리케이션의 클래스패스에 로드되지 않아, 컴포넌트의
   추가·교체가 활성화되지 않습니다.

pom.xml 전체 구성(부모 POM·의존 관계 선언 방법 등)은
:doc:`plugin-architecture` 를 참조하십시오.

확장 패턴
=========

컴포넌트 추가(app++.xml)
-------------------------

가장 기본적인 확장 방법은 자체 컴포넌트를 추가하는 것입니다. Lasta Di 는
클래스패스 상의 ``app++.xml`` 을 |Fess| 본체의 ``app.xml`` 로부터 구축되는
``app`` 네임스페이스에 **병합** 합니다(끝의 ``++`` 는 추가 병합 규약입니다).
추가하는 컴포넌트는 |Fess| 본체에 존재하지 않는 이름을 사용하므로, 아무것도
덮어쓰지 않습니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleHelper"
            class="org.codelibs.fess.webapp.example.helper.ExampleHelper">
        </component>
    </components>

컴포넌트 구현에서는 초기화에 ``@PostConstruct`` 를 사용하고, |Fess| 본체의
컴포넌트는 ``ComponentUtil`` 에서 가져와 재사용합니다(복사나 덮어쓰기는
하지 않습니다):

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import org.codelibs.fess.helper.SystemHelper;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;

    public class ExampleHelper {

        protected String pluginName = "fess-webapp-example";

        @PostConstruct
        public void init() {
            // DI 에 의한 생성 후 한 번만 호출되는 초기화 처리
        }

        public String getPluginLabel() {
            // 코어의 SystemHelper 를 재사용하여 실행 중인 Fess 버전을 취득
            final SystemHelper systemHelper = ComponentUtil.getSystemHelper();
            final String version = systemHelper != null ? systemHelper.getProductVersion() : "unknown";
            return pluginName + " (Fess " + version + ")";
        }
    }

.. tip::

   먼저 이 「컴포넌트 추가」를 검토하십시오. 코어 기능을 변경할 필요가
   없는 한, 교체보다 안전하고 유지보수성이 뛰어납니다.

코어 컴포넌트 교체(fess+componentName.xml)
-------------------------------------------

|Fess| 본체 컴포넌트의 동작을 변경하고 싶은 경우, 대상 클래스를
서브클래스화하고 ``<baseDicon>+<componentName>.xml`` 이라는 이름의 DI
설정 파일로 **동일한 컴포넌트 이름으로 재등록** 합니다. 예를 들어
``systemHelper`` 는 |Fess| 본체의 ``fess.xml`` 에서 선언되어 있으므로,
교체 파일은 ``fess+systemHelper.xml`` 이 됩니다(``app+systemHelper.xml``
이 아닙니다).

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import java.nio.file.Path;

    import org.codelibs.fess.helper.SystemHelper;

    public class CustomSystemHelper extends SystemHelper {

        @Override
        protected void parseProjectProperties(final Path propPath) {
            try {
                super.parseProjectProperties(propPath);
            } catch (final Exception e) {
                // 자체 처리
            }
            System.setProperty("fess.webapp.plugin", "true");
        }
    }

.. warning::

   교체(단일 ``+``)는 컴포넌트 정의를 **통째로** 교체합니다. 이 때문에
   교체 파일에는 코어 정의가 수행하고 있는 ``<postConstruct>`` 를 모두
   기술해야 합니다(예: ``app.xml`` 의 ``queryHelper``). 이는 |Fess|
   릴리스마다 동기화해야 합니다. 코어에서 삭제된 메서드를 계속 호출하면, 그
   컴포넌트 정의는 ``BeanMethodNotFoundException`` 으로 초기화에 실패합니다.
   예를 들어 15.9 에서는 ``systemHelper`` 의 ``addDesignJspFileName`` 이
   삭제되었기 때문에, 이를 호출하는 교체 파일은 실패합니다. 이러한 유지보수
   비용이 교체보다 추가가 권장되는 이유입니다.

REST API 추가(fess_api++.xml)
-------------------------------

새로운 REST API 엔드포인트를 추가하려면 ``WebApiManager`` 를 구현합니다.
``BaseApiManager`` 를 상속하고, ``@PostConstruct`` 에서
``WebApiManagerFactory`` 에 자신을 등록합니다. 등록된 API 매니저는
요청마다 ``WebApiFilter`` 에서 호출됩니다. ``fess_api++.xml`` 에서
컴포넌트를 등록합니다:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleApiManager"
            class="org.codelibs.fess.webapp.example.api.ExampleApiManager">
        </component>
    </components>

.. code-block:: java

    package org.codelibs.fess.webapp.example.api;

    import java.io.IOException;

    import org.codelibs.fess.api.BaseApiManager;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;
    import jakarta.servlet.FilterChain;
    import jakarta.servlet.ServletException;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;

    public class ExampleApiManager extends BaseApiManager {

        public ExampleApiManager() {
            // 이 매니저가 처리하는 경로의 프리픽스
            setPathPrefix("/api/example");
        }

        @PostConstruct
        public void register() {
            ComponentUtil.getWebApiManagerFactory().add(this);
        }

        @Override
        public boolean matches(final HttpServletRequest request) {
            // 이 매니저가 요청을 처리할지 여부를 판정
            return request.getServletPath().startsWith(pathPrefix);
        }

        @Override
        public void process(final HttpServletRequest request, final HttpServletResponse response,
                final FilterChain chain) throws IOException, ServletException {
            // 요청 처리 및 응답 작성
        }

        @Override
        protected void writeHeaders(final HttpServletResponse response) {
            // 응답 헤더 설정(필요한 경우)
        }
    }

구현 예로는 ``/api/v1`` 을 제공하는
`fess-webapp-v1-api <https://github.com/codelibs/fess-webapp-v1-api>`__ 나,
``/json`` / ``/suggest`` 를 제공하는
`fess-webapp-classic-api <https://github.com/codelibs/fess-webapp-classic-api>`__
가 참고가 됩니다.

.. _webapp-plugin-password-encoder:

비밀번호 해시 알고리즘 추가(fess++.xml)
---------------------------------------

로컬 사용자의 비밀번호 해시는 컴포넌트가 만듭니다. 저장된 비밀번호는 ``{id}hash`` 형식입니다. |Fess| 는 저장된 값의 ``id`` 와, 새 비밀번호의 경우 ``app.password.algorithm`` 의 값(기본값은 ``bcrypt`` )으로 DI 컴포넌트 ``<id>PasswordEncoder`` 를 찾습니다. ``<sso.type>Authenticator`` 와 ``<storage.type>StorageClient`` 를 해석하는 방식과 같습니다. |Fess| 는 ``bcryptPasswordEncoder`` 를 직접 등록합니다. 알고리즘을 추가하려면 ``org.codelibs.fess.crypto.password.PasswordEncoder`` 를 구현하고 그 클래스를 ``fess++.xml`` 에 등록합니다. ``fess++.xml`` 은 Lasta Di가 |Fess| 코어의 ``fess.xml`` 에 병합합니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="argon2PasswordEncoder"
            class="com.example.Argon2PasswordEncoder">
        </component>
    </components>

인터페이스에는 다음 메서드가 있습니다.

.. list-table:: PasswordEncoder의 메서드
   :header-rows: 1
   :widths: 35 65

   * - 메서드
     - 설명
   * - ``String encode(String rawPassword)``
     - 비밀번호를 해시합니다. 결과는 |Fess| 가 붙이는 ``{id}`` 접두사 뒤에 저장됩니다. 원래 비밀번호를 충실히 해시할 수 없는 비밀번호에는 ``IllegalArgumentException`` 을 던지십시오. 메시지에 비밀번호를 포함해서는 안 됩니다.
   * - ``boolean matches(String rawPassword, String encodedPassword)``
     - 이 인코더가 만든 해시에 대해 비밀번호를 검증합니다. 비밀번호가 틀렸거나 해시 형식이 잘못된 경우 ``false`` 를 반환하십시오.
   * - ``boolean needsUpgrade(String encodedPassword)``
     - 선택 사항(기본값 ``false`` ). 저장된 해시가 현재 ``encode`` 가 만드는 것보다 약한지를 반환합니다. ``true`` 이면 그 사용자의 다음 로그인 때 해시를 다시 만듭니다. BCrypt는 비용이 ``app.password.bcrypt.cost`` 보다 낮으면 ``true`` 를 반환합니다.
   * - ``int getMaxPasswordBytes()``
     - 선택 사항(기본값 ``0`` 이며 제한 없음). ``encode`` 가 받아들이는 비밀번호의 최대 길이(UTF-8 바이트)입니다. BCrypt는 ``72`` 를 반환합니다.
   * - ``boolean isVerificationCostly()`` 와 ``void applyTimingPadding()``
     - 선택 사항(기본값은 ``false`` 와 아무것도 하지 않음). 의도적으로 느린 알고리즘은 ``true`` 를 반환하고 ``applyTimingPadding()`` 에서 ``matches`` 한 번 정도의 시간을 사용합니다. |Fess| 는 해시를 검증하지 않은 채 로그인이 실패했을 때(예: 존재하지 않는 사용자) 이것을 호출하므로, 응답 시간으로 사용자의 존재 여부를 알 수 없습니다.

인코더를 사용하려면 다음과 같이 합니다.

#. jar를 ``WEB-INF/plugin`` 디렉터리에 둡니다. 웹앱 플러그인과 마찬가지로 매니페스트에 ``Fess-WebAppJar: true`` 가 필요합니다("pom.xml과 매니페스트" 참조). 이것이 없으면 컴포넌트를 찾을 수 없습니다.
#. ``fess_config.properties`` 의 ``app.password.algorithm`` 에 ID를 설정합니다( ``argon2PasswordEncoder`` 라면 ``argon2`` ). ID는 소문자여야 하며 ``}`` 를 포함해서는 안 됩니다. 이후 새로 설정하거나 변경한 비밀번호는 이 인코더로 해시됩니다. 다른 ID로 저장된 비밀번호나 ID가 없는 이전 해시는 ``app.password.upgrade.enabled`` 가 ``true`` (기본값)인 동안, 그 사용자의 다음 로그인 성공 시 해시를 다시 만듭니다.

다음 사항에 유의하십시오.

- 인코더는 모든 스레드가 공유하는 싱글턴이므로 스레드 안전해야 합니다.
- 길이 제한은 인코더의 것입니다. 비밀번호를 설정할 때(사용자 관리 화면, 강제 비밀번호 변경, ``/api/v2/auth/password`` , Admin API), |Fess| 는 ``app.password.algorithm`` 알고리즘의 ``getMaxPasswordBytes()`` 보다 긴 비밀번호를 "비밀번호는 N바이트 이하여야 합니다."로 거부합니다. ``0`` 이하이면 ``password.max.length`` 만 확인합니다. 저장된 해시를 검증할 때 |Fess| 는 길이 제한을 적용하지 않습니다. 더 긴 비밀번호가 일치해도 되는지는 ``matches`` 가 정합니다.
- 그 ID로 저장된 비밀번호가 있는 동안에는 플러그인을 설치해 두십시오. 컴포넌트가 없으면 그 ID의 해시는 어떤 비밀번호와도 일치하지 않으므로 해당 사용자는 로그인할 수 없고, 해시도 다시 만들어지지 않습니다.
- ``app.password.algorithm`` 에 컴포넌트가 없는 ID를 지정한 경우(예: 플러그인 jar를 삭제한 뒤), |Fess| 는 시작되고 다른 ID의 해시를 가진 사용자는 계속 로그인할 수 있지만, 비밀번호 설정은 ``app.password.algorithm`` 을 지목하는 오류로 실패합니다.

검색 화면 커스터마이즈
======================

웹앱 플러그인은 JSP 뷰를 추가할 수 없습니다. JSP 뷰는 |Fess| 본체 WAR 의
``WEB-INF/view/`` 에 배치되어 있으며, 플러그인 JAR 는 클래스패스
(``WEB-INF/classes``)에 마운트되기 때문입니다. 검색 화면의 디자인을
변경하려면 테마를 사용합니다. 테마는 검색 화면의 디자인
(HTML/CSS/JavaScript)을 커스터마이즈합니다. :doc:`theme-development` 를
참조하십시오.

빌드와 설치
===========

::

    mvn clean package

``target/`` 디렉터리에 JAR 파일(예: ``fess-webapp-example-15.10.0.jar``)이
생성됩니다. 생성한 JAR 는 관리 화면에서 설치하거나, ``app/WEB-INF/plugin/``
디렉터리에 배치하고 |Fess| 를 재시작합니다. 설치 절차의 자세한 내용은
:doc:`../admin/plugin-guide` 를 참조하십시오.

공개 플러그인 예
================

|Fess| 프로젝트에서는 다음의 웹앱 플러그인이 공개되어 있습니다.
개발 참고용으로 `GitHub <https://github.com/codelibs>`__ 에 공개되어
있습니다:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 플러그인
     - 설명
   * - ``fess-webapp-example``
     - 플러그인 구현의 템플릿
   * - ``fess-webapp-v1-api``
     - ``/api/v1`` REST API
   * - ``fess-webapp-classic-api``
     - ``/json`` / ``/suggest`` 레거시 REST API
   * - ``fess-webapp-mcp``
     - MCP(Model Context Protocol) 서버
   * - ``fess-webapp-bangs``
     - DuckDuckGo 방식의 뱅(``!g``). 다른 사이트로 검색을 보냄
   * - ``fess-webapp-semantic-search``
     - 뉴럴 검색/벡터 검색(사용 중단됨; 15.8의 코어 통합 기능으로 대체됨)
   * - ``fess-webapp-multimodal``
     - 멀티모달(이미지·텍스트) 검색

참고 정보
=========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`theme-development` - 테마 커스터마이즈
- :doc:`../admin/plugin-guide` - 플러그인 설치
- :doc:`overview` - 개발자 문서 개요
