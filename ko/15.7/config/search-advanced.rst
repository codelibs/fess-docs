===========
검색 관련 설정
===========

다음 설명의 설정은 fess_config.properties 에서 지정합니다.
변경 후에는 |Fess| 의 재시작이 필요합니다.

퍼지 검색
=========

4자 이상은 퍼지 검색이 적용되어 1자 차이도 히트합니다.
이 설정을 비활성화하려면 ``-1`` 을 지정합니다.
::

    query.boost.fuzzy.min.length=-1

기본값은 ``4`` 입니다. 퍼지 검색의 상세 설정에 대해서는 뒤에서 설명하는 「관련도(부스트) 설정」을 참조하십시오.

검색 시 타임아웃 값
=================

검색 시 타임아웃 값을 밀리초 단위로 지정할 수 있습니다.
기본값은 10초(10000밀리초)입니다.
::

    query.timeout=10000

검색 시 최대 문자 수
==============

검색 쿼리의 최대 문자 수를 지정할 수 있습니다.
이 값을 초과하는 길이의 검색 쿼리는 허용되지 않습니다.
기본값은 1000자입니다.
::

    query.max.length=1000

검색 시 타임아웃 로그 출력
=======================

검색 시 타임아웃된 경우의 로그 출력 설정입니다.
기본값은 ``true`` (활성화)입니다.
::

    query.timeout.logging=true

히트 건수 표시
===========

정확하게 집계하는 히트 건수의 상한을 지정합니다.
기본값에서는 10,000건 이상 히트하는 경우 다음과 같은 표시가 됩니다.

``xxxxx 의 검색 결과 약 10,000 건 이상 1 - 10 건째 (4.94 초)``

10,000건을 초과하는 정확한 히트 건수 표시가 필요한 경우에 더 큰 값을 지정합니다.
::

    query.track.total.hits=10000

.. note::
   큰 값을 설정하면 검색 성능에 영향을 줄 수 있습니다. 사용 상황에 맞게 적절한 값을 설정하십시오.

검색 결과의 최대 오프셋
==================

검색 결과로 취득할 수 있는 오프셋(검색 시작 위치)의 상한을 지정합니다.
이 값을 초과하는 오프셋이 지정된 경우 검색 오류가 발생합니다.
페이징에서 깊은 페이지까지 이동하는 경우의 상한값으로 동작합니다.
기본값은 100000입니다.
::

    query.max.search.result.offset=100000

OR 검색에 의한 재검색 임계값
=====================

일반 검색에서의 히트 건수가 여기서 지정한 값 이하인 경우 검색 연산자를 OR 로 전환하여 재검색을 실행합니다.
이를 통해 AND 검색에서 히트 건수가 적은 경우에도 결과를 보완할 수 있습니다.
기본값은 ``-1`` 로, 이 기능은 비활성화됩니다.
::

    query.orsearch.min.hit.count=-1

위치 정보 검색 시 필드명
=====================

위치 정보 검색 시 대상으로 하는 필드명을 지정합니다.
여러 필드를 지정하는 경우 쉼표로 구분하여 지정합니다.
기본값은 ``location`` 입니다.
::

    query.geo.fields=location

위치 정보 검색의 사용 방법에 대해서는 :doc:`search-geosearch` 를 참조하십시오.

요청 매개변수의 언어 지정
=======================

요청 매개변수로 언어를 지정하는 경우의 매개변수명을 지정합니다.
예를 들어 요청 매개변수로 ``browser_lang=en`` 과 같이 URL 로 전달하면 화면의 표시 언어가 영어로 전환됩니다.
::

    query.browser.lang.parameter.name=browser_lang

검색 대상 기본 언어
==================

검색 시 대상으로 하는 기본 언어를 쉼표로 구분하여 지정합니다.
값이 설정되어 있는 경우 요청 매개변수나 브라우저의 언어보다 우선하여 사용됩니다.
기본값은 비어 있음(미지정)으로, 요청 매개변수 또는 브라우저의 언어가 사용됩니다.
::

    query.default.languages=

언어 코드 매핑
=================

