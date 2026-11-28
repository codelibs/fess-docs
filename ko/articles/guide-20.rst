===================================
MCP로 AI 에이전트에서 Fess 검색하기
===================================

들어가며
========

Claude Code 같은 AI 에이전트에게 사내 문서를 조사하게 하고 싶을 때, 에이전트가 Fess 검색을 직접 호출할 수 있으면 인덱싱된 문서를 그대로 근거로 사용할 수 있습니다.
이를 위한 구조가 MCP(Model Context Protocol)입니다.
Fess에서는 플러그인 ``fess-webapp-mcp``\ 를 설치하면 ``/mcp``\ 에 MCP 서버 엔드포인트가 추가됩니다.

이 글에서는 Fess 15.9에 이 플러그인을 설치하고, 인증을 필수로 설정한 다음 AI 에이전트에서 접속하여 동작을 확인하기까지의 과정을 설명합니다.

이 글의 절차를 마치면 다음 상태가 됩니다.

- ``/mcp``\ 가 동작하는지 ``curl``\ 로 확인할 수 있다
- 액세스 토큰이 없는 호출은 거부된다
- 에이전트가 검색할 수 있는 문서의 범위를 토큰의 권한으로 정할 수 있다
- Claude Code에서 Fess의 ``search`` 도구를 호출할 수 있다

.. note::

   :doc:`guide-19`\ 의 AI 검색 모드와는 호출 방향이 반대입니다.
   AI 검색 모드에서는 Fess가 LLM(Ollama, OpenAI 등)을 호출하여 답변을 만듭니다. Ollama는 이를 위한 LLM 실행 환경이며, MCP 클라이언트가 아닙니다.
   MCP에서는 외부 AI 에이전트가 Fess를 검색 도구로 호출하고, 답변은 에이전트 쪽 LLM이 만듭니다.

``/mcp``\ 가 제공하는 것
========================

``/mcp``\ 는 ``POST``\ 만 받으며, 요청 1건에 JSON 1개를 반환합니다(세션은 유지하지 않습니다).
검색은 검색 화면과 같은 처리를 거치므로, 역할에 따른 검색 결과 구분이 그대로 적용됩니다.

15.9.0 플러그인이 공개하는 것은 다음과 같습니다.
모두 읽기 전용이며, Fess의 데이터를 변경하는 것은 없습니다.

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - 이름
     - 내용
     - 사용 조건
   * - ``search`` (도구)
     - 전문 검색. 결과의 각 건에 ``doc_id``\ 가 붙습니다
     - 항상 사용 가능
   * - ``suggest`` (도구)
     - 입력 중인 단어에 대한 추천 후보
     - 항상 사용 가능
   * - ``get_document`` (도구)
     - ``doc_id``\ 를 지정하여 문서 1건의 본문을 가져옵니다
     - 항상 사용 가능
   * - ``get_index_stats`` (도구)
     - 인덱스 이름, 문서 수, JVM 메모리 사용량
     - 기본 설정에서는 사용할 수 없음(후술)
   * - ``fess://document/{doc_id}`` (리소스)
     - ``get_document``\ 와 같은 가져오기를 리소스로 수행합니다
     - 항상 사용 가능
   * - ``fess://index/stats`` (리소스)
     - ``get_index_stats``\ 와 같은 내용
     - ``get_index_stats``\ 와 같음
   * - ``basic_search`` / ``advanced_search`` (프롬프트)
     - 검색용 프롬프트 템플릿. ``advanced_search``\ 는 ``sort``\ 와 ``num``\ 도 받습니다
     - 항상 사용 가능

``search``\ 에서 ``num``\ 을 생략하면 3건만 반환됩니다(``mcp.default.page.size``\ 의 기본값).
본문은 ``search``\ 의 발췌도 ``get_document``\ 의 본문도 최대 10000자로 잘리며, ``get_document``\ 에서는 ``truncated``\ 가 ``true``\ 가 됩니다(``mcp.content.max.length``).

플러그인 설치하기
=================

플러그인 버전은 Fess의 마이너 버전에 맞춥니다.
Fess 15.9에는 ``fess-webapp-mcp``\ 의 15.9.x를 사용합니다.
다음 방법 중 하나로 설치하고, 설치 후 Fess를 재시작합니다.

