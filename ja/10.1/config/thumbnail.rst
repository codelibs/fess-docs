====================
サムネイル画像の設定
====================

実施環境と画像作成対象
======================

環境:CentOS7
インストール後でfessユーザが作成済みの状態を想定しています。
今回は例としてWord(doc, docx),  Excel(xls, xlsx), PowerPoint(ppt, pptx), rtf
をサムネイルの作成対象としていますが、作成対象は変更することができます。

fessユーザのホームディレクトリ変更
==================================

Fessインストール後、実行結果にfessユーザが存在することを確認します。

::
    cat /etc/passwd | grep fess

Fessのサービス停止中に以下を実行して、
fessユーザのホームディレクトリの変更を行います。

::
    usermod -d /var/lib/fess fess

サムネイル画像の作成に必要なパッケージをインストール
====================================================

::
    $ sudo yum install unoconv
    $ sudo yum install libreoffice-headless
    $ sudo yum install vlgothic-fonts
    $ sudo yum install ImageMagick

サムネイル画像の出力対象の設定
==============================

以下のコメントを外します。
/usr/share/fess/app/WEB-INF/classes/fess_screenshot.xml

::
    <!-- (削除)
    		<postConstruct name="add">
    			<arg>officeScreenShotGenerator</arg>

        <!-- 省略 -->

    			<arg>"application/rtf"
    			</arg>
    		</postConstruct>
    	</component>
    --> (削除)

サムネイル作成対象は以下のようにmimetypeを記述することで設定されます。
PDFを追加する場合は以下のように追加します。

::
    <postConstruct name="addCondition">
    	<arg>"mimetype"</arg>
    	<arg>"application/pdf"
    	</arg>
    </postConstruct>

サムネイル画像サイズの変更
==========================

サムネイルの画像サイズを変更する場合はconvertのthumbnailオプションの値を変更してください。
/use/share/fess/bin/office-screenshot.sh

::
    convert -thumbnail 200x150! ${pdfFile} ${outputFile}

サムネイル画像の表示
====================

以下の行を追加します。
/usr/share/fess/app/WEB-INF/view/search.jsp

::
    <script type="text/javascript" src="${f:url('/js/search.js')}"></script>
    <script type="text/javascript" src="${f:url('/js/screenshot.js')}"></script> <!-- 追加 -->

以下の行を追加することでサムネイル画像を表示することができます。
/usr/share/fess/app/WEB-INF/view/searchResult.jsp

::
    <c:forEach var="doc" varStatus="s" items="${documentItems}">
        <li id="result${s.index}">
          <div class="screenShotBox"> <!-- 追加 -->
            <c:if test="${doc.has_cache=='true'}"> <!-- 追加 -->
              <img src="/screenshot/?docId=${f:u(doc.doc_id)}&queryId=${f:u(queryId)}" onError="noimage(this)" > <!-- 追加 -->
            </c:if> <!-- 追加 -->
          </div> <!-- 追加 -->