검색 시 사용하는 언어 코드의 정규화 매핑을 지정합니다.
브라우저나 요청에서 전달된 언어 코드를 |Fess| 가 내부적으로 사용하는 언어 코드로 변환합니다.
일반적으로 변경할 필요는 없습니다. 기본값에는 주요 언어의 매핑이 정의되어 있습니다.
::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    ...

전방 일치 검색 지정
==============

검색어 끝에 ``*`` 를 붙인 경우(예: ``검색*``), 해당 어구를 전방 일치 쿼리로 검색합니다.
기본값은 ``true`` (활성화)입니다. ``false`` 를 지정하면 ``*`` 를 끝에 가진 어구도 그대로 검색합니다.
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

OpenSearch 에서 가져오는 하이라이트 프래그먼트의 문자 수나 프래그먼트 수를 지정합니다.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

하이라이트 생성 방법
==============

OpenSearch 의 하이라이트 생성 방법을 지정합니다.
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

고급 하이라이트 설정
==================

하이라이트의 세부 동작을 제어하기 위한 설정입니다.
::

    query.highlight.force.source=false
    query.highlight.fragmenter=span
    query.highlight.fragment.offset=-1
    query.highlight.no.match.size=0
    query.highlight.order=score
    query.highlight.phrase.limit=256
    query.highlight.content.description.fields=hl_content,digest
    query.highlight.boundary.position.detect=true
    query.highlight.text.fragment.type=query
    query.highlight.text.fragment.size=3
    query.highlight.text.fragment.prefix.length=5
    query.highlight.text.fragment.suffix.length=5

응답에 추가할 필드명
========================

일반 검색 또는 API 검색 시 응답에 추가할 필드명을 지정합니다.
각각 일반 검색, API(JSON/GSA) 검색, 스크롤 검색, 캐시 표시 시의 응답에 대응합니다.
::

    query.additional.response.fields=
    query.additional.api.response.fields=
    query.additional.scroll.response.fields=
    query.additional.cache.response.fields=

스크롤 검색의 응답 필드에 대한 자세한 내용은 :doc:`search-scroll` 을 참조하십시오.

필드명 추가
==============

검색 필드명이나 패싯 필드명, 정렬 대상 필드명 등을 추가할 때 지정합니다.
::

    query.additional.default.fields=
    query.additional.search.fields=
    query.additional.facet.fields=
    query.additional.sort.fields=
    query.additional.highlighted.fields=
    query.additional.analyzed.fields=
    query.additional.not.analyzed.fields=

각 설정의 의미는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 설정
     - 설명
   * - ``query.additional.default.fields``
     - 필드 지정이 없는 쿼리에서 검색 대상으로 하는 기본 필드에 추가합니다.
   * - ``query.additional.search.fields``
     - 필드를 지정하여 검색할 수 있는 필드에 추가합니다.
   * - ``query.additional.facet.fields``
     - 패싯으로 이용할 수 있는 필드에 추가합니다.
   * - ``query.additional.sort.fields``
     - 정렬 대상으로 이용할 수 있는 필드에 추가합니다.
   * - ``query.additional.highlighted.fields``
     - 하이라이트 대상으로 하는 필드에 추가합니다.
   * - ``query.additional.analyzed.fields``
     - Analyzer 에 의한 분석 대상으로 취급하는 필드에 추가합니다.
   * - ``query.additional.not.analyzed.fields``
     - Analyzer 에 의한 분석을 수행하지 않는 필드에 추가합니다.

유사 문서 접기(collapse)
================================

유사(니어 중복) 문서를 ``content_minhash_bits`` 필드로 접어서 표시하는 collapse 기능의 설정입니다.
``query.collapse.inner.hits.name`` 은 검색 결과 중 유사 문서를 저장하는 필드명,
``query.collapse.inner.hits.size`` 는 1그룹당 취득하는 유사 문서 수( ``0`` 은 취득하지 않음),
``query.collapse.inner.hits.sorts`` 는 유사 문서 취득 시 정렬 조건,
``query.collapse.max.concurrent.group.results`` 는 그룹 취득 시 최대 동시 요청 수를 나타냅니다.
::

    query.collapse.max.concurrent.group.results=4
    query.collapse.inner.hits.name=similar_docs
    query.collapse.inner.hits.size=0
    query.collapse.inner.hits.sorts=

