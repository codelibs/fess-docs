====================
OGNL 스크립트 가이드
====================

개요
====

OGNL(Object-Graph Navigation Language)은 |Fess|\ 에서 사용할 수 있는 스크립트 엔진 중 하나입니다.
``fess-script-ognl`` 플러그인으로 제공되며, 식별자는 ``ognl`` 입니다.

OGNL 스크립트는 ``title + " - " + siteName`` 이나 ``content.length() > 0`` 과 같은
하나의 값 식입니다. 문(statement), 제어 구문, ``return`` 이 없습니다. 필드 매핑,
문서 부스트, 경로 매핑처럼 짧은 식으로 충분한 용도에 적합합니다.
문이나 반복이 필요한 스크립트에는 :doc:`scripting-javascript` 또는 :doc:`scripting-groovy`\ 를 사용하세요.

.. important::
   플러그인은 **배포물에 동봉되지 않습니다**. 관리 화면의 「시스템 > 플러그인」
   페이지에서 설치하거나 ``bin/fess-setup install plugin fess-script-ognl`` 을
   실행하세요. 수동으로 설치할 경우, JAR 파일(예: ``fess-script-ognl-15.10.0.jar`` )을
   ``app/WEB-INF/plugin/``\ 에 배치하고 |Fess|\ 를 재시작합니다.

OGNL 선택
=========

OGNL은 스크립트 타입으로 명시적으로 선택한 곳에서만 사용됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 위치
     - OGNL 선택 방법
   * - 데이터 스토어
     - 데이터 스토어 설정의 파라미터에 ``script_type=ognl`` 을 추가합니다
   * - 웹 크롤링·파일 크롤링
     - 설정 파라미터에 ``config.script.type=ognl`` 을 추가하고, 필드 스크립트를
       ``field.script.<필드명>=<식>`` 형식으로 작성합니다
   * - 문서 부스트 규칙
     - 규칙의 스크립트 타입을 ``ognl`` 로 설정합니다(스크립트 타입은 규칙마다 가집니다)
   * - 경로 매핑
     - 치환 문자열을 ``ognl:`` 로 시작합니다. 식의 결과가 치환 후 URL이 되며, 원래 URL과
       ``Matcher`` 는 ``url`` 과 ``matcher`` 로 참조할 수 있습니다
   * - 스케줄 작업
     - 작업의 스크립트 타입을 ``ognl`` 로 설정합니다. 작업은 보통 절차를 기술하는 것이라
       하나의 식으로는 표현할 수 없습니다

식 작성 방법
============

데이터 스토어와 필드 스크립트는 한 줄에 하나의 ``필드명=식`` 을 작성합니다.
각 파라미터는 ``name`` 과 ``#name`` 어느 쪽으로도 참조할 수 있습니다.

::

    title=title
    content=content.trim()
    digest=content.length() > 200 ? content.substring(0, 200) + "..." : content

OGNL은 Groovy의 부분집합이 아닙니다. 스크립트를 이식할 때는 다음 사항에 주의하세요.

- ``return``, 문, ``if`` / ``for`` 가 없습니다. 삼항 연산자 ``cond ? a : b`` 를 사용합니다.
- 엘비스 연산자 ``?:`` 와 안전 탐색 연산자 ``?.`` 는 사용할 수 없습니다.
  ``a != null ? a.b : null`` 과 같이 작성합니다.
- ``"x${id}"`` 는 오류가 되지 않으며 전개도 되지 않습니다. 리터럴 문자열 ``x${id}`` 로
  평가되므로 필드에 잘못된 텍스트가 인덱싱됩니다. 연결에는 ``+`` 를 사용하세요.

설정
====

엔진은 다음 키를 ``system.properties`` 또는 JVM 시스템 프로퍼티
``-Dfess.system.<키>`` 에서 읽습니다. 양쪽에 모두 있으면 ``system.properties`` 가 우선합니다.
``system.properties`` 는 ZIP 버전에서는 ``app/WEB-INF/conf/system.properties``,
RPM·DEB 버전에서는 ``/etc/fess/system.properties`` 입니다.

