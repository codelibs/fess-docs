===================================
오픈소스 전문 검색 서버 Fess
===================================

개요
====

Fess (페스)는 "\ **5분 만에 간단히 구축 가능한 전문 검색 서버**\ "입니다.

.. figure:: ../resources/images/en/demo-1.png
   :scale: 100%
   :alt: 표준 데모
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   표준 데모

.. figure:: ../resources/images/en/demo-3.png
   :scale: 100%
   :alt: 사이트 내 검색 데모
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   사이트 내 검색 데모

.. figure:: ../resources/images/en/demo-2.png
   :scale: 100%
   :alt: Code Search
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   소스 코드 검색

.. figure:: ../resources/images/en/demo-4.png
   :scale: 100%
   :alt: Document Search
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   문서 검색

Java 또는 Docker 실행 환경이 있으면 어떤 OS에서도 실행 가능합니다.
Fess는 Apache 라이센스로 제공되며, 무료(프리 소프트웨어)로 이용하실 수 있습니다.


다운로드
============

- :doc:`Fess 15.3.0 <downloads>` (zip/rpm/deb 패키지)

특징
====

-  Apache 라이센스로 제공 (프리 소프트웨어로 무료 이용 가능)

-  웹, 파일 시스템, Windows 공유 폴더, 데이터베이스를 크롤

-  MS Office(Word/Excel/PowerPoint) 및 PDF 등 다양한 파일 형식 지원

-  OS 독립적 (Java 기반 구축)

-  기존 사이트 통합용 JavaScript 제공

-  OpenSearch 또는 Elasticsearch를 검색 엔진으로 이용

-  BASIC/DIGEST/NTLM/FORM 인증 사이트도 검색 가능

-  로그인 상태에 따른 검색 결과 분류 가능

-  ActiveDirectory나 SAML 등을 이용한 싱글 사인온(SSO)

-  지도 정보와 연계한 위치 정보 검색

-  브라우저에서 크롤 대상 설정 및 검색 화면 편집 등 가능

-  검색 결과를 라벨로 분류

-  리퀘스트 헤더에 정보 추가, 중복 도메인 설정, 검색 결과 경로 변환

-  JSON 형식 검색 결과 출력으로 외부 시스템 연계 가능

-  검색 로그 및 클릭 로그 집계

-  패싯 · 드릴다운 지원

-  자동 완성 · 제안 기능

-  사용자 사전 및 동의어 사전 편집 기능

-  검색 결과 캐시 표시 기능 및 썸네일 표시 기능

-  검색 결과 프록시 기능

-  스마트폰 지원 (Responsive Web Design)

-  액세스 토큰으로 외부 시스템 연계

-  OCR 등 외부 텍스트 추출 지원

-  용도에 맞게 유연하게 대응 가능한 설계

뉴스
========

2025-10-25
    `Fess 15.3.0 릴리스 <https://github.com/codelibs/fess/releases/tag/fess-15.3.0>`__

2025-09-04
    `Fess 15.2.0 릴리스 <https://github.com/codelibs/fess/releases/tag/fess-15.2.0>`__

2025-07-20
    `Fess 15.1.0 릴리스 <https://github.com/codelibs/fess/releases/tag/fess-15.1.0>`__

2025-06-22
    `Fess 15.0.0 릴리스 <https://github.com/codelibs/fess/releases/tag/fess-15.0.0>`__

2025-05-24
    `Fess 14.19.2 릴리스 <https://github.com/codelibs/fess/releases/tag/fess-14.19.2>`__

과거 뉴스는 :doc:`여기 <news>` 를 참조하세요.

포럼
==========

질문이 있으시면 `포럼 <https://discuss.codelibs.org/c/FessJA/>`__ 을 이용하세요.

상용 지원
============

Fess는 Apache 라이센스로 제공되는 오픈소스 제품으로, 개인 및 상용 용도로 무료로 자유롭게 이용하실 수 있습니다.

Fess의 커스터마이즈 및 도입·구축 등의 지원 서비스가 필요한 경우 \ `상용 지원(유상) <https://www.n2sm.net/products/n2search.html>`__\ 을 참조하세요.
또한, 검색 품질 및 크롤 속도 개선 등의 성능 튜닝도 상용 지원으로 대응하고 있습니다.

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (최적화된 Fess의 상용 패키지)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (Google Site Search 대체 서비스)

- :doc:`각종 지원 서비스 <support-services>`


Fess Site Search
================

