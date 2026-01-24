===========
대시보드
===========

개요
====

대시보드에서는 |Fess| 가 액세스하는 OpenSearch 클러스터와 인덱스를 관리하는 웹 관리 도구를 제공합니다.

|image0|

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table:: |Fess| 가 관리하는 인덱스
   :header-rows: 1

   * - 인덱스명
     - 설명
   * - fess.YYYYMMDD
     - 인덱싱된 문서
   * - fess_log
     - 액세스 로그
   * - fess.suggest.YYYYMMDD
     - 제안 키워드
   * - fess_config
     - |Fess| 의 설정
   * - fess_user
     - 사용자/역할/그룹 데이터
   * - configsync
     - 사전 설정
   * - fess_suggest
     - 제안 메타데이터
   * - fess_suggest_array
     - 제안 메타데이터
   * - fess_suggest_badword
     - 제안 금지어 목록
   * - fess_suggest_analyzer
     - 제안 메타데이터
   * - fess_crawler
     - 크롤 정보


점(.)으로 시작하는 인덱스명은 시스템용 인덱스이므로 표시되지 않습니다.
시스템용 인덱스도 표시하려면 special 체크박스를 활성화하십시오.

인덱싱된 문서 수 확인
================================

인덱싱된 문서의 수는 아래 그림과 같이 fess인덱스에 표시됩니다.

|image1|

각 인덱스의 오른쪽 상단 아이콘을 클릭하면 인덱스에 대한 작업 메뉴가 표시됩니다.
인덱싱된 문서를 삭제하는 경우 관리용 검색 화면에서 삭제합니다. "delete index"로 삭제하지 않도록 주의하십시오.

.. |image0| image:: ../../../resources/images/en/15.5/admin/dashboard-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/dashboard-2.png
.. pdf            :width: 400 px