.. important::
   키는 시작 시 엔진이 초기화될 때 한 번만 읽힙니다.
   값을 변경한 후에는 |Fess|\ 를 재시작하세요. 실행 중인 프로세스에는 반영되지 않습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 키
     - 기본값
     - 설명
   * - ``script.ognl.mode``
     - ``compat``
     - ``compat`` 또는 ``strict`` 입니다. 다음 섹션을 참조하세요. 그 외의 값은
       경고를 로그에 기록하고 ``compat`` 로 취급합니다
   * - ``script.ognl.allowed.classes``
     - 아래 참조
     - 허용할 클래스의 쉼표 구분 목록. ``strict`` 모드에서만 사용됩니다
   * - ``script.ognl.denied.packages``
     - 아래 참조
     - 호출을 거부할 선언 클래스의 쉼표 구분 목록. ``strict`` 모드에서만 사용됩니다
   * - ``script.ognl.cache.size``
     - ``1000``
     - 구문 분석한 식을 캐시하는 최대 개수. 최솟값은 ``1`` 입니다
   * - ``script.ognl.expression.max.length``
     - ``4000``
     - 식의 최대 문자 수. 이보다 긴 식은 평가되지 않고 실패합니다. 최솟값은 ``1`` 입니다
   * - ``script.ognl.max.log.length``
     - ``200``
     - 로그 메시지에 기록하는 식의 최대 문자 수. 최솟값은 ``3`` 입니다

정수가 아닌 값은 경고를 남기고 무시되며 기본값이 사용됩니다. 최솟값보다 작은 값은 경고를 남기고
최솟값으로 올려집니다.

compat 모드와 strict 모드
=========================

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - ``compat`` (기본값)
     - ``strict``
   * - DI 컨테이너
     - ``container`` 로 참조할 수 있습니다
     - 참조할 수 없습니다(``container`` 는 ``null`` 로 평가됩니다)
   * - 클래스
     - ``@임의.클래스@메서드(...)`` 로 모든 클래스에 접근할 수 있습니다
     - ``script.ognl.allowed.classes`` 에 포함된 클래스에만 접근할 수 있습니다
   * - 멤버
     - 제한 없음
     - ``script.ognl.denied.packages`` 의 클래스가 선언한 멤버는 호출할 수 없습니다.
       public이 아닌 멤버는 항상 거부됩니다

``compat`` 는 기존 설정의 동작을 유지합니다. ``strict`` 모드에서는
``@java.lang.System@getProperty("user.name")`` 이나 ``new java.io.File("/etc/hosts")`` 와 같은
식이 거부됩니다. 거부된 식은 ``null`` 로 평가되는 것이 아니라, 경고가 로그에 기록되고
평가가 오류로 실패합니다.

엔진은 시작 시 유효한 모드를 ``INFO`` 레벨로 로그에 기록합니다
(``ognl script engine: mode=strict, ...``). ``strict`` 가 적용되었는지는 이 줄로 확인하세요.

허용 목록
---------

``script.ognl.allowed.classes`` 는 정규화된 클래스 이름과의 완전 일치, 또는 패키지명·클래스명에
``.`` 를 붙인 전방 일치로 판정합니다. 예를 들어 ``java.time`` 은 ``java.time.LocalDate`` 를 포함한
이 패키지 아래의 모든 클래스를 허용합니다. 기본값은 다음과 같습니다.

``java.lang.Math``, ``java.lang.String``, ``java.lang.Boolean``, ``java.lang.Integer``,
``java.lang.Long``, ``java.lang.Float``, ``java.lang.Double``, ``java.lang.Number``,
``java.util.Date``, ``java.util.Arrays``, ``java.util.List``, ``java.util.Map``,
``java.util.Set``, ``java.util.Collections``, ``java.math.BigDecimal``, ``java.time``,
``org.codelibs.core.lang.StringUtil``, ``org.codelibs.fess.util.DocumentUtil``,
``org.codelibs.fess.taglib.FessFunctions``

중첩 클래스의 이름에는 ``$`` 가 포함되며(예: ``java.util.Map$Entry``), 바깥 클래스의 이름으로는
허용되지 않습니다. 필요한 경우 ``$`` 를 포함한 이름을 목록에 추가하세요.

거부 목록
---------

``script.ognl.denied.packages`` 는 멤버를 선언한 클래스의 이름이 항목 중 하나로 시작하면
그 멤버를 거부합니다. 기본값은 다음과 같습니다.

``java.io``, ``java.nio``, ``java.net``, ``java.lang.reflect``, ``java.lang.invoke``,
``java.lang.System``, ``java.lang.Class``, ``java.lang.Runtime``, ``java.lang.ProcessBuilder``,
``java.lang.Process``, ``java.lang.Thread``, ``java.lang.ClassLoader``, ``javax.script``,
``jdk.``, ``sun.``, ``org.lastaflute.di``

.. note::
   설정한 값은 기본 목록에 추가되는 것이 아니라 기본 목록을 대체합니다. 허용 목록에 클래스를
   하나 추가하려면 기본 항목과 새 항목을 함께 작성하세요.

.. warning::
   ``strict`` 모드가 제한하는 것은 식이 접근할 수 있는 클래스와 멤버입니다. 식에 전달되는
   객체로부터 식을 격리하는 것은 아닙니다. |Fess|\ 의 헬퍼나 엔티티가 파라미터로 전달되면
   어느 모드에서든 그 public 메서드를 식에서 호출할 수 있습니다.
