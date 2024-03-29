============
位置情報検索
============

概要
====

緯度経度の位置情報を持つドキュメントをGoogleマップなどと連携して、位置情報検索を利用することができます。

設定
====

インデックス生成時
------------------

位置情報を格納するフィードとして `location` が定義されています。
インデックス生成時に 緯度経度を ``45.17614,-93.87341`` のような形式で
`location` フィードに設定して、ドキュメントを登録します。

検索時
------

位置情報を用いて検索を行う場合は、リクエストパラメーターの `geo.location.point` と `geo.location.distance` に値を指定します。
`geo.location.point` に緯度・経度の組を与え、 `geo.location.distance` にその地点からの距離を与えることで、
ある地点から一定の範囲内の位置情報をもつデータを対象に検索できます。
与えられる数値はDouble型として扱われます。


**例:**

::

    geo.location.point=35.681,139.766&geo.location.distance=10.0km

をリクエストパラメーターとして指定すると、(35.681, 139.766) の地点から半径10kmの範囲内の位置情報をもつドキュメントを対象として検索ができます。
