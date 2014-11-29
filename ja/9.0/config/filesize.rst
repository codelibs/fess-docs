================================
クロールするファイルサイズの設定
================================

ファイルサイズの設定方法
========================

|Fess| 
のクロールするファイルサイズ上限を指定することができます。デフォルトでは
HTML ファイルは 2.5M バイト、それ以外は 10M
バイトまで処理します。扱うファイルサイズを変更したい場合は
webapps/fess/WEB-INF/classes/s2robot\_contentlength.dicon
を編集します。標準の s2robot\_contentlength.dicon は以下の通りです。

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//SEASAR//DTD S2Container 2.4//EN"
            "http://www.seasar.org/dtd/components24.dtd">
    <components>
            <component name="contentLengthHelper"
                class="org.seasar.robot.helper.ContentLengthHelper" instance="singleton" >
                    <property name="defaultMaxLength">10485760L</property><!-- 10M -->
                    <initMethod name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440L</arg><!-- 2.5M -->
                    </initMethod>
            </component>
    </components>

デフォルト値を変更したい場合は defaultMaxLength
の値を変更します。扱うファイルサイズはコンテンツタイプごとに指定できます。HTML
ファイルであれば、text/html と扱うファイルサイズの上限を記述します。

扱うファイルサイズの上限値を変更する場合は、使用するヒープメモリ量にも注意してください。設定方法については\ `メモリ関連 <memory-config.html>`__\ を参照してください。