- 관리 화면: [시스템] > [플러그인]에서 [설치]를 클릭하고, [원격] 탭에서 ``fess-webapp-mcp``\ 를 선택하여 설치합니다
- 명령줄: ``bin/fess-setup install plugin fess-webapp-mcp:15.9.0``
- Docker: ``compose.yaml``\ 의 ``fess01``\ 의 ``environment``\ 에 ``FESS_PLUGINS``\ 를 추가합니다. Docker 이미지에는 이 플러그인이 포함되어 있지 않습니다

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"

Docker 버전에서 이름이나 버전 지정이 잘못되면 해당 플러그인은 건너뛰고 컨테이너는 그대로 기동합니다.
추가한 후에는 기동 로그에서 플러그인을 가져왔는지 확인하십시오.

.. warning::

   Fess를 업그레이드할 때는 기동하기 전에 이 플러그인도 새 버전으로 교체하십시오.
   오래된 버전(예: 15.8용)의 플러그인 jar가 ``WEB-INF/plugin``\ 에 남아 있으면 Fess 15.9는 기동 시 초기화에 실패하고, ``/mcp``\ 뿐 아니라 모든 화면과 API가 404를 반환합니다.
   명령줄에서는 ``bin/fess-setup upgrade plugins``\ 로 교체할 수 있습니다.

재시작 후 로그 파일 ``fess.log``\ 에 다음 WARN이 출력되면 엔드포인트가 활성화된 것입니다.

::

    [MCP] mcp.auth.mode=none - every /mcp caller is treated as anonymous. Set mcp.auth.mode=fess_token, ...

이 메시지는 다음 절에서 설명하는 "인증 없음" 상태로 동작하고 있음을 나타냅니다.

먼저 인증 없이 동작 확인하기
============================

.. warning::

   설치 직후의 ``/mcp``\ 는 인증 없이 동작합니다(``mcp.auth.mode=none``).
   ``/mcp``\ 에 도달할 수 있는 사람은 누구나 로그인하지 않은 사용자(게스트)와 같은 권한으로 검색하고, ``get_document``\ 로 문서 본문까지 가져올 수 있습니다.
   권한을 기본값 ``{role}guest`` 그대로 둔 크롤링 설정의 문서는 모두 대상이 됩니다.
   이 상태에서 시험하는 것은 로컬 환경으로 한정하고, 다음 절에서 인증을 필수로 설정하십시오.
   참고로 [시스템] > [일반]에서 "로그인 필요"를 활성화한 경우, 이 상태의 ``/mcp``\ 는 모든 호출을 HTTP 403으로 거부합니다. 이 경우에는 다음 절로 진행하십시오.

Fess가 ``http://localhost:8080``\ 에서 동작하고 있다고 가정하고 ``server/discover``\ 를 호출합니다.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: server/discover' \
        -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

응답의 ``result.supportedVersions``\ 에 ``2026-07-28``\ 이, ``result.capabilities``\ 에 ``tools`` 등이 들어 있으면 성공입니다.

이어서 ``search`` 도구를 호출합니다.
크롤링한 문서에 포함된 단어를 ``q``\ 에 지정하십시오.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: tools/call' \
        -H 'Mcp-Name: search' \
        -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search","arguments":{"q":"Fess","num":5},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

``result.structuredContent.hits``\ 에 검색 결과가, ``total``\ 에 검색 건수가 들어갑니다.
헤더 값은 요청 본문과 일치해야 합니다.
``MCP-Protocol-Version``\ 은 ``params._meta``\ 의 버전과, ``Mcp-Method``\ 는 ``method``\ 와, ``Mcp-Name``\ 은 도구 이름과 같은 값으로 합니다.
서로 다르면 HTTP 400(오류 코드 ``-32020``)이 됩니다.

인증을 필수로 설정하기
======================

Fess의 액세스 토큰으로 인증하는 ``fess_token`` 모드로 전환합니다.
외부 인가 서버가 발급하는 JWT로 인증하는 ``oauth`` 모드도 있습니다.
설정은 README의 "OAuth 2.1 reference"를 참조하십시오.

액세스 토큰 만들기
------------------

