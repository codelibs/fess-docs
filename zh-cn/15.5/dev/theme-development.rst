==================================
主题开发指南
==================================

概述
====

使用 |Fess| 的主题系统，您可以自定义搜索界面的设计。
主题可以作为插件分发，并支持多主题切换使用。

主题结构
========

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        └── theme/example/
            ├── css/
            │   ├── style.css
            │   └── custom.css
            ├── js/
            │   └── custom.js
            ├── images/
            │   └── logo.png
            └── templates/
                └── search.html

基本主题创建
============

CSS自定义
---------

``css/style.css``:

.. code-block:: css

    /* 头部自定义 */
    .navbar {
        background-color: #1a237e;
    }

    /* 搜索框样式 */
    .search-box {
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* 搜索结果样式 */
    .search-result-item {
        border-left: 3px solid #1a237e;
        padding-left: 15px;
    }

更改Logo
--------

1. 将自定义Logo放置到 ``images/logo.png``
2. 在CSS中引用Logo:

.. code-block:: css

    .logo img {
        content: url("../images/logo.png");
        max-height: 40px;
    }

模板自定义
----------

模板为JSP格式。

``templates/search.html`` (部分):

.. code-block:: html

    <div class="search-header">
        <h1>自定义搜索门户</h1>
        <p>搜索内部文档</p>
    </div>

主题注册
========

pom.xml
-------

.. code-block:: xml

    <groupId>org.codelibs.fess</groupId>
    <artifactId>fess-theme-example</artifactId>
    <version>15.5.0</version>
    <packaging>jar</packaging>

配置文件
--------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

安装
====

::

    ./bin/fess-plugin install fess-theme-example

从管理界面选择主题:

1. "系统" -> "设计"
2. 选择主题
3. 保存并应用

现有主题示例
============

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`../admin/design-guide` - 设计设置指南

