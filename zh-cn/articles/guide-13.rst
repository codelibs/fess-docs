============================
一个 Fess 供多个组织分别使用
============================

前言
====

如果想为各集团公司或部门分别提供搜索服务，而按组织数量构建多个 Fess，服务器和爬网配置的管理工作也会随组织数量成倍增加。
使用 Fess 的虚拟主机功能，可以用多个主机名发布同一个 Fess，并按主机名切换搜索对象、标签和搜索页面。

不过，虚拟主机只是根据“通过哪个主机名访问”来区分显示内容的功能，并不是访问控制。
要确保其他组织的文档不被看到，必须结合基于角色的权限设置和登录。

本文以 A 公司和 B 公司两个租户为例，在 Fess 15.9 中依次完成以下设置。

- 在 [通用] 的「虚拟主机」中将主机名与租户对应起来
- 在爬网配置和标签中指定虚拟主机和权限，分开各租户的文档
- 使用与虚拟主机名同名的主题，为每个租户提供不同的搜索页面
- 以租户用户登录，确认看不到其他租户的文档
- 按正确的顺序添加和删除租户

角色、组和用户的基础知识在 :doc:`guide-05` 中介绍。

首先要明确：虚拟主机不是访问控制
================================

对于每个请求，Fess 会从上到下依次评估 [通用] 的「虚拟主机」中填写的各行，并使用第一个指定请求头（通常为 ``Host``）的值相匹配的行中的虚拟主机名（以下称为键）。
确定键之后，以下功能会按该键进行筛选。

- 搜索结果：只返回爬网配置的「虚拟主机」中包含该键的文档（搜索 API 也一样）
- 标签：只显示「虚拟主机」项为该键的标签
- 关键词匹配、相关内容、相关查询：只使用「虚拟主机」项为该键的设置
- 搜索页面：如果存在名称为该键小写形式的主题，则使用该主题显示

另一方面，对于与任何一行都不匹配的请求，上述筛选全部不会进行。
如果直接通过服务器的 IP 地址访问，或者反向代理改写了 ``Host`` 请求头，虚拟主机筛选就会失效，权限范围内所有租户的文档都会成为搜索对象。
[通用] 中主机名写错或漏写端口号，也不会报错，而是被当作“不匹配”处理。

因此，要让文档在租户之间互不可见，需要结合以下两点。

- 将各租户文档的权限仅设为该租户的角色（例如 ``{role}tenanta_user``）
- 搜索页面必须登录，并为用户分配租户的角色

本文构建的配置
==============

.. list-table::
   :header-rows: 1
   :widths: 16 26 14 18 26

   * - 租户
     - 公开主机名
     - 键
     - 角色
     - 爬取对象
   * - A 公司
     - ``search-a.example.com``
     - ``tenanta``
     - ``tenanta_user``
     - ``https://portal-a.example.com/``
   * - B 公司
     - ``search-b.example.com``
     - ``tenantb``
     - ``tenantb_user``
     - ``https://portal-b.example.com/``

键中只能使用字母、数字和下划线（``a-zA-Z0-9_``）。
其他字符会在保存时被去除，因此如果写成 ``tenant-a``，键会变成 ``tenanta``，在爬网配置中写 ``tenant-a`` 也无法匹配。
``admin``、``common``、``error``、``login``、``profile`` 为保留字，不能使用。

爬网配置和标签的「虚拟主机」项是自由输入的，与键的比对区分大小写。
主题名称也只能使用小写字母，因此从一开始就将键统一为小写字母和数字，可以避免出错。

步骤 1：将主机名与键对应起来
============================

打开管理页面的 [系统] > [通用]，在「虚拟主机」中每行填写一条 ``请求头名称:请求头值=键``，然后更新。

::

    Host:search-a.example.com=tenanta
    Host:search-b.example.com=tenantb

请求头的值以不区分大小写的完全匹配方式进行比较。
浏览器通过标准端口（80、443）以外的端口访问时，会在 ``Host`` 请求头中附带端口号，因此如果让用户直接访问 Fess 的 8080 端口，需要像下面这样连端口一起写上。
两种写法并列填写也没有问题。

