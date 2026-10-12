=========
백업
=========

개요
====

백업 페이지에서는 |Fess| 의 설정 정보를 다운로드하고 업로드할 수 있습니다.

다운로드
---------

|Fess| 는 설정 정보를 인덱스로 보유하고 있습니다.
다운로드하려면 인덱스 이름을 클릭하십시오.

|image0|

.. note::

   사전(동의어, 불용어 등) 파일은 백업 대상에 포함되지 않습니다.
   사전 파일은 검색 엔진의 사전 디렉터리(``FESS_DICTIONARY_PATH``)에 저장되어 있으므로,
   필요하면 별도로 복사하십시오.

fess_config.bulk
::::::::::::::::

fess_config.bulk는 |Fess| 의 설정 정보를 포함하고 있습니다.

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk는 크롤링 정보, 장애 URL, 작업 로그, 썸네일 큐, 사용자 태그 등을 제외한 |Fess| 의 설정 정보를 포함하고 있습니다.

fess_user.bulk
::::::::::::::

fess_user.bulk는 사용자, 역할 및 그룹 정보를 포함합니다.

system.properties
:::::::::::::::::

system.properties는 전체 설정 정보를 포함합니다.

fess.json
:::::::::

fess.json은 fess 인덱스의 설정 정보를 포함합니다.

doc.json
::::::::

doc.json은 fess 인덱스의 매핑 정보를 포함합니다.

chat_log.ndjson
:::::::::::::::

chat_log.ndjson은 AI 채팅 이용 로그 정보를 포함합니다.

click_log.ndjson
::::::::::::::::

click_log.ndjson은 클릭 로그 정보를 포함합니다.

favorite_log.ndjson
:::::::::::::::::::

favorite_log.ndjson은 즐겨찾기 로그 정보를 포함합니다.

search_log.ndjson
:::::::::::::::::

search_log.ndjson은 검색 로그 정보를 포함합니다.

user_info.ndjson
::::::::::::::::

user_info.ndjson은 검색 사용자 정보를 포함합니다.

업로드
---------

설정 정보를 업로드하여 가져올 수 있습니다.
복원 가능한 파일은 다음과 같습니다.

- ``*.bulk``
- ``system.properties``
- ``fess.json`` , ``doc.json``: |Fess| 가 사용하는 인덱스 정의 파일을 교체합니다. 기존 인덱스의 설정이나 매핑은 그 자리에서 변경되지 않습니다.
- ``gsa*.xml``: Google Search Appliance 의 설정 파일입니다. 웹 크롤링 설정, 파일 크롤링 설정, 레이블로 가져옵니다.

``*.ndjson`` (검색 로그 등의 로그)은 업로드하여 복원할 수 없습니다.

\*.bulk 안의 문서 중 ``updatedTime`` 이 있는 문서는 저장된 문서가 없거나, ``updatedTime`` 이 없거나,
더 오래된 경우에만 기록됩니다. 더 새롭지 않은 문서는 건너뛰고 ``fess.log`` 에 INFO 수준으로
기록하므로, 복원해도 백업 이후의 변경이 되돌려지지 않고 설치된 버전이 포함하는 예약 작업
(``updatedTime`` 0)도 그대로 유지됩니다. ``updatedTime`` 이 없는 문서는 항상 기록됩니다.

  .. |image0| image:: ../../../resources/images/en/15.9/admin/backup-1.png
