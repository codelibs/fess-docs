==================================
Wikipedia 커넥터
==================================

개요
====

Wikipedia 커넥터는 Wikipedia 덤프 파일을 읽어서 그 페이지를
|Fess| 인덱스에 등록하는 기능을 제공합니다.
Wikipedia, 다른 Wikimedia 프로젝트, 모든 MediaWiki 사이트의 덤프를 사용할 수 있습니다.

이 기능을 사용하려면 ``fess-ds-wikipedia`` 플러그인이 필요합니다.

지원하는 덤프
=============

덤프 형식은 ``source`` 파라미터로 선택합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ``source``
     - 설명
   * - ``cirrus``
     - CirrusSearch 인덱스 덤프. Wikimedia가 각 위키에 대해
       ``https://dumps.wikimedia.org/other/cirrus_search_index/`` 에서 공개합니다. MediaWiki가 직접 템플릿을 전개하여 렌더링한 텍스트를 포함하므로
       위키텍스트 마크업이 인덱스에 섞이지 않습니다. Wikipedia와 다른 Wikimedia 위키에는 이 형식을 권장합니다
   * - ``xml``
     - MediaWiki XML 내보내기(``*-pages-articles.xml.bz2``, 또는 임의의 MediaWiki의 ``Special:Export`` 나 ``dumpBackup.php`` 출력).
       위키텍스트를 포함하며 커넥터가 일반 텍스트로 변환합니다("XML 덤프의 일반 텍스트 변환" 참조)
   * - ``auto``
     - 기본값. ``cirrus_search_index`` 를 포함하거나 ``.json.bz2`` 또는 ``.json`` 으로 끝나는 위치는 ``cirrus`` 로, 그 외의 위치는 ``xml`` 로 읽습니다

덤프의 압축 형식(bzip2, gzip 등)은 내용에서 자동으로 판별되며, 압축되지 않은 파일도 읽을 수 있습니다.

전제조건
========

1. 플러그인 설치가 필요합니다
2. HTTP(S) URL 또는 |Fess| 서버상의 경로로 덤프 파일에 접근할 수 있어야 합니다
3. 크롤링 시간이 필요합니다. 큰 Wikipedia의 덤프는 수 기가바이트입니다. 먼저 ``limit`` 를 지정하여 설정을 시험해 보세요

플러그인 설치
-------------

관리 화면의 "시스템" → "플러그인"에서 설치하거나, ``bin/fess-setup install plugin fess-ds-wikipedia`` 를 실행한 후
|Fess| 를 재시작합니다.
자세한 내용은 :doc:`../../admin/plugin-guide` 를 참조하세요.

설정 방법
=========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - Japanese Wikipedia
   * - 핸들러 이름
     - WikipediaDataStore
   * - 활성화
     - 켬

파라미터 설정
-------------

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    limit=10000

파라미터 목록
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``url``
     - 아니오
     - 덤프의 위치. HTTP(S) URL, ``file:`` URL 또는 로컬 경로. 기본값은 영어판 Wikipedia 덤프
       (``http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2``)이므로 반드시 명시적으로 지정하세요.
       ``source=cirrus`` 에서 지정할 수 있는 형식은 "CirrusSearch 덤프"를 참조하세요
   * - ``source``
     - 아니오
     - ``auto``, ``cirrus``, ``xml`` 중 하나(기본값: ``auto``)
   * - ``limit``
     - 아니오
     - 이 페이지 수에서 처리를 종료합니다. ``0`` 은 무제한입니다(기본값: ``0``). 소수의 페이지로 설정을 시험할 때 사용합니다
   * - ``user_agent``
     - 아니오
     - 덤프를 다운로드할 때 전송하는 User-Agent 헤더. 지정하지 않으면 |Fess| 크롤러의 User-Agent 이름을 사용합니다
   * - ``max_digest_length``
     - 아니오
     - ``digest`` 의 최대 문자 수(기본값: ``100``)
   * - ``total_entity_size_limit``
     - 아니오
     - XML 파서가 처리하는 엔터티의 총 크기 상한(바이트, 기본값: ``100000000``). ``source=xml`` 에만 적용됩니다
   * - ``text_extractor``
     - 아니오
     - XML 덤프의 위키텍스트를 일반 텍스트로 변환하는 방법. ``sweble`` (기본값) 또는 ``regex``. "XML 덤프의 일반 텍스트 변환"을 참조하세요
   * - ``drop_templates``
     - 아니오
     - XML 덤프의 ``content`` 에서 텍스트를 제외할 템플릿 이름의 쉼표 구분 목록. ``*`` 은 모든 템플릿을 제외합니다
   * - ``keep_templates``
     - 아니오
     - ``drop_templates`` 에 일치하더라도 텍스트를 남길 템플릿 이름의 쉼표 구분 목록
   * - ``drop_captions``
     - 아니오
     - XML 덤프의 ``content`` 에서 이미지와 갤러리의 캡션을 제외합니다(기본값: ``false``)

CirrusSearch 덤프
~~~~~~~~~~~~~~~~~