CodeLibs 프로젝트에서는 `Fess Site Search(FSS) <https://fss-generator.codelibs.org/ja/>`__ 를 제공하고 있습니다.
기존 사이트에 JavaScript를 배치하는 것만으로 Fess의 검색 페이지를 통합할 수 있습니다.
FSS를 이용하면 Google Site Search나 Yahoo! 검색 커스텀 서치로부터의 이전도 간단하게 할 수 있습니다.
저렴한 Fess 서버가 필요한 경우 `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ 를 참조하세요.

Data Store 플러그인
====================

- `Confluence/Jira <https://github.com/codelibs/fess-ds-atlassian>`__
- `Box <https://github.com/codelibs/fess-ds-box>`__
- `CSV <https://github.com/codelibs/fess-ds-csv>`__
- `Database <https://github.com/codelibs/fess-ds-db>`__
- `Dropbox <https://github.com/codelibs/fess-ds-dropbox>`__
- `Elasticsearch <https://github.com/codelibs/fess-ds-elasticsearch>`__
- `Git <https://github.com/codelibs/fess-ds-git>`__
- `Gitbucket <https://github.com/codelibs/fess-ds-gitbucket>`__
- `G Suite <https://github.com/codelibs/fess-ds-gsuite>`__
- `JSON <https://github.com/codelibs/fess-ds-json>`__
- `Office 365 <https://github.com/codelibs/fess-ds-office365>`__
- `S3 <https://github.com/codelibs/fess-ds-s3>`__
- `Salesforce <https://github.com/codelibs/fess-ds-salesforce>`__
- `SharePoint <https://github.com/codelibs/fess-ds-sharepoint>`__
- `Slack <https://github.com/codelibs/fess-ds-slack>`__

Theme 플러그인
===============

- `Simple <https://github.com/codelibs/fess-theme-simple>`__
- `Classic <https://github.com/codelibs/fess-theme-classic>`__

Ingester 플러그인
==================

- `Logger <https://github.com/codelibs/fess-ingest-logger>`__
- `NDJSON <https://github.com/codelibs/fess-ingest-ndjson>`__

Script 플러그인
==================

- `Groovy <https://github.com/codelibs/fess-script-groovy>`__
- `OGNL <https://github.com/codelibs/fess-script-ognl>`__

관련 프로젝트
================

- `Code Search <https://github.com/codelibs/docker-codesearch>`__
- `Document Search <https://github.com/codelibs/docker-docsearch>`__
- `Fione <https://github.com/codelibs/docker-fione>`__
- `Form Assist <https://github.com/codelibs/docker-formassist>`__

게재 미디어
============

- `【제48회】SAML에 의한 싱글 사인온 <https://news.mynavi.jp/techplus/article/_ossfess-48/>`__

- `【제47회】MinIO로 스토리지 관리 및 크롤 <https://news.mynavi.jp/techplus/article/_ossfess-47/>`__

- `【제46회】Amazon S3 크롤 <https://news.mynavi.jp/techplus/article/_ossfess-46/>`__

- `【제45회】Compose V2에서의 시작 방법 <https://news.mynavi.jp/techplus/article/_ossfess-45/>`__

- `【제44회】Fess에서 OpenSearch 사용 <https://news.mynavi.jp/techplus/article/_ossfess-44/>`__

- `【제43회】Elasticsearch 8 이용 방법 <https://news.mynavi.jp/techplus/article/_ossfess-43/>`__

- `【제42회】액세스 토큰을 사용한 검색 API 이용 방법 <https://news.mynavi.jp/techplus/article/_ossfess-42/>`__

- `【제41회】Microsoft Teams 크롤 <https://news.mynavi.jp/itsearch/article/bizapp/5880>`__

- `【제40회】각종 기능 설정 방법 (문서 부스트, 관련 콘텐츠, 관련 쿼리) <https://news.mynavi.jp/itsearch/article/bizapp/5804>`__

- `【제39회】각종 기능 설정 방법 (경로 매핑, 리퀘스트 헤더, 중복 호스트) <https://news.mynavi.jp/itsearch/article/bizapp/5686>`__

- `【제38회】각종 기능 설정 방법 (라벨, 키 매치) <https://news.mynavi.jp/itsearch/article/bizapp/5646>`__

- `【제37회】AWS Elasticsearch Service 이용 방법 <https://news.mynavi.jp/itsearch/article/devsoft/5557>`__

- `【제36회】Elastic Cloud 이용 방법 <https://news.mynavi.jp/itsearch/article/devsoft/5507>`__

- `【제35회】SharePoint Server 크롤 <https://news.mynavi.jp/itsearch/article/devsoft/5457>`__

- `【제34회】OpenID Connect 인증 방법 <https://news.mynavi.jp/itsearch/article/devsoft/5338>`__

