=========================================
이미지와 텍스트를 함께 검색하기(멀티모달)
=========================================

들어가며
========

파일 서버나 사내 사이트에는 제품 사진이나 현장 사진처럼 파일 이름 외에는 단서가 없는 이미지가 많이 있습니다.
키워드 검색으로는 파일 이름이나 메타데이터에 포함된 단어로만 이미지를 찾을 수 있습니다.

멀티모달 검색 플러그인 ``fess-webapp-multimodal``\ 을 사용하면 "산의 석양"이나 "강아지" 같은 말로, 찍혀 있는 내용이 가까운 이미지를 검색할 수 있습니다.
이 글에서는 Fess 15.9로 다음을 진행합니다.

- 검증용 Docker 환경 ``docker-multimodalsearch``\ 를 15.9 버전으로 기동하고, 이미지를 크롤링하여 검색한다
- 이미지가 벡터로 검색되었는지를 검색 API 응답으로 확인한다
- 기존 Fess에 도입할 때 필요한 설정과 막히기 쉬운 부분을 짚어 둔다

할 수 있는 것과 할 수 없는 것
=============================

먼저 15.9의 ``fess-webapp-multimodal``\ 이 다루는 범위를 정리해 둡니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 항목
     - 15.9에서의 동작
   * - 검색 방향
     - 텍스트로 이미지를 찾는 방향만 지원합니다. 이미지를 업로드해 비슷한 이미지를 찾는 기능은 없습니다
   * - 벡터화되는 이미지
     - MIME 타입이 ``image/gif``, ``image/jpeg``, ``image/png``\ 인 파일만입니다. BMP나 TIFF는 벡터화되지 않습니다
   * - PDF나 Office 문서 안의 이미지
     - 벡터화되지 않습니다. 이미지 안의 문자를 검색하려면 OCR(별도 기능)을 사용합니다
   * - 이미지가 아닌 문서
     - 평소처럼 키워드 검색(BM25)으로 검색됩니다. 검색 결과에는 이미지와 텍스트 문서가 섞여서 표시됩니다
   * - 영어 이외의 검색어(한국어 등)
     - 다국어를 지원하는 CLIP 모델을 사용합니다. ``docker-multimodalsearch``\ 의 기본 모델은 다국어 모델로, README에서는 영어에 한정되지 않는다고 설명합니다(README에서는 일본어를 예로 듭니다)
   * - 텍스트 시맨틱 검색
     - 같은 Fess에서 함께 사용할 수 없습니다(후술)

OCR은 `OCR(이미지 내 문자 인식) 설정 <https://fess.codelibs.org/ko/stable/config/crawler-ocr.html>`__\ 을 참조하십시오.

동작 원리
=========

CLIP은 텍스트와 이미지를 같은 벡터 공간으로 변환하는 모델입니다.
"강아지"라는 텍스트의 벡터는 강아지가 찍힌 이미지의 벡터 가까이에 놓이므로, 벡터끼리의 거리로 이미지를 검색할 수 있습니다.

Fess 15.8 이후에는 벡터의 저장과 검색을 Fess 본체가 담당합니다.
플러그인이 추가하는 것은 CLIP 서버와 주고받는 부분뿐입니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 시점
     - 처리
   * - 크롤링 시
     - GIF/JPEG/PNG 이미지를 CLIP 서버로 보내 벡터로 변환하고, 본체의 벡터 필드 ``content_chunk_vector``\ 에 기록합니다
   * - 검색 시
     - 검색어를 CLIP 서버에서 벡터로 변환하고 가까운 이미지를 찾습니다. 이 검색은 키워드 검색과 병행하여 실행되며, Rank Fusion으로 하나의 결과로 통합됩니다
   * - 결과
     - 벡터 검색으로 찾은 문서에는 ``searcher`` 필드에 ``multi_modal``\ 이 붙습니다. 키워드 검색으로 찾은 문서는 ``default``\ 입니다

