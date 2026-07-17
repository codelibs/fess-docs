============================
인덱스 내보내기 기능
============================

개요
====

인덱스 내보내기 기능은 OpenSearch에 색인된 검색 문서를 HTML 또는 JSON 파일로 로컬 파일 시스템에 내보냅니다. 이 기능은 다음과 같은 용도에 유용합니다.

- 색인된 콘텐츠의 정적 백업 생성
- 아카이브 목적의 문서 오프라인 복사본 생성
- 정적 검색 결과 페이지 구축
- 다른 시스템으로 콘텐츠 마이그레이션

내보낸 파일은 소스 문서의 원본 URL 경로 구조를 유지하므로 내보낸 콘텐츠를 쉽게 관리할 수 있습니다.

작동 방식
=========

인덱스 내보내기 작업이 실행되면 다음 처리가 수행됩니다.

1. **문서 취득**: 스크롤 API를 사용하여 OpenSearch에서 문서를 효율적으로 배치 취득
2. **콘텐츠 처리**: 문서 필드(제목, 콘텐츠, URL 등)를 추출하고 제외 대상 필드를 제거
3. **디렉토리 구조 생성**: 문서의 ``url`` 필드를 기반으로 내보내기 디렉토리에 URL 경로 구조를 재현
4. **파일 생성**: 문서 콘텐츠를 포함하는 파일(HTML 또는 JSON) 생성
5. **완료될 때까지 계속**: 인덱스가 완전히 내보내질 때까지 배치 처리를 계속

스크롤 API를 사용하므로 메모리 문제 없이 대규모 문서 세트를 효율적으로 처리할 수 있습니다.

.. note::

   내보내기 대상은 검색 인덱스(``fess.search``)의 문서입니다. ``url`` 필드가 없는 문서는 건너뜁니다.

설정 속성
=========

``fess_config.properties``\ 에서 인덱스 내보내기 기능을 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 속성
     - 기본값
     - 설명
   * - ``index.export.path``
     - ``/var/lib/fess/export``
     - 내보낸 파일을 저장하는 디렉토리
   * - ``index.export.exclude.fields``
     - ``cache``
     - 내보내기에서 제외할 필드(쉼표로 구분)
   * - ``index.export.scroll.size``
     - ``100``
     - 배치당 처리할 문서 수
   * - ``index.export.format``
     - ``html``
     - 내보내기 파일 형식(``html`` 또는 ``json``)

설정 예:

::

    index.export.path=/data/fess/export
    index.export.exclude.fields=cache,boost,role
    index.export.scroll.size=200

작업 활성화
===========

인덱스 내보내기 작업은 예약된 작업으로 등록되어 있지만 기본적으로 비활성화되어 있습니다.

작업을 활성화하려면:

1. |Fess| 관리 콘솔에 로그인
2. **시스템** > **스케줄러**\ 로 이동
3. 작업 목록에서 **Index Exporter** 찾기
4. 클릭하여 작업 설정 편집
5. cron 표현식을 사용하여 일정 설정
6. 설정 저장

cron 표현식 예:

- ``0 0 2 * * ?`` - 매일 오전 2시에 실행
- ``0 0 3 ? * SUN`` - 매주 일요일 오전 3시에 실행
- ``0 0 0 1 * ?`` - 매월 1일 자정에 실행

사용자 정의 쿼리 필터링
=======================

작업 스크립트를 수정하여 특정 문서만 내보내도록 사용자 정의할 수 있습니다.

**Index Exporter** 작업의 기본 스크립트는 모든 문서를 내보냅니다:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.matchAllQuery())
        .execute()

사용자 정의 쿼리 필터를 추가하려면:

1. **시스템** > **스케줄러**\ 로 이동
2. **Index Exporter** 편집
3. 쿼리 필터를 포함하도록 작업 스크립트 수정

날짜 필터 예(최근 7일간의 문서만 내보내기):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.rangeQuery("created").gte("now-7d"))
        .execute()

사이트 필터 예(특정 사이트의 문서만 내보내기):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.wildcardQuery("url", "*example.com*"))
        .execute()

JSON 형식으로 내보내기 예:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .format("json")
        .execute()

내보낸 파일 구조
================

내보낸 파일은 원본 URL 구조를 반영하도록 구성됩니다.

예를 들어, URL이 ``https://example.com/docs/guide/intro.html``\ 인 문서는 다음과 같이 내보내집니다:

::

    /var/lib/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

파일 경로는 문서의 ``url`` 필드로부터 다음 규칙에 따라 결정됩니다:

