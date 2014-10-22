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
    ...-Dpdfbox.cjk.support=true -Xmx1024m

    Unixの場合
    ...-Dpdfbox.cjk.support=true -Xmx1024m"
