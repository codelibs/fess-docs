================
위치 정보 검색
================

개요
====

|Fess| 는 위도와 경도의 위치 정보를 가진 문서에 대해 지리적 범위를 지정한 검색을 실행할 수 있습니다.
이 기능을 사용하면 특정 지점에서 일정 거리 내에 있는 문서를 검색하거나,
Google Maps 등의 지도 서비스와 연계한 검색 시스템을 구축할 수 있습니다.

내부적으로는 OpenSearch의 geo-distance 쿼리를 사용하여, 지정한 중심점에서 지정한 거리 이내에
존재하는 문서를 필터링합니다.

활용 사례
============

위치 정보 검색은 다음과 같은 용도로 활용할 수 있습니다.

- 매장 검색: 사용자의 현재 위치에서 가까운 매장 검색
- 부동산 검색: 특정 역이나 시설에서 일정 거리 내의 매물 검색
- 이벤트 검색: 지정한 장소 주변의 이벤트 정보 검색
- 시설 검색: 관광 명소나 공공 시설의 인근 검색

설정 방법
=========

인덱스 생성 시 설정
-------------------

위치 정보 필드 정의
~~~~~~~~~~~~~~~~~~~

|Fess| 에서는 위치 정보를 저장하는 필드로 ``location`` 이 표준으로 정의되어 있습니다.
이 필드는 OpenSearch의 ``geo_point`` 타입으로 설정되어 있습니다.

위치 정보 등록 형식
~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

데이터 스토어 크롤링을 사용하는 경우 위치 정보를 가진 데이터 소스에서 ``location`` 필드에
위도와 경도를 설정합니다.

**예: 데이터베이스에서 가져오기**

위도·경도를 별도 컬럼으로 저장하는 경우, SQL에서 쉼표로 구분된 문자열로 결합합니다.

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) AS location
    FROM stores

데이터 스토어 설정 스크립트에서 가져온 값을 ``location`` 필드에 매핑합니다.

::

    location=data.location

스크립트로 위치 정보 추가
~~~~~~~~~~~~~~~~~~~~~~~~~~

크롤 설정의 스크립트 기능(Groovy)을 사용하여 문서에 위치 정보를 동적으로 추가할 수도 있습니다.
필드 이름에 직접 값을 대입합니다.

::

    // 위도와 경도를 location 필드에 설정
    location="37.566536,126.977966"

스크립트의 자세한 내용은 :doc:`scripting-groovy` 를 참조하십시오.

검색 시 설정
------------

위치 정보 검색을 실행하려면 요청 파라미터로 검색의 중심점과 범위를 지정합니다.

요청 파라미터
~~~~~~~~~~~~~

위치 정보 검색의 파라미터 이름은 ``geo.<필드명>.point`` 및 ``geo.<필드명>.distance``
형식입니다. ``<필드명>`` 에는 ``query.geo.fields`` 에서 설정된 필드 이름이 들어갑니다
(기본값은 ``location`` ).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 파라미터 이름
     - 설명
   * - ``geo.location.point``
     - 검색 중심이 되는 지점의 위도·경도(쉼표 구분. 예: ``37.566536,126.977966`` )
   * - ``geo.location.distance``
     - 중심점에서의 검색 반경(단위 포함. 예: ``10km`` )

.. note::
   ``point`` 와 ``distance`` 는 쌍으로 지정합니다. ``distance`` 를 지정하지 않은 ``point`` 는 무시됩니다.
   또한 ``point`` 의 값은 "위도,경도" 의 두 숫자로 구성되어야 하며, 형식이 올바르지 않은 경우
   오류가 발생합니다.

.. note::
   같은 필드에 대해 여러 개의 ``point`` 를 지정한 경우 OR 조건(어느 범위 내), 여러 필드에 대해
   지정한 경우 AND 조건(모든 범위 내)으로 처리됩니다.

거리 단위
~~~~~~~~~

거리에는 다음 단위를 사용할 수 있습니다.

- ``km``: 킬로미터
- ``m``: 미터
- ``mi``: 마일
- ``yd``: 야드

.. note::
   거리 값은 OpenSearch에 그대로 전달되므로, 위 외에도 OpenSearch가 지원하는 단위
   ( ``cm`` , ``mm`` , ``ft`` , ``in`` , ``nmi`` 등)를 사용할 수 있습니다.

검색 결과 정렬 순서
~~~~~~~~~~~~~~~~~~~

위치 정보 검색은 지정한 범위 내의 문서로 결과를 필터링하는 **필터** 로 동작합니다.
검색 스코어(관련도)에는 영향을 미치지 않으며, 중심점에서 가까운 순으로 정렬하지는 않습니다.
결과는 일반적으로 관련도 순(또는 ``sort`` 파라미터로 지정한 순서)으로 반환됩니다.

.. note::
   |Fess| 는 거리에 의한 정렬(가까운 순 정렬)을 지원하지 않습니다.
   거리 순으로 표시하려면 응답에 포함된 위도·경도를 기반으로 클라이언트 측에서 정렬하십시오.

검색 예
=======

기본 검색
---------

서울역(37.566536, 126.977966)에서 반경 10km 이내의 문서를 검색하는 경우:

::

    http://localhost:8080/search?q=검색키워드&geo.location.point=37.566536,126.977966&geo.location.distance=10km

현재 위치 주변 검색
--------------------

사용자의 현재 위치에서 1km 이내를 검색하는 경우:

