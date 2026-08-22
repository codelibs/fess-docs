============
位置情報検索
============

概要
====

|Fess| は、緯度経度の位置情報を持つドキュメントに対して、地理的な範囲を指定した検索を実行できます。
この機能を使用することで、特定の地点から一定の距離内にあるドキュメントを検索したり、
Googleマップなどの地図サービスと連携した検索システムを構築できます。

内部的には、OpenSearch の geo-distance クエリを使用して、指定した中心点から指定した距離以内に
存在するドキュメントを絞り込みます。

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

緯度・経度を別々のカラムで保持している場合は、SQL でカンマ区切りの文字列に結合します。

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) AS location
    FROM stores

データストアの設定スクリプトで、取得した値を ``location`` フィールドにマッピングします。

::

    location=data.location

スクリプトでの位置情報追加
~~~~~~~~~~~~~~~~~~~~~~~~~~

クロール設定のスクリプト機能（Groovy）を使用して、ドキュメントに位置情報を動的に追加することもできます。
フィールド名に直接値を代入します。

::

    // 緯度経度を location フィールドに設定
    location="35.681236,139.767125"

スクリプトの詳細については :doc:`scripting-groovy` を参照してください。

検索時の設定
------------

位置情報検索を実行するには、リクエストパラメーターで検索の中心点と範囲を指定します。

リクエストパラメーター
~~~~~~~~~~~~~~~~~~~~~~

位置情報検索のパラメーター名は ``geo.<フィールド名>.point`` および ``geo.<フィールド名>.distance``
の形式です。 ``<フィールド名>`` には ``query.geo.fields`` で設定されたフィールド名が入ります
（既定は ``location`` ）。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター名
     - 説明
   * - ``geo.location.point``
     - 検索の中心となる地点の緯度・経度（カンマ区切り。例: ``35.681236,139.767125`` ）
   * - ``geo.location.distance``
     - 中心点からの検索半径（単位付き。例: ``10km`` ）

.. note::
   ``point`` と ``distance`` は対で指定します。 ``distance`` を指定しない ``point`` は無視されます。
   また、 ``point`` の値は「緯度,経度」の2つの数値で構成されている必要があり、形式が不正な場合は
   エラーになります。

.. note::
   同じフィールドに対して複数の ``point`` を指定した場合は OR 条件（いずれかの範囲内）、
   複数のフィールドに対して指定した場合は AND 条件（すべての範囲内）として扱われます。

距離の単位
~~~~~~~~~~

距離には以下の単位を使用できます。

- ``km``: キロメートル
- ``m``: メートル
- ``mi``: マイル
- ``yd``: ヤード

.. note::
   距離の値は OpenSearch にそのまま渡されるため、上記以外にも OpenSearch がサポートする単位
   （ ``cm`` 、 ``mm`` 、 ``ft`` 、 ``in`` 、 ``nmi`` など）を使用できます。

検索結果の並び順
~~~~~~~~~~~~~~~~

位置情報検索は、指定した範囲内のドキュメントに結果を絞り込む **フィルター** として動作します。
検索スコア（関連度）には影響せず、中心点からの距離が近い順に並べ替えるわけではありません。
結果は通常どおり関連度順（または ``sort`` パラメーターで指定した順序）で返ります。

.. note::
   |Fess| は距離によるソート（近い順の並べ替え）には対応していません。
   距離順に表示したい場合は、レスポンスに含めた緯度経度をもとに、クライアント側で並べ替えてください。

検索例
======

基本的な検索
------------

東京駅（35.681236, 139.767125）から半径10km以内のドキュメントを検索する場合:

::

    http://localhost:8080/search?q=検索キーワード&geo.location.point=35.681236,139.767125&geo.location.distance=10km

現在地周辺の検索
----------------

ユーザーの現在地から1km以内を検索する場合:

::

    http://localhost:8080/search?q=ラーメン&geo.location.point=35.681236,139.767125&geo.location.distance=1km

