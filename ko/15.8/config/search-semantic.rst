===================================================
시맨틱 검색(콘텐츠 청킹 + 벡터 검색)
===================================================

개요
====

|Fess| 15.8\ 에서는 문서 본문을 청크(조각)로 분할하고 각 청크의 임베딩 벡터를 생성·저장하는
**콘텐츠 청킹 기능**\ 이 코어에 통합되었습니다. 생성된 벡터는 다음 두 가지 용도로 사용됩니다.

- **시맨틱 검색**: 키워드(BM25) 검색과 벡터 검색을 Rank Fusion으로 통합한 하이브리드 검색입니다.
  키워드가 정확히 일치하지 않아도 질의와 의미적으로 가까운 문서가 매칭될 수 있습니다.
- **AI 검색 모드(RAG)**: 답변을 생성할 때 질문과 의미적으로 가장 가까운 청크만 LLM의 컨텍스트로
  선택하여 답변 품질과 토큰 효율을 향상시킵니다.

이 기능은 모두 기본적으로 비활성화되어 있습니다. 활성화하지 않는 한 |Fess|\ 는 이전과 완전히
동일하게 키워드 검색만으로 동작합니다. 15.7 이전 버전에서 |Fess|\ 를 업그레이드하는 경우나
``fess-webapp-semantic-search`` 플러그인을 사용하고 있었던 경우에는 :ref:`semantic-search-migration`
을 참조하세요.

처리 흐름
----------

1. 크롤러는 평소처럼 문서를 인덱싱합니다(이 시점에는 청크가 존재하지 않습니다).
2. 스케줄러 작업 **Content Chunk Vector Indexer**\ 가 미처리 문서를 찾아 본문(``content`` 필드)을
   청크로 분할하고 임베딩 벡터를 생성하여 ``content_chunk_vector`` 필드에 저장합니다. 이때
   ``content`` 필드 자체도 청크의 배열로 재작성됩니다(``content_length`` 는 원래 값 그대로
   유지됩니다).
3. 처리 결과는 ``content_chunk_status`` 필드에 기록됩니다(아래에서 설명).
4. ``content_chunker.search.enabled=true`` 인 경우, 검색 시점에 시맨틱 서처가 Rank Fusion에
   참여합니다.

전제 조건
=========

- **k-NN 플러그인이 포함된 OpenSearch**: |Fess| 15.8\ 에서는 콘텐츠 청킹 기능의 활성화 여부와
  관계없이 검색 인덱스(``fess.search``)의 매핑에 ``content_chunk_vector`` 필드(``nested``
  타입이며, 그 ``vector`` 서브필드가 ANN용 ``knn_vector`` 타입)가 항상 포함되고, 인덱스 설정에도
  ``index.knn: true`` 가 항상 포함됩니다. 이 때문에 OpenSearch에 k-NN 플러그인이 설치되어 있지
  않으면 인덱스 신규 생성 자체가 실패하며, |Fess|\ 는 시작할 수 없습니다.

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - 구성
       - k-NN 플러그인 지원 여부
     * - 임베디드 OpenSearch(``bin/fess``, 또는 ``SEARCH_ENGINE_HTTP_URL``\ 을 설정하지 않은
         TAR.GZ/ZIP 패키지의 기본 상태)
       - k-NN 플러그인이 동봉되어 있습니다. 다만 JNI 네이티브 라이브러리는 포함되지 않으므로 지원되는
         ANN 엔진은 ``lucene`` 뿐입니다. ``content_chunker.search.knn.engine`` 은 ``faiss`` 도
         값으로 허용하며, 여기에 설정해도 매핑 자체는 정상적으로 생성되지만 **쓰기가 일어날
         때마다 문서가 소리 없이 유실되고 검색 결과도 0건이 됩니다**\ (|Fess|\ 는 이 조합을
         감지하면 시작 시 경고 로그를 남깁니다).
     * - Docker(``ghcr.io/codelibs/fess-opensearch``), 별도로 설치한 외부 OpenSearch에 항상
         연결하는 RPM/DEB 패키지, 또는 그 밖의 외부 OpenSearch(표준 배포판)
       - ``faiss`` 를 포함하여 완전히 지원됩니다.
     * - 외부 OpenSearch의 **minimal 배포판**
       - **지원되지 않습니다.** k-NN 플러그인이 포함되어 있지 않으므로 인덱스 신규 생성이
         실패합니다.

  ``content_chunker.search.knn.engine`` 은 위의 어떤 구성에서도 ``nmslib`` 를 값으로 허용하지
  않습니다. ``content_chunk_vector`` 는 ``nested`` 필드이며, k-NN 플러그인이 nested 필드를
  지원하는 엔진은 ``lucene`` / ``faiss`` 뿐이기 때문입니다(``nmslib`` 는 OpenSearch 3.0 이후
  지원 중단·제한되기도 했습니다). 설정하면 경고와 함께 ``lucene`` 으로 대체됩니다. 다른 ANN
  설정값은 아래 「설정 레퍼런스」를 참조하세요.

- **외부 클러스터의 OpenSearch 버전**: 동봉된 ``fess.search`` 인덱스 설정은
  ``fess_indices/fess.json``\ (및 AWS/cloud 버전)에서 ``index.knn`` 과
  ``knn.derived_source.enabled`` 를 항상 전송합니다. 후자는 k-NN 플러그인의 비교적 새로운
  설정이며, 이를 인식하지 못하는 오래된 OpenSearch에서는 k-NN 플러그인 유무와 관계없이 인덱스
  생성에 실패합니다. |Fess| 15.8\ 이 지원하는 OpenSearch 버전은
  :doc:`../install/prerequisites` 를 참조하세요.

