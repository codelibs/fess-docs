===========================================
AI 검색 모드(RAG)로 사내 문서에 답하게 하기
===========================================

들어가며
========

검색 결과를 하나씩 열어 비교해 읽는 대신, "경비 정산 마감일은 언제인가요?"라고 질문하고 사내 문서에 근거한 답을 받고 싶다는 요구는 흔합니다.
Fess의 AI 검색 모드(RAG 채팅)는 질문과 관련된 문서를 Fess 스스로 검색하고, 그 내용을 LLM(대규모 언어 모델)에 넘겨 답변을 만들게 한 뒤, 근거로 삼은 문서의 링크를 붙여 돌려줍니다.

이 글에서는 Fess 15.9에서 AI 검색 모드를 동작시키고, 사용할 수 있는 사람과 참조하는 문서를 좁히고, 화면과 API로 동작을 확인하는 데까지를 다룹니다.
이 글의 절차를 마치면 다음을 할 수 있게 됩니다.

- 4종류의 LLM 제공자 중 하나를 골라, 대응하는 플러그인과 설정을 넣는다
- Docker로 실행하는 Fess에, docker-fess가 제공하는 오버레이용 Compose 파일로 LLM을 연결한다
- 채팅을 사용할 수 있는 사용자와, 답변의 근거로 삼을 문서의 범위를 좁힌다
- 검색 화면, ``/api/v2/chat``\ , 검색 로그에서 동작하는지 확인한다

전제로서 Fess가 실행 중이고 문서가 크롤링되어 있어야 합니다.
아직이라면 :doc:`guide-02`\ 의 절차로 준비하십시오.
의미가 가까운 문서를 찾는 시맨틱 검색은 :doc:`guide-18`\ , AI 에이전트가 Fess를 검색하게 하는 MCP는 :doc:`guide-20`\ 에서 다룹니다.

AI 검색 모드의 구조
===================

AI 검색 모드는 전용 벡터 인덱스를 사용하지 않습니다.
평소의 검색과 같은 검색 처리(기본값은 키워드 검색)로 문서를 찾으므로, 임베딩 모델이나 청크 분할을 준비하지 않고 시작할 수 있습니다.
시맨틱 검색을 활성화한 경우에는 AI 검색 모드의 검색에도 자동으로 포함됩니다.

처리 흐름은 호출하는 엔드포인트에 따라 다릅니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 엔드포인트
     - 처리 흐름
   * - ``POST /api/v2/chat/stream``\ (검색 화면의 AI 검색이 사용)
     - 의도 판정 → 검색 → LLM에 의한 관련도 평가 → 본문 가져오기 → 답변 생성. 각 단계의 진행 상황과 답변 조각을 Server-Sent Events로 차례로 돌려줍니다
   * - ``POST /api/v2/chat``
     - 의도 판정 → 검색 → 답변 생성. 관련도 평가는 없으며, 결과는 하나의 JSON으로 돌아옵니다

두 경우 모두, 검색 결과가 0건이면 LLM이 검색어를 다시 만들어 재검색합니다(기본값 최대 2회, ``rag.chat.query.regeneration.max.count``\ ).
질문 하나에 LLM을 여러 번 호출하므로 일반 검색보다 응답에 시간이 걸리며, 클라우드 LLM에서는 호출할 때마다 요금이 발생합니다.

LLM에는 사용자의 질문과, 검색으로 찾은 문서의 본문이나 그 발췌가 전송됩니다.
제공자를 고를 때는 이 전송처를 확인하십시오.

대화는 ``session_id``\ 로 식별되며 Fess의 메모리에 보관됩니다.
기본적으로 30분 동안 조작이 없으면 사라지고(\ ``rag.chat.session.timeout.minutes``\ ), 한 대화에 남기는 메시지는 30건까지입니다(\ ``rag.chat.history.max.messages``\ ).
대화는 Fess를 재시작해도 사라집니다.

LLM 제공자 고르기
=================

Fess 15.9에서는 LLM과의 연결이 제공자별 ``fess-llm-*`` 플러그인으로 제공됩니다.
어떤 제공자를 사용할지는 ``rag.llm.name``\ 으로 지정합니다.