::

    Host:search-a.example.com:8080=tenanta
    Host:search-b.example.com:8080=tenantb

设置在保存时即生效，无需重启。
也可以按相同格式写在 ``fess_config.properties`` 的 ``virtual.host.headers`` 中，但如果 [通用] 中有值，则以 [通用] 为准。

放在反向代理后面时，需要将浏览器发送的 ``Host`` 请求头传递到 Fess。
Nginx 默认会将 ``Host`` 设为 ``proxy_pass`` 的目标，因此需要 ``proxy_set_header Host $host;``。

::

    server {
        server_name search-a.example.com search-b.example.com;
        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
        }
    }

在会改写 ``Host`` 的配置中，也可以将请求头名称指定为 ``X-Forwarded-Host``\ （例如 ``X-Forwarded-Host:search-a.example.com=tenanta``）。

.. warning::

   [通用] 的设置保存在容器内的 ``system.properties`` 中。
   docker-fess 的 ``fess01`` 没有卷，因此用 ``docker compose down`` 重新创建容器后，「虚拟主机」的值也会丢失（``stop``、``start`` 则会保留）。
   后续步骤中上传的主题也放在容器内，同样会丢失。
   保留设置的方法请参阅 `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__。

步骤 2：创建租户的角色和用户
============================

1. 在 [用户] > [角色] 中创建名称为 ``tenanta_user`` 和 ``tenantb_user`` 的角色。
2. 在 [用户] > [用户] 中创建各租户的用户，并在「角色」中选择该租户的角色。
3. 在 [系统] > [通用] 中启用「需要登录」。

已登录的用户不会附带 ``{role}guest``，只以用户、组和角色的权限进行搜索。
如果想直接使用 LDAP 或 SSO 的组，可以用 ``{group}<组名>`` 代替角色进行指定。
权限机制和 LDAP 集成请参阅 :doc:`guide-05`，SSO 请参阅 :doc:`guide-15`。

步骤 3：为每个租户创建标签
==========================

标签会在爬取时添加到 URL 与「包含的路径」相匹配的文档上。
请在爬取之前创建好。

在 [爬虫] > [标签] 中点击 [新建]，为 A 公司输入以下内容（B 公司也同样创建）。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 值
   * - 名称
     - ``A 公司门户``
   * - 值
     - ``tenanta_docs``\ （仅限字母、数字和下划线）
   * - 包含的路径
     - ``https://portal-a\.example\.com/.*``
   * - 权限
     - ``{role}tenanta_user``
   * - 虚拟主机
     - ``tenanta``

新标签的权限中已填入 ``{role}guest``。
标签只在用户拥有其权限中的角色时才会显示，因此如果保留 ``{role}guest``，已登录的租户用户将看不到该标签。

「虚拟主机」为空的标签，在通过虚拟主机访问时不会显示。
一个标签只能指定一个虚拟主机，因此如果想让多个租户看到同一个标签，需要按租户数量创建名称和值都相同的标签，并在各自的「虚拟主机」中填入键。
关键词匹配、相关内容、相关查询也一样，「虚拟主机」为空的设置不会在租户的主机上使用。

步骤 4：在爬网配置中指定虚拟主机和权限
======================================

在 [爬虫] > [Web] 中创建 A 公司的爬网配置。
文件系统和数据存储的爬网配置中也有相同的两个项目。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 值
   * - 名称
     - ``A 公司门户``
   * - URL
     - ``https://portal-a.example.com/``
   * - 要包含在爬网中的URL
     - ``https://portal-a.example.com/.*``
   * - 权限
     - ``{role}tenanta_user``\ （删除默认填入的 ``{role}guest``）
   * - 虚拟主机
     - ``tenanta``

如果保留 ``{role}guest``，通过 IP 地址访问或登录前访问时就能看到这些文档。

像集团通用的规章制度这样需要给多个租户看的文档，在一个爬网配置的「虚拟主机」和「权限」中，分别为两个租户各写一行。

::

    虚拟主机:
    tenanta
    tenantb

    权限:
    {role}tenanta_user
    {role}tenantb_user

虚拟主机和权限会在爬取时写入文档。
如果在已经爬取过的配置中修改了这些项目，在重新爬取之前不会反映到现有文档上。

保存设置后，可以在详细页面用 [创建新作业] 创建租户专用的作业，或者在 [系统] > [调度器] 中用 [立即开始] 运行 ``Default Crawler``。

步骤 5：准备租户专用的搜索页面
==============================

Fess 15.9 的搜索页面由主题显示。
安装 ``theme.yml`` 中 ``name`` 与键的小写形式相同的主题后，该键的请求就会使用该主题。
无需将其设为默认主题，与任何键都不匹配的访问会使用默认主题。

复制自带的 ``bootstrap`` 主题来制作。
使用 Docker 时，按如下方式从容器中取出。

::

    $ docker cp fess01:/usr/share/fess/app/themes/bootstrap ./tenanta

1. 将 ``tenanta/theme.yml`` 的 ``name`` 改为 ``tenanta``，``displayName`` 改为 ``A 公司搜索`` 等。
2. 替换 ``assets/styles.css``\ （配色）以及 ``assets/logo-head.png``、``assets/logo.png``\ （徽标）。``index.html`` 无需修改。
3. 打包时让 ``theme.yml`` 位于 ZIP 的根目录。

   ::

       $ cd tenanta && zip -r ../tenanta.zip .

4. 在 [系统] > [主题] 中通过 [上传] 上传 ``tenanta.zip``。

登录页面（``/login/``）为所有租户共用，无法通过主题更改。
复制自带主题的详细方法请参阅 `主题开发指南 <https://fess.codelibs.org/zh-cn/stable/dev/theme-development.html>`__。

