====================
サムネイル画像の設定
====================

サムネイル画像
==============

|サムネイル画像は検索結果に画像出力対象のmimetypeが存在する場合に作成されます。
|サムネイル画像の出力対象はmimetypeを設定して追加することができます。

fessユーザのホームディレクトリ変更
==================================

|Linux環境では`RPM パッケージのインストール <http://fess.codelibs.org/ja/10.1/install/install.html#id1>`後、以下のコマンドの実行結果にfessユーザが存在することを確認します。

::
    cat /etc/passwd | grep fess

|Fessのサービス停止中に以下のコマンドを実行して、fessユーザのホームディレクトリを変更します。

::
    usermod -d /var/lib/fess fess

サムネイル画像作成に必要なパッケージをインストール
==================================================

|画像の作成用に以下のパッケージをインストールします。
::
    $ sudo yum install unoconv
    $ sudo yum install libreoffice-headless
    $ sudo yum install vlgothic-fonts
    $ sudo yum install ImageMagick

サムネイル画像の作成
====================

|サムネイル画像の作成を有効にするため、/usr/share/fess/app/WEB-INF/classes/fess_screenshot.xmlの以下のコメントを外します。

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

|サムネイル画像の出力対象は<property name="commandList"> </property> 以下にmimetypeを追加することで設定します。
|PDFを作成対象とする場合は以下を設定します。

::
    <postConstruct name="addCondition">
    	<arg>"mimetype"</arg>
    	<arg>"application/pdf"
    	</arg>
    </postConstruct>

サムネイル画像サイズの変更
==========================

|サムネイルの画像サイズを変更する場合は /use/share/fess/bin/office-screenshot.sh で
|convertのthumbnailオプションの値を変更してください。

::
    convert -thumbnail 200x150! ${pdfFile} ${outputFile}

サムネイル画像の表示
====================

|サムネイル画像の表示は以下のJSPを編集します。
|/usr/share/fess/app/WEB-INF/view/search.jsp に以下の行を追加します。

::
    <script type="text/javascript" src="${f:url('/js/search.js')}"></script>
    <script type="text/javascript" src="${f:url('/js/screenshot.js')}"></script> <!-- 追加 -->

|/usr/share/fess/app/WEB-INF/view/searchResult.jsp に以下の行を追加します。

::
    <c:forEach var="doc" varStatus="s" items="${documentItems}">
        <li id="result${s.index}">
          <div class="screenShotBox"> <!-- 追加 -->
            <c:if test="${doc.has_cache=='true'}"> <!-- 追加 -->
              <img src="/screenshot/?docId=${f:u(doc.doc_id)}&queryId=${f:u(queryId)}" onError="noimage(this)" > <!-- 追加 -->
            </c:if> <!-- 追加 -->
          </div> <!-- 追加 -->
