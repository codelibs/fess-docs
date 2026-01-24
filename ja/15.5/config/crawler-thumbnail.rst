===============
サムネイル画像の設定
===============

概要
====

|Fess| では検索結果のサムネイル画像を表示することができます。
サムネイル画像は検索結果のMIME Typeを元に生成されます。
サポートしているMIME Typeであれば、検索結果の表示時にサムネイル画像を生成します。
サムネイル画像を生成する処理はMIME Typeごとに設定して追加することができます。

サムネイル画像を表示するためには、管理者としてログインして、全般の設定でサムネイル表示を有効にして保存してください。

サポートしているファイル形式
========================

画像ファイル
----------

.. list-table::
   :widths: 15.50 20
   :header-rows: 1

   * - 形式
     - MIMEタイプ
     - 説明
   * - JPEG
     - ``image/jpeg``
     - 写真など
   * - PNG
     - ``image/png``
     - 透過画像など
   * - GIF
     - ``image/gif``
     - アニメーションGIF含む
   * - BMP
     - ``image/bmp``, ``image/x-windows-bmp``, ``image/x-ms-bmp``
     - ビットマップ画像
   * - TIFF
     - ``image/tiff``
     - 高品質画像
   * - SVG
     - ``image/svg+xml``
     - ベクター画像
   * - Photoshop
     - ``image/vnd.adobe.photoshop``, ``image/photoshop``, ``application/x-photoshop``, ``application/photoshop``
     - PSDファイル

ドキュメントファイル
----------------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - 形式
     - MIMEタイプ
     - 説明
   * - PDF
     - ``application/pdf``
     - PDFドキュメント
   * - Word
     - ``application/msword``, ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - Word文書
   * - Excel
     - ``application/vnd.ms-excel``, ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - Excelスプレッドシート
   * - PowerPoint
     - ``application/vnd.ms-powerpoint``, ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - PowerPointプレゼンテーション
   * - RTF
     - ``application/rtf``
     - リッチテキスト
   * - PostScript
     - ``application/postscript``
     - PostScriptファイル

HTMLコンテンツ
------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - 形式
     - MIMEタイプ
     - 説明
   * - HTML
     - ``text/html``
     - HTMLページ内の埋め込み画像からサムネイルを生成

必要な外部ツール
==============

サムネイル生成には、以下の外部ツールが必要です。使用するファイル形式に応じてインストールしてください。

基本ツール（必須）
---------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - ツール
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - ImageMagick
     - 画像変換・リサイズ
     - ``apt install imagemagick``
     - ``brew install imagemagick``

.. note::

   ImageMagick 6（``convert`` コマンド）とImageMagick 7（``magick`` コマンド）の両方に対応しています。

SVGサポート
----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - ツール
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - rsvg-convert
     - SVG→PNG変換
     - ``apt install librsvg2-bin``
     - ``brew install librsvg``

PDFサポート
----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - ツール
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - pdftoppm
     - PDF→PNG変換
     - ``apt install poppler-utils``
     - ``brew install poppler``

MS Officeサポート
----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - ツール
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - unoconv
     - Office→PDF変換
     - ``apt install unoconv``
     - ``brew install unoconv``
   * - pdftoppm
     - PDF→PNG変換
     - ``apt install poppler-utils``
     - ``brew install poppler``

Redhat系OSの場合は以下のパッケージをインストールします。

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick poppler-utils

PostScriptサポート
-----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - ツール
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - ps2pdf
     - PS→PDF変換
     - ``apt install ghostscript``
     - ``brew install ghostscript``
   * - pdftoppm
     - PDF→PNG変換
     - ``apt install poppler-utils``
     - ``brew install poppler``

HTMLファイルのサムネイル画像
========================

HTMLのサムネイル画像はHTML内で指定された画像または含まれている画像を利用します。
以下の順にサムネイル画像を探して指定されている場合に表示します。

1. name属性がthumbnailで指定されたmetaタグのcontentの値
2. property属性がog:imageで指定されたmetaタグのcontentの値
3. imgタグでサムネイルに適したサイズの画像

設定
====

設定ファイル
----------

サムネイルジェネレータの設定は ``fess_thumbnail.xml`` で行います。

::

    src/main/resources/fess_thumbnail.xml

主な設定項目（fess_config.properties）
----------------------------------

``app/WEB-INF/classes/fess_config.properties`` または ``/etc/fess/fess_config.properties`` で以下の項目を設定できます。

::

    # サムネイル画像の最小幅（ピクセル）
    thumbnail.html.image.min.width=100

    # サムネイル画像の最小高さ（ピクセル）
    thumbnail.html.image.min.height=100

    # 最大アスペクト比（幅:高さまたは高さ:幅）
    thumbnail.html.image.max.aspect.ratio=3.0

    # 生成されるサムネイルの幅
    thumbnail.html.image.thumbnail.width=100

    # 生成されるサムネイルの高さ
    thumbnail.html.image.thumbnail.height=100

    # 出力フォーマット
    thumbnail.html.image.format=png

    # HTML内の画像を抽出するXPath
    thumbnail.html.image.xpath=//IMG

    # 除外する拡張子
    thumbnail.html.image.exclude.extensions=svg,html,css,js

    # サムネイル生成の間隔（ミリ秒）
    thumbnail.generator.interval=0

    # コマンド実行タイムアウト（ミリ秒）
    thumbnail.command.timeout=30000

    # プロセス破棄タイムアウト（ミリ秒）
    thumbnail.command.destroy.timeout=5000

