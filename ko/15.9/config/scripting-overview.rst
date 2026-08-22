==================================
스크립팅 개요
==================================

개요
====

|Fess|\ 에서는 다양한 장면에서 스크립트를 사용하여 커스텀 로직을 구현할 수 있습니다.
스크립트를 활용하면 크롤링 시 데이터 가공, URL 변환,
스케줄 작업 실행 등을 유연하게 제어할 수 있습니다.

지원 스크립트 언어
==================

|Fess|\ 는 다음 스크립트 언어를 지원합니다:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 언어
     - 식별자
     - 설명
   * - Groovy
     - ``groovy``
     - 기본으로 등록된 스크립트 언어. Java 호환으로 강력한 기능 제공

.. note::
   |Fess|\ 에 기본으로 등록된 스크립트 엔진은 Groovy뿐입니다.
   기본 스크립트 언어는 ``groovy``\ 입니다（ ``Constants.DEFAULT_SCRIPT`` ）.
   이 문서의 스크립트 예제는 모두 Groovy 구문으로 작성되어 있습니다.

스크립트 사용 장면
==================

데이터 스토어 설정
------------------

데이터 스토어 커넥터에서는 가져온 데이터를 인덱스 필드에 매핑하기 위해
스크립트를 사용합니다. 설정은 ``필드명=식`` 형식으로 한 줄씩 기술하며,
각 줄은 독립된 하나의 Groovy 식으로 평가됩니다.

::

    url=site_url
    title=name
    content=description
    last_modified=updated_at

데이터 스토어 스크립트에서 참조할 수 있는 변수명은 커넥터 종류에 따라 다릅니다.
예를 들어 CSV 데이터 스토어나 JSON 데이터 스토어에서는 각 컬럼명·필드명을
그대로 변수로 사용할 수 있습니다（ ``data`` 와 같은 공통 접두사는 붙지 않습니다）.
파일 계열 커넥터（Box, Google Drive, OneDrive 등）에서는 ``file.*``,
Slack에서는 ``message.*`` 등 커넥터마다 접두사가 다릅니다.
사용 가능한 변수의 자세한 내용은 각 데이터 스토어 커넥터 문서를 참조하세요.

.. note::
   데이터 스토어의 각 줄은 하나의 식으로 평가되기 때문에, 여러 줄에 걸친
   ``if`` 블록이나 ``import`` 문, ``def`` 에 의한 변수 선언은 사용할 수 없습니다.
   조건에 따라 값을 변경할 경우에는 필드마다 삼항 연산자를 사용하세요
   （예: ``title=enabled == "true" ? name : null`` ）. 클래스를 참조할 경우에는
   완전 한정 이름（FQCN）을 인라인으로 기술합니다.

경로 매핑
---------

경로 매핑은 크롤링 대상 URL을 정규화·변환하기 위한 기능입니다.
기본적으로는 「정규 표현식」과 「치환 문자열」의 쌍으로 설정하며, Groovy 스크립트가 아닙니다.
예를 들어 정규 표현식에 ``http://``, 치환 문자열에 ``https://``\ 를 지정하면
URL의 스킴을 교체할 수 있습니다.

치환 문자열 앞에 ``groovy:``\ 를 붙인 경우에 한해, 이후 문자열이 Groovy 스크립트로
평가됩니다. 이 스크립트 내에서는 변환 대상 URL 문자열을 나타내는 ``url``\ 과,
정규 표현식의 ``java.util.regex.Matcher``\ 를 나타내는 ``matcher``\ 를 사용할 수 있습니다.

::

    groovy:url.replaceAll("http://", "https://")

스케줄 작업
-----------

스케줄 작업에서는 커스텀 처리 로직을 Groovy 스크립트로 작성할 수 있습니다.
스크립트 전체가 하나의 Groovy 스크립트로 평가되기 때문에,
여러 줄 기술이나 ``import`` 문, ``def``\ 에 의한 변수 선언도 사용할 수 있습니다.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

``logLevel("info")`` 등의 메서드는 작업 클래스（ ``ExecJob`` 및 그 서브클래스）의
메서드이며, 메서드 체인으로 기술할 수 있습니다. ``executor`` 변수에 대해서는
「실행 컨텍스트와 사용 가능한 객체」를 참조하세요.

기본 구문
=========

다음은 Groovy의 기본 구문 예제입니다. 주석은 ``//``\ （줄 주석）또는
``/* */``\ （블록 주석）을 사용합니다. ``#``\ 으로 시작하는 주석은 Groovy에서
사용할 수 없다는 점에 주의하세요.

