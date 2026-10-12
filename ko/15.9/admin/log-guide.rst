=========
로그 파일
=========

개요
====

여기서는 |Fess| 에서 출력되는 로그 파일의 다운로드에 대해 설명합니다.

설정 방법
======

표시 방법
------

아래 그림의 로그 파일 페이지를 열려면 왼쪽 메뉴의 [시스템 정보 > 로그 파일]을 클릭합니다.

|image0|

다운로드
---------

표시된 로그 파일 이름을 클릭하면 로그 파일을 다운로드할 수 있습니다.

``server_*.log``
::::::::::::::::

|Fess| 의 애플리케이션 서버로서의 로그가 기록됩니다.

fess.log
::::::::

|Fess| 의 애플리케이션으로서의 로그가 기록됩니다.

fess-crawler.log
::::::::::::::::

크롤러의 로그가 기록됩니다.

audit.log
:::::::::

로그인 정보 및 관리 화면의 액세스 로그가 기록됩니다.

fess-thumbnail.log
::::::::::::::::::

썸네일 기능의 로그가 기록됩니다.

fess-suggest.log
::::::::::::::::

추천 기능의 로그가 기록됩니다.

fess-urls.log
:::::::::::::

하나의 크롤링에 걸린 시간이 기록됩니다.

searchlog.log
:::::::::::::

검색 로그가 기록됩니다.
[시스템 > 일반] 의 「검색 로그」가 활성화되어 있으면, 기본 설정에서는 검색할 때마다 1행(JSON)이 추가됩니다.
1행에는 그 검색이 반환한 문서의 필드(``logging.search.docs.fields`` )가 포함되므로, 크기는 반환한 건수에 따라 커집니다(``num=100`` 에서는 1행이 70 KB 정도가 되는 예가 있습니다).
로그 로테이션과 보존 기간은 :doc:`../config/admin-logging` 을 참조하십시오.
반환한 문서의 필드를 검색 로그에 포함하지 않으려면 ``fess_config.properties`` 에서 ``logging.search.docs.enabled=false`` 를, 이 파일에 출력하지 않으려면 ``logging.search.use.logfile=false`` 를 설정합니다.

gc-crawler.log
::::::::::::::

크롤러 프로세스의 GC 로그가 기록되어 있습니다(기본 「Default Crawler」 작업이 출력합니다).

gc-fess.log
:::::::::::

|Fess| 본체의 GC 로그가 기록되어 있습니다. 환경 변수 ``FESS_USE_GC_LOGGING`` 에 비어 있지 않은 값을 설정한 경우에만 출력됩니다(:doc:`../install/run` 참조).

.. |image0| image:: ../../../resources/images/en/15.9/admin/log-1.png
