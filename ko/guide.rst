============================================
실천 가이드
============================================

Fess로 실현하는 지식 활용 전략
================================

목표 지향으로 배우는 엔터프라이즈 검색 실천 가이드.
유스케이스 기점으로, Fess의 도입부터 AI 활용까지를 전 23회로 해설합니다.

**기초편 (초보자용)**

- :doc:`articles/guide-01` - 기업에서 정보 검색이 필요한 이유와 분산된 정보 활용의 과제를 해설
- :doc:`articles/guide-02` - Docker Compose로 수분 만에 Fess를 기동하고 검색을 체험하는 퀵스타트
- :doc:`articles/guide-03` - 기존 웹사이트에 검색 위젯을 임베딩하는 3가지 패턴 소개
- :doc:`articles/guide-04` - 파일 서버와 클라우드 스토리지 등 복수 소스의 횡단 검색 구축
- :doc:`articles/guide-05` - 역할과 라벨을 사용한 부서별·권한별 검색 결과 필터링

**실전 솔루션편 (중급자용)**

- :doc:`articles/guide-06` - Git·Wiki·티켓 등 개발 관련 지식을 통합 검색하는 환경 구축
- :doc:`articles/guide-07` - Google Drive·SharePoint·Box를 통합 검색하는 설정과 운용
- :doc:`articles/guide-08` - 검색 로그 분석에 기반한 튜닝 개선 사이클 실천
- :doc:`articles/guide-09` - 일본어·영어·중국어 문서를 올바르게 검색하는 분석기 설정
- :doc:`articles/guide-10` - 운영 환경의 모니터링·백업·장애 대책 모범 사례
- :doc:`articles/guide-11` - REST API를 사용한 CRM·사내 시스템과의 연계 패턴집
- :doc:`articles/guide-12` - Salesforce·데이터베이스 등 SaaS 데이터의 인덱싱 절차

**아키텍처·스케일링편 (상급자용)**

- :doc:`articles/guide-13` - 하나의 Fess 인스턴스로 여러 조직에 서비스하는 테넌트 설계
- :doc:`articles/guide-14` - 싱글 서버에서 클러스터 구성으로의 단계적 스케일링 전략
- :doc:`articles/guide-15` - SSO(OIDC/SAML) 연계와 제로 트러스트 환경에서의 접근 제어 설계
- :doc:`articles/guide-16` - Fess 설정의 코드 관리와 CI/CD 파이프라인에 의한 배포 자동화
- :doc:`articles/guide-17` - 커스텀 데이터소스 플러그인과 Ingest 파이프라인의 구현 방법

**AI·차세대 검색편 (상급자용)**

- :doc:`articles/guide-18` - 키워드 검색에서 벡터 검색·시맨틱 검색으로의 진화를 개설
- :doc:`articles/guide-19` - RAG를 활용한 사내 문서 기반 질의응답 시스템 구축 절차
- :doc:`articles/guide-20` - MCP 서버로서 Fess를 Claude 등 외부 AI 도구와 통합
- :doc:`articles/guide-21` - 벡터 임베딩을 통한 텍스트·이미지의 횡단 멀티모달 검색
- :doc:`articles/guide-22` - 검색 로그를 OpenSearch Dashboards로 시각화하여 정보 활용을 분석

**총괄**

- :doc:`articles/guide-23` - 전 23회의 요소를 통합한 전사 지식 기반의 레퍼런스 아키텍처

활용 사례 및 비교
==================

- :doc:`articles/use-cases` - 업종별, 규모별 활용 사례
- :doc:`articles/comparison` - Fess와 다른 검색 솔루션 비교 (Elasticsearch, Solr 등)

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-03
   articles/guide-04
   articles/guide-05
   articles/guide-06
   articles/guide-07
   articles/guide-08
   articles/guide-09
   articles/guide-10
   articles/guide-11
   articles/guide-12
   articles/guide-13
   articles/guide-14
   articles/guide-15
   articles/guide-16
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-22
   articles/guide-23
   articles/use-cases
   articles/comparison