APIでの使用
-----------

v2 の JSON 検索 API（ ``/api/v2/search`` ）でも位置情報検索を使用できます。
``geo.location.point`` と ``geo.location.distance`` をリクエストパラメーターとして指定します。

::

    curl "http://localhost:8080/api/v2/search?q=ホテル&geo.location.point=35.681236,139.767125&geo.location.distance=5km"

検索結果は共通エンベロープの ``response.data`` 配列で返ります。API の詳細は :doc:`../api/api-search`
および :doc:`../api/api-overview` を参照してください。

.. note::
   ``location`` フィールドは、既定では API レスポンスに含まれません。検索結果に緯度経度を含めたい場合は、
   ``fess_config.properties`` に次の設定を追加してください。

   ::

       query.additional.api.response.fields=location

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

.. note::
   - リクエストパラメーター名は設定したフィールド名に連動します。たとえば
     ``query.geo.fields=coordinates`` と設定した場合は、 ``geo.coordinates.point`` および
     ``geo.coordinates.distance`` を指定します。
   - ここで指定する各フィールドは、インデックスのマッピングで ``geo_point`` 型として
     定義されている必要があります。

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

.. note::
   この例では検索結果から ``location`` フィールドを参照します。事前に
   ``query.additional.api.response.fields=location`` を設定して、レスポンスに緯度経度を
   含めておく必要があります。

.. code-block:: javascript

    // 地図の初期化
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Fess の v2 検索 API で位置情報検索を実行
    fetch('/api/v2/search?q=店舗&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(json => {
            // 検索結果（response.data 配列）をマーカーとして表示
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

パフォーマンス最適化
====================

インデックス設定の確認
----------------------

位置情報フィールドは、インストール先の
``app/WEB-INF/classes/fess_indices/fess/doc.json`` で ``geo_point`` 型として定義されています。

::

    "location": {
        "type": "geo_point"
    }

``geo_point`` 型のフィールドは BKD ツリーでインデックスされるため、geo-distance クエリは
効率的に実行されます。

検索範囲とレスポンスの最適化
----------------------------

検索半径を大きくすると、範囲内に該当するドキュメント数が増え、結果の取得・描画に時間が
かかる場合があります。

- 用途に応じて適切な検索半径を設定してください。
- 地図表示などで多くの結果を扱う場合は、ページサイズ（ ``num`` パラメーター）を調整して
  取得件数を制限してください。

トラブルシューティング
======================

位置情報検索が動作しない
------------------------

1. ``location`` フィールドにデータが正しく格納されているか確認してください。
2. 緯度経度の形式が正しいか確認してください（ ``緯度,経度`` のカンマ区切り。値が2つでない場合はエラーになります）。
3. OpenSearch のインデックスマッピングで ``location`` が ``geo_point`` 型として定義されているか確認してください。
4. ``point`` と ``distance`` の両方を指定しているか確認してください（ ``distance`` のない ``point`` は無視されます）。

検索結果が返ってこない
----------------------

1. 指定した距離の範囲内にドキュメントが存在するか確認してください。
2. 緯度経度の値が正しい範囲内（緯度: -90〜90, 経度: -180〜180）か確認してください。
3. 距離の単位が正しく指定されているか確認してください。

APIレスポンスに位置情報が含まれない
----------------------------------

``location`` フィールドは既定では API レスポンスに含まれません。
検索結果に緯度経度を含めるには、 ``fess_config.properties`` に
``query.additional.api.response.fields=location`` を設定してください。

位置情報が正しく登録されない
----------------------------

1. クロール時に ``location`` フィールドが正しく設定されているか確認してください。
2. データソースの緯度経度が正しく取得できているか確認してください。
3. スクリプトで位置情報を設定する場合、 ``緯度,経度`` の文字列形式になっているか確認してください。

参考情報
========

位置情報検索の詳細については、以下のリソースを参照してください。

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/ja/docs/Web/API/Geolocation_API>`_