- 호스트명이 최상위 디렉토리가 됩니다. URL에 호스트명이 포함되지 않은 경우 ``_local``\ 이 사용됩니다.
- 경로가 슬래시로 끝나거나 경로가 없는 경우 인덱스 파일(``index.html`` 또는 ``index.json``)이 생성됩니다.
- 경로에 파일 확장자가 포함되지 않은 경우 형식에 따른 확장자(``.html`` 또는 ``.json``)가 추가됩니다.
- 파일명에 사용할 수 없는 문자(``< > : " | ? * \``)는 ``_``\ 로 대체되며, 각 경로 구성 요소는 최대 200자로 잘립니다.
- URL을 파싱할 수 없거나 경로 탐색이 감지된 경우 ``_invalid`` 디렉토리에 URL의 해시값을 파일명으로 저장됩니다.

HTML 형식의 경우 각 파일은 다음 구조로 생성됩니다:

- ``title`` 필드 → ``<title>`` 요소
- ``lang`` 필드 → ``<html>`` 요소의 ``lang`` 속성
- ``content`` 필드 → ``<body>`` 요소의 본문
- 그 외 제외되지 않은 필드 → ``<head>`` 내의 ``<meta name="fess:필드명" content="값">`` 태그

::

    <!DOCTYPE html>
    <html lang="ko">
    <head>
    <meta charset="UTF-8">
    <title>샘플 문서</title>
    <meta name="fess:url" content="https://example.com/docs/guide/intro.html">
    <meta name="fess:last_modified" content="2024-01-01T00:00:00.000Z">
    <meta name="fess:content_type" content="text/html">
    </head>
    <body>
    문서의 본문 콘텐츠
    </body>
    </html>

JSON 형식의 경우 각 파일은 제외되지 않은 모든 필드를 포함하는 JSON 객체가 됩니다:

::

    {
      "url": "https://example.com/docs/guide/intro.html",
      "title": "샘플 문서",
      "content": "문서의 본문 콘텐츠",
      "last_modified": "2024-01-01T00:00:00.000Z",
      "content_type": "text/html"
    }

모범 사례
=========

스토리지 고려 사항
------------------

- 내보내기 디렉토리에 충분한 디스크 공간 확보
- 대규모 문서 세트에는 전용 스토리지 사용 고려
- 정기 내보내기를 실행하는 경우 이전 내보내기의 정기적인 정리 구현

성능 팁
-------

- 문서 크기에 따라 ``index.export.scroll.size`` 조정:
  - 작은 문서: 큰 배치 크기(200-500)
  - 큰 문서: 작은 배치 크기(50-100)
- 사용량이 적은 시간대에 내보내기 예약
- 내보내기 작업 중 디스크 I/O 모니터링

보안 권장 사항
--------------

- 내보내기 디렉토리에 적절한 파일 권한 설정
- 내보내기 디렉토리를 웹에 직접 노출하지 않음
- 민감한 정보가 포함된 콘텐츠는 내보낸 후 암호화 고려
- 내보낸 파일에 대한 접근을 정기적으로 감사

문제 해결
=========

내보내기 작업이 실행되지 않음
-----------------------------

1. 스케줄러에서 작업이 활성화되어 있는지 확인
2. cron 표현식 구문 확인
3. |Fess| 로그에서 오류 메시지 확인:

::

    tail -f /var/log/fess/fess.log | grep IndexExport

내보내기 디렉토리가 비어 있음
-----------------------------

1. 인덱스에 문서가 있는지 확인
2. 내보내기 경로의 권한 확인
3. 쿼리 필터(사용자 정의인 경우)가 문서와 일치하는지 확인

::

    # 인덱스 문서 수 확인
    curl -X GET "localhost:9201/fess.search/_count?pretty"

내보내기가 중간에 실패함
------------------------

1. 사용 가능한 디스크 공간 확인
2. 메모리 또는 타임아웃 오류에 대한 로그 확인
3. 대용량 문서의 경우 ``scroll.size`` 감소 고려
4. OpenSearch 스크롤 컨텍스트의 타임아웃 설정 확인

파일에 액세스할 수 없음
-----------------------

1. 파일 권한 확인: ``ls -la /var/lib/fess/export``
2. 디렉토리 소유자가 |Fess| 프로세스 사용자와 일치하는지 확인
3. SELinux 또는 AppArmor 정책이 액세스를 허용하는지 확인

관련 주제
=========

- :doc:`admin-index-backup` - 인덱스 백업 및 복원 절차
- :doc:`admin-logging` - 문제 해결을 위한 로그 설정 구성