Rank Fusion의 원리는 `하이브리드 검색과 Rank Fusion(시맨틱 + 키워드) <https://fess.codelibs.org/ko/stable/config/rank-fusion.html>`__\ 을 참조하십시오.

docker-multimodalsearch로 시험하기
==================================

``docker-multimodalsearch``\ 는 멀티모달 검색을 바로 시험해 볼 수 있도록 필요한 컨테이너와 설정을 묶어 둔 Docker Compose 환경입니다.
``v15.9.0`` 태그에서는 다음 서비스가 기동합니다.

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - 서비스
     - 역할
   * - ``fess01``
     - Fess 본체. 이미지는 ``ghcr.io/codelibs/fess:15.9.0-noble``\ 이며, 기동 시 플러그인 ``fess-webapp-multimodal:15.9.0``\ 을 설치합니다. 검색 화면에는 이미지 갤러리형 테마 ``mosaic``\ 을 사용합니다
   * - ``search01``
     - OpenSearch 3.9.0. 포트 9200은 호스트의 루프백(127.0.0.1)에만 공개됩니다
   * - ``clip_server``
     - CLIP 서버. 기본 모델은 다국어를 지원하는 ``xlm-roberta-base-ViT-B-32::laion5b-s13b-b90k``\ (512차원)이며, CPU에서 동작합니다
   * - ``content``
     - 샘플 이미지를 ``http://content/``\ 로 제공하는 nginx. 컨테이너 간 네트워크에서만 접근할 수 있습니다
   * - ``init-fess-verify``
     - 기동 시 한 번만 실행되어, 인덱스의 벡터 필드가 설정대로인지 확인하고 종료합니다

준비
----

- Docker(``docker compose`` 명령), Git, bash
- 인터넷 연결(이미지와 CLIP 모델을 받는 데 사용합니다. README에 따르면 모델은 약 1.6GB입니다)
- Linux에서는 OpenSearch를 위해 ``vm.max_map_count``\ 를 올려 둡니다(:doc:`guide-02`\ 의 준비 단계와 같습니다)

15.9 버전 받기
--------------

``docker-multimodalsearch``\ 의 기본 브랜치는 개발 중인 다음 버전을 따라가므로, ``v15.9.0`` 태그를 지정하여 받습니다.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-multimodalsearch.git
    $ cd docker-multimodalsearch
    $ cp .env.example .env

``.env``\ 를 열고 테마를 가져올 곳을 15.9용 브랜치로 변경합니다.

::

    FESS_THEMES_REF=15.9.x

``v15.9.0``\ 의 ``.env.example``\ 은 ``FESS_THEMES_REF=main`` 그대로이지만, ``fess-themes``\ 의 ``main``\ 에 있는 ``mosaic`` 테마는 현재 Fess 15.10 이상용(``minFessVersion: 15.10``)입니다.
15.9용 ``mosaic``\ 은 ``15.9.x`` 브랜치에 있습니다.

``.env``\ 의 ``FESS_VERSION=15.9.0``\ 과 ``FESS_PLUGINS=fess-webapp-multimodal:15.9.0``\ 은 그대로 둡니다.
플러그인 버전은 Fess 버전과 맞춰야 합니다.

설정하고 기동하기
-----------------

::

    $ bash bin/setup.sh
    $ docker compose up -d

``bin/setup.sh``\ 는 데이터용 디렉터리 생성, 테마 가져오기, 썸네일 생성 스크립트 준비를 수행합니다.
처음 ``docker compose up -d``\ 를 실행하면 ``clip_server`` 이미지를 빌드하고 CLIP 모델을 다운로드합니다.
``fess01``\ 은 ``clip_server``\ 의 준비가 끝날 때까지 기동을 기다리므로, 처음에는 몇 분이 걸립니다.

상태는 다음 명령으로 확인합니다.

::

    $ docker compose ps -a
    $ docker compose logs init-fess-verify

