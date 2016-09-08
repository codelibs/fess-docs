====================
サムネイル画像の設定
====================

サムネイル画像の表示
====================

|Fess| では検索結果のサムネイル画像を表示することができます。
サムネイル画像は検索結果のMIME Typeを元の生成されます。
サポートしているMIME Typeであれば、検索結果の表示時にサムネイル画像を生成します。
サムネイル画像を生成する処理はMIME Typeごとに設定して追加することができます。

サムネイル画像を表示するためには、管理者としてログインして、全般の設定でサムネイル表示を有効にして保存してください。

HTMLファイルのサムネイル画像
============================

HTMLのサムネイル画像はphantomjsを用いて生成されます。
|Fess| がphantomjsコマンドを検出できた場合は自動で利用されます。

コマンドパスの指定
------------------

phantomjsのコマンドパスを明示的に指定したい場合、$FESS_HOME/app/WEB-INF/classes/fess_thumbnail.xml の${path}/phantomjsの箇所を変更してください。

::

    <component name="htmlThumbnailGenerator" class="org.codelibs.fess.thumbnail.impl.WebDriverGenerator">
        <property name="generatorList">
            ["${path}/phantomjs"]
        </property>
        <property name="webDriverCapabilities">
            <component class="org.openqa.selenium.remote.DesiredCapabilities">
                <postConstruct name="setCapability">
                    <arg>"phantomjs.binary.path"</arg>
                    <arg>"${path}/phantomjs"</arg>
                </postConstruct>
            </component>
        </property>
        <postConstruct name="addCondition">
            <arg>"mimetype"</arg>
            <arg>"text/html"</arg>
        </postConstruct>
    </component>


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
-------------

RPM/Debパッケージでインストールすると、MS Office用のサムネイル生成スクリプトは/usr/share/fess/bin/generate-thumbnailにインストールされます。