- **임베딩 프로바이더**: 다음 중 하나를 사용합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - 설정값
     - 제공 주체
     - 설명
   * - ``opensearch``
     - |Fess| 코어(내장)
     - OpenSearch ML Commons에 배포된 임베딩 모델을 사용합니다. 추가 플러그인이 필요하지 않습니다.
       기본 설정값입니다.
   * - ``ollama``
     - ``fess-llm-ollama`` 플러그인
     - Ollama 임베딩 모델(예: ``nomic-embed-text``)을 사용합니다.
   * - ``openai``
     - ``fess-llm-openai`` 플러그인
     - OpenAI 임베딩 API를 사용합니다.
   * - ``gemini``
     - ``fess-llm-gemini`` 플러그인
     - Google Gemini 임베딩 API를 사용합니다.
   * - ``none``
     - |Fess| 코어(내장)
     - 문서를 청크로 분할만 하고 벡터는 생성하지 않습니다(chunk-only 모드).

설정 레퍼런스
===============

모든 ``content_chunker.*`` 설정은 **시스템 프로퍼티**\ (``system.properties``) 하나의 채널로
통합되어 있습니다. ``app/WEB-INF/conf/system.properties``\ (RPM/DEB 패키지는
``/etc/fess/system.properties``, Docker 버전은 ``/opt/fess/system.properties``)에 설정하거나,
시작 옵션 ``-Dfess.system.<키>`` 로 초기값을 지정할 수 있습니다. 값은 실행 중에 다시 로드되므로
대부분의 설정은 변경 직후 바로 반영됩니다. 유일한 예외는 ``content_chunker.search.enabled`` 를
활성화(``false`` → ``true``)하는 경우입니다. 시맨틱 서처는 시작 시에만 등록되므로, **이 변경을
반영하려면 재시작이 필요합니다**.

.. note::

   ``content_chunker.*`` 의 키 목록은 ``fess_config.properties`` 에도 주석으로 기재되어 있지만,
   이 값들은 ``system.properties`` 채널에서만 읽힙니다. ``fess_config.properties`` 나
   ``-Dfess.config.<키>`` 에 기술해도 무시되므로 반드시 ``system.properties`` 에 설정하세요.
   또한 관리 화면의 「시스템 정보」→「설정 정보」는 현재 값을 **확인만 할 수 있는** 화면이며,
   이 화면에서 ``content_chunker.*`` 를 설정할 수는 없습니다.

system.properties 설정
------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``content_chunker.enabled``
     - ``false``
     - 콘텐츠 청킹 기능 전체의 마스터 스위치
   * - ``content_chunker.chunker.name``
     - ``length``
     - 청크 분할 방식
   * - ``content_chunker.length.chunk_size``
     - ``800``
     - 청크당 문자 수
   * - ``content_chunker.length.overlap``
     - ``0``
     - 청크 간에 중복시킬 문자 수
   * - ``content_chunker.max_chunks_per_document``
     - ``1000``
     - 문서당 최대 청크 수. 이를 초과하는 문서는 ``skipped`` 로 표시됩니다
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - 임베딩 프로바이더(``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``)
   * - ``content_chunker.embedding.dimension``
     - ``768``
     - 임베딩 벡터의 차원 수. 매핑 생성 시 이 값이 사용되므로 사용하는 임베딩 모델의 차원 수와
       **반드시** 일치해야 합니다. 이 값에는 읽기 경로가 두 가지 있으며 동작이 다릅니다. 인덱스
       매핑 생성 시에는 미설정·숫자가 아닌 값·0 이하·``16000``\ (k-NN 플러그인 자체의 상한) 초과
       중 어느 경우든 경고와 함께 ``768`` 이 사용됩니다. 반면 임베딩 처리 실행 시에는 폴백이
       없어, 미설정·숫자가 아닌 값·0 이하는 모두 오류가 됩니다. ``16000`` 을 초과하는 값은 실행
       시에 거부되지 않으므로, 매핑만 ``768`` 로 생성되어 차원 불일치가 발생합니다
   * - ``content_chunker.job.concurrency``
     - ``2``
     - 인덱서 작업의 병렬 워커 수
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - 한 번의 배치로 가져와서 쓰는 문서 수
   * - ``content_chunker.job.max_documents_per_run``
     - ``-1``\ (무제한)
     - 작업 1회 실행당 처리하는 최대 문서 수. ``0`` 이하의 값은 모두 무제한으로 취급됩니다
   * - ``content_chunker.job.retry_failed``
     - ``false``
     - ``true`` 로 설정하면 이전 실행에서 ``content_chunk_status=fail`` 로 끝난 문서도 다음 실행의
       처리 대상에 포함됩니다. 자동 재시도나 시도 횟수 기록은 없으며, 근본 원인을 수정한 뒤
       일시적으로 활성화하여 재시도하는 방식을 의도한 것입니다
   * - ``content_chunker.chat.top_k``
     - ``3``
     - AI 검색 모드가 답변을 생성할 때 선택하는 청크 수
   * - ``content_chunker.search.enabled``
     - ``false``
     - 시맨틱 검색을 위한 Rank Fusion 통합(**활성화에는 재시작이 필요**)
   * - ``content_chunker.search.min_score``
     - (미설정)
     - 결과에 포함되기 위해 필요한 최소 코사인 유사도(0-1). 미설정 시 컷오프 없음. ``ann``
       모드에서 ``search.knn.space_type`` 이 ``cosinesimil`` 이외인 경우에는 코사인 기준의
       컷오프를 정의할 수 없으므로, 경고와 함께 스킵됩니다
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - ANN 인덱스 방식. 현재 허용되는 값은 ``hnsw`` 뿐이며, 그 외의 값은 경고와 함께 ``hnsw`` 로
       대체됩니다(매핑에 반영됨. 변경하려면 인덱스 재작성이 필요)
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - ANN 엔진. 허용되는 값은 ``lucene`` 또는 ``faiss`` 뿐입니다(위의 전제 조건 참조). 그 외의
       값은 경고와 함께 ``lucene`` 으로 대체됩니다(매핑에 반영됨. 변경하려면 인덱스 재작성이
       필요)
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - 거리 공간. 허용되는 값은 ``cosinesimil``, ``innerproduct``, ``l2`` 뿐이며, 그 외의 값은
       경고와 함께 ``cosinesimil`` 로 대체됩니다(매핑에 반영됨. 변경하려면 인덱스 재작성이 필요)
   * - ``content_chunker.search.knn.k``
     - ``100``
     - ANN 쿼리당 검색할 이웃 수(딥 페이징 시 자동으로 확대됨)
   * - ``content_chunker.search.knn.param.ef_search``
     - (미설정)
     - ANN 쿼리의 ``ef_search`` 파라미터

