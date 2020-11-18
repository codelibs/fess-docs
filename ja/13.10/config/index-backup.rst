==================
インデックスの管理
==================

インデックスのバックアップとリストア
====================================

|Fess| で扱うデータは elasticsearch のインデックスとして管理されています。
インデックスのバックアップ方法に関しては、elasticsearch がスナップショット機能として提供しています。
手順等の情報は `スナップショット機能 <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html>`_ を参照してください。

一部の設定は app/WEB-INF/conf/system.properties または /etc/fess/system.properties に保存されます。
データ移行する際には必要に応じて、これらのファイルもコピーしてください。

