==================================
OCR（画像内の文字認識）の設定
==================================

概要
====

|Fess| は Apache Tika を使ってドキュメントからテキストを抽出します。
Tika の Tesseract OCR パーサーは |Fess| に同梱されており、これを有効にすると、画像やスキャンした PDF に含まれる文字を認識して検索対象にできます。

OCR は次の 2 つの条件がそろったときに実行されます。

- |Fess| のクローラープロセスが動作するホストに ``tesseract`` コマンドがインストールされている
- |Fess| で OCR が有効になっている

OCR はデフォルトでは無効です。
``tesseract`` がインストールされていない場合、|Fess| は OCR をスキップします。エラーにはなりません。

OCR の対象
==========

OCR を有効にすると、次のものが対象になります。

- 画像ファイル（PNG、JPEG、TIFF、GIF、BMP など）
- Tika が処理するドキュメントに埋め込まれた画像（Office ファイルなど）
- テキストレイヤーが空の PDF（スキャンした PDF）

スキャンした PDF の扱い
-----------------------

|Fess| は通常、PDFBox で PDF からテキストを抽出します。
OCR が有効で、PDFBox が PDF からまったくテキストを取得できなかった場合、|Fess| はその PDF を Tika で再抽出します。
このとき Tika がページを画像に変換し、OCR を実行します。

.. note::
   すでにテキストを含む PDF は OCR の対象になりません。
   一部のページだけがスキャン画像の PDF（混在した PDF）は対象外です。

Tesseract のインストール
========================

|Fess| を実行するホストに Tesseract をインストールします。
日本語の文字を認識するには、日本語の学習データ（traineddata）も必要です。

Debian / Ubuntu::

    $ sudo apt-get install tesseract-ocr tesseract-ocr-jpn

RHEL / Rocky Linux / AlmaLinux（EPEL を有効にしてください）::

    $ sudo dnf install tesseract tesseract-langpack-jpn

インストールされている言語は、次のコマンドで確認できます::

    $ tesseract --list-langs

OCR の有効化
============

``fess_config.properties`` に次のプロパティを設定します。

- ZIP 版: ``app/WEB-INF/classes/fess_config.properties``
- RPM/DEB 版: ``/etc/fess/fess_config.properties``

::

    # OCR を有効にする（デフォルト: false）
    crawler.document.ocr.enabled=true

    # Tesseract の言語（複数の場合は + で連結、デフォルト: eng）
    crawler.document.ocr.language=jpn+eng

    # Tesseract 1 回の実行のタイムアウト（秒、デフォルト: 120）
    crawler.document.ocr.timeout=120

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - プロパティ
     - デフォルト
     - 説明
   * - ``crawler.document.ocr.enabled``
     - ``false``
     - ``true`` にすると OCR を有効にします。
   * - ``crawler.document.ocr.language``
     - ``eng``
     - Tesseract の言語です。複数の言語は ``+`` で連結します（例: ``jpn+eng``）。対応する traineddata がインストールされている必要があります。
   * - ``crawler.document.ocr.timeout``
     - ``120``
     - Tesseract 1 回の実行（画像 1 枚、または PDF の 1 ページ）のタイムアウトです。単位は秒です。

これらの設定は、JVM のシステムプロパティとしても指定できます。
たとえば ``FESS_JAVA_OPTS`` に次のように指定します。Docker 環境で便利です。

::

    -Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng

.. note::
   設定を変更した後は、|Fess| を再起動してください。

Docker で使う場合
=================

Docker 環境で OCR を使うには、|Fess| のイメージに Tesseract を追加します。
`docker-fess <https://github.com/codelibs/docker-fess>`__ の ``compose/tesseract/Dockerfile`` を使って、Tesseract を追加したイメージをビルドします。

``compose/tesseract/Dockerfile`` の例::

    FROM ghcr.io/codelibs/fess:15.9.0

    RUN apk add --no-cache tesseract-ocr tesseract-ocr-data-osd tesseract-ocr-data-eng tesseract-ocr-data-jpn

``compose/compose.yaml`` では、``image:`` の行を ``build: ./tesseract`` に置き換え、``FESS_JAVA_OPTS`` の行を有効にします。
``build: ./playwright`` と同じ使い方です。

