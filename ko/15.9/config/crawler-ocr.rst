==================================
OCR(이미지 내 문자 인식) 설정
==================================

개요
====

|Fess|\ 는 Apache Tika를 사용하여 문서에서 텍스트를 추출합니다.
Tika의 Tesseract OCR 파서는 |Fess|\ 에 포함되어 있으며, 이를 활성화하면 이미지나 스캔한 PDF에 포함된 문자를 인식하여 검색 대상으로 만들 수 있습니다.

OCR은 다음 두 조건이 모두 충족될 때 실행됩니다.

- |Fess| 크롤러 프로세스가 동작하는 호스트에 ``tesseract`` 명령이 설치되어 있음
- |Fess|\ 에서 OCR이 활성화되어 있음

OCR은 기본적으로 비활성화되어 있습니다.
``tesseract``\ 가 설치되어 있지 않으면 |Fess|\ 는 OCR을 건너뜁니다. 오류는 발생하지 않습니다.

OCR 대상
========

OCR을 활성화하면 다음이 대상이 됩니다.

- 이미지 파일(PNG, JPEG, TIFF, GIF, BMP 등)
- Tika가 처리하는 문서에 포함된 이미지(Office 파일 등)
- 텍스트 레이어가 비어 있는 PDF(스캔한 PDF)

스캔한 PDF의 처리
-----------------

|Fess|\ 는 보통 PDFBox로 PDF에서 텍스트를 추출합니다.
OCR이 활성화되어 있고 PDFBox가 PDF에서 텍스트를 전혀 얻지 못한 경우, |Fess|\ 는 해당 PDF를 Tika로 다시 추출합니다.
이때 Tika가 페이지를 이미지로 변환하여 OCR을 실행합니다.

.. note::
   이미 텍스트를 포함하고 있는 PDF는 OCR 대상이 되지 않습니다.
   일부 페이지만 스캔 이미지인 PDF(혼합 PDF)는 대상 외입니다.

Tesseract 설치
==============

|Fess|\ 를 실행하는 호스트에 Tesseract를 설치합니다.
일본어 문자를 인식하려면 일본어 학습 데이터(traineddata)도 필요합니다.

Debian / Ubuntu::

    $ sudo apt-get install tesseract-ocr tesseract-ocr-jpn

RHEL / Rocky Linux / AlmaLinux (EPEL을 활성화하십시오)::

    $ sudo dnf install tesseract tesseract-langpack-jpn

설치된 언어는 다음 명령으로 확인할 수 있습니다::

    $ tesseract --list-langs

OCR 활성화
==========

``fess_config.properties``\ 에 다음 프로퍼티를 설정합니다.

- ZIP 버전: ``app/WEB-INF/classes/fess_config.properties``
- RPM/DEB 버전: ``/etc/fess/fess_config.properties``

::

    # OCR을 활성화(기본값: false)
    crawler.document.ocr.enabled=true

    # Tesseract 언어(여러 개인 경우 +로 연결, 기본값: eng)
    crawler.document.ocr.language=jpn+eng

    # Tesseract 1회 실행의 타임아웃(초, 기본값: 120)
    crawler.document.ocr.timeout=120

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``crawler.document.ocr.enabled``
     - ``false``
     - ``true``\ 로 설정하면 OCR이 활성화됩니다.
   * - ``crawler.document.ocr.language``
     - ``eng``
     - Tesseract 언어입니다. 여러 언어는 ``+``\ 로 연결합니다(예: ``jpn+eng``). 해당 traineddata가 설치되어 있어야 합니다.
   * - ``crawler.document.ocr.timeout``
     - ``120``
     - Tesseract 1회 실행(이미지 1장 또는 PDF 1페이지)의 타임아웃입니다. 단위는 초입니다.

이 설정은 JVM 시스템 프로퍼티로도 지정할 수 있습니다.
예를 들어 ``FESS_JAVA_OPTS``\ 에 다음과 같이 지정합니다. Docker 환경에서 편리합니다.

::

    -Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng

.. note::
   설정을 변경한 후에는 |Fess|\ 를 재시작하십시오.

Docker에서 사용하는 경우
========================

Docker 환경에서 OCR을 사용하려면 |Fess| 이미지에 Tesseract를 추가합니다.
`docker-fess <https://github.com/codelibs/docker-fess>`__\ 의 ``compose/tesseract/Dockerfile``\ 을 사용하여 Tesseract를 추가한 이미지를 빌드합니다.

``compose/tesseract/Dockerfile`` 예::

    FROM ghcr.io/codelibs/fess:15.9.0

    RUN apk add --no-cache tesseract-ocr tesseract-ocr-data-osd tesseract-ocr-data-eng tesseract-ocr-data-jpn

