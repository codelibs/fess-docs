==================================
JSON连接器
==================================

概述
====

JSON连接器提供从本地文件系统上的JSON文件获取数据并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-json`` 插件。

支持以下三种格式，默认情况下会根据文件内容自动判断。

- JSON Lines格式（每行一个JSON对象）
- JSON对象数组（无论是格式化后的还是压缩为一行的均可）
- 单个JSON对象

由于记录是逐条读取的，因此即使是较大的数组，也不会将文件全部内容
保留在内存中。

.. note::

   此连接器仅面向本地文件系统上的JSON文件。不支持HTTP等远程获取方式，
   若指定了 ``urls`` 参数，不会被忽略，而是会导致报错。

前提条件
========

1. 需要安装插件
2. 需要具有JSON文件的访问权限
3. 需要了解JSON的结构

插件安装
------------------------

方法1: 从管理界面安装

1. 打开「系统」→「插件」
2. 上传JAR文件
3. 重启 |Fess|

方法2: 直接放置JAR文件

::

    # 从CodeLibs仓库下载
    wget https://maven.codelibs.org/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 放置
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # 或者
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

.. note::

   15.8.0及以后版本的JAR文件发布在 `CodeLibs仓库 <https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-json/>`_
   ，15.7.0及以前版本位于
   `Maven Central <https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/>`_ 。

配置方法
========

从管理界面的「爬虫」→「数据存储」→「新建」进行配置。

基本设置
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 设置示例
   * - 名称
     - Products JSON
   * - 处理器名称
     - JsonDataStore
   * - 启用
     - 开

参数设置
----------------

本地文件:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

多个文件:

::

    files=/var/data/data1.json,/var/data/data2.json
    file_encoding=UTF-8

目录指定:

::

    directories=/var/data/json_dir/
    file_encoding=UTF-8

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - 参数
     - 默认值
     - 说明
   * - ``files``
     -
     - 要处理的JSON文件路径（可指定多个：逗号分隔）。将按指定的顺序处理。
   * - ``directories``
     -
     - 包含JSON文件的目录路径（可指定多个：逗号分隔）。
   * - ``recursive``
     - ``false``
     - 是否对 ``directories`` 递归扫描子目录。
   * - ``max_depth``
     - ``10``
     - ``recursive=true`` 时，从各目录向下扫描的层数。指定 ``0`` 时的行为与 ``recursive=false`` 相同。
   * - ``include_pattern``
     -
     - 文件的绝对路径必须完全匹配的正则表达式。
   * - ``exclude_pattern``
     -
     - 文件的绝对路径不得匹配的正则表达式。
   * - ``file_suffixes``
     - ``.json,.jsonl``
     - 作为处理对象的文件后缀（可指定多个：逗号分隔）。不区分大小写。
   * - ``file_encoding``
     - ``UTF-8``
     - 文件的字符编码。
   * - ``format``
     - ``auto``
     - 文档的格式。可选 ``auto``、``jsonl``、``json`` 之一。
   * - ``root_path``
     -
     - 指定读取记录位置的JSON Pointer（例: ``/data/items`` ）。

.. note::

   参数名以蛇形命名法（snake_case）书写，但驼峰命名法的拼写
   （如对应 ``file_encoding`` 的 ``fileEncoding`` 等）同样可以正常使用。

.. note::

   请至少指定 ``files`` 和 ``directories`` 中的一个。
   两者均为空时将报错。
   两者并非互斥关系，若同时指定则两者都会被处理。
   即使同一个文件通过两者都能到达，也只会被读取一次。

文件搜索顺序
~~~~~~~~~~~~~~~~~~

- 通过 ``files`` 指定的文件将按指定的顺序处理。
- 在 ``directories`` 下找到的文件将按更新时间从旧到新的顺序处理。
- 通过 ``files`` 指定的文件会先于 ``directories`` 下的文件被处理。

通过 ``file_suffixes`` 进行的筛选也适用于通过 ``files`` 直接指定的文件。
后缀不匹配的文件会在日志中输出原因后被跳过。