CirrusSearch 덤프는 ``jawiki_content-20261004-00000.json.bz2`` 와 같은 번호가 붙은 청크로 공개됩니다.
``source=cirrus`` 에서는 ``url`` 에 쉼표로 구분한 목록을 지정할 수 있으며, 각 요소에는 다음을 지정할 수 있습니다:

- 단일 파일(HTTP(S) URL 또는 로컬 경로)
- 로컬 디렉터리: 이름이 ``.json.bz2`` 또는 ``.json`` 으로 끝나는 디렉터리 내의 모든 파일을 이름 순으로 읽습니다
- ``/`` 로 끝나는 HTTP(S) URL: 디렉터리 목록을 가져와서 이름이 ``.json.bz2`` 또는 ``.json`` 으로 끝나는 모든 파일을 이름 순으로 읽습니다

예를 들어 일본어판 Wikipedia의 콘텐츠 인덱스의 모든 청크를 읽으려면 다음과 같이 합니다:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

.. note::

   Wikimedia 서버에서는 오래된 날짜의 덤프가 삭제됩니다. 크롤링을 설정하기 전에
   ``https://dumps.wikimedia.org/other/cirrus_search_index/`` 의 목록에서 존재하는 날짜를 확인하세요.

스크립트 설정
-------------

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    anchor=
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

사용 가능한 필드
~~~~~~~~~~~~~~~~

스크립트에서는 다음 값을 참조할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 페이지 ID
   * - ``title``
     - 페이지 제목
   * - ``encodedTitle``
     - MediaWiki 페이지 URL에서 사용하는 형식의 제목(공백은 ``_`` 가 되고 그 외의 문자는 퍼센트 인코딩됩니다)
   * - ``content``
     - 페이지의 일반 텍스트
   * - ``digest``
     - ``max_digest_length`` 문자로 줄인 ``content``
   * - ``contentLength``
     - ``content`` 의 길이
   * - ``wikitext``
     - 페이지의 위키텍스트(덤프에 포함된 경우)
   * - ``format``, ``model``
     - 페이지의 형식과 콘텐츠 모델
   * - ``timestamp``
     - 페이지의 타임스탬프
   * - ``ns``
     - 이름공간 번호
   * - ``categories``, ``links``
     - 페이지의 분류와 링크 대상 페이지
   * - ``redirect``, ``redirectTitle``
     - 페이지가 넘겨주기인지 여부와 그 대상
   * - ``stub``, ``disambiguation``
     - 페이지가 토막글인지 여부와 동음이의 문서인지 여부
   * - ``lang``, ``host``, ``site``, ``url``
     - 덤프의 위치에서 도출됩니다. "덤프의 위치에서 도출되는 값"을 참조하세요

``source=cirrus`` 에서는 다음 값도 사용할 수 있습니다:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``openingText``
     - 페이지의 도입부 텍스트
   * - ``headings``
     - 제목(헤딩)
   * - ``externalLinks``
     - 외부 링크
   * - ``templates``
     - 페이지가 사용하는 템플릿
   * - ``redirects``
     - 이 페이지로 넘겨주는 제목
   * - ``auxiliaryText``
     - 이미지 캡션 등의 보조 텍스트
   * - ``weightedTags``
     - 가중치가 있는 태그
   * - ``wikibaseItem``
     - Wikidata 항목 ID
   * - ``incomingLinks``
     - 들어오는 링크 수
   * - ``popularityScore``
     - 인기도 점수
   * - ``revisionId``
     - 리비전 ID

덤프의 위치에서 도출되는 값
---------------------------

``lang``, ``host``, ``site``, ``url`` 은 덤프의 이름에서 도출됩니다. ``jawiki-latest-pages-articles.xml.bz2`` 나
``index_name=jawiki_content`` 같은 이름에서는 ``lang`` 이 ``ja``, ``host`` 와 ``site`` 가 ``ja.wikipedia.org``,
``url`` 이 ``https://ja.wikipedia.org/wiki/<인코딩된 제목>`` 이 됩니다.
이름에는 언어 코드 바로 뒤에 ``wiki``, 그 바로 뒤에 ``-``, ``_``, ``.`` 중 하나가 이어지는 부분이 있어야 합니다.
Wikiquote(``jawikiquote-...``) 같은 자매 프로젝트는 잘못된 호스트가 깨진 링크를 만들기 때문에 의도적으로 도출하지 않습니다.

.. warning::

   덤프 이름이 일치하지 않으면 ``host``, ``site``, ``url`` 은 설정되지 않고, ``url`` 에는 ``url`` 파라미터의 값, 즉 덤프의 위치가 남습니다.
   스크립트에서 ``url`` 을 그대로 사용하면 모든 페이지가 같은 URL이 되어 크롤링 전체가 인덱스에서 한 건의 문서가 됩니다. 오류도 출력되지 않습니다.
   이름을 바꾼 덤프나 다른 Wikimedia 프로젝트에서는 위 예제처럼 스크립트에서 URL을 조립하세요. 예:
   ``url="https://ja.wikiquote.org/wiki/" + encodedTitle``