.. note::

   HNSW의 ``m`` 및 ``ef_construction`` 파라미터는 ``doc.json`` 에 하드코딩되어 있으며
   (``m=16`` / ``ef_construction=100``), 설정으로 변경할 수 없습니다.

opensearch 프로바이더 연결 설정
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

내장 ``opensearch`` 프로바이더(OpenSearch ML Commons)의 연결 설정입니다. 위와 동일한
``system.properties`` 파일에 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 50 20 30

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``content_chunker.embedding.opensearch.model.id``
     - (필수)
     - ML Commons에 이미 배포된 모델의 ID
   * - ``content_chunker.embedding.opensearch.api.url``
     - 검색 엔진의 주소
     - ML Commons API 엔드포인트. 미설정 시 |Fess|\ 가 이미 사용 중인 검색 엔진으로 기본
       설정됩니다(예: ``http://localhost:9200``)
   * - ``content_chunker.embedding.opensearch.username`` / ``password``
     - 검색 엔진의 인증 정보
     - 미설정 시 검색 엔진 연결에 사용하는 인증 정보로 대체되지만, 이는 ``api.url``\ 이 설정되지
       않은 동안(즉 대상이 |Fess|\ 가 이미 사용 중인 클러스터와 동일한 경우)에만 적용됩니다.
       ``api.url``\ 을 설정하면 이 대체 동작은 적용되지 않습니다
   * - ``content_chunker.embedding.opensearch.timeout``
     - ``60000``
     - 요청 타임아웃(ms)
   * - ``content_chunker.embedding.opensearch.connect.timeout``
     - ``5000``
     - 연결 타임아웃(ms)
   * - ``content_chunker.embedding.opensearch.retry.max``
     - ``3``
     - 일시적 오류(429, 5xx 등)에 대한 재시도 횟수
   * - ``content_chunker.embedding.opensearch.retry.base.delay.ms``
     - ``2000``
     - 재시도 기본 백오프 지연(ms)
   * - ``content_chunker.embedding.opensearch.availability.check.interval``
     - ``60``
     - 프로바이더 가용성 확인 간격(초)
   * - ``content_chunker.embedding.opensearch.document.prefix`` / ``query.prefix``
     - (빈 값)
     - 임베딩 전에 문서/쿼리 텍스트 앞에 붙이는 접두사

.. warning::

   ``system.properties`` 의 내용은 관리 화면의 「시스템 정보」→「설정 정보」 화면, 「앱 속성」
   패널에서 확인할 수 있습니다. ``content_chunker.embedding.opensearch.password`` 는 이 화면에서
   ``XXXXXXXX`` 로 마스킹되지만 ``username`` 은 그대로 표시됩니다. 또한 ``-Dfess.system.<키>`` 로
   지정한 값은 같은 화면의 「시스템 속성」 패널에 **마스킹되지 않은 채** 표시되므로, 인증 정보는
   시작 옵션이 아니라 ``system.properties`` 에 기술하세요.

기타 프로바이더(ollama / openai / gemini)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ollama`` 프로바이더(``fess-llm-ollama`` 플러그인)는 ``content_chunker.embedding.ollama.``
접두사 아래에 동일한 형식의 설정을 사용합니다(``api.url`` 기본값은 ``http://localhost:11434``,
``model`` 기본값은 ``embeddinggemma``, ``document.prefix`` / ``query.prefix`` 기본값은 각각
``title: none | text:`` / ``task: search result | query:`` 입니다). ``nomic-embed-text`` 계열의
모델을 사용하는 경우에는 ``document.prefix`` / ``query.prefix`` 에 ``search_document:`` /
``search_query:`` 를 명시적으로 설정하세요. 이 접두사는 임베딩할 텍스트에 그대로 연결되며
앞뒤 공백이 잘리지 않으므로, 위의 기본값과 ``search_document:`` / ``search_query:`` 는 모두
**끝에 반각 공백이 하나 포함되어 있습니다**\ . 접두사를 직접 설정할 때는 구분용 공백을
잊지 마세요.
``openai`` 와 ``gemini`` 프로바이더도 각각
``content_chunker.embedding.openai.`` 및 ``content_chunker.embedding.gemini.`` 접두사 아래에
동일한 방식으로 설정합니다. 전체 설정 항목은 각 플러그인의 문서를 참조하세요.

설정 절차(opensearch 프로바이더 예시)
=======================================

이 섹션에서는 내장 ``opensearch`` 프로바이더(ML Commons)를 사용하는 설정 예시를 설명합니다.

1. 임베딩 모델 배포
---------------------

OpenSearch ML Commons에 임베딩 모델을 등록하고 배포합니다. 단일 노드 클러스터에서는 먼저 다음
설정을 적용해야 합니다.

.. code-block:: bash

    curl -XPUT "http://localhost:9200/_cluster/settings" \
         -H "Content-Type: application/json" -d '
    {"persistent": {"plugins.ml_commons.only_run_on_ml_node": false}}'

모델을 등록하고 배포합니다(예: 384차원 문장 임베딩 모델):

.. code-block:: bash

    # 모델 등록(응답의 task_id로부터 model_id를 얻습니다)
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/_register" \
         -H "Content-Type: application/json" -d '
    {
      "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
      "version": "1.0.2",
      "model_format": "TORCH_SCRIPT"
    }'

    # 작업 완료 확인 및 model_id 취득(state가 COMPLETED가 되면 model_id가 반환됩니다)
    curl "http://localhost:9200/_plugins/_ml/tasks/<task_id>"

    # 배포
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # 상태 확인: model_state가 DEPLOYED가 되어야 합니다
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   ``REGISTERED`` 상태 그대로인 모델은 사용할 수 없습니다. 반드시 배포한 뒤 ``model_state`` 가
   ``DEPLOYED`` 가 되었는지 확인하세요.

2. |Fess| 설정
------------------

``app/WEB-INF/conf/system.properties``\ (RPM/DEB 패키지는 ``/etc/fess/system.properties``,
Docker 버전은 ``/opt/fess/system.properties``. 아래 항목은 모두 같은 파일에 기술합니다)::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384
    content_chunker.embedding.opensearch.model.id=<model_id>

시맨틱 검색도 함께 사용하려면 다음도 추가합니다::

    content_chunker.search.enabled=true

변경 후 |Fess|\ 를 재시작합니다.

3. 인덱스 재작성(기존 환경에서 활성화하는 경우)
-------------------------------------------------

``content_chunk_vector`` 필드의 매핑(설정한 차원 수와 ANN 방식 설정 포함)은 ``fess.search``
인덱스가 **새로 생성되는 시점에** 적용됩니다.

- **신규 설치의 경우**: |Fess|\ 를 처음 시작하기 전에 위 설정을 ``system.properties`` 에
  적용해 두면, 인덱스가 처음 생성될 때 올바른 매핑이 자동으로 적용되므로 이 단계는 필요하지
  않습니다.
- **이미 인덱스가 존재하는 경우**\ (즉 이전에 |Fess|\ 를 한 번이라도 시작한 적이 있는 경우): 실행
  중인 인덱스에는 새 매핑이 자동으로 반영되지 않으며, 기존 매핑을 나중에 수정할 수도 없습니다.
  다음과 같이 인덱스를 재작성하세요.

  「시스템 정보」→「유지보수」를 열고, 「재인덱싱」에서 「에일리어스 갱신」을 활성화한 상태로
  실행합니다.

  재작성된 인덱스에 인덱스 설정의 ``index.knn: true`` 와, 설정한 차원 수 및 ANN 방식 설정을 가진
  ``content_chunk_vector`` 매핑이 포함되어 있는지 확인할 수 있습니다(``index.knn`` 은 인덱스
  설정, ANN 방식 설정은 매핑으로 적용 대상이 서로 다릅니다).

.. warning::

   「재인덱싱」은 백그라운드에서 비동기로 실행되며, 관리 화면에는 완료를 알리는 알림이
   표시되지 않습니다. ``_cat/indices`` 는 새 인덱스가 존재한다는 것(상태, 문서 수 등)만
   보여줄 뿐, 에일리어스가 어느 인덱스를 가리키는지는 보여주지 않습니다. 아래 인덱서 작업
   절차로 넘어가기 전에 ``_cat/aliases`` 로 ``fess.search`` 와 ``fess.update`` 가 모두 새
   인덱스를 가리키는지 확인하세요. |Fess|\ 의 로그는 실패 시에만 경고를 남기므로, 로그가
   조용하다는 것이 성공의 증거가 되지는 않으며 알려진 실패가 없다는 것만 나타냅니다. 이전
   인덱스(그동안 ``fess.search`` 에일리어스가 가리키고 있던 실체 인덱스로,
   ``fess.<timestamp>`` 형태의 이름을 가집니다)는 자동으로 삭제되지 않으므로, 더 이상
   필요하지 않게 되면 수동으로 삭제하세요. 두 인덱스가 모두 존재하는 동안에는 인덱스용
   디스크 사용량이 평소의 약 2배가 됩니다.

4. 인덱서 작업 활성화
-----------------------

청크 분할과 임베딩 생성은 스케줄러 작업 **Content Chunk Vector Indexer**\ (ID:
``content-chunk-vector-indexer``; 기본 비활성화; 스케줄 ``0 13 * * *``)가 수행합니다.

「시스템」→「스케줄러」에서 이 작업을 활성화한 뒤 「지금 시작」으로 한 번 실행합니다. 이후에는
크롤링 완료 여부와 관계없이 설정된 일정(기본값은 매일 13:00)에 따라 미처리 문서가 처리됩니다.
이 작업은 크롤링 작업과 연쇄되지 않으므로, 크롤링 직후에 처리하고 싶다면 일정을 크롤링 작업의
예상 완료 시각보다 뒤로 설정하세요.

.. note::

   다중 노드 구성에서는 이 작업을 정확히 하나의 노드에서만 실행하도록 고정하는 것을 권장합니다.
   모든 노드에서 동시에 실행해도 정합성이 깨지지는 않지만, 모든 노드가 동일한 문서를 중복해서
   처리하고 임베딩하게 되어 임베딩 프로바이더에 대한 부하와 비용이 노드 수만큼 배로 늘어납니다.

   고정하려면 다음 **두 가지** 설정이 모두 필요합니다. 둘 중 하나만으로는 고정되지 않습니다.

   1. **작업을 실행하고자 하는 노드에서**: ``app/WEB-INF/classes/fess_config.properties``\ (RPM/DEB
      패키지는 ``/etc/fess/fess_config.properties``)에 ``scheduler.target.name=<임의의 식별자>`` 를
      설정(또는 ``-Dfess.config.scheduler.target.name=<임의의 식별자>`` 로 지정)한 뒤 해당 노드를
      재시작합니다. (기본값은 빈 문자열이며, 다른 모든 노드는 기본값 그대로 둡니다.)
   2. 관리 화면의 「시스템」→「스케줄러」에서 Content Chunk Vector Indexer 작업을 열고, 「대상」
      필드를 ``all`` 에서 1단계에서 설정한 것과 동일한 식별자로 변경한 뒤 저장합니다.

   「대상」 필드의 의미는 :doc:`../admin/scheduler-guide` 를 참조하세요. 「대상」 필드를 ``all``
   로 남겨두면 ``scheduler.target.name`` 을 설정하더라도 작업이 고정되지 **않습니다**. ``all`` 은
   항상 일치하는 특수 값으로 취급되므로, 1단계만 또는 2단계만으로는 충분하지 않으며 반드시 둘 다
   수행해야 합니다.

.. warning::

   고정한 뒤에는 「지금 시작」도 **1단계에서 식별자를 설정한 노드의 관리 화면에서** 실행하세요.
   대상이 아닌 노드에서 「지금 시작」을 누르면 화면에는 작업을 시작했다는 메시지가 표시되지만,
   「대상」이 일치하지 않으므로 작업은 실행되지 않습니다(해당 노드의 로그에 ``Ignoring job`` 이
   INFO로 출력될 뿐입니다).

5. 처리 상태 확인
-------------------

각 문서의 처리 결과는 ``content_chunk_status`` 필드에서 확인할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 값
     - 의미
   * - (필드 없음)
     - 아직 미처리(다음 작업 실행에서 처리됨). 재크롤링된 문서도 이 상태로 돌아갑니다
   * - ``done``
     - 청크 분할과 벡터 생성이 완료됨
   * - ``chunked``
     - 청크 분할만 완료됨(chunk-only 모드). ``embedding.name=none`` 인 경우 외에,
       ``embedding.name`` 에 지정한 프로바이더의 플러그인이 설치되어 있지 않은 경우에도 이
       상태가 됩니다
   * - ``skipped``
     - 처리가 스킵됨(예: ``max_chunks_per_document`` 초과)
   * - ``fail``
     - 처리 실패(로그를 확인하세요)

검색 엔진에 직접 질의하여 상태 분포를 확인할 수 있습니다::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

``missing`` 옵션에 의해 ``content_chunk_status`` 를 가지지 않는(즉 미처리) 문서는 ``pending``
이라는 키의 버킷으로 집계됩니다.

시맨틱 검색의 동작 방식
==========================

``content_chunker.search.enabled=true`` 를 설정하면 시맨틱 서처가 Rank Fusion에 등록되며,
그 이후 키워드 검색 결과와 벡터 검색 결과가 병합됩니다(Rank Fusion의 동작 방식은
:doc:`rank-fusion` 을 참조하세요).
또한 검색 시에는 ``content_chunker.enabled`` 도 함께 참조됩니다. ``content_chunker.enabled=false``
이거나 ``content_chunker.embedding.name=none`` 인 경우에는 서처가 등록되어 있더라도 시맨틱
검색은 실행되지 않습니다(이 판정은 요청마다 이루어지므로 재시작은 필요하지 않습니다).

.. warning::

   시맨틱 서처는 시작 시에 등록되므로 **활성화에는 재시작이 필요합니다**. 비활성화(값을 다시
   ``false`` 로 변경)는 요청 단위로 판정되므로 즉시 반영됩니다.

exact 모드와 ann 모드
------------------------

검색 방식은 인덱스의 상태에 따라 자동으로 선택됩니다.

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - 모드
     - 조건
     - 특징
   * - ``ann``
     - ``index.knn`` 과 ANN 방식 설정을 가진 인덱스
     - HNSW를 이용한 근사 최근접 이웃 검색. 대규모 인덱스에 적합
   * - ``exact``
     - 그 외(``index.knn`` 또는 ANN 방식 설정 중 어느 하나라도 없는 인덱스. 인덱스 상태 판정에
       실패한 경우를 포함)
     - 모든 벡터에 대한 정확한 코사인 유사도 계산. 중소 규모 인덱스에 적합

|Fess| 15.8\ 에서 새로 생성되는 ``fess.search`` 인덱스는 ``content_chunker.search.enabled`` 값과
관계없이 항상 ``index.knn`` 과 ANN 방식 설정을 가지므로, 평소에는 항상 ``ann`` 모드가
사용됩니다. ``exact`` 모드는 이 메커니즘이 도입되기 전에 만들어진 오래된 인덱스를 위한
폴백입니다. 기존 인덱스에는 나중에 k-NN 설정을 추가할 수 없으므로, ``exact`` 모드 인덱스를
``ann`` 모드로 전환하려면 인덱스를 재작성해야 합니다(:ref:`semantic-search-migration` 참조).
또한 이 판정 결과는 60초 동안 캐시되므로, 인덱스를 재작성한 직후에는 반영되기까지 최대 60초가
걸립니다.

스코어 컷오프
----------------

``content_chunker.search.min_score`` 에 코사인 유사도(0-1)를 설정하면, 가장 유사도가 높은
청크마저 그 값에 도달하지 못하는 문서가 시맨틱 검색 결과에서 제외됩니다(문서의 스코어는 가장
점수가 높은 청크의 스코어가 되므로, 컷오프는 문서 단위로 동작합니다). 어휘가 겹치지 않는 쿼리가
너무 광범위하게 매칭될 때 히트 수를 줄이는 용도로 사용합니다::

    content_chunker.search.min_score=0.4

설정값은 ``exact`` / ``ann`` 어느 모드에서도 코사인 유사도로 해석됩니다(내부적으로 모드별 스코어
스케일로 변환됩니다).

.. note::

   이 컷오프가 적용되는 것은 ``content_chunker.search.knn.space_type`` 이
   ``cosinesimil``\ (기본값)인 경우뿐입니다. ``innerproduct`` 나 ``l2`` 를 지정한 ``ann`` 모드
   인덱스에서는 코사인 유사도를 정의할 수 없으므로, 컷오프는 경고 로그를 한 번 출력한 뒤
   스킵됩니다.

제한 사항
----------

- **검색 구문을 포함하는 쿼리에서는 시맨틱 검색이 스킵**\ 되고 키워드 검색만 실행됩니다. 판정은
  쿼리를 조립한 **뒤**\ 의 문자열에 대해 이루어지며, ``"`` ``(`` ``)`` ``:`` ``[`` ``]`` ``{``
  ``}`` ``^`` ``~`` ``*`` ``?`` ``\``, ``&&``, ``||``, 맨 앞 또는 공백 바로 뒤의 ``+`` / ``-``,
  대문자 ``AND`` / ``OR`` / ``NOT`` / ``TO`` 중 하나라도 포함되면 대상이 됩니다. 따라서 사용자가
  검색 구문을 입력하지 않았더라도 다음 조작은 마찬가지로 스킵됩니다.

  - 라벨 지정(내부적으로 ``label:"..."`` 이 부가됩니다)
  - 정렬 조건 지정(내부적으로 ``sort:...`` 이 부가됩니다)
  - 패싯을 이용한 좁히기(내부적으로 ``filetype:...`` 등이 부가됩니다)
  - 상세 검색의 구문 검색·제외어·파일 종류·사이트 지정·일시 지정
  - 연관 쿼리가 설정된 검색어(내부적으로 ``("A" OR "B")`` 로 전개됩니다)

  반각 ``?`` 도 대상에 포함되므로, "~란?"처럼 반각 물음표로 끝나는 자연문도 스킵됩니다(전각
  ``？`` 는 대상이 아닙니다).