``compose/compose.yaml``\ 에서 ``image:`` 행을 ``build: ./tesseract``\ 로 바꾸고 ``FESS_JAVA_OPTS`` 행을 활성화합니다.
``build: ./playwright``\ 와 같은 방식입니다.

::

    services:
      fess01:
        # image: ghcr.io/codelibs/fess:15.9.0
        build: ./tesseract
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng"

변경 후에는 이미지를 다시 빌드하여 컨테이너를 시작합니다::

    $ docker compose up -d --build

.. note::
   ``-noble``\ 이나 ``-al2023`` 등 Alpine이 아닌 베이스 이미지를 사용하는 경우, ``apk`` 대신 해당 배포판의 패키지 관리자로 Tesseract를 추가하십시오.

자세한 내용은 :doc:`../install/install-docker`\ 를 참조하십시오.

크롤링 설정별 설정
==================

크롤링 설정의 「설정 파라미터」에 ``config.tika.tesseract.config``\ 를 지정하면, 해당 크롤링 설정에 한해 OCR 설정을 덮어쓸 수 있습니다.

::

    config.tika.tesseract.config=tesseract.properties

``tesseract.properties``\ 는 클래스패스 상의 리소스 이름입니다. 파일 시스템 경로가 아닙니다.
파일은 크롤러의 클래스패스에 포함된 |Fess| 설정 디렉터리에 둡니다.

- ZIP 버전: ``app/WEB-INF/classes/``
- RPM/DEB 버전: ``/etc/fess/``

``tesseract.properties``\ 에는 Tika의 ``TesseractOCRConfig`` 프로퍼티를 작성합니다.
확실하게 반영되는 것은 ``language``\ 나 ``timeoutSeconds`` 같은 단순한 키입니다.

::

    language=jpn
    timeoutSeconds=300

이 크롤링 설정에 대해서는 위의 전역 설정보다 이 지정이 우선합니다.

운영상의 주의
=============

- OCR은 CPU에 높은 부하를 주며 크롤링 처리 시간이 크게 늘어납니다. 크롤러 스레드 수를 줄이거나 OCR이 필요한 크롤링 설정에서만 활성화하는 등 부하를 고려하십시오.
- 웹 크롤링 설정에서는 신규 생성 시 기본값으로 이미지 URL(jpg, png, gif 등)이 크롤링 대상에서 제외됩니다. 웹 사이트의 이미지를 크롤링하려면 「크롤링 대상에서 제외할 URL」에서 이를 삭제하십시오. 파일 크롤링에서는 이미지도 크롤링 대상이 됩니다.
- 크롤러의 크기 제한도 적용됩니다. 파일 종류별 인덱스 크기 상한(기본값 10MB)에 대해서는 :doc:`crawler-basic`\ 을 참조하십시오.
- OCR 정확도는 스캔한 이미지의 품질에 좌우됩니다. 손글씨는 일반적으로 인식되기 어렵습니다.

업그레이드 시 주의
==================

15.8 이전에 포함된 ``tika.xml``\ 은 ``org.apache.tika.parser.ocr.TesseractOCRParser``\ 를 제외하고 있었습니다.
15.9부터는 포함된 ``tika.xml``\ 이 이 파서를 제외하지 않습니다.

``tika.xml``\ 을 커스터마이즈하여 계속 사용하고 있는 경우, 다음 행을 삭제하십시오.

::

    <parser-exclude class="org.apache.tika.parser.ocr.TesseractOCRParser"/>

이 행이 남아 있으면 ``crawler.document.ocr.enabled=true``\ 를 지정해도 OCR은 비활성화된 상태로 유지됩니다.

``tika.xml``\ 의 위치는 다음과 같습니다.

- ZIP 버전: ``app/WEB-INF/conf/tika.xml``
- RPM/DEB 버전: ``/etc/fess/tika.xml``

동작 확인
=========

1. 스캔한 이미지(문자가 포함된 이미지)를 둔 폴더를 파일 크롤링 대상으로 설정합니다.
2. 크롤링을 실행합니다.
3. 이미지에 포함된 단어로 검색하여 해당 이미지가 검색 결과에 표시되는지 확인합니다.

검색 결과에 표시되지 않으면 다음 사항을 확인하십시오.

- ``tesseract --list-langs``\ 에 사용하는 언어가 표시됨
- ``crawler.document.ocr.enabled``\ 가 ``true``\ 로 되어 있음
- ``tika.xml``\ 에 ``TesseractOCRParser`` 제외가 남아 있지 않음
- 크롤링 시 ``fess-crawler.log``\ 에 ``OCR is enabled``\ 가 출력됨(``Tesseract OCR is not available`` 경고가 출력되면 |Fess|\ 에서 Tesseract를 사용할 수 없는 상태입니다)
