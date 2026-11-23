==================================
速率限制配置
==================================

概述
====

|Fess| 具有速率限制功能，用于维护系统的稳定性和性能。
通过此功能，可以保护系统免受过度请求的影响，实现公平的资源分配。

速率限制适用于以下场景:

- 包括搜索API和AI搜索模式API在内的所有HTTP请求（``RateLimitFilter``）
- 爬虫请求（通过爬取设置进行控制）

HTTP请求的速率限制
==========================

可以按IP地址单位限制对 |Fess| 的HTTP请求数。
此限制适用于搜索API、AI搜索模式API、管理界面等所有HTTP请求。

设置
----

``app/WEB-INF/classes/fess_config.properties``:

::

    # 启用速率限制（默认: false）
    rate.limit.enabled=true

    # 每个IP地址每个窗口的最大请求数（默认: 100）
    rate.limit.requests.per.window=100

    # 窗口大小（毫秒）（默认: 60000）
    rate.limit.window.ms=60000

行为
----

- 超过速率限制的请求返回HTTP 429 (Too Many Requests)
- 因超过限制而被阻止的IP地址，以及阻止IP列表中的IP地址的请求返回HTTP 403 (Forbidden)
- 响应体为JSON（429 为 ``{"error":"rate_limit_exceeded",...,"retry_after":60}`` ，403 为 ``{"error":"ip_blocked",...}`` ）。429 附带 ``Retry-After`` 头
- 限制按IP地址单位应用
- 每个IP从首次请求开始计算窗口，窗口期间过后计数重置（固定窗口方式）
- 超过限制时，IP会被阻止 ``rate.limit.block.duration.ms`` 的期间

AI搜索模式的速率限制
====================

AI搜索模式功能具有速率限制，用于控制LLM API的成本和资源消耗。
AI搜索模式除了上述HTTP请求速率限制外，还可以设置AI搜索模式固有的速率限制。

AI搜索模式固有的速率限制设置请参阅 :doc:`rag-chat`。

.. note::
   AI搜索模式的速率限制与LLM提供商端的速率限制分别应用。
   请同时考虑两者的限制进行设置。

爬虫的速率限制
======================

可以设置请求间隔，以避免爬虫对目标站点造成过度负载。

Web爬取设置
---------------

在管理界面的「爬虫」→「Web」中设置以下内容:

- **请求间隔**: 请求间的等待时间（毫秒）
- **线程数**: 并行爬取线程数

推荐设置:

::

    # 一般站点
    intervalTime=1000
    numOfThread=1

    # 大型站点（有授权时）
    intervalTime=500
    numOfThread=3

遵守robots.txt
----------------

|Fess| 默认遵守robots.txt的Crawl-delay指令。

::

    # robots.txt示例
    User-agent: *
    Crawl-delay: 10

robots.txt的处理由 ``app/WEB-INF/classes/fess_config.properties`` 中的 ``crawler.ignore.robots.txt`` 控制（默认值: ``false``）。
将其设置为 ``true`` 可禁用robots.txt的处理，包括Crawl-delay的遵守。

::

    # 忽略robots.txt（默认: false）
    crawler.ignore.robots.txt=false

Crawl-delay 按访问目标（源）分别应用，上限为 60 秒。等待以 URL 为单位进行，因此在增量爬取中，对同一个 URL 发送的 HEAD 和 GET 会连续发送。爬取配置的“间隔”与此分开，作为到下一个 URL 之前的等待时间生效。

robots.txt 按照 RFC 9309 解释。 ``Allow:`` 和 ``Disallow:`` 以最长匹配的规则优先，起始 URL 也会根据 robots.txt 进行检查。被 robots.txt 禁止的 URL 会以 INFO 级别记录到 ``fess-crawler.log``\ ，不会登记为故障 URL。

Request-rate
------------

从 15.10 起，|Fess| 也会遵守 robots.txt 中的 ``Request-rate`` 行和 ``Visit-time`` 行（15.9 及更早版本会忽略它们）。两者都不属于 RFC 9309，而是由 `扩展的机器人排除协议提案 <https://www.conman.org/people/spc/robots2.html>`__ 定义。SeznamBot 也使用 Request-rate（请参阅 `Seznam 文档 <https://www.napoveda.seznam.cz/en/crawling-control>`__ ）。与 Crawl-delay 一样，它们仅在 robots.txt 处理启用时生效：设置 ``crawler.ignore.robots.txt=true`` 会同时关闭这三者，没有只关闭其中一个的设置。它们不是 ``Allow:`` 或 ``Disallow:`` 规则，因此不会结束 ``User-agent`` 组，也不会改变被禁止的 URL。