- 위치 정보 검색(지오 필터) 또는 유사 문서 검색과 조합된 경우에도 스킵됩니다.
- 깊은 페이지에서는 Rank Fusion 자체가 비활성화되어 키워드 검색만의 결과가 됩니다. 경계는
  ``rank.fusion.window_size``\ (기본값 ``200``)로 결정되며, 기본 설정에서는 검색 결과의 101번째
  이후가 여기에 해당합니다.
- 임베딩 프로바이더에 연결할 수 없거나 검색 오류가 발생한 경우, |Fess|\ 는 자동으로 키워드
  검색만의 결과로 폴백합니다(그 결과로 검색 자체가 실패하는 일은 없습니다).
- 역할 및 가상 호스트 기반 접근 제어는 시맨틱 검색 결과에도 적용됩니다.

AI 검색 모드와의 연계
========================

AI 검색 모드(:doc:`rag-chat`, ``rag.chat.enabled=true``)가 활성화되어 있는 경우,
``content_chunk_status`` 가 ``done`` 인 문서에 대해 답변을 생성할 때 각 청크와의 유사도를
계산하고, 가장 관련성이 높은 상위 ``content_chunker.chat.top_k`` 개(기본값: ``3``)의 청크만
LLM의 컨텍스트로 사용합니다.

