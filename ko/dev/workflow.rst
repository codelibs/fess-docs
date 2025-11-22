==============
개발 워크플로우
==============

이 페이지에서는 |Fess| 개발의 표준 워크플로우를 설명합니다.
기능 추가, 버그 수정, 테스트, 코드 리뷰 등
개발 작업 진행 방법을 배울 수 있습니다.

.. contents:: 목차
   :local:
   :depth: 2

개발 기본 플로우
==============

|Fess| 개발은 다음과 같은 흐름으로 진행합니다:

.. code-block:: text

    1. Issue 확인·작성
       ↓
    2. 브랜치 생성
       ↓
    3. 코딩
       ↓
    4. 로컬 테스트 실행
       ↓
    5. 커밋
       ↓
    6. 푸시
       ↓
    7. 풀 리퀘스트 작성
       ↓
    8. 코드 리뷰
       ↓
    9. 리뷰 피드백 대응
       ↓
    10. 병합

각 단계에 대해 자세히 설명합니다.

Step 1: Issue 확인·작성
=========================

개발을 시작하기 전에 GitHub의 Issue를 확인합니다.

기존 Issue 확인
-----------------

1. `Fess의 Issue 페이지 <https://github.com/codelibs/fess/issues>`__ 에 접속
2. 작업하고 싶은 Issue 찾기
3. Issue에 코멘트하여 작업 시작 의사 전달

.. tip::

   처음 기여하는 경우 ``good first issue`` 라벨이 붙은 Issue부터 시작하는 것을 권장합니다.

새로운 Issue 작성
-----------------

새로운 기능이나 버그 수정의 경우 Issue를 작성합니다.

1. `New Issue <https://github.com/codelibs/fess/issues/new>`__ 클릭
2. Issue 템플릿 선택
3. 필요한 정보 기입:

   - **제목**: 간결하고 알기 쉬운 설명
   - **설명**: 상세한 배경, 예상되는 동작, 현재 동작
   - **재현 절차**: 버그의 경우
   - **환경 정보**: OS, Java 버전, Fess 버전 등

4. ``Submit new issue`` 클릭

Issue 템플릿
~~~~~~~~~~~~~~~~~~

**버그 리포트:**

.. code-block:: markdown

    ## 문제 설명
    버그에 대한 간결한 설명

    ## 재현 절차
    1. ...
    2. ...
    3. ...

    ## 예상되는 동작
    본래 어떻게 되어야 하는가

    ## 실제 동작
    현재 어떻게 되고 있는가

    ## 환경
    - OS:
    - Java 버전:
    - Fess 버전:

**기능 요청:**

.. code-block:: markdown

    ## 기능 설명
    추가하고 싶은 기능 설명

    ## 배경 및 동기
    왜 이 기능이 필요한가

    ## 제안하는 구현 방법
    어떻게 구현할 것인가(선택사항)

Step 2: 브랜치 생성
====================

작업용 브랜치를 생성합니다.

브랜치 명명 규칙
--------------

브랜치명은 다음 형식을 따릅니다:

.. code-block:: text

    <type>/<issue-number>-<short-description>

**type 종류:**

- ``feature``: 새 기능 추가
- ``fix``: 버그 수정
- ``refactor``: 리팩토링
- ``docs``: 문서 업데이트
- ``test``: 테스트 추가·수정

**예:**

.. code-block:: bash

    # 새 기능 추가
    git checkout -b feature/123-add-search-filter

    # 버그 수정
    git checkout -b fix/456-fix-crawler-timeout

    # 문서 업데이트
    git checkout -b docs/789-update-api-docs

브랜치 생성 절차
----------------

1. 최신 main 브랜치 가져오기:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. 새 브랜치 생성:

   .. code-block:: bash

       git checkout -b feature/123-add-search-filter

3. 브랜치가 생성되었는지 확인:

   .. code-block:: bash

       git branch

Step 3: 코딩
==================

기능 구현이나 버그 수정을 수행합니다.

코딩 규약
--------------

|Fess| 에서는 다음 코딩 규약을 따릅니다.

기본 스타일
~~~~~~~~~~~~~~

- **인덴트**: 공백 4개
- **줄 길이**: 120자 이내 권장
- **인코딩**: UTF-8
- **개행 코드**: LF(Unix 스타일)

명명 규칙
~~~~~~

- **클래스명**: PascalCase(예: ``SearchService``)
- **메서드명**: camelCase(예: ``executeSearch``)
- **상수**: UPPER_SNAKE_CASE(예: ``MAX_SEARCH_SIZE``)
- **변수**: camelCase(예: ``searchResults``)

주석
~~~~~~

- **Javadoc**: public 클래스와 메서드에는 필수
- **구현 주석**: 복잡한 로직에는 일본어 또는 영어로 설명 추가