``Request-rate: <文档数>/<时间>[ 单位]`` 要求爬虫在该时间内最多获取这么多文档。时间的单位为 ``s`` （秒，默认）、 ``m`` 、 ``h`` 或 ``d`` 。示例：

- ``1/10`` ：每 10 秒 1 个页面
- ``10/10m`` ：每 10 分钟 10 个页面
- ``20/1h`` ：每小时 20 个页面
- ``100/15 m`` ：每 15 分钟 100 个页面

|Fess| 会将该速率换算为两个 URL 之间的间隔（ ``1/10`` 为 10 秒， ``5/1m`` 为 12 秒），并按源（origin）分别在下一个 URL 之前等待 Crawl-delay 与 Request-rate 间隔中较长的一个。上限 60 秒同样适用于这一等待，因此像 ``1/1h`` 这样更慢的速率会被限制为 60 秒。Request-rate 控制的是 URL 之间的间隔，而不是可以一次性集中获取的额度。与 Crawl-delay 一样，源的第一个 URL 不受限速（获取它的同时才会读取 robots.txt），在增量爬取中，对同一个 URL 发送的 HEAD 和 GET 会连续发送。

速率后面可以加上时间段。这时速率只在该时间段内生效，在时间段之外 Request-rate 不设限制（Crawl-delay 仍然适用）：

::

    User-agent: *
    Request-rate: 1/10 s 1800-1900

时间为 UT/GMT（UTC）的 00:00 至 23:59，写作 ``HHMM-HHMM`` 或 ``HH:MM-HH:MM`` ，两端都包含在内。时间段可以跨越午夜（ ``2300-0100`` ）。有多行 Request-rate 时全部生效，适用其中此刻有效的最慢的一个。格式不正确的速率或时间段（例如小时超过 23、分钟超过 59）会被忽略。

Visit-time
----------

``Visit-time: HH:MM-HH:MM`` （也可写作 ``HHMM-HHMM`` ）要求爬虫只在该时间段内访问，时间为 UTC，两端都包含在内。可以写多行，此时允许的时间段为各行的并集。

::

    User-agent: *
    Visit-time: 02:00-06:00

|Fess| 不会等待时间段开始，因为那样会让爬取线程被占用数小时。在时间段之外从队列取出的该源的 URL 会被跳过，与被 ``Disallow:`` 禁止的 URL 相同：每个源以 INFO 级别记录一次，不会重新放回队列（同一次爬取中之后也不会重试），也不会计为故障。因此爬取必须在时间段内开始。在时间段开始之前从队列取出的起始 URL，即使时间段开始时爬取仍在运行，在这次爬取中也会丢失。格式不正确的 Visit-time 行会被忽略，即没有限制。

如果声明了 Visit-time 的站点的爬取作业从不在该时间段内运行，该站点就不会被爬取，已建立索引的文档也不会被刷新。在默认的“删除以前的文档”设置（ ``day.for.cleanup`` ，3 天）下，这些文档会在最后一次到达它们的爬取之后约 3 天过期，与站点停机时相同。请将爬取作业安排在该时间段内运行。

429/503 响应时的退避
--------------------

当服务器返回 ``429 Too Many Requests`` 或 ``503 Service Unavailable`` 时，会暂时停止对该源的访问，并最多重试该 URL 3 次。等待时间在有 ``Retry-After`` 头时为该值，否则为从 10 秒开始的指数增长时间（最长 5 分钟）。最后一次重试也失败时，会在 ``fess-crawler.log`` 中输出 WARN。

无法获取 robots.txt 时
----------------------

当获取 robots.txt 因 5xx、429 或超时等失败时，该源的 URL 会被放回队列，直到退避结束。首次失败后再重试 3 次仍失败时，在本次爬取期间该源的所有 URL 都不会被爬取，并会在 ``fess-crawler.log`` 中输出一次 WARN。15.8 及更早版本会将无法获取的 robots.txt 一律视为允许。要恢复该行为，请在 Web 爬取配置的“配置参数”中指定以下内容。

::

    client.robotsTxtAllowOnUnavailable=true

要完全禁用 robots.txt 处理，请使用 ``client.robotsTxtEnabled=false`` （按爬取配置）或 ``crawler.ignore.robots.txt=true``\ 。

速率限制的全部配置项
======================

