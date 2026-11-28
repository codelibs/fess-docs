=======================================
시맨틱 검색으로 의미가 가까운 문서 찾기
=======================================

들어가며
========

사용자가 "월급 받는 통장을 바꾸고 싶다"로 검색해도 사내 규정의 표현이 "급여 계좌 변경 절차"라면 키워드 검색으로는 찾을 수 없습니다.
Fess 15.9에는 본문을 의미 벡터로 변환하여 검색하는 "시맨틱 검색"이 본체에 내장되어 있어 플러그인 없이 사용할 수 있습니다(임베딩 모델의 연결 대상에 따라서는 플러그인을 추가합니다).

이 글의 절차를 따라 하면 다음을 할 수 있게 됩니다.

- 시맨틱 검색이 도움이 되는 경우와 키워드 검색으로 충분한 경우를 구별한다
- Docker로 시맨틱 검색이 설정된 환경을 바로 실행한다
- 기존 Fess에서 ``content_chunker.*``\ 를 설정하고 인덱서 작업으로 벡터를 만든다
- 검색 결과가 벡터 검색으로 찾은 것인지 ``searcher`` 필드로 확인한다

AI 검색 모드(RAG) 설정은 :doc:`guide-19`\ 에서 다룹니다.

시맨틱 검색이 도움이 되는 경우
==============================

Fess의 시맨틱 검색은 키워드 검색(BM25)을 대체하는 것이 아닙니다.
키워드 검색과 벡터 검색을 모두 실행하고, 결과를 Rank Fusion(RRF)으로 하나의 순위로 합치는 "하이브리드 검색"으로 동작합니다.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 시맨틱 검색이 도움이 된다
     - 키워드 검색으로 충분하다
   * - 사용자와 문서가 쓰는 말이 다르다("월급 통장"과 "급여 계좌", "집에서 일하기"와 "재택근무")
     - 제품 모델 번호, 오류 코드, 사람 이름 등 문서와 같은 문자열로 찾는다
   * - 문장으로 질문한다("새 PC를 신청하려면")
     - 바꿔 말하는 조합이 적어서 동의어 사전에 모두 등록할 수 있다
   * - 한국어로 검색해서 영어 문서를 찾고 싶다(다국어 지원 임베딩 모델이 필요)
     - 구문 지정이나 와일드카드 등의 검색 구문을 사용한다(이 경우에는 벡터 검색 자체가 실행되지 않습니다)

바꿔 말하는 조합이 한정되어 있다면 동의어 사전을 먼저 시도하는 편이 간편합니다.
검색 로그의 제로 히트 검색어로부터 동의어를 등록하는 절차는 :doc:`guide-08`\ 을 참조하십시오.

Fess 내부의 처리 흐름
=====================

#. 크롤러가 평소처럼 문서를 인덱스에 등록합니다. 이 시점에는 벡터가 없습니다.
#. 스케줄러 작업 ``Content Chunk Vector Indexer``\ 가 처리되지 않은 문서를 찾아 본문을 청크(조각)로 나누고, 청크마다 임베딩 벡터를 만들어 ``content_chunk_vector`` 필드에 저장합니다. 결과는 ``content_chunk_status`` 필드에 기록됩니다.
#. ``content_chunker.search.enabled=true``\ 일 때는 검색할 때마다 키워드 검색(서처 이름 ``default``)과 벡터 검색(서처 이름 ``semantic_chunk``)이 실행되고, RRF로 융합됩니다.

이 작업은 초기 상태에서 비활성화되어 있으며 크롤링과도 연동되지 않습니다.
설정을 넣기만 해서는 벡터가 만들어지지 않고 검색 결과도 키워드 검색 그대로라는 점에 주의하십시오.

전제 조건
=========

**k-NN 플러그인이 포함된 OpenSearch**

Fess 15.9가 만드는 검색 인덱스에는 시맨틱 검색 사용 여부와 관계없이 ``knn_vector`` 타입의 필드가 포함됩니다.
Docker의 ``ghcr.io/codelibs/fess-opensearch`` 이미지와 표준 배포판 OpenSearch에는 k-NN 플러그인이 포함되어 있습니다.
k-NN 플러그인을 포함하지 않는 minimal 배포판에서는 인덱스를 만들 수 없어 Fess가 기동하지 않습니다.

**임베딩 프로바이더**