::

    http://localhost:8080/search?q=카페&geo.location.point=37.566536,126.977966&geo.location.distance=1km

API 사용
--------

v2 JSON 검색 API( ``/api/v2/search`` )에서도 위치 정보 검색을 사용할 수 있습니다.
``geo.location.point`` 와 ``geo.location.distance`` 를 요청 파라미터로 지정합니다.

::

    curl "http://localhost:8080/api/v2/search?q=호텔&geo.location.point=37.566536,126.977966&geo.location.distance=5km"

검색 결과는 공통 엔벨로프의 ``response.data`` 배열로 반환됩니다. API의 자세한 내용은 :doc:`../api/api-search`
및 :doc:`../api/api-overview` 를 참조하십시오.

.. note::
   ``location`` 필드는 기본적으로 API 응답에 포함되지 않습니다. 검색 결과에 위도·경도를 포함하려면
   ``fess_config.properties`` 에 다음 설정을 추가하십시오.

   ::

       query.additional.api.response.fields=location

필드 이름 사용자 정의
======================

기본 필드 이름 변경
-------------------

위치 정보 검색에서 사용하는 필드 이름을 변경하는 경우
``fess_config.properties`` 에서 다음 설정을 변경합니다.

::

    query.geo.fields=location

여러 필드 이름을 지정하는 경우 쉼표로 구분하여 지정합니다.

::

    query.geo.fields=location,geo_point,coordinates

.. note::
   - 요청 파라미터 이름은 설정한 필드 이름과 연동됩니다. 예를 들어
     ``query.geo.fields=coordinates`` 로 설정한 경우, ``geo.coordinates.point`` 및
     ``geo.coordinates.distance`` 를 지정합니다.
   - 여기서 지정하는 각 필드는 인덱스 매핑에서 ``geo_point`` 타입으로
     정의되어 있어야 합니다.

구현 예
=======

웹 애플리케이션에서의 구현
--------------------------

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

.. note::
   이 예에서는 검색 결과에서 ``location`` 필드를 참조합니다. 사전에
   ``query.additional.api.response.fields=location`` 을 설정하여 응답에 위도·경도를
   포함해 두어야 합니다.

.. code-block:: javascript

    // 지도 초기화
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.566536, lng: 126.977966},
        zoom: 13
    });

    // Fess v2 검색 API로 위치 정보 검색 실행
    fetch('/api/v2/search?q=매장&geo.location.point=37.566536,126.977966&geo.location.distance=5km')
        .then(response => response.json())
        .then(json => {
            // 검색 결과(response.data 배열)를 마커로 표시
            json.response.data.forEach(doc => {
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
===========

인덱스 설정 확인
----------------

위치 정보 필드는 설치 경로의
``app/WEB-INF/classes/fess_indices/fess/doc.json`` 에서 ``geo_point`` 타입으로 정의되어 있습니다.

::

    "location": {
        "type": "geo_point"
    }

``geo_point`` 타입의 필드는 BKD 트리로 인덱싱되므로, geo-distance 쿼리는
효율적으로 실행됩니다.

검색 범위와 응답 최적화
------------------------

검색 반경을 크게 할수록 범위 내에 해당하는 문서 수가 증가하여, 결과를 가져오고 렌더링하는 데
시간이 걸릴 수 있습니다.

- 용도에 맞게 적절한 검색 반경을 설정하십시오.
- 지도 표시 등에서 많은 결과를 처리하는 경우, 페이지 크기( ``num`` 파라미터)를 조정하여
  가져오는 건수를 제한하십시오.

문제 해결
==========

위치 정보 검색이 작동하지 않음
-------------------------------

1. ``location`` 필드에 데이터가 올바르게 저장되어 있는지 확인하십시오.
2. 위도·경도의 형식이 올바른지 확인하십시오( ``위도,경도`` 의 쉼표 구분. 값이 두 개가 아닌 경우 오류가 발생합니다).
3. OpenSearch의 인덱스 매핑에서 ``location`` 이 ``geo_point`` 타입으로 정의되어 있는지 확인하십시오.
4. ``point`` 와 ``distance`` 를 모두 지정하고 있는지 확인하십시오( ``distance`` 가 없는 ``point`` 는 무시됩니다).

검색 결과가 반환되지 않음
--------------------------

1. 지정한 거리 범위 내에 문서가 존재하는지 확인하십시오.
2. 위도·경도 값이 올바른 범위 내(위도: -90~90, 경도: -180~180)인지 확인하십시오.
3. 거리 단위가 올바르게 지정되어 있는지 확인하십시오.

API 응답에 위치 정보가 포함되지 않음
--------------------------------------

``location`` 필드는 기본적으로 API 응답에 포함되지 않습니다.
검색 결과에 위도·경도를 포함하려면 ``fess_config.properties`` 에
``query.additional.api.response.fields=location`` 을 설정하십시오.

위치 정보가 올바르게 등록되지 않음
------------------------------------

1. 크롤 시 ``location`` 필드가 올바르게 설정되어 있는지 확인하십시오.
2. 데이터 소스의 위도·경도가 올바르게 가져와지고 있는지 확인하십시오.
3. 스크립트로 위치 정보를 설정하는 경우, ``위도,경도`` 의 문자열 형식인지 확인하십시오.

참고 정보
=========

위치 정보 검색의 자세한 내용은 다음 리소스를 참조하십시오.

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/ko/docs/Web/API/Geolocation_API>`_
