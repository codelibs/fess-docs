=======================================
일본어·영어·중국어가 섞인 문서 검색하기
=======================================

들어가며
========

일본어 회의록, 영어 기술 사양서, 중국어 시장 보고서가 같은 파일 서버나 사내 사이트에 함께 있으면 "영어 문서는 찾아지는데 일본어 활용형으로는 걸리지 않는다", "중국어 문서만 찾고 싶다", "영어로 쓰인 자료를 일본어 단어로 찾고 싶다"와 같은 목소리가 나옵니다.

Fess는 특별한 설정 없이도 어떤 언어의 문서든 검색할 수 있습니다.
다만 어떤 언어의 분석이 어디에서 작동하는지 모른 채 사전에 항목을 추가해도 결과는 달라지지 않습니다.
이 글에서는 Fess 15.9가 다국어 문서를 어떻게 인덱싱하고 검색하는지를 설정 파일의 실제 값을 바탕으로 설명합니다.
그런 다음 다음과 같은 작업을 할 수 있게 합니다.

- 문서마다 판정된 언어를 확인하고, ``lang:``\ 으로 언어를 좁혀 검색한다
- 검색할 때 어떤 언어의 분석을 사용할지 ``query.default.languages`` 등으로 정한다
- 사전(동의어, Kuromoji, 불용어 등)을 작동하는 필드에 맞춰 편집하고 반영한다
- 변경이 효과를 냈는지 검색 결과와 ``_analyze`` API로 확인한다

검색 로그를 활용한 개선 방법 자체는 :doc:`guide-08`\ 에서 다룹니다.

인덱스의 구조: 공통 필드와 언어별 필드
======================================

Fess의 인덱스에는 본문과 제목이 두 가지 형태로 들어갑니다.
정의는 Fess에 포함된 ``fess_indices/fess.json``\ (애널라이저)과 ``fess_indices/fess/doc.json``\ (매핑)에 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 28 32 40

   * - 필드
     - 애널라이저
     - 분석 내용
   * - ``content``, ``title``, ``important_content``
     - ``standard_analyzer``\ (검색 시에는 ``standard_search_analyzer``)
     - 모든 문서에 공통입니다. 한자, 히라가나, 가타카나, 한글은 2글자씩(bi-gram) 나누고, 영어 불용어 제거와 어간 추출(stemming)을 적용합니다. 동의어는 검색 시에만 전개됩니다
   * - ``content_ja``, ``title_ja`` 등
     - ``japanese_analyzer``
     - Kuromoji에 의한 형태소 분석입니다. 동사 등을 기본형으로 맞추고, 조사, 조동사, 기호를 제거합니다
   * - ``content_en``, ``title_en`` 등
     - ``english_analyzer``
     - 영어 불용어 제거와 어간 추출입니다
   * - ``content_zh-cn``, ``title_zh-cn`` 등
     - ``simplified_chinese_analyzer``
     - 중국어용 토크나이저로 단어 단위로 나눕니다
   * - ``content_zh-tw``, ``title_zh-tw`` 등
     - ``traditional_chinese_analyzer``
     - 번체자를 간체자로 변환한 다음, 간체자와 같은 토크나이저로 나눕니다

공통 필드는 모든 문서에 있습니다.
언어별 필드는 문서의 언어가 정해졌을 때만 만들어집니다.
인덱스 처리에서 ``lang`` 필드에 언어 코드를 넣고, ``content``, ``important_content``, ``title``\ (``indexer.language.fields``)의 값을 ``content_ja``\ 와 같은 ``<필드>_<언어>``\ 에 복사합니다.
하나의 문서에 붙는 언어는 하나뿐입니다.

문서의 언어가 정해지는 방식
---------------------------

``lang``\ 은 다음 순서로 정해집니다.

