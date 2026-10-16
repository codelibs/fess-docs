======
组
======

概述
====

可以管理用户所属的组。
在与 LDAP 集成等情况下可以使用。

管理方法
======

显示方法
------

要打开下图所示的组设置列表页面，请点击左侧菜单中的 [用户 > 组]。

|image0|

点击设置名称可进行编辑。

创建设置
--------

要打开组设置页面，请点击新建按钮。

|image1|

配置项
------

名称
::::

组名称。

gidNumber
:::::::::

组的 gidNumber（LDAP 中的 POSIX 组 ID），以数字指定。可以省略。输入非数字的值会出错。
当 |Fess| 设置为通过管理界面管理 LDAP（ ``ldap.admin.enabled=true`` ）时，该值会写入 LDAP 中组条目的 ``gidNumber`` 属性（属性名可通过 ``ldap.attr.gidNumber`` 更改）。不使用 LDAP 时无需指定。

删除方法
--------

点击列表页面的设置名称，然后点击删除按钮，将显示确认画面。
点击删除按钮将删除该设置。

.. |image0| image:: ../../../resources/images/en/15.10/admin/group-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/group-2.png