``app/WEB-INF/classes/fess_config.properties`` 中可配置的所有属性。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rate.limit.enabled``
     - 启用速率限制
     - ``false``
   * - ``rate.limit.requests.per.window``
     - 每个窗口的最大请求数
     - ``100``
   * - ``rate.limit.window.ms``
     - 窗口大小（毫秒）
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - 超过限制时的IP阻止期间（毫秒）
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Retry-After响应头的值（秒）
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - 从速率限制中排除的IP地址（逗号分隔）
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - 要阻止的IP地址（逗号分隔）
     - （空）
   * - ``rate.limit.trusted.proxies``
     - 信任的代理IP（从X-Forwarded-For/X-Real-IP获取客户端IP，也用于审计日志和搜索日志中的客户端IP）
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - 清理间隔（请求数，预留）
     - ``1000``

.. note::
   ``rate.limit.cleanup.interval`` 是为将来使用而预留的设置项。
   在当前实现中，请求计数器和被阻止的IP信息会根据内部缓存过期时间（``rate.limit.window.ms`` 和 ``rate.limit.block.duration.ms``）自动清理，因此该值不会被使用。

登录次数限制
============

登录除上述限制外，还有通过 ``theme.api.login.*`` 设置的单独的次数限制。
从 15.10 起，``/api/v2/auth/login`` 与登录页面（``/login/``）的登录表单共用同一限制和锁定。
每次尝试会占用该客户端IP每分钟限额（默认值为 ``10``）中的一个名额，登录成功后会归还。
同一IP地址的尝试超过上限时，该IP地址将被锁定 ``theme.api.login.lockout.seconds`` （默认值为 ``900``）秒，在此期间即使使用正确的凭据也无法登录。
因此，如果同一IP地址在成功之前出现超过上限的尝试（例如同时登录），该地址将被锁定。
按用户的上限（ ``theme.api.login.rate.limit.per.user.per.minute`` ）按客户端 IP 地址与用户名的组合分别统计。用户名不区分大小写，因此 ``alice`` 和 ``Alice`` 合并为一个计数。用于认证和写入日志的用户名保持输入时的样子。
详情请参阅 :doc:`../api/api-auth`。

高级速率限制设置
====================

自定义速率限制
------------------

要根据特定条件应用不同的速率限制逻辑，
需要实现自定义组件。

::

    // RateLimitHelper自定义示例
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // 自定义逻辑
        }
    }

排除设置
========

可以将特定IP地址从速率限制中排除或阻止。

::

    # 白名单IP（从速率限制中排除，逗号分隔）
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # 阻止IP列表（始终阻止，逗号分隔）
    rate.limit.blocked.ips=203.0.113.50

    # 信任的代理IP（逗号分隔）
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   使用反向代理时，请将代理的IP地址设置在 ``rate.limit.trusted.proxies`` 中。
   仅从信任的代理发出的请求，才会从X-Forwarded-For和X-Real-IP头获取客户端IP。
   当 X-Forwarded-For 被拆分为多个头部行时（例如代理像 HAProxy 的 ``option forwardfor`` 那样添加自己的一行），
   15.10 及以后版本会按接收顺序连接所有行，从右向左读取，并将第一个不是信任代理的地址作为客户端IP。
   15.9 及之前只读取第一行，即客户端发送的那一行。

监控与告警
==============

用于监控速率限制状况的设置:

日志输出
--------

应用速率限制时，会记录在日志中:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

该消息以 INFO 级别输出，因此默认日志级别（``warn``）不会写出。请将上面的 ``Logger`` 添加到 ``log4j2.xml``\ （位置参见 :doc:`admin-logging`），或将 ``FESS_LOG_LEVEL`` 设为 ``info``。

故障排除
======================

正常请求被阻止
--------------------------------

**原因**: 限制值过于严格

**解决方法**:

1. 增加 ``rate.limit.requests.per.window``
2. 将特定IP添加到白名单（``rate.limit.whitelist.ips``）
3. 调整窗口大小（``rate.limit.window.ms``）

速率限制不生效
--------------------

**原因**: 设置未正确生效

**确认事项**:

1. 是否设置了 ``rate.limit.enabled=true``
2. 配置文件是否正确加载
3. 是否重启了 |Fess|

性能影响
----------------------

速率限制检查本身影响性能时:

1. 利用白名单跳过信任IP的检查
2. 禁用速率限制（``rate.limit.enabled=false``）

参考信息
========

- :doc:`rag-chat` - AI搜索模式功能配置
- :doc:`../admin/webconfig-guide` - Web爬取配置指南
- :doc:`../api/api-overview` - API概述