不存在的路径、在 ``files`` 中指定的目录、在 ``directories`` 中指定的文件，
均会作为警告记录到日志中，爬取本身会继续进行。

``format``
----------

``auto`` 会读取文档开头，并根据其语法判断格式。无论是三种格式中的哪一种，
只要文件书写正确，就能通过这种方式判断出来。

需要明确指定 ``format=jsonl`` 的情况，是文件为JSON Lines格式，且开头附近的行
可能已损坏时（例如横幅行、进度日志、传输中途中断的记录等）。
这是因为自动判别需要跳过这类行才能做出判断。

此设置还决定了错误记录的影响范围。

- **JSON Lines格式**: 由于每行都是独立解析的，因此错误行的代价仅限于该行本身。
  失败会以 ``<文件的绝对路径>@<行号>`` 为键记录到失败URL中，
  之后会从下一行继续处理。
- **其他格式**: 由于是作为令牌流读取的，一次失败可能会连累后续的记录。
  在对象中途中断的文档无法恢复，若连续失败达到一定次数，
  该文件会输出警告并被中止处理。

``root_path``
-------------

若指定指向嵌套数组的JSON Pointer，则该元素会被注册为记录。

::

    root_path=/data/items

.. code-block:: json

    { "meta": { "count": 2 }, "data": { "items": [ { "id": "1" }, { "id": "2" } ] } }

- 若指向数组，则每个元素对应一条记录。
- 若指向对象，则该对象即为一条记录。
- 若未匹配到任何位置，则不会报错，记录数为0。
- 可以使用JSON Pointer的转义（ ``~1`` 表示 ``/`` 、 ``~0`` 表示 ``~`` ）。

``root_path`` 的优先级高于 ``format`` 。这是因为通过JSON Pointer到达的文档
不会按行读取，若与 ``format=jsonl`` 同时指定，日志中会输出相应的警告。

.. warning::

   ``root_path`` 必须以 ``/`` 开头。如果像 ``data/items`` 那样遗漏了开头的 ``/`` ，
   将无法作为JSON Pointer解析，导致整个数据存储配置报错。
   此时失败URL记录的不是参数名而是数据存储配置本身，
   因此需要根据日志中的
   ``JSON Pointer expression must start with '/'`` 来判断是哪个参数导致的问题。

.. note::

   如果不指定 ``root_path`` ，而直接读取记录跨多行格式化的文档
   （即包含元信息和数组的所谓包装器格式），系统会尝试按行解析，
   导致无法获取预期的记录并记录失败。
   对于此类文档，请务必指定 ``root_path`` 。

脚本设置
--------------

各字段的值通过引用JSON对象各字段的值来构建。
JSON对象的顶层字段在脚本中可作为 **无前缀的变量**
直接引用（不加 ``data.`` 等前缀）。

简单的JSON对象:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description
    digest=description
    host="shop.example.com"
    site="shop.example.com"

嵌套的对象可作为map引用，嵌套的数组可作为list引用:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    first_tag=tags[0]

可用字段
~~~~~~~~~~~~~~~~~~~~

- ``<字段名>`` - 通过名称直接引用JSON对象的顶层字段
- ``<父>.<子>`` - 嵌套对象的字段
- ``<数组>[<索引>]`` - 数组元素

.. note::

   若字段的值为 ``null`` ，则该字段不会被注册到文档中。

.. note::

   在 |Fess| 15.9 中，内置脚本引擎变为JavaScript。
   Groovy作为 ``fess-script-groovy`` 插件提供。
   要使用的引擎通过数据存储的参数 ``script_type`` 指定
   （如 ``script_type=javascript`` ）。省略时使用 ``groovy`` 。
   上述示例中简单的引用和字符串拼接在两种引擎中的行为相同，
   但除此之外的写法因引擎而异。

注意事项
========

名称与 ``app.encrypt.property.pattern`` 匹配的参数（默认情况下以 ``password`` 、
``key`` 、 ``token`` 、 ``secret`` 结尾的参数），从脚本中引用时会得到 ``null`` 。
这是为了防止写在数据存储参数中的凭据被复制到索引的
字段中。

