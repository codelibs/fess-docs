======================
使用メモリー関連の設定
======================

ヒープメモリーの最大値変更
==========================

クロール設定の内容によっては以下のような OutOfMemory
エラーが発生する場合があります。

::

    java.lang.OutOfMemoryError: Java heap space

発生した場合は ヒープメモリの最大値を増やしてください。
bin/setenv.[sh\|bat] に -Xmx1024m のように変更します(この場合は最大値を
1024M に設定)。

::

    Windowsの場合
    ...-server -Xmx1024m

    Unixの場合
    ...-server -Xmx1024m"

クローラ側のメモリー最大値変更
==============================

クローラ側のメモリーの最大値も変更可能です。デフォルトでは、512Mとなっています。

変更するには、webapps/fess/WEB-INF/classes/fess.dicon の
crawlerJavaOptions のコメントアウトを外し、-Xmx1024m
のように変更します(この場合は最大値を 1024M に設定)。

::

            <property name="crawlerJavaOptions">new String[] {
    "-Djava.awt.headless=true",
    "-server",
    "-Xmx1024m",
    "-XX:MaxPermSize=128m",
    "-XX:-UseGCOverheadLimit",
    "-XX:+UseConcMarkSweepGC",
    "-XX:CMSInitiatingOccupancyFraction=75",
    "-XX:+CMSIncrementalMode",
    "-XX:+CMSIncrementalPacing",
    "-XX:CMSIncrementalDutyCycleMin=0",
    "-XX:+UseParNewGC",
    "-XX:+UseStringCache",
    "-XX:+UseTLAB",
    "-XX:+DisableExplicitGC"
    }</property>
