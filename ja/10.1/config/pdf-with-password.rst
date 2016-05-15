=================
パスワード付きPDF
=================

パスワード付きPDFの対応方法
===========================

パスワードが設定されたPDFを検索対象にするためには設定ファイルで対象ファイルのパスワードを登録しておく必要があります．

設定
====

まず、webapps/fess/WEB-INF/classes/s2robot\_extractor.dicon
を以下のように作成します。 今回は，test\_〜.pdf というファイルに pass
というパスワードが設定されている場合です．
対象ファイルが複数ある場合は，addPassword で複数設定します．

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//SEASAR//DTD S2Container 2.4//EN"
        "http://www.seasar.org/dtd/components24.dtd">
    <components>
        <component name="tikaExtractor" class="org.codelibs.robot.extractor.impl.TikaExtractor"/>
        <component name="msWordExtractor"
            class="org.codelibs.robot.extractor.impl.MsWordExtractor"/>
        <component name="msExcelExtractor"
            class="org.codelibs.robot.extractor.impl.MsExcelExtractor"/>
        <component name="msPowerPointExtractor"
            class="org.codelibs.robot.extractor.impl.MsPowerPointExtractor"/>
        <component name="msPublisherExtractor"
            class="org.codelibs.robot.extractor.impl.MsPublisherExtractor"/>
        <component name="msVisioExtractor"
            class="org.codelibs.robot.extractor.impl.MsVisioExtractor"/>
        <component name="pdfExtractor" class="org.codelibs.robot.extractor.impl.PdfExtractor">
            <initMethod name="addPassword">
                <!-- 正規表現で対象ファイルのパスを指定 -->
                <arg>".*test_.*.pdf"</arg>
                <!-- パスワード -->
                <arg>"pass"</arg>
            </initMethod>
        </component>
        <component name="textExtractor" class="org.codelibs.robot.extractor.impl.TextExtractor"/>
        <component name="htmlExtractor" class="org.codelibs.robot.extractor.impl.HtmlExtractor"/>
        <component name="xmlExtractor" class="org.codelibs.robot.extractor.impl.XmlExtractor"/>
        <component name="htmlXpathExtractor"
            class="org.codelibs.robot.extractor.impl.HtmlXpathExtractor">
            <initMethod name="addFeature">
                <arg>"http://xml.org/sax/features/namespaces"</arg>
                <arg>"false"</arg>
            </initMethod>
        </component>

    ...

次に、webapps/fess/WEB-INF/classes/s2robot\_rule.dicon
に以下を編集します。

::

    ...
        <component name="fsFileRule" class="org.codelibs.robot.rule.impl.RegexRule" >
            <property name="ruleId">"fsFileRule"</property>
            <property name="responseProcessor">
                <component class="org.codelibs.robot.processor.impl.DefaultResponseProcessor">
                    <property name="transformer">fessFileTransformer</property>
                </component>
            </property>
            <property name="allRequired">true</property>
            <initMethod name="addRule">
                <arg>"url"</arg>
                <arg>"file:.*"</arg>
            </initMethod>
            <initMethod name="addRule">
                <arg>"mimeType"</arg>
                <!-- Supported MIME type -->
                <arg>
      "(application/xml"
    + "|application/xhtml+xml"
    + "|application/rdf+xml"
    + "|application/pdf"
    + "|text/xml"
    + "|text/xml-external-parsed-entity"
    + "|text/html)"
                </arg>
            </initMethod>
        </component>
    ...

上記を設定したら、 |Fess| 
を起動してクロールを実行してください。基本的な利用方法は特に変わりません。
