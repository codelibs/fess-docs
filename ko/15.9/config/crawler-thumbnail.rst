=======================
썸네일 이미지 설정
=======================

개요
====

|Fess| 에서는 검색 결과의 썸네일 이미지를 표시할 수 있습니다.
썸네일 이미지는 검색 결과의 MIME Type을 기준으로 생성됩니다.
지원하는 MIME Type이면 검색 결과 표시 시 썸네일 이미지를 생성합니다.
썸네일 이미지를 생성하는 처리는 MIME Type별로 설정하여 추가할 수 있습니다.

썸네일 이미지를 표시하려면 관리자로 로그인하여 전반 설정에서 썸네일 표시를 활성화하고 저장하십시오.

지원하는 파일 형식
==================

이미지 파일
-----------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - 형식
     - MIME 타입
     - 설명
   * - JPEG
     - ``image/jpeg``
     - 사진 등
   * - PNG
     - ``image/png``
     - 투명 이미지 등
   * - GIF
     - ``image/gif``
     - 애니메이션 GIF 포함
   * - BMP
     - ``image/bmp``, ``image/x-windows-bmp``, ``image/x-ms-bmp``
     - 비트맵 이미지
   * - TIFF
     - ``image/tiff``
     - 고품질 이미지
   * - SVG
     - ``image/svg+xml``
     - 벡터 이미지
   * - Photoshop
     - ``image/vnd.adobe.photoshop``, ``image/photoshop``, ``application/x-photoshop``, ``application/photoshop``
     - PSD 파일

문서 파일
---------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - 형식
     - MIME 타입
     - 설명
   * - PDF
     - ``application/pdf``
     - PDF 문서
   * - Word
     - ``application/msword``, ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - Word 문서
   * - Excel
     - ``application/vnd.ms-excel``, ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``, ``application/vnd.ms-excel.sheet.2``, ``application/vnd.ms-excel.sheet.3``, ``application/vnd.ms-excel.sheet.4``, ``application/vnd.ms-excel.workspace.3``, ``application/vnd.ms-excel.workspace.4``
     - Excel 스프레드시트
   * - PowerPoint
     - ``application/vnd.ms-powerpoint``, ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - PowerPoint 프레젠테이션
   * - RTF
     - ``application/rtf``
     - 서식 있는 텍스트
   * - PostScript
     - ``application/postscript``
     - PostScript 파일

HTML 콘텐츠
-----------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - 형식
     - MIME 타입
     - 설명
   * - HTML
     - ``text/html``
     - HTML 페이지 내 포함 이미지로부터 썸네일을 생성

필요한 외부 도구
================

썸네일 생성에는 다음 외부 도구가 필요합니다. 사용하는 파일 형식에 따라 설치하십시오.

기본 도구（필수）
----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 도구
     - 용도
     - Linux (apt)
     - Mac (Homebrew)
   * - ImageMagick
     - 이미지 변환 · 크기 조정
     - ``apt install imagemagick``
     - ``brew install imagemagick``

.. note::

   ImageMagick 6（``convert`` 명령）와 ImageMagick 7（``magick`` 명령）을 모두 지원합니다.

SVG 지원
--------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 도구
     - 용도
     - Linux (apt)
     - Mac (Homebrew)
   * - rsvg-convert
     - SVG→PNG 변환
     - ``apt install librsvg2-bin``
     - ``brew install librsvg``

PDF 지원
--------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 도구
     - 용도
     - Linux (apt)
     - Mac (Homebrew)
   * - pdftoppm
     - PDF→PNG 변환
     - ``apt install poppler-utils``
     - ``brew install poppler``

MS Office 지원
--------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 도구
     - 용도
     - Linux (apt)
     - Mac (Homebrew)
   * - unoconv
     - Office→PDF 변환
     - ``apt install unoconv``
     - ``brew install unoconv``
   * - pdftoppm
     - PDF→PNG 변환
     - ``apt install poppler-utils``
     - ``brew install poppler``

Redhat 계열 OS의 경우 다음 패키지를 설치합니다.

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick poppler-utils

PostScript 지원
---------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 도구
     - 용도
     - Linux (apt)
     - Mac (Homebrew)
   * - ps2pdf
     - PS→PDF 변환
     - ``apt install ghostscript``
     - ``brew install ghostscript``
   * - pdftoppm
     - PDF→PNG 변환
     - ``apt install poppler-utils``
     - ``brew install poppler``