确认隔离效果
============

在切换 DNS 之前，可以在本地的 ``/etc/hosts`` 中添加 ``127.0.0.1 search-a.example.com search-b.example.com``，然后从浏览器以 ``http://search-a.example.com:8080/`` 这样的地址试用各主机（[通用] 中需要带端口的行）。
用爬取对象中存在的词进行搜索，确认以下 4 种情况。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 访问方式
     - 预期结果
   * - 以 A 公司用户从 ``search-a.example.com`` 访问
     - 只显示 A 公司的文档。标签只有“A 公司门户”。以 A 公司的主题显示
   * - 以 A 公司用户从 ``search-b.example.com`` 访问
     - 0 条（对 B 公司的文档没有权限，A 公司的文档被虚拟主机排除）
   * - 以 A 公司用户从 IP 地址（``http://<服务器>:8080/``）访问
     - 只显示 A 公司的文档（没有虚拟主机筛选，但受权限保护）
   * - 不登录直接访问
     - 登录之前无法搜索

如果创建了两个租户共用的文档，第 1～3 行中也会显示这些文档。
如果第 3 行显示了 B 公司的文档，说明某个爬网配置中还留有 ``{role}guest``。
如果第 1 行为 0 条，请对照 [通用] 中的行（有无端口号）与爬网配置「虚拟主机」的拼写。

也可以用搜索 API 进行同样的确认。
在 [系统] > [访问令牌] 中创建权限为 ``{role}tenanta_user`` 的令牌，然后更换 ``Host`` 请求头进行调用。

::

    $ curl -s -H "Authorization: Bearer <A 公司的令牌>" \
        -H "Host: search-a.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"
    $ curl -s -H "Authorization: Bearer <A 公司的令牌>" \
        -H "Host: search-b.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"

如果第一次调用的 ``response.record_count`` 为 1 以上、第二次为 0，即符合预期。
访问令牌并不与虚拟主机绑定，虚拟主机由请求发送到的主机名决定。
决定令牌可见范围的是令牌的权限，因此交给租户系统的令牌务必只指定该租户的角色。
API 的用法请参阅 :doc:`guide-11`。

开始运营后，可以在 [系统信息] > [搜索日志] 的 [用户与环境] 选项卡中查看各虚拟主机的搜索次数。

租户的添加与删除
================

添加租户时，由于后面的步骤会用到前面步骤的值，请按以下顺序进行。

