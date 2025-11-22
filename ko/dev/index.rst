====================================
오픈소스 전문 검색 서버 - |Fess| 개발 가이드
====================================

이 가이드는 |Fess| 개발에 참여하기 위해 필요한 정보를 제공합니다.
|Fess| 개발을 처음 시작하는 분부터 경험이 풍부한 개발자까지, 폭넓은 분들을 대상으로 합니다.

.. contents:: 목차
   :local:
   :depth: 2

대상 독자
========

이 가이드는 다음과 같은 분들을 대상으로 합니다:

- |Fess| 의 기능 추가나 개선에 기여하고 싶은 개발자
- |Fess| 의 코드를 이해하고 싶은 기술자
- |Fess| 를 커스터마이즈하여 사용하고 싶은 분
- 오픈소스 프로젝트 참여에 관심이 있는 분

필요한 사전 지식
============

|Fess| 개발에 참여하려면 다음과 같은 지식이 도움이 됩니다:

**필수**

- Java 프로그래밍 기초 지식(Java 21 이상)
- Git 및 GitHub 기본 사용법
- Maven 기본 사용법

**권장**

- LastaFlute 프레임워크 지식
- DBFlute 지식
- OpenSearch/Elasticsearch 지식
- 웹 애플리케이션 개발 경험

개발 가이드 구성
==============

이 가이드는 다음 섹션으로 구성되어 있습니다.

:doc:`getting-started`
    |Fess| 개발 개요와 개발을 시작하기 위한 첫 단계를 설명합니다.
    개발에 필요한 기술 스택과 프로젝트 전체 구조를 이해할 수 있습니다.

:doc:`setup`
    개발 환경 설정 절차를 자세히 설명합니다.
    Java, IDE, OpenSearch 등 필요한 도구 설치부터
    |Fess| 소스 코드 취득 및 실행까지 단계별로 해설합니다.

:doc:`architecture`
    |Fess| 의 아키텍처와 코드 구조에 대해 설명합니다.
    주요 패키지, 모듈, 디자인 패턴을 이해함으로써
    효율적으로 개발을 진행할 수 있습니다.

:doc:`workflow`
    |Fess| 개발의 표준 워크플로우를 설명합니다.
    기능 추가, 버그 수정, 코드 리뷰, 테스트 등
    개발 작업 진행 방법을 배울 수 있습니다.

:doc:`building`
    |Fess| 의 빌드 방법과 테스트 방법에 대해 설명합니다.
    빌드 도구 사용법, 단위 테스트 실행,
    배포 패키지 생성 방법 등을 해설합니다.

:doc:`contributing`
    |Fess| 프로젝트 기여 방법에 대해 설명합니다.
    풀 리퀘스트 작성, 코딩 규약,
    커뮤니티와의 커뮤니케이션 방법 등을 배울 수 있습니다.

빠른 시작
==============

|Fess| 개발을 지금 바로 시작하고 싶다면 다음 절차를 따르세요:

1. **시스템 요구사항 확인**

   개발에는 다음 도구가 필요합니다:

   - Java 21 이상
   - Maven 3.x 이상
   - Git
   - IDE(Eclipse, IntelliJ IDEA 등)

2. **소스 코드 취득**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

3. **OpenSearch 플러그인 다운로드**

   .. code-block:: bash

       mvn antrun:run

4. **실행**

   IDE에서 ``org.codelibs.fess.FessBoot`` 을 실행하거나
   Maven에서 실행합니다:

   .. code-block:: bash

       mvn compile exec:java

자세한 내용은 :doc:`setup` 을 참조하세요.

개발 환경 선택
==============

|Fess| 개발은 다음 환경 중 하나에서 수행할 수 있습니다:

로컬 개발 환경
--------------

가장 일반적인 개발 환경입니다. 자신의 머신에 개발 도구를 설치하고
IDE를 사용하여 개발합니다.

**장점:**

- 빠른 빌드 및 실행
- IDE 기능을 완전히 활용 가능
- 오프라인에서도 작업 가능

**단점:**

- 초기 설정에 시간이 걸림
- 환경 차이로 인한 문제가 발생할 가능성

Docker를 사용한 개발 환경
------------------------

Docker 컨테이너를 사용하여 일관된 개발 환경을 구축할 수 있습니다.

**장점:**

- 환경의 일관성 유지
- 설정이 간단
- 깨끗한 상태로 되돌리기 쉬움

**단점:**

- Docker 지식이 필요
- 성능이 다소 저하될 수 있음

자세한 내용은 :doc:`setup` 을 참조하세요.

자주 묻는 질문
==========

Q: 개발에 필요한 최소 사양은?
--------------------------------

A: 다음을 권장합니다:

- CPU: 4코어 이상
- 메모리: 8GB 이상
- 디스크: 20GB 이상의 여유 공간

Q: 어떤 IDE를 사용해야 하나요?
---------------------------------

A: Eclipse, IntelliJ IDEA, VS Code 등 원하는 IDE를 사용할 수 있습니다.
이 가이드는 주로 Eclipse를 예로 설명하지만
다른 IDE에서도 마찬가지로 개발할 수 있습니다.

Q: LastaFlute나 DBFlute 지식이 필수인가요?
------------------------------------------

A: 필수는 아니지만 있으면 개발이 원활하게 진행됩니다.
기본적인 사용법은 본 가이드에서도 설명하지만
자세한 내용은 각 프레임워크의 공식 문서를 참조하세요.

Q: 첫 기여는 무엇부터 시작하면 좋을까요?
------------------------------------------------------

A: 다음과 같은 비교적 간단한 작업부터 시작하는 것을 권장합니다:

- 문서 개선
- 테스트 추가
- 버그 수정
- 기존 기능의 작은 개선

자세한 내용은 :doc:`contributing` 을 참조하세요.

관련 리소스
==========

공식 리소스
----------

- `Fess 공식 사이트 <https://fess.codelibs.org/ja/>`__
- `GitHub 리포지토리 <https://github.com/codelibs/fess>`__
- `Issue 트래커 <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__

기술 문서
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

커뮤니티
----------

- `Fess 커뮤니티 포럼 <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__

다음 단계
==========

개발을 시작하려면 :doc:`getting-started` 부터 읽는 것을 권장합니다.

.. toctree::
   :maxdepth: 2
   :caption: 목차:

   getting-started
   setup
   architecture
   workflow
   building
   contributing