1. 관리 화면의 [시스템] > [액세스 토큰]을 열고 [새로 만들기]를 클릭합니다
2. "이름"에 ``mcp-agent``\ 처럼 용도를 알 수 있는 이름을 입력합니다
3. "권한"에 에이전트에게 보여도 되는 문서의 역할을 한 줄에 하나씩 입력합니다. 게스트용 문서만으로 충분하다면 ``{role}guest``\ 입니다(정하는 방법은 "토큰의 권한과 검색 결과"에서 설명합니다)
4. 필요에 따라 "만료"를 지정하고 [작성]을 클릭합니다
5. 목록에서 만든 토큰의 이름을 클릭하면 상세 화면의 "토큰"에 값이 표시됩니다

mcp.auth.mode 설정하기
----------------------

``mcp.*`` 설정은 모두 Fess의 시스템 속성(``system.properties``)에서 읽어 들입니다.
``fess_config.properties``\ 나 ``-Dfess.config.*``\ 에 써도 무시되며, 오류도 로그도 출력되지 않습니다.

ZIP 버전은 ``app/WEB-INF/conf/system.properties``\ 에, RPM/DEB 버전은 ``/etc/fess/system.properties``\ 에 다음 줄을 추가합니다.

::

    mcp.auth.mode=fess_token

값은 실행 중에 다시 읽어 들이므로 몇 초 안에 반영되며, 재시작은 필요 없습니다.

Docker 버전의 ``fess01`` 컨테이너에는 볼륨이 없어서, 컨테이너 안의 파일에 쓴 설정은 컨테이너를 다시 만들면 사라집니다.
``compose.yaml``\ 의 ``FESS_JAVA_OPTS``\ 에 ``-Dfess.system.``\ 을 붙여 지정하십시오(``fess.config.``\ 가 아닙니다).

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"
      - "FESS_JAVA_OPTS=-Dfess.system.mcp.auth.mode=fess_token"

``FESS_PLUGINS``\ 와 ``FESS_JAVA_OPTS``\ 는 컨테이너를 다시 만들 때 반영됩니다.
``compose.yaml``\ 을 편집했다면 다음 명령을 실행합니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

``system.properties``\ 에 같은 키가 있으면 그쪽이 우선합니다.

인증이 적용되었는지 확인하기
----------------------------

앞 절의 ``server/discover``\ 를 그대로 다시 실행합니다.
토큰을 붙이지 않았으므로 HTTP 401과 ``WWW-Authenticate: Bearer realm="fess-mcp"`` 헤더가 반환됩니다(``curl -i``\ 로 헤더를 표시할 수 있습니다).
``fess_token`` 모드에서는 ``server/discover``\ 도 인증 대상입니다.

다음으로 앞 절의 ``search`` ``curl``\ 에 ``-H 'Authorization: Bearer <토큰>'``\ 을 추가하여 실행합니다.
``<토큰>``\ 은 상세 화면에 표시된 값으로 바꿉니다.
검색 결과가 반환되면 설정이 완료된 것입니다.
존재하지 않는 토큰이나 만료된 토큰으로는 HTTP 401이 됩니다.

토큰의 권한과 검색 결과
=======================

``fess_token`` 모드에서는 토큰의 권한이 그대로 검색 역할이 됩니다.
``search``\ 뿐 아니라 ``get_document``\ 도 같은 역할로 필터링되므로, ``doc_id``\ 를 알고 있어도 권한이 없는 문서는 가져올 수 없습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 토큰의 권한
     - 검색할 수 있는 문서
   * - 비어 있음
     - 게스트와 같음(``{role}guest``\ 의 문서)
   * - ``{role}guest``
     - 게스트와 같음
   * - ``{role}sales``
     - ``{role}sales``\ 의 문서만. 게스트용 문서는 포함되지 않습니다
   * - ``{role}sales``\ 와 ``{role}guest``
     - 양쪽 문서

게스트 역할이 보충되는 것은 권한이 비어 있는 토큰뿐입니다.
부서 문서와 전체 공개 문서를 모두 검색하게 하려면 ``{role}guest``\ 도 함께 지정합니다.
역할과 권한의 개념은 :doc:`guide-05`\ 를 참조하십시오.

확인하려면 권한이 다른 두 토큰으로 같은 단어를 ``search``\ 하고 ``total``\ 을 비교합니다.

.. warning::

   에이전트용 토큰에 ``{role}admin-api``\ 를 붙이지 마십시오.
   ``{role}admin-api``\ 를 가진 토큰은 Fess의 Admin API를 모두 호출할 수 있습니다.
   게다가 ``{role}admin-api``\ 만 있는 토큰으로 ``search``\ 하면, 이 역할을 가진 문서가 없으므로 0건이 됩니다.

