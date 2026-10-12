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
복원 가능한 파일은 \*.bulk와 system.properties입니다.

\*.bulk 안의 문서 중 ``updatedTime`` 이 있는 문서는 저장된 문서가 없거나, ``updatedTime`` 이 없거나,
더 오래된 경우에만 기록됩니다. 더 새롭지 않은 문서는 건너뛰고 ``fess.log`` 에 INFO 수준으로
기록하므로, 복원해도 백업 이후의 변경이 되돌려지지 않고 설치된 버전이 포함하는 예약 작업
(``updatedTime`` 0)도 그대로 유지됩니다. ``updatedTime`` 이 없는 문서는 항상 기록됩니다.

.. note::

   |Fess| 15.9 는 웹 인증과 파일 인증의 ``password`` 를 애플리케이션 암호화 키(``fess_config.properties`` 의
   ``app.cipher.key``)로 암호화하여 저장하므로, ``fess_basic_config.bulk`` 와 ``fess_config.bulk`` 에도 암호화된 값이
   포함됩니다. 백업을 다른 설치에 복원할 때는 동일한 ``app.cipher.key`` 를 이어받으십시오. 키가 다르면 이 인증 정보를
   사용하는 크롤이 오류로 실패합니다. 15.9 이전에 만든 백업에는 평문으로 들어 있으며 그대로 사용할 수 있습니다.

   또한 ``*.bulk`` 에는 이 외의 값이 암호화되지 않은 채 포함되므로, 이 파일들은 기밀 파일로 보관하십시오.

  .. |image0| image:: ../../../resources/images/en/15.9/admin/backup-1.png
