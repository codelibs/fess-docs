============
위치 정보 검색
============

개요
====

|Fess| 는 위도와 경도의 위치 정보를 가진 문서에 대해 지리적 범위를 지정한 검색을 실행할 수 있습니다.
이 기능을 사용하면 특정 지점에서 일정 거리 내에 있는 문서를 검색하거나,
Google Maps 등의 지도 서비스와 연계한 검색 시스템을 구축할 수 있습니다.

활용 사례
============

위치 정보 검색은 다음과 같은 용도로 활용할 수 있습니다.

- 매장 검색: 사용자의 현재 위치에서 가까운 매장 검색
- 부동산 검색: 특정 역이나 시설에서 일정 거리 내의 매물 검색
- 이벤트 검색: 지정한 장소 주변의 이벤트 정보 검색
- 시설 검색: 관광 명소나 공공 시설의 인근 검색

설정 방법
========

인덱스 생성 시 설정
------------------------

위치 정보 필드 정의
~~~~~~~~~~~~~~~~~~~~~~~~

|Fess| 에서는 위치 정보를 저장하는 필드로 ``location`` 이 표준으로 정의되어 있습니다.
이 필드는 OpenSearch의 ``geo_point`` 타입으로 설정되어 있습니다.

위치 정보 등록 형식
~~~~~~~~~~~~~~~~~~

인덱스 생성 시 위도와 경도를 쉼표로 구분하여 ``location`` 필드에 설정합니다.

**형식:**

::

    위도,경도

**예:**

::

    45.17614,-93.87341

.. note::
   위도는 -90에서 90 범위, 경도는 -180에서 180 범위로 지정합니다.

데이터 스토어 크롤링 설정 예
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

데이터 스토어 크롤링을 사용하는 경우 위치 정보를 가진 데이터 소스에서 ``location`` 필드에
위도와 경도를 설정합니다.

**예: 데이터베이스에서 가져오기**

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) as location
    FROM stores

스크립트로 위치 정보 추가
~~~~~~~~~~~~~~~~~~~~~~~~~~

크롤 설정의 스크립트 기능을 사용하여 문서에 위치 정보를 동적으로 추가할 수도 있습니다.

::

    // 위도와 경도를 location 필드에 설정
    doc.location = "37.566536,126.977966";

검색 시 설정
------------

위치 정보 검색을 실행하려면 요청 파라미터로 검색의 중심점과 범위를 지정합니다.

요청 파라미터
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 파라미터 이름
     - 설명
   * - ``geo.location.point``
     - 검색 중심이 되는 지점의 위도·경도(쉼표 구분)
   * - ``geo.location.distance``
     - 중심점에서의 검색 반경(단위 포함)

거리 단위
~~~~~~~~~~

거리에는 다음 단위를 사용할 수 있습니다.

- ``km``: 킬로미터
- ``m``: 미터
- ``mi``: 마일
- ``yd``: 야드

검색 예
======

기본 검색
------------

서울역(37.566536, 126.977966)에서 반경 10km 이내의 문서를 검색하는 경우:

::

    http://localhost:8080/search?q=검색키워드&geo.location.point=37.566536,126.977966&geo.location.distance=10km

현재 위치 주변 검색
----------------

사용자의 현재 위치에서 1km 이내를 검색하는 경우:

::

    http://localhost:8080/search?q=카페&geo.location.point=37.566536,126.977966&geo.location.distance=1km

거리순 정렬
----------------

검색 결과를 거리순으로 정렬하는 경우 ``sort`` 파라미터를 사용합니다.

::

    http://localhost:8080/search?q=편의점&geo.location.point=37.566536,126.977966&geo.location.distance=5km&sort=location.distance

API 사용
-----------

JSON API에서도 위치 정보 검색을 사용할 수 있습니다.

::

    curl -X POST "http://localhost:8080/json/?q=호텔" \
      -H "Content-Type: application/json" \
      -d '{
        "geo.location.point": "37.566536,126.977966",
        "geo.location.distance": "5km"
      }'

필드 이름 사용자 정의
==========================

기본 필드 이름 변경
----------------------------

위치 정보 검색에서 사용하는 필드 이름을 변경하는 경우
``fess_config.properties`` 에서 다음 설정을 변경합니다.

::

    query.geo.fields=location

여러 필드 이름을 지정하는 경우 쉼표로 구분하여 지정합니다.

::

    query.geo.fields=location,geo_point,coordinates

구현 예
======

웹 애플리케이션에서의 구현
---------------------------

JavaScript로 현재 위치를 가져와 검색하는 예:

.. code-block:: javascript

    // 브라우저의 Geolocation API로 현재 위치 가져오기
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const distance = "5km";

        // 검색 URL 구축
        const searchUrl = `/search?q=&geo.location.point=${latitude},${longitude}&geo.location.distance=${distance}`;

        // 검색 실행
        window.location.href = searchUrl;
    });

Google Maps와의 연계
--------------------

검색 결과를 Google Maps에 마커로 표시하는 예:

.. code-block:: javascript

    // 지도 초기화
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.566536, lng: 126.977966},
        zoom: 13
    });

    // Fess API로 위치 정보 검색 실행
    fetch('/json/?q=매장&geo.location.point=37.566536,126.977966&geo.location.distance=5km')
        .then(response => response.json())
        .then(data => {
            // 검색 결과를 마커로 표시
            data.response.result.forEach(doc => {
                if (doc.location) {
                    const [lat, lng] = doc.location.split(',').map(Number);
                    new google.maps.Marker({
                        position: {lat: lat, lng: lng},
                        map: map,
                        title: doc.title
                    });
                }
            });
        });

성능 최적화
====================

인덱스 설정 최적화
------------------------

대량의 위치 정보 데이터를 다루는 경우 인덱스 설정을 최적화합니다.

``app/WEB-INF/classes/fess_indices/fess.json`` 에서 위치 정보 필드의 설정을 확인하십시오.

::

    "location": {
        "type": "geo_point"
    }

검색 범위 제한
--------------

성능을 고려하여 검색 범위는 필요 최소한으로 설정하는 것을 권장합니다.

- 광범위한 검색(50km 이상)은 처리에 시간이 걸릴 수 있습니다
- 용도에 따라 적절한 범위를 설정하십시오

문제 해결
======================

위치 정보 검색이 작동하지 않음
------------------------

1. ``location`` 필드에 데이터가 올바르게 저장되어 있는지 확인하십시오.
2. 위도와 경도의 형식이 올바른지 확인하십시오(쉼표 구분).
3. OpenSearch의 인덱스 매핑에서 ``location`` 이 ``geo_point`` 타입으로 정의되어 있는지 확인하십시오.

검색 결과가 반환되지 않음
----------------------

1. 지정한 거리 범위 내에 문서가 존재하는지 확인하십시오.
2. 위도와 경도 값이 올바른 범위 내(위도: -90〜90, 경도: -180〜180)인지 확인하십시오.
3. 거리 단위가 올바르게 지정되어 있는지 확인하십시오.

위치 정보가 올바르게 표시되지 않음
----------------------------

1. 크롤 시 ``location`` 필드가 올바르게 설정되어 있는지 확인하십시오.
2. 데이터 소스의 위도와 경도 데이터 타입이 숫자 타입인지 확인하십시오.
3. 스크립트로 위치 정보를 설정하는 경우 문자열 결합 형식이 올바른지 확인하십시오.

참고 정보
========

위치 정보 검색의 자세한 내용은 다음 리소스를 참조하십시오.

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/ko/docs/Web/API/Geolocation_API>`_