``fess01``\ 이 ``(healthy)``\ 가 되고 ``init-fess-verify``\ 가 ``Exited (0)``\ 으로 끝나며, 로그에 다음 줄이 출력되어 있으면 벡터 필드는 설정대로 만들어진 것입니다.

::

    [init-fess-verify] OK: dimension=512, engine=lucene, space_type=cosinesimil, index.knn=true

샘플 이미지 크롤링하기
----------------------

샘플 이미지(동물, 탈것, 음식, 자연, 건물)와 HTML, PDF를 받습니다.

::

    $ bash bin/fetch-sample-images.sh

이어서 관리 화면에서 크롤링합니다.

1. ``http://localhost:8080/admin/``\ 에 ``admin`` / ``admin``\ 으로 로그인하고, 요청이 있으면 새 비밀번호를 설정합니다
2. [크롤러] > [웹]에서 [새로 만들기]를 클릭하고, "이름"에 ``content``, "URL"에 ``http://content/``\ 를 입력한 뒤 [작성]을 클릭합니다
3. [시스템] > [스케줄러]에서 "Default Crawler"를 열고 [지금 시작]을 클릭합니다
4. [시스템 정보] > [크롤링 정보]에서 크롤링이 끝나기를 기다립니다

이미지의 벡터는 이 크롤링 과정에서 기록됩니다.
README에 따르면 동봉된 샘플에서는 43건(이미지 37건, HTML 5건, PDF 1건)이 등록됩니다.
건수는 기준치입니다.

검색하기
--------

``http://localhost:8080/``\ 을 열고 ``강아지``\ 나 ``산의 석양``, ``mountain sunset``\ 으로 검색합니다.
기본 모델은 다국어를 지원하므로 한국어로도 영어로도 이미지가 반환됩니다.

``mosaic`` 테마는 결과를 썸네일 갤러리로 표시하고, 각 결과에 "키워드", "비주얼", "블렌드" 배지를 붙입니다.
"비주얼"은 이미지 유사도로, "블렌드"는 키워드와 이미지 양쪽으로 찾은 결과입니다.

썸네일은 크롤링 후 백그라운드 작업으로 생성됩니다.
크롤링 직후 일부가 표시되지 않으면 잠시 기다린 뒤 새로 고칩니다.

정지할 때는 ``docker compose down``\ 을 실행합니다.
데이터는 ``./data`` 아래에 남습니다.

동작 확인하기
=============

검색 API의 ``searcher`` 보기
----------------------------

벡터 검색이 사용되었는지는 검색 API 응답의 ``searcher``\ 로 확인할 수 있습니다.
``jq``\ 가 있으면 다음과 같이 실행합니다.

::

    $ curl -s -G 'http://localhost:8080/api/v2/search' --data-urlencode 'q=강아지' | jq -c '.response.data[] | {url, searcher}'

``searcher`` 값의 의미는 다음과 같습니다.

- ``["multi_modal"]``: 이미지 유사도로 찾았다
- ``["default"]``: 키워드 검색으로 찾았다
- 둘 다 포함: 양쪽으로 찾았다

모든 결과가 ``["default"]``\ 뿐이라면 벡터 검색은 실행되지 않은 것입니다.
아래의 "벡터 검색이 실행되지 않는 검색"에 해당하지 않는지 확인합니다.

``searcher``\ 는 기본적으로 API 응답에 포함되지 않습니다.
``docker-multimodalsearch``\ 는 ``fess_config.properties``\ 의 ``query.additional.api.response.fields=searcher``\ 를 기동 옵션(``-Dfess.config.query.additional.api.response.fields=searcher``)으로 설정하고 있으므로 응답에 포함됩니다.
검색 API에 대한 자세한 내용은 `검색 API <https://fess.codelibs.org/ko/stable/api/api-search.html>`__\ 를 참조하십시오.

벡터가 기록되었는지 보기
------------------------

검색에서 이미지가 전혀 반환되지 않으면 벡터를 가진 문서 수를 OpenSearch에서 셉니다(이 환경의 9200번 포트는 호스트에서만 사용할 수 있습니다).