generate-thumbnail スクリプト
============================

概要
----

``generate-thumbnail`` は、実際のサムネイル生成を行うシェルスクリプトです。
RPM/Debパッケージでインストールすると、 ``/usr/share/fess/bin/generate-thumbnail`` にインストールされます。

使用方法
-------

::

    generate-thumbnail <type> <url> <output_file> [mimetype]

引数
----

.. list-table::
   :widths: 15.50 30
   :header-rows: 1

   * - 引数
     - 説明
     - 例
   * - ``type``
     - ファイルタイプ
     - ``image``, ``svg``, ``pdf``, ``msoffice``, ``ps``
   * - ``url``
     - 入力ファイルのURL
     - ``file:/path/to/file.jpg``
   * - ``output_file``
     - 出力ファイルパス
     - ``/var/lib/fess/thumbnails/_0/_1/abc.png``
   * - ``mimetype``
     - MIMEタイプ（オプション）
     - ``image/gif``

サポートするタイプ
----------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - タイプ
     - 説明
     - 使用ツール
   * - ``image``
     - 画像ファイル
     - ImageMagick (convert/magick)
   * - ``svg``
     - SVGファイル
     - rsvg-convert
   * - ``pdf``
     - PDFファイル
     - pdftoppm + ImageMagick
   * - ``msoffice``
     - MS Officeファイル
     - unoconv + pdftoppm + ImageMagick
   * - ``ps``
     - PostScriptファイル
     - ps2pdf + pdftoppm + ImageMagick

使用例
-----

::

    # 画像ファイルのサムネイル生成
    ./generate-thumbnail image file:/path/to/image.jpg /tmp/thumbnail.png image/jpeg

    # SVGファイルのサムネイル生成
    ./generate-thumbnail svg file:/path/to/image.svg /tmp/thumbnail.png

    # PDFファイルのサムネイル生成
    ./generate-thumbnail pdf file:/path/to/document.pdf /tmp/thumbnail.png

    # GIFファイル（MIMEタイプを指定してフォーマットヒントを有効化）
    ./generate-thumbnail image file:/path/to/image.gif /tmp/thumbnail.png image/gif

サムネイル保存先
==============

デフォルトパス
------------

::

    ${FESS_VAR_PATH}/thumbnails/

または

::

    /var/lib/fess/thumbnails/

ディレクトリ構造
--------------

サムネイルはハッシュベースのディレクトリ構造で保存されます。

::

    thumbnails/
    ├── _0/
    │   ├── _1/
    │   │   ├── _2/
    │   │   │   └── _3/
    │   │   │       └── abcdef123456.png
    │   │   └── ...
    │   └── ...
    └── ...

サムネイルジョブの無効化
====================

サムネイルジョブを無効化する場合は以下を設定します。

1. 管理画面の システム > 全般 で「サムネイル表示」のチェックを外し、「更新」ボタンをクリック。
2. ``app/WEB-INF/classes/fess_config.properties`` または ``/etc/fess/fess_config.properties`` の ``thumbnail.crawler.enabled`` に ``false`` を設定。

::

    thumbnail.crawler.enabled=false

3. Fessのサービスを再起動。

トラブルシューティング
==================

サムネイルが生成されない
---------------------

1. **外部ツールの確認**

::

    # ImageMagickの確認
    which convert || which magick

    # rsvg-convertの確認（SVG用）
    which rsvg-convert

    # pdftoppmの確認（PDF用）
    which pdftoppm

2. **ログの確認**

::

    ${FESS_LOG_PATH}/fess-thumbnail.log

3. **手動でスクリプトを実行**

::

    /usr/share/fess/bin/generate-thumbnail image file:/path/to/test.jpg /tmp/test_thumbnail.png image/jpeg

GIF/TIFFでエラーが発生する
------------------------

ImageMagick 6を使用している場合、MIMEタイプを指定してフォーマットヒントを有効にしてください。Fessの設定が正しければ自動的に行われます。

エラー例::

    convert-im6.q16: corrupt image `/tmp/thumbnail_xxx' @ error/gif.c/DecodeImage/512

対処法:

- ImageMagick 7にアップグレード
- または、MIMEタイプが正しく渡されていることを確認

SVGのサムネイルが生成されない
--------------------------

1. ``rsvg-convert`` がインストールされているか確認

::

    which rsvg-convert

2. 手動で変換をテスト

::

    rsvg-convert -w 100 -h 100 --keep-aspect-ratio input.svg -o output.png

権限エラー
---------

サムネイル保存ディレクトリの権限を確認します。

::

    ls -la /var/lib/fess/thumbnails/

必要に応じて権限を修正します。

::

    chown -R fess:fess /var/lib/fess/thumbnails/
    chmod -R 755 /var/lib/fess/thumbnails/

プラットフォーム対応
=================

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - プラットフォーム
     - 対応状況
     - 備考
   * - Linux
     - 完全対応
     - \-
   * - macOS
     - 完全対応
     - Homebrewで外部ツールをインストール
   * - Windows
     - 非対応
     - bashスクリプトのため
