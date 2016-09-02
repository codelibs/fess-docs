====================
サムネイル画像の設定
====================

サムネイル画像の表示
====================

|Fess|では検索結果の内容として、その結果のサムネイル画像を表示することができます。
サムネイル画像は検索結果のMIME Typeを元の生成されます。
サポートしているMIME Typeであれば、検索結果の表示時にサムネイル画像を生成します。
サムネイル画像を生成する処理はMIME Typeごとに設定して追加することができます。

HTMLファイルのサムネイル画像
============================

phantomjsを用いて、HTMLのサムネイル画像を生成することができます。
phantomjsは事前にインストールしておいてください。

設定ファイルの変更
------------------

サムネイル画像の作成を有効にするため、$FESS_HOME/app/WEB-INF/classes/fess_thumbnail.xmlの以下のコメントを外します。

::

        <component name="screenShotManager" class="org.codelibs.fess.screenshot.ScreenShotManager">
                <postConstruct name="add">
                        <arg>htmlScreenShotGenerator</arg>
                </postConstruct>
        </component>
        <component name="webDriver" class="org.openqa.selenium.phantomjs.PhantomJSDriver">
                <arg>
                        <component class="org.openqa.selenium.remote.DesiredCapabilities">
                                <postConstruct name="setCapability">
                                        <arg>"phantomjs.binary.path"</arg>
                                        <arg>"/usr/bin/phantomjs"</arg>
                                </postConstruct>
                        </component>
                </arg>
                <preDestroy name="quit"></preDestroy>
        </component>
        <component name="htmlScreenShotGenerator" class="org.codelibs.fess.screenshot.impl.WebDriverGenerator">
                <property name="webDriver">webDriver</property>
                <postConstruct name="addCondition">
                        <arg>"mimetype"</arg>
                        <arg>"text/html"</arg>
                </postConstruct>
        </component>


MS Officeファイルのサムネイル画像
=================================

LibreOfficeを利用して、MS Office系ファイルのサムネイル画像を生成することができます。

パッケージのインストール
------------------------

画像の作成用に必要な以下のパッケージをインストールします。

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

設定ファイルの変更
------------------

サムネイル画像の作成を有効にするため、$FESS_HOME/app/WEB-INF/classes/fess_screenshot.xmlを以下のように編集します。

::

	<component name="screenShotManager" class="org.codelibs.fess.screenshot.ScreenShotManager">
		<postConstruct name="add">
			<arg>officeScreenShotGenerator</arg>
		</postConstruct>
	</component>
	<component name="officeScreenShotGenerator"
		class="org.codelibs.fess.screenshot.impl.CommandGenerator">
		<property name="commandList">
			["sh",
			"/use/share/fess/bin/office-screenshot.sh",
			"${url}",
			"${outputFile}"]
		</property>
		<postConstruct name="addCondition">
			<arg>"mimetype"</arg>
			<arg>"application/vnd.openxmlformats-officedocument.wordprocessingml.document"
			</arg>
		</postConstruct>
		<postConstruct name="addCondition">
			<arg>"mimetype"</arg>
			<arg>"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
			</arg>
		</postConstruct>
		<postConstruct name="addCondition">
			<arg>"mimetype"</arg>
			<arg>"application/vnd.openxmlformats-officedocument.presentationml.presentation"
			</arg>
		</postConstruct>
		<postConstruct name="addCondition">
			<arg>"mimetype"</arg>
			<arg>"application/msword"
			</arg>
		</postConstruct>
		<postConstruct name="addCondition">
			<arg>"mimetype"</arg>
			<arg>"application/vnd.ms-excel"
			</arg>
		</postConstruct>
		<postConstruct name="addCondition">
			<arg>"mimetype"</arg>
			<arg>"application/vnd.ms-powerpoint"
			</arg>
		</postConstruct>
		<postConstruct name="addCondition">
			<arg>"mimetype"</arg>
			<arg>"application/rtf"
			</arg>
		</postConstruct>
	</component>

生成スクリプトの作成
--------------------

/usr/share/fess/bin/generate-thumbnailに以下の内容で生成処理を作成します。

::

    #!/bin/sh

    CMD_TYPE=$1
    URL=$2
    OUTPUT_FILE=$3

    if [ x"$CMD_TYPE" = "xmsoffice" ] ; then
      TARGET_FILE=`echo $URL | sed -e "s#^file:/*#/#g"`
      TMP_FILE=/tmp/thumbnail.$$.pdf
      unoconv -o $TMP_FILE -f pdf $TARGET_FILE
      convert -thumbnail 160x120! $TMP_FILE $OUTPUT_FILE
      rm $TMP_FILE
    else
      echo "Unsupported type: $CMD_TYPE"
      exit 1
    fi

サムネイルの画像サイズを変更する場合は、convertのthumbnailオプションの値を変更してください。

その他
======

実行ユーザのホームディレクトリ変更
----------------------------------

Linux環境ではRPMパッケージでインストールした場合、|Fess|の起動ユーザーでコマンドを実行することができない場合があります。
そのため、ホームディレクトリを変更する必要があります。
以下のコマンドの実行結果にfessユーザが存在することを確認します。

::

    grep fess /etc/passwd

|Fess|のサービス停止中に以下のコマンドを実行して、fessユーザのホームディレクトリを変更します。

::

    usermod -d /var/lib/fess fess