**예:**

.. code-block:: java

    /**
     * 검색을 실행합니다.
     *
     * @param query 검색 쿼리
     * @return 검색 결과
     */
    public SearchResponse executeSearch(String query) {
        // 쿼리 정규화
        String normalizedQuery = normalizeQuery(query);

        // 검색 실행
        return searchEngine.search(normalizedQuery);
    }

null 처리
~~~~~~~~~

- 가능한 한 ``null`` 을 반환하지 않음
- ``Optional`` 사용 권장
- ``null`` 체크는 명시적으로 수행

**예:**

.. code-block:: java

    // 좋은 예
    public Optional<User> findUser(String id) {
        return userRepository.findById(id);
    }

    // 피해야 할 예
    public User findUser(String id) {
        return userRepository.findById(id);  // null 가능성
    }

예외 처리
~~~~~~

- 예외는 적절히 캐치하여 처리
- 로그 출력 수행
- 사용자에게 이해하기 쉬운 메시지 제공

**예:**

.. code-block:: java

    try {
        // 처리
    } catch (IOException e) {
        logger.error("파일 읽기 오류", e);
        throw new FessSystemException("파일 읽기에 실패했습니다", e);
    }

로그 출력
~~~~~~

적절한 로그 레벨을 사용합니다:

- ``ERROR``: 오류 발생 시
- ``WARN``: 경고해야 할 상황
- ``INFO``: 중요한 정보
- ``DEBUG``: 디버그 정보
- ``TRACE``: 상세 추적 정보

**예:**

.. code-block:: java

    if (logger.isDebugEnabled()) {
        logger.debug("검색 쿼리: {}", query);
    }

개발 중 테스트
------------

개발 중에는 다음 방법으로 테스트합니다:

로컬 실행
~~~~~~~~~~

IDE 또는 명령줄에서 Fess를 실행하고 동작을 확인합니다:

.. code-block:: bash

    mvn compile exec:java

디버그 실행
~~~~~~~~~~

IDE의 디버거를 사용하여 코드 동작을 추적합니다.

단위 테스트 실행
~~~~~~~~~~~~~~

변경과 관련된 테스트를 실행합니다:

.. code-block:: bash

    # 특정 테스트 클래스 실행
    mvn test -Dtest=SearchServiceTest

    # 모든 테스트 실행
    mvn test

자세한 내용은 :doc:`building` 을 참조하세요.

Step 4: 로컬 테스트 실행
=========================

커밋 전에 반드시 테스트를 실행합니다.

단위 테스트 실행
--------------

.. code-block:: bash

    mvn test

통합 테스트 실행
--------------

.. code-block:: bash

    mvn verify

코드 스타일 검사
--------------------

.. code-block:: bash

    mvn checkstyle:check

모든 검사 실행
-------------------

.. code-block:: bash

    mvn clean verify

Step 5: 커밋
==============

변경 사항을 커밋합니다.

커밋 메시지 규약
--------------------

커밋 메시지는 다음 형식을 따릅니다:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**type 종류:**

- ``feat``: 새 기능
- ``fix``: 버그 수정
- ``docs``: 문서만 변경
- ``style``: 코드 의미에 영향이 없는 변경(포맷 등)
- ``refactor``: 리팩토링
- ``test``: 테스트 추가·수정
- ``chore``: 빌드 프로세스나 도구 변경

**예:**

.. code-block:: text

    feat: 검색 필터 기능 추가

    사용자가 검색 결과를 파일 타입으로 필터링할 수 있도록 했습니다.

    Fixes #123

커밋 절차
----------

1. 변경 사항 스테이징:

   .. code-block:: bash

       git add .

2. 커밋:

   .. code-block:: bash

       git commit -m "feat: 검색 필터 기능 추가"

3. 커밋 이력 확인:

   .. code-block:: bash

       git log --oneline

커밋 단위
------------

- 하나의 커밋에는 하나의 논리적 변경 포함
- 큰 변경은 여러 커밋으로 분할
- 커밋 메시지는 알기 쉽고 구체적으로

Step 6: 푸시
==============

브랜치를 원격 리포지토리에 푸시합니다.

.. code-block:: bash

    git push origin feature/123-add-search-filter

첫 푸시의 경우:

.. code-block:: bash

    git push -u origin feature/123-add-search-filter

Step 7: 풀 리퀘스트 작성
=========================

GitHub에서 풀 리퀘스트(PR)를 작성합니다.

PR 작성 절차
-----------

1. `Fess 리포지토리 <https://github.com/codelibs/fess>`__ 에 접속
2. ``Pull requests`` 탭 클릭
3. ``New pull request`` 클릭
4. 베이스 브랜치(``main``)와 비교 브랜치(작업 브랜치) 선택
5. ``Create pull request`` 클릭
6. PR 내용 기입(템플릿 따름)
7. ``Create pull request`` 클릭

