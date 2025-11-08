============
位置信息搜索
============

概述
====

|Fess| 可以对具有经纬度位置信息的文档执行指定地理范围的搜索。
使用此功能可以搜索距离特定地点一定距离内的文档,
或构建与 Google 地图等地图服务集成的搜索系统。

用例
============

位置信息搜索可用于以下用途。

- 店铺搜索: 搜索距用户当前位置较近的店铺
- 房地产搜索: 搜索距特定车站或设施一定距离内的房产
- 活动搜索: 搜索指定地点周边的活动信息
- 设施搜索: 搜索旅游景点或公共设施附近

配置方法
========

索引生成时的配置
------------------------

位置信息字段定义
~~~~~~~~~~~~~~~~~~~~~~~~

在 |Fess| 中,``location`` 作为存储位置信息的字段已标准定义。
此字段被配置为 OpenSearch 的 ``geo_point`` 类型。

位置信息注册格式
~~~~~~~~~~~~~~~~~~

索引生成时,将纬度和经度用逗号分隔设置到 ``location`` 字段中。

**格式:**

::

    纬度,经度

**示例:**

::

    45.17614,-93.87341

.. note::
   纬度范围为 -90 到 90,经度范围为 -180 到 180。

数据存储爬取的配置示例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用数据存储爬取时,从具有位置信息的数据源将
经纬度设置到 ``location`` 字段。

**示例: 从数据库获取**

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) as location
    FROM stores

脚本添加位置信息
~~~~~~~~~~~~~~~~~~

也可以使用爬取配置的脚本功能动态向文档添加位置信息。

::

    // 将经纬度设置到 location 字段
    doc.location = "35.681236,139.767125";

搜索时的配置
------------

要执行位置信息搜索,需在请求参数中指定搜索中心点和范围。

请求参数
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数名
     - 说明
   * - ``geo.location.point``
     - 搜索中心地点的纬度·经度(逗号分隔)
   * - ``geo.location.distance``
     - 距中心点的搜索半径(带单位)

距离单位
~~~~~~~~~~

距离可使用以下单位。

- ``km``: 千米
- ``m``: 米
- ``mi``: 英里
- ``yd``: 码

搜索示例
======

基本搜索
------------

搜索东京站(35.681236, 139.767125)半径10km内的文档:

::

    http://localhost:8080/search?q=搜索关键词&geo.location.point=35.681236,139.767125&geo.location.distance=10km

当前位置周边搜索
----------------

搜索距用户当前位置1km内的内容:

::

    http://localhost:8080/search?q=拉面&geo.location.point=35.681236,139.767125&geo.location.distance=1km

按距离排序
----------------

要按距离对搜索结果排序,请使用 ``sort`` 参数。

::

    http://localhost:8080/search?q=便利店&geo.location.point=35.681236,139.767125&geo.location.distance=5km&sort=location.distance

API 使用
-----------

JSON API 也可以使用位置信息搜索。

::

    curl -X POST "http://localhost:8080/json/?q=酒店" \
      -H "Content-Type: application/json" \
      -d '{
        "geo.location.point": "35.681236,139.767125",
        "geo.location.distance": "5km"
      }'

字段名自定义
==========================

更改默认字段名
----------------------------

要更改位置信息搜索使用的字段名,
请在 ``fess_config.properties`` 中修改以下配置。

::

    query.geo.fields=location

指定多个字段名时,请用逗号分隔。

::

    query.geo.fields=location,geo_point,coordinates

实现示例
======

Web 应用程序实现
---------------------------

JavaScript 获取当前位置并搜索的示例:

.. code-block:: javascript

    // 使用浏览器的 Geolocation API 获取当前位置
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const distance = "5km";

        // 构建搜索 URL
        const searchUrl = `/search?q=&geo.location.point=${latitude},${longitude}&geo.location.distance=${distance}`;

        // 执行搜索
        window.location.href = searchUrl;
    });

Google 地图集成
--------------------

在 Google 地图上用标记显示搜索结果的示例:

.. code-block:: javascript

    // 初始化地图
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // 使用 Fess API 执行位置信息搜索
    fetch('/json/?q=店铺&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(data => {
            // 将搜索结果显示为标记
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

性能优化
====================

索引配置优化
------------------------

处理大量位置信息数据时,请优化索引配置。

请在 ``app/WEB-INF/classes/fess_indices/fess.json`` 中确认位置信息字段的配置。

::

    "location": {
        "type": "geo_point"
    }

搜索范围限制
--------------

考虑性能,建议将搜索范围设置为必要的最小值。

- 大范围搜索(50km以上)可能需要较长处理时间
- 请根据用途设置适当的范围

故障排除
======================

位置信息搜索无法工作
------------------------

1. 请确认 ``location`` 字段中是否正确存储了数据。
2. 请确认纬度经度格式是否正确(逗号分隔)。
3. 请确认 OpenSearch 的索引映射中 ``location`` 是否定义为 ``geo_point`` 类型。

搜索结果未返回
----------------------

1. 请确认指定距离范围内是否存在文档。
2. 请确认纬度经度值是否在正确范围内(纬度: -90〜90, 经度: -180〜180)。
3. 请确认距离单位是否正确指定。

位置信息未正确显示
----------------------------

1. 请确认爬取时 ``location`` 字段是否正确设置。
2. 请确认数据源的纬度经度数据类型是否为数值类型。
3. 使用脚本设置位置信息时,请确认字符串连接格式是否正确。

参考信息
========

有关位置信息搜索的详细信息,请参考以下资源。

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/ja/docs/Web/API/Geolocation_API>`_
