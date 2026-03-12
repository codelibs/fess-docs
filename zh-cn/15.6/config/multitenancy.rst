==================================
多租户配置
==================================

概述
====

使用 |Fess| 的多租户功能，可以在单个 |Fess| 实例中
隔离运行多个租户（组织、部门、客户等）。

通过使用虚拟主机功能，可以为每个租户提供:

- 独立的搜索UI
- 隔离的内容
- 定制的设计

虚拟主机功能
==============

虚拟主机是根据HTTP请求的主机名提供不同搜索环境的功能。

工作原理
------

1. 用户访问 ``tenant1.example.com``
2. |Fess| 识别主机名
3. 应用对应的虚拟主机设置
4. 显示租户特定的内容和UI

虚拟主机配置
================

管理界面配置
----------------

1. 登录管理界面
2. 导航到「爬虫」→「虚拟主机」
3. 点击「新建」
4. 设置以下内容:

   - **主机名**: ``tenant1.example.com``
   - **路径**: ``/tenant1``（可选）

与爬取设置的联动
--------------------

通过在Web爬取设置中指定虚拟主机，可以隔离内容:

1. 在「爬虫」→「Web」中创建爬取设置
2. 在「虚拟主机」字段中选择目标虚拟主机
3. 使用此设置爬取的内容仅在指定的虚拟主机中可搜索

访问控制
============

虚拟主机与角色的组合
------------------------------

通过组合虚拟主机和基于角色的访问控制，
可以实现更精细的访问控制:

::

    # 配置示例
    virtual.host=tenant1.example.com
    permissions=role_tenant1_user

基于角色的搜索
----------------

详情请参阅 :doc:`security-role`。

UI定制
==============

可以为每个虚拟主机定制UI。

主题应用
------------

为每个虚拟主机应用不同的主题:

1. 在「系统」→「设计」中设置主题
2. 在虚拟主机设置中指定主题

自定义CSS
-----------

为每个虚拟主机应用自定义CSS:

::

    # 虚拟主机特定的CSS文件
    /webapp/WEB-INF/view/tenant1/css/custom.css

标签设置
----------

限制每个虚拟主机显示的标签:

1. 在标签类型设置中指定虚拟主机
2. 标签仅在指定的虚拟主机中显示

API认证
=======

按虚拟主机控制API访问:

访问令牌
----------------

发行与虚拟主机关联的访问令牌:

1. 在「系统」→「访问令牌」中创建令牌
2. 将令牌与虚拟主机关联

API请求
-------------

::

    curl -H "Authorization: Bearer TENANT_TOKEN" \
         "https://tenant1.example.com/api/v1/search?q=keyword"

DNS设置
=======

实现多租户的DNS设置示例:

指向同一服务器的子域名
----------------------------

::

    # DNS设置
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # 或使用通配符
    *.example.com          A    192.168.1.100

反向代理设置
--------------------

使用Nginx的反向代理设置示例:

::

    server {
        server_name tenant1.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    server {
        server_name tenant2.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

数据隔离
==========

需要完全数据隔离时，考虑以下方法:

索引级别隔离
------------------------

为每个租户使用单独的索引:

::

    # 租户1用索引
    index.document.search.index=fess_tenant1.search

    # 租户2用索引
    index.document.search.index=fess_tenant2.search

.. note::
   索引级别隔离可能需要自定义实现。

最佳实践
==================

1. **明确的命名规则**: 对虚拟主机和角色使用一致的命名规则
2. **测试**: 充分测试每个租户的功能
3. **监控**: 监控每个租户的资源使用情况
4. **文档**: 记录租户设置

限制事项
========

- 管理界面在所有租户间共享
- 系统设置影响所有租户
- 部分功能可能不支持虚拟主机

参考信息
========

- :doc:`security-role` - 基于角色的访问控制
- :doc:`security-virtual-host` - 虚拟主机设置详情
- :doc:`../admin/design-guide` - 设计定制
