===========
실천 가이드
===========

Fess로 실현하는 지식 활용
=========================

사내 정보를 Fess로 검색할 수 있게 하고, 계속 사용되는 검색 기반으로 키워 나가기 위한 실천 가이드입니다.
각 글은 Fess 15.9를 대상으로, 설정 화면의 항목과 설정 키, 제대로 되었는지 확인하는 방법까지 구체적으로 설명합니다.
15.10 이후에서만 사용할 수 있는 기능은 글 안에 그 사실을 명시합니다.

목적별로 고르기
===============

- **우선 시험해 보고 싶다**: :doc:`articles/guide-01` → :doc:`articles/guide-02`
- **파일 서버를 검색하고 싶다**: :doc:`articles/file-server-search` → :doc:`articles/guide-04` → :doc:`articles/guide-05`
- **클라우드나 SaaS의 데이터를 검색하고 싶다**: :doc:`articles/datastore-basics` → :doc:`articles/guide-07` / :doc:`articles/guide-06` / :doc:`articles/guide-12`
- **기존 사이트나 시스템에 검색을 넣고 싶다**: :doc:`articles/guide-03` → :doc:`articles/guide-11`
- **부서나 사용자별로 보여 줄 정보를 나누고 싶다**: :doc:`articles/guide-05` → :doc:`articles/guide-15` → :doc:`articles/guide-13`
- **AI로 검색을 강화하고 싶다**: :doc:`articles/guide-18` → :doc:`articles/guide-19` → :doc:`articles/guide-20`
- **운영 환경에서 사용을 시작한다**: :doc:`articles/guide-10` → :doc:`articles/guide-16` → :doc:`articles/guide-14`

시작하기
========

- :doc:`articles/guide-01` - Fess의 구성, 본체와 플러그인의 역할 분담, 목적별로 읽어 나가는 순서
- :doc:`articles/guide-02` - Docker Compose로 Fess를 기동하고, 크롤링부터 검색까지 한 차례 시험해 본다

정보 수집하기
=============

- :doc:`articles/guide-04` - 웹 사이트와 파일 서버를 크롤링하고, 라벨로 범위를 좁힐 수 있게 한다
- :doc:`articles/datastore-basics` - 데이터 저장소 플러그인의 설정 항목, 권한, 라벨, 스케줄, 결과 확인 방법
- :doc:`articles/guide-07` - Google Drive, SharePoint Online / OneDrive, Box의 파일을 검색 대상으로 한다
- :doc:`articles/guide-06` - Git 리포지토리, Confluence, Jira, Slack의 정보를 검색 대상으로 한다
- :doc:`articles/guide-12` - 데이터베이스, CSV 파일, Salesforce의 데이터를 검색 대상으로 한다

검색 넣기·보여 주는 방식 바꾸기
===============================

- :doc:`articles/guide-03` - 기존 사이트에 검색창을 두고, 테마로 검색 화면의 모양을 다듬는다
- :doc:`articles/guide-11` - 검색 API와 액세스 토큰을 사용해 업무 시스템에서 검색하고 등록한다

접근 제어하기
=============

- :doc:`articles/guide-05` - 역할과 그룹으로 검색 결과를 나누어 보여 주고, LDAP / Active Directory와 연동한다
- :doc:`articles/guide-15` - SSO(OIDC / SAML / Entra ID / SPNEGO)를 도입하고, 외부로부터의 접근을 보호한다
- :doc:`articles/guide-13` - 가상 호스트와 역할로 하나의 Fess를 여러 조직이 나누어 사용한다

검색 품질 높이기
================

- :doc:`articles/guide-08` - 검색 로그 분석 화면에서 과제를 찾아, 동의어나 키 매치로 개선한다
- :doc:`articles/guide-09` - 다국어 문서가 어떻게 색인되고 검색되는지 이해하고, 언어별로 조정한다
- :doc:`articles/guide-22` - OpenSearch Dashboards로 검색 로그를 독자적으로 집계하고 시각화한다

운영하기
========

- :doc:`articles/guide-10` - 헬스 체크, 로그, 알림, 백업과 복원, 장애 URL 처리
- :doc:`articles/guide-16` - fessctl과 관리 API로 설정을 코드로 관리하고, 환경을 재현한다
- :doc:`articles/guide-14` - 메모리 설정, 외부 OpenSearch 클러스터, Fess 다중 서버 구성
- :doc:`articles/guide-17` - 데이터 저장소 플러그인이나 인제스터를 직접 만들어 기능을 추가한다

AI로 검색 강화하기
==================

- :doc:`articles/guide-18` - 벡터 검색과 랭크 융합으로, 표현이 달라도 찾을 수 있는 검색을 만든다
- :doc:`articles/guide-19` - LLM을 연결하고, 사내 문서를 근거로 답변하는 AI 검색 모드를 사용한다
- :doc:`articles/guide-20` - MCP 서버 플러그인으로 AI 에이전트가 Fess를 검색하게 한다
- :doc:`articles/guide-21` - 이미지와 텍스트를 함께 검색할 수 있는 멀티모달 검색을 구축한다

전사 확대 계획하기
==================

- :doc:`articles/guide-23` - 도입부터 전사 확대까지 단계별로 설정하고 확인해야 할 항목을 정리한다

유스케이스·비교
===============

- :doc:`articles/use-cases` - 업종별·규모별 활용 사례와 각각에 도움이 되는 글
- :doc:`articles/comparison` - Fess와 다른 검색 솔루션(OpenSearch 단독, Solr, 상용 제품 등)의 비교
- :doc:`articles/file-server-search` - 파일 서버 전문 검색을 도입하기 전에 확인해야 할 점

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-04
   articles/datastore-basics
   articles/guide-07
   articles/guide-06
   articles/guide-12
   articles/guide-03
   articles/guide-11
   articles/guide-05
   articles/guide-15
   articles/guide-13
   articles/guide-08
   articles/guide-09
   articles/guide-22
   articles/guide-10
   articles/guide-16
   articles/guide-14
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-23
   articles/use-cases
   articles/comparison
   articles/file-server-search