텍스트를 벡터로 변환하는 모델의 연결 대상을 ``content_chunker.embedding.name``\ 으로 선택합니다.

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - 설정값
     - 필요한 것
     - 내용
   * - ``opensearch``\ (기본값)
     - 추가 플러그인 불필요
     - OpenSearch의 ML Commons에 배포한 모델을 사용합니다
   * - ``ollama``
     - 플러그인 ``fess-llm-ollama``
     - Ollama의 임베딩 모델을 사용합니다(기본 모델은 ``embeddinggemma``)
   * - ``openai``
     - 플러그인 ``fess-llm-openai``
     - OpenAI의 임베딩 API를 사용합니다(기본 모델은 ``text-embedding-3-small``)
   * - ``gemini``
     - 플러그인 ``fess-llm-gemini``
     - Google Gemini의 임베딩 API를 사용합니다
   * - ``bedrock``
     - 플러그인 ``fess-llm-bedrock``
     - Amazon Bedrock의 임베딩 모델을 사용합니다

플러그인은 Fess와 같은 마이너 버전(15.9.x)을 설치하고, 설치 후 Fess를 재시작합니다.
OpenAI·Gemini·Bedrock은 종량 과금이므로 첫 작업 실행 시 기존 전체 문서분의 이용 요금이 한꺼번에 발생합니다.

가장 빠른 방법: docker-semanticsearch로 시험해 보기
===================================================

docker-semanticsearch 저장소는 시맨틱 검색이 설정된 Fess 15.9를 Docker Compose로 기동합니다.
OpenSearch의 ML Commons에 다국어 임베딩 모델(``paraphrase-multilingual-MiniLM-L12-v2``, 384차원)을 자동으로 배포하고, 인덱서 작업의 활성화까지 마칩니다.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-semanticsearch.git
    $ cd docker-semanticsearch
    $ FESS_THEMES_REF=15.9.x bash ./bin/setup.sh
    $ docker compose up -d
    $ docker compose logs -f init-semantic init-fess-chunk

``setup.sh``\ 는 검색 화면의 테마 ``semanticlens``\ 를 ``fess-themes`` 저장소에서 가져옵니다.
``v15.9.0``\ 의 기본 가져오기 대상인 ``main``\ 에 있는 테마는 Fess 15.10 이후용(``minFessVersion: 15.10``)이므로, 15.9용 테마가 있는 ``15.9.x`` 브랜치를 ``FESS_THEMES_REF``\ 로 지정하고 있습니다.

처음에는 모델(약 490MB) 다운로드에 몇 분이 걸립니다.
``docker compose ps -a``\ 에서 ``fess01``\ 이 healthy가 되고 ``init-semantic``\ 과 ``init-fess-chunk``\ 가 ``Exited (0)``\ 이 되면 준비가 끝난 것입니다.