HTML 파일의 썸네일 이미지
=========================

HTML의 썸네일 이미지는 HTML 내에서 지정된 이미지 또는 포함된 이미지를 사용합니다.
다음 순서로 썸네일 이미지를 찾아 지정된 경우 표시합니다.

1. name 속성이 thumbnail로 지정된 meta 태그의 content 값
2. property 속성이 og:image로 지정된 meta 태그의 content 값
3. img 태그에서 썸네일에 적합한 크기의 이미지

설정
====

설정 파일
---------

썸네일 생성기 설정은 ``fess_thumbnail.xml`` 에서 수행합니다.

::

    app/WEB-INF/classes/fess_thumbnail.xml

주요 설정 항목（fess_config.properties）
-----------------------------------------

``app/WEB-INF/classes/fess_config.properties`` 또는 ``/etc/fess/fess_config.properties`` 에서 다음 항목을 설정할 수 있습니다.

::

    # 썸네일 이미지의 최소 너비（픽셀）
    thumbnail.html.image.min.width=100

    # 썸네일 이미지의 최소 높이（픽셀）
    thumbnail.html.image.min.height=100

    # 최대 종횡비（너비:높이 또는 높이:너비）
    thumbnail.html.image.max.aspect.ratio=3.0

    # 생성되는 썸네일의 너비
    thumbnail.html.image.thumbnail.width=100

    # 생성되는 썸네일의 높이
    thumbnail.html.image.thumbnail.height=100

    # 출력 형식
    thumbnail.html.image.format=png

    # HTML 내 이미지를 추출하는 XPath
    thumbnail.html.image.xpath=//IMG

    # 제외할 확장자
    thumbnail.html.image.exclude.extensions=svg,html,css,js

    # 썸네일 생성 간격（밀리초）
    thumbnail.generator.interval=0

    # 썸네일 생성 대상
    thumbnail.generator.targets=all

    # 썸네일 시스템 모니터링 간격（초）
    thumbnail.system.monitor.interval=60

.. note::
   다음 속성은 ``fess_config.properties`` 가 아니라 관리 화면의 「전반 설정」 또는 ``system.properties`` 에서 설정합니다.

::

    # 명령 실행 타임아웃（밀리초）
    thumbnail.command.timeout=30000

    # 프로세스 종료 타임아웃（밀리초）
    thumbnail.command.destroy.timeout=5000

generate-thumbnail 스크립트
============================

개요
----

``generate-thumbnail`` 은 실제 썸네일 생성을 수행하는 셸 스크립트입니다.
RPM/Deb 패키지로 설치하면 ``/usr/share/fess/bin/generate-thumbnail`` 에 설치됩니다.

사용 방법
---------

::

    generate-thumbnail <type> <url> <output_file> [mimetype]

인수
----

.. list-table::
   :widths: 15 50 30
   :header-rows: 1

   * - 인수
     - 설명
     - 예시
   * - ``type``
     - 파일 타입
     - ``image``, ``svg``, ``pdf``, ``msoffice``, ``ps``
   * - ``url``
     - 입력 파일의 URL
     - ``file:/path/to/file.jpg``
   * - ``output_file``
     - 출력 파일 경로
     - ``/var/lib/fess/thumbnails/_0/_1/abc.png``
   * - ``mimetype``
     - MIME 타입（선택）
     - ``image/gif``

.. note::

   ``mimetype`` 인수는 ``image`` 타입에서만 사용되며, ImageMagick에 전달하는 형식 힌트를 결정합니다.
   힌트가 적용되는 MIME 타입은 ``image/gif`` , ``image/tiff`` , ``image/png`` , ``image/jpeg`` ,
   ``image/bmp`` （및 해당 별칭）, Photoshop（PSD）계열 MIME 타입입니다.
   ``pdf`` , ``msoffice`` , ``ps`` 타입에서는 ``mimetype`` 인수가 무시됩니다.

지원하는 타입
-------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - 타입
     - 설명
     - 사용 도구
   * - ``image``
     - 이미지 파일
     - ImageMagick (convert/magick)
   * - ``svg``
     - SVG 파일
     - rsvg-convert
   * - ``pdf``
     - PDF 파일
     - pdftoppm + ImageMagick
   * - ``msoffice``
     - MS Office 파일
     - unoconv + pdftoppm + ImageMagick
   * - ``ps``
     - PostScript 파일
     - ps2pdf + pdftoppm + ImageMagick