1. 在 [通用] 的「虚拟主机」中添加一行
2. 创建角色、用户，必要时创建访问令牌
3. 创建标签（带虚拟主机和权限）
4. 创建爬网配置（带虚拟主机和权限）并爬取
5. 上传主题
6. 确认“确认隔离效果”中的 4 种情况
7. 通过 DNS 和反向代理发布

删除租户时，则反过来先关闭使用入口。

1. 从 DNS 和反向代理中移除主机名
2. 删除爬网配置以及为其创建的作业（[系统] > [调度器]）
3. 从索引中删除文档（见下文）
4. 删除访问令牌、用户和角色
5. 删除标签、关键词匹配等该键的设置以及主题
6. 从 [通用] 的「虚拟主机」中删除该行

即使删除爬网配置，已爬取的文档仍会留在索引中。
文档需要在 [系统信息] > [搜索] 中删除。
该页面不会应用角色和虚拟主机的筛选，因此所有租户的文档都在操作范围内。
在搜索框中像 ``label:tenantb_docs`` 这样指定租户的标签进行搜索，确认条数和结果都只是 B 公司的文档后，再点击 [删除此查询的所有内容]。
如果是 Web 文档，也可以像 ``site:portal-b.example.com`` 这样用 URL 的开头部分指定。

请不要使用 ``virtual_host:tenantb`` 这样的指定。
``virtual_host`` 默认不在可用于搜索的字段之中，整个字符串会被当作在正文中查找该文本的搜索处理，因此无法选中想要的文档。

分开部署实例的选择
==================

在共享一个 Fess 的配置中，以下内容无法分开。

- 管理页面和管理员：任何管理员都能操作所有租户的设置、用户和文档
- [通用] 的设置、词典等整个系统的设置
- 登录页面

如果希望由各租户自行管理，或者合同上要求分开索引，请为每个租户启动一个 Fess，并使用不同的索引名称。
docker-fess 的 ``compose/multi-instance`` 是将 2 个 Fess（端口 8080 和 8081）连接到一个 OpenSearch 的配置。

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess
    $ git checkout v15.9.0
    $ cd compose/multi-instance
    $ docker compose -f compose.yaml -f compose-fess01.yaml -f compose-fess02.yaml up -d

各 Fess 的 ``FESS_JAVA_OPTS`` 中，文档、建议词、爬取、配置、用户、日志、词典的索引名称（``-Dfess.config.index.document.search.index=fess01.search`` 等 8 项）按实例分别设置。
由于配置和用户也按索引分开，管理页面、用户和搜索日志也都以租户为单位。
增加租户时，复制 ``compose-fess02.yaml``，并修改服务名、端口和所有索引名称。

.. warning::

   该配置中的 OpenSearch 在安全插件禁用的状态下公开了 9200 端口。
   能访问到 9200 端口的人可以读取所有租户的索引，因此在生产环境中请关闭该端口。

延伸阅读
========

- 想详细了解基于角色、组和 LDAP 的权限设计：:doc:`guide-05`
- 想从租户的系统调用搜索 API：:doc:`guide-11`
- 想通过 SSO 登录、保护访问：:doc:`guide-15`
- 租户增加后想扩展 Fess 和 OpenSearch：:doc:`guide-14`
- 想将搜索页面嵌入现有网站：:doc:`guide-03`

参考资料
========

- `虚拟主机 <https://fess.codelibs.org/zh-cn/stable/config/security-virtual-host.html>`__
- `多租户配置 <https://fess.codelibs.org/zh-cn/stable/config/multitenancy.html>`__
- `基于角色的搜索配置 <https://fess.codelibs.org/zh-cn/stable/config/security-role.html>`__
- `标签 <https://fess.codelibs.org/zh-cn/stable/admin/labeltype-guide.html>`__
- `主题 <https://fess.codelibs.org/zh-cn/stable/admin/theme-guide.html>`__
- `搜索 <https://fess.codelibs.org/zh-cn/stable/admin/searchlist-guide.html>`__
- `docker-fess multi-instance（v15.9.0） <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose/multi-instance>`__