이때 임베딩의 대상이 되는 것은 사용자의 발화 그 자체가 아니라 **의도 판정 단계에서 LLM이 생성한
검색 쿼리**\ 입니다(재검색이 발생한 경우에는 재생성된 쿼리가 됩니다). 문서 요약을 요청한 경우처럼
검색 쿼리가 생성되지 않는 경우에는 청크 선택이 이루어지지 않습니다.

그 결과 긴 문서라도 관련된 부분만 LLM에 전달되어 답변 정확도 향상과 토큰 사용량 절감을 기대할 수
있습니다. ``content_chunk_status`` 가 ``chunked``\ (청크는 있지만 벡터가 없는 상태)인 문서에서는
유사도 계산 대신 키워드(하이라이트) 일치에 의한 청크 선택이 이루어집니다. ``skipped`` /
``fail`` 및 미처리 문서는 이전과 마찬가지로 전체 본문(또는 하이라이트된 발췌)을 사용합니다.

이 동작은 ``content_chunker.search.enabled`` 와 무관하지만, ``content_chunker.enabled`` 가
활성화되어 있어야 합니다. 또한 선택된 청크를 연결한 텍스트도
``rag.chat.content.fulltext.max.length``\ (기본값 ``3000``)로 잘리므로,
``content_chunker.chat.top_k`` 나 ``content_chunker.length.chunk_size`` 를 크게 설정하더라도
LLM에 전달되는 문자 수는 이 상한을 넘지 않습니다.

