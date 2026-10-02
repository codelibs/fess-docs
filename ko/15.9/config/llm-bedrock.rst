===================================
Amazon Bedrock 설정 (AI 검색 / RAG)
===================================

개요
====

이 페이지에서는 |Fess| 가 Amazon Bedrock을 **AI 검색 모드(RAG: Retrieval-Augmented Generation)** 및 콘텐츠 청크의 임베딩 프로바이더로 사용할 수 있도록 ``fess-llm-bedrock`` 플러그인을 설정하는 방법을 설명합니다.

Amazon Bedrock은 Amazon을 비롯한 여러 모델 프로바이더의 파운데이션 모델을 하나의 API로 제공하는 AWS 서비스입니다.
플러그인은 지정한 AWS 리전의 Bedrock Runtime API를 호출합니다.

- **AI 검색 모드**: Converse API(스트리밍 응답에는 ``ConverseStream`` )
- **콘텐츠 청크 임베딩**: InvokeModel API(Amazon Titan Text Embeddings V2 또는 Cohere Embed)

지원 모델
---------

AI 검색 모드는 사용하는 리전에서 Converse API를 지원하는 모델이라면 모두 사용할 수 있습니다.
기본값은 미국 교차 리전 추론 프로파일을 통한 Amazon Nova 2 Lite( ``us.amazon.nova-2-lite-v1:0`` )입니다.
``rag.llm.bedrock.model`` 에는 모델 ID, 추론 프로파일 ID(예: ``us.``, ``eu.``, ``global.`` 접두사가 붙은 것) 또는 ARN을 지정할 수 있습니다.

콘텐츠 청크 임베딩은 다음 모델을 지원합니다.

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - 모델
     - ``content_chunker.embedding.dimension``
     - 요청당 텍스트 수
   * - ``amazon.titan-embed-text-v2:0``
     - ``256``, ``512`` 또는 ``1024``
     - 1
   * - ``cohere.embed-english-v3`` / ``cohere.embed-multilingual-v3``
     - ``1024``
     - 최대 96(각 텍스트는 2048자 이내)
   * - ``cohere.embed-v4:0`` (추론 프로파일을 통한 사용도 가능)
     - ``256``, ``512``, ``1024`` 또는 ``1536``
     - 최대 96

임베딩 모델은 설정된 ID에 포함된 기반 모델 이름으로 판별됩니다. 기반 모델 ID, 교차 리전 추론 프로파일 ID( ``us.``, ``eu.``, ``global.`` 등) 또는 이들을 포함하는 ARN을 사용할 수 있습니다.
애플리케이션 추론 프로파일의 ID는 의미를 알 수 없는 문자열이므로 판별되지 않습니다.

.. note::
   각 리전에서 사용 가능한 모델은 `Supported foundation models in Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html>`__ 를 참조하세요.

전제조건
========

1. **AWS 계정**: 사용하는 리전에서 Amazon Bedrock을 사용할 수 있어야 합니다
2. **모델 액세스**: 설정하는 모델을 해당 리전에서 계정으로 사용할 수 있어야 합니다
3. **인증 정보**: Bedrock API 키, 또는 모델 호출이 허용된 AWS 인증 정보( :ref:`bedrock-authentication` 참조)

플러그인 설치
=============

Bedrock 연계 기능은 ``fess-llm-bedrock`` 플러그인으로 제공됩니다.
관리 화면의 「시스템」>「플러그인」에서 설치하거나, JAR 파일을 수동으로 배치한 후 |Fess| 를 재시작합니다.

::

    cp fess-llm-bedrock-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   플러그인 버전은 |Fess| 버전과 맞춰주세요.

기본 설정
=========

LLM 프로바이더 선택( ``rag.llm.name`` )은 관리 화면(관리 화면 > 시스템 > 전반) 또는 ``system.properties`` 에서 수행합니다.
AI 검색 모드 활성화와 ``rag.llm.bedrock.*`` 설정은 ``fess_config.properties`` 에 기술합니다.

``system.properties`` (관리 화면 > 시스템 > 전반 에서도 설정 가능):

::

    rag.llm.name=bedrock

``app/WEB-INF/classes/fess_config.properties`` (패키지 설치에서는 ``/etc/fess/fess_config.properties`` ), AWS 인증 정보를 사용하는 경우:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.model=us.amazon.nova-2-lite-v1:0

AWS 인증 정보 대신 Bedrock API 키를 사용하는 경우:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.api.key=your-bedrock-api-key