- `【제33회】입력 지원 환경 구축 방법 <https://news.mynavi.jp/itsearch/article/devsoft/5292>`__

- `【제32회】인덱스 관리 <https://news.mynavi.jp/itsearch/article/devsoft/5233>`__

- `【제31회】Office 365 크롤 <https://news.mynavi.jp/itsearch/article/bizapp/5180>`__

- `【제30회】Azure AD 인증 방법 <https://news.mynavi.jp/itsearch/article/bizapp/5136>`__

- `【제29회】Docker 사용법 <https://news.mynavi.jp/itsearch/article/devsoft/5058>`__

- `【제28회】로그 파일 참조 방법 <https://news.mynavi.jp/itsearch/article/devsoft/5032>`__

- `【제27회】Fess 클러스터화 <https://news.mynavi.jp/itsearch/article/devsoft/4994>`__

- `【제26회】위치 정보 검색 <https://news.mynavi.jp/itsearch/article/devsoft/4963>`__

- `【제25회】Tesseract OCR 이용 <https://news.mynavi.jp/itsearch/article/devsoft/4928>`__

- `【제24회】GitBucket 크롤 <https://news.mynavi.jp/itsearch/article/devsoft/4924>`__

- `【제23회】제안 기능 사용법 <https://news.mynavi.jp/itsearch/article/bizapp/4890>`__

- `【제22회】Dropbox 크롤 <https://news.mynavi.jp/itsearch/article/bizapp/4844>`__

- `【제21회】Slack 메시지 크롤 <https://news.mynavi.jp/itsearch/article/bizapp/4808>`__

- `【제20회】검색 로그 시각화 <https://news.mynavi.jp/itsearch/article/devsoft/4781>`__

- `【제19회】CSV 파일 크롤 <https://news.mynavi.jp/itsearch/article/devsoft/4761>`__

- `【제18회】Google Drive 크롤 <https://news.mynavi.jp/itsearch/article/devsoft/4732>`__

- `【제17회】데이터베이스 크롤 <https://news.mynavi.jp/itsearch/article/devsoft/4659>`__

- `【제16회】검색 API 이용 방법 <https://news.mynavi.jp/itsearch/article/devsoft/4613>`__

- `【제15회】인증이 필요한 파일 서버 크롤 <https://news.mynavi.jp/itsearch/article/devsoft/4569>`__

- `【제14회】관리 API 사용법 <https://news.mynavi.jp/itsearch/article/devsoft/4514>`__

- `【제13회】검색 결과에 썸네일 이미지 표시 방법 <https://news.mynavi.jp/itsearch/article/devsoft/4456>`__

- `【제12회】가상 호스트 기능 사용법 <https://news.mynavi.jp/itsearch/article/devsoft/4394>`__

- `【제11회】Fess로 싱글 사인온 <https://news.mynavi.jp/itsearch/article/devsoft/4357>`__

- `【제10회】Windows 환경 구축 방법 <https://news.mynavi.jp/itsearch/article/bizapp/4320>`__

- `【제9회】Fess에서 Active Directory 연계 <https://news.mynavi.jp/itsearch/article/bizapp/4283>`__

- `【제8회】롤 기반 검색 <https://news.mynavi.jp/itsearch/article/hardware/4201>`__

- `【제7회】인증이 있는 사이트 크롤 <https://news.mynavi.jp/itsearch/article/hardware/4158>`__

- `【제6회】일본어 전문 검색에서의 Analyzer <https://news.mynavi.jp/itsearch/article/devsoft/3671>`__

- `【제5회】전문 검색의 토큰화 처리 <https://news.mynavi.jp/itsearch/article/devsoft/3539>`__

- `【제4회】Fess를 사용한 자연어 처리 <https://news.mynavi.jp/itsearch/article/bizapp/3445>`__

- `【제3회】설정만으로 할 수 있는 웹 스크래핑 <https://news.mynavi.jp/itsearch/article/bizapp/3341>`__

- `【제2회】Google Site Search로부터 간단 이전 <https://news.mynavi.jp/itsearch/article/bizapp/3260>`__

- `【제1회】전문 검색 서버 Fess 도입 <https://news.mynavi.jp/itsearch/article/bizapp/3154>`__

.. |image0| image:: ../resources/images/en/demo-1.png
.. |image1| image:: ../resources/images/en/demo-2.png
.. |image2| image:: ../resources/images/en/demo-3.png
.. |image3| image:: ../resources/images/en/n2search_225x50.png
   :target: https://www.n2sm.net/products/n2search.html
.. |image4| image:: ../resources/images/en/n2search_b.png


.. toctree::
   :hidden:

   overview
   basic
   documentation
   tutorial
   development
   others
   archives