.. _semantic-search-migration:

15.7 이전 버전에서 업그레이드하는 경우의 마이그레이션
========================================================

15.7 이전 버전에서 |Fess|\ 를 업그레이드하는 경우, 현재 이 기능들을 어떻게 사용하고 있는지에 따라
아래 네 가지 패턴 중 하나에 해당합니다. 해당하는 패턴의 안내를 따르세요.

신규 설치의 경우
------------------

추가 작업은 필요하지 않습니다. 벡터 검색을 사용하고 싶다면 |Fess|\ 를 처음 시작하기 전에 이
페이지의 *설정 레퍼런스* 섹션에 따라 ``system.properties`` 를 설정해 두기만 하면, 인덱스가 처음
생성될 때 올바른 매핑이 자동으로 적용됩니다.(구체적인 절차는 위의 *설정 절차* 를 참조하세요.)

.. note::

   이전에 |Fess|\ 를 한 번이라도 시작한 적이 있다면(즉 인덱스가 이미 존재한다면), 이 패턴이
   아니라 아래의 *기존 사용자* 패턴 중 하나를 따르세요.

기존 사용자로, 벡터 검색을 이용하지 않는 경우
------------------------------------------------

아무런 작업도 필요하지 않습니다. ``content_chunker.enabled`` 와 ``content_chunker.search.enabled``
는 모두 기본값이 ``false`` 이므로, 업그레이드 후에도 검색 결과와 기존 인덱스의 동작은 변하지
않습니다. 새로 추가된 스케줄러 작업 **Content Chunk Vector Indexer**\ 는 시작 시 자동으로
등록되지만, 기본적으로 비활성화되어 있으므로 실행되지 않으며 시맨틱 서처도 Rank Fusion에
등록되지 않습니다(이 작업은 시작할 때마다 등록되므로, 관리 화면에서 삭제해도 다음 시작 시
비활성화 상태로 다시 생성됩니다).

