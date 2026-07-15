========
排序检索
========

可以指定搜索日期等字段对搜索结果进行排序。

排序对象字段
---------------

默认情况下,可以指定以下字段进行排序。

.. list-table::
   :header-rows: 1

   * - 字段名
     - 说明
   * - created
     - 爬取的日期和时间
   * - content_length
     - 爬取的文档大小
   * - last_modified
     - 爬取的文档的最后修改日期和时间
   * - filename
     - 文件名
   * - score
     - 评分值
   * - timestamp
     - 文档索引的日期和时间
   * - click_count
     - 文档的点击次数
   * - favorite_count
     - 文档的收藏次数

表: 排序对象字段列表


也可以添加自己的字段作为排序对象。添加时,在 ``fess_config.properties`` 的 ``query.additional.sort.fields`` 中,用逗号分隔指定要作为排序对象的字段名(初始值为空)。在此指定的字段将被添加到上述标准字段中,从而可用于排序。另外,作为排序对象的字段必须事先在索引中注册。

使用方法
------

搜索时可以选择排序条件。单击选项按钮,在显示的搜索选项对话框中可以选择排序条件。

|image0|

此外,在搜索字段中进行排序时,以"sort:字段名"的格式,用冒号(:)分隔 sort 和字段名,在搜索表单中输入并搜索。

以下以 fess 为搜索词,按文档大小升序排序。

::

    fess sort:content_length

降序排序时,在字段名后添加 ``.desc``。

::

    fess sort:content_length.desc

字段名后可以指定的是 ``.asc`` (升序)或 ``.desc`` (降序),省略时默认为升序。

按多个字段排序时,如下所示以逗号(,)分隔指定。优先采用先指定的字段,该字段值相同的文档将按下一个字段进行排序。

::

    fess sort:content_length.desc,last_modified

.. note::
   如果指定了排序对象字段列表中不存在的字段名,或指定了 ``asc``,``desc`` 以外的排序顺序,则搜索会出现错误。

.. |image0| image:: ../../../resources/images/en/15.8/user/search-sort-1.png
.. pdf            :width: 300 px