PR 템플릿
---------------

.. code-block:: markdown

    ## 변경 내용
    이 PR에서 무엇을 변경했는가

    ## 관련 Issue
    Closes #123

    ## 변경 종류
    - [ ] 새 기능
    - [ ] 버그 수정
    - [ ] 리팩토링
    - [ ] 문서 업데이트
    - [ ] 기타

    ## 테스트 방법
    이 변경을 어떻게 테스트했는가

    ## 체크리스트
    - [ ] 코드가 동작함
    - [ ] 테스트를 추가함
    - [ ] 문서를 업데이트함
    - [ ] 코딩 규약을 따름

PR 설명
-------

PR 설명에는 다음을 포함합니다:

- **변경 목적**: 왜 이 변경이 필요한가
- **변경 내용**: 무엇을 변경했는가
- **테스트 방법**: 어떻게 테스트했는가
- **스크린샷**: UI 변경의 경우

Step 8: 코드 리뷰
====================

메인테이너가 코드를 리뷰합니다.

리뷰 관점
------------

리뷰에서는 다음 사항이 체크됩니다:

- 코드 품질
- 코딩 규약 준수
- 테스트 충실도
- 성능에 대한 영향
- 보안 문제
- 문서 업데이트

리뷰 코멘트 예
------------------

**승인:**

.. code-block:: text

    LGTM (Looks Good To Me)

**수정 요청:**

.. code-block:: text

    여기는 null 체크가 필요하지 않을까요?

**제안:**

.. code-block:: text

    이 처리는 Helper 클래스로 이동하는 게 좋을 것 같습니다.

Step 9: 리뷰 피드백 대응
===================================

리뷰 코멘트에 대응합니다.

피드백 대응 절차
----------------------

1. 리뷰 코멘트 읽기
2. 필요한 수정 수행
3. 변경 사항 커밋:

   .. code-block:: bash

       git add .
       git commit -m "fix: 리뷰 코멘트 대응"

4. 푸시:

   .. code-block:: bash

       git push origin feature/123-add-search-filter

5. PR 페이지에서 코멘트에 답변

코멘트 답변
--------------

리뷰 코멘트에는 반드시 답변합니다:

.. code-block:: text

    수정했습니다. 확인 부탁드립니다.

또는:

.. code-block:: text

    의견 감사합니다.
    ○○의 이유로 현재 구현을 했는데 어떻게 생각하시나요?

Step 10: 병합
=============

리뷰가 승인되면 메인테이너가 PR을 병합합니다.

병합 후 대응
------------

1. 로컬 main 브랜치 업데이트:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. 작업 브랜치 삭제:

   .. code-block:: bash

       git branch -d feature/123-add-search-filter

3. 원격 브랜치 삭제(GitHub에서 자동 삭제되지 않은 경우):

   .. code-block:: bash

       git push origin --delete feature/123-add-search-filter

자주 발생하는 개발 시나리오
==================

기능 추가
------

1. Issue 작성(또는 기존 Issue 확인)
2. 브랜치 생성: ``feature/xxx-description``
3. 기능 구현
4. 테스트 추가
5. 문서 업데이트
6. PR 작성

버그 수정
------

1. 버그 리포트 Issue 확인
2. 브랜치 생성: ``fix/xxx-description``
3. 버그를 재현하는 테스트 추가
4. 버그 수정
5. 테스트가 통과하는지 확인
6. PR 작성

리팩토링
--------------

1. Issue 작성(리팩토링 이유 설명)
2. 브랜치 생성: ``refactor/xxx-description``
3. 리팩토링 실행
4. 기존 테스트가 통과하는지 확인
5. PR 작성

문서 업데이트
--------------

1. 브랜치 생성: ``docs/xxx-description``
2. 문서 업데이트
3. PR 작성

개발 팁
==========

효율적인 개발
----------

- **작은 커밋**: 자주 커밋
- **초기 피드백**: Draft PR 활용
- **테스트 자동화**: CI/CD 활용
- **코드 리뷰**: 다른 사람의 코드도 리뷰

문제 해결
--------

어려움이 있을 때는 다음을 활용합니다:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- GitHub의 Issue 코멘트

다음 단계
==========

워크플로우를 이해했다면 다음 문서도 참조하세요:

- :doc:`building` - 빌드 및 테스트 상세
- :doc:`contributing` - 기여 가이드라인
- :doc:`architecture` - 코드베이스 이해

참고 자료
======

- `GitHub 플로우 <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `커밋 메시지 가이드라인 <https://chris.beams.io/posts/git-commit/>`__
- `코드 리뷰 모범 사례 <https://google.github.io/eng-practices/review/>`__