.. note::

   벡터 검색을 사용하지 않더라도 |Fess| 15.8 이후에서 인덱스를 **신규 생성**\ (재인덱싱 포함)하면
   ``content_chunk_vector``\ (``knn_vector`` 타입)를 포함하는 매핑과 ``index.knn: true`` 가
   적용됩니다. OpenSearch에 k-NN 플러그인이 설치되어 있지 않은 구성에서는 그 시점에 인덱스
   생성이 실패합니다. 자세한 내용은 이 페이지의 *전제 조건* 을 참조하세요.

기존 사용자로, 벡터 검색을 이용하려는 경우
----------------------------------------------

실행 중인 인덱스에는 새 매핑이 자동으로 반영되지 않으므로, 다음 단계가 필요합니다.

1. 이 페이지의 *설정 레퍼런스* 에 설명된 대로 ``system.properties`` 에 설정을 적용합니다
   (opensearch 프로바이더를 사용하는 경우의 구체적인 절차는 위의 *설정 절차* 를 참조하세요).
2. |Fess|\ 를 재시작합니다.
3. 관리 화면에서 「시스템 정보」→「유지보수」의 「재인덱싱」을, 「에일리어스 갱신」을 활성화한
   상태로 실행합니다. 이 작업은 백그라운드에서 비동기로 진행되며 완료 알림은 표시되지
   않습니다. ``_cat/indices`` 는 새 인덱스의 존재만 보여줄 뿐 에일리어스가 전환되었는지는
   보여주지 않으므로, 다음 단계로 넘어가기 전에 ``_cat/aliases`` 로 ``fess.search``/
   ``fess.update`` 가 새 인덱스를 가리키는지 확인하세요(|Fess|\ 의 로그는 실패 시에만
   경고를 남기므로 조용하다고 해서 성공을 의미하지는 않습니다). 이전 인덱스는 자동으로
   삭제되지 않으므로 필요 없어지면 수동으로 삭제하세요(두 인덱스가 모두 존재하는 동안
   디스크 사용량은 평소의 약 2배가 됩니다).
4. 위의 에일리어스 전환이 완료되었음을 확인한 후에, 「시스템」→「스케줄러」에서 Content Chunk
   Vector Indexer 작업을 활성화하고 실행합니다(재크롤링은 필요하지 않습니다. 이 작업은 기존
   인덱스의 ``_source`` 에서 ``content`` 를 읽어 청크로 나누고 임베딩합니다).

.. note::

   1단계에서 ``content_chunker.search.enabled=true`` 까지 함께 적용하면, 2단계의 재시작부터
   4단계가 완료될 때까지 검색할 때마다 쿼리의 임베딩만 실행되고 그 결과는 반영되지 않는 상태가
   됩니다. ``openai`` 나 ``gemini`` 처럼 종량제 프로바이더를 사용하는 경우에는
   ``content_chunker.search.enabled=true`` 의 적용과 재시작을 4단계 완료 후에 수행하세요.

fess-webapp-semantic-search 플러그인을 사용하고 있었던 경우
----------------------------------------------------------------

|Fess| 15.7 이전에서 시맨틱 검색을 제공하던 ``fess-webapp-semantic-search`` 플러그인은 15.8에서
코어로 통합되어 이제 **불필요(사용 중단)**\ 합니다. 위의 *기존 사용자로, 벡터 검색을 이용하려는
경우* 의 단계에 더해 다음 작업도 필요합니다.

1. **플러그인 제거**: ``app/WEB-INF/plugin/`` 에서 ``fess-webapp-semantic-search-*.jar`` 를
   삭제합니다(Docker에서는 ``FESS_PLUGINS`` 에서 제외합니다).

2. **기존 설정 제거**: ``-Dfess.semantic_search.*`` 시작 옵션을 모두 삭제합니다. 또한 기존
   플러그인용으로 ``-Drank.fusion.searchers=default,semantic`` 을 지정했다면 이것도
   제거합니다. 그대로 두면 새 시맨틱 서처(``semantic_chunk``)가 Rank Fusion에서 제외되고 시작
   시 경고 로그가 남습니다.

3. **기존 인제스트 파이프라인 분리**: 기존 플러그인은 ``-Dfess.semantic_search.pipeline`` 을
   설정했던 경우에 한해, 인덱스를 생성할 때 ``default_pipeline``\ (뉴럴 검색용 인제스트
   파이프라인)을 인덱스 설정에 심어 넣습니다. **플러그인을 제거해도 파이프라인은 인덱스에 그대로
   남아 계속 동작하므로**, 위의 *기존 사용자로, 벡터 검색을 이용하려는 경우* 에 있는 재인덱싱을
   수행하기 **전에** 분리하세요. 재인덱싱 후의 새 인덱스에는 이 설정이 붙지 않으므로, 나중에
   실행해도 의미가 없습니다. ``_cat/aliases`` 로 ``fess.search`` 가 가리키는
   ``fess.<timestamp>`` 를 확인하고, 에일리어스가 아니라 실체 인덱스 이름을 지정합니다::

       curl -XPUT "http://localhost:9200/fess.<timestamp>/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": "_none"}}'

   인덱스 설정을 해제해도 인제스트 파이프라인 자체는 검색 엔진에 남아 있습니다. 앞으로 사용하지
   않을 경우에는 삭제하세요::

       curl -XDELETE "http://localhost:9200/_ingest/pipeline/<파이프라인명>"

