==========
ポート変更
==========

ポートの変更
============

|Fess| がデフォルトで利用するポートは 8080 になります。
変更する場合は、Linux 環境であれば bin/fess.in.sh の

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

Windows 環境であれば bin\\fess.bat の

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

を変更します。