XML 덤프의 일반 텍스트 변환
---------------------------

``source=xml`` 에서는 위키텍스트를 Sweble 위키텍스트 파서로 일반 텍스트로 변환합니다. 이름공간 이름은 내보내기의 ``<siteinfo>`` 에서 읽으므로,
이미지와 분류 구문은 어떤 언어(``[[ファイル:...]]``, ``[[Kategorie:...]]``)에서도, 고유한 이름공간 이름을 가진 위키에서도 인식됩니다.
Sweble이 변환하지 못하는 페이지는 정규식으로 변환됩니다.

``text_extractor=regex`` 는 모든 페이지를 정규식으로 변환합니다. 몇 배 빠르지만 중첩된 템플릿, 표, 여러 줄에 걸친 마크업이 텍스트에 남습니다.

기본적으로 모든 템플릿 인수의 텍스트(파라미터 이름은 제외)와 모든 이미지 및 갤러리의 캡션이 ``content`` 에 남으므로 그 텍스트도 검색할 수 있습니다.
``drop_templates``, ``keep_templates``, ``drop_captions`` 로 걸러낼 수 있습니다:

::

    # 이 템플릿들의 텍스트를 제외합니다(중첩된 경우도 포함. "*" 는 모든 템플릿을 제외)
    drop_templates=Cite web,Cite news,Use dmy dates
    # drop_templates 에 일치하더라도 이 템플릿들은 남깁니다
    # (drop_templates=* 와 keep_templates=Note,Warning 을 함께 지정하면 그 두 개만 남습니다)
    keep_templates=
    # 이미지와 갤러리의 캡션을 제외합니다
    drop_captions=false

템플릿 이름은 MediaWiki가 해석하는 방식과 같게 비교됩니다. 첫 글자는 대소문자를 구분하지 않고, ``_`` 는 공백과 같으며, ``Template:`` 접두사는 생략할 수 있습니다.
템플릿은 전개되지 않으므로 남긴 템플릿이 추가하는 것은 인수의 텍스트이며 MediaWiki가 렌더링하는 내용이 아닙니다.
CirrusSearch 덤프에는 MediaWiki가 렌더링한 텍스트가 이미 포함되어 있으므로 이 파라미터들은 ``source=cirrus`` 에는 적용되지 않습니다.

사용 예
=======

CirrusSearch 덤프로 일본어판 Wikipedia를 크롤링
-----------------------------------------------

파라미터:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

스크립트:

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

XML 덤프로 일본어판 Wikipedia를 크롤링(출처 템플릿 제외)
--------------------------------------------------------

파라미터:

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    source=xml
    drop_templates=Cite web,Cite news
    limit=10000

스크립트는 "스크립트 설정"과 같습니다.

다른 Wikimedia 프로젝트(Wikiquote) 크롤링
-----------------------------------------

덤프 이름 ``jawikiquote-...`` 에서는 ``host`` 와 ``url`` 이 도출되지 않으므로 스크립트에서 조립합니다.

스크립트:

::

    lang="ja"
    url="https://ja.wikiquote.org/wiki/" + encodedTitle
    host="ja.wikiquote.org"
    site="ja.wikiquote.org"
    title=title
    content=content
    digest=digest
    last_modified=timestamp
    timestamp=timestamp

문제 해결
=========

색인되는 문서가 한 건뿐임
-------------------------

"덤프의 위치에서 도출되는 값"을 참조하세요. 스크립트가 모든 페이지에 대해 ``url`` 을 설정하고 있는지 확인합니다.

크롤링에 시간이 너무 오래 걸림
------------------------------

1. 먼저 ``limit`` 를 지정하여 설정을 확인합니다
2. ``source=cirrus`` 를 사용합니다. XML 덤프에서는 ``text_extractor=regex`` 를 사용합니다
3. 덤프를 |Fess| 서버에 배치하고 로컬 경로를 지정합니다

콘텐츠에 위키텍스트 마크업이 남음
---------------------------------

CirrusSearch 덤프(``source=cirrus``)를 사용하세요. ``source=xml`` 에서 ``text_extractor=regex`` 는 중첩된 템플릿, 표, 여러 줄 마크업을 텍스트에 남기므로 ``sweble`` (기본값)을 사용하세요.

덤프를 읽을 수 없음
-------------------

1. URL 또는 경로가 올바른지 확인합니다(CirrusSearch 덤프의 날짜가 서버에서 삭제되었을 수 있습니다)
2. 디렉터리 URL은 ``/`` 로 끝나는지, 그 안의 파일이 ``.json.bz2`` 또는 ``.json`` 으로 끝나는지 확인합니다
3. 로그에서 정확한 오류를 확인합니다

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../../admin/plugin-guide` - 플러그인 관리 가이드
- `Wikimedia Downloads <https://dumps.wikimedia.org/>`_
- `CirrusSearch index dumps <https://dumps.wikimedia.org/other/cirrus_search_index/>`_