1. 웹 크롤링의 HTML은 ``<html lang="...">``\ 의 값을 사용합니다(``crawler.document.html.lang.xpath=//HTML/@lang``). 크롤링 설정의 "설정 파라미터"에 ``field.xpath.default.lang=<XPath>``\ 를 쓰면 해당 설정에서만 값을 읽는 위치를 바꿀 수 있습니다
2. 1에서 정해지지 않은 문서는 본문에서 자동으로 판정합니다. ``content``, ``important_content``, ``title`` 순으로 앞부분 1000글자(``indexer.language.detect.length``)를 봅니다. 파일 크롤링에서는 추출한 본문만으로 판정합니다
3. 판정 결과가 ``supported.languages``\ 에 없는 언어이거나 판정할 수 없을 때는 ``lang``\ 이 붙지 않고, 언어별 필드도 만들어지지 않습니다

``ja-JP``\ 나 ``zh_CN`` 같은 값은 소문자와 하이픈 형태(``ja``, ``zh-cn``)로 맞춰 저장됩니다.

데이터 스토어의 문서도 인덱싱할 때 같은 자동 판정을 거칩니다.
스크립트에서 ``lang``\ 에 ``supported.languages``\ 에 있는 언어(``ja`` 등)를 넣으면 자동 판정보다 우선합니다.

검색의 구조: 어떤 언어의 필드를 검색하는가
==========================================

검색어는 항상 공통 필드를 대상으로 검색됩니다.
여기에 더해, 검색할 때마다 정해지는 "검색 언어"마다 언어별 필드가 검색 조건에 추가됩니다.
각 필드의 조건은 OR(``bool`` 쿼리의 ``should``)로 연결되므로, 어느 한 필드에만 일치해도 검색 결과에 포함됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - 필드
     - 설정 키
     - 기본값
   * - ``title``
     - ``query.boost.title``
     - ``0.5``
   * - ``content``
     - ``query.boost.content``
     - ``0.05``
   * - ``title_<검색 언어>``
     - ``query.boost.title.lang``
     - ``1.0``
   * - ``content_<검색 언어>``
     - ``query.boost.content.lang``
     - ``0.1``

검색 언어는 다음 중 처음으로 값이 있는 것에서 정해집니다.

1. ``fess_config.properties``\ 의 ``query.default.languages``\ (기본값은 비어 있음). 값이 있으면 다른 지정은 모두 무시됩니다
2. 요청의 ``lang`` 파라미터. 검색 화면의 [옵션] > "우선 언어"나 고급 검색의 "우선 언어"에서 선택한 언어, 또는 ``/api/v2/search``\ 의 ``lang``\ 입니다
3. 브라우저가 보내는 ``Accept-Language`` 헤더의 언어

예를 들어 일본어 브라우저에서 "会議"(회의)로 검색하면 검색 언어는 ``ja``\ 가 되고, ``content``\ 에 더해 ``content_ja``\ 도 검색됩니다.
영어 문서에는 ``content_ja``\ 가 없으므로, 영어 문서는 공통 필드의 bi-gram으로만 일치합니다.
반대로 일본어 문서는 ``title_ja``, ``content_ja``\ 에서도 일치하면 그만큼 점수가 올라가 상위에 오기 쉬워집니다.
Kuromoji는 활용형을 기본형으로 맞추기 때문에 "走った"(달렸다)로 검색하면 "走る"(달리다)라고 쓰인 일본어 문서도 ``content_ja``\ 에서 일치합니다.

따라서 "우선 언어"는 해당 언어의 문서를 상위로 끌어올리는 지정이며, 다른 언어의 문서를 제외하는 필터가 아닙니다.

언어로 좁히기: ``lang:`` 검색
=============================

언어로 좁히려면 ``lang`` 필드를 지정하여 검색합니다.
``lang``\ 은 키워드 타입의 검색 가능한 필드이므로, 언어마다 라벨을 만들 필요가 없습니다.

::

    lang:en meeting
    lang:ja 会議
    lang:zh-cn 会议
    会議 -lang:ja

마지막 예는 일본어로 판정된 문서를 제외하고 "会議"를 검색합니다.
API에서는 ``q``\ 에 같은 식을 쓰거나 ``fields.lang=en``\ 을 붙입니다(``lang:"en"`` 조건이 추가됩니다).

::

    $ curl -s "http://localhost:8080/api/v2/search?q=meeting&fields.lang=en"

``lang``\ 이 붙지 않은 문서(언어를 판정할 수 없었던 문서)는 어떤 ``lang:`` 조건에도 일치하지 않습니다.

언어 판정 결과 확인하기
-----------------------

사전이나 설정을 바꾸기 전에 문서에 어떤 언어가 붙어 있는지 확인합니다.

1. 검색 화면에서 ``lang:ja``, ``lang:en``, ``lang:zh-cn``, ``lang:zh-tw``\ 를 각각 검색하여 건수를 비교합니다. API라면 ``response.record_count``\ 로 건수를 볼 수 있습니다

   ::

       $ curl -s "http://localhost:8080/api/v2/search?q=lang:zh-cn&num=1"

2. 개별 문서는 관리 화면의 [시스템 정보] > [검색]에서 URL 등으로 찾아 열면 ``lang`` 칸에서 값을 확인할 수 있습니다

판정이 기대와 다를 때는 다음 사항을 확인하십시오.

- HTML의 ``<html lang>``\ 은 자동 판정보다 우선합니다. 사이트 템플릿이 일본어 페이지에도 ``lang="en"``\ 을 출력하면 그 페이지는 영어로 취급됩니다
- ``<html lang="zh">``\ 처럼 지역이 없는 중국어는 ``zh``\ 가 됩니다. ``zh``\ 에는 중국어용 애널라이저의 언어별 필드가 없으므로, 중국어 분석은 공통 필드의 bi-gram뿐입니다
- 한자가 많고 가나가 적은 짧은 일본어 문서는 ``zh-cn`` 등으로 판정될 수 있습니다

모든 HTML 또는 모든 파일을 하나의 언어로 취급하는 설정도 있습니다.
``crawler.document.html.default.lang``\ 과 ``crawler.document.file.default.lang``\ 에 값을 넣으면 ``<html lang>``\ 도 자동 판정도 사용하지 않고, Fess 전체의 크롤링에서 그 언어로 고정됩니다.
문서의 언어가 섞여 있는 환경에서는 비워 두십시오.

검색 언어 정하기: ``query.default.languages``
=============================================

기본적으로는 사용자마다 브라우저의 언어에 따라 검색 언어가 바뀝니다.
영어 브라우저를 쓰는 직원이 일본어 문서를 검색하면 ``content_ja``\ 가 사용되지 않는 등, 사용자에 따라 결과의 순서가 달라집니다.
이를 피하고 싶다면 ``query.default.languages``\ 로 검색 언어를 고정합니다.

::

    query.default.languages=ja,en,zh-cn,zh-tw

이 예에서는 누가 어떤 언어로 검색하든 4개의 언어별 필드가 모두 검색 조건에 추가됩니다.
각 문서는 자기 언어의 필드를 하나만 가지므로, 어떤 언어의 문서든 같은 조건에서 언어별 분석의 혜택을 받습니다.
그 대신 "우선 언어"로 특정 언어를 상위로 끌어올리는 조작은 효과가 없어집니다.
일본어 문서가 중심이라면 ``query.default.languages=ja``\ 처럼 한 언어만 지정하는 방법도 있습니다.

설정은 ``fess_config.properties``\ 에 쓰고 Fess를 재시작합니다.
파일 위치는 ZIP 버전에서는 ``app/WEB-INF/classes/fess_config.properties``, RPM/DEB 버전에서는 ``/etc/fess/fess_config.properties``\ 입니다.
Docker에서는 ``compose.yaml``\ 의 ``fess01``\ 의 ``environment``\ 에 JVM 옵션으로 추가하고 컨테이너를 다시 만듭니다.

::

    - "FESS_JAVA_OPTS=-Dfess.config.query.default.languages=ja,en,zh-cn,zh-tw"

``FESS_JAVA_OPTS``\ 는 공백으로 구분되므로 값에 공백을 넣지 마십시오.
컨테이너를 다시 만들면 [시스템] > [일반]에서 바꾼 설정은 컨테이너 안의 ``system.properties``\ 와 함께 사라집니다(:doc:`guide-02`).

언어별 필드의 일치를 얼마나 중요하게 볼지는 ``query.boost.title.lang``\ 과 ``query.boost.content.lang``\ 으로 조정할 수 있습니다.
변경했다면 아래 "확인하기"의 절차로 검색 결과의 순서를 비교하십시오.

언어에 맞춰 사전 구분해 쓰기
============================

사전은 [시스템] > [사전]에서 편집합니다.
사전마다 작동하는 필드가 정해져 있으므로, 목적하는 필드에 작동하는 사전을 고르지 않으면 검색 결과는 달라지지 않습니다.

.. list-table::
   :header-rows: 1
   :widths: 24 36 40

   * - 사전(파일)
     - 작동하는 필드
     - 다국어 환경에서의 활용
   * - 동의어(``synonym.txt``)
     - ``content``, ``title``\ (검색 시에만)
     - 언어를 넘나드는 바꿔 말하기("会議"와 "meeting"), 표기 흔들림. 언어별 필드에는 작동하지 않습니다
   * - Kuromoji(``ja/kuromoji.txt``)
     - ``_ja`` 필드만
     - 사내 용어나 제품명을 일본어 한 단어로 취급하게 한다
   * - 불용어(``ja/stopwords.txt``)
     - ``_ja`` 필드만
     - 일본어 문서에서 검색에 사용하지 않을 단어
   * - 불용어(``en/stopwords.txt``)
     - ``content``, ``title``\ 과 ``_en`` 필드
     - 영어의 불필요한 단어. 공통 필드에 작동하므로 모든 언어의 문서에 영향을 줍니다
   * - Protwords(``en/protwords.txt``)
     - ``content``, ``title``\ 과 ``_en`` 필드
     - 어간 추출을 하고 싶지 않은 영어 단어(제품명 등)
   * - Stemmer 덮어쓰기(``en/stemmer_override.txt``)
     - ``content``, ``title``\ 과 ``_en`` 필드
     - 영어 어간 추출의 결과를 지정한다
   * - 매핑(``mapping.txt``)
     - ``content``, ``title``
     - 문자 치환. ``ja/mapping.txt``\ 는 ``_ja`` 필드용의 별도 파일입니다

일본어용 보호어(Protwords) 사전은 없습니다.
``japanese_analyzer``\ 에는 보호어를 읽는 필터가 없기 때문입니다.
간체자, 번체자 중국어 필드에는 관리 화면에서 편집할 수 있는 사용자 사전이 없습니다(불용어는 ``zh-cn/stopwords.txt``, ``zh-tw/stopwords.txt``).

언어를 넘나드는 동의어
----------------------

일본어 단어로 영어 문서를 찾고 싶다면 대역어를 동의어로 등록합니다.
업로드하는 파일 형식에서는 한 줄에 같은 의미의 단어를 쉼표로 구분하여 나열합니다.

::

    会議,ミーティング,meeting
    見積,quotation

동의어는 검색 시에 공통 필드에서 전개되므로 다시 크롤링할 필요가 없습니다.
히라가나는 가타카나로, 전각 영숫자는 반각으로 등록하는 등 등록 규칙은 `동의어 사전 <https://fess.codelibs.org/ko/stable/admin/synonym-guide.html>`__\ 을 참조하십시오.

Kuromoji 사용자 사전
--------------------

Kuromoji 사전에는 토큰, 분할한 토큰, 읽기(가타카나), 품사를 등록합니다.
Kuromoji가 잘게 나눠 버리는 사내 용어나 제품명을 한 단어로 취급하게 하려면 토큰과 분할한 토큰에 같은 단어를 씁니다.

::

    東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞

이 사전이 작동하는 것은 ``_ja`` 필드뿐입니다.
공통 필드인 ``content``\ 는 bi-gram으로 나누므로, Kuromoji 사전을 바꿔도 ``content``\ 에서의 일치는 달라지지 않습니다.
효과가 나타나는 것은 검색 언어에 ``ja``\ 가 포함된 검색에서, 일본어로 판정된 문서에 대해서입니다.

사전 변경 반영하기
------------------

사전을 저장하기만 해서는 검색 결과가 달라지지 않습니다.

1. [시스템 정보] > [유지보수]를 열고 "문서 인덱스 다시 로드"의 [다시 로드]를 클릭합니다. 인덱스를 닫았다가 다시 열기 때문에 그동안 검색은 오류가 나거나 0건이 됩니다. 이용이 적은 시간대에 실행하십시오
2. 동의어는 검색 시에만 사용되므로 다시 로드하면 반영이 끝납니다
3. 동의어 이외의 사전(Kuromoji, 매핑, 불용어, Protwords, Stemmer 덮어쓰기)은 인덱스를 만들 때의 분석도 바꿉니다. 이미 인덱스에 있는 문서는 이전 사전으로 분석된 상태이므로 대상을 다시 크롤링합니다

다시 크롤링할 때 [시스템] > [일반]의 "최종 갱신 일시 확인"이 활성화되어 있으면(기본값) 갱신되지 않은 파일이나 페이지는 다시 가져오지 않습니다.
일시적으로 비활성화하고 크롤링을 실행한 다음, 끝나면 다시 활성화합니다.

확인하기
========

토큰 구분을 ``_analyze`` API로 보기
-----------------------------------

사전이 반영되었는지 확인하려면 OpenSearch의 ``_analyze`` API로 같은 문자열을 공통 필드와 일본어 필드의 애널라이저에 넣어 비교하는 것이 확실합니다.
:doc:`guide-02`\ 의 Docker 구성에서는 호스트의 9200번 포트로 OpenSearch에 접속할 수 있습니다.

::

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"japanese_analyzer","text":"全文検索エンジンを導入した"}'

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"standard_analyzer","text":"全文検索エンジンを導入した"}'