설정 항목
=========

AI 검색 모드 클라이언트에서 사용 가능한 모든 설정 항목입니다. ``fess_config.properties`` (또는 ``-Dfess.config.<key>`` JVM 옵션)에 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.bedrock.api.key``
     - Bedrock API 키. 비어 있으면 AWS 인증 정보(SigV4)로 요청에 서명합니다
     - ``""``
   * - ``rag.llm.bedrock.region``
     - Bedrock Runtime 엔드포인트 및 SigV4 서명의 AWS 리전
     - ``us-east-1``
   * - ``rag.llm.bedrock.endpoint``
     - 엔드포인트 URL(예: VPC 인터페이스 엔드포인트). 비어 있으면 ``https://bedrock-runtime.<region>.amazonaws.com``
     - ``""``
   * - ``rag.llm.bedrock.model``
     - 모델 ID, 추론 프로파일 ID 또는 ARN
     - ``us.amazon.nova-2-lite-v1:0``
   * - ``rag.llm.bedrock.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``120000``
   * - ``rag.llm.bedrock.availability.check.interval``
     - 가용성 체크 간격(초)
     - ``60``
   * - ``rag.llm.bedrock.temperature.enabled``
     - ``false`` 로 설정하면 ``temperature`` 를 전송하지 않습니다(이를 거부하는 모델 또는 모드용)
     - ``true``
   * - ``rag.llm.bedrock.additional.model.request.fields``
     - 모델 고유 파라미터를 위해 ``additionalModelRequestFields`` 로 전송하는 JSON 객체
     - ``""``
   * - ``rag.llm.bedrock.max.concurrent.requests``
     - 최대 동시 요청 수
     - ``5``
   * - ``rag.llm.bedrock.concurrency.wait.timeout``
     - 동시 요청 대기 타임아웃(밀리초)
     - ``30000``
   * - ``rag.llm.bedrock.answer.context.max.chars``
     - 응답 생성 시 검색된 컨텍스트의 최대 문자 수
     - ``16000``
   * - ``rag.llm.bedrock.summary.context.max.chars``
     - 요약 생성 시 문서의 최대 문자 수
     - ``16000``
   * - ``rag.llm.bedrock.faq.context.max.chars``
     - FAQ 생성 시 검색된 컨텍스트의 최대 문자 수
     - ``10000``
   * - ``rag.llm.bedrock.chat.evaluation.max.relevant.docs``
     - 평가 시 최대 관련 문서 수
     - ``3``
   * - ``rag.llm.bedrock.chat.evaluation.description.max.chars``
     - 평가 시 문서 설명 최대 문자 수
     - ``500``
   * - ``rag.llm.bedrock.history.max.chars``
     - 채팅 이력의 최대 문자 수
     - ``8000``
   * - ``rag.llm.bedrock.intent.history.max.messages``
     - 의도 판정 시 이력 최대 메시지 수
     - ``8``
   * - ``rag.llm.bedrock.intent.history.max.chars``
     - 의도 판정 시 이력 최대 문자 수
     - ``4000``
   * - ``rag.llm.bedrock.history.assistant.max.chars``
     - 어시스턴트 이력의 최대 문자 수
     - ``800``
   * - ``rag.llm.bedrock.history.assistant.summary.max.chars``
     - 어시스턴트 요약 이력의 최대 문자 수
     - ``800``
   * - ``rag.llm.bedrock.retry.max``
     - HTTP 최대 시도 횟수( ``429``, ``500``, ``502``, ``503``, ``504`` 시)
     - ``10``
   * - ``rag.llm.bedrock.retry.base.delay.ms``
     - 지수 백오프의 기준 지연 시간(밀리초)
     - ``2000``

.. _bedrock-authentication:

인증 방식
=========

API 키
------

``rag.llm.bedrock.api.key`` 가 설정되어 있으면 ``Authorization: Bearer <key>`` 로 전송됩니다.
단기 Bedrock API 키는 만료되며 생성된 리전에서만 유효합니다. 장기 키는 IAM 사용자에 연결됩니다.
이 값이 ``fess_config.properties`` 에 설정된 경우( ``content_chunker.embedding.bedrock.api.key`` 는 ``system.properties`` 에 설정된 경우) 관리 화면 > 시스템 정보에서 마스킹됩니다.
환경 변수와 JVM 시스템 프로퍼티( ``-Dfess.config.*`` 및 ``-Dfess.system.*`` 옵션 포함)는 마스킹되지 않은 채 표시되므로, 키를 이 방법으로 전달하지 마세요.