변수 접근
---------

::

    // 데이터 스토어의 필드（CSV/JSON에서는 컬럼명·필드명으로 접근）
    title

    // DI 컨테이너에서 컴포넌트 취득
    container.getComponent("systemHelper")

문자열 조작
-----------

::

    // 연결
    title + " - " + category

    // 치환
    content.replaceAll("old", "new")

    // 분할
    tags.split(",")

조건 분기
---------

::

    // 삼항 연산자
    status == "active" ? "유효" : "무효"

    // null/빈 값인 경우의 기본값（Elvis 연산자）
    description ?: "설명 없음"

날짜 조작
---------

::

    // 현재 날짜/시간
    new Date()

    // 포맷
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(updated_at)

실행 컨텍스트와 사용 가능한 객체
=================================

스크립트 내에서 사용할 수 있는 객체는 스크립트를 실행하는 컨텍스트에 따라
다릅니다. ``container``\ 만이 모든 컨텍스트에서 사용 가능합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - 실행 컨텍스트
     - 사용 가능한 객체
     - 설명
   * - 모든 컨텍스트
     - ``container``
     - DI 컨테이너. ``container.getComponent("systemHelper")`` 나
       ``container.getComponent("fessConfig")`` 로 각 컴포넌트에 접근 가능
   * - 데이터 스토어 스크립트
     - 커넥터 고유의 필드 변수
     - 데이터 스토어에서 가져온 각 필드가 변수로 사용 가능
       （변수명·접두사는 커넥터에 따라 다름. CSV/JSON은 필드명이 그대로 변수가 됨）
   * - 경로 매핑
     - ``url`` ``matcher``
     - 변환 대상 URL 문자열과 정규 표현식의 ``Matcher``\ （ ``groovy:`` 접두사 부가 시의 치환에서만）
   * - 스케줄 작업
     - ``executor``
     - 작업 실행 인스턴스（ ``JobExecutor`` ）. 작업의 셧다운 제어에 사용

.. note::
   ``container`` 이외의 객체는 특정 컨텍스트에서만 주입됩니다.
   예를 들어 ``executor``\ 는 스케줄 작업에서만 사용 가능하며, 데이터 스토어 스크립트나
   경로 매핑에서는 사용할 수 없습니다.

보안
====

.. warning::
   스크립트는 강력한 기능을 갖기 때문에 신뢰할 수 있는 소스에서만 사용하세요.

- 스크립트는 서버에서 실행됩니다
- 파일 시스템이나 네트워크에 접근할 수 있습니다
- 관리자 권한을 가진 사용자만 스크립트를 편집할 수 있도록 하세요
- 스크립트 실행은 감사 로그（ ``audit.log`` ）에 기록됩니다.
  기록 여부는 ``script.audit.log.enabled``\ 로 제어하며 기본값은 ``true``\ 입니다.
  기록되는 스크립트 문자열의 최대 길이는 ``script.audit.log.max.length``\ 로 제어하며
  기본값은 ``100``\ 자입니다.

성능
====

스크립트 성능을 최적화하기 위한 팁:

1. **복잡한 처리 피하기**: 데이터 스토어 스크립트는 문서마다 실행됩니다
2. **외부 리소스 접근 최소화**: 네트워크 호출은 지연의 원인이 됩니다
3. **캐시 활용**: 반복적으로 사용하는 값은 캐시를 검토

디버그
======

스케줄 작업의 스크립트에서는 스크립트 전체가 하나의 Groovy 스크립트로
평가되기 때문에 로그 출력을 활용하여 디버깅할 수 있습니다.
（데이터 스토어 스크립트는 한 줄이 하나의 식으로 평가되기 때문에 ``import`` 문이나
여러 줄의 처리는 사용할 수 없습니다.）

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("fess.script")
    logger.info("executor = {}", executor)

위 예제에서는 ``fess.script``\ 라는 이름의 로거를 사용합니다.
이 로그를 출력하려면 ``app/WEB-INF/classes/log4j2.xml``\ 에 해당 로거 설정을
추가합니다.

::

    <Logger name="fess.script" level="DEBUG"/>

또한 스크립트 엔진 자체의 디버그 로그를 활성화하려면 ``org.codelibs.fess.script``
패키지의 로그 레벨을 ``DEBUG``\ 로 설정합니다.

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

참고 정보
=========

- :doc:`scripting-groovy` - Groovy 스크립트 가이드
- :doc:`../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../admin/scheduler-guide` - 스케줄러 설정 가이드
