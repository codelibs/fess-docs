====================
サムネイル画像の設定
====================

サムネイル画像の表示
====================

|Fess| では検索結果のサムネイル画像を表示することができます。
サムネイル画像は検索結果のMIME Typeを元に生成されます。
サポートしているMIME Typeであれば、検索結果の表示時にサムネイル画像を生成します。
サムネイル画像を生成する処理はMIME Typeごとに設定して追加することができます。

サムネイル画像を表示するためには、管理者としてログインして、全般の設定でサムネイル表示を有効にして保存してください。

HTMLファイルのサムネイル画像
============================

HTMLのサムネイル画像はHTML内で指定された画像または含まれている画像を利用します。
以下の順にサムネイル画像を探して指定されている場合に表示します。

- name属性がthumbnailで指定されたmetaタグののcontentの値
- property属性がog:imageで指定されたmetaタグののcontentの値
- imgタグでサムネイルに適したサイズの画像


MS Officeファイルのサムネイル画像
=================================

MS Office系のサムネイル画像は LibreOffice および ImageMagick を用いて生成されます。
unoconv と convert コマンドがインストールされている場合、サムネイル画像が生成されます。

パッケージのインストール
------------------------

Redhat系OSの場合、画像の作成用に以下のパッケージをインストールします。

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

生成スクリプト
--------------

RPM/Debパッケージでインストールすると、MS Office用のサムネイル生成スクリプトは/usr/share/fess/bin/generate-thumbnailにインストールされます。

PDFファイルのサムネイル画像
===========================

PDFのサムネイル画像はImageMagickを用いて生成されます。
convert コマンドがインストールされている場合、サムネイル画像が生成されます。

サムネイルジョブの無効化
=========================

サムネイルジョブを無効化する場合は以下を設定します。

1. 管理画面の システム > 全般 で「サムネイル表示」のチェックを外し、「更新」ボタンをクリック。
2. ``app/WEB-INF/classes/fess_config.properties`` または ``/etc/fess/fess_config.properties`` の ``thumbnail.crawler.enabled`` に ``false`` を設定。

::

    thumbnail.crawler.enabled=false

3. Fessのサービスを再起動。