검색 프리퍼런스
==============

JSON 형식의 API 검색 시 OpenSearch 에 전달하는 프리퍼런스(검색할 샤드를 결정하는 값)를 지정합니다.
``_query`` 를 지정하면 검색 쿼리의 해시값이 프리퍼런스로 사용되어 동일한 쿼리가 같은 샤드로 배분됩니다.
기본값은 ``_query`` 입니다.
::

    query.json.default.preference=_query

관련도(부스트) 설정
==================

검색 시 관련도(스코어) 계산에 사용하는 부스트 값을 지정합니다.
``.lang`` 이 붙는 설정은 언어별 필드(예: ``content_ja``)에 대한 부스트 값입니다.
::

    query.boost.title=0.5
    query.boost.title.lang=1.0
    query.boost.content=0.05
    query.boost.content.lang=0.1
    query.boost.important_content=-1.0
    query.boost.important_content.lang=-1.0

퍼지 검색의 부스트 값과 동작은 다음에서 지정합니다.
``query.boost.fuzzy.min.length`` 는 퍼지 검색을 적용하는 최소 문자 수( ``-1`` 로 비활성화)입니다.
::

    query.boost.fuzzy.min.length=4
    query.boost.fuzzy.title=0.01
    query.boost.fuzzy.title.fuzziness=AUTO
    query.boost.fuzzy.title.expansions=10
    query.boost.fuzzy.title.prefix_length=0
    query.boost.fuzzy.title.transpositions=true
    query.boost.fuzzy.content=0.005
    query.boost.fuzzy.content.fuzziness=AUTO
    query.boost.fuzzy.content.expansions=10
    query.boost.fuzzy.content.prefix_length=0
    query.boost.fuzzy.content.transpositions=true

쿼리 타입 설정
==============

검색 시 사용하는 쿼리의 종류와 그 세부 동작을 지정합니다.
``query.default.query_type`` 은 기본으로 사용하는 쿼리 타입,
``query.dismax.tie_breaker`` 는 dismax 쿼리의 tie breaker 값,
``query.bool.minimum_should_match`` 는 bool 쿼리의 minimum_should_match 값(비어 있는 경우 미지정)입니다.
::

    query.default.query_type=bool
    query.dismax.tie_breaker=0.1
    query.bool.minimum_should_match=

프리픽스 검색 및 퍼지 검색 상세 설정
==============================

프리픽스 쿼리 및 퍼지 쿼리의 세부 동작을 지정합니다.
::

    query.prefix.expansions=50
    query.prefix.slop=0
    query.fuzzy.prefix_length=0
    query.fuzzy.expansions=50
    query.fuzzy.transpositions=true

패싯 설정
============

패싯 검색의 기본 동작을 지정합니다.
``query.facet.fields`` 는 패싯 대상 필드,
``query.facet.fields.size`` 는 취득하는 패싯 수의 상한,
``query.facet.fields.min_doc_count`` 는 패싯에 표시하는 최소 문서 수,
``query.facet.fields.sort`` 는 패싯의 정렬 순서,
``query.facet.fields.missing`` 은 값이 존재하지 않는 문서에 할당하는 값입니다.
::

    query.facet.fields=label
    query.facet.fields.size=100
    query.facet.fields.min_doc_count=1
    query.facet.fields.sort=count.desc
    query.facet.fields.missing=

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

GSA 호환 XML 형식을 사용할 때 메타데이터 접두사를 지정.
    ::

        query.gsa.meta.prefix=MT_

GSA 호환 XML 형식을 사용할 때 charset 필드를 지정.
    ::

        query.gsa.index.field.charset=charset

GSA 호환 XML 형식을 사용할 때 content_type 필드를 지정.
    ::

        query.gsa.index.field.content_type.=content_type

GSA 호환 XML 형식을 사용할 때 기본 preference를 지정.
    ::

        query.gsa.default.preference=_query
