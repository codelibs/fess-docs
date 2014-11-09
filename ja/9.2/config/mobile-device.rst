==================
携帯端末情報の設定
==================

携帯端末情報の更新
==================

携帯端末情報は\ `ValueEngine社 <http://valueengine.jp/>`__\ より提供されるものを利用しています。最新の携帯端末情報を利用したい場合は、端末プロファイルをダウンロードして、webapps/fess/WEB-INF/classes/device
/ に \_YYYY-MM-DD を取り除いて保存します。
再起動後に変更が有効になります。

::

    ProfileData_YYYY-MM-DD.csv -> ProfileData.csv
    UserAgent_YYYY-MM-DD.csv -> UserAgent.csv
    DisplayInfo_YYYY-MM-DD.csv -> DisplayInfo.csv