::

    $ curl -s 'http://localhost:9200/fess.search/_count' -H 'Content-Type: application/json' -d '{"query":{"nested":{"path":"content_chunk_vector","query":{"exists":{"field":"content_chunk_vector.vector"}}}}}'

``count``\ 가 0이면 크롤링 시 벡터가 만들어지지 않은 것입니다.
``docker compose logs fess01``\ 이나 크롤러 로그에 ``Failed to convert an image to a vector.``\ 라는 경고가 나오지 않았는지 확인합니다.

벡터 검색이 실행되지 않는 검색
------------------------------

다음 경우에는 벡터 검색이 실행되지 않고 키워드 검색만의 결과가 됩니다.
오류가 발생하지 않아 알아차리기 어려우므로 주의하십시오.

- 정렬 순서를 지정한 검색(``sort`` 파라미터). [시스템] > [일반]에서 "기본 정렬 값"을 설정하면 ``mosaic`` 테마가 그 값을 ``sort``\ 로 보내므로, 일반 검색도 여기에 해당합니다
- 검색어에 검색 구문을 사용한 검색: 구문(``"산의 석양"``), 와일드카드(``dog*``), 부스트(``dog^2``), 제외(``-dog``), ``allintitle:``, ``allinurl:``
- 검색어 없이 라벨 등의 필터 조건만 있는 검색
- 101번째 이후의 페이지(시작 위치가 ``rank.fusion.window_size``\ (기본값 200)의 절반 이상인 경우)
- CLIP 서버에 연결할 수 없을 때(``fess.log``\ 에 ``Embedding provider is unavailable`` 등의 WARN이 출력됩니다)

반면 검색어와 함께 ``filetype:jpg`` 같은 필드 지정이나 라벨 필터를 사용해도 벡터 검색은 실행되며, 그 조건으로 좁혀집니다.

기존 Fess에 도입하기
====================

``docker-multimodalsearch``\ 를 사용하지 않고 기존 Fess 15.9에 도입하는 경우 다음 절차로 진행합니다.

1. 플러그인 설치하기
--------------------

``fess-webapp-multimodal``\ 의 15.9.x를 다음 중 한 가지 방법으로 설치하고 Fess를 재시작합니다.

- 관리 화면의 [시스템] > [플러그인] > [설치]
- ``bin/fess-setup install plugin fess-webapp-multimodal:15.9.0``
- Docker의 경우 환경 변수 ``FESS_PLUGINS``\ 에 ``fess-webapp-multimodal:15.9.0``\ 을 추가한다

