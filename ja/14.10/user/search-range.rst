=========
範囲指定検索
=========

範囲指定検索
=========

数値など範囲指定が可能でデータをフィールドに格納している場合、そのフィールドに対して範囲指定検索が可能です。

利用方法
------

範囲指定検索をするためには、「フィールド名:[値 TO 値]」
を検索フォームに入力します。

たとえば、content_length
フィールドに対して、1kバイトから10kバイトにあるドキュメントを検索する場合は以下のように検索フォームに入力します。

::

    content_length:[1000 TO 10000]

時間の範囲指定検索をするためには、「last_modified:[日時1 TO
日時2]」(日時1＜日時2) を検索フォームに入力します。

日時はISO 8601を基準にしています。

.. list-table::

   * - 年月日および時分秒および小数部分
     - 現在日時を基準にする場合
   * - YYYY-MM-DDThh:mm:sssZ (例：2012-12-02T10:45:235Z)
     - now(現在の日時)、y(年)、M(月)、w(週)、d(日)、h(時)、m(分)、s(秒)

nowや時刻を基準にした場合には+、-(加算、減算)や/(丸め)といった記号を付けることができます。ただし、時刻を基準にした場合は記号との間に||を入れる必要があります。

/は/の後ろの単位で丸める記号です。now-1d/dは本日何時に実行したとしても、本日00:00から-1日した前日の00:00を表します。

たとえば、last_modified
フィールドに対して、2016年2月21日20時(現在日時とする)から30日前までに更新されたドキュメントを検索する場合は以下のように検索フォームに入力します。

::

    last_modified:[now-30d TO now](=[2016-01-23T00:00:000Z+TO+2016-02-21T20:00:000Z(現在日時)])
