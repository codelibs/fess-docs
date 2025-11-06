============
位置情報検索
============

概要
====

|Fess| は、緯度経度の位置情報を持つドキュメントに対して、地理的な範囲を指定した検索を実行できます。
この機能を使用することで、特定の地点から一定の距離内にあるドキュメントを検索したり、
Googleマップなどの地図サービスと連携した検索システムを構築できます。

ユースケース
============

位置情報検索は、以下のような用途に活用できます。

- 店舗検索: ユーザーの現在地から近い店舗を検索
- 不動産検索: 特定の駅や施設から一定距離内の物件を検索
- イベント検索: 指定した場所周辺のイベント情報を検索
- 施設検索: 観光スポットや公共施設の近隣検索

設定方法
========

インデックス生成時の設定
------------------------

位置情報フィールドの定義
~~~~~~~~~~~~~~~~~~~~~~~~

|Fess| では、位置情報を格納するフィールドとして ``location`` が標準で定義されています。
このフィールドは OpenSearch の ``geo_point`` 型として設定されています。

位置情報の登録形式
~~~~~~~~~~~~~~~~~~

インデックス生成時に、緯度と経度をカンマ区切りで ``location`` フィールドに設定します。

**形式:**

::

    緯度,経度

**例:**

::

    45.17614,-93.87341

.. note::
   緯度は -90 から 90 の範囲、経度は -180 から 180 の範囲で指定します。

データストアクロールでの設定例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

データストアクロールを使用する場合、位置情報を持つデータソースから ``location`` フィールドに
緯度経度を設定します。

**例: データベースからの取得**

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) as location
    FROM stores

スクリプトでの位置情報追加
~~~~~~~~~~~~~~~~~~~~~~~~~~

クロール設定のスクリプト機能を使用して、ドキュメントに位置情報を動的に追加することもできます。

::

    // 緯度経度を location フィールドに設定
    doc.location = "35.681236,139.767125";

検索時の設定
------------

位置情報検索を実行するには、リクエストパラメータで検索の中心点と範囲を指定します。

リクエストパラメータ
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメータ名
     - 説明
   * - ``geo.location.point``
     - 検索の中心となる地点の緯度・経度(カンマ区切り)
   * - ``geo.location.distance``
     - 中心点からの検索半径(単位付き)

距離の単位
~~~~~~~~~~

距離には以下の単位を使用できます。

- ``km``: キロメートル
- ``m``: メートル
- ``mi``: マイル
- ``yd``: ヤード

検索例
======

基本的な検索
------------

東京駅(35.681236, 139.767125)から半径10km以内のドキュメントを検索する場合:

::

    http://localhost:8080/search?q=検索キーワード&geo.location.point=35.681236,139.767125&geo.location.distance=10km

現在地周辺の検索
----------------

ユーザーの現在地から1km以内を検索する場合:

::

    http://localhost:8080/search?q=ラーメン&geo.location.point=35.681236,139.767125&geo.location.distance=1km

距離によるソート
----------------

検索結果を距離順にソートする場合は、``sort`` パラメータを使用します。

::

    http://localhost:8080/search?q=コンビニ&geo.location.point=35.681236,139.767125&geo.location.distance=5km&sort=location.distance

APIでの使用
-----------

JSON APIでも位置情報検索を使用できます。

::

    curl -X POST "http://localhost:8080/json/?q=ホテル" \
      -H "Content-Type: application/json" \
      -d '{
        "geo.location.point": "35.681236,139.767125",
        "geo.location.distance": "5km"
      }'

フィールド名のカスタマイズ
==========================

デフォルトのフィールド名変更
----------------------------

位置情報検索で使用するフィールド名を変更する場合は、
``fess_config.properties`` で以下の設定を変更します。

::

    query.geo.fields=location

複数のフィールド名を指定する場合は、カンマ区切りで指定します。

::

    query.geo.fields=location,geo_point,coordinates

実装例
======

Webアプリケーションでの実装
---------------------------

JavaScriptで現在地を取得して検索する例:

.. code-block:: javascript

    // ブラウザのGeolocation APIで現在地を取得
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const distance = "5km";

        // 検索URLの構築
        const searchUrl = `/search?q=&geo.location.point=${latitude},${longitude}&geo.location.distance=${distance}`;

        // 検索実行
        window.location.href = searchUrl;
    });

Googleマップとの連携
--------------------

検索結果をGoogleマップ上にマーカーで表示する例:

.. code-block:: javascript

    // 地図の初期化
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Fess APIで位置情報検索を実行
    fetch('/json/?q=店舗&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(data => {
            // 検索結果をマーカーとして表示
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

パフォーマンス最適化
====================

インデックス設定の最適化
------------------------

大量の位置情報データを扱う場合は、インデックスの設定を最適化します。

``app/WEB-INF/classes/fess_indices/fess.json`` で位置情報フィールドの設定を確認してください。

::

    "location": {
        "type": "geo_point"
    }

検索範囲の制限
--------------

パフォーマンスを考慮して、検索範囲は必要最小限に設定することを推奨します。

- 広範囲の検索(50km以上)は処理に時間がかかる可能性があります
- 用途に応じて適切な範囲を設定してください

トラブルシューティング
======================

位置情報検索が動作しない
------------------------

1. ``location`` フィールドにデータが正しく格納されているか確認してください。
2. 緯度経度の形式が正しいか確認してください(カンマ区切り)。
3. OpenSearch のインデックスマッピングで ``location`` が ``geo_point`` 型として定義されているか確認してください。

検索結果が返ってこない
----------------------

1. 指定した距離の範囲内にドキュメントが存在するか確認してください。
2. 緯度経度の値が正しい範囲内(緯度: -90〜90, 経度: -180〜180)か確認してください。
3. 距離の単位が正しく指定されているか確認してください。

位置情報が正しく表示されない
----------------------------

1. クロール時に ``location`` フィールドが正しく設定されているか確認してください。
2. データソースの緯度経度のデータ型が数値型であることを確認してください。
3. スクリプトで位置情報を設定する場合、文字列結合の形式が正しいか確認してください。

参考情報
========

位置情報検索の詳細については、以下のリソースを参照してください。

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/ja/docs/Web/API/Geolocation_API>`_