자세한 내용은 `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__\ 을 참조하십시오.

2. CLIP 서버 준비하기
---------------------

플러그인은 Jina의 CLIP 서버와 같은 형식의 HTTP API에 연결합니다.
벡터화에는 ``POST /post``, 연결 확인에는 ``GET /health``\ 를 사용합니다.
``/health``\ 가 2xx를 반환하지 않으면 벡터 검색이 비활성화된 상태로 동작합니다.
연결 대상은 ``content_chunker.embedding.clip.api.url``\ 로 지정하며, 기본값은 ``http://localhost:51000``\ 입니다.

- 플러그인 저장소에 있는 ``docker/compose.yaml``\ 은 ``jinaai/clip-server``\ 를 기동합니다. 설정 ``docker/clip_config.yaml``\ 은 모델을 지정하지 않으므로 기본 모델(README에서는 ViT-B/32, 512차원)이 사용됩니다. 또한 이 Compose 파일은 GPU를 요구합니다
- 영어 이외의 검색어(한국어 등)를 사용하는 경우 ``docker-multimodalsearch``\ 의 ``docker/clip-server``\ 처럼 다국어 모델을 실행하는 서버를 준비합니다

3. system.properties에 설정하기
-------------------------------

멀티모달 검색 설정은 ``system.properties``\ 에 작성합니다.
위치는 ZIP 버전이 ``app/WEB-INF/conf/system.properties``, RPM/DEB 버전이 ``/etc/fess/system.properties``, Docker 버전이 ``/opt/fess/system.properties``\ 입니다.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=clip
    content_chunker.embedding.dimension=512
    content_chunker.embedding.clip.api.url=http://localhost:51000
    content_chunker.search.enabled=true

- ``content_chunker.embedding.dimension``\ 은 CLIP 모델이 출력하는 차원 수에 맞춥니다(ViT-B/32 계열은 512)
- ``content_chunker.search.enabled``\ 는 기동 시에만 읽히므로 설정 후 Fess를 재시작합니다
- 기동 옵션으로 전달하는 경우 ``-Dfess.system.<키 이름>``\ 을 사용합니다. ``fess_config.properties``\ 나 ``-Dfess.config.<키 이름>``\ 에 작성해도 무시되며, 경고도 출력되지 않습니다
- ``system.properties``\ 의 값은 ``-Dfess.system.*``\ 보다 우선합니다. 양쪽에 작성하면 파일의 값이 사용됩니다
- docker-fess의 Compose 파일에서는 ``fess01``\ 에 볼륨이 없어 ``docker compose down``\ 으로 ``system.properties``\ 가 사라집니다. Docker에서는 환경 변수 ``FESS_JAVA_OPTS``\ 에 ``-Dfess.system.<키 이름>=<값>``\ 을 나열하는 방법이 확실합니다(``docker-multimodalsearch``\ 의 ``compose.yaml``\ 도 이 방법입니다)

키 목록은 `시맨틱 검색(콘텐츠 청킹 + 벡터 검색) <https://fess.codelibs.org/ko/stable/config/search-semantic.html>`__\ 의 "설정 레퍼런스"를 참조하십시오.
멀티모달 검색에서도 같은 ``content_chunker.*``\ 를 사용합니다.

4. 인덱스 다시 만들기
---------------------

벡터 필드 ``content_chunk_vector``\ 의 매핑은 인덱스가 만들어질 때 설정된 차원 수로 만들어집니다.
위 설정을 하기 전에 한 번이라도 Fess를 기동했다면 [시스템 정보] > [유지보수]의 "재인덱싱"을 "에일리어스 갱신"을 활성화한 상태로 실행합니다.
자세한 내용은 `유지보수 <https://fess.codelibs.org/ko/stable/admin/maintenance-guide.html>`__\ 를 참조하십시오.

5. 썸네일 활성화하기
--------------------

이미지 검색에서는 썸네일이 없으면 결과를 구별할 수 없습니다.
썸네일은 기본적으로 비활성화되어 있습니다.

- [시스템] > [일반]에서 "썸네일 표시"를 활성화하고 저장합니다
- 이미지, PDF, Office 문서의 썸네일 생성에는 ImageMagick 등의 외부 도구가 필요합니다. Docker의 기본(Alpine) 이미지에는 포함되어 있지 않으므로 ``-noble`` 이미지(예: ``ghcr.io/codelibs/fess:15.9.0-noble``)를 사용합니다

필요한 도구는 `썸네일 이미지 설정 <https://fess.codelibs.org/ko/stable/config/crawler-thumbnail.html>`__\ 을 참조하십시오.

6. 크롤링하고 확인하기
----------------------

GIF/JPEG/PNG 이미지를 포함한 사이트나 폴더를 크롤링합니다.
이미지의 벡터는 크롤링 시 기록됩니다.

검색 API에서 ``searcher``\ 를 확인하려면 ``fess_config.properties``\ 에 ``query.additional.api.response.fields=searcher``\ 를 설정합니다(기동 옵션이라면 ``-Dfess.config.query.additional.api.response.fields=searcher``).

스케줄러의 "Content Chunk Vector Indexer" 작업은 비활성화된 상태로 둡니다(기본적으로 비활성화되어 있습니다).
이미지의 벡터는 크롤러가 기록하므로 이 작업은 필요 없습니다.
활성화하면 텍스트 문서도 CLIP의 텍스트 쪽으로 벡터화되고, ``content`` 필드가 분할됩니다.