4. **새 설정 추가**: 이 페이지의 *설정 레퍼런스* 에 설명된 대로 ``system.properties`` 에
   ``content_chunker.*`` 를 설정합니다. 기존 ML Commons 모델을 계속 사용하려면
   ``content_chunker.embedding.name=opensearch`` 로 설정하고, 기존 ``model_id`` 를
   ``content_chunker.embedding.opensearch.model.id`` 에 지정합니다.

5. **인덱스 재작성 및 작업 실행**: 기존 플러그인이 저장하던 벡터 필드(기본 구성에서는
   ``content_vector``)와 새 코어 기능이 사용하는 ``content_chunk_vector`` 필드는 별개의 필드이므로,
   기존 벡터를 새 기능에서 사용할 수는 없습니다. 한편 재인덱싱은 ``_source`` 를 그대로
   복사하므로, 기존 벡터는 새 인덱스에도 복제되어 동적 매핑으로 디스크를 계속 소비합니다.
   재인덱싱 **전에** 제거해 둘 것을 권장합니다(필드 이름을 변경했다면 그에 맞게 바꿔 읽으세요)::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_vector"}},
         "script": {"source": "ctx._source.remove(\"content_vector\")"}
       }'

   그 후 「시스템 정보」→「유지보수」에서 「재인덱싱」을 실행한 뒤, Content Chunk Vector Indexer
   작업을 활성화·실행하여 벡터를 다시 생성하세요.

주의 사항
==========

임베딩 모델(차원) 변경
------------------------

차원이 다른 임베딩 모델로 전환하려면 다음 순서로 진행합니다.

1. 기존의 오래된 벡터를 삭제합니다. 차원 수가 다른 오래된 벡터가 남아 있는 상태로 재인덱싱하면,
   새 매핑이 그 벡터들을 받아들이지 못해 해당 문서가 새 인덱스로 복사되지 않은 채 처리가
   진행됩니다. |Fess|\ 는 재인덱싱의 HTTP 상태 코드만 확인하므로, 관리 화면에는 오류가 표시되지
   않은 채 문서가 누락됩니다::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

   .. note::

      대상으로 ``fess.update``\ (재인덱싱의 읽기 원본이 되는 갱신용 에일리어스)를 지정해도
      됩니다. 또한 이 작업으로는 ``content`` 필드가 청크의 배열 그대로 남습니다. 다음 작업 실행
      시에 다시 연결한 뒤 재분할되므로, ``content_chunker.length.overlap`` 에 0 이외의 값을
      설정한 경우에는 중복 부분이 이중으로 포함된 상태로 재분할됩니다. 이것이 문제가 된다면
      해당 문서를 다시 크롤링하세요.

2. ``content_chunker.embedding.dimension`` 과 사용 중인 프로바이더의 모델 설정을 변경합니다.
3. 위의 *설정 절차* 에 있는 *3. 인덱스 재작성(기존 환경에서 활성화하는 경우)* 에 따라 인덱스를
   재작성하고 인덱서 작업을 다시 실행합니다.

디스크 사용량
--------------

청크 벡터는 검색 인덱스 구조 외에도 ``_source`` 에 보관되므로, 각 문서는 청크 수 × 벡터 차원
수에 비례하는 추가 디스크 용량을 소비합니다. 디스크 용량이 문제가 되면
``content_chunker.length.chunk_size`` 나 ``content_chunker.max_chunks_per_document`` 를
조정하세요.

chunk-only 모드
-----------------

``content_chunker.embedding.name=none`` 을 설정하면 임베딩 벡터를 생성하지 않고 청크 분할만
수행합니다(``content_chunk_status`` 는 ``chunked`` 가 됩니다). 이를 이용하면 임베딩
프로바이더가 준비되기 전에 청크 분할을 미리 실행해 둘 수 있으며, 이후 프로바이더를 설정하고
작업을 다시 실행하면 이미 저장된 청크에 대해 벡터만 생성됩니다(다시 청크로 나누지는 않습니다).

대규모 코퍼스에서의 메모리 설정
----------------------------------

인덱서 작업의 자식 JVM은 ``fess_config.properties`` 의 ``jvm.chunk.options``\ (기본값은
``-Xms128m -Xmx1g`` 를 포함하는 JVM 옵션)로 시작됩니다.
``content_chunker.job.max_documents_per_run`` 의 기본값이 무제한이므로, 한 번의 실행에서 대기
중인 모든 문서 ID를 메모리에 보관합니다. 문서 ID는 SHA-512 다이제스트(128자)이며, 한 건당 대략
200바이트를 힙에 보관합니다. 청크 처리 자체에도 200~250MB 정도를 사용하므로, **100만~200만 건을
넘는 코퍼스**\ 에서는 ``jvm.chunk.options`` 의 ``-Xmx`` 값을 높이거나
``content_chunker.job.max_documents_per_run`` 에 유한한 값을 설정하여 분할 실행하세요.
``jvm.chunk.options`` 는 ``app/WEB-INF/classes/fess_config.properties``\ (RPM/DEB 패키지는
``/etc/fess/fess_config.properties``)에서 재정의합니다(JVM 옵션의 개념은 :doc:`setup-memory` 를
참조하세요).

동일한 무제한 기본값은 ``openai``, ``gemini`` 와 같은 종량제 임베딩 프로바이더를 사용할 때
비용 측면에도 영향을 줍니다. 첫 인덱서 실행에서 기존 코퍼스 전체가 한 번에 임베딩되어
그만큼의 비용이 한꺼번에 청구됩니다. 비용을 여러 번의 실행에 분산시키려면
``content_chunker.job.max_documents_per_run`` 에 유한한 값을 설정하세요.

참고 정보
==========

- :doc:`rank-fusion` - Rank Fusion(하이브리드 검색) 설정
- :doc:`rag-chat` - AI 검색 모드 설정
- :doc:`llm-overview` - LLM 통합 개요
- :doc:`llm-ollama` - Ollama 설정
- :doc:`setup-memory` - JVM 메모리 설정
- :doc:`../install/upgrade` - 업그레이드 절차
