===============
썸네일 이미지 설정
===============

썸네일 이미지 표시
===============

|Fess| 에서는 검색 결과의 썸네일 이미지를 표시할 수 있습니다.
썸네일 이미지는 검색 결과의 MIME Type을 기준으로 생성됩니다.
지원하는 MIME Type이면 검색 결과 표시 시 썸네일 이미지를 생성합니다.
썸네일 이미지를 생성하는 처리는 MIME Type별로 설정하여 추가할 수 있습니다.

썸네일 이미지를 표시하려면 관리자로 로그인하여 전반 설정에서 썸네일 표시를 활성화하고 저장하십시오.

HTML 파일의 썸네일 이미지
======================

HTML의 썸네일 이미지는 HTML 내에서 지정된 이미지 또는 포함된 이미지를 사용합니다.
다음 순서로 썸네일 이미지를 찾아 지정된 경우 표시합니다.

- name 속성이 thumbnail로 지정된 meta 태그의 content 값
- property 속성이 og:image로 지정된 meta 태그의 content 값
- img 태그에서 썸네일에 적합한 크기의 이미지


MS Office 파일의 썸네일 이미지
===========================

MS Office 계열의 썸네일 이미지는 LibreOffice 및 ImageMagick을 사용하여 생성됩니다.
unoconv 및 convert 명령이 설치되어 있으면 썸네일 이미지가 생성됩니다.

패키지 설치
------------------

Redhat 계열 OS의 경우 이미지 생성을 위해 다음 패키지를 설치합니다.

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

생성 스크립트
-----------

RPM/Deb 패키지로 설치하면 MS Office용 썸네일 생성 스크립트는 /usr/share/fess/bin/generate-thumbnail에 설치됩니다.

PDF 파일의 썸네일 이미지
=====================

PDF의 썸네일 이미지는 ImageMagick을 사용하여 생성됩니다.
convert 명령이 설치되어 있으면 썸네일 이미지가 생성됩니다.

썸네일 작업 비활성화
==================

썸네일 작업을 비활성화하는 경우 다음과 같이 설정합니다.

1. 관리 화면의 시스템 > 전반에서 "썸네일 표시" 체크를 해제하고 "업데이트" 버튼을 클릭합니다.
2. ``app/WEB-INF/classes/fess_config.properties`` 또는 ``/etc/fess/fess_config.properties`` 의 ``thumbnail.crawler.enabled`` 에 ``false`` 를 설정합니다.

::

    thumbnail.crawler.enabled=false

3. Fess 서비스를 재시작합니다.