운용상의 주의
=============

텍스트 시맨틱 검색과는 함께 사용할 수 없다
------------------------------------------

플러그인은 본체의 시맨틱 검색 검색 처리(``semanticChunkSearcher``)를 CLIP용으로 바꿉니다.
또한 ``content_chunker.embedding.name``\ 에는 하나의 값만 설정할 수 있습니다.
그래서 :doc:`guide-18`\ 의 텍스트 시맨틱 검색과 멀티모달 검색은 하나의 Fess에서 동시에 사용할 수 없습니다.
둘 다 필요하다면 Fess를 따로 구축합니다.

또한 ``rank.fusion.searchers``\ 로 사용할 검색 처리를 좁혀 두었다면 ``multi_modal``\ 을 포함하지 않으면 벡터 검색이 제외됩니다.
보통은 이 설정을 비워 둡니다.

모델을 바꿀 때는 재크롤링까지 진행한다
--------------------------------------

모델과 차원 수는 반드시 함께 변경합니다.
차원 수는 인덱스 생성 시 매핑에 고정되므로, 변경 후에는 다음 절차가 필요합니다.

1. [시스템 정보] > [유지보수]에서 "재인덱싱"("에일리어스 갱신" 활성화)을 실행하여 새 차원 수로 인덱스를 다시 만든다
2. 다시 크롤링한다

재인덱싱은 문서를 복사할 뿐 벡터를 다시 계산하지 않습니다.
차원 수가 같더라도 모델이나 CLIP 서버를 바꾸면 벡터 공간이 달라지므로, 문서를 삭제한 뒤 다시 크롤링합니다.
``docker-multimodalsearch``\ 에서는 ``.env``\ 의 ``CLIP_MODEL_NAME``\ 과 ``MULTIMODAL_DIMENSION``\ 을 변경합니다.
절차는 README의 "Model swap"에 있습니다.

CPU와 GPU
---------

``docker-multimodalsearch``\ 의 기본 모델(512차원)은 CPU에서 동작하는 것을 전제로 하며, ``CLIP_DEVICE=cpu``\ 가 기본값입니다.
더 큰 ``xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k``\ (1024차원)로 바꾸는 경우 GPU가 권장되며, ``CLIP_DEVICE=auto``\ 로 하면 GPU가 있을 때 사용합니다.

정리
====

- ``fess-webapp-multimodal``\ 은 텍스트로 GIF/JPEG/PNG 이미지를 찾는 기능입니다. 이미지로 검색하거나 문서에 포함된 이미지를 벡터화할 수는 없습니다
- 시험해 보려면 ``docker-multimodalsearch``\ 의 ``v15.9.0``\ 을 사용하고 ``FESS_THEMES_REF=15.9.x``\ 를 지정합니다
- 설정은 ``content_chunker.*``\ 를 ``system.properties``\ (또는 ``-Dfess.system.*``)에 작성합니다
- 벡터 검색이 사용되었는지는 검색 API의 ``searcher``\ 에 있는 ``multi_modal``\ 로 확인합니다
- 영어 이외의 검색어(한국어 등)에는 다국어 모델이 필요하며, 텍스트 시맨틱 검색과는 같은 Fess에서 함께 사용할 수 없습니다

다음에 읽을 글
==============

- :doc:`guide-18` — 텍스트 문서를 벡터로 검색하기(멀티모달과는 별도의 구성)
- :doc:`guide-02` — Docker로 Fess를 실행하는 기본
- :doc:`guide-11` — 검색 API로 업무 시스템과 연동하기

참고 자료
=========

- `docker-multimodalsearch(v15.9.0) <https://github.com/codelibs/docker-multimodalsearch/tree/v15.9.0>`__
- `fess-webapp-multimodal(15.9.0) <https://github.com/codelibs/fess-webapp-multimodal/tree/fess-webapp-multimodal-15.9.0>`__