.. list-table::
   :header-rows: 1
   :widths: 14 12 18 22 34

   * - 제공자
     - ``rag.llm.name``
     - 플러그인
     - 기본 모델
     - 연결에 필요한 설정과, 질문·문서의 전송처
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ``gemma4:e4b``
     - ``rag.llm.ollama.api.url``\ (기본값 ``http://localhost:11434``\ ). 전송처는 직접 운영하는 Ollama 서버입니다
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - ``gpt-5-mini``
     - ``rag.llm.openai.api.key``\ . 전송처는 OpenAI입니다
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - ``gemini-3.1-flash-lite-preview``
     - ``rag.llm.gemini.api.key``\ . 전송처는 Google입니다
   * - Amazon Bedrock
     - ``bedrock``
     - ``fess-llm-bedrock``
     - ``us.amazon.nova-2-lite-v1:0``
     - ``rag.llm.bedrock.region``\ (기본값 ``us-east-1``\ )과, ``rag.llm.bedrock.api.key`` 또는 AWS 자격 증명. 전송처는 지정한 리전의 Amazon Bedrock입니다

모델은 ``rag.llm.<제공자>.model``\ 로 바꿀 수 있습니다.

OpenAI와 Gemini는 API 키만 준비하면 시작할 수 있지만, 질문과 문서가 각 서비스로 전송됩니다.
Ollama는 질문과 문서를 자신의 서버 밖으로 내보내지 않지만, 모델을 실행할 서버가 필요합니다.
docker-fess의 Ollama용 Compose 파일은 NVIDIA GPU를 전제로 합니다.
Bedrock은 AWS 자격 증명과 리전 설정이 필요합니다.
설정 방법은 `Amazon Bedrock 설정 <https://fess.codelibs.org/ko/stable/config/llm-bedrock.html>`__\ 을 참조하십시오.

필요한 설정은 세 가지
=====================

AI 검색 모드를 동작시키려면 다음 세 가지가 모두 갖추어져 있어야 합니다.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 설정
     - 설정하는 곳
     - Docker에서 전달하는 방법
   * - ``rag.chat.enabled=true``\ (기본값은 ``false``\ )
     - ``fess_config.properties``\ . 관리 화면에는 항목이 없습니다
     - ``FESS_JAVA_OPTS``\ 에 ``-Dfess.config.rag.chat.enabled=true``
   * - ``fess-llm-*`` 플러그인
     - [시스템] > [플러그인], 또는 ``bin/fess-setup``
     - ``FESS_PLUGINS=fess-llm-openai:15.9.0`` 등
   * - ``rag.llm.name``\ 과 제공자별 연결 설정
     - ``rag.llm.name``\ 은 [시스템] > [일반], 연결 설정(\ ``rag.llm.<제공자>.*``\ )은 ``fess_config.properties``
     - ``-Dfess.system.rag.llm.name=openai``\ , ``-Dfess.config.rag.llm.openai.api.key=...`` 등

``rag.llm.name``\ 의 기본값은 ``ollama``\ 입니다.
OpenAI 플러그인만 넣고 ``rag.llm.name``\ 을 바꾸지 않으면, Fess는 존재하지 않는 Ollama용 클라이언트를 계속 찾으며 AI 검색 모드를 사용할 수 없습니다.
이때 로그에 ``[LLM] LlmClient not found. componentName=ollamaLlmClient``\ 라는 경고가 출력됩니다.

``-Dfess.system.rag.llm.name``\ 은 ``system.properties``\ 에 값이 없을 때만 사용되는 초깃값입니다.
[일반]에서 저장한 값이 ``system.properties``\ 에 기록되면 그쪽이 우선합니다.

Docker에서 실행하기(OpenAI·Gemini)
==================================

docker-fess에는 LLM을 연결하기 위한 오버레이용 Compose 파일이 준비되어 있습니다.
:doc:`guide-02`\ 에서 Compose 파일을 둔 디렉터리에서 v15.9.0의 파일을 받습니다.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-openai.yaml

API 키를 셸의 환경 변수에 넣고, 세 파일을 지정하여 시작합니다.

::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml``\ 은 ``fess01``\ 에 다음 환경 변수를 추가합니다.
API 키와 모델 이름은 셸의 ``OPENAI_API_KEY``\ 와 ``OPENAI_MODEL``\ (설정하지 않으면 ``gpt-5-mini``\ )에서 설정되므로, 파일에 키를 적을 필요가 없습니다.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

``FESS_PLUGINS``\ 의 플러그인은 컨테이너 시작 시 Fess보다 먼저 설치되므로, 따로 재시작할 필요가 없습니다.
이미 ``fess01``\ 이 실행 중이라면 이 명령으로 ``fess01``\ 이 다시 만들어지며, [일반]에서 변경했던 설정은 컨테이너와 함께 사라집니다.
이후의 ``ps``\ ·\ ``logs``\ ·\ ``down`` 등의 명령에도 같은 세 파일을 지정하십시오.

Gemini의 경우에는 ``compose-gemini.yaml``\ 을 받고 ``GEMINI_API_KEY``\ 를 설정하여, 같은 방법으로 세 번째 파일로 지정합니다.
이 파일은 모델을 ``GEMINI_MODEL``\ (설정하지 않으면 ``gemini-2.5-flash``\ )에서 설정하므로, 플러그인의 기본 모델이 아니라 ``gemini-2.5-flash``\ 가 사용됩니다.

.. note::

   ``FESS_JAVA_OPTS``\ 를 설정하는 오버레이용 파일을 두 개 이상 지정하면, 마지막 파일의 값만 사용됩니다(OCR용 설정 등과 조합하는 경우).
   그럴 때는 필요한 ``-D`` 옵션을 모두 하나의 ``FESS_JAVA_OPTS``\ 로 모은 Compose 파일을 직접 준비합니다.
   ``FESS_JAVA_OPTS``\ 는 공백으로 구분되므로, 값에 공백을 포함하는 옵션은 쓸 수 없습니다.

``-Dfess.config.rag.llm.openai.api.key``\ 처럼 전달한 API 키는 [시스템 정보] > [설정 정보]에서 마스킹되어 표시됩니다.
사내 프록시를 거쳐 외부로 나가야 하는 경우에는 ``-Dfess.config.http.proxy.host=...``\ 와 ``-Dfess.config.http.proxy.port=...``\ 를 추가합니다.
LLM 플러그인은 Fess 공통의 프록시 설정을 사용합니다.

Docker에서 실행하기(Ollama)
===========================

``compose-ollama.yaml``\ 은 Ollama 컨테이너 ``ollama01``\ 을 추가하고 ``fess01``\ 을 거기에 연결합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 대상
     - 설정되는 내용
   * - ``fess01``
     - ``FESS_PLUGINS=fess-llm-ollama:15.9.0``\ , ``-Dfess.config.rag.chat.enabled=true``\ , ``-Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434``
   * - ``ollama01``
     - 이미지 ``ollama/ollama:latest``\ , 네트워크 ``search_net``\ , 포트 11434, 볼륨 ``ollama-data``\ , NVIDIA GPU 1개 할당

``rag.llm.name``\ 과 모델은 설정되지 않으므로, 기본값인 ``ollama``\ 와 ``gemma4:e4b``\ 가 사용됩니다.
URL을 ``ollama01``\ 로 향하게 하는 것은, 기본값인 ``http://localhost:11434``\ 가 ``fess01`` 컨테이너 자신을 가리키게 되기 때문입니다.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-ollama.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gemma4:e4b

이 파일을 사용하려면 NVIDIA Container Toolkit이 설치된 환경이 필요합니다.
GPU가 없는 환경에서 시험하려면, 받은 파일에서 ``ollama01``\ 의 ``deploy:`` 이하를 삭제합니다.
CPU로 동작하므로 답변에 시간이 걸립니다.

Fess는 설정된 모델이 Ollama의 모델 목록(\ ``/api/tags``\ )에 있을 때만 Ollama를 사용 가능하다고 판단하며, 이 확인을 기본적으로 60초마다 수행합니다.
따라서 모델을 받은 뒤 1분 정도 지나면 AI 검색 모드를 사용할 수 있게 됩니다.
파일 첫머리의 주석에는 다른 파일 이름과 ``gpt-oss:20b``\ 를 받는 절차가 적혀 있지만, 위의 절차를 따르십시오.
다른 모델을 사용하려면 그 모델을 ``ollama pull``\ 한 다음, ``FESS_JAVA_OPTS``\ 에 ``-Dfess.config.rag.llm.ollama.model=<모델 이름>``\ 을 추가합니다.

Docker 이외(ZIP·RPM·DEB)에서 설정하기
=====================================

1. 플러그인을 설치합니다. [시스템] > [플러그인] > [설치]에서 고르거나, 명령으로 설치합니다

   ::

       $ bin/fess-setup install plugin fess-llm-openai:15.9.0

2. ``fess_config.properties``\ 에 설정을 추가합니다. ZIP 판은 ``app/WEB-INF/classes/fess_config.properties``\ , RPM/DEB 판은 ``/etc/fess/fess_config.properties``\ 입니다

   ::

       rag.chat.enabled=true
       rag.llm.openai.api.key=sk-...
       rag.llm.openai.model=gpt-5-mini

3. Fess를 재시작합니다. 플러그인도 ``fess_config.properties``\ 의 변경도 재시작 시 읽어 들입니다
4. [시스템] > [일반]을 열고, "AI 검색" 영역의 "LLM 제공자"에서 ``openai``\ 를 골라 [갱신]을 클릭합니다

"AI 검색" 영역은 ``rag.chat.enabled=true``\ 이고, LLM 플러그인이 하나 이상 로드되어 있을 때만 표시됩니다.
"LLM 제공자"의 선택지는 설치된 플러그인에 대응하는 제공자뿐입니다.
영역이 보이지 않으면 1~3단계를 다시 확인하십시오.

동작 확인하기
=============

검색 화면에서 확인하기
----------------------

1. ``http://localhost:8080/``\ 을 엽니다. 위쪽 내비게이션 바에 로봇 아이콘이 붙은 [AI 검색]이 표시됩니다
2. [AI 검색]을 클릭하면 채팅 화면(\ ``/chat``\ )이 열립니다
3. 크롤링한 문서에 답이 있을 법한 질문을 입력합니다. :doc:`guide-02`\ 에서 검색 가이드를 크롤링했다면 "와일드카드 검색에서 사용할 수 있는 기호를 알려 주세요" 등으로 시험할 수 있습니다

답변을 생성하는 동안 분석·검색·평가·가져오기·답변의 각 단계가 차례로 표시됩니다.
답변 아래에는 근거로 삼은 문서가 "출처"로 번호와 함께 나열되며, 본문 중의 ``[1]`` 같은 번호와 대응합니다.
화제를 바꿀 때 [새 채팅]을 클릭하면 대화 이력이 지워집니다.

[AI 검색]이 표시되지 않으면 뒤에 나오는 "자주 걸리는 부분"을 확인하십시오.

API로 확인하기
--------------

화면을 사용하지 않고 확인하려면 ``/api/v2/ui/config``\ 를 호출합니다.
``response.features.rag_chat_enabled``\ 가 ``true``\ 이면 그 사용자는 AI 검색 모드를 사용할 수 있습니다.

``/api/v2/chat`` 같은 상태를 바꾸는 요청에는 세션에 연결된 CSRF 토큰을 ``X-Fess-CSRF-Token`` 헤더로 보내야 합니다.
``/api/v2/ui/config``\ 의 응답에 토큰이 포함되므로, 쿠키를 저장하면서 가져오고 같은 쿠키로 호출합니다(예에서는 ``jq``\ 를 사용합니다).

::

    $ curl -s -c cookies.txt http://localhost:8080/api/v2/ui/config > ui-config.json
    $ jq '.response.features.rag_chat_enabled' ui-config.json
    true
    $ TOKEN=$(jq -r '.response.csrf_token' ui-config.json)
    $ curl -s -b cookies.txt -X POST http://localhost:8080/api/v2/chat \
        -H 'Content-Type: application/json' \
        -H "X-Fess-CSRF-Token: $TOKEN" \
        -d '{"message":"와일드카드 검색에서 사용할 수 있는 기호를 알려 주세요"}' | jq '.response'

응답의 ``content``\ 가 답변, ``sources``\ 가 근거로 삼은 문서(\ ``rank``\ , ``title``\ , ``url`` 등), ``session_id``\ 가 대화의 ID입니다.
이어서 질문할 때는 ``{"message":"...","session_id":"<이전 session_id>"}``\ 처럼 ``session_id``\ 를 다시 보냅니다.

이 예는 로그인하지 않은 익명 사용자로 호출하므로, ``{role}guest``\ 가 붙은 문서만 검색 대상이 됩니다.
로그인한 사용자로 호출하는 방법, 스트리밍 버전인 ``/api/v2/chat/stream``\ 의 이벤트, 오류 코드는 `Chat API <https://fess.codelibs.org/ko/stable/api/api-chat.html>`__\ 와 `API 개요 <https://fess.codelibs.org/ko/stable/api/api-overview.html>`__\ 를 참조하십시오.
``/api/v1/chat``\ 은 ``fess-webapp-v1-api`` 플러그인을 설치한 경우에만 사용할 수 있는 이전 형식의 API입니다.
새로 만드는 연동에는 ``/api/v2/chat``\ 을 사용하십시오.

관리 화면과 로그에서 확인하기
-----------------------------

[시스템 정보] > [검색 로그]의 [AI 채팅] 탭에 요청 수, 사용자 수, 총 토큰 수, 평균 응답 시간, 오류율과 함께 사용자별·의도별·모델별 건수가 표시됩니다.
이 기록은 ``rag.chat.log.enabled``\ (기본값 ``true``\ )로 활성화되어 있으며, 질문과 답변의 본문은 기록되지 않습니다.
토큰 수는 LLM 플러그인이 보고한 경우에만 기록됩니다.

Docker의 경우, 플러그인이 설치되었는지는 컨테이너 로그에서 확인할 수 있습니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml logs fess01 | grep -E 'Installing|\[LLM\]'

``Installing fess-llm-openai-15.9.0.jar``\ 가 있으면 설치된 것입니다.
``[LLM] LlmClient not found``\ 가 계속해서 출력된다면 ``rag.llm.name``\ 과 설치한 플러그인이 맞지 않는 것입니다.

사용자와 참조하는 문서 좁히기
=============================

AI 검색 모드의 검색에는 평소의 검색과 같은 역할에 의한 필터링이 적용됩니다.
사용자가 검색 결과에서 볼 수 없는 문서는 답변의 근거에도 출처에도 사용되지 않습니다.
문서별로 보여 줄 대상은 크롤링 설정의 "권한"으로 정해집니다.
설계의 방향은 :doc:`guide-05`\ 를 참조하십시오.

그 위에, [시스템] > [일반]의 "AI 검색" 영역에서 채팅 자체의 사용 범위를 좁힐 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 내용
   * - "채팅 권한"(\ ``rag.chat.permissions``\ )
     - 채팅을 사용할 수 있는 사용자를 ``{role}rag_user,{group}sales,{user}taro``\ 처럼 쉼표로 구분하여 지정합니다. 비어 있으면 모두가 사용할 수 있습니다. 로그인하지 않은 사용자도 사용하게 하려면 ``{role}guest``\ 를 포함합니다
   * - "채팅 라벨"(\ ``rag.chat.labels``\ )
     - 답변의 근거로 삼는 문서를, 지정한 라벨 값 중 하나가 붙은 문서로 한정합니다. ``faq,policy``\ 처럼 쉼표로 구분하여 지정하며, 비어 있으면 사용자가 볼 수 있는 모든 문서가 대상입니다

"채팅 권한"의 대상이 아닌 사용자에게는 [AI 검색]이 표시되지 않으며, API는 로그인하지 않았으면 401, 로그인했으면 403을 돌려줍니다.
로그인한 사용자에게는 ``{role}guest``\ 가 붙지 않으므로, ``{role}guest``\ 만 지정하면 로그인한 사용자는 채팅을 사용할 수 없게 됩니다.
유효한 항목이 하나도 없는 값(\ ``{role}``\ 만 등)을 저장하면 아무도 사용할 수 없게 됩니다.

"채팅 라벨"은, 예를 들어 사내 규정과 FAQ처럼 답변의 근거로서 신뢰할 수 있는 문서에 라벨을 붙여 두고, 거기에서만 답하게 하고 싶을 때 사용합니다.
라벨을 만드는 방법과 붙이는 방법은 :doc:`guide-04`\ 를 참조하십시오.

자주 걸리는 부분
================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 증상
     - 확인할 것
   * - [AI 검색]이 표시되지 않는다
     - 다음 순서로 확인합니다. (1) ``rag.chat.enabled=true``\ 가 전달되었는가. (2) 플러그인이 설치되었는가(로그의 ``Installing``\ ). (3) ``rag.llm.name``\ 이 설치한 플러그인과 맞는가(\ ``LlmClient not found`` 경고). (4) API 키가 비어 있지 않은가, Ollama에서는 모델을 받았는가. (5) "채팅 권한"에서 자신이 빠져 있지 않은가
   * - [일반]에 "AI 검색" 영역이 없다
     - ``rag.chat.enabled``\ 가 ``false``\ 인 채이거나, LLM 플러그인이 로드되지 않았습니다. 설정과 플러그인 설치 후에 Fess를 재시작했는지 확인합니다
   * - ``down``\ 과 ``up -d`` 후에 "LLM 제공자"가 원래대로 돌아갔다
     - [일반]의 값은 ``fess01`` 컨테이너 안의 ``system.properties``\ 에 저장되므로, 컨테이너를 다시 만들면 사라집니다. ``FESS_JAVA_OPTS``\ 의 ``-Dfess.system.rag.llm.name``\ 으로 지정해 둡니다
   * - API가 ``403``\ 을 돌려준다
     - CSRF 토큰을 ``X-Fess-CSRF-Token``\ 으로 보내고 있는지, 토큰을 가져왔을 때의 쿠키를 보내고 있는지 확인합니다. 로그인한 사용자가 "채팅 권한"에서 빠져 있는 경우에도 403입니다
   * - API가 ``429``\ 를 돌려준다
     - 사용자별로 1분당 30회까지의 제한이 있습니다(\ ``api.chat.rate.limit.per.user.per.minute``\ )
   * - 클라우드 LLM에 연결할 수 없다
     - 컨테이너에서 외부로 나갈 수 있는지 확인하고, 프록시가 필요하면 ``http.proxy.host``\ 와 ``http.proxy.port``\ 를 설정합니다

답변의 질을 높이고 싶을 때는 먼저 검색의 질을 확인합니다.
AI 검색 모드는 일반 검색에서 상위에 온 문서(기본값 5건, ``rag.chat.context.max.documents``\ )를 근거로 삼으므로, 같은 질문의 단어로 검색했을 때 관계없는 문서가 상위에 온다면 답변도 그에 끌려갑니다.
검색의 개선은 :doc:`guide-08`\ 에서 다룹니다.
프롬프트 유형별 온도나 최대 토큰 수, 프롬프트 교체는 `AI 검색(RAG) 및 LLM 통합 개요 <https://fess.codelibs.org/ko/stable/config/llm-overview.html>`__\ 를 참조하십시오.

다음에 읽을 글
==============

- 키워드가 일치하지 않아도 의미가 가까운 문서를 검색에 더하고 싶다: :doc:`guide-18`
- Claude 같은 AI 에이전트가 Fess를 검색하게 하고 싶다: :doc:`guide-20`
- 부서나 역할에 따라 검색할 수 있는 문서를 나누고 싶다: :doc:`guide-05`
- 검색 로그를 보고 검색의 질을 개선하고 싶다: :doc:`guide-08`
- SSO로 로그인하게 하여 사용자별로 보여 주는 문서를 나누고 싶다: :doc:`guide-15`

참고 자료
=========

- `AI 검색 모드 기능 설정 <https://fess.codelibs.org/ko/stable/config/rag-chat.html>`__
- `AI 검색(RAG) 및 LLM 통합 개요 <https://fess.codelibs.org/ko/stable/config/llm-overview.html>`__
- `Ollama 설정 <https://fess.codelibs.org/ko/stable/config/llm-ollama.html>`__
- `OpenAI 설정 <https://fess.codelibs.org/ko/stable/config/llm-openai.html>`__
- `Google Gemini 설정 <https://fess.codelibs.org/ko/stable/config/llm-gemini.html>`__
- `Amazon Bedrock 설정 <https://fess.codelibs.org/ko/stable/config/llm-bedrock.html>`__
- `Chat API <https://fess.codelibs.org/ko/stable/api/api-chat.html>`__
- `AI 검색 모드(사용자용) <https://fess.codelibs.org/ko/stable/user/chat-search.html>`__
- `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
- `docker-fess의 compose 디렉터리(v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