``japanese_analyzer``\ 에서는 단어 단위로 나뉘고 "を"와 "た"가 제거됩니다.
``standard_analyzer``\ 에서는 "全文", "文検", "検索"처럼 2글자씩 나뉩니다.
Kuromoji 사전에 "東京スカイツリー"를 등록하고 다시 로드한 뒤에는 ``japanese_analyzer``\ 로 이 단어를 분석하면 하나의 토큰으로 반환됩니다.
등록한 동의어는 ``"analyzer":"standard_search_analyzer"``\ 로 "会議"를 분석하여 "meeting"에서 만들어진 토큰(어간 추출되어 ``meet``)이 나오는 것으로 확인할 수 있습니다.

검색 결과로 확인하기
--------------------

1. 검색 화면에서 일본어와 영어 문서 양쪽에 나오는 단어를 검색합니다
2. [옵션]의 "우선 언어"를 "일본어"와 "영어"로 바꿔 가며 상위 문서의 언어가 바뀌는지 확인합니다. ``query.default.languages``\ 를 설정한 경우에는 바꿔도 순서가 달라지지 않는지 확인합니다
3. 대역어 동의어를 등록하고 다시 로드했다면 ``lang:en 会議``\ 로 영어 문서가 찾아지는지 확인합니다
4. Kuromoji 사전을 바꾸고 다시 크롤링했다면 등록한 단어로 검색하여 그 단어를 포함한 일본어 문서가 찾아지는지 확인합니다. 구분이 바뀐 것 자체는 앞의 ``_analyze``\ 로 확인합니다