AWS 인증 정보(SigV4)
--------------------

API 키가 설정되어 있지 않으면 모든 요청이 AWS Signature Version 4로 서명됩니다.
인증 정보는 다음 소스 중 처음으로 제공되는 것을 사용합니다.

1. ``aws.accessKeyId`` / ``aws.secretAccessKey`` / ``aws.sessionToken`` JVM 시스템 프로퍼티
2. ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` / ``AWS_SESSION_TOKEN`` 환경 변수
3. 웹 ID( ``AWS_WEB_IDENTITY_TOKEN_FILE`` 및 ``AWS_ROLE_ARN``, Amazon EKS에서 사용)
4. 공유 ``~/.aws/credentials`` 및 ``~/.aws/config`` 파일( ``AWS_PROFILE`` 로 프로파일 선택)
5. 컨테이너 인증 정보 엔드포인트(Amazon ECS)
6. EC2 인스턴스 메타데이터 서비스(인스턴스 프로파일)

JVM 시스템 프로퍼티(1번)는 |Fess| 웹 프로세스에만 전달됩니다.
콘텐츠 청크(문서) 임베딩은 별도의 자식 JVM에서 실행되므로, 이 경우에는 환경 변수, 공유 인증 정보 프로파일 또는 IAM 역할을 사용하거나 ``jvm.chunk.options`` 에도 ``-Daws.*`` 옵션을 지정하세요.

리전은 항상 ``rag.llm.bedrock.region`` 에서 가져오며, ``AWS_REGION`` 은 읽지 않습니다.
IAM Identity Center(SSO)를 사용하는 프로파일은 지원되지 않습니다.

.. warning::
   IAM 역할(EC2 인스턴스 프로파일, ECS 태스크 역할, EKS 웹 ID) 또는 |Fess| 를 실행하는 사용자의 공유 인증 정보 파일을 사용하는 것을 권장합니다.
   환경 변수와 JVM 시스템 프로퍼티는 관리 화면 > 시스템 정보에 마스킹 없이 표시되므로, 장기 키는 여기에 두지 마세요.

IAM 주체에는 사용하는 모델에 대한 ``bedrock:InvokeModel`` (Converse 및 InvokeModel)과 ``bedrock:InvokeModelWithResponseStream`` (ConverseStream) 권한이 필요합니다.
모델이 추론 프로파일인 경우 추론 프로파일과 그것이 라우팅하는 파운데이션 모델을 모두 허용하세요.

재시도 동작
===========

``429``, ``500``, ``502``, ``503``, ``504`` 가 반환된 경우와 Bedrock에 대한 연결을 수립하지 못한 경우 요청이 재시도됩니다.
재시도 시에는 지수 백오프(기준값 ``rag.llm.bedrock.retry.base.delay.ms``, ±20%의 지터 포함, 최대 ``rag.llm.bedrock.retry.max`` 회)로 대기하며, ``Retry-After`` 헤더가 있으면 그것이 우선합니다.
스트리밍 요청에서는 초기 요청만 재시도 대상이며, 응답 스트리밍이 시작된 이후의 오류(스트림 내부의 예외 이벤트 포함)는 요청을 종료시킵니다.

프롬프트 타입별 설정
====================

``temperature`` 와 ``max.tokens`` 는 다른 프로바이더와 마찬가지로 프롬프트 타입별로 설정할 수 있습니다.

::

    rag.llm.bedrock.{promptType}.temperature
    rag.llm.bedrock.{promptType}.max.tokens
    rag.llm.bedrock.{promptType}.context.max.chars
    rag.llm.bedrock.{promptType}.additional.model.request.fields

``{promptType}`` 은 ``intent``, ``evaluation``, ``unclear``, ``noresults``, ``docnotfound``, ``direct``, ``faq``, ``answer``, ``summary``, ``queryregeneration`` 중 하나입니다.
프롬프트 타입별 ``additional.model.request.fields`` 는 해당 프롬프트 타입에 대해 전역 값을 대체합니다.

아무것도 설정하지 않았을 때 사용되는 기본값은 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - 프롬프트 타입
     - temperature
     - max.tokens
   * - ``intent``, ``evaluation``
     - ``0.1``
     - ``256``
   * - ``unclear``, ``noresults``
     - ``0.7``
     - ``512``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
   * - ``direct``, ``faq``
     - ``0.7``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``

.. note::
   ``rag.llm.bedrock.{promptType}.thinking.budget`` 은 지원되지 않습니다. Bedrock에서는 추론 설정이 모델마다 다르기 때문입니다.
   설정된 값은 전송되지 않으며 WARN이 기록됩니다. 대신 ``additional.model.request.fields`` 를 사용하세요.

모델 고유 파라미터
==================

``additional.model.request.fields`` 는 JSON 객체를 그대로 모델에 전달합니다.
JSON 객체가 아닌 값은 전송되지 않으며, 해당 프로퍼티 이름을 포함한 WARN이 기록됩니다.

예를 들어 Anthropic Claude 모델의 확장 사고(extended thinking)를 응답 생성에만 사용하려면 다음과 같이 설정합니다.

::

    rag.llm.bedrock.model=<a Claude model ID or inference profile ID>
    rag.llm.bedrock.temperature.enabled=false
    rag.llm.bedrock.answer.additional.model.request.fields={"thinking":{"type":"enabled","budget_tokens":2048}}
    rag.llm.bedrock.answer.max.tokens=6144

Claude는 사고가 활성화된 동안 ``temperature`` 를 거부하며, ``max.tokens`` 는 ``budget_tokens`` 보다 커야 합니다.
추론 텍스트는 사용자에게 표시되지 않으며, 응답 텍스트만 표시됩니다.

콘텐츠 청크 임베딩
==================

Bedrock을 콘텐츠 청크 임베딩에 사용하려면 ``app/WEB-INF/conf/system.properties`` (RPM/DEB 패키지는 ``/etc/fess/system.properties``, Docker 버전은 ``/opt/fess/system.properties`` ) 또는 ``-Dfess.system.<key>`` 옵션으로 다음을 설정합니다.
``rag.llm.bedrock.*`` 와 달리 이 키들은 ``fess_config.properties`` 에서 읽히지 않습니다.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=bedrock
    content_chunker.embedding.dimension=1024
    content_chunker.embedding.bedrock.region=us-east-1
    content_chunker.embedding.bedrock.model=amazon.titan-embed-text-v2:0

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``content_chunker.embedding.bedrock.api.key``
     - Bedrock API 키. 비어 있으면 AWS 인증 정보를 사용합니다
     - ``""``
   * - ``content_chunker.embedding.bedrock.region``
     - AWS 리전
     - ``us-east-1``
   * - ``content_chunker.embedding.bedrock.endpoint``
     - 엔드포인트 URL. 비어 있으면 리전에서 도출됩니다
     - ``""``
   * - ``content_chunker.embedding.bedrock.model``
     - 임베딩 모델( `지원 모델`_ 참조)
     - ``amazon.titan-embed-text-v2:0``
   * - ``content_chunker.embedding.bedrock.normalize``
     - Titan 전용: 벡터를 정규화할지 여부
     - ``true``
   * - ``content_chunker.embedding.bedrock.truncate``
     - Cohere 전용: ``truncate`` (v3는 ``NONE``/``START``/``END``, v4는 ``NONE``/``LEFT``/``RIGHT`` ). 비어 있으면 전송되지 않습니다
     - ``""``
   * - ``content_chunker.embedding.bedrock.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``120000``
   * - ``content_chunker.embedding.bedrock.connect.timeout``
     - 연결 타임아웃 시간(밀리초)
     - ``5000``
   * - ``content_chunker.embedding.bedrock.availability.check.interval``
     - 가용성 체크 간격(초)
     - ``60``
   * - ``content_chunker.embedding.bedrock.retry.max``
     - HTTP 최대 시도 횟수( ``429``, ``500``, ``502``, ``503``, ``504`` 시)
     - ``10``
   * - ``content_chunker.embedding.bedrock.retry.base.delay.ms``
     - 지수 백오프의 기준 지연 시간(밀리초)
     - ``2000``
   * - ``content_chunker.embedding.bedrock.retry.max.delay.ms``
     - 한 번의 백오프 대기 시간의 상한( ``Retry-After`` 포함, 밀리초)
     - ``60000``

``content_chunker.embedding.dimension`` 은 모델이 생성하는 크기여야 합니다( `지원 모델`_ 참조). 그렇지 않으면 임베딩 프로바이더는 사용할 수 없는 것으로 보고되고 ERROR가 기록됩니다.
문서는 Cohere의 ``input_type=search_document`` 로, 쿼리는 ``search_query`` 로 임베딩됩니다.
Cohere Embed v3는 텍스트당 최대 2048자까지 받습니다. 이보다 긴 텍스트는 ``truncate`` 설정과 관계없이 Bedrock이 ``400 ValidationException`` 으로 거부하며, 플러그인은 텍스트를 줄이거나 분할하지 않습니다.
``truncate`` (설정하지 않으면 ``END`` )는 2048자 이내이면서 512 토큰을 초과하는 텍스트에만 적용됩니다.

HTTP 프록시 경유 사용
=====================

Bedrock으로의 요청은 |Fess| 전체의 HTTP 프록시 설정( ``fess_config.properties`` 의 ``http.proxy.host``, ``http.proxy.port``, ``http.proxy.username``, ``http.proxy.password`` )을 사용합니다.
AWS 엔드포인트를 호출하는 인증 정보 조회(웹 ID용 STS, 컨테이너 인증 정보 엔드포인트, 인스턴스 메타데이터 서비스)는 이 설정을 사용하지 않습니다.
VPC 인터페이스 엔드포인트를 통해 Bedrock에 접속하려면 ``rag.llm.bedrock.endpoint`` (및 ``content_chunker.embedding.bedrock.endpoint`` )에 해당 URL을 설정하세요. 서명 리전은 계속 리전 설정으로 선택됩니다.

문제 해결
=========

AI 검색 모드를 사용할 수 없음
-----------------------------

클라이언트는 모델과 리전이 설정되어 있고, 엔드포인트가 올바른 URL이며, API 키가 설정되어 있거나 AWS 인증 정보를 확인할 수 있을 때 자신이 사용 가능하다고 보고합니다.
올바르지 않은 리전 또는 엔드포인트는 ERROR로 기록됩니다. 인증 정보를 확인하지 못한 이유를 보려면 ``org.codelibs.fess.llm.bedrock`` 의 DEBUG를 활성화하세요.
인증 정보 조회 실패는 60초 동안 기억되므로, 나중에 사용 가능해진 인증 정보는 1분 이내에 반영됩니다.

액세스 거부
-----------

WARN 로그에 ``type=AccessDeniedException`` 이 포함된 ``403`` 은 API 키 또는 IAM 주체에 모델 호출이 허용되지 않았음을 의미합니다.
위의 IAM 권한과, 설정된 리전에서 계정으로 모델을 사용할 수 있는지 확인하세요.

검증 오류
---------

``type=ValidationException`` 이 포함된 ``400`` 은 대개 해당 모델 ID를 리전에서 사용할 수 없거나(일부 모델은 추론 프로파일 ID만 사용 가능), ``additional.model.request.fields`` 에 모델이 받아들이지 않는 파라미터가 포함되어 있음을 의미합니다.

디버그 설정
-----------

``org.codelibs.fess.llm.bedrock`` 의 DEBUG를 활성화하면 AI 검색 모드의 요청 및 응답 본문과 AWS 인증 정보를 확인하지 못한 이유가 기록됩니다.
``org.codelibs.fess.embedding.bedrock`` 의 DEBUG는 쿼리 텍스트가 어떻게 정규화되었는지와 동일한 인증 정보 관련 이유를 기록하며, 임베딩 요청은 기록하지 않습니다.
이 로거들은 API 키, AWS 인증 정보, 서명을 절대 기록하지 않습니다.

.. warning::
   다른 두 로거는 DEBUG에서 인증 정보를 기록합니다. Apache HttpClient의 와이어 로깅은 ``Authorization`` 헤더를 기록하고, AWS SDK의 서명기( ``software.amazon.awssdk.http.auth.aws.internal.signer`` )는 임시 인증 정보의 ``x-amz-security-token`` 을 포함한 정규 요청(canonical request)을 기록합니다.
   루트 로그 레벨을 DEBUG로 하여 |Fess| 를 시작하면 둘 다 활성화되므로, ``org.apache.hc`` 와 ``software.amazon.awssdk`` 는 INFO 이상으로 유지하세요.

참고 정보
=========

- :doc:`llm-overview` - LLM 통합 개요
- :doc:`rag-chat` - AI 검색 모드 기능 상세
- :doc:`search-semantic` - 시맨틱 검색과 콘텐츠 청크 임베딩
- `Amazon Bedrock User Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>`__
