==================
インデックスの管理
==================

インデックスのバックアップとリストア
====================================

|Fess| で扱うデータは OpenSearch のインデックスとして管理されています。
インデックスのバックアップ方法に関しては、OpenSearch がスナップショット機能として提供しています。
手順等の情報は `スナップショット機能 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_ を参照してください。

一部の設定は app/WEB-INF/conf/system.properties または /etc/fess/system.properties に保存されます。
データ移行する際には必要に応じて、これらのファイルもコピーしてください。
