=========
유지보수
=========

개요
====

유지보수 페이지는 시스템의 데이터 조작을 실행할 때 사용합니다.

|image0|

작업 방법
======

재인덱싱
------------

기존 fess 인덱스에서 새 인덱스를 재생성할 수 있습니다.
인덱스의 매핑을 변경하고 싶은 경우 등에 실행합니다.


설정 항목
------

별칭 업데이트
::::::::::::

활성화하면 재인덱싱이 완료된 후 기존 인덱스에 할당된 fess.search와 fess.update 별칭을 새 인덱스로 변경할 수 있습니다.


사전 초기화
:::::::::

활성화하면 사전 설정을 초기화할 수 있습니다.

``search_engine.type`` 이 ``vanilla`` 또는 ``aws`` 이면 이 항목은 표시되지 않습니다.


샤드 수
::::::::

OpenSearch의 샤드 수(index.number_of_shards)를 지정할 수 있습니다.


최대 복제본 수
:::::::::::

OpenSearch의 최대 복제본 수(index.auto_expand_replicas)를 지정할 수 있습니다.


설정 인덱스 재구축
--------------------------

설정 인덱스(fess_config, fess_user, fess_log)를 최신 매핑으로 재구축할 수 있습니다.
이 작업은 백그라운드에서 실행됩니다. 실행하기 전에 설정의 백업 등을 수행해 주십시오.


대상 인덱스
::::::::::::

재구축할 인덱스를 선택합니다. fess_config, fess_user, fess_log에서 선택할 수 있습니다.


기본 데이터 불러오기
::::::::::::::::

활성화하면 재구축 시 기본 데이터를 불러옵니다. 기존 문서는 덮어쓰지 않습니다.


문서 인덱스 리로드
--------------------------

인덱스 설정을 반영하기 위해 문서 인덱스를 리로드할 수 있습니다.
사전 변경을 검색에 반영할 때도 사용합니다. 저장된 사전을 OpenSearch 의 파일에 기록한 다음
``fess.update`` 별칭이 가리키는 인덱스를 close 하고 open 합니다. close 하는 동안에는 그 인덱스를
검색할 수 없습니다. 자세한 내용은 :ref:`dict-apply-changes` 를 참조하십시오.

``search_engine.type`` 이 ``vanilla`` 또는 ``aws`` 이면 이 기능은 표시되지 않습니다.


Crawler 인덱스
----------------

fess_crawler 인덱스(크롤링 정보)를 삭제할 수 있습니다.
크롤러 실행 중에는 실행하지 마십시오.


진단
----

진단용 zip 파일을 다운로드할 수 있습니다. zip 의 ``log<yyyyMMddHHmm>/`` 디렉터리 아래에 다음 파일이 들어 있습니다.

- 로그 디렉터리의 ``*.log`` 와 ``*.log.gz`` (``fess.log`` , ``fess-crawler.log`` , ``audit.log`` , ``searchlog.log`` 등)
- ``system.properties`` (시스템 설정)와 ``fess_config.properties`` (애플리케이션 설정)
- ``fess_basic_config.bulk`` (크롤링 설정, 인증 설정, 라벨 등 설정 인덱스의 내용. 관리 API의 액세스 토큰은 포함되지 않습니다)
- ``es_cat_*.txt`` 와 ``es_*.json`` (OpenSearch ``_cat`` API의 출력과 클러스터, 노드, 태스크 등의 상태)

``system.properties`` 와 ``fess_config.properties`` 에서는 시스템 정보 화면과 같은 규칙으로 비밀 값을 ``XXXXXXXX`` 로 바꿉니다. 스토리지 비밀 키, Webhook URL(Slack, Google Chat), SSO 클라이언트 시크릿, LLM 및 임베딩 API 키, 애플리케이션 암호화 키(``app.cipher.key``) 등이 대상입니다. 키는 남으므로 어떤 설정이 있는지는 알 수 있습니다.

.. note::

   로그 파일과 ``fess_basic_config.bulk`` 의 내용은 마스킹되지 않습니다. zip을 외부로 보내기 전에 내용을 확인하십시오.

.. |image0| image:: ../../../resources/images/en/15.9/admin/maintenance-1.png