::

    services:
      fess01:
        # image: ghcr.io/codelibs/fess:15.9.0
        build: ./tesseract
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng"

変更後は、イメージを再ビルドしてコンテナーを起動します::

    $ docker compose up -d --build

.. note::
   ``-noble`` や ``-al2023`` など、Alpine 以外のベースイメージを使う場合は、``apk`` の代わりにそのディストリビューションのパッケージマネージャーで Tesseract を追加してください。

詳細は :doc:`../install/install-docker` を参照してください。

クロール設定ごとの設定
======================

クロール設定の「設定パラメーター」に ``config.tika.tesseract.config`` を指定すると、そのクロール設定に限って OCR の設定を上書きできます。

::

    config.tika.tesseract.config=tesseract.properties

``tesseract.properties`` はクラスパス上のリソース名です。ファイルシステムのパスではありません。
ファイルは、クローラーのクラスパスに含まれる |Fess| の設定ディレクトリに置きます。

- ZIP 版: ``app/WEB-INF/classes/``
- RPM/DEB 版: ``/etc/fess/``

``tesseract.properties`` には、Tika の ``TesseractOCRConfig`` のプロパティを記述します。
確実に反映されるのは ``language`` や ``timeoutSeconds`` などの単純なキーです。

::

    language=jpn
    timeoutSeconds=300

この指定は、このクロール設定について、上記のグローバル設定より優先されます。

運用上の注意
============

- OCR は CPU に高い負荷をかけ、クロールの処理時間が大幅に長くなります。クローラーのスレッド数を減らす、OCR が必要なクロール設定だけで有効にするなど、負荷を考慮してください。
- Web クロール設定では、新規作成時のデフォルトで画像の URL（jpg、png、gif など）がクロール対象から除外されます。Web サイトの画像をクロールするには、「クロール対象から除外するURL」からこれらを削除してください。ファイルクロールでは、画像もクロール対象になります。
- クローラーの取得サイズの上限も適用されます。ファイルの種類ごとのインデックスサイズの上限（デフォルトは 10MB）については :doc:`crawler-basic` を参照してください。
- OCR の精度は、スキャンした画像の品質に左右されます。手書きの文字は、一般に認識されにくくなります。
- OCR を有効にする前に索引に登録済みのファイルには、そのままでは OCR が適用されません。差分クロール（:doc:`../admin/general-guide` の「最終更新日時の確認」）が有効な場合、ファイルの更新日時が変わっていなければ再クロールでも取得し直されないためです。既存のファイルに OCR を適用するには、「最終更新日時の確認」を一時的に無効にしてクロールするか、対象のドキュメントを索引から削除してからクロールし直してください。

アップグレード時の注意
======================

15.8 以前の同梱の ``tika.xml`` は、``org.apache.tika.parser.ocr.TesseractOCRParser`` を除外していました。
15.9 からは、同梱の ``tika.xml`` はこのパーサーを除外しません。

``tika.xml`` をカスタマイズして使い続けている場合は、次の行を削除してください。

::

    <parser-exclude class="org.apache.tika.parser.ocr.TesseractOCRParser"/>

この行が残っていると、``crawler.document.ocr.enabled=true`` を指定しても OCR は無効のままです。

``tika.xml`` の場所は次のとおりです。

- ZIP 版: ``app/WEB-INF/conf/tika.xml``
- RPM/DEB 版: ``/etc/fess/tika.xml``

動作確認
========

1. スキャンした画像（文字を含む画像）を置いたフォルダーを、ファイルクロールの対象にします。
2. クロールを実行します。
3. 画像に含まれる単語で検索し、その画像が検索結果に表示されることを確認します。

検索結果に表示されない場合は、次の点を確認してください。

- ``tesseract --list-langs`` で、使用する言語が表示される
- ``crawler.document.ocr.enabled`` が ``true`` になっている
- ``tika.xml`` に ``TesseractOCRParser`` の除外が残っていない
- クロール時の ``fess-crawler.log`` に ``OCR is enabled`` が出力されている（``Tesseract OCR is not available`` の警告が出る場合は、|Fess| から Tesseract を利用できていません）