``get_index_stats``\ 를 사용할 수 있게 하기
-------------------------------------------

``get_index_stats``\ 와 ``fess://index/stats``\ 는 ``mcp.tools.index_stats.permissions``\ 에 나열한 권한 중 하나를 가진 호출자에게만 표시됩니다.
기본값은 ``Radmin-api``\ (``{role}admin-api``\ 의 내부 표기)이며, ``none`` 모드에서는 어떤 호출자도 권한을 갖지 않으므로 누구에게도 표시되지 않습니다.
권한이 없는 호출자에게는 존재하지 않는 도구와 같은 오류가 반환됩니다.

검색만 한다면 이 도구는 필요 없습니다.
사용하는 경우에는 ``{role}admin-api``\ 를 주는 대신 전용 역할을 정하고, 그 역할을 토큰의 권한에 추가합니다.
``system.properties`` 쪽은 내부 표기(``{role}``\ 은 ``R``)로 씁니다.

::

    mcp.tools.index_stats.permissions=Rmcp-stats

이 예에서는 토큰의 권한에 ``{role}mcp-stats``\ 를 추가합니다.

그 밖의 설정
============

모두 ``system.properties``\ 에 씁니다(Docker 버전은 ``-Dfess.system.<키>``).
불리언 값은 ``true``\ 만 참으로 취급되며, ``1``\ 이나 ``yes``\ 는 거짓이 됩니다.

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - 키
     - 기본값
     - 내용
   * - ``mcp.allowed.origins``
     - (비어 있음)
     - 브라우저에서 호출하는 경우에 허용할 ``Origin``\ 을 ``https://app.example.com`` 형식으로 쉼표로 구분하여 지정합니다. 비어 있으면 ``Origin`` 헤더가 있는 요청을 모두 HTTP 403으로 거부합니다. ``curl``\ 이나 CLI 에이전트는 ``Origin``\ 을 보내지 않으므로 영향을 받지 않습니다
   * - ``mcp.rate.limit.per.minute``
     - ``60``
     - 호출자(토큰, 없으면 IP 주소)별 1분당 ``tools/call`` 등의 상한. 초과하면 HTTP 429와 ``Retry-After``\ 가 반환됩니다. ``0``\ 이면 비활성화
   * - ``mcp.content.max.length``
     - ``10000``
     - ``search``\ 와 ``get_document``\ 가 반환하는 본문의 최대 문자 수
   * - ``mcp.default.page.size``
     - ``3``
     - ``search``\ 에서 ``num``\ 을 생략했을 때의 건수
   * - ``mcp.enabled``
     - ``true``
     - ``false``\ 로 하면 ``/mcp``\ 는 모두 HTTP 503을 반환합니다
   * - ``mcp.legacy.protocol.enabled``
     - ``true``
     - ``initialize``\ 로 접속하는 구버전(``2025-11-25`` / ``2025-06-18``) 클라이언트도 받아들입니다

다음 2개는 ``mcp.*``\ 와 달리 Fess 본체의 ``fess_config.properties`` 설정입니다(Docker 버전은 ``-Dfess.config.<키>``).

- 다른 호스트의 리버스 프록시를 거치게 하는 경우에는 ``rate.limit.trusted.proxies``\ (기본값 ``127.0.0.1,::1``)에 프록시의 IP 주소를 추가합니다. 추가하지 않으면 프록시를 거친 호출자가 모두 같은 상한을 공유합니다
- 브라우저에서 다른 오리진으로 호출하는 경우에는 ``mcp.allowed.origins`` 외에 ``api.cors.allow.headers``\ 에 ``MCP-Protocol-Version``, ``Mcp-Method``, ``Mcp-Name``\ 을 추가합니다. 자세한 내용은 README의 "Browser clients"를 참조하십시오

AI 에이전트에서 접속하기
========================

Claude Code
-----------

Claude Code는 ``2026-07-28``\ 로 직접 접속할 수 있습니다.
``claude mcp add``\ 로 HTTP MCP 서버로 등록하고, ``--header``\ 로 토큰을 전달합니다.

::

    $ claude mcp add --transport http fess http://localhost:8080/mcp \
        --header "Authorization: Bearer <토큰>"

