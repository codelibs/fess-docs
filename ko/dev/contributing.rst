========================
기여 가이드
========================

|Fess| 프로젝트에 대한 기여를 환영합니다!
이 페이지에서는 |Fess| 에 기여하는 방법, 커뮤니티 가이드라인,
풀 리퀘스트 작성 절차 등을 설명합니다.

.. contents:: 목차
   :local:
   :depth: 2

시작하기
======

|Fess| 는 오픈소스 프로젝트이며
커뮤니티의 기여로 성장하고 있습니다.
프로그래밍 경험 수준에 관계없이 누구나 기여할 수 있습니다.

기여 방법
========

|Fess| 에는 다양한 방법으로 기여할 수 있습니다.

코드 기여
----------

- 새로운 기능 추가
- 버그 수정
- 성능 개선
- 리팩토링
- 테스트 추가

문서 기여
----------------

- 사용자 매뉴얼 개선
- API 문서 추가·업데이트
- 튜토리얼 작성
- 번역

Issue 보고
-----------

- 버그 리포트
- 기능 요청
- 질문 및 제안

커뮤니티 활동
--------------

- GitHub Discussions에서 토론
- 포럼에서 질문에 답변
- 블로그 글이나 튜토리얼 작성
- 이벤트에서 발표

첫 번째 기여
==========

처음 |Fess| 에 기여하는 경우 다음 단계를 권장합니다.

Step 1: 프로젝트 이해하기
---------------------------

1. `Fess 공식 사이트 <https://fess.codelibs.org/ja/>`__ 에서 기본 정보 확인
2. :doc:`getting-started` 에서 개발 개요 이해
3. :doc:`architecture` 에서 코드 구조 학습

Step 2: Issue 찾기
-------------------

`GitHub의 Issue 페이지 <https://github.com/codelibs/fess/issues>`__ 에서
``good first issue`` 라벨이 붙은 Issue를 찾습니다.

이러한 Issue는 처음 기여하는 사람에게 적합한 비교적 간단한 작업입니다.

Step 3: 개발 환경 설정
----------------------------

:doc:`setup` 에 따라 개발 환경을 구축합니다.

Step 4: 브랜치 생성하여 작업
----------------------------

:doc:`workflow` 에 따라 브랜치를 생성하고 코딩을 시작합니다.

Step 5: 풀 리퀘스트 작성
--------------------------

변경 사항을 커밋하고 풀 리퀘스트를 작성합니다.

코딩 규약
==============

|Fess| 에서는 일관성 있는 코드를 유지하기 위해
다음 코딩 규약을 따릅니다.

Java 코딩 스타일
----------------------

기본 스타일
~~~~~~~~~~

- **인덴트**: 공백 4개
- **개행 코드**: LF(Unix 스타일)
- **인코딩**: UTF-8
- **줄 길이**: 120자 이내 권장

명명 규칙
~~~~~~

- **패키지**: 소문자, 점 구분(예: ``org.codelibs.fess``)
- **클래스**: PascalCase(예: ``SearchService``)
- **인터페이스**: PascalCase(예: ``Crawler``)
- **메서드**: camelCase(예: ``executeSearch``)
- **변수**: camelCase(예: ``searchResult``)
- **상수**: UPPER_SNAKE_CASE(예: ``MAX_SEARCH_SIZE``)

주석
~~~~~~

**Javadoc:**

public 클래스, 메서드, 필드에는 Javadoc을 작성합니다.

.. code-block:: java

    /**
     * 검색을 실행합니다.
     *
     * @param query 검색 쿼리
     * @return 검색 결과
     * @throws SearchException 검색에 실패한 경우
     */
    public SearchResponse executeSearch(String query) throws SearchException {
        // 구현
    }

**구현 주석:**

복잡한 로직에는 일본어 또는 영어로 주석을 추가합니다.

.. code-block:: java

    // 쿼리 정규화(전각을 반각으로 변환)
    String normalizedQuery = QueryNormalizer.normalize(query);

클래스와 메서드 설계
~~~~~~~~~~~~~~~~~~~~

- **단일 책임 원칙**: 하나의 클래스는 하나의 책임만 가짐
- **작은 메서드**: 하나의 메서드는 하나의 일만 수행
- **의미 있는 이름**: 클래스명, 메서드명은 의도가 명확하도록

예외 처리
~~~~~~

.. code-block:: java

    // 좋은 예: 적절한 예외 처리
    try {
        executeSearch(query);
    } catch (IOException e) {
        logger.error("검색 중 오류가 발생했습니다", e);
        throw new SearchException("검색 실행에 실패했습니다", e);
    }

    // 피해야 할 예: 빈 catch 블록
    try {
        executeSearch(query);
    } catch (IOException e) {
        // 아무것도 하지 않음
    }

