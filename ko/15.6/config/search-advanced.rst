===========
검색 관련 설정
===========

다음 설명의 설정은 fess_config.properties 에서 지정합니다.
변경 후에는 |Fess| 의 재시작이 필요합니다.

퍼지 검색
=========

4자 이상은 퍼지 검색이 적용되어 1자 차이도 히트합니다.
이 설정을 비활성화하려면 `-1` 을 지정합니다.
::

    query.boost.fuzzy.min.length=-1

검색 시 타임아웃 값
=================

검색 시 타임아웃 값을 지정할 수 있습니다.
기본값은 10초입니다.
::

    query.timeout=10000

검색 시 최대 문자 수
==============

검색 시 최대 문자 수를 지정할 수 있습니다.
기본값은 1000자입니다.
::

    query.max.length=1000

검색 시 타임아웃 로그 출력
=======================

검색 시 타임아웃된 경우의 로그 출력 설정입니다.
기본값은 `true(활성화)` 입니다.
::

    query.timeout.logging=true

히트 건수 표시
===========

10,000건 이상의 히트 건수 표시가 필요한 경우에 지정합니다.
기본값에서는 10,000건 이상 히트하는 경우 다음과 같은 표시가 됩니다.

`xxxxx 의 검색 결과 약 10,000 건 이상 1 - 10 건째 (4.94 초)`

::

    query.track.total.hits=10000

위치 정보 검색 시 인덱스명
=======================

위치 정보 검색 시 인덱스명을 지정합니다.
기본값은 `location` 입니다.
::

    query.geo.fields=location

요청 매개변수의 언어 지정
=======================

요청 매개변수로 언어를 지정하는 경우의 매개변수명을 지정합니다.
예를 들어 요청 매개변수로 `browser_lang=en` 과 같이 URL로 전달하면 화면의 표시 언어가 영어로 전환됩니다.
::

    query.browser.lang.parameter.name=browser_lang

전방 일치 검색 지정
==============

완전 일치 검색 시 `〜\*` 로 지정한 경우 전방 일치 검색으로 검색합니다.
기본값은 `true(활성화)` 입니다.
::

    query.replace.term.with.prefix.query=true

하이라이트 문자열
==============

여기서 지정한 문자열로 문장을 구분하여 자연스러운 형태의 하이라이트 표시를 구현합니다.
지정하는 문자열은 u를 시작 구분 문자로 하는 Unicode 문자로 합니다.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

기본값은 다음과 같이 설정되어 있습니다. (디코드 변환한 것입니다)

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

하이라이트 프래그먼트
==================

OpenSearch에서 가져오는 하이라이트 프래그먼트의 문자 수나 프래그먼트 수를 지정합니다.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

하이라이트 생성 방법
==============

OpenSearch의 하이라이트 생성 방법을 지정합니다.
::

    query.highlight.type=fvh

하이라이트 대상 태그
===============

하이라이트 대상의 시작 및 종료 태그를 지정합니다.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

OpenSearch 하이라이터에 전달할 값
===========================

OpenSearch 하이라이터에 전달할 값을 지정합니다.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

응답에 추가할 필드명
========================

일반 검색 또는 API 검색 시 응답에 추가할 필드명을 지정합니다.
::

    query.additional.response.fields=
    query.additional.api.response.fields=

필드명 추가
==============

검색 필드명이나 패싯 필드명을 추가할 때 지정합니다.
::

    query.additional.search.fields=
    query.additional.facet.fields=

검색 결과를 GSA 호환 XML 형식으로 가져올 때의 설정
===================================

검색 결과를 GSA 호환 XML 형식으로 가져올 때 사용합니다.

GSA 호환 XML 형식을 사용할 때 응답에 추가할 필드명을 지정.
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

GSA 호환 XML 형식을 사용할 때의 언어를 지정.
    ::

        query.gsa.default.lang=en

GSA 호환 XML 형식을 사용할 때 기본 정렬을 지정.
    ::

        query.gsa.default.sort=