``claude mcp list``\ 를 실행하면 등록한 ``fess``\ 가 표시되며, 접속 상태도 확인할 수 있습니다.
Claude Code에 "Fess에서 출장비 정산 절차를 검색해 줘"처럼 요청하면, 에이전트는 ``search`` 도구를 다음과 같은 인수로 호출하고, 결과의 ``doc_id``\ 로 ``get_document``\ 를 호출하여 본문을 읽습니다.

.. code-block:: json

    {
      "name": "search",
      "arguments": {
        "q": "출장비 정산",
        "num": 5,
        "fields": { "label": ["manual"] }
      }
    }

``fields``\ 의 ``label``\ 에는 Fess 라벨의 값을 지정합니다(라벨로 범위를 좁히지 않는 경우에는 생략합니다).
``search``\ 의 인수로는 이 밖에 ``start``\ (페이징), ``sort``\ (``last_modified.desc`` 등), ``lang`` 등이 있습니다.

다른 클라이언트
---------------

OpenCode, Codex CLI, Gemini CLI 등 구버전(``initialize``)으로 접속하는 클라이언트도 ``mcp.legacy.protocol.enabled``\ 가 기본값 ``true``\ 이면 사용할 수 있습니다.
``2025-03-26`` 이전 버전만 지원하는 클라이언트는 접속할 수 없습니다.
stdio로만 MCP 서버를 기동할 수 있는 데스크톱용 클라이언트는 stdio와 HTTP를 중계하는 ``mcp-remote``\ 를 거칩니다.
클라이언트별 접속 가능 여부는 README의 "Client compatibility"에 정리되어 있습니다.

검색 결과의 외부 전송에 주의하기
--------------------------------

에이전트가 사용하는 LLM이 클라우드 서비스라면 ``search``\ 의 발췌나 ``get_document``\ 의 본문은 그 서비스로 전송됩니다.
토큰의 권한으로 보내도 되는 문서만 선택하고, 필요에 따라 ``mcp.content.max.length``\ 를 작게 하면 전송되는 범위를 좁힐 수 있습니다.

문제가 생겼을 때
================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 증상
     - 원인과 대처
   * - HTTP 400, 오류 코드 ``-32020``
     - ``MCP-Protocol-Version``, ``Mcp-Method``, ``Mcp-Name``\ 의 누락 또는 본문과의 불일치
   * - HTTP 401
     - ``fess_token`` 모드에서 토큰이 없거나, 존재하지 않거나, 만료됨
   * - 모든 요청이 HTTP 403
     - ``Origin`` 헤더가 ``mcp.allowed.origins``\ 에 없음. 또는 ``none`` 모드에서 "로그인 필요"가 활성화됨
   * - 첫 호출이 ``-32601``\ 이고 ``initialize``\ 를 언급함
     - 구버전 클라이언트이며, ``mcp.legacy.protocol.enabled``\ 가 ``true``\ 가 아님
   * - ``search``\ 가 0건
     - 토큰의 권한에 문서의 역할이 없음. 결과의 ``partial``\ 이 ``true``\ 이면 검색이 완료되지 않은 것이며(타임아웃이나 OpenSearch 장애), 해당 문서가 없다고 단정할 수 없습니다
   * - ``Tool execution failed (error_code:...)``
     - 원인은 ``fess.log``\ 에 WARN으로 기록되어 있습니다. ``error_code`` 값으로 로그를 검색합니다

다음에 읽을 글
==============

- MCP를 통해 보여 주는 문서를 역할로 나누고 싶다: :doc:`guide-05`
- Fess 자체가 LLM으로 답변하게 하고 싶다: :doc:`guide-19`
- 키워드가 일치하지 않아도 의미가 가까운 문서를 찾고 싶다: :doc:`guide-18`
- 검색 API를 업무 시스템에서 사용하고 싶다, 액세스 토큰을 용도별로 나누어 쓰고 싶다: :doc:`guide-11`
- SSO와 접근 보호를 한꺼번에 설정하고 싶다: :doc:`guide-15`

참고 자료
=========

- `fess-webapp-mcp README(15.9.0) <https://github.com/codelibs/fess-webapp-mcp/blob/fess-webapp-mcp-15.9.0/README.md>`__
- `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
- `액세스 토큰 <https://fess.codelibs.org/ko/stable/admin/accesstoken-guide.html>`__
- `Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__
- `Model Context Protocol <https://modelcontextprotocol.io/>`__