null 처리
~~~~~~~~~

- 가능한 한 ``null`` 을 반환하지 않음
- ``Optional`` 사용 권장
- ``@Nullable`` 어노테이션으로 null 가능성 명시

.. code-block:: java

    // 좋은 예
    public Optional<User> findUser(String id) {
        return Optional.ofNullable(userMap.get(id));
    }

    // 사용 예
    findUser("123").ifPresent(user -> {
        // 사용자가 존재하는 경우의 처리
    });

테스트 작성
~~~~~~~~~~

- 모든 public 메서드에 테스트 작성
- 테스트 메서드명은 ``test`` 로 시작
- Given-When-Then 패턴 사용

.. code-block:: java

    @Test
    public void testSearch() {
        // Given: 테스트 전제 조건
        SearchService service = new SearchService();
        String query = "test";

        // When: 테스트 대상 실행
        SearchResponse response = service.search(query);

        // Then: 결과 검증
        assertNotNull(response);
        assertEquals(10, response.getDocuments().size());
    }

코드 리뷰 가이드라인
========================

풀 리퀘스트 리뷰 프로세스
----------------------------

1. **자동 체크**: CI가 자동으로 빌드 및 테스트 실행
2. **코드 리뷰**: 메인테이너가 코드 리뷰
3. **피드백**: 필요에 따라 수정 요청
4. **승인**: 리뷰 승인
5. **병합**: 메인테이너가 main 브랜치에 병합

리뷰 관점
----------

리뷰에서는 다음 사항을 확인합니다:

**기능성**

- 요구사항을 충족하는가
- 의도한 대로 동작하는가
- 엣지 케이스가 고려되었는가

**코드 품질**

- 코딩 규약을 따르는가
- 읽기 쉽고 유지보수하기 쉬운 코드인가
- 적절한 추상화가 되었는가

**테스트**

- 충분한 테스트가 작성되었는가
- 테스트가 통과하는가
- 테스트가 의미 있는 검증을 하는가

**성능**

- 성능에 영향이 없는가
- 리소스 사용이 적절한가

**보안**

- 보안상 문제가 없는가
- 입력 검증이 적절한가

**문서**

- 필요한 문서가 업데이트되었는가
- Javadoc이 적절히 작성되었는가

리뷰 코멘트 대응
--------------------

리뷰 코멘트에는 신속하고 정중하게 대응합니다.

**수정이 필요한 경우:**

.. code-block:: text

    지적해 주셔서 감사합니다. 수정했습니다.
    [수정 내용의 간단한 설명]

**논의가 필요한 경우:**

.. code-block:: text

    의견 감사합니다.
    ○○의 이유로 현재 구현을 했는데
    △△라는 구현이 더 좋을까요?

풀 리퀘스트 모범 사례
================================

PR 크기
---------

- 작고 리뷰하기 쉬운 PR을 지향
- 하나의 PR에는 하나의 논리적 변경 포함
- 큰 변경은 여러 PR로 분할

PR 제목
-----------

명확하고 설명적인 제목을 작성합니다:

.. code-block:: text

    feat: 검색 결과 필터링 기능 추가
    fix: 크롤러 타임아웃 문제 수정
    docs: API 문서 업데이트

PR 설명
-------

다음 정보를 포함합니다:

