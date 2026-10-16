===========
문서 리포트
===========

개요
====

문서 리포트는 크롤링한 파일 서버 등을 정리하는 데 도움이 되는 관리 화면입니다. 내용이 같은 문서와 오랫동안 갱신되지 않은 문서를 목록으로 표시하며, 각각 CSV 로 다운로드할 수 있습니다.

화면을 열려면 왼쪽 메뉴의 [시스템 정보 > 문서 리포트] 를 클릭합니다. 열람하려면 ``admin-docreport`` 또는 ``admin-docreport-view`` 역할이 필요합니다. 이 화면은 표시와 다운로드만 하며 문서를 변경하지 않습니다.

두 탭 모두 「URL 접두사」(예: ``smb://server/share/`` )로 대상을 좁힐 수 있습니다.

중복 문서
=========

내용이 같거나 거의 같은 문서를 그룹으로 묶어 문서 수가 많은 순으로 표시합니다.
그룹화에는 색인 시 계산되는 내용 서명( ``content_minhash_bits`` , 검색 결과의 중복 묶기와 같은 것)을 사용하므로 재인덱싱은 필요하지 않습니다.
내용에 단어가 없는 문서(빈 파일 등)는 대상에서 제외됩니다.

화면에는 최대 ``docreport.duplicate.group.size`` (기본값: 100)개 그룹을 표시하고, 각 그룹의 문서는 ``docreport.duplicate.docs.size`` (기본값: 10)건까지 표시합니다. 모든 그룹은 [CSV 다운로드] 로 가져올 수 있습니다. CSV 는 큰 인덱스에서도 모든 그룹을 읽어 들이며 ``group, groupSize, url, title, filename, contentLength, lastModified, owner, lastModifier, clickCount, docId`` 열을 출력합니다.

.. note::

   중복 문서 리포트에는 내용 서명이 필요한데, CodeLibs 플러그인이 없는 OpenSearch 용 인덱스 정의(``search_engine.type`` 이 ``vanilla``, ``aws``, 사용 중단 예정인 ``cloud`` 인 경우)에서는 서명이 계산되지 않습니다. 이러한 종류에서는 「중복 문서」 탭이 표시되지 않으며 「휴면 문서」만 사용할 수 있습니다. 자세한 내용은 :doc:`../config/search-engine-type` 을 참조하십시오.

휴면 문서
=========

최종 갱신 일시가 지정한 일수(「미갱신 일수」, 기본값은 ``docreport.dormant.days`` 의 365)보다 이전인 문서를 오래된 순으로 표시합니다. 최종 갱신 일시가 없는 문서는 표시하지 않습니다.
「검색 결과에서 한 번도 열리지 않음」을 활성화하면 검색 결과에서 클릭된 적이 있는 문서를 제외합니다.

화면에는 해당 문서의 건수와 합계 크기, 문서 목록을 표시합니다. 목록의 페이지 이동에는 상한( ``indexer.max.result.window.size`` )이 있으며, 이를 넘는 문서는 [CSV 다운로드] 로 가져옵니다.

설정
====

``fess_config.properties`` 의 다음 설정으로 동작을 조정할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 45 15

   * - 속성
     - 설명
     - 기본값
   * - ``docreport.duplicate.group.size``
     - 화면에 표시하는 중복 그룹의 최대 수
     - ``100``
   * - ``docreport.duplicate.docs.size``
     - 화면에서 그룹 하나에 표시하는 문서의 최대 수
     - ``10``
   * - ``docreport.duplicate.export.page.size``
     - CSV 다운로드 시 한 번에 읽어 들이는 서명의 수
     - ``10000``
   * - ``docreport.dormant.days``
     - 휴면 문서로 간주하는, 최종 갱신 이후 일수의 기본값
     - ``365``