사용 예시
---------

::

    # 이미지 파일의 썸네일 생성
    ./generate-thumbnail image file:/path/to/image.jpg /tmp/thumbnail.png image/jpeg

    # SVG 파일의 썸네일 생성
    ./generate-thumbnail svg file:/path/to/image.svg /tmp/thumbnail.png

    # PDF 파일의 썸네일 생성
    ./generate-thumbnail pdf file:/path/to/document.pdf /tmp/thumbnail.png

    # GIF 파일（MIME 타입을 지정하여 형식 힌트 활성화）
    ./generate-thumbnail image file:/path/to/image.gif /tmp/thumbnail.png image/gif

썸네일 저장 위치
================

기본 경로
---------

::

    ${FESS_VAR_PATH}/thumbnails/

또는

::

    /var/lib/fess/thumbnails/

디렉터리 구조
-------------

썸네일은 해시 기반의 디렉터리 구조로 저장됩니다.
문서 ID를 10자마다 분할하고, 분할마다 ``_<0-9>`` 형식（해시값）의 하위 디렉터리를 생성합니다.
따라서 디렉터리의 계층 수는 문서 ID의 길이에 따라 달라집니다. 최하위 파일명은 ``<문서 ID>.png`` 입니다.

::

    thumbnails/
    └── _3/
        └── _7/
            └── <문서 ID>.png

썸네일 작업 비활성화
====================

썸네일 작업을 비활성화하는 경우 다음과 같이 설정합니다.

1. 관리 화면의 시스템 > 전반에서 「썸네일 표시」 체크를 해제하고 「업데이트」 버튼을 클릭합니다.
2. ``app/WEB-INF/classes/fess_config.properties`` 또는 ``/etc/fess/fess_config.properties`` 의 ``thumbnail.crawler.enabled`` 에 ``false`` 를 설정합니다（기본값은 ``true``）.

::

    thumbnail.crawler.enabled=false

3. Fess 서비스를 재시작합니다.

트러블슈팅
==========

썸네일이 생성되지 않는 경우
----------------------------

1. **외부 도구 확인**

::

    # ImageMagick 확인
    which convert || which magick

    # rsvg-convert 확인（SVG용）
    which rsvg-convert

    # pdftoppm 확인（PDF용）
    which pdftoppm

2. **로그 확인**

::

    ${FESS_LOG_PATH}/fess-thumbnail.log

3. **수동으로 스크립트 실행**

::

    /usr/share/fess/bin/generate-thumbnail image file:/path/to/test.jpg /tmp/test_thumbnail.png image/jpeg

GIF/TIFF에서 오류가 발생하는 경우
-----------------------------------

ImageMagick 6을 사용하는 경우, MIME 타입을 지정하여 형식 힌트를 활성화하십시오. Fess의 설정이 올바르면 자동으로 처리됩니다.

오류 예::

    convert-im6.q16: corrupt image `/tmp/thumbnail_xxx' @ error/gif.c/DecodeImage/512

대처 방법:

- ImageMagick 7로 업그레이드
- 또는 MIME 타입이 올바르게 전달되고 있는지 확인

SVG 썸네일이 생성되지 않는 경우
---------------------------------

1. ``rsvg-convert`` 가 설치되어 있는지 확인

::

    which rsvg-convert

2. 수동으로 변환을 테스트

::

    rsvg-convert -w 100 -h 100 --keep-aspect-ratio input.svg -o output.png

권한 오류
---------

썸네일 저장 디렉터리의 권한을 확인합니다.

::

    ls -la /var/lib/fess/thumbnails/

필요에 따라 권한을 수정합니다.

::

    chown -R fess:fess /var/lib/fess/thumbnails/
    chmod -R 755 /var/lib/fess/thumbnails/

플랫폼 지원
===========

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - 플랫폼
     - 지원 상태
     - 비고
   * - Linux
     - 완전 지원
     - \-
   * - macOS
     - 완전 지원
     - Homebrew로 외부 도구를 설치
   * - Windows
     - 미지원
     - bash 스크립트이기 때문