若记录一侧存在同名字段，则与其他参数一样，以记录一侧的值
优先。

.. note::

   匹配判定是对参数名区分大小写的完全匹配。
   ``access_token`` 属于匹配对象，但驼峰命名法的 ``accessToken``
   不属于匹配对象。若需要在参数中记述凭据，请使用蛇形命名法
   （snake_case）书写。

参数错误与报错
==========================

若为 ``format`` 、 ``include_pattern`` 、 ``exclude_pattern`` 、 ``urls`` 指定了无法使用的值，
则会在读取文件之前结束爬取，并记录包含该参数名的
失败URL（例: ``JsonDataStore:format`` ）。

若为 ``max_depth`` 指定了非数值，则会在记录到日志后使用默认值。

.. note::

   数据存储的爬取即使一个对象都未能获取到，作为任务也会
   正常结束。若获取件数与预期不符，请确认索引的件数、失败URL，
   以及 ``fess-crawler.log`` 。

使用示例
========

产品目录
------------

参数:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

脚本:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description
    digest=category
    host="shop.example.com"
    site="shop.example.com"

保存API响应的文件
--------------------------------

参数:

::

    files=/var/data/response.json
    root_path=/data/items

脚本:

::

    url="https://example.com/item/" + id
    title=title
    content=body
    host="example.com"
    site="example.com"

递归处理目录
------------------------------

参数:

::

    directories=/var/data/exports
    recursive=true
    max_depth=3
    include_pattern=.*\.jsonl
    file_encoding=UTF-8

故障排除
======================

找不到文件
----------------------

**症状**: 日志中输出 ``... does not exist.`` 、 ``... is not a file.`` 、
``... is skipped because its suffix is not one of ...``

**确认事项**:

1. 确认文件路径是否正确
2. 确认文件是否存在
3. 确认文件后缀是否与 ``file_suffixes`` （默认为 ``.json`` 或 ``.jsonl`` ）
   相匹配
4. 确认 |Fess| 的运行用户是否具有读取权限

JSON解析错误
--------------

**症状**: 日志中输出 ``Failed to parse ...`` 或 ``Failed to read ...`` ，
或记录了失败URL

**确认事项**:

1. 验证文件是否为有效的JSON

   ::

       # 若为JSON Lines格式，验证每行是否为有效的JSON对象
       cat data.jsonl | jq -c .

       # 若为数组或单个对象
       jq . data.json

2. 确认字符编码是否正确
3. 确认文件是否中途被截断
4. 确认是否包含注释（JSON标准不允许注释）

无法获取数据
--------------------

**症状**: 爬取成功但件数为0

**确认事项**:

1. 若指定了 ``root_path`` ，请确认该JSON Pointer是否与文档结构
   相符（不相符时不会报错，而是件数为0）
2. 确认是否因 ``include_pattern`` 、 ``exclude_pattern`` 、 ``file_suffixes`` 而将对象
   全部排除在外。此时日志中会输出 ``No sources to process``
3. 确认脚本设置是否正确（字段引用是否未带 ``data.`` 前缀）
4. 确认字段名是否正确（含大小写）
5. 确认 ``url`` 是否已构建成功。若 ``url`` 为空，则每条记录都会失败

出现乱码
------------

**症状**: 注册的文档中字符出现乱码

若在 ``file_encoding`` 中指定了实际存在但错误的编码，不会报错，而是会
以乱码状态注册。请确认文件的实际编码。
若指定了不存在的编码名称，则会按文件记录失败URL。

大型JSON文件
------------------

**症状**: 内存不足或超时

由于记录是逐条读取的，文件的整体大小不会直接影响内存使用量。
但是，当单条记录极大，或索引注册的负荷较高时，
可能会出现问题。

**解决方法**:

1. 将JSON文件分割成多个
2. 增加 |Fess| 的堆大小

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-csv` - CSV连接器
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `JSON Pointer (RFC 6901) <https://datatracker.ietf.org/doc/html/rfc6901>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