그다음에는 일반 Fess와 마찬가지로 관리 화면(``http://localhost:8080/admin``)에서 크롤링 설정을 만들고 크롤링을 실행합니다.
이 구성에서는 인덱서 작업이 1시간마다 실행됩니다.
바로 벡터를 만들고 싶다면 [시스템] > [스케줄러]에서 ``Content Chunk Vector Indexer``\ 를 열고 [지금 시작]을 클릭합니다.

이 구성은 이 글의 후반에서 설명하는 설정 외에 다음 값을 사용합니다.

- 융합을 OpenSearch 쪽에서 수행(``rank.fusion.engine.enabled=true``)
- 청크 길이는 250자(모델의 입력 상한이 128토큰이므로)
- 유사도 하한 ``content_chunker.search.min_score=0.5``
- 검색 결과마다 키워드·시맨틱·양쪽 중 어느 것으로 찾았는지 표시하는 테마 ``semanticlens``

값을 변경하는 방법은 저장소 README의 Configuration을 참조하십시오.

기존 Fess에서 시맨틱 검색 활성화하기
====================================

여기서는 Ollama의 ``embeddinggemma``\ (768차원, 다국어 지원)를 사용하는 예로 절차를 보여 줍니다.
내장 ``opensearch`` 프로바이더를 사용하는 경우에는 절차 1·2 대신 ML Commons에 모델을 배포하고 ``content_chunker.embedding.name=opensearch``\ 와 ``content_chunker.embedding.opensearch.model.id``\ 를 설정합니다.
절차는 `시맨틱 검색 <https://fess.codelibs.org/ko/stable/config/search-semantic.html>`__\ 의 "설정 절차(opensearch 프로바이더 예시)"에 있습니다.

절차 1: 플러그인 설치하기
-------------------------

[시스템] > [플러그인] > [설치]에서 ``fess-llm-ollama``\ 의 15.9.x를 선택하여 설치하고 Fess를 재시작합니다.
Docker의 경우에는 ``compose.yaml``\ 의 ``fess01``\ 에 ``FESS_PLUGINS=fess-llm-ollama:15.9.0``\ 을 지정합니다.

절차 2: 임베딩 모델 준비하기
----------------------------

Ollama를 실행하는 서버에서 모델을 가져옵니다.

::

    $ ollama pull embeddinggemma

절차 3: system.properties에 설정 작성하기
-----------------------------------------

``content_chunker.*`` 설정은 ``system.properties``\ 에서만 읽어 들입니다.
``fess_config.properties``\ 나 ``-Dfess.config.``\ 로 작성해도 무시됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 설치 형태
     - 작성 위치
   * - ZIP 버전
     - ``app/WEB-INF/conf/system.properties``
   * - RPM/DEB 버전
     - ``/etc/fess/system.properties``
   * - Docker(docker-fess)
     - ``compose.yaml``\ 의 ``FESS_JAVA_OPTS``\ 에 ``-Dfess.system.<키 이름>=<값>`` 형식으로 지정

Docker 컨테이너 안의 ``/opt/fess/system.properties``\ 도 읽어 들이지만, docker-fess의 ``fess01``\ 에는 볼륨이 없으므로 ``docker compose down``\ 으로 사라집니다.

다음 내용을 작성합니다.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=ollama
    content_chunker.embedding.dimension=768
    content_chunker.embedding.ollama.api.url=http://localhost:11434
    content_chunker.embedding.ollama.model=embeddinggemma
    content_chunker.search.enabled=true

``api.url``\ 은 Fess에서 본 Ollama의 주소입니다.
Fess가 Docker에서 동작하는 경우 ``localhost``\ 는 컨테이너 자신을 가리키므로, 컨테이너에서 도달할 수 있는 주소로 바꾸십시오.

``content_chunker.embedding.dimension``\ 은 반드시 모델의 출력 차원 수와 일치시킵니다.
이 값은 인덱스를 만드는 시점에 매핑에 기록되며 나중에 변경할 수 없습니다.

절차 4: Fess 재시작하기
-----------------------

``content_chunker.search.enabled``\ 를 ``true``\ 로 바꾼 변경은 재시작할 때까지 반영되지 않습니다(다른 ``content_chunker.*``\ 는 실행 중에 다시 읽어 들입니다).

절차 5: 기존 인덱스 다시 만들기
-------------------------------

한 번이라도 Fess를 기동한 적이 있는 환경에서는 새 차원 수의 매핑이 인덱스에 반영되어 있지 않습니다.
[시스템 정보] > [유지보수]의 "재인덱싱"에서 "에일리어스 갱신"을 활성화하고 [시작]을 클릭합니다.
첫 기동 전에 절차 3을 마친 신규 환경에서는 필요하지 않습니다.

재인덱싱은 백그라운드에서 비동기로 진행되며, 화면에는 완료가 표시되지 않습니다.
다음 절차로 넘어가기 전에 ``fess.search``\ 와 ``fess.update`` 두 에일리어스가 모두 새 인덱스(``fess.<타임스탬프>``)를 가리키는지 확인합니다.

::

    $ curl -s "http://localhost:9200/_cat/aliases/fess.search,fess.update?v"

오래된 인덱스는 자동으로 삭제되지 않으므로 확인이 끝나면 수동으로 삭제합니다.
크롤링을 다시 할 필요는 없습니다.
인덱서 작업은 저장된 본문으로부터 벡터를 만듭니다.

절차 6: 인덱서 작업을 활성화하고 실행하기
-----------------------------------------

#. [시스템] > [스케줄러]에서 ``Content Chunk Vector Indexer``\ 를 열고 [편집]을 클릭합니다.
#. "상태"의 "유효"에 체크하고, 필요하면 스케줄을 바꾼 뒤 [갱신]을 클릭합니다. 기본 스케줄은 ``0 13 * * *``\ (매일 13:00)입니다.
#. 상세 화면으로 돌아오면 [지금 시작]이 표시되므로 클릭하여 한 번 실행합니다.

작업은 크롤링과 연동되지 않으므로, 크롤링한 문서는 키워드로는 바로 검색할 수 있지만 벡터 검색의 대상이 되는 것은 다음에 이 작업이 실행된 후입니다.
스케줄은 크롤링 작업이 끝나는 시각보다 뒤로 설정하십시오.

동작 확인하기
=============

벡터가 만들어졌는지 확인하기
----------------------------

문서별 처리 결과를 OpenSearch로 집계합니다.

::

    $ curl -s -XPOST "http://localhost:9200/fess.search/_search" \
        -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 값
     - 의미
   * - ``pending``
     - 미처리(다음 작업 실행 시 처리됩니다). 다시 크롤링된 문서도 이 상태로 돌아갑니다
   * - ``done``
     - 청크 분할과 벡터 생성이 완료됨
   * - ``chunked``
     - 청크 분할만 됨. 프로바이더의 플러그인이 설치되어 있지 않을 때도 이 상태가 됩니다
   * - ``skipped``
     - 본문이 비어 있거나 청크 수가 상한(기본값 1000)을 넘음
   * - ``fail``
     - 실패. 로그 파일 ``fess-chunk.log``\ 에서 원인을 확인합니다

작업을 실행할 때마다 ``pending``\ 이 줄고 ``done``\ 이 늘어나면 순조로운 것입니다.

벡터 검색으로 찾은 결과인지 확인하기
------------------------------------

검색 결과의 ``searcher`` 필드에는 그 문서를 찾은 서처 이름이 들어갑니다.
초기 상태에서는 검색 API 응답에 포함되지 않으므로 ``fess_config.properties``\ 에 다음 한 줄을 추가하고 재시작합니다(Docker에서는 ``-Dfess.config.query.additional.api.response.fields=searcher``).

::

    query.additional.api.response.fields=searcher

키워드가 문서와 일치하지 않는 바꿔 말한 표현으로 검색합니다.
"급여 계좌 변경 절차"를 설명한 문서가 있다면 다음과 같이 검색합니다.

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=월급 받는 통장을 바꾸고 싶다" \
      | jq '.response.data[] | {title, searcher}'

``searcher``\ 가 ``["semantic_chunk"]``\ 인 결과는 벡터 검색으로만 찾은 문서이고, ``["default", "semantic_chunk"]``\ 는 양쪽에서 찾은 문서입니다.
모든 결과가 ``["default"]``\ 뿐이라면 벡터 검색이 결과를 반환하지 않고 있는 것입니다.
다음 절을 확인하십시오.

자주 걸려 넘어지는 점
=====================

**이전 플러그인 시절의 rank.fusion.searchers가 남아 있다**

15.7 이전의 ``fess-webapp-semantic-search`` 플러그인에서는 ``-Drank.fusion.searchers=default,semantic``\ 을 지정했습니다.
15.9의 서처 이름은 ``semantic_chunk``\ 이므로, 이 설정이 남아 있으면 시맨틱 검색이 실행되지 않고 키워드 검색 결과만 반환됩니다.
기동 시 ``rank.fusion.searchers allows 'semantic' but not 'semantic_chunk'``\ 라는 WARN 로그가 출력됩니다.
JVM 옵션과 [시스템] > [일반]의 "시스템 속성" 항목을 모두 확인하여 이 설정을 삭제하십시오(지정하지 않으면 모든 서처가 사용됩니다).
이전 플러그인에서 마이그레이션하는 절차는 `시맨틱 검색 <https://fess.codelibs.org/ko/stable/config/search-semantic.html>`__\ 의 "15.7 이전 버전에서 업그레이드하는 경우의 마이그레이션"을 참조하십시오.

**검색 구문이 포함된 쿼리에서는 벡터 검색이 실행되지 않는다**

다음 쿼리는 키워드 검색만으로 처리됩니다.

- 구문(``"..."``), 와일드카드, 퍼지 검색, 범위 지정
- 반각 ``?``\ 로 끝나는 문장("…이란?"). 일본어나 중국어에서 쓰는 전각 "？"는 대상이 아닙니다
- 제외(``-단어``, ``NOT 단어``)나 부스트(``단어^2``)
- 정렬을 지정한 검색

``label:``\ 이나 ``site:``, 패싯으로 좁히는 것은 벡터 검색에도 필터로 적용되므로 문제없습니다.

**차원 수가 맞지 않거나, 설정하지 않고 인덱스를 만들었다**

``content_chunker.embedding.dimension``\ 을 설정하지 않은 채 인덱스를 만들면 매핑은 768차원이 되고, 작업은 문서를 ``fail``\ 로 만듭니다.
모델의 차원 수가 768이 아니라면 올바른 값을 설정한 다음 절차 5의 재인덱싱을 다시 수행합니다.
``fail``\ 과 ``skipped``\ 는 작업을 다시 실행해도 다시 처리되지 않습니다.
원인을 해결한 후 ``content_chunker.job.retry_failed=true``\ 를 일시적으로 설정하고 작업을 실행합니다.

**임베딩 모델을 바꿨다**

저장된 벡터는 이전 모델로 만들어졌으므로, 모델만 바꾸면 검색 정확도가 무너집니다(차원 수가 같으면 오류도 나지 않습니다).
``content_chunk_vector``\ 와 ``content_chunk_status``\ 를 삭제하고 작업을 다시 실행하는 절차가 레퍼런스의 "주의 사항"에 있습니다.

**관련이 적은 문서까지 상위에 온다**

벡터 검색은 유사도가 낮은 문서도 가까운 순서대로 반환합니다.
``content_chunker.search.min_score``\ 에 코사인 유사도의 하한(0~1)을 설정하면 그에 미치지 못하는 문서를 제외할 수 있습니다.
적절한 값은 모델과 문서에 따라 달라지므로, 제로 히트였던 검색어와 무관한 검색어 양쪽으로 검색하면서 조정하십시오.

**2페이지 이후 후반에서 결과의 경향이 바뀐다**

Fess 쪽에서 융합하는 기본 구성에서는 각 서처의 상위 200건(``rank.fusion.window_size``)까지만 융합되고, 101건째 이후는 키워드 검색만의 결과가 됩니다.
히트 건수도 벡터 검색만 찾은 문서만큼 늘어납니다.
융합의 구조와 조정 항목(``rank.fusion.rank_constant``, OpenSearch 쪽에서의 융합)은 `하이브리드 검색과 Rank Fusion <https://fess.codelibs.org/ko/stable/config/rank-fusion.html>`__\ 을 참조하십시오.

AI 검색 모드·멀티모달 검색과의 관계
===================================

AI 검색 모드(RAG)는 시맨틱 검색을 활성화하지 않아도 사용할 수 있습니다.
``content_chunker.enabled=true``\ 로 벡터가 만들어진 문서에 대해서는 답변에 사용할 본문을 질문에 가까운 청크로만 좁히므로, 긴 문서라도 관련 부분을 LLM에 전달할 수 있습니다.
AI 검색 모드 설정은 :doc:`guide-19`\ 를 참조하십시오.

이미지와 텍스트를 함께 검색하는 멀티모달 검색(``fess-webapp-multimodal``)은 같은 Fess에서 이 글의 텍스트 시맨틱 검색과 동시에 사용할 수 없습니다.
자세한 내용은 :doc:`guide-21`\ 을 참조하십시오.

다음에 읽을 글
==============

- 검색 로그의 제로 히트 검색어를 동의어나 키 매치로 개선하고 싶다: :doc:`guide-08`
- 생성형 AI가 사내 문서를 바탕으로 답변하게 하고 싶다: :doc:`guide-19`
- 이미지도 포함해서 검색하고 싶다: :doc:`guide-21`
- 검색 API로 업무 시스템에서 검색하고 싶다: :doc:`guide-11`

참고 자료
=========

- `시맨틱 검색(콘텐츠 청킹 + 벡터 검색) <https://fess.codelibs.org/ko/stable/config/search-semantic.html>`__
- `하이브리드 검색과 Rank Fusion(시맨틱 + 키워드) <https://fess.codelibs.org/ko/stable/config/rank-fusion.html>`__
- `Ollama 설정 (로컬 LLM / RAG) <https://fess.codelibs.org/ko/stable/config/llm-ollama.html>`__
- `스케줄러 <https://fess.codelibs.org/ko/stable/admin/scheduler-guide.html>`__
- `유지보수 <https://fess.codelibs.org/ko/stable/admin/maintenance-guide.html>`__
- `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
- `docker-semanticsearch(GitHub) <https://github.com/codelibs/docker-semanticsearch>`__
