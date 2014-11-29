==========
ログの設定
==========

ログの設定
==========

|Fess| の出力ログは webapps/fess/WEB-INF/logs/fess.out に出力されます
(Solr に関するログは logs/catalina.out に出力されています)。fess.out
に出力する内容は、webapps/fess/WEB-INF/classes/log4j.xml
で設定します。デフォルトでは INFO レベルとして出力しています。

たとえば、 |Fess| が Solr
に対してドキュメントを投入処理をするログをより出力したい場合は log4j.xml
で以下の部分をコメントアウトから外します。

::

    <logger name="jp.sf.fess.solr" >
        <level value ="debug" />
    </logger>
