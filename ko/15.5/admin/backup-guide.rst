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

fess_config.bulk
::::::::::::::::

fess_config.bulk는 |Fess| 의 설정 정보를 포함하고 있습니다.

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk는 장애 URL을 제외한 |Fess| 의 설정 정보를 포함하고 있습니다.

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
복원 가능한 파일은 \*.bulk와 system.properties입니다.

  .. |image0| image:: ../../../resources/images/en/15.5/admin/backup-1.png