- **변경 내용**: 무엇을 변경했는가
- **이유**: 왜 이 변경이 필요한가
- **테스트 방법**: 어떻게 테스트했는가
- **스크린샷**: UI 변경의 경우
- **관련 Issue**: Issue 번호(예: Closes #123)

.. code-block:: markdown

    ## 변경 내용
    검색 결과를 파일 타입으로 필터링할 수 있는 기능을 추가했습니다.

    ## 이유
    사용자로부터 "특정 파일 타입만 검색하고 싶다"는
    요청이 많이 들어왔기 때문입니다.

    ## 테스트 방법
    1. 검색 화면에서 파일 타입 필터 선택
    2. 검색 실행
    3. 선택한 파일 타입의 결과만 표시되는지 확인

    ## 관련 Issue
    Closes #123

커밋 메시지
----------------

명확하고 설명적인 커밋 메시지를 작성합니다:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**예:**

.. code-block:: text

    feat: 검색 필터 기능 추가

    사용자가 검색 결과를 파일 타입으로 필터링할 수 있도록 했습니다.

    - 필터 UI 추가
    - 백엔드 필터 처리 구현
    - 테스트 추가

    Closes #123

Draft PR 활용
--------------

작업 중인 PR은 Draft PR로 작성하고
완성되면 Ready for review로 변경합니다.

.. code-block:: text

    1. PR 작성 시 "Create draft pull request" 선택
    2. 작업이 완료되면 "Ready for review" 클릭

커뮤니티 가이드라인
======================

행동 규범
------

|Fess| 커뮤니티에서는 다음 행동 규범을 준수합니다:

- **존중**: 모든 사람을 존중
- **협력적**: 건설적인 피드백 제공
- **개방적**: 다른 관점과 경험 환영
- **예의 바르게**: 정중한 언어 사용

커뮤니케이션
----------------

**질문할 곳:**

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 일반적인 질문과 토론
- `Issue 트래커 <https://github.com/codelibs/fess/issues>`__: 버그 보고 및 기능 요청
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 일본어 포럼

**질문하는 방법:**

- 구체적으로 질문
- 시도한 것을 설명
- 오류 메시지나 로그 포함
- 환경 정보(OS, Java 버전 등) 기재

**답변하는 방법:**

- 정중하고 친절하게
- 구체적인 해결책 제시
- 참고 자료 링크 제공

감사 표현
--------

기여에 대해서는 감사의 마음을 표현합니다.
작은 기여도 프로젝트에 가치가 있습니다.

자주 묻는 질문
==========

Q: 초보자도 기여할 수 있나요?
---------------------------

A: 네, 환영합니다! ``good first issue`` 라벨의 Issue부터 시작하는 것을 권장합니다.
문서 개선도 초보자에게 적합한 기여입니다.

Q: 풀 리퀘스트는 얼마나 걸려서 리뷰되나요?
-------------------------------------------------

A: 일반적으로 며칠 이내에 리뷰합니다.
다만 메인테이너의 일정에 따라 달라질 수 있습니다.

Q: 풀 리퀘스트가 거부된 경우는?
-----------------------------------

A: 거부 이유를 확인하고 필요에 따라 수정하여 재제출할 수 있습니다.
모르는 점이 있으면 편하게 질문해 주세요.

Q: 코딩 규약을 위반한 경우는?
---------------------------------------

A: 리뷰에서 지적되므로 수정하면 문제없습니다.
Checkstyle을 실행하여 사전에 확인할 수 있습니다.

Q: 큰 기능을 추가하고 싶은 경우는?
-------------------------------

A: 먼저 Issue를 작성하여 제안 내용을 논의하는 것을 권장합니다.
사전에 합의를 얻음으로써 작업 낭비를 피할 수 있습니다.

Q: 일본어로 질문해도 되나요?
-------------------------------

A: 네, 일본어도 영어도 괜찮습니다.
Fess는 일본 발 프로젝트이므로 일본어 지원도 충실합니다.

기여 유형별 가이드
================

문서 개선
----------------

1. 문서 리포지토리를 포크:

   .. code-block:: bash

       git clone https://github.com/codelibs/fess-docs.git

2. 변경 사항 추가
3. 풀 리퀘스트 작성

버그 보고
------

1. 기존 Issue를 검색하여 중복 확인
2. 새 Issue 작성
3. 다음 정보 포함:

   - 버그 설명
   - 재현 절차
   - 예상되는 동작
   - 실제 동작
   - 환경 정보

기능 요청
------------

1. Issue 작성
2. 다음을 설명:

   - 기능 설명
   - 배경 및 동기
   - 제안하는 구현 방법(선택사항)

코드 리뷰
------------

다른 사람의 풀 리퀘스트를 리뷰하는 것도 기여입니다:

1. 관심 있는 PR 찾기
2. 코드 확인
3. 건설적인 피드백 제공

라이센스
========

|Fess| 는 Apache License 2.0으로 공개됩니다.
기여된 코드도 동일한 라이센스가 적용됩니다.

풀 리퀘스트를 작성함으로써
귀하의 기여가 이 라이센스로 공개되는 것에 동의한 것으로 간주됩니다.

감사의 말
====

|Fess| 프로젝트에 기여해 주셔서 감사합니다!
귀하의 기여가 |Fess| 를 더 나은 소프트웨어로 만듭니다.

다음 단계
==========

기여할 준비가 되었다면:

1. :doc:`setup` 에서 개발 환경 설정
2. :doc:`workflow` 에서 개발 플로우 확인
3. `GitHub <https://github.com/codelibs/fess>`__ 에서 Issue 찾기

참고 자료
======

- `GitHub 플로우 <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `오픈소스 기여 방법 <https://opensource.guide/ja/how-to-contribute/>`__
- `좋은 커밋 메시지 작성법 <https://chris.beams.io/posts/git-commit/>`__

커뮤니티 리소스
==================

- **GitHub**: `codelibs/fess <https://github.com/codelibs/fess>`__
- **Discussions**: `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- **Forum**: `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- **Twitter**: `@codelibs <https://twitter.com/codelibs>`__
- **Website**: `fess.codelibs.org <https://fess.codelibs.org/ja/>`__