결과가 달라지지 않을 때는 사전 표의 "작동하는 필드"와 문서의 ``lang``\ 을 대조해 보십시오.
예를 들어 ``en/stopwords.txt``\ 에 3글자 이상의 일본어 단어를 추가해도, 공통 필드에서는 2글자씩의 토큰이 되므로 일치하지 않아 효과가 없습니다.

정리
====

- 모든 문서는 bi-gram과 영어 어간 추출을 적용하는 공통 필드(``content``, ``title``)로 검색할 수 있습니다
- 판정된 언어의 ``lang``\ 과 언어별 필드(``content_ja`` 등)가 언어에 맞는 분석을 더합니다
- 검색 언어는 ``query.default.languages``, 요청의 ``lang``, 브라우저의 언어 순으로 정해지며, 필터가 아니라 상위로 끌어올리는 방향으로 작동합니다
- 언어로 좁힐 때는 ``lang:en``\ 처럼 ``lang`` 필드를 지정합니다
- 사전은 작동하는 필드를 골라 편집하고, 문서 인덱스 다시 로드와 필요하면 다시 크롤링으로 반영합니다

다음에 읽을 글
==============

- 검색 로그에서 개선점을 찾아 동의어나 키 매치로 고치고 싶다: :doc:`guide-08`
- 사내 웹 사이트와 파일 서버를 한꺼번에 크롤링하고 싶다: :doc:`guide-04`
- 키워드가 일치하지 않아도 의미가 가까운 문서를 찾고 싶다: :doc:`guide-18`
- 검색 API를 업무 시스템에서 호출하고 싶다: :doc:`guide-11`

참고 자료
=========

- `사전 <https://fess.codelibs.org/ko/stable/admin/dict-guide.html>`__
- `Kuromoji 사전 <https://fess.codelibs.org/ko/stable/admin/kuromoji-guide.html>`__
- `동의어 사전 <https://fess.codelibs.org/ko/stable/admin/synonym-guide.html>`__
- `불용어 사전 <https://fess.codelibs.org/ko/stable/admin/stopwords-guide.html>`__
- `유지보수 <https://fess.codelibs.org/ko/stable/admin/maintenance-guide.html>`__
- `검색 관련 설정(검색 대상 기본 언어) <https://fess.codelibs.org/ko/stable/config/search-advanced.html>`__
- `크롤러 고급 설정 <https://fess.codelibs.org/ko/stable/config/crawler-advanced.html>`__
- `필드 지정 검색 <https://fess.codelibs.org/ko/stable/user/search-field.html>`__
- `검색 API <https://fess.codelibs.org/ko/stable/api/api-search.html>`__
