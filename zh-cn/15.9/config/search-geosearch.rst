============
位置信息搜索
============

概述
====

|Fess| 可以对具有经纬度位置信息的文档执行指定地理范围的搜索。
使用此功能可以搜索距离特定地点一定距离内的文档,
或构建与 Google 地图等地图服务集成的搜索系统。

在内部,使用 OpenSearch 的 geo-distance 查询,对存在于指定中心点
指定距离以内的文档进行筛选。

用例
====

位置信息搜索可用于以下用途。

- 店铺搜索: 搜索距用户当前位置较近的店铺
- 房地产搜索: 搜索距特定车站或设施一定距离内的房产
- 活动搜索: 搜索指定地点周边的活动信息
- 设施搜索: 搜索旅游景点或公共设施附近

配置方法
========

索引生成时的配置
----------------

位置信息字段定义
~~~~~~~~~~~~~~~~

在 |Fess| 中,\ ``location`` 作为存储位置信息的字段已标准定义。
此字段被配置为 OpenSearch 的 ``geo_point`` 类型。

位置信息注册格式
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~

使用数据存储爬取时,从具有位置信息的数据源将经纬度设置到 ``location`` 字段。

**示例: 从数据库获取**

如果纬度和经度分别保存在不同的列中,请在 SQL 中将其拼接为逗号分隔的字符串。

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) AS location
    FROM stores

在数据存储配置脚本中,将获取到的值映射到 ``location`` 字段。

::

    location=data.location

通过脚本添加位置信息
~~~~~~~~~~~~~~~~~~~~

也可以使用爬取配置的脚本功能（Groovy）动态向文档添加位置信息。
直接向字段名赋值即可。

::

    // 将经纬度设置到 location 字段
    location="35.681236,139.767125"

有关脚本的详细信息,请参阅 :doc:`scripting-groovy`。

搜索时的配置
------------

要执行位置信息搜索,需在请求参数中指定搜索中心点和范围。

请求参数
~~~~~~~~

位置信息搜索的参数名格式为 ``geo.<字段名>.point`` 和 ``geo.<字段名>.distance``\ 。
``<字段名>`` 处填写通过 ``query.geo.fields`` 配置的字段名
（默认为 ``location``）。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数名
     - 说明
   * - ``geo.location.point``
     - 搜索中心地点的纬度·经度（逗号分隔。示例: ``35.681236,139.767125`` ）
   * - ``geo.location.distance``
     - 距中心点的搜索半径（带单位。示例: ``10km`` ）

.. note::
   ``point`` 和 ``distance`` 须成对指定。未指定 ``distance`` 的 ``point`` 将被忽略。
   此外, ``point`` 的值必须由"纬度,经度"两个数值组成,格式不正确时将报错。

.. note::
   对同一字段指定多个 ``point`` 时为 OR 条件（位于任一范围内），
   对多个字段分别指定时为 AND 条件（同时位于所有范围内）。

距离单位
~~~~~~~~

距离可使用以下单位。

- ``km``: 千米
- ``m``: 米
- ``mi``: 英里
- ``yd``: 码

.. note::
   距离值将直接传递给 OpenSearch,因此除上述单位外,还可使用 OpenSearch 支持的其他单位
   （ ``cm`` 、 ``mm`` 、 ``ft`` 、 ``in`` 、 ``nmi`` 等）。

搜索结果的排序顺序
~~~~~~~~~~~~~~~~~~

位置信息搜索作为 **过滤器** 运行,将结果限定为指定范围内的文档。
它不影响搜索评分（相关度），也不会按距中心点的远近进行排序。
结果将按常规方式以相关度顺序（或 ``sort`` 参数指定的顺序）返回。

.. note::
   |Fess| 不支持按距离排序（按由近到远排列）。
   如需按距离顺序显示,请在客户端根据响应中包含的经纬度自行排序。

搜索示例
========

基本搜索
--------

搜索东京站（35.681236, 139.767125）半径 10km 内的文档:

::

    http://localhost:8080/search?q=搜索关键词&geo.location.point=35.681236,139.767125&geo.location.distance=10km

当前位置周边搜索
----------------

搜索距用户当前位置 1km 内的内容:

::

    http://localhost:8080/search?q=拉面&geo.location.point=35.681236,139.767125&geo.location.distance=1km

通过 API 使用
-------------

v2 JSON 搜索 API（ ``/api/v2/search`` ）同样支持位置信息搜索。
将 ``geo.location.point`` 和 ``geo.location.distance`` 作为请求参数指定即可。

::

    curl "http://localhost:8080/api/v2/search?q=酒店&geo.location.point=35.681236,139.767125&geo.location.distance=5km"

搜索结果通过公共信封的 ``response.data`` 数组返回。API 的详细信息请参阅 :doc:`../api/api-search`
和 :doc:`../api/api-overview`。

.. note::
   ``location`` 字段默认不包含在 API 响应中。如需在搜索结果中包含经纬度,
   请在 ``fess_config.properties`` 中添加以下配置。

   ::

       query.additional.api.response.fields=location

字段名自定义
============

更改默认字段名
--------------

要更改位置信息搜索使用的字段名,
请在 ``fess_config.properties`` 中修改以下配置。

::

    query.geo.fields=location

指定多个字段名时,请用逗号分隔。

::

    query.geo.fields=location,geo_point,coordinates

.. note::
   - 请求参数名与所配置的字段名联动。例如,设置
     ``query.geo.fields=coordinates`` 时,需指定 ``geo.coordinates.point`` 和
     ``geo.coordinates.distance``\ 。
   - 此处指定的各字段必须在索引映射中定义为 ``geo_point`` 类型。

实现示例
========

Web 应用程序实现
----------------

JavaScript 获取当前位置并执行搜索的示例:

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
---------------

在 Google 地图上用标记显示搜索结果的示例:

.. note::
   此示例从搜索结果中引用 ``location`` 字段。需要事先设置
   ``query.additional.api.response.fields=location``,以便在响应中包含经纬度。

.. code-block:: javascript

    // 初始化地图
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // 使用 Fess v2 搜索 API 执行位置信息搜索
    fetch('/api/v2/search?q=店铺&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(json => {
            // 将搜索结果（response.data 数组）显示为标记
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

性能优化
========

确认索引设置
------------

位置信息字段在安装目录的
``app/WEB-INF/classes/fess_indices/fess/doc.json`` 中定义为 ``geo_point`` 类型。

::

    "location": {
        "type": "geo_point"
    }

``geo_point`` 类型的字段使用 BKD 树进行索引,因此 geo-distance 查询可高效执行。

搜索范围和响应的优化
--------------------

增大搜索半径时,范围内匹配的文档数量会增加,获取和渲染结果可能需要更长时间。

- 请根据用途设置适当的搜索半径。
- 在地图显示等需要处理大量结果的场景中,请调整页面大小（ ``num`` 参数）以限制获取数量。

故障排除
========

位置信息搜索无法工作
--------------------

1. 请确认 ``location`` 字段中是否正确存储了数据。
2. 请确认纬度经度格式是否正确（ ``纬度,经度`` 逗号分隔。值不为两个时将报错）。
3. 请确认 OpenSearch 的索引映射中 ``location`` 是否定义为 ``geo_point`` 类型。
4. 请确认是否同时指定了 ``point`` 和 ``distance``\ （未指定 ``distance`` 的 ``point`` 将被忽略）。

搜索结果未返回
--------------

1. 请确认指定距离范围内是否存在文档。
2. 请确认纬度经度值是否在正确范围内（纬度: -90〜90, 经度: -180〜180）。
3. 请确认距离单位是否正确指定。

API 响应中不包含位置信息
------------------------

``location`` 字段默认不包含在 API 响应中。
如需在搜索结果中包含经纬度,请在 ``fess_config.properties`` 中
设置 ``query.additional.api.response.fields=location``\ 。

位置信息未正确注册
------------------

1. 请确认爬取时 ``location`` 字段是否正确设置。
2. 请确认数据源的纬度经度是否能够正确获取。
3. 通过脚本设置位置信息时,请确认是否为 ``纬度,经度`` 的字符串格式。

参考信息
========

有关位置信息搜索的详细信息,请参考以下资源。

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/zh-CN/docs/Web/API/Geolocation_API>`_
